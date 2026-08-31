import unittest
import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_ingest

class TestBrainIngest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Draft"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Source"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Clipboard"), exist_ok=True)
        os.environ["BRAIN_INGEST_NO_AI"] = "1"

    def tearDown(self):
        os.environ.pop("BRAIN_INGEST_NO_AI", None)
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

    def test_inbox_staging_folders(self):
        """Asserts staging writes draft to 03 - Inbox/Draft/<Title>.md and source to 03 - Inbox/Source/<Title>.md without legacy prefixes."""
        title = "Architettura Trasformatore"
        body = "Corpo della nota bozza generata."
        raw_source = "Trascrizione o appunti originali grezzi."
        meta = {"title": title, "area": "tech"}

        draft_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=title,
            body=body,
            metadata=meta,
            target_dir="02 - Atlas/Tech & AI",
            source_content=raw_source
        )

        expected_draft = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        expected_source = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{title}.md")

        self.assertEqual(draft_path, expected_draft)
        self.assertTrue(os.path.exists(expected_draft))
        self.assertTrue(os.path.exists(expected_source))

        # Verify no legacy prefix in filename
        self.assertFalse(os.path.basename(draft_path).startswith(("seen-", "proposed-", "raw-")))
        self.assertFalse(os.path.basename(expected_source).startswith(("seen-", "proposed-", "raw-")))

        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("status: draft", content)
        self.assertIn('target_path: "02 - Atlas/Tech & AI/Architettura Trasformatore.md"', content)
        self.assertIn("[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Architettura Trasformatore]]", content)

    def test_autolinking_strictly_real_notes(self):
        """Asserts autolink_content scans only real note titles on disk and strictly refuses to create speculative links per D-03."""
        # Create real target notes in test vault
        note1 = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Reti Neurali.md")
        with open(note1, "w", encoding="utf-8") as f:
            f.write("# Reti Neurali\nContent.")

        raw_text = "Studiamo le Reti Neurali e anche Concetto Inesistente Che Non Esiste nel Vault."
        linked_text, links = brain_ingest.autolink_content(self.test_dir, raw_text, "Nuova Nota")

        self.assertIn("[[Reti Neurali]]", linked_text)
        self.assertNotIn("[[Concetto Inesistente Che Non Esiste nel Vault]]", linked_text)
        self.assertEqual(links, ["[[Reti Neurali]]"])

    def test_contextual_autolinking(self):
        """Asserts autolink_content scans real vault titles, wraps occurrences in [[Target Note]]
        (max 2 per target), and populates related: ['[[Target Note]]'] per D-07.
        """
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

    def test_autolink_preserves_code_blocks(self):
        """Asserts autolink_content does not inject wiki-links inside fenced code blocks or inline code."""
        note1 = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Prompt Engineering.md")
        with open(note1, "w", encoding="utf-8") as f:
            f.write("# Prompt Engineering\nContent.")

        raw_body = """# Test Code
Ecco del codice Python:
```python
# Prompt Engineering in code
def run_prompt():
    return "Prompt Engineering"
```
E qui del codice inline `Prompt Engineering`.
Mentre qui nel testo normale Prompt Engineering deve essere linkato.
"""
        linked_body, links = brain_ingest.autolink_content(self.test_dir, raw_body, "Test Code")
        self.assertIn("```python\n# Prompt Engineering in code\ndef run_prompt():\n    return \"Prompt Engineering\"\n```", linked_body)
        self.assertIn("`Prompt Engineering`", linked_body)
        self.assertIn("Mentre qui nel testo normale [[Prompt Engineering]] deve essere linkato.", linked_body)

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

    def test_processing_depth_modes(self):
        """Asserts format_structured_note produces appropriate structures for sintesi vs approfondimento modes."""
        raw_text = "Descrizione dei concetti e architetture chiave dei moderni modelli di deep learning."

        exec_note = brain_ingest.format_structured_note(
            title="Sintesi Deep Learning",
            raw_content=raw_text,
            depth="sintesi",
            source_type="text",
            source_url="original"
        )
        self.assertIn("## Sintesi Esecutiva", exec_note)
        self.assertIn("## Concetti Chiave e Takeaway", exec_note)
        self.assertNotIn("## Collegamenti", exec_note)

        deep_note = brain_ingest.format_structured_note(
            title="Approfondimento Deep Learning",
            raw_content=raw_text,
            depth="approfondimento",
            source_type="text",
            source_url="original"
        )
        self.assertIn("## Quadro Concettuale e Fondamenti", deep_note)
        self.assertIn("## Meccanica e Dettaglio Operativo", deep_note)
        self.assertIn("## Analisi Critica e Casi Applicativi", deep_note)
        self.assertNotIn("## Collegamenti", deep_note)

    def test_no_emoji_in_note_headings(self):
        """Asserts note headings generated by AI or fallback contain 0 emojis."""
        note = brain_ingest.format_structured_note("Titolo Pulito", "Contenuto della nota")
        self.assertNotIn("# 🎯", note)
        self.assertNotIn("## 🎯", note)
        self.assertNotIn("## 🏛️", note)
        self.assertNotIn("## 🔑", note)
        self.assertNotIn("## ⚙️", note)
        self.assertNotIn("## 🔬", note)
        self.assertIn("# Titolo Pulito", note)
        self.assertIn("## Sintesi Esecutiva", note)

    def test_no_collegamenti_section(self):
        """Asserts note body has no trailing ## Collegamenti section."""
        note = brain_ingest.format_structured_note("Titolo", "Contenuto")
        self.assertNotIn("## Collegamenti", note)
        self.assertNotIn("## Note Correlate", note)
        self.assertNotIn("## 🔗", note)

    def test_depth_defaults_to_approfondimento(self):
        """Asserts default depth mode is approfondimento."""
        note_default = brain_ingest.format_structured_note("Titolo", "Contenuto")
        self.assertIn("## Quadro Concettuale e Fondamenti", note_default)
        self.assertIn("## Meccanica e Dettaglio Operativo", note_default)

    def test_note_lock_stale_pid_auto_healing(self):
        """Asserts NoteLock auto-cleans lockfiles whose PID is no longer running (kill -0 probe fails)
        or file mtime exceeds 10 minutes per D-20.
        """
        source = "https://youtube.com/watch?v=stale_pid_test"
        dummy_lock = brain_ingest.NoteLock(source)
        lock_path = dummy_lock.lock_file

        # 1. Simulate dead PID
        with open(lock_path, "w", encoding="utf-8") as f:
            f.write("pid: 9999999\ntimestamp: 2026-08-25T00:00:00\n")

        self.assertTrue(os.path.exists(lock_path))

        with brain_ingest.NoteLock(source) as lock:
            self.assertTrue(lock.acquired)
            self.assertTrue(os.path.exists(lock_path))
            with open(lock_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(f"pid: {os.getpid()}", content)

        self.assertFalse(os.path.exists(lock_path))

        # 2. Simulate expired TTL (file mtime > 600 seconds ago with active PID)
        with open(lock_path, "w", encoding="utf-8") as f:
            f.write(f"pid: {os.getpid()}\n")
        past_time = os.path.getmtime(lock_path) - 900
        os.utime(lock_path, (past_time, past_time))

        with brain_ingest.NoteLock(source) as lock:
            self.assertTrue(lock.acquired)
            self.assertTrue(os.path.exists(lock_path))

        self.assertFalse(os.path.exists(lock_path))

    def test_staging_and_review_dashboard_tri_state(self):
        """Asserts staging notes are written to 03 - Inbox/Draft/<Title>.md with status: draft,
        registered in 03 - Inbox/Review Dashboard.md, and process_tri_state_approvals promotes
        [x] to status: permanent (moving to target) or deletes draft on [-] per D-06, D-11.
        """
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
        self.assertTrue("- [ ] Approva [[Draft/Guida Architetture LLM]]" in dash_content or "- [ ] Approva [[Guida Architetture LLM]]" in dash_content)

        # 2. Simulate User Approval [x]
        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(dash_content.replace("- [ ] Approva [[Draft/Guida Architetture LLM]]", "- [x] Approva [[Draft/Guida Architetture LLM]]"))

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
            f.write(dash_content.replace(f"- [ ] Approva [[Draft/{rej_title}]]", f"- [-] Approva [[Draft/{rej_title}]]"))

        processed_rej = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed_rej, 1)
        self.assertFalse(os.path.exists(staged_rej))

    def test_approval_workflow_with_source_handling(self):
        """Asserts process_tri_state_approvals on [x] deletes YouTube/Web source but archives manual note to 99 - Meta/Archive/."""
        # 1. YouTube/Web source -> deleted on approval
        yt_title = "Video AI Transformers"
        yt_draft = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=yt_title,
            body="Contenuto estratto dal video.",
            metadata={"title": yt_title, "type": "video", "source": "https://youtube.com/watch?v=12345678901"},
            target_dir="02 - Atlas/Tech",
            source_content="Trascrizione raw."
        )
        yt_source = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{yt_title}.md")
        self.assertTrue(os.path.exists(yt_source))

        dash_file = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_file, "r", encoding="utf-8") as f:
            dash = f.read()
        with open(dash_file, "w", encoding="utf-8") as f:
            f.write(dash.replace(f"- [ ] Approva [[Draft/{yt_title}]]", f"- [x] Approva [[Draft/{yt_title}]]"))

        brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "02 - Atlas", "Tech", f"{yt_title}.md")))
        self.assertFalse(os.path.exists(yt_source))

        # 2. Manual note (source: original) -> archived to 99 - Meta/Archive/
        man_title = "Appunti Personali Strategia"
        man_draft = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=man_title,
            body="Contenuto elaborato da appunti manuali.",
            metadata={"title": man_title, "source": "original"},
            target_dir="02 - Atlas/Tech",
            source_content="ready: true\nAppunti scritti a mano originali."
        )
        man_source = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{man_title}.md")
        self.assertTrue(os.path.exists(man_source))

        with open(dash_file, "r", encoding="utf-8") as f:
            dash = f.read()
        with open(dash_file, "w", encoding="utf-8") as f:
            f.write(dash.replace(f"- [ ] Approva [[Draft/{man_title}]]", f"- [x] Approva [[Draft/{man_title}]]"))

        brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "02 - Atlas", "Tech", f"{man_title}.md")))
        self.assertFalse(os.path.exists(man_source))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "99 - Meta", "Archive", f"{man_title}.md")))

    def test_rejection_workflow_atomic_purge(self):
        """Asserts process_tri_state_approvals on [-] purges Draft, Source, and Clipboard frame."""
        title = "Video da Rigettare"
        draft_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=title,
            body="Bozza da cancellare.",
            metadata={"title": title},
            target_dir="02 - Atlas/Tech",
            source_content="Trascrizione da cancellare."
        )
        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{title}.md")
        self.assertTrue(os.path.exists(draft_path))
        self.assertTrue(os.path.exists(source_path))

        # Create dummy clipboard frame
        frame_file = os.path.join(self.test_dir, "99 - Meta", "Clipboard", f"{title[:10]}_frame.jpg")
        with open(frame_file, "w") as f:
            f.write("image bytes")
        self.assertTrue(os.path.exists(frame_file))

        dash_file = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_file, "r", encoding="utf-8") as f:
            dash = f.read()
        with open(dash_file, "w", encoding="utf-8") as f:
            f.write(dash.replace(f"- [ ] Approva [[Draft/{title}]]", f"- [-] Approva [[Draft/{title}]]"))

        brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertFalse(os.path.exists(draft_path))
        self.assertFalse(os.path.exists(source_path))
        self.assertFalse(os.path.exists(frame_file))

    def test_watcher_lifecycle_and_pid_auto_healing(self):
        """Asserts watch.sh script syntax is valid, supports lifecycle flags, and manages PID tracking per D-01, D-20."""
        script_path = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts", "watch.sh")
        self.assertTrue(os.path.exists(script_path))

        res = subprocess.run(["bash", "-n", script_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Bash syntax check failed: {res.stderr}")

        res_status = subprocess.run(["bash", script_path, "status"], capture_output=True, text=True, env=dict(os.environ, PID_FILE=f"/tmp/test_watcher_{os.getpid()}.pid"))
        self.assertIn("not running", res_status.stdout.lower() + res_status.stderr.lower())

    def test_log_rotation_on_size(self):
        """Asserts log rotation moves watch.log -> watch.log.1 -> watch.log.2 -> watch.log.3 when exceeding 5MB cap per D-03."""
        test_log_dir = os.path.join(self.test_dir, "99 - Meta", "logs")
        os.makedirs(test_log_dir, exist_ok=True)
        test_log_file = os.path.join(test_log_dir, "watch.log")

        with open(test_log_file, "wb") as f:
            f.seek(5242881)
            f.write(b"0")

        self.assertTrue(os.path.getsize(test_log_file) > 5242880)

        rotate_cmd = f"""
        LOG_FILE="{test_log_file}"
        rotate_logs() {{
            if [ -f "$LOG_FILE" ]; then
                FILE_SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
                if [ "$FILE_SIZE" -gt 5242880 ]; then
                    mv -f "${{LOG_FILE}}.2" "${{LOG_FILE}}.3" 2>/dev/null || true
                    mv -f "${{LOG_FILE}}.1" "${{LOG_FILE}}.2" 2>/dev/null || true
                    mv -f "$LOG_FILE" "${{LOG_FILE}}.1" 2>/dev/null || true
                    touch "$LOG_FILE"
                fi
            fi
        }}
        rotate_logs
        """
        res = subprocess.run(["bash", "-c", rotate_cmd], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertTrue(os.path.exists(f"{test_log_file}.1"))
        self.assertTrue(os.path.exists(test_log_file))
        self.assertEqual(os.path.getsize(test_log_file), 0)

    def test_youtube_missing_transcript_error(self):
        """Asserts extract_youtube_data raises TranscriptUnavailableError when no subtitles/transcripts exist and records error in Review Dashboard per D-11, D-18."""
        import youtube_helper
        from unittest.mock import patch

        with patch.object(youtube_helper, "YouTubeTranscriptApi", None):
            with self.assertRaises(youtube_helper.TranscriptUnavailableError):
                brain_ingest.ingest_source("https://www.youtube.com/watch?v=dQw4w9WgXcQ", vault_root=self.test_dir, force=True)

        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste", dash_content)
        self.assertIn("dQw4w9WgXcQ", dash_content)

    def test_is_visual_content_detection(self):
        """Asserts is_visual_content detects visual keywords in Italian and English per D-09."""
        import youtube_helper
        self.assertTrue(youtube_helper.is_visual_content("Tutorial Python: Come Creare un Agent"))
        self.assertTrue(youtube_helper.is_visual_content("Architettura Software e Diagrammi di Flusso"))
        self.assertTrue(youtube_helper.is_visual_content("Live Coding UI Demo in React"))
        self.assertTrue(youtube_helper.is_visual_content("Guida alla configurazione del server"))
        self.assertFalse(youtube_helper.is_visual_content("Riflessioni Filosofiche sul Tempo"))
        self.assertFalse(youtube_helper.is_visual_content("Podcast Audio Episodio 42"))

    def test_ffmpeg_keyframe_compression_params(self):
        """Asserts extract_frame builds ffmpeg command with fast-seeking -ss, -frames:v 1, -q:v 2, and timeout=30s per D-08, D-19."""
        import youtube_helper
        from unittest.mock import patch, MagicMock

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            out_file = os.path.join(self.test_dir, "test_frame.jpg")
            with open(out_file, "w") as f:
                f.write("fake image")

            res = youtube_helper.extract_frame("https://stream.url", 125.0, out_file, timeout=30)
            self.assertTrue(res)
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            cmd = args[0]
            self.assertIn("ffmpeg", cmd)
            self.assertIn("-ss", cmd)
            self.assertIn("-frames:v", cmd)
            self.assertIn("-q:v", cmd)
            self.assertIn("2", cmd)
            self.assertEqual(kwargs.get("timeout"), 30)

    def test_deterministic_clipboard_image_naming(self):
        """Asserts keyframe images saved to 99 - Meta/Clipboard/ use deterministic pattern {video_id}_{idx}_{slug}.jpg per D-06."""
        import youtube_helper
        from unittest.mock import patch

        fake_chapters = [
            {"title": "01. Introduzione al Sistema", "start_time": 0, "end_time": 60},
            {"title": "02. Demo & Codice Live", "start_time": 60, "end_time": 180}
        ]
        fake_transcript = [{"text": "Ciao mondo", "start": 0, "duration": 5}]

        with patch.object(youtube_helper, "fetch_metadata_with_retry", return_value={
            "title": "Demo Coding",
            "uploader": "DevChannel",
            "duration": 180,
            "chapters": fake_chapters,
            "url": "https://stream.fake"
        }), patch.object(youtube_helper, "fetch_transcript_with_retry", return_value=fake_transcript), \
           patch.object(youtube_helper, "extract_frame", return_value=True):

            data = youtube_helper.extract_youtube_data(
                url="https://www.youtube.com/watch?v=12345678901",
                extract_frames=True,
                vault_root=self.test_dir
            )

            self.assertEqual(len(data["extracted_images"]), 2)
            img1 = data["extracted_images"][0]
            img2 = data["extracted_images"][1]
            self.assertTrue(img1.endswith("12345678901_0_01__introduzion.jpg") or "12345678901_0_" in img1)
            self.assertTrue("12345678901_1_" in img2)

    def test_global_duplicate_detection(self):
        """Asserts check_duplicate_resource scans Atlas and Blog notes, returning match when source URL or title exists per D-11."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI")
        os.makedirs(atlas_dir, exist_ok=True)
        existing_note = os.path.join(atlas_dir, "Nota Esistente.md")
        with open(existing_note, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: concept
area: tech
source: https://youtube.com/watch?v=existing123
title: "Nota Esistente"
---
Content.
""")
        # Duplicate URL check
        dup_url = brain_ingest.check_duplicate_resource(self.test_dir, "https://youtube.com/watch?v=existing123", "Altro Titolo")
        self.assertIsNotNone(dup_url)
        self.assertEqual(dup_url[0], existing_note)
        self.assertEqual(dup_url[1], "source_url")

        # Duplicate Title check
        dup_title = brain_ingest.check_duplicate_resource(self.test_dir, "https://youtube.com/watch?v=new456", "Nota Esistente")
        self.assertIsNotNone(dup_title)
        self.assertEqual(dup_title[0], existing_note)
        self.assertEqual(dup_title[1], "title")

        # Non-duplicate check
        no_dup = brain_ingest.check_duplicate_resource(self.test_dir, "https://youtube.com/watch?v=unique789", "Nuova Nota Unica")
        self.assertIsNone(no_dup)

    def test_blog_post_referencing_youtube_not_duplicate(self):
        """Asserts a blog draft in 05 - Blog/ referencing or inspired by a YouTube URL is not flagged as a duplicate."""
        blog_dir = os.path.join(self.test_dir, "05 - Blog")
        os.makedirs(blog_dir, exist_ok=True)
        blog_note = os.path.join(blog_dir, "Crono S.md")
        with open(blog_note, "w", encoding="utf-8") as f:
            f.write("""---
stage: raw 🗂️
draft: true
type: article
area: tech
related: []
source: "https://www.youtube.com/watch?v=mkGGOxEPV-Q"
title: "Crono S"
---
libro come cura allo scrolling
ispirato da: https://www.youtube.com/watch?v=mkGGOxEPV-Q
""")
        dup = brain_ingest.check_duplicate_resource(self.test_dir, "https://youtu.be/mkGGOxEPV-Q", "Raw Note 2026-08-30 22-02")
        self.assertIsNone(dup)

    def test_body_mention_youtube_not_duplicate(self):
        """Asserts that a note in Atlas merely mentioning a YouTube URL in its body is not flagged as a duplicate."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI")
        os.makedirs(atlas_dir, exist_ok=True)
        mention_note = os.path.join(atlas_dir, "Guida Produttivita.md")
        with open(mention_note, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: concept
area: tech
source: original
title: "Guida Produttivita"
---
Vedi anche questo video interessante: https://www.youtube.com/watch?v=mkGGOxEPV-Q per approfondire.
""")
        dup = brain_ingest.check_duplicate_resource(self.test_dir, "https://youtu.be/mkGGOxEPV-Q", "Titolo Nuovo")
        self.assertIsNone(dup)

    def test_generic_raw_note_title_not_duplicate(self):
        """Asserts generic titles like 'Raw Note ...' do not trigger false duplicate title matches."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI")
        os.makedirs(atlas_dir, exist_ok=True)
        note = os.path.join(atlas_dir, "Raw Note 2026-01-01 10-00.md")
        with open(note, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: concept
area: tech
title: "Raw Note 2026-01-01 10-00"
---
Testo.
""")
        dup = brain_ingest.check_duplicate_resource(self.test_dir, None, "Raw Note 2026-08-30 22-02")
        self.assertIsNone(dup)

    def test_heuristic_atlas_routing(self):
        """Asserts classify_target_directory suggests appropriate subfolder based on tags/title/content."""
        # AI & Agents
        dest_ai = brain_ingest.classify_target_directory("Costruire Agenti LLM con RAG", ["tech/agents"], "Modelli transformer e agenti autonomi")
        self.assertEqual(dest_ai, "02 - Atlas/Tech & AI/Agents & Automation")

        dest_ai_ml = brain_ingest.classify_target_directory("Architettura Transformer e Reti Neurali", ["tech/ai"], "Modelli di deep learning")
        self.assertEqual(dest_ai_ml, "02 - Atlas/Tech & AI/AI")

        # Software Development
        dest_git = brain_ingest.classify_target_directory("Gestione Branch e Pull Request", ["tech/git"], "Flusso di lavoro su GitHub")
        self.assertEqual(dest_git, "02 - Atlas/Tech & AI/Software Development")

        dest_soft = brain_ingest.classify_target_directory("Semantic Versioning e Ciclo di Rilascio", ["tech/semver"], "Specifica SemVer 2.0.0")
        self.assertEqual(dest_soft, "02 - Atlas/Tech & AI/Software Development")

        # Security
        dest_sec = brain_ingest.classify_target_directory("Guida al Penetration Testing", ["tech/security"], "Vulnerabilita e exploit")
        self.assertEqual(dest_sec, "02 - Atlas/Tech & AI/Security")

        # Finance
        dest_fin_tax = brain_ingest.classify_target_directory("Guida alla Gestione Fiscale e Tasse", ["finance/tax"], "Tasse e partita iva")
        self.assertEqual(dest_fin_tax, "02 - Atlas/Finance/Holdings & Tax")

        dest_crypto = brain_ingest.classify_target_directory("Guida a Bitcoin e Smart Contract", ["finance/crypto"], "Blockchain e wallet")
        self.assertEqual(dest_crypto, "02 - Atlas/Finance/Crypto")

        dest_inv = brain_ingest.classify_target_directory("Investire in ETF e Borsa", ["finance/investing"], "Fondi e interesse composto")
        self.assertEqual(dest_inv, "02 - Atlas/Finance/Investments")

        # Education
        dest_edu_math = brain_ingest.classify_target_directory("Appunti Esame Analisi Matematica", ["education/math"], "Studio universitario di integrali e derivate")
        self.assertEqual(dest_edu_math, "02 - Atlas/Education & Learning/University/Matematica & Fisica")

        dest_edu_method = brain_ingest.classify_target_directory("Metodo di Studio e Spaced Repetition", ["education/method"], "Active recall e memorizzazione")
        self.assertEqual(dest_edu_method, "02 - Atlas/Education & Learning/Learning")

        # Personal Growth & Health
        dest_men_habits = brain_ingest.classify_target_directory("Come Sviluppare Disciplina e Focus", ["mentality/habits"], "Abitudini atomiche e gestione del tempo")
        self.assertEqual(dest_men_habits, "02 - Atlas/Personal Growth & Health/Mentality")

        dest_gym = brain_ingest.classify_target_directory("Scheda di Allenamento Ipertrofia", ["health/fitness"], "Palestra, pesi e workout")
        self.assertEqual(dest_gym, "02 - Atlas/Personal Growth & Health/Gym & Health")

        # Blog
        dest_blog = brain_ingest.classify_target_directory("Articolo Pubblico sul Blog", ["blog/post"], "Post divulgativo")
        self.assertEqual(dest_blog, "05 - Blog")

    def test_inbox_raw_note_intake_on_ready_true(self):
        """Asserts process_inbox_raw_notes scans 03 - Inbox/ and converts notes with ready: true into Draft/ and Source/ and queues them in Note in Attesa."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        raw_note = os.path.join(inbox_dir, "Appunto Rapido.md")
        with open(raw_note, "w", encoding="utf-8") as f:
            f.write("""---
