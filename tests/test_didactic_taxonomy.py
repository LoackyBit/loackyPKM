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

    def test_full_academic_stem_note_compliance_end_to_end(self):
        """Asserts a full realistic STEM university note passes audit_academic_note_compliance with zero issues (TAX-01, TAX-02, TAX-03, D-01, D-02, D-03, D-04, D-06, D-07)."""
        full_note = r"""# Elettrotecnica - Risonanza RLC e Teoremi di Rete
[[Home MOC|Home]] / [[University|University MOC]] / [[Elettrotecnica MOC]] / [[Elettrotecnica - Risonanza RLC e Teoremi di Rete]]

## Sintesi Esecutiva
L'analisi dei regimi sinusoidali in risonanza consente di determinare le condizioni di minimo dell'impedenza d'ingresso nei circuiti RLC.

## Fenomenologia della Risonanza nei Circuiti RLC
La spiegazione del docente parte dalla configurazione serie. La pulsazione di risonanza <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>pulsazione naturale</b></font></mark> soddisfa l'annullamento della reattanza complessiva:
$$X(\omega) = \omega L - \frac{1}{\omega C} = 0 \implies \omega_0 = \frac{1}{\sqrt{LC}}$$

> [!quote]- Divagazione del Docente: La Guerra delle Correnti
> Durante la spiegazione il docente illustra la diatriba storica tra Edison e Tesla riguardo i vantaggi del trasporto di energia in corrente alternata ad alta tensione rispetto alla continua.

## Teoremi Fondamentali e Semplificazione di Bipoli
Nel passaggio all'analisi delle reti complesse, il docente formalizza la riduzione equivalente:

> [!example] Teorema di Thévenin
> Qualsiasi rete lineare vista da due morsetti può essere sostituita da un generatore ideale di tensione in serie a un'impedenza equivalente:
> $$V_{AB} = V_{\text{th}} - Z_{\text{th}} \cdot I$$
> - **Ipotesi:** Rete lineare a costanti concentrate operante in regime sinusoidale permanente.
> - **Condizioni di validità:** Risposta lineare garantita nell'intero campo operativo; generatori dipendenti inclusi purché lineari.
> - **Significato dei simboli:**
>   - $V_{AB}$: tensione a vuoto tra i morsetti $[\text{V}]$
>   - $V_{\text{th}}$: tensione a vuoto equivalente $[\text{V}]$
>   - $Z_{\text{th}}$: impedenza equivalente interna $[\Omega]$
>   - $I$: corrente erogata al bipolo di carico $[\text{A}]$
> - **Esempio operativo:** Calcolo della corrente erogata a un carico ad impedenza variabile massimizzando il trasferimento di potenza attiva.

```mermaid
flowchart TD
    A["Rete Attiva Lineare con Morsetti A-B"] --> B["Calcolo Tensione a Vuoto Vth"]
    A --> C["Spegnimento Generatori Indipendenti"]
    C --> D["Calcolo Impedenza Equivalente Zth"]
    B --> E["Circuito Equivalente di Thevenin"]
    D --> E
```

La valutazione dei parametri di merito mette a confronto la configurazione serie e parallelo mediante la <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>larghezza di banda a -3dB</b></font></mark>:

| Parametro | RLC Serie | RLC Parallelo |
|:---|:---|:---|
| Pulsazione $\omega_0$ | $1/\sqrt{LC}$ | $1/\sqrt{LC}$ |
| Fattore di Merito $Q$ | $\frac{\omega_0 L}{R}$ | $\frac{R}{\omega_0 L}$ |
| Larghezza di Banda $B$ | $\frac{R}{L}$ | $\frac{1}{RC}$ |
"""
        audit_res = brain_health.audit_academic_note_compliance(full_note)
        self.assertTrue(audit_res["compliant"], f"Audit failed with issues: {audit_res['issues']}")
        self.assertEqual(len(audit_res["issues"]), 0)
        self.assertTrue(audit_res["features"]["has_stem_callout"])
        self.assertTrue(audit_res["features"]["has_highlights"])
        self.assertTrue(audit_res["features"]["has_yellow_mark"])
        self.assertTrue(audit_res["features"]["has_purple_mark"])
        self.assertTrue(audit_res["features"]["has_mermaid"])
        self.assertTrue(audit_res["features"]["has_digression"])

    def test_ai_enrichment_sanitization_pipeline(self):
        """Asserts AI enrichment post-sanitization pipeline produces 100% compliant output audited by brain_health."""
        mock_ai_response = r"""# 💡 Macchine Elettriche e Trasformatori

## ⚙️ Funzionamento del Trasformatore Ideale
Nel trasformatore ideale il <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>flusso magnetico comune</b></font></mark> concatena primario e secondario.
`<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>rapporto di trasformazione k</b></font></mark>`: costante del dispositivo.

Calcolo algebrico della fem indotta:
$$e_1(t) = -N_1 \frac{d\Phi}{dt}$$

> [!quote]- Divagazione del Docente: Aneddoto su Faraday
> Il docente cita l'esperimento originale di Faraday dell'anello d'induzione nel 1831.

> [!example] Legge dell'Induzione Elettromagnetica di Faraday-Neumann
> La forza elettromotrice indotta in un circuito chiuso è pari all'opposto della variazione temporale del flusso concatenato:
> $$\mathcal{E} = -\frac{d\Phi_B}{dt}$$
> - **Ipotesi:** Circuito filiforme stazionario immerso in un campo magnetico variabile nel tempo.
> - **Condizioni di validità:** Velocità del mezzo trascurabile rispetto alla velocità della luce nel vuoto; assenza di effetti relativistici.
> - **Significato dei simboli:**
>   - $\mathcal{E}$: forza elettromotrice indotta $[\text{V}]$
>   - $\Phi_B$: flusso magnetico concatenato $[\text{Wb}]$
>   - $t$: variabile temporale $[\text{s}]$
> - **Esempio operativo:** Calcolo della fem indotta ai morsetti di una bobina con $N=500$ spire sottoposta a campo sinusoidale a $50\text{ Hz}$.

```mermaid
flowchart TD
    A["Tensione Primaria V1(t)"] --> B["Flusso Magnetico nel Nucleo"]
    B --> C["Tensione Indotta Secondaria V2(t)"]
```

## 🔗 Collegamenti
- [[Elettrotecnica]]
- [[Fisica]]

---SUMMARY---
Modello ideale del trasformatore monofase e formulazione della legge di Faraday-Neumann con rapporto di trasformazione.
"""
        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = mock_ai_response
            mock_run.return_value = mock_proc

            body, summary = brain_ingest.enrich_draft_with_ai(
                self.test_dir,
                "Macchine Elettriche e Trasformatori",
                "Appunti sul trasformatore",
                depth="approfondimento"
            )

            audit_res = brain_health.audit_academic_note_compliance(body)
            self.assertTrue(audit_res["compliant"], f"Post-sanitization note failed compliance: {audit_res['issues']}")
            self.assertEqual(len(audit_res["issues"]), 0)
            self.assertIn("Modello ideale del trasformatore monofase", summary)


if __name__ == "__main__":
    unittest.main()
