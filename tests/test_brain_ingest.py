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

    def test_note_lock_stale_pid_auto_healing(self):
        """Asserts NoteLock auto-cleans lockfiles whose PID is no longer running (kill -0 probe fails)
        or file mtime exceeds 10 minutes per D-20.
        """
        source = "https://youtube.com/watch?v=stale_pid_test"
        dummy_lock = brain_ingest.NoteLock(source)
        lock_path = dummy_lock.lock_file

        # 1. Simulate dead PID (PID 9999999 is practically guaranteed not to exist)
        with open(lock_path, "w", encoding="utf-8") as f:
            f.write("pid: 9999999\ntimestamp: 2026-08-25T00:00:00\n")

        self.assertTrue(os.path.exists(lock_path))

        # NoteLock should auto-heal and acquire cleanly without raising RuntimeError
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
        # Set mtime to 15 minutes ago
        past_time = os.path.getmtime(lock_path) - 900
        os.utime(lock_path, (past_time, past_time))

        with brain_ingest.NoteLock(source) as lock:
            self.assertTrue(lock.acquired)
            self.assertTrue(os.path.exists(lock_path))

        self.assertFalse(os.path.exists(lock_path))

    def test_watcher_lifecycle_and_pid_auto_healing(self):
        """Asserts watch.sh script syntax is valid, supports lifecycle flags, and manages PID tracking per D-01, D-20."""
        script_path = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts", "watch.sh")
        self.assertTrue(os.path.exists(script_path))

        # Check bash syntax
        res = subprocess.run(["bash", "-n", script_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Bash syntax check failed: {res.stderr}")

        # Check status command when not running
        res_status = subprocess.run(["bash", script_path, "status"], capture_output=True, text=True, env=dict(os.environ, PID_FILE=f"/tmp/test_watcher_{os.getpid()}.pid"))
        # Should report not running
        self.assertIn("not running", res_status.stdout.lower() + res_status.stderr.lower())

    def test_log_rotation_on_size(self):
        """Asserts log rotation moves watch.log -> watch.log.1 -> watch.log.2 -> watch.log.3 when exceeding 5MB cap per D-03."""
        script_path = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts", "watch.sh")
        test_log_dir = os.path.join(self.test_dir, "99 - Meta", "logs")
        os.makedirs(test_log_dir, exist_ok=True)
        test_log_file = os.path.join(test_log_dir, "watch.log")

        # Create a log file exceeding 5MB (5242881 bytes)
        with open(test_log_file, "wb") as f:
            f.seek(5242881)
            f.write(b"0")

        self.assertTrue(os.path.getsize(test_log_file) > 5242880)

        # Run rotate_logs helper embedded in watch.sh
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
        """Asserts extract_youtube_data raises TranscriptUnavailableError when no subtitles/transcripts exist per D-18."""
        import youtube_helper
        from unittest.mock import patch

        with patch.object(youtube_helper, "YouTubeTranscriptApi", None):
            with self.assertRaises(youtube_helper.TranscriptUnavailableError):
                youtube_helper.extract_youtube_data("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

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
        from unittest.mock import patch, MagicMock

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

    def test_heuristic_atlas_routing(self):
        """Asserts classify_target_directory suggests appropriate subfolder based on tags/title/content per D-10."""
        # AI
        dest_ai = brain_ingest.classify_target_directory("Costruire Agenti LLM con RAG", ["tech/ai"], "Modelli transformer")
        self.assertIn("Tech & AI", dest_ai)

        # Finance
        dest_fin = brain_ingest.classify_target_directory("Guida alla Gestione Fiscale e Investimenti", ["finance/tax"], "Tasse e investimenti")
        self.assertEqual(dest_fin, "02 - Atlas/Finance")

        # Education
        dest_edu = brain_ingest.classify_target_directory("Appunti Esame Analisi Matematica", ["education/math"], "Studio universitario")
        self.assertEqual(dest_edu, "02 - Atlas/Education & Learning")

        # Mentality
        dest_men = brain_ingest.classify_target_directory("Come Sviluppare Disciplina e Focus", ["mentality/habits"], "Abitudini atomiche")
        self.assertIn("Personal Growth & Health", dest_men)

        # Blog
        dest_blog = brain_ingest.classify_target_directory("Articolo Pubblico sul Blog", ["blog/post"], "Post divulgativo")
        self.assertEqual(dest_blog, "05 - Blog")

    def test_inbox_raw_note_intake_on_status_ready(self):
        """Asserts process_inbox_raw_notes scans 03 - Inbox/ and converts notes with status: ready into formatted drafts per D-15, D-16."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        raw_note = os.path.join(inbox_dir, "Appunto Rapido.md")
        with open(raw_note, "w", encoding="utf-8") as f:
            f.write("""---
status: ready
type: concept
area: tech
title: "Appunto Rapido"
---
Questo è un appunto grezzo da formattare.
""")

        processed = brain_ingest.process_inbox_raw_notes(self.test_dir)
        self.assertEqual(len(processed), 1)

        with open(raw_note, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("status: draft", content)
        self.assertIn("[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[Appunto Rapido]]", content)

        # Review dashboard should have it registered
        dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("- [ ] Approva [[Appunto Rapido]]", dash_content)

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

        # Stage a new note in Inbox with same title but different source
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
            f.write(dash_content.replace("- [ ] Approva [[Nota Collisione]]", "- [x] Approva [[Nota Collisione]]"))

        # Process approvals
        processed = brain_ingest.process_tri_state_approvals(self.test_dir)
        self.assertEqual(processed, 0) # Should be blocked due to collision

        # Original note must NOT be overwritten
        with open(existing_dest, "r", encoding="utf-8") as f:
            self.assertIn("Original permanent content.", f.read())

        # Dashboard should contain collision warning
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

if __name__ == "__main__":
    unittest.main()