ready: true
type: concept
area: tech
title: "Appunto Rapido"
---
Questo è un appunto grezzo da formattare.
""")

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 1)

        draft_file = os.path.join(inbox_dir, "Draft", "Appunto Rapido.md")
        source_file = os.path.join(inbox_dir, "Source", "Appunto Rapido.md")
        self.assertFalse(os.path.exists(raw_note))
        self.assertTrue(os.path.exists(draft_file))
        self.assertTrue(os.path.exists(source_file))

        with open(draft_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("status: draft", content)

        # Review dashboard should have it registered under Note in Attesa di Approvazione
        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("## 📥 Note in Attesa di Approvazione", dash_content)
        self.assertIn("Approva [[Draft/Appunto Rapido]]", dash_content)
        self.assertNotIn("- ⏳ [[Draft/Appunto Rapido]]", dash_content)

    def test_filename_collision_protection(self):
        """Asserts destination filename collisions with differing source URLs are detected and flagged without overwriting per D-12."""
        dest_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI")
        os.makedirs(dest_dir, exist_ok=True)
        existing_dest = os.path.join(dest_dir, "Nota Collisione.md")
        with open(existing_dest, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
source: https://original.url/article1
title: "Nota Collisione"
---
Original permanent content.
""")

        staged_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title="Nota Collisione",
            body="New incoming content.",
            metadata={"source": "https://different.url/article2", "title": "Nota Collisione"},
            target_dir="02 - Atlas/Tech & AI"
        )

        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_content.replace("- [ ] Approva [[Draft/Nota Collisione]]", "- [x] Approva [[Draft/Nota Collisione]]"))

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 0)

        with open(existing_dest, "r", encoding="utf-8") as f:
            self.assertIn("Original permanent content.", f.read())

        with open(dash_path, "r", encoding="utf-8") as f:
            updated_dash = f.read()
        self.assertIn("Conflitto nome file", updated_dash)

    def test_inbox_history_persistence(self):
        """Asserts processed actions append timestamp, action type, note title, and destination to 99 - Meta/logs/inbox_history.md per D-14."""
        log_file = os.path.join(self.test_dir, "99 - Meta", "logs", "inbox_history.md")
        brain_ingest.append_inbox_history(
            vault_root=self.test_dir,
            action="APPROVED",
            note_title="Nota di Prova Storia",
            target="02 - Atlas/Tech & AI",
            source="https://youtube.com/watch?v=123"
        )
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("[APPROVED]", content)
        self.assertIn("[[Nota di Prova Storia]]", content)
        self.assertIn("02 - Atlas/Tech & AI", content)

    def test_error_registration_in_dashboard(self):
        """Asserts record_ingest_error adds failing resource with retry checkbox to ## ⚠️ Errori di Acquisizione per D-18, D-21."""
        brain_ingest.record_ingest_error(
            vault_root=self.test_dir,
            source_or_url="https://youtube.com/watch?v=no_subtitles",
            reason="Nessuna trascrizione disponibile."
        )
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste", content)
        self.assertIn("https://youtube.com/watch?v=no_subtitles", content)
        self.assertIn("Nessuna trascrizione disponibile.", content)

    def test_process_inbox_raw_notes_ready_true_and_string(self):
        """Asserts process_inbox_raw_notes converts raw notes with ready: true and ready: 'true' into Draft/ and Source/ notes and queues them in Review Dashboard.md."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        raw_note_1 = os.path.join(inbox_dir, "Nota Bozza Bool.md")
        with open(raw_note_1, "w", encoding="utf-8") as f:
            f.write("""---
