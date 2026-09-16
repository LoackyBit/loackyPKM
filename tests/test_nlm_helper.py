import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import subprocess
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import nlm_helper


class TestNLMHelperSubprocess(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_build_nlm_query_with_course(self):
        query = nlm_helper.build_nlm_query(
            title="Sistemi Operativi e Concorrenza",
            course="Informatica",
            snippet="La concorrenza gestisce processi multipli."
        )
        expected_prefix = "Come schematizzare ed estrarre i principi primi di Sistemi Operativi e Concorrenza per la materia Informatica?"
        self.assertTrue(query.startswith(expected_prefix))
        self.assertIn("Ecco un estratto contestuale:\n\nLa concorrenza gestisce processi multipli.", query)

    def test_build_nlm_query_without_course(self):
        query = nlm_helper.build_nlm_query(
            title="Principi di Metacognizione",
            course=None,
            snippet="L'apprendimento attivo supera la memoria passiva."
        )
        expected_prefix = "Come schematizzare ed estrarre i principi primi di Principi di Metacognizione?"
        self.assertTrue(query.startswith(expected_prefix))
        self.assertNotIn("per la materia", query)
        self.assertIn("Ecco un estratto contestuale:\n\nL'apprendimento attivo supera la memoria passiva.", query)

    def test_sanitize_json_output_clean(self):
        raw = '{"answer": "Usa schemi causa-effetto.", "citations": {}, "references": [], "sources_used": []}'
        data = nlm_helper.sanitize_json_output(raw)
        self.assertEqual(data["answer"], "Usa schemi causa-effetto.")

    def test_sanitize_json_output_with_ansi_and_trailing_logs(self):
        raw = '\x1b[32m[INFO] Iniziando query...\x1b[0m\n{"answer": "Principio di atomicità per Anki.", "citations": {"c1": "test"}}\n[DEBUG] Finished in 12s.'
        data = nlm_helper.sanitize_json_output(raw)
        self.assertEqual(data["answer"], "Principio di atomicità per Anki.")
        self.assertIn("c1", data["citations"])

    @patch("nlm_helper.resolve_nlm_binary")
    @patch("subprocess.run")
    def test_query_notebook_success_mock(self, mock_run, mock_resolve):
        mock_resolve.return_value = "/mock/bin/nlm"
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = json.dumps({
            "answer": "Identifica le variabili di stato e crea diagramma causale.",
            "citations": {"ref1": "Slide 4"},
            "references": ["Ref A"],
            "sources_used": ["Notebook ADC"]
        })
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        result = nlm_helper.query_notebook(
            title="Architettura Concorrente",
            content="Estratto lungo della lezione...",
            course="Informatica",
            vault_root=self.test_dir,
            timeout=120,
            use_cache=False
        )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["title"], "Architettura Concorrente")
        self.assertEqual(result["course"], "Informatica")
        self.assertIn("diagramma causale", result["answer"])
        self.assertEqual(mock_run.call_count, 1)

        # Verify arguments passed to subprocess.run (shell=False, timeout=120, correct list command)
        called_args, called_kwargs = mock_run.call_args
        cmd_list = called_args[0]
        self.assertEqual(cmd_list[0], "/mock/bin/nlm")
        self.assertEqual(cmd_list[1], "notebook")
        self.assertEqual(cmd_list[2], "query")
        self.assertEqual(cmd_list[3], nlm_helper.DEFAULT_NOTEBOOK_ID)
        self.assertEqual(cmd_list[-1], "--json")
        self.assertEqual(called_kwargs.get("timeout"), 120)
        self.assertFalse(called_kwargs.get("shell", False))

    @patch("nlm_helper.resolve_nlm_binary")
    @patch("subprocess.run")
    def test_query_notebook_timeout_raises_timeout_error(self, mock_run, mock_resolve):
        mock_resolve.return_value = "/mock/bin/nlm"
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["nlm"], timeout=120)

        with self.assertRaises(nlm_helper.NLMTimeoutError):
            nlm_helper.query_notebook(
                title="Nota Lenta",
                content="Contenuto...",
                vault_root=self.test_dir,
                timeout=120,
                use_cache=False
            )

    @patch("nlm_helper.resolve_nlm_binary")
    @patch("subprocess.run")
    def test_query_notebook_auth_expired_raises_auth_error(self, mock_run, mock_resolve):
        mock_resolve.return_value = "/mock/bin/nlm"
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = "Authentication expired. Please run 'nlm login'."
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        with self.assertRaises(nlm_helper.NLMAuthError):
            nlm_helper.query_notebook(
                title="Nota Auth",
                content="Contenuto...",
                vault_root=self.test_dir,
                timeout=120,
                use_cache=False
            )

    def test_compute_cache_key_deterministic(self):
        k1 = nlm_helper.compute_cache_key("nb1", "Titolo A", "Corso 1", "Snippet 1")
        k2 = nlm_helper.compute_cache_key("nb1", "Titolo A", "Corso 1", "Snippet 1")
        k3 = nlm_helper.compute_cache_key("nb1", "Titolo B", "Corso 1", "Snippet 1")
        k4 = nlm_helper.compute_cache_key("nb1", "Titolo A", None, "Snippet 1")

        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)
        self.assertNotEqual(k1, k4)
        self.assertEqual(len(k1), 64)  # SHA-256 hex length (T-14-02)

    def test_cache_lifecycle_save_and_retrieve(self):
        cache_key = "testkey123"
        payload = {"answer": "Risposta cached", "notebook_id": "test_id"}

        nlm_helper.save_response_to_cache(self.test_dir, cache_key, payload)
        retrieved = nlm_helper.get_cached_response(self.test_dir, cache_key)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["answer"], "Risposta cached")

    @patch("subprocess.run")
    def test_query_notebook_uses_cache_when_available(self, mock_run):
        title = "Nota In Cache"
        content = "Estratto nota"
        cache_key = nlm_helper.compute_cache_key(nlm_helper.DEFAULT_NOTEBOOK_ID, title, None, content)
        cached_data = {
            "title": title,
            "answer": "Risposta prelevata direttamente da cache.",
            "citations": {}
        }
        nlm_helper.save_response_to_cache(self.test_dir, cache_key, cached_data)

        result = nlm_helper.query_notebook(
            title=title,
            content=content,
            vault_root=self.test_dir,
            use_cache=True
        )

        self.assertEqual(result["answer"], "Risposta prelevata direttamente da cache.")
        mock_run.assert_not_called()

    def test_clear_cache(self):
        cache_dir = nlm_helper.get_cache_dir(self.test_dir)
        with open(os.path.join(cache_dir, "cache1.json"), "w", encoding="utf-8") as f:
            f.write("{}")
        with open(os.path.join(cache_dir, "cache2.json"), "w", encoding="utf-8") as f:
            f.write("{}")
        with open(os.path.join(cache_dir, "ignored.txt"), "w", encoding="utf-8") as f:
            f.write("text")

        deleted = nlm_helper.clear_cache(self.test_dir)
        self.assertEqual(deleted, 2)
        self.assertFalse(os.path.exists(os.path.join(cache_dir, "cache1.json")))
        self.assertTrue(os.path.exists(os.path.join(cache_dir, "ignored.txt")))

    def test_format_metacognitive_sections_zero_emoji(self):
        directives = {
            "answer": "Identifica le entità cardine e crea schema causale Mermaid."
        }
        prompt_text = nlm_helper.format_metacognitive_constraints_prompt(directives)
        self.assertIn("DIRETTIVE METACOGNITIVE SPECIALISTICHE", prompt_text)
        self.assertIn("VINCOLI ATTIVI DI STRUTTURAZIONE", prompt_text)
        self.assertIn("Mermaid", prompt_text)

        markdown_section = nlm_helper.format_metacognitive_markdown_section(directives)
        self.assertIn("## Direttive Metacognitive", markdown_section)
        # Check zero emoji in H1-H3 headings (GEMINI.md, D-06)
        for line in markdown_section.splitlines():
            if line.startswith("#"):
                for char in line:
                    self.assertLess(ord(char), 0x1F000, f"Emoji detected in heading line: {line}")

    @patch("nlm_helper.clear_cache")
    def test_cli_standalone_arguments(self, mock_clear):
        mock_clear.return_value = 5
        with patch.object(sys, "argv", ["nlm_helper.py", "--clear-cache"]):
            with self.assertRaises(SystemExit) as cm:
                nlm_helper.main()
            self.assertEqual(cm.exception.code, 0)
            mock_clear.assert_called_once()


if __name__ == "__main__":
    unittest.main()

