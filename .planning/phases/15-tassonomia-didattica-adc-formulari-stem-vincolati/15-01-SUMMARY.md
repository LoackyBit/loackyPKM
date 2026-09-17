---
phase: 15-tassonomia-didattica-adc-formulari-stem-vincolati
plan: "01"
subsystem: ingestion
tags: [adc, didactic-taxonomy, stem, latex, mathjax, mermaid, style-guide]
requires: []
provides: [didactic-prompt-enrichment, stem-formulary-callouts, didactic-test-harness]
affects:
  - "99 - Meta/Scripts/brain_ingest.py"
  - "tests/test_didactic_taxonomy.py"
tech-stack:
  added: []
  patterns: ["hybrid-stem-callout", "collapsible-digression", "style-guide-highlights", "quoted-mermaid-nodes"]
key-files:
  created:
    - "tests/test_didactic_taxonomy.py"
  modified:
    - "99 - Meta/Scripts/brain_ingest.py"
key-decisions:
  - "D-01 & TAX-03: Evidenziazioni cromatiche Style Guide (<mark> giallo #cc8800 per cardini e viola #9a54c1 per secondari) obbligatorie su ogni nota e in puro HTML senza backtick markdown"
  - "D-02 & D-03: Palette visiva completa (callout semantici, checkbox, tabelle standard) e diagrammi causali Mermaid flowchart TD contestuali non obbligatori con nodi quotati id[\"...\"]"
  - "D-04 & TAX-02: Modello ibrido per formule STEM: calcoli intermedi in $$...$$ e teoremi/leggi cardine racchiusi in callout dedicati (> [!example] o > [!info]) con 5 sezioni obbligatorie (display LaTeX, ipotesi, validità, simboli SI, esempio operativo)"
  - "D-05: Disaccoppiamento da Anki con adozione di sintassi MathJax naturale ($...$ e $$...$$) senza escaping prematuro (demandato a Fase 17)"
  - "D-06 & TAX-01: Sequenza logico-temporale della lezione senza sezioni generiche vuote, con incapsulamento di digressioni/aneddoti del docente in callout collassabile > [!quote]- Divagazione del Docente:"
  - "D-08 & D-09: Flessibilità nella scelta del callout (> [!example] / > [!info]) e precisione sulle unità di misura SI esplicitate"
requirements-completed:
  - "TAX-01"
  - "TAX-02"
  - "TAX-03"
duration: "15 min"
completed: "2026-09-17"
coverage:
  - deliverable: "Constrained STEM Formulary Callouts (5 points, natural MathJax, SI units)"
    human_judgment: false
    verification:
      kind: "test"
      ref: "tests/test_didactic_taxonomy.py#test_stem_formulary_callout_structure"
      status: "pass"
  - deliverable: "Chronological Sequence and Collapsible Teacher Digressions ([!quote]-)"
    human_judgment: false
    verification:
      kind: "test"
      ref: "tests/test_didactic_taxonomy.py#test_chronological_sequence_and_digressions"
      status: "pass"
  - deliverable: "Mandatory Style Guide Highlights and Quoted Mermaid Node Labels"
    human_judgment: false
    verification:
      kind: "test"
      ref: "tests/test_didactic_taxonomy.py#test_visual_enrichment_and_mermaid_quotes"
      status: "pass"
  - deliverable: "End-to-end AI Enrichment Sanitization"
    human_judgment: false
    verification:
      kind: "test"
      ref: "tests/test_didactic_taxonomy.py#test_enrich_draft_with_ai_end_to_end_sanitization"
      status: "pass"
  - deliverable: "Compliant Fallback Heuristic Note Formatter"
    human_judgment: false
    verification:
      kind: "test"
      ref: "tests/test_didactic_taxonomy.py#test_fallback_format_structured_note_compliance"
      status: "pass"
---

# Plan 15-01 Summary: Regole di arricchimento didattico ADC per formule STEM vincolate e diagrammi Mermaid quotati (TAX-01, TAX-02, TAX-03)