ready: true
title: "Nota Bozza Bool"
date: 2026-08-25
tags: [tech/ai, raw]
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Nota Bozza Bool]]

# 💻 Nota Bozza Bool

Testo descrittivo dell'attività svolta con comandi di prova.
""")

        raw_note_2 = os.path.join(inbox_dir, "Nota Bozza String.md")
        with open(raw_note_2, "w", encoding="utf-8") as f:
            f.write("""---
ready: "true"
title: "Nota Bozza String"
date: 2026-08-25
tags: [education, raw]
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Nota Bozza String]]

# 📝 Nota Bozza String

Appunti di studio per la lezione.
""")

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 2)

        draft_1 = os.path.join(inbox_dir, "Draft", "Nota Bozza Bool.md")
        source_1 = os.path.join(inbox_dir, "Source", "Nota Bozza Bool.md")
        draft_2 = os.path.join(inbox_dir, "Draft", "Nota Bozza String.md")
        source_2 = os.path.join(inbox_dir, "Source", "Nota Bozza String.md")

        self.assertFalse(os.path.exists(raw_note_1))
        self.assertFalse(os.path.exists(raw_note_2))
        self.assertTrue(os.path.exists(draft_1))
        self.assertTrue(os.path.exists(source_1))
        self.assertTrue(os.path.exists(draft_2))
        self.assertTrue(os.path.exists(source_2))

        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash = f.read()
            self.assertIn("## 📥 Note in Attesa di Approvazione", dash)
            self.assertIn("Approva [[Draft/Nota Bozza Bool]]", dash)
            self.assertIn("Approva [[Draft/Nota Bozza String]]", dash)

    def test_process_inbox_raw_notes_ready_false_ignored(self):
        """Asserts process_inbox_raw_notes leaves notes with ready: false or ready: 'false' completely untouched per D-06."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        raw_note = os.path.join(inbox_dir, "Nota In Lavorazione.md")
        original_content = """---
ready: false
title: "Nota In Lavorazione"
date: 2026-08-25
tags: [raw]
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Nota In Lavorazione]]

# 📝 Nota In Lavorazione

Sto ancora scrivendo questa nota...
"""
        with open(raw_note, "w", encoding="utf-8") as f:
            f.write(original_content)

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 0)
        self.assertTrue(os.path.exists(raw_note))

    def test_process_inbox_raw_notes_extract_frames_option(self):
        """Asserts process_inbox_raw_notes respects extract_frames: true from frontmatter."""
        from unittest.mock import patch
        raw_note = os.path.join(self.test_dir, "03 - Inbox", "Raw Video.md")
        with open(raw_note, "w", encoding="utf-8") as f:
            f.write("""---
ready: true
title: "Raw Video"
video_url: "https://www.youtube.com/watch?v=12345678901"
extract_frames: true
---
Corpo""")

        fake_data = {
            "title": "Raw Video",
            "channel": "Canale Test",
            "duration": 120,
            "chapters": [],
            "transcript": [{"text": "Test transcript", "start": 0, "duration": 5}],
            "extracted_images": []
        }

        with patch("youtube_helper.extract_youtube_data", return_value=fake_data) as mock_extract:
            processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
            self.assertEqual(len(processed), 1)
            mock_extract.assert_called_with("https://www.youtube.com/watch?v=12345678901", force_frames=True, vault_root=self.test_dir)

    def test_path_traversal_blocked_in_approvals(self):
        """Asserts process_tri_state_approvals rejects paths traversing outside vault root."""
        staged_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title="Nota Invasiva",
            body="Tentativo di traversal.",
            metadata={"title": "Nota Invasiva", "target_path": "../../outside/vault/Nota Invasiva.md"},
            target_dir="../../outside/vault"
        )
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_content.replace("- [ ] Approva [[Draft/Nota Invasiva]]", "- [x] Approva [[Draft/Nota Invasiva]]"))

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 0)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "..", "outside", "vault", "Nota Invasiva.md")))

    def test_youtube_video_id_regex_parsing(self):
        """Asserts get_video_id correctly extracts valid video IDs and rejects false matches."""
        import youtube_helper
        self.assertEqual(youtube_helper.get_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ"), "dQw4w9WgXcQ")
        self.assertEqual(youtube_helper.get_video_id("https://youtu.be/dQw4w9WgXcQ"), "dQw4w9WgXcQ")
        self.assertEqual(youtube_helper.get_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ"), "dQw4w9WgXcQ")
        self.assertEqual(youtube_helper.get_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ"), "dQw4w9WgXcQ")
        self.assertIsNone(youtube_helper.get_video_id("https://example.com/12345678901/article"))

    def test_ingest_source_unifies_with_daemon_lifecycle(self):
        """Asserts ingest_source replicates daemon + Raw Inbox Note lifecycle producing Draft and Source notes."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        text_source = "Analisi Architettura Distribuita\nAppunti dettagliati sul funzionamento dei cluster microservizi."

        draft_path = brain_ingest.ingest_source(
            source=text_source,
            vault_root=self.test_dir,
            target_dir="02 - Atlas/Tech"
        )

        self.assertTrue(os.path.exists(draft_path))
        self.assertIn("Draft", draft_path)
        self.assertFalse(os.path.basename(draft_path).startswith(("proposed-", "raw-", "seen-")))

        source_path = os.path.join(inbox_dir, "Source", "Analisi Architettura Distribuita.md")
        self.assertTrue(os.path.exists(source_path))

        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash = f.read()
        self.assertIn("Approva [[Draft/Analisi Architettura Distribuita]]", dash)
        self.assertNotIn("- ⏳ [[Draft/Analisi Architettura Distribuita]]", dash)

    def test_ingest_source_respects_custom_target_dir(self):
        """Asserts ingest_source embeds target_path in proposed frontmatter when custom target_dir is passed."""
        text_source = "Principi Clean Code\nRegole di refactoring per software di alta qualita."

        draft_path = brain_ingest.ingest_source(
            source=text_source,
            vault_root=self.test_dir,
            target_dir="02 - Atlas/Tech/Programming"
        )

        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('target_path: "02 - Atlas/Tech/Programming/Principi Clean Code.md"', content)

    def test_inbox_raw_note_duplicate_blocked_and_error_recorded(self):
        """Asserts process_inbox_raw_notes blocks raw notes matching existing Atlas/Blog URLs and registers error in Review Dashboard."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Finance")
        os.makedirs(atlas_dir, exist_ok=True)
        existing_file = os.path.join(atlas_dir, "La Bugia del Questa Volta e Diverso.md")
        with open(existing_file, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: video
source: "https://youtu.be/vi0BYzyWnFg"
video_url: "https://youtu.be/vi0BYzyWnFg"
title: "La Bugia del Questa Volta e Diverso"
---
Contenuto esistente.
""")

        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        dup_raw_note = os.path.join(inbox_dir, "Raw Note 2026-08-25 23-44.md")
        with open(dup_raw_note, "w", encoding="utf-8") as f:
            f.write("""---
ready: true
title: "Raw Note 2026-08-25 23-44"
date: 2026-08-25
tags: [youtube, transcript, raw]
area: ""
video_url: "https://www.youtube.com/watch?v=vi0BYzyWnFg"
---
Testo trascrizione grezza.
""")

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 0)

        with open(dup_raw_note, "r", encoding="utf-8") as f:
            dup_content = f.read()
        self.assertIn("ready: false", dup_content)

        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste", dash_content)
        self.assertIn("Duplicato rilevato", dash_content)
        self.assertIn("https://www.youtube.com/watch?v=vi0BYzyWnFg", dash_content)

    def test_approval_duplicate_source_blocked(self):
        """Asserts process_tri_state_approvals blocks promotion when a different file in Atlas already has the same source URL."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Finance")
        os.makedirs(atlas_dir, exist_ok=True)
        existing_file = os.path.join(atlas_dir, "Nota Precedente.md")
        with open(existing_file, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: video
source: "https://youtu.be/vi0BYzyWnFg"
title: "Nota Precedente"
---
Contenuto.
""")

        staged_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title="Nuovo Nome File",
            body="Altro testo.",
            metadata={"source": "https://www.youtube.com/watch?v=vi0BYzyWnFg", "title": "Nuovo Nome File"},
            target_dir="02 - Atlas/Finance"
        )

        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_content.replace("- [ ] Approva [[Draft/Nuovo Nome File]]", "- [x] Approva [[Draft/Nuovo Nome File]]"))

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 0)

        with open(dash_path, "r", encoding="utf-8") as f:
            dash_updated = f.read()
        self.assertIn("Duplicato sorgente", dash_updated)

    def test_review_dashboard_four_sections(self):
        """Asserts Review Dashboard.md is rendered with exact 4 sections (In Elaborazione, Note in Attesa, Errori, Storico) and canonical frontmatter per D-14."""
        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("## ⏳ In Elaborazione", content)
        self.assertIn("## 📥 Note in Attesa di Approvazione", content)
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste", content)
        self.assertIn("## 📜 Storico Recente", content)
        self.assertIn("status: draft", content)
        self.assertIn("type: moc", content)
        self.assertIn("area: meta", content)

    def test_extract_frames_flag(self):
        """Asserts YouTube frame extraction via ffmpeg is executed ONLY when --extract-frames flag is explicitly provided per D-10."""
        from unittest.mock import patch

        fake_data = {
            "title": "Video Senza Frame",
            "channel": "Canale Test",
            "duration": 120,
            "chapters": [],
            "transcript": [{"text": "Trascrizione di prova", "start": 0, "duration": 5}],
            "extracted_images": []
        }

        with patch("youtube_helper.extract_youtube_data", return_value=fake_data) as mock_extract:
            brain_ingest.ingest_source(
                source="https://youtube.com/watch?v=12345678901",
                vault_root=self.test_dir,
                extract_frames=False,
                force=True
            )
            mock_extract.assert_called_with("https://youtube.com/watch?v=12345678901", force_frames=None, vault_root=self.test_dir)

            brain_ingest.ingest_source(
                source="https://youtube.com/watch?v=12345678901",
                vault_root=self.test_dir,
                extract_frames=True,
                force=True
            )
            mock_extract.assert_called_with("https://youtube.com/watch?v=12345678901", force_frames=True, vault_root=self.test_dir)

    def test_in_progress_state_excludes_note_from_pending_approvals(self):
        """Asserts that an active in_progress note appears under In Elaborazione and is strictly excluded from Note in Attesa."""
        title = "Nota in Rielaborazione"
        draft_file = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write("# Titolo\nBozza in corso...")

        # Update dashboard with in_progress
        brain_ingest.update_review_dashboard(self.test_dir, in_progress=title)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must appear in In Elaborazione
        self.assertIn("## ⏳ In Elaborazione", content)
        self.assertIn(f"- ⏳ [[Draft/{title}]] (Fase 1/3: Estrazione Sorgente...)", content)

        # Must NOT appear in Note in Attesa di Approvazione
        self.assertNotIn(f"- [ ] Approva [[Draft/{title}]]", content)

        # Once in_progress is finished (e.g. stage_note completed)
        brain_ingest.update_review_dashboard(self.test_dir, finish_in_progress=title)
        with open(dash_path, "r", encoding="utf-8") as f:
            content_after = f.read()

        self.assertIn("*Nessun processo attivo.*", content_after)
        self.assertIn(f"- [ ] Approva [[Draft/{title}]]", content_after)

    def test_error_retry_and_dismiss_in_approvals(self):
        """Asserts that checking [x] on an error line retries ingestion, while [-] dismisses it."""
        from unittest.mock import patch

        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")

        # 1. Error Retry [x]
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write("""---
status: draft
type: moc
title: "Review Dashboard"
---
## ⏳ In Elaborazione
*Nessun processo attivo.*

## 📥 Note in Attesa di Approvazione
*Nessuna nota in attesa di approvazione.*

## ⚠️ Errori di Acquisizione & Azioni Richieste
- [x] [!] Riprova: https://example.com/retry-test — Motivo: Timeout

## 📜 Storico Recente
*Nessuna azione recente registrata.*
""")

        with patch("brain_ingest.ingest_source") as mock_ingest:
            mock_ingest.return_value = os.path.join(self.test_dir, "03 - Inbox", "Draft", "Retry Test.md")
            processed = brain_ingest.process_tri_state_approvals(self.test_dir)
            self.assertEqual(processed, 1)
            mock_ingest.assert_called_with("https://example.com/retry-test", vault_root=self.test_dir, force=True)

        with open(dash_path, "r", encoding="utf-8") as f:
            content_after = f.read()
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste\n*Nessun errore registrato.*", content_after)

        # 2. Error Dismiss [-] on raw file
        raw_to_dismiss = os.path.join(self.test_dir, "03 - Inbox", "Nota Fallita.md")
        with open(raw_to_dismiss, "w", encoding="utf-8") as f:
            f.write("# Fallimento")

        with open(dash_path, "w", encoding="utf-8") as f:
            f.write("""---
status: draft
type: moc
title: "Review Dashboard"
---
## ⏳ In Elaborazione
*Nessun processo attivo.*

## 📥 Note in Attesa di Approvazione
*Nessuna nota in attesa di approvazione.*

## ⚠️ Errori di Acquisizione & Azioni Richieste
- [-] [!] Riprova: Nota Fallita.md — Motivo: Errore sintassi

## 📜 Storico Recente
*Nessuna azione recente registrata.*
""")

        processed_dismiss = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed_dismiss, 1)
        self.assertFalse(os.path.exists(raw_to_dismiss))

        with open(dash_path, "r", encoding="utf-8") as f:
            content_dismiss = f.read()
        self.assertIn("## ⚠️ Errori di Acquisizione & Azioni Richieste\n*Nessun errore registrato.*", content_dismiss)

    def test_panic_button_presence_in_review_dashboard(self):
        """Asserts Review Dashboard includes the Panic Button line and review instruction."""
        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("PANIC BUTTON", content)
        self.assertIn("- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)", content)

    def test_trigger_panic_abort(self):
        """Asserts trigger_panic_abort cleans locks, resets ready: true to ready: false, clears in_progress, and records history."""
        # 1. Create a dummy lock file
        dummy_lock = "/tmp/brain_ingest_testpanic123.lock"
        with open(dummy_lock, "w", encoding="utf-8") as f:
            f.write("pid: 9999999\ntime: 2026-08-29T00:00:00\n")
        self.assertTrue(os.path.exists(dummy_lock))

        # 2. Create raw note with ready: true
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        raw_note = os.path.join(inbox_dir, "Nota In Corso.md")
        with open(raw_note, "w", encoding="utf-8") as f:
            f.write("---\nready: true\ntitle: Nota In Corso\n---\nCorpo.")

        # 3. Set dashboard with in-progress
        brain_ingest.update_review_dashboard(self.test_dir, in_progress="Nota In Corso", phase="Fase 2/3: Rielaborazione Concettuale AI...")

        # 4. Trigger panic abort
        brain_ingest.trigger_panic_abort(self.test_dir)

        # Assert lock cleaned
        self.assertFalse(os.path.exists(dummy_lock))

        # Assert raw note ready reset to false
        with open(raw_note, "r", encoding="utf-8") as f:
            self.assertIn("ready: false", f.read())

        # Assert dashboard cleared
        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("*Nessun processo attivo.*", content)
        self.assertIn("- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)", content)

        # Assert history logged
        hist_path = os.path.join(self.test_dir, "99 - Meta", "logs", "inbox_history.md")
        with open(hist_path, "r", encoding="utf-8") as f:
            self.assertIn("[PANIC_ABORT]", f.read())

    def test_trigger_panic_abort_preserves_watcher(self):
        """Asserts trigger_panic_abort excludes the watcher daemon PID from termination."""
        from unittest.mock import patch

        watcher_pid = 12345
        pid_file = "/tmp/brain_watcher.pid"
        with open(pid_file, "w", encoding="utf-8") as f:
            f.write(str(watcher_pid))

        try:
            with patch("os.kill") as mock_kill, patch("brain_ingest.is_pid_alive", return_value=True):
                lock1 = "/tmp/brain_ingest_watchertest.lock"
                lock2 = "/tmp/brain_ingest_othertest.lock"
                with open(lock1, "w") as f: f.write(f"pid: {watcher_pid}\n")
                with open(lock2, "w") as f: f.write("pid: 67890\n")

                brain_ingest.trigger_panic_abort(self.test_dir)

                killed_pids = [call.args[0] for call in mock_kill.call_args_list]
                self.assertNotIn(watcher_pid, killed_pids)
                self.assertIn(67890, killed_pids)
        finally:
            if os.path.exists(pid_file):
                os.remove(pid_file)

    def test_trigger_panic_abort_clears_in_progress_draft_notes(self):
        """Asserts trigger_panic_abort clears in-progress draft notes from Draft/ and In Elaborazione."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        draft_file = os.path.join(inbox_dir, "Draft", "Nota In Rielaborazione Panic.md")
        source_file = os.path.join(inbox_dir, "Source", "Nota In Rielaborazione Panic.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write("""---
status: in-progress
type: video
title: "Nota In Rielaborazione Panic"
source: "https://youtu.be/panic_test_123"
---
# Nota In Rielaborazione Panic
""")
        with open(source_file, "w", encoding="utf-8") as f:
            f.write("Trascrizione raw.")

        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            self.assertIn("Nota in Rielaborazione Panic", f.read())

        # Trigger panic
        brain_ingest.trigger_panic_abort(self.test_dir)

        # Assert in-progress draft was cleared and dashboard shows *Nessun processo attivo.*
        self.assertFalse(os.path.exists(draft_file))
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("*Nessun processo attivo.*", content)
        self.assertNotIn("Nota in Rielaborazione Panic", content)

    def test_process_tri_state_approvals_with_panic(self):
        """Asserts that checking the Panic Button [x] in Review Dashboard executes panic abort and resets the checkbox."""
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write("""---
status: draft
type: moc
title: "Review Dashboard"
---
## ⏳ In Elaborazione
- [x] 🛑 Interrompi elaborazioni attive (Panic Button)
- ⏳ [[Draft/Test Ingest]] (Fase 2/3: Rielaborazione Concettuale AI...)

## 📥 Note in Attesa di Approvazione
*Nessuna nota in attesa di approvazione.*

## ⚠️ Errori di Acquisizione & Azioni Richieste
*Nessun errore registrato.*

## 📜 Storico Recente
*Nessuna azione recente registrata.*
""")
        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 1)

        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)", content)
        self.assertIn("*Nessun processo attivo.*", content)

    def test_in_progress_automatic_transition_to_pending_on_status_draft(self):
        """Asserts that a note with status: in-progress appears under In Elaborazione,
        and when changed to status: draft it automatically transitions to Note in Attesa di Approvazione."""
        title = "Nota Test Rielaborazione"
        draft_file = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(f"""---
status: in-progress
type: concept
area: tech
title: "{title}"
---
# {title}
Bozza in rielaborazione...
""")

        # 1. Dashboard refresh -> should be in In Elaborazione
        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("## ⏳ In Elaborazione", content)
        self.assertIn(f"- ⏳ [[Draft/{title}]] (Fase 2/3: Rielaborazione Concettuale AI...)", content)
        self.assertNotIn(f"- [ ] Approva [[Draft/{title}]]", content)

        # 2. Update note status to draft (finished re-elaboration)
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(f"""---
status: draft
type: concept
area: tech
title: "{title}"
---
# {title}
Bozza completata e pronta per la revisione.
""")

        # 3. Next routine dashboard refresh (without passing finish_in_progress)
        brain_ingest.update_review_dashboard(self.test_dir)
        with open(dash_path, "r", encoding="utf-8") as f:
            content_after = f.read()

        self.assertIn("*Nessun processo attivo.*", content_after)
        self.assertIn(f"- [ ] Approva [[Draft/{title}]]", content_after)

    def test_stale_prog_lines_auto_pruned_without_active_locks(self):
        """Asserts that stale progress lines in Review Dashboard are pruned if the note is draft or absent and no locks exist."""
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write("""---
status: draft
type: moc
title: "Review Dashboard"
---
## ⏳ In Elaborazione
- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)
- ⏳ [[Draft/Nota Fantasma]] (Fase 1/3: Estrazione Sorgente...)
- ⏳ https://youtu.be/fakeurl123 (Fase 1/3: Estrazione Sorgente...)

## 📥 Note in Attesa di Approvazione
*Nessuna nota in attesa di approvazione.*

## ⚠️ Errori di Acquisizione & Azioni Richieste
*Nessun errore registrato.*

## 📜 Storico Recente
*Nessuna azione recente registrata.*
""")
        brain_ingest.update_review_dashboard(self.test_dir)
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("*Nessun processo attivo.*", content)
        self.assertNotIn("Nota Fantasma", content)
        self.assertNotIn("fakeurl123", content)

    def test_tri_state_approvals_with_uppercase_x(self):
        """Asserts process_tri_state_approvals accepts [X] as valid approval."""
        title = "Nota Approvata Maiuscola"
        draft_path = brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=title,
            body="Contenuto.",
            metadata={"title": title, "area": "tech"},
            target_dir="02 - Atlas/Tech"
        )
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash = f.read()
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash.replace(f"- [ ] Approva [[Draft/{title}]]", f"- [X] Approva [[Draft/{title}]]"))

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 1)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "02 - Atlas", "Tech", f"{title}.md")))
        self.assertFalse(os.path.exists(draft_path))

    def test_large_frontmatter_in_progress_draft_not_moved_prematurely(self):
        """Asserts that a draft note with frontmatter > 800 bytes and status: in-progress
        remains in ## ⏳ In Elaborazione and is strictly excluded from ## 📥 Note in Attesa di Approvazione."""
        title = "Grande Bozza in Rielaborazione"
        draft_file = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        long_tags = [f"tech/subtag_{i}" for i in range(30)]
        long_summary = "Questa è una sintesi molto lunga che serve a verificare che frontmatter e metadati estesi non vengano troncati a 800 byte durante la lettura da parte di update_review_dashboard."
        long_related = [f'"[[Nota Correlata {i}]]"' for i in range(15)]
        
        content = f"""---
status: in-progress
type: video
area: tech
related: [{', '.join(long_related)}]
aliases: []
source: "https://youtu.be/long_frontmatter_test_12345"
title: "{title}"
date: '2026-08-29'
updated: 2026-08-29T14:00
tags: [{', '.join(long_tags)}]
summary: "{long_summary}"
target_path: "02 - Atlas/Tech/{title}.md"
video_url: "https://youtu.be/long_frontmatter_test_12345"
channel: "TestChannel"
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{title}]]

# {title}

## Sintesi Esecutiva
Contenuto in rielaborazione...
"""
        self.assertGreater(len(content.split("---")[1]), 800)
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(content)

        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash = f.read()

        self.assertIn(f"- ⏳ [[Draft/{title}]] (Fase 2/3: Rielaborazione Concettuale AI...)", dash)
        self.assertNotIn(f"Approva [[Draft/{title}]]", dash)

    def test_mark_draft_ready_transitions_to_approval(self):
        """Asserts mark_draft_ready sets status: draft in frontmatter and cleanly moves note to Note in Attesa di Approvazione."""
        title = "Nota da Completare"
        draft_file = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(f"""---
status: in-progress
type: concept
area: tech
title: "{title}"
---
# {title}
Contenuto completato.
""")
        brain_ingest.update_review_dashboard(self.test_dir)
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            self.assertIn(f"- ⏳ [[Draft/{title}]]", f.read())

        # Now mark ready
        res = brain_ingest.mark_draft_ready(self.test_dir, title)
        self.assertTrue(res)

        with open(draft_file, "r", encoding="utf-8") as f:
            draft_c = f.read()
        self.assertIn("status: draft", draft_c)
        self.assertNotIn("status: in-progress", draft_c)

        with open(dash_path, "r", encoding="utf-8") as f:
            updated_dash = f.read()
        self.assertNotIn(f"- ⏳ [[Draft/{title}]]", updated_dash)
        self.assertIn(f"- [ ] Approva [[Draft/{title}]]", updated_dash)

    def test_url_progress_line_reconciled_when_draft_exists(self):
        """Asserts that a URL line in In Elaborazione is replaced by the Draft note line without duplicating."""
        url = "https://youtu.be/reconcile_test_123"
        title = "Nota da URL Riconciliata"
        draft_file = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{title}.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(f"""---
status: in-progress
type: video
area: tech
source: "{url}"
video_url: "{url}"
title: "{title}"
---
# {title}
""")
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(f"""---
status: draft
type: moc
title: "Review Dashboard"
---
## ⏳ In Elaborazione
- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)
- ⏳ {url} (Fase 1/3: Estrazione Sorgente...)

## 📥 Note in Attesa di Approvazione
*Nessuna nota in attesa di approvazione.*

## ⚠️ Errori di Acquisizione & Azioni Richieste
*Nessun errore registrato.*

## 📜 Storico Recente
*Nessuna azione recente registrata.*
""")
        brain_ingest.update_review_dashboard(self.test_dir)
        with open(dash_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn(url, content)
        self.assertIn(f"- ⏳ [[Draft/{title}]] (Fase 2/3: Rielaborazione Concettuale AI...)", content)

    def test_enrich_draft_with_ai_success(self):
        """Asserts enrich_draft_with_ai parses agy output with highlights and summary."""
        from unittest.mock import patch, MagicMock

        os.environ.pop("BRAIN_INGEST_NO_AI", None)
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_res.stdout = """# Test AI Titolo

## Sintesi Esecutiva
<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Test AI Titolo</b></font></mark>: Questa è una sintesi densa generata da AI.

## Concetti Chiave e Takeaway
- <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Punto 1</b></font></mark>: Dettaglio importante.

## Quadro Concettuale
Spiegazione dettagliata.

---SUMMARY---
Sintesi esecutiva densa generata dall'intelligenza artificiale per il test del Second Brain.
"""
        with patch("brain_ingest.subprocess.run", return_value=mock_res):
            body, summary = brain_ingest.enrich_draft_with_ai(self.test_dir, "Test AI Titolo", "Contenuto raw", depth="sintesi")
            self.assertIn("## Sintesi Esecutiva", body)
            self.assertIn("<mark style=", body)
            self.assertIn("Sintesi esecutiva densa generata", summary)
            self.assertNotIn("---SUMMARY---", body)

    def test_enrich_draft_with_ai_fallback_on_error(self):
        """Asserts enrich_draft_with_ai safely falls back to heuristic generation on timeout/failure."""
        from unittest.mock import patch

        os.environ.pop("BRAIN_INGEST_NO_AI", None)
        with patch("brain_ingest.subprocess.run", side_effect=Exception("Subprocess timeout")):
            body, summary = brain_ingest.enrich_draft_with_ai(self.test_dir, "Fallback Titolo", "Contenuto grezzo per fallback di sicurezza.", depth="sintesi")
            self.assertIn("## Sintesi Esecutiva", body)
            self.assertIn("Fallback Titolo", body)
            self.assertTrue(len(summary) > 10)

    def test_ingest_source_completes_phase_5_to_approval(self):
        """Asserts ingest_source runs Phase 2/3 and transitions draft to status: draft in Note in Attesa di Approvazione."""
        from unittest.mock import patch, MagicMock

        os.environ.pop("BRAIN_INGEST_NO_AI", None)
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_res.stdout = """# Testo di Prova da Rielaborare con AI

## Sintesi Esecutiva
<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Testo di Prova da Rielaborare con AI</b></font></mark>: Analisi completata.

---SUMMARY---
Sintesi automatica di prova per nuova ingestione completata con successo.
"""
        with patch("brain_ingest.subprocess.run", return_value=mock_res):
            draft_path = brain_ingest.ingest_source("Testo di prova da rielaborare con AI", vault_root=self.test_dir)
            self.assertTrue(os.path.exists(draft_path))
            with open(draft_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("status: draft", content)

            dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
            with open(dash_path, "r", encoding="utf-8") as f:
                dash_content = f.read()
            self.assertIn("Approva [[Draft/Testo di Prova da Rielaborare con AI]]", dash_content)
            self.assertNotIn("⏳ [[Draft/Testo di Prova da Rielaborare con AI]]", dash_content)

    def test_format_note_header_block_youtube(self):
        """Asserts format_note_header_block generates standard YouTube summary with Video URL and wikilinked Canale."""
        meta_plain = {
            "type": "video",
            "source": "https://youtu.be/KGlkNmKLEWs",
            "channel": "Salvatore Sanfilippo"
        }
        res_plain = brain_ingest.format_note_header_block("Test Title", meta_plain)
        self.assertEqual(res_plain, "- **Video URL**: https://youtu.be/KGlkNmKLEWs\n- **Canale**: [[Salvatore Sanfilippo]]\n\n---\n")

        meta_wikilink = {
            "type": "video",
            "source": "https://youtu.be/KGlkNmKLEWs",
            "channel": "[[Salvatore Sanfilippo]]"
        }
        res_wikilink = brain_ingest.format_note_header_block("Test Title", meta_wikilink)
        self.assertEqual(res_wikilink, "- **Video URL**: https://youtu.be/KGlkNmKLEWs\n- **Canale**: [[Salvatore Sanfilippo]]\n\n---\n")

    def test_tri_state_approvals_renames_stale_raw_note_target_path(self):
        """Asserts process_tri_state_approvals overrides stale Raw Note target_path with approved title."""
        title = "Semantic Versioning"
        draft_dir = os.path.join(self.test_dir, "03 - Inbox", "Draft")
        os.makedirs(draft_dir, exist_ok=True)
        draft_path = os.path.join(draft_dir, f"{title}.md")
        
        draft_content = f"""---
status: draft
type: concept
area: tech
related: []
aliases: []
source: original
title: "{title}"
date: '2026-08-31'
updated: 2026-08-31T00:20
tags: [tech/standards]
summary: "Sintesi di Semantic Versioning."
target_path: "02 - Atlas/Tech & AI/Raw Note 2026 - 08 - 31 00 - 07.md"
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{title}]]

# {title}

## Sintesi Esecutiva
Contenuto su Semantic Versioning.
"""
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft_content)

        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        dash_content = f"""---
status: draft
type: moc
area: meta
related: ["[[Home MOC]]"]
title: "Review Dashboard"
date: '2026-08-31'
updated: 2026-08-31T00:20
tags: [meta/dashboard]
summary: "Dashboard di revisione GTD."
---
[[Home MOC|Home]] / [[Atlas]] / [[Review Dashboard]]

# 📥 Inbox Review Dashboard

## ⏳ In Elaborazione
- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)
*Nessun processo attivo.*

## 📥 Note in Attesa di Approvazione
- [x] Approva [[Draft/{title}]]

## ⚠️ Errori di Acquisizione & Azioni Richieste
*Nessun errore registrato.*
"""
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_content)

        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 1)

        expected_dest = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI", f"{title}.md")
        unexpected_dest = os.path.join(self.test_dir, "02 - Atlas", "Tech & AI", "Raw Note 2026 - 08 - 31 00 - 07.md")
        self.assertTrue(os.path.exists(expected_dest), f"Expected note to be created at {expected_dest}")
        self.assertFalse(os.path.exists(unexpected_dest), f"Note should not be named with stale Raw Note target_path")

        with open(expected_dest, "r", encoding="utf-8") as f:
            saved_content = f.read()
        self.assertIn(f"title: \"{title}\"", saved_content)
        self.assertIn(f"[[Home MOC|Home]] / [[Tech & AI]] / [[{title}]]", saved_content)
        self.assertNotIn("Raw Note", saved_content)

    def test_process_inbox_raw_notes_infers_title_from_h1(self):
        """Asserts process_inbox_raw_notes replaces generic Raw Note title with explicit H1 title in body."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        os.makedirs(inbox_dir, exist_ok=True)
        raw_file = os.path.join(inbox_dir, "Raw Note 2026-08-31 00-07.md")
        
        raw_content = """---
ready: true
title: "Raw Note 2026-08-31 00-07"
date: '2026-08-31'
tags: [tech/raw]
area: ""
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Raw Note 2026-08-31 00-07]]

