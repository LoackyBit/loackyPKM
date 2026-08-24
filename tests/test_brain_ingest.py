import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_ingest

class TestBrainIngest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Clipboard"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_per_note_lock_concurrency(self):
        """Asserts NoteLock(identifier) creates /tmp/brain_ingest_<sha256>.lock atomically
        and prevents duplicate runs for the same source while allowing distinct sources to run concurrently per D-12.
        """
        source_a = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        source_b = "https://youtube.com/watch?v=9bZkp7q19f0"

        with brain_ingest.NoteLock(source_a) as lock_a:
            self.assertTrue(lock_a.acquired)
            self.assertTrue(os.path.exists(lock_a.lock_file))

            # Attempt duplicate lock on source_a -> must raise RuntimeError
            with self.assertRaises(RuntimeError):
                with brain_ingest.NoteLock(source_a):
                    pass

            # Concurrent lock on distinct source_b -> must succeed
            with brain_ingest.NoteLock(source_b) as lock_b:
                self.assertTrue(lock_b.acquired)
                self.assertTrue(os.path.exists(lock_b.lock_file))

        # After exiting context, lock files must be cleaned up
        self.assertFalse(os.path.exists(lock_a.lock_file))

    def test_polymorphic_input_detection(self):
        """Asserts detect_input_type correctly identifies YouTube URLs, Web URLs, pasted text, and local files per D-05."""
        yt_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        for url in yt_urls:
            self.assertEqual(brain_ingest.detect_input_type(url), "youtube")

        web_urls = [
            "https://arxiv.org/abs/2303.08774",
            "http://example.com/article/react-state"
        ]
        for url in web_urls:
            self.assertEqual(brain_ingest.detect_input_type(url), "web")

        # Create local file in Inbox
        local_file = os.path.join(self.test_dir, "03 - Inbox", "raw_notes.md")
        with open(local_file, "w", encoding="utf-8") as f:
            f.write("# Appunti\nTesto.")
        self.assertEqual(brain_ingest.detect_input_type(local_file), "file")

        # Free text
        raw_text = "Ecco alcuni appunti sparsi presi durante la conferenza sul deep learning..."
        self.assertEqual(brain_ingest.detect_input_type(raw_text), "text")

    def test_contextual_autolinking(self):
        """Asserts autolink_content scans real vault titles, wraps occurrences in [[Target Note]]
        (max 2 per target), and populates related: ['[[Target Note]]'] and ## Collegamenti per D-07.
        """
        # Create target notes in test vault
        note1 = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Prompt Engineering.md")
        with open(note1, "w", encoding="utf-8") as f:
            f.write("# Prompt Engineering\nContent.")

        note2 = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Reti Neurali.md")
        with open(note2, "w", encoding="utf-8") as f:
            f.write("# Reti Neurali\nContent.")

        raw_body = """# Nuova Nota

Questo studio introduce le basi di Prompt Engineering per modelli avanzati.
Inoltre, confrontiamo l'approccio con le Reti Neurali e discutiamo ancora di Prompt Engineering nel dettaglio.
Anche una terza menzione di Prompt Engineering non dovrebbe superare il cap.
"""
        linked_body, links = brain_ingest.autolink_content(self.test_dir, raw_body, "Nuova Nota")
        self.assertIn("[[Prompt Engineering]]", linked_body)
        self.assertIn("[[Reti Neurali]]", linked_body)
        self.assertIn("[[Prompt Engineering]]", links)
        self.assertIn("[[Reti Neurali]]", links)

        # Max 2 occurrences check
        occurrences = linked_body.count("[[Prompt Engineering]]")
        self.assertEqual(occurrences, 2)

    def test_style_guide_highlight_sanitization(self):
        """Asserts sanitize_style_highlights strips markdown backticks from <mark> and <font> tags per D-10."""
        dirty = """Qui abbiamo `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>` con backticks.
Ed anche `<font color="#8a5cf6"><b>secondario</b></font>` con backticks.
"""
        cleaned = brain_ingest.sanitize_style_highlights(dirty)
        self.assertNotIn("`<mark", cleaned)
        self.assertNotIn("`</mark>`", cleaned)
        self.assertNotIn("`<font", cleaned)
        self.assertIn('<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>', cleaned)
        self.assertIn('<font color="#8a5cf6"><b>secondario</b></font>', cleaned)

    def test_staging_and_review_dashboard_tri_state(self):
        """Asserts staging notes are written to 03 - Inbox/<Title>.md with status: draft,
        registered in 03 - Inbox/Review Dashboard.md, and process_tri_state_approvals promotes
        [x] to status: permanent (moving to target) or deletes draft on [-] per D-06, D-11.
        """
        # 1. Stage a note
        title = "Guida Architetture LLM"
        body = "Corpo della nota di prova per architetture transformer."
        meta = {
            "title": title,
            "type": "concept",
            "area": "tech",
            "source": "original",
            "date": "2026-08-25",
            "tags": ["tech/ai", "tech/llm"],
            "summary": "Guida introduttiva ai modelli linguistici transformer."
        }
        staged_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=title,
            body=body,
            metadata=meta,
            target_dir="02 - Atlas/Tech"
        )
        self.assertTrue(os.path.exists(staged_path))
        with open(staged_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("status: draft", content)
        self.assertIn("[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Guida Architetture LLM]]", content)

        # Check Review Dashboard
        dashboard_file = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        self.assertTrue(os.path.exists(dashboard_file))
        with open(dashboard_file, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("- [ ] Approva [[Guida Architetture LLM]]", dash_content)

        # 2. Simulate User Approval [x]
        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(dash_content.replace("- [ ] Approva [[Guida Architetture LLM]]", "- [x] Approva [[Guida Architetture LLM]]"))

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 1)

        # Staged note moved to 02 - Atlas/Tech/
        promoted_path = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Guida Architetture LLM.md")
        self.assertTrue(os.path.exists(promoted_path))
        self.assertFalse(os.path.exists(staged_path))

        with open(promoted_path, "r", encoding="utf-8") as f:
            promoted_content = f.read()
        self.assertIn("status: permanent", promoted_content)
        self.assertIn("[[Home MOC|Home]] / [[Tech]] / [[Guida Architetture LLM]]", promoted_content)

        # 3. Simulate User Rejection [-] for a second note
        rej_title = "Nota da Rifiutare"
        staged_rej = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=rej_title,
            body="Bozza da scartare.",
            metadata={"title": rej_title, "area": "tech"},
            target_dir="02 - Atlas/Tech"
        )
        self.assertTrue(os.path.exists(staged_rej))

        with open(dashboard_file, "r", encoding="utf-8") as f:
            dash_content = f.read()
        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(dash_content.replace(f"- [ ] Approva [[{rej_title}]]", f"- [-] Approva [[{rej_title}]]"))

        processed_rej = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed_rej, 1)
        self.assertFalse(os.path.exists(staged_rej))

    def test_processing_depth_modes(self):
        """Asserts format_ingest_note produces appropriate structures for executive vs deep modes per D-08."""
        raw_text = "Descrizione dei concetti e architetture chiave dei moderni modelli di deep learning."
        
        exec_note = brain_ingest.format_structured_note(
            title="Sintesi Deep Learning",
            raw_content=raw_text,
            depth="executive",
            source_type="text",
            source_url="original"
        )
        self.assertIn("## 🎯 Sintesi Esecutiva", exec_note)
        self.assertIn("## 🔑 Concetti Chiave & Takeaway", exec_note)

        deep_note = brain_ingest.format_structured_note(
            title="Approfondimento Deep Learning",
            raw_content=raw_text,
            depth="deep",
            source_type="text",
            source_url="original"
        )
        self.assertIn("## 🏛️ Quadro Concettuale & Fondamenti", deep_note)
        self.assertIn("## ⚙️ Meccanica & Architettura di Dettaglio", deep_note)
        self.assertIn("## 🔬 Analisi Critica, Limiti & Casi d'Uso", deep_note)

if __name__ == "__main__":
    unittest.main()
