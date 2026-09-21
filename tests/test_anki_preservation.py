#!/usr/bin/env python3
"""Test Suite for Anki Helper, Flashcard Syntax, MathJax Conversion,
AST Extraction, and ID Preservation (ANKI-01, ANKI-02, ANKI-03, D-01..D-18).
"""

import os
import sys
import shutil
import tempfile
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import anki_helper
import brain_health
import brain_ingest
from unittest.mock import patch, MagicMock


class TestAnkiSyntax(unittest.TestCase):
    """Verifies MathJax LaTeX conversion and callout card formatting (Task 17-01-01)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_inline_math_conversion(self):
        text = "L'energia è definita come $E = mc^2$ secondo la relatività."
        converted = anki_helper.convert_math_to_anki(text)
        self.assertIn("[$]E = mc^2[/$]", converted)
        self.assertNotIn("$E = mc^2$", converted)

    def test_display_math_conversion(self):
        text = "Formula di Gauss:\n$$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$$"
        converted = anki_helper.convert_math_to_anki(text)
        self.assertIn("[$$]\\sum_{i=1}^n i = \\frac{n(n+1)}{2}[/$$]", converted)
        self.assertNotIn("$$\\sum", converted)
        self.assertNotIn("2$$", converted)

    def test_multiline_display_flattening(self):
        text = "$$\\begin{aligned}\na &= b + c \\\\\nx &= y\n\\end{aligned}$$"
        converted = anki_helper.convert_math_to_anki(text)
        self.assertIn("[$$]", converted)
        self.assertIn("[/$$]", converted)
        # Verify no raw newline inside the [$$] block
        math_block = converted[converted.index("[$$]"):converted.index("[/$$]") + 5]
        self.assertNotIn("\n", math_block)

    def test_bare_pipe_escaping(self):
        text = "La cardinalità è $|V| + |E|$ in tempo $O(|V|)$."
        converted = anki_helper.convert_math_to_anki(text)
        self.assertIn(r"[$]\vert V\vert + \vert E\vert[/$]", converted)
        self.assertIn(r"[$]O(\vert V\vert)[/$]", converted)
        self.assertNotIn("|V|", converted)

    def test_cloze_spacing_protection(self):
        text = r"[$]\frac{ {{c1::A}} }{B}[/$]"
        converted = anki_helper.convert_math_to_anki(text)
        self.assertIn(r"{ {{c1::A}} }", converted)

    def test_avoid_double_conversion(self):
        text = "Già convertito: [$]E = mc^2[/$] e [$$]\\int x dx[/$$]."
        converted = anki_helper.convert_math_to_anki(text)
        self.assertEqual(converted, text)

    def test_format_anki_card_basic(self):
        card = anki_helper.format_anki_card(
            concept_name="Equazioni di Maxwell",
            course_name="Fisica Generale II",
            model="Basic",
            field1_content="Qual è la prima equazione di Maxwell in forma differenziale?",
            field2_content="La legge di Gauss: $\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\varepsilon_0}$.",
            tags=["Fisica_II::Elettromagnetismo::Maxwell"],
            card_id=1726588291001
        )
        self.assertIn("> [!tip]- Flashcard: Equazioni di Maxwell", card)
        self.assertIn("> %% TARGET DECK: University::Fisica_Generale_II %%", card)
        self.assertIn("> START", card)
        self.assertIn("> Basic", card)
        self.assertIn("> Front: Qual è la prima equazione di Maxwell in forma differenziale?", card)
        self.assertIn(r"> Back: La legge di Gauss: [$]\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}[/$].", card)
        self.assertIn("> Tags: Fisica_II::Elettromagnetismo::Maxwell", card)
        self.assertIn("> <!--ID: 1726588291001-->", card)
        self.assertIn("> END", card)

    def test_format_anki_card_cloze(self):
        card = anki_helper.format_anki_card(
            concept_name="Complessità Dijkstra",
            course_name="Algoritmi e Strutture Dati",
            model="Cloze",
            field1_content="Dijkstra con min-heap binario impiega tempo {{c1::$O((|V| + |E|) \\log |V|)$}}.",
            field2_content="Con heap di Fibonacci il tempo scende a $O(|E| + |V| \\log |V|)$.",
            tags=["ASD::Grafi::Cammini_Minimi"]
        )
        self.assertIn("> [!tip]- Flashcard: Complessità Dijkstra", card)
        self.assertIn("> %% TARGET DECK: University::Algoritmi_e_Strutture_Dati %%", card)
        self.assertIn("> START", card)
        self.assertIn("> Cloze", card)
        self.assertIn("> Text: ", card)
        self.assertIn("{{c1::[$]O((\\vert V\\vert + \\vert E\\vert) \\log \\vert V\\vert)[/$]}}", card)
        self.assertIn("> Extra: ", card)
        self.assertIn("> Tags: ASD::Grafi::Cammini_Minimi", card)
        self.assertNotIn("<!--ID:", card)  # No ID when not provided
        self.assertIn("> END", card)


class TestAnkiExtraction(unittest.TestCase):
    """Verifies AST extraction of flashcards, callouts, fields, and IDs (Task 17-01-02)."""

    def test_extract_basic_card_with_id(self):
        text = """# Nota di Esempio