## Execution Summary

Plan 15-01 ha integrato nel motore di ingestione del Second Brain (`99 - Meta/Scripts/brain_ingest.py`) le direttive metodologiche della Tassonomia Didattica di Alessandro de Concini (ADC) e le convenzioni visive di `Style Guide.md`:

1. **Formulari STEM Vincolati a Callout (TAX-02, D-04, D-05, D-08, D-09):**
   - Implementato l'approccio ibrido: calcoli intermedi e passaggi algebrici in blocchi display MathJax standard `$$...$$` o inline `$..$`.
   - Reclusione vincolata di teoremi, leggi fisiche e formule cardine in callout dedicati (`> [!example] Teorema / Legge: [Nome]` o `> [!info]`).
   - Obbligo tassativo dei 5 punti strutturati all'interno del callout del teorema:
     1. Espressione display LaTeX centrale `$$...$$`
     2. `- **Ipotesi:**` (assunzioni necessarie preliminari)
     3. `- **Condizioni di validità:**` (limiti operativi, regimi fisici o vincoli)
     4. `- **Significato dei simboli:**` (parametri corredati da unità di misura SI es. `$[\text{V}]$`, `$[\Omega]$`, `$[\text{A}]$`, `$[\text{m/s}^2]$`)
     5. `- **Esempio operativo:**` (caso applicativo pratico o calcolo rapido)
   - Disaccoppiamento da Anki (D-05): formule espresse unicamente in sintassi MathJax naturale senza blocchi ```` ```latex ```` o sanitizzazioni per cloze.

2. **Sequenza Logico-Temporale & Incapsulamento Digressioni (TAX-01, D-06):**
   - La trattazione segue l'ordine cronologico di esposizione del docente nella lezione, eliminando template statici prefissati o sezioni vuote.
   - Tutte le divagazioni, commenti personali e aneddoti extra-curriculari vengono incapsulati in callout collassabili dedicati `> [!quote]- Divagazione del Docente: [Oggetto]`, preservando la TOC (zero titoli H3/H4 spuri) e consentendone l'eliminazione con un singolo click in fase di review.
   - Confermati il divieto assoluto di emoji nei titoli H1-H3 e l'assorbimento organico dei wiki-link senza sezioni isolate `## Collegamenti`.

3. **Arricchimento Visivo & Mermaid Contestuale (TAX-03, D-01, D-02, D-03):**
   - Evidenziazioni cromatiche `<mark>` obbligatorie su ogni nota (giallo `#cc8800` per cardini, viola `#9a54c1` per secondari), rigorosamente in puro HTML inline senza backtick markdown.
   - Generazione contestuale (non obbligatoria) di diagrammi Mermaid `flowchart TD`: prodotti solo per reali catene causali o derivazioni complesse; nodi rigorosamente quotati tra doppi apici `id["..."]` e divieto assoluto di HTML nei nodi Mermaid.
   - Tabelle comparative Markdown standard per confronti sinottici.

4. **Test Harness Didattico (`tests/test_didactic_taxonomy.py`):**
   - Creata la suite unitaria con 5 test completi a copertura di TAX-01, TAX-02, TAX-03, sanitizzazione end-to-end e formattatore euristico di fallback.

---

## Verification Results

- Tracer per formulari STEM: `python3 -m unittest tests/test_didactic_taxonomy.py -k test_stem_formulary_callout_structure` (1 test — OK)
- Verifica sequenza e digressioni: `python3 -m unittest tests/test_didactic_taxonomy.py -k test_chronological_sequence_and_digressions` (1 test — OK)
- Suite completa tassonomia didattica: `python3 -m unittest tests/test_didactic_taxonomy.py` (5 test, 0.003s — OK)
- Regressione completa vault: `python3 -m unittest discover tests` (205 test, 13.8s — OK)

## Self-Check: PASSED
