import unittest
import os
import sys
import re
import tempfile
import shutil
from unittest.mock import patch, MagicMock

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import brain_ingest
import brain_health


class TestDidacticTaxonomy(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.environ.pop("BRAIN_INGEST_NO_AI", None)

    def tearDown(self):
        os.environ.pop("BRAIN_INGEST_NO_AI", None)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_stem_formulary_callout_structure(self):
        """Asserts STEM formulas have intermediate $$...$$ and key theorems in callouts with hypotheses, validity, SI symbols, examples (TAX-02, D-04, D-05, D-08, D-09)."""
        sample_note = r"""# Elettrotecnica - Teoremi Fondamentali

Calcolo intermedio della corrente di maglia:
$$I_m = \frac{E_1 - E_2}{R_1 + R_2}$$

> [!example] Teorema di Thévenin
> Qualsiasi rete lineare vista da due morsetti può essere sostituita da un generatore equivalente:
> $$V_{AB} = V_{\text{th}} - R_{\text{th}} \cdot I$$
> - **Ipotesi:** Rete lineare a parametri concentrati costituita da elementi ideali.
> - **Condizioni di validità:** Regime stazionario o quasi-stazionario; risposta lineare garantita nell'intero campo operativo.
> - **Significato dei simboli:**
>   - $V_{AB}$: tensione a vuoto tra i morsetti $[\text{V}]$
>   - $V_{\text{th}}$: tensione a vuoto equivalente $[\text{V}]$
>   - $R_{\text{th}}$: resistenza equivalente vista dai morsetti $[\Omega]$
>   - $I$: corrente erogata al carico $[\text{A}]$
> - **Esempio operativo:** Calcolo della corrente su carico variabile in ponte di Wheatstone.
"""
        # 1. Verifica presenza calcolo intermedio display $$...$$
        self.assertRegex(sample_note, r'\$\$[\s\S]*?I_m[\s\S]*?\$\$')

        # 2. Verifica callout teorema con i 5 elementi obbligatori (D-04, D-08)
        self.assertRegex(sample_note, r'>\s*\[!(?:example|info)\]\s+Teorema')
        self.assertIn("- **Ipotesi:**", sample_note)
        self.assertIn("- **Condizioni di validità:**", sample_note)
        self.assertIn("- **Significato dei simboli:**", sample_note)
        self.assertIn("- **Esempio operativo:**", sample_note)

        # 3. Verifica unità di misura SI esplicitate (D-09)
        self.assertRegex(sample_note, r'\[\\text\{[A-Za-z\u03a9/\\cdot\s]+\}\]|\[\\Omega\]|\[\u03a9\]|\[V\]|\[A\]')

        # 4. Disaccoppiamento da Anki (D-05): formule in MathJax naturale puro, nessun blocco ```latex
        self.assertNotRegex(sample_note, r'```latex')
        self.assertNotRegex(sample_note, r'\{\{c\d+::')

        # 5. Verifica che il prompt AI contenga le istruzioni vincolate per formulari STEM
        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = f"# Elettrotecnica\n\n{sample_note}\n\n---SUMMARY---\nTrattazione approfondita dei teoremi di rete lineare."
            mock_run.return_value = mock_proc

            brain_ingest.enrich_draft_with_ai(self.test_dir, "Elettrotecnica", "Spiegazione teorema di Thevenin")
            self.assertTrue(mock_run.called)
            sent_prompt = mock_run.call_args[0][0][-1]  # --print=<prompt>
            self.assertIn("FORMULARIO STEM VINCOLATO E FORMALISMO MATEMATICO", sent_prompt)
            self.assertIn("Ipotesi:", sent_prompt)
            self.assertIn("Condizioni di validità:", sent_prompt)
            self.assertIn("Significato dei simboli:", sent_prompt)
            self.assertIn("Esempio operativo:", sent_prompt)
            self.assertIn("DIVIETO DI BACKTICK PER FORMULE", sent_prompt)

    def test_chronological_sequence_and_digressions(self):
        """Asserts lecture follows chronological flow, encapsulates digressions in [!quote]-, and forbids emoji in H1-H3 (TAX-01, D-06)."""
        sample_note = """# Teoria dei Circuiti - Lezione 04
[[Home MOC|Home]] / [[University|University MOC]] / [[Elettrotecnica MOC]] / [[Teoria dei Circuiti - Lezione 04]]

## Analisi Nodale dei Circuiti Lineari
La spiegazione del docente inizia con la formulazione matriciale dell'analisi ai nodi...

> [!quote]- Divagazione del Docente: Aneddoto sulla Guerra delle Correnti
> Durante la spiegazione il docente racconta la controversia storica tra Edison e Tesla sull'adozione della corrente alternata...

## Metodo del Potenziale ai Nodi
Proseguendo nella trattazione sequenziale della lezione, si formalizza il sistema risolvente...
"""
        # 1. Zero emoji nei titoli H1-H3
        for line in sample_note.splitlines():
            if line.startswith("#"):
                for char in line:
                    self.assertLess(ord(char), 0x1F000, f"Rilevata emoji nel titolo: {line}")
                    self.assertFalse(0x2600 <= ord(char) <= 0x27BF, f"Rilevato simbolo/emoji nel titolo: {line}")

        # 2. Nessuna sezione finale ## Collegamenti
        self.assertFalse(re.search(r'^##\s+(?:🔗\s*)?(?:Collegamenti|Note Correlate|Vedi anche)', sample_note, re.MULTILINE | re.IGNORECASE))

        # 3. Incapsulamento digressioni con callout collassabile (D-06)
        self.assertRegex(sample_note, r'>\s*\[!quote\]-\s+Divagazione del Docente:')

        # 4. Verifica che il prompt AI contenga le istruzioni vincolanti per sequenza e digressioni
        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = f"# Circuito\n\n{sample_note}\n\n---SUMMARY---\nAnalisi nodale e trattazione cronologica della lezione."
            mock_run.return_value = mock_proc

            brain_ingest.enrich_draft_with_ai(self.test_dir, "Circuito", "Lezione 04 analisi nodale")
            self.assertTrue(mock_run.called)
            sent_prompt = mock_run.call_args[0][0][-1]
            self.assertIn("SEQUENZA LOGICO-TEMPORALE E DIGRESSIONI DEL DOCENTE", sent_prompt)
            self.assertIn("INCAPSULAMENTO DELLE DIGRESSIONI", sent_prompt)
            self.assertIn("[!quote]- Divagazione del Docente:", sent_prompt)
            self.assertIn("DIVIETO ASSOLUTO DI EMOJI NEI TITOLI", sent_prompt)
            self.assertIn("NESSUNA SEZIONE COLLEGAMENTI SEPARATA", sent_prompt)

    def test_visual_enrichment_and_mermaid_quotes(self):
        """Asserts <mark> tags are present without backticks, and Mermaid node labels are quoted (TAX-03, D-01, D-02, D-03)."""
        sample_note = """# Principi di Macchine Elettriche

Il principio fondante è il <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>campo magnetico rotante</b></font></mark>, scoperto da <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Galileo Ferraris</b></font></mark>.

```mermaid
flowchart TD
    A["Tensioni Trifase Simmetriche"] --> B["Correnti nelle Tre Fasi"]
    B --> C["Induzione Magnetica Risultante B(t)"]
```

| Parametro | Stella (Y) | Triangolo ($\\Delta$) |
|:---|:---|:---|
| Tensione di Fase | $V_f = V_l / \\sqrt{3}$ | $V_f = V_l$ |
"""
        # 1. Verifica evidenziazioni <mark> cromatiche obbligatorie (D-01)
        self.assertRegex(sample_note, r'<mark style="background:rgba\(255, 193, 69, 0\.32\)"><font color="#cc8800"><b>.*?</b></font></mark>')
        self.assertRegex(sample_note, r'<mark style="background:rgba\(181, 113, 255, 0\.36\)"><font color="#9a54c1"><b>.*?</b></font></mark>')

        # 2. Regola Critica: nessun backtick attorno ai tag HTML <mark>
        self.assertNotRegex(sample_note, r'`<mark[^>]*>.*?</mark>`')
        self.assertNotRegex(sample_note, r'`<font[^>]*>.*?</font>`')

        # 3. Verifica diagramma Mermaid con nodi quotati (D-03)
        mermaid_match = re.search(r'```mermaid([\s\S]*?)```', sample_note)
        self.assertIsNotNone(mermaid_match)
        for line in mermaid_match.group(1).splitlines():
            line = line.strip()
            if "-->" in line:
                matches = re.findall(r'\b[A-Za-z0-9_]+\[(.*?)\]', line)
                for label in matches:
                    self.assertTrue(label.startswith('"') and label.endswith('"'), f"Nodo non quotato: {label}")
                    self.assertNotIn("<mark>", label)

        # 4. Verifica tabella Markdown standard (D-02)
        self.assertRegex(sample_note, r'\|[\s\S]*?\|[\s\S]*?\|\n\|:?---')

        # 5. Verifica che il prompt AI contenga le istruzioni vincolanti per evidenziazioni e Mermaid
        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = f"# Macchine Elettriche\n\n{sample_note}\n\n---SUMMARY---\nCampo magnetico rotante e macchine elettriche."
            mock_run.return_value = mock_proc

            brain_ingest.enrich_draft_with_ai(self.test_dir, "Macchine Elettriche", "Contenuto macchine elettriche")
            self.assertTrue(mock_run.called)
            sent_prompt = mock_run.call_args[0][0][-1]
            self.assertIn("EVIDENZIAZIONI CROMATICHE E ARRICCHIMENTO VISIVO", sent_prompt)
            self.assertIn("#cc8800", sent_prompt)
            self.assertIn("#9a54c1", sent_prompt)
            self.assertIn("REGOLA CRITICA: Non racchiudere MAI i tag HTML <mark>", sent_prompt)
            self.assertIn("DIAGRAMMI MERMAID CONTESTUALI (NON OBBLIGATORI)", sent_prompt)
            self.assertIn("REGOLE MERMAID RIGOROSE: Tutte le etichette dei nodi DEVONO essere rigorosamente racchiuse tra doppi apici", sent_prompt)

    def test_enrich_draft_with_ai_end_to_end_sanitization(self):
        """Asserts enrich_draft_with_ai strips emoji from headers, cleans backticks from marks, and removes unwanted link sections."""
        ai_raw_output = """# 🎯 Teoria dei Segnali e Sistemi

## 📊 Sintesi Esecutiva
`<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Trasformata di Fourier</b></font></mark>`: analisi spettrale.

## 🚀 Trattazione di Dettaglio
Formalizzazione con <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>integrale di Fourier</b></font></mark>.

> [!quote]- Divagazione del Docente: Storia di Fourier
> Fourier durante la campagna d'Egitto studiò la propagazione del calore.

## 🔗 Collegamenti
- [[Segnali]]
- [[Matematica]]

---SUMMARY---
Analisi spettrale dei segnali tempo-continui e proprietà della Trasformata di Fourier.
"""
        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = ai_raw_output
            mock_run.return_value = mock_proc

            body, summary = brain_ingest.enrich_draft_with_ai(
                self.test_dir,
                "Teoria dei Segnali e Sistemi",
                "Appunti su Fourier",
                depth="approfondimento"
            )

            # Titolo H1 pulito senza emoji
            self.assertTrue(body.startswith("# Teoria dei Segnali e Sistemi\n"))

            # Titoli H2 puliti senza emoji
            self.assertIn("## Sintesi Esecutiva", body)
            self.assertNotIn("## 📊", body)
            self.assertIn("## Trattazione di Dettaglio", body)
            self.assertNotIn("## 🚀", body)

            # Tag <mark> senza backtick
            self.assertNotIn("`<mark", body)
            self.assertIn('<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Trasformata di Fourier</b></font></mark>', body)

            # Sezione Collegamenti rimossa
            self.assertNotIn("## Collegamenti", body)
            self.assertNotIn("## 🔗", body)

            # Callout digressione preservato
            self.assertIn("> [!quote]- Divagazione del Docente: Storia di Fourier", body)

            # Summary estratto correttamente
            self.assertEqual(summary, "Analisi spettrale dei segnali tempo-continui e proprietà della Trasformata di Fourier.")

    def test_fallback_format_structured_note_compliance(self):
        """Asserts format_structured_note fallback respects clean headers, style highlights, and no links section."""
        note_deep = brain_ingest.format_structured_note("Fisica Sperimentale", "Legge di gravitazione universale.", depth="approfondimento")
        self.assertTrue(note_deep.startswith("# Fisica Sperimentale\n"))
        self.assertIn("## Sintesi Esecutiva", note_deep)
        self.assertIn('<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Fisica Sperimentale</b></font></mark>', note_deep)
        self.assertIn('<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>principi operativi</b></font></mark>', note_deep)
        self.assertNotIn("`<mark", note_deep)
        self.assertNotIn("## Collegamenti", note_deep)


if __name__ == "__main__":
    unittest.main()