> [!tip]- Flashcard: Equazioni di Maxwell
> %% TARGET DECK: University::Fisica_II %%
> START
> Basic
> Front: Qual è la prima equazione di Maxwell?
> Back: La legge di Gauss: [$]\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\varepsilon_0}[/$].
> Tags: Fisica_II::Maxwell
> <!--ID: 1726588291001-->
> END

Testo successivo della nota.
"""
        cards = anki_helper.extract_anki_cards_from_text(text)
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertEqual(card["concept_name"], "Equazioni di Maxwell")
        self.assertEqual(card["deck"], "University::Fisica_II")
        self.assertEqual(card["model"], "Basic")
        self.assertEqual(card["fields"]["Front"], "Qual è la prima equazione di Maxwell?")
        self.assertEqual(card["fields"]["Back"], r"La legge di Gauss: [$]\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}[/$].")
        self.assertEqual(card["tags"], ["Fisica_II::Maxwell"])
        self.assertEqual(card["card_id"], 1726588291001)
        self.assertTrue(card["raw_block"].startswith("> [!tip]- Flashcard: Equazioni di Maxwell"))
        self.assertTrue(card["raw_block"].strip().endswith("> END"))

    def test_extract_cloze_card_without_id(self):
        text = """> [!tip]- Flashcard: Complessità Dijkstra
> %% TARGET DECK: University::Algoritmi %%
> START
> Cloze
> Text: Dijkstra impiega {{c1::[$]O((|V| + |E|) \\log |V|)[/$]}}.
> Extra: Con Fibonacci heap scende a [$]O(|E| + |V| \\log |V|)[/$].
> Tags: Algoritmi::Grafi
> END
"""
        cards = anki_helper.extract_anki_cards_from_text(text)
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertEqual(card["concept_name"], "Complessità Dijkstra")
        self.assertEqual(card["deck"], "University::Algoritmi")
        self.assertEqual(card["model"], "Cloze")
        self.assertIn("{{c1::", card["fields"]["Text"])
        self.assertIn("Fibonacci", card["fields"]["Extra"])
        self.assertIsNone(card["card_id"])

    def test_extract_multiline_fields(self):
        text = """> [!tip]- Flashcard: Definizione DFA
> %% TARGET DECK: University::Linguaggi_Formali %%
> START
> Basic
> Front: Cos'è un DFA e da cosa è composto?
> Back: Un DFA è una quintupla [$](Q, \\Sigma, \\delta, q_0, F)[/$]:
> - [$]Q[/$]: stati
> - [$]\\Sigma[/$]: alfabeto
> - [$]F[/$]: stati finali
> Tags: Linguaggi_Formali::Automi
> <!--ID: 1726588292002-->
> END
"""
        cards = anki_helper.extract_anki_cards_from_text(text)
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertIn("- [$]Q[/$]: stati", card["fields"]["Back"])
        self.assertIn("- [$]F[/$]: stati finali", card["fields"]["Back"])
        self.assertEqual(card["card_id"], 1726588292002)

    def test_extract_multiple_cards(self):
        text = """> [!tip]- Flashcard: Concetto Uno