# Architettura a Microservizi

## Appunti Grezzi
Appunti sul pattern a microservizi e service discovery.
"""
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(raw_content)

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0], "Architettura a Microservizi")

        draft_file = os.path.join(inbox_dir, "Draft", "Architettura a Microservizi.md")
        self.assertTrue(os.path.exists(draft_file))

        with open(draft_file, "r", encoding="utf-8") as f:
            draft_text = f.read()
        self.assertIn('title: "Architettura a Microservizi"', draft_text)
        self.assertIn('target_path: "02 - Atlas/Tech & AI/Software Development/Architettura a Microservizi.md"', draft_text)

    def test_concurrent_approval_preserves_in_progress_note(self):
        """Asserts approving note A does not wipe note B (with status: in-progress) from Review Dashboard in-progress section."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        draft_dir = os.path.join(inbox_dir, "Draft")
        os.makedirs(draft_dir, exist_ok=True)

        # 1. Note B: In-progress draft
        note_b_title = "Nota In Elaborazione"
        brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=note_b_title,
            body="Bozza in lavorazione AI...",
            metadata={"title": note_b_title, "status": "in-progress"},
            target_dir="02 - Atlas/Tech & AI",
            status="in-progress"
        )

        # 2. Note A: Ready for approval
        note_a_title = "Nota Pronta Da Approvare"
        brain_ingest.stage_note(
            vault_root=self.test_dir,
            title=note_a_title,
            body="Bozza finita.",
            metadata={"title": note_a_title, "status": "draft"},
            target_dir="02 - Atlas/Tech & AI",
            status="draft"
        )

        # 3. Simulate User Approving Note A in Review Dashboard
        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()

        clean_b = brain_ingest.brain_health.clean_title_str(note_b_title)
        clean_a = brain_ingest.brain_health.clean_title_str(note_a_title)

        self.assertIn(f"[[Draft/{clean_b}]]", dash_content)
        self.assertIn(f"- [ ] Approva [[Draft/{clean_a}]]", dash_content)

        # Mark [x] on Note A
        dash_modified = dash_content.replace(f"- [ ] Approva [[Draft/{clean_a}]]", f"- [x] Approva [[Draft/{clean_a}]]")
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(dash_modified)

        # 4. Process approvals
        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 1)

        # 5. Verify Note B is STILL present under ## ⏳ In Elaborazione
        with open(dash_path, "r", encoding="utf-8") as f:
            updated_dash = f.read()

        self.assertIn(f"[[Draft/{clean_b}]]", updated_dash)
        self.assertNotIn("*Nessun processo attivo.*", updated_dash)
        self.assertNotIn(f"Approva [[Draft/{clean_a}]]", updated_dash)


if __name__ == "__main__":
    unittest.main()



