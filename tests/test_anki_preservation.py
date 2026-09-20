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


if __name__ == "__main__":
    unittest.main()