> %% TARGET DECK: University::CorsoA %%
> START
> Basic
> Front: D1
> Back: R1
> Tags: TagA
> <!--ID: 11111-->
> END

Testo intermedio tra le carte.

> [!tip]- Flashcard: Concetto Due
> %% TARGET DECK: University::CorsoB %%
> START
> Cloze
> Text: {{c1::D2}}
> Extra: R2
> Tags: TagB
> <!--ID: 22222-->
> END
"""
        cards = anki_helper.extract_anki_cards_from_text(text)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["card_id"], 11111)
        self.assertEqual(cards[0]["concept_name"], "Concetto Uno")
        self.assertEqual(cards[1]["card_id"], 22222)
        self.assertEqual(cards[1]["concept_name"], "Concetto Due")
        # Ensure spans do not overlap
        self.assertLess(cards[0]["span"][1], cards[1]["span"][0])

    def test_extract_real_vault_fixture(self):
        test_md_path = os.path.join(PROJECT_ROOT, "test.md")
        if os.path.exists(test_md_path):
            with open(test_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            cards = anki_helper.extract_anki_cards_from_text(content)
            self.assertEqual(len(cards), 3)
            ids = [c["card_id"] for c in cards]
            self.assertIn(1718902991001, ids)
            self.assertIn(1718902991002, ids)
            self.assertIn(1718902845126, ids)

    def test_extract_multiline_comment_card(self):
        text = """> [!tip]- Flashcard: Convergenza Assoluta e Semplice
