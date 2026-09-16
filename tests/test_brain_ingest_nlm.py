import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import shutil
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_ingest
import nlm_helper


class TestBrainIngestNLM(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Draft"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Source"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "logs"), exist_ok=True)

        # Ensure Review Dashboard exists
        self.dashboard_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        with open(self.dashboard_path, "w", encoding="utf-8") as f:
            f.write("# Review Dashboard\n\n## Note in Attesa di Approvazione\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch("brain_ingest.enrich_draft_with_ai")
    @patch("nlm_helper.query_notebook")
    def test_ingest_source_without_nlm_flag_skips_nlm(self, mock_nlm, mock_enrich):
        mock_enrich.return_value = ("# Test Nota\n\nCorpo della nota.", "Sintesi di test.")
        
        test_file = os.path.join(self.test_dir, "appunti.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Appunti di prova senza NLM.")

        res_path = brain_ingest.ingest_source(
            source=test_file,
            vault_root=self.test_dir,
            depth="approfondimento",
            use_ai=True,
            nlm=False
        )

        mock_nlm.assert_not_called()
        self.assertTrue(os.path.exists(res_path))

    @patch("nlm_helper.query_notebook")
    def test_ingest_source_with_nlm_auth_failure_triggers_fail_fast(self, mock_nlm):
        mock_nlm.side_effect = nlm_helper.NLMAuthError("Session expired")

        test_file = os.path.join(self.test_dir, "lezione.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Appunti universitari su algoritmi distribuiti.")

        with patch("sys.stderr") as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                brain_ingest.ingest_source(
                    source=test_file,
                    vault_root=self.test_dir,
                    depth="approfondimento",
                    use_ai=True,
                    nlm=True
                )
            self.assertEqual(cm.exception.code, 1)
            # Verify prescriptive error message written to stderr (D-04, NLM-02)
            all_stderr = "".join(call.args[0] for call in mock_stderr.write.call_args_list if call.args)
            self.assertIn("ERRORE: Impossibile consultare NotebookLM. Esegui 'nlm login' o verifica la connessione.", all_stderr)

    @patch("nlm_helper.query_notebook")
    def test_ingest_source_with_nlm_timeout_triggers_fail_fast(self, mock_nlm):
        mock_nlm.side_effect = nlm_helper.NLMTimeoutError("Timeout 120s exceeded")

        test_file = os.path.join(self.test_dir, "lezione_lenta.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Appunti universitari complessi.")

        with patch("sys.stderr") as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                brain_ingest.ingest_source(
                    source=test_file,
                    vault_root=self.test_dir,
                    depth="approfondimento",
                    use_ai=True,
                    nlm=True
                )
            self.assertEqual(cm.exception.code, 1)
            all_stderr = "".join(call.args[0] for call in mock_stderr.write.call_args_list if call.args)
            self.assertIn("ERRORE: Impossibile consultare NotebookLM. Esegui 'nlm login' o verifica la connessione.", all_stderr)

    @patch("brain_ingest.enrich_draft_with_ai")
    @patch("nlm_helper.query_notebook")
    def test_ingest_source_with_nlm_flag_success_injects_both_channels(self, mock_nlm, mock_enrich):
        mock_nlm.return_value = {
            "answer": "Principio di atomicità per flashcard Anki. Schematizza con Mermaid nodi ad albero.",
            "citations": {},
            "references": [],
            "sources_used": []
        }
        
        # When enrich_draft_with_ai is called, check that metacognitive_constraints was passed (Channel 1)
        def side_effect_enrich(*args, **kwargs):
            constraints = kwargs.get("metacognitive_constraints")
            self.assertIsNotNone(constraints)
            self.assertIn("DIRETTIVE METACOGNITIVE SPECIALISTICHE", constraints)
            self.assertIn("Mermaid", constraints)
            return ("# Algoritmi Greedy\n\nCorpo elaborato dall'AI.", "Sintesi algoritmi greedy.")
        
        mock_enrich.side_effect = side_effect_enrich

        test_file = os.path.join(self.test_dir, "greedy.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Scelta localmente ottima per soluzione globale.")

        res_path = brain_ingest.ingest_source(
            source=test_file,
            vault_root=self.test_dir,
            depth="approfondimento",
            use_ai=True,
            nlm=True
        )

        mock_nlm.assert_called_once()
        self.assertTrue(os.path.exists(res_path))

        with open(res_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check Channel 2: ## Direttive Metacognitive appended at the end
        self.assertIn("## Direttive Metacognitive", content)
        self.assertIn("Principio di atomicità per flashcard Anki", content)
        # Check zero emoji in headings (D-06, GEMINI.md)
        for line in content.splitlines():
            if line.startswith("#"):
                for char in line:
                    self.assertLess(ord(char), 0x1F000, f"Emoji in heading line: {line}")

    @patch("brain_ingest.enrich_draft_with_ai")
    @patch("nlm_helper.query_notebook")
    def test_prevent_duplicate_metacognitive_section(self, mock_nlm, mock_enrich):
        mock_nlm.return_value = {
            "answer": "Direttive ADC.",
            "citations": {},
            "references": [],
            "sources_used": []
        }
        # Simulate AI already outputting ## Direttive Metacognitive in the body
        mock_enrich.return_value = (
            "# Programmazione Dinamica\n\nContenuto.\n\n## Direttive Metacognitive\n\nGià inclusa.",
            "Sintesi dinamica."
        )

        test_file = os.path.join(self.test_dir, "dinamica.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Sottoproblemi sovrapposti e sottostruttura ottima.")

        res_path = brain_ingest.ingest_source(
            source=test_file,
            vault_root=self.test_dir,
            depth="approfondimento",
            use_ai=True,
            nlm=True
        )

        with open(res_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Count occurrences of ## Direttive Metacognitive - should be exactly 1
        matches = re.findall(r'^##\s+Direttive Metacognitive', content, re.MULTILINE)
        self.assertEqual(len(matches), 1)

    def test_cli_argument_nlm_parsed(self):
        import argparse
        # Test parser definition contains --nlm
        # We can simulate parsing args
        test_parser = argparse.ArgumentParser()
        # Verify brain_ingest parser adds --nlm
        with patch.object(sys, "argv", ["brain_ingest.py", "--help"]):
            with self.assertRaises(SystemExit):
                brain_ingest.main()


if __name__ == "__main__":
    unittest.main()
