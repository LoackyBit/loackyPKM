import unittest
import os
import sys
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".agents", "skills", "meta", "scripts"))

import backfill_summaries

class TestBackfillSummaries(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.checkpoint_file = os.path.join(self.test_dir, "99 - Meta", ".backfill_checkpoint.json")
        os.makedirs(os.path.dirname(self.checkpoint_file), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_checkpoint_persistence_and_resume(self):
        """Asserts CheckpointManager saves progress to JSON atomically and skips previously completed notes on subsequent runs per D-20."""
        cm = backfill_summaries.CheckpointManager(self.test_dir)
        self.assertFalse(cm.is_completed("02 - Atlas/Tech/Note.md"))

        cm.record_success("02 - Atlas/Tech/Note.md", "Sintesi concettuale esecutiva della nota.")
        self.assertTrue(cm.is_completed("02 - Atlas/Tech/Note.md"))
        self.assertTrue(os.path.exists(self.checkpoint_file))

        # Reload from disk
        cm2 = backfill_summaries.CheckpointManager(self.test_dir)
        self.assertTrue(cm2.is_completed("02 - Atlas/Tech/Note.md"))
        self.assertEqual(cm2.data["completed"]["02 - Atlas/Tech/Note.md"]["summary"], "Sintesi concettuale esecutiva della nota.")

    def test_summary_prompt_formatting(self):
        """Asserts summary prompt enforces 1-2 dense sentences between 120 and 180 characters (max 200) without fluff phrases per D-10."""
        prompt = backfill_summaries.build_summary_prompt("Architetture LLM", "Corpo della nota su RAG e modelli linguistici.", lang="it")
        self.assertIn("Architetture LLM", prompt)
        self.assertIn("120 e 180 caratteri", prompt)
        self.assertIn("MAI iniziare con", prompt)
        self.assertIn("RESTITUISCI ESCLUSIVAMENTE", prompt.upper())

    def test_summary_language_alignment(self):
        """Asserts Italian prompt instructions for Italian notes and English instructions for English notes per D-12."""
        it_prompt = backfill_summaries.build_summary_prompt("Reti Neurali", "Questo testo e in italiano con parole chiave.", lang="it")
        self.assertIn("italiano", it_prompt.lower())

        en_prompt = backfill_summaries.build_summary_prompt("Neural Networks", "This text is written in english about deep learning.", lang="en")
        self.assertIn("english", en_prompt.lower())

    def test_summary_scalar_serialization(self):
        """Asserts summary is stored as a double-quoted string with character escaping per D-13."""
        sample_note = """---
status: permanent
type: concept
area: tech
title: "Nota Test Summary"
date: 2026-02-01
---
[[Home MOC|Home]] / [[Tech MOC]] / [[Nota Test Summary]]

# Nota Test Summary

Corpo del testo della nota di test.
"""
        note_path = os.path.join(self.test_dir, "Nota Test Summary.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(sample_note)

        summary_text = 'Sintesi con caratteri "speciali" e citazioni.'
        changed, new_content = backfill_summaries.inject_summary_into_note(note_path, summary_text, vault_root=self.test_dir, execute=True)
        self.assertTrue(changed)
        self.assertIn('summary: "Sintesi con caratteri \\"speciali\\" e citazioni."', new_content)

    def test_special_cases_handling(self):
        """Asserts template files in 99 - Meta/Template/ are excluded, MOCs receive structural index summaries, and Daily notes receive journal summaries per D-18."""
        self.assertTrue(backfill_summaries.should_skip_path("99 - Meta/Template/Global Note.md"))
        self.assertFalse(backfill_summaries.should_skip_path("02 - Atlas/Tech/AI Note.md"))

        moc_summary = backfill_summaries.get_special_summary("01 - Map of Content/Tech MOC.md", "Tech MOC", "")
        self.assertEqual(moc_summary, "Indice e mappa concettuale per Tech MOC.")

        daily_summary = backfill_summaries.get_special_summary("04 - Calendar/DailyNote - 20260201.md", "DailyNote - 20260201", "")
        self.assertEqual(daily_summary, "Diario giornaliero e tracciamento delle attività del 20260201.")

    def test_heuristic_fallback(self):
        """Asserts offline/timeout fallback extracts dense opening sentences capped at 197 chars + '...' when LLM is unavailable."""
        long_body = "Prima riga descrittiva molto lunga che contiene moltissimi dettagli sul funzionamento dell'architettura e deve essere troncata adeguatamente qualora superi la soglia massima consentita di caratteri per il formato summary. Ulteriore testo."
        fallback = backfill_summaries.generate_heuristic_fallback("Titolo", long_body)
        self.assertLessEqual(len(fallback), 200)
        self.assertTrue(fallback.endswith("..."))

if __name__ == "__main__":
    unittest.main()