%%
TARGET DECK: University::Analisi_1
START
Basic
Front: Qual è la relazione logica tra convergenza assoluta e convergenza semplice per una serie numerica in R o C?
Back: La convergenza assoluta implica sempre la convergenza semplice ([$]\\sum \\vert a_n \\vert < +\\infty \\implies \\sum a_n \\text{ converge}[/$]).
Tags: Analisi_1::SerieNumeriche::Convergenza
END
%%
"""
        cards = anki_helper.extract_anki_cards_from_text(text)
        self.assertEqual(len(cards), 1)
        card = cards[0]
        self.assertEqual(card["concept_name"], "Convergenza Assoluta e Semplice")
        self.assertEqual(card["deck"], "University::Analisi_1")
        self.assertEqual(card["model"], "Basic")
        self.assertIn("convergenza assoluta", card["fields"]["Front"])
        self.assertIn(r"[$]\sum \vert a_n \vert < +\infty", card["fields"]["Back"])
        self.assertEqual(card["tags"], ["Analisi_1::SerieNumeriche::Convergenza"])
        self.assertTrue(card["raw_block"].strip().startswith("> [!tip]- Flashcard:"))
        self.assertTrue(card["raw_block"].strip().endswith("%%"))



class TestAnkiAudit(unittest.TestCase):
    """Verifies vault audit engine, duplicate detection, and CLI interface (Task 17-01-03)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.course_dir = os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University", "ASD")
        os.makedirs(self.course_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_detection_and_duplicates(self):
        note1_path = os.path.join(self.course_dir, "Tabelle Hash.md")
        card1 = anki_helper.format_anki_card(
            concept_name="Tabelle Hash Chaining",
            course_name="Algoritmi",
            model="Basic",
            field1_content="Domanda 1",
            field2_content="Risposta 1",
            card_id=99001
        )
        with open(note1_path, "w", encoding="utf-8") as f:
            f.write(f"# Note 1\n\n{card1}\n")

        note2_path = os.path.join(self.course_dir, "Alberi Binari.md")
        card2 = anki_helper.format_anki_card(
            concept_name="Ricerca BST",
            course_name="Algoritmi",
            model="Cloze",
            field1_content="Testo {{c1::cloze}}",
            field2_content="Extra 2"
            # pending, no ID
        )
        with open(note2_path, "w", encoding="utf-8") as f:
            f.write(f"# Note 2\n\n{card2}\n")

        note3_path = os.path.join(self.course_dir, "Heap.md")
        card3 = anki_helper.format_anki_card(
            concept_name="Heapify",
            course_name="Algoritmi",
            model="Basic",
            field1_content="Domanda 3",
            field2_content="Risposta 3",
            card_id=99001  # Duplicate of card 1!
        )
        with open(note3_path, "w", encoding="utf-8") as f:
            f.write(f"# Note 3\n\n{card3}\n")

        stats = anki_helper.audit_anki_cards(self.test_dir)
        self.assertEqual(stats["total_cards"], 3)
        self.assertEqual(stats["synced_cards"], 2)
        self.assertEqual(stats["pending_cards"], 1)
        self.assertEqual(stats["basic_count"], 2)
        self.assertEqual(stats["cloze_count"], 1)
        self.assertEqual(stats["duplicate_count"], 1)
        self.assertIn(99001, stats["duplicates"])
        self.assertEqual(len(stats["duplicates"][99001]), 2)

        # CLI audit should return 1 because duplicates exist
        exit_code = anki_helper.main(["--audit", "--vault-root", self.test_dir])
        self.assertEqual(exit_code, 1)

        # Fix duplicate in note 3
        card3_fixed = anki_helper.format_anki_card(
            concept_name="Heapify",
            course_name="Algoritmi",
            model="Basic",
            field1_content="Domanda 3",
            field2_content="Risposta 3",
            card_id=99003
        )
        with open(note3_path, "w", encoding="utf-8") as f:
            f.write(f"# Note 3\n\n{card3_fixed}\n")

        stats_fixed = anki_helper.audit_anki_cards(self.test_dir)
        self.assertEqual(stats_fixed["duplicate_count"], 0)

        # CLI audit should return 0 when clean
        exit_code_clean = anki_helper.main(["--audit", "--vault-root", self.test_dir])
        self.assertEqual(exit_code_clean, 0)

        # Test check-file CLI
        exit_code_file = anki_helper.main(["--check-file", note1_path, "--vault-root", self.test_dir])
        self.assertEqual(exit_code_file, 0)


class TestAnkiGeneration(unittest.TestCase):
    """Verifies AI prompt injection, --anki flag, and autolink masking (Task 17-02-01)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tech_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech")
        os.makedirs(self.tech_dir, exist_ok=True)
        # Create a couple of existing notes for autolinking
        with open(os.path.join(self.tech_dir, "Algoritmi.md"), "w", encoding="utf-8") as f:
            f.write("---\ntitle: Algoritmi\nstatus: permanent\ntype: concept\narea: tech\ntags: [tech/algo]\n---\n# Algoritmi\n")
        with open(os.path.join(self.tech_dir, "Dijkstra.md"), "w", encoding="utf-8") as f:
            f.write("---\ntitle: Dijkstra\nstatus: permanent\ntype: concept\narea: tech\ntags: [tech/algo]\n---\n# Dijkstra\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_autolink_masks_anki_callouts(self):
        body = """Questa sezione introduce Dijkstra e Algoritmi nel testo ordinario.

> [!tip]- Flashcard: Dijkstra
> %% TARGET DECK: University::Algoritmi %%
> START
> Basic
> Front: Come funziona Dijkstra per trovare i cammini minimi?
> Back: Algoritmi con min-heap binario.
> Tags: Algoritmi::Grafi
> END

Testo finale con menzione di Algoritmi.
"""
        linked, links = brain_ingest.autolink_content(self.test_dir, body, "Grafi")
        # Outside callout, words should be autolinked
        self.assertIn("[[Dijkstra]]", linked)
        self.assertIn("[[Algoritmi]]", linked)

        # Extract the callout from the linked result
        callout_start = linked.index("> [!tip]- Flashcard: Dijkstra")
        callout_end = linked.index("> END") + 5
        callout_text = linked[callout_start:callout_end]

        # Inside the callout, words MUST NOT be converted to wikilinks
        self.assertNotIn("[[Dijkstra]]", callout_text)
        self.assertNotIn("[[Algoritmi]]", callout_text)
        self.assertIn("Come funziona Dijkstra", callout_text)
        self.assertIn("Algoritmi con min-heap", callout_text)

    def test_autolink_masks_mathjax_delimiters(self):
        body = "Formula inline: [$]f(x) con Algoritmi[/$] e display: [$$]\\sum Algoritmi[/$$]."
        linked, _ = brain_ingest.autolink_content(self.test_dir, body, "Titolo")
        self.assertNotIn("[[Algoritmi]]", linked)
        self.assertIn("[$]f(x) con Algoritmi[/$]", linked)
        self.assertIn("[$$]\\sum Algoritmi[/$$]", linked)

    @patch('subprocess.run')
    def test_enrich_draft_with_ai_prompt_generation(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="# Titolo Nota\nContenuto\n---SUMMARY---\nSintesi esecutiva.")

        # Test with enable_anki=True
        brain_ingest.enrich_draft_with_ai(
            self.test_dir, "Titolo Nota", "Contenuto sorgente",
            enable_anki=True, course_name="Linguaggi Formali"
        )
        self.assertTrue(mock_run.called)
        call_args = mock_run.call_args[0][0]
        prompt_arg = [arg for arg in call_args if arg.startswith("--print=")][0]

        self.assertIn("7. GENERAZIONE FLASHCARD ANKI CONTESTUALI", prompt_arg)
        self.assertIn("TARGET DECK: University::Linguaggi_Formali", prompt_arg)
        self.assertIn("> [!tip]- Flashcard:", prompt_arg)

        # Test with enable_anki=False
        mock_run.reset_mock()
        brain_ingest.enrich_draft_with_ai(
            self.test_dir, "Titolo Nota", "Contenuto sorgente",
            enable_anki=False
        )
        call_args_no_anki = mock_run.call_args[0][0]
        prompt_arg_no_anki = [arg for arg in call_args_no_anki if arg.startswith("--print=")][0]
        self.assertNotIn("7. GENERAZIONE FLASHCARD ANKI CONTESTUALI", prompt_arg_no_anki)


class TestAnkiPreservation(unittest.TestCase):
    """Verifies bi-phase ID realignment, orphan preservation, bitwise guard, and dashboard section (Task 17-02-02 & 17-02-03)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech")
        os.makedirs(self.atlas_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_reinject_anki_cards_exact_match(self):
        orig_content = """# Automi a Stati Finiti

> [!tip]- Flashcard: Definizione DFA
> %% TARGET DECK: University::Linguaggi_Formali %%
> START
> Basic
> Front: Cos'è un DFA?
> Back: Quintupla formale.
> Tags: LF::Automi
> <!--ID: 1726588291001-->
> END
"""
        new_content = """# Automi a Stati Finiti

Rielaborazione migliorata.

> [!tip]- Flashcard: Definizione DFA
> %% TARGET DECK: University::Linguaggi_Formali %%
> START
> Basic
> Front: Cos'è un automa a stati finiti deterministico (DFA)?
> Back: Modello descritto da quintupla formale.
> Tags: LF::Automi
> END
"""
        realigned = anki_helper.reinject_anki_cards(orig_content, new_content)
        self.assertIn("> <!--ID: 1726588291001-->", realigned)
        cards = anki_helper.extract_anki_cards_from_text(realigned)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["card_id"], 1726588291001)

    def test_reinject_anki_cards_fuzzy_match(self):
        orig_content = """> [!tip]- Flashcard: Complessità Algoritmo Dijkstra
> %% TARGET DECK: University::Algoritmi %%
> START
> Basic
> Front: Qual è la complessità temporale di Dijkstra con heap binario?
> Back: Tempo O((V + E) log V).
> Tags: Algoritmi::Grafi
> <!--ID: 1726588292002-->
> END
"""
        new_content = """> [!tip]- Flashcard: Tempo Asintotico Dijkstra
> %% TARGET DECK: University::Algoritmi %%
> START
> Basic
> Front: Qual è la complessità temporale di Dijkstra con heap binario per grafi?
> Back: Il tempo è O((V + E) log V).
> Tags: Algoritmi::Grafi
> END
"""
        realigned = anki_helper.reinject_anki_cards(orig_content, new_content)
        cards = anki_helper.extract_anki_cards_from_text(realigned)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["card_id"], 1726588292002)

    def test_reinject_preserves_unmatched_orphans(self):
        orig_content = """> [!tip]- Flashcard: Card Conservata
> START
> Basic
> Front: Domanda 1
> Back: Risposta 1
> <!--ID: 3001-->
> END

> [!tip]- Flashcard: Card Rimossa
> START
> Basic
> Front: Domanda 2 che non esiste più
> Back: Risposta 2
> <!--ID: 3002-->
> END
"""
        new_content = """> [!tip]- Flashcard: Card Conservata
> START
> Basic
> Front: Domanda 1
> Back: Risposta 1
> END
"""
        realigned = anki_helper.reinject_anki_cards(orig_content, new_content)
        self.assertIn("## Flashcard Archiviate (Preservazione ID Anki)", realigned)
        self.assertIn("<!--ID: 3002-->", realigned)
        cards = anki_helper.extract_anki_cards_from_text(realigned)
        ids = [c["card_id"] for c in cards]
        self.assertIn(3001, ids)
        self.assertIn(3002, ids)

    def test_reinject_leaves_new_cards_without_id(self):
        orig_content = """> [!tip]- Flashcard: Card Vecchia
> START
> Basic
> Front: D1
> Back: R1
> <!--ID: 4001-->
> END
"""
        new_content = """> [!tip]- Flashcard: Card Vecchia
> START
> Basic
> Front: D1
> Back: R1
> END

> [!tip]- Flashcard: Card Totalmente Nuova
> START
> Cloze
> Text: Testo {{c1::inedito}}
> Extra: Extra
> END
"""
        realigned = anki_helper.reinject_anki_cards(orig_content, new_content)
        cards = anki_helper.extract_anki_cards_from_text(realigned)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["card_id"], 4001)
        self.assertIsNone(cards[1]["card_id"])

    def test_lint_file_preserves_anki_ids(self):
        note_path = os.path.join(self.atlas_dir, "Test Linter Anki.md")
        card = anki_helper.format_anki_card(
            concept_name="Integrità",
            course_name="Sistemi",
            model="Basic",
            field1_content="Domanda",
            field2_content="Risposta",
            card_id=1726588299999
        )
        raw_note = f"""---
title: Test Linter Anki
area: tech
tags: [tech/systems]
---
# Test Linter Anki

{card}
"""
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(raw_note)

        # Run lint_file with execute=True
        modified, new_c = brain_health.lint_file(note_path, vault_root=self.test_dir, execute=True)
        self.assertTrue(modified)
        with open(note_path, "r", encoding="utf-8") as f:
            saved_content = f.read()

        self.assertIn("<!--ID: 1726588299999-->", saved_content)
        cards = anki_helper.extract_anki_cards_from_text(saved_content)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["card_id"], 1726588299999)

    def test_lint_file_aborts_on_id_tampering(self):
        note_path = os.path.join(self.atlas_dir, "Tamper Note.md")
        card = anki_helper.format_anki_card(
            concept_name="Integrità",
            course_name="Sistemi",
            model="Basic",
            field1_content="Domanda",
            field2_content="Risposta",
            card_id=1726588277777
        )
        content = f"# Tamper Note\n\n{card}\n"
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Simulate tampering where assemble_markdown_note strips the ID
        with patch('brain_health.assemble_markdown_note', return_value="# Tamper Note\n\nCard without ID\n"):
            modified, ret_content = brain_health.lint_file(note_path, vault_root=self.test_dir, execute=True)
            self.assertFalse(modified)
            with open(note_path, "r", encoding="utf-8") as f:
                disk_content = f.read()
            # File on disk must remain unchanged with ID intact
            self.assertIn("<!--ID: 1726588277777-->", disk_content)

    def test_dashboard_contains_anki_integrity_section(self):
        dashboard = brain_health.generate_health_dashboard(self.test_dir, notes_data=[], audit_stats={})
        self.assertIn("## Integrità Flashcard Anki", dashboard)
        self.assertIn("Flashcard Totali", dashboard)
        self.assertIn("Flashcard Sincronizzate", dashboard)
        self.assertIn("Flashcard Inedite", dashboard)


class TestAnkiFormatSanitizationAndValidation(unittest.TestCase):
    """Tests for flashcard sanitization and validation complying with official Anki documentation."""

    def test_sanitize_math_derivatives(self):
        raw = "Consideriamo $f'(x) = 2x$ e $f''(t) = a$ e $f'(\\xi)(b - a)$ e $$g'(u) = 1$$. L'insieme dell'operatore."
        sanitized = anki_helper.sanitize_math_derivatives(raw)
        self.assertIn(r"$f^\prime(x) = 2x$", sanitized)
        self.assertIn(r"$f^{\prime\prime}(t) = a$", sanitized)
        self.assertIn(r"$f^\prime(\xi)(b - a)$", sanitized)
        self.assertIn(r"$$g^\prime(u) = 1$$", sanitized)
        self.assertIn("L'insieme dell'operatore", sanitized)

    def test_sanitize_flashcard_text(self):
        raw_card = """> [!tip]- Flashcard: Teorema Test
> %%
> TARGET DECK: University::Analisi_1
> START
> cloze
> text: Enunciato con {{c1:termine errato}} e formula $f'(x) = |x|$.
> tags: Analisi_1::Test
> END
> %%"""
        sanitized = anki_helper.sanitize_flashcard_text(raw_card)
        self.assertIn("Cloze", sanitized)
        self.assertIn("Text: Enunciato con {{c1::termine errato}}", sanitized)
        self.assertIn(r"$f^\prime(x) = \vert x\vert$", sanitized)
        self.assertIn("Tags: Analisi_1::Test", sanitized)
        # Verify no leading '>' inside the %% ... %% block
        lines = sanitized.splitlines()
        self.assertTrue(lines[0].startswith("> [!tip]- Flashcard:"))
        for inner in lines[1:]:
            self.assertFalse(inner.strip().startswith(">"), f"Line still has leading quote: {inner}")

    def test_validate_flashcard_text(self):
        valid_card = r"""> [!tip]- Flashcard: Valid Card
%%
TARGET DECK: University::Analisi_1
START
Cloze
Text: Formula corretta {{c1::$f^\prime(x) = 2x$}}.
Extra: Note
Tags: Analisi_1::Test
END
%%"""
        errors = anki_helper.validate_flashcard_text(valid_card)
        self.assertEqual(errors, [])

        invalid_card = """> [!tip]- Flashcard: Bad Card
%%
START
Cloze
Text: Formula con errore {{c1:singolo due punti}} e $f'(x) = 2x$.
END
%%"""
        errs = anki_helper.validate_flashcard_text(invalid_card)
        self.assertTrue(any("TARGET DECK" in e for e in errs))
        self.assertTrue(any("single-colon" in e for e in errs))
        self.assertTrue(any("prime" in e for e in errs))

    def test_sanitize_all_flashcards(self):
        full_note = """# Nota di Prova

Introduzione concettuale alla materia.

> [!tip]- Flashcard: Derivata
> %%
> TARGET DECK: University::Analisi_1
> START
> cloze
> text: La derivata è {{c1:$f'(x)$}}.
> tags: Analisi_1::Derivate
> END
> %%

Trattazione successiva senza alterazioni dell'apostrofo.
"""
        result = anki_helper.sanitize_all_flashcards(full_note)
        self.assertIn(r"{{c1::$f^\prime(x)$}}", result)
        self.assertIn("Trattazione successiva senza alterazioni dell'apostrofo.", result)


if __name__ == "__main__":
    unittest.main()

