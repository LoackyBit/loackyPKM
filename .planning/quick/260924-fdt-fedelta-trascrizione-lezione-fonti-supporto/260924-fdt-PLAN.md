---
id: 260924-fdt
slug: fedelta-trascrizione-lezione-fonti-supporto
title: "Fedeltà alla nota originale e alla trascrizione della lezione con dispense e slide come fonti di supporto in brain-ingest"
date: 2026-09-24
type: quick-plan
status: complete
---

# Quick Plan 260924-fdt: Fedeltà alla nota originale e alla trascrizione della lezione con dispense e slide come fonti di supporto in brain-ingest

## Contesto & Requisito
Durante l'ingestione multi-sorgente con `brain-ingest` (specie per lezioni universitarie o appunti con dipendenze locali come slide PDF, dispense e trascrizioni), l'AI non deve discostarsi troppo dalla nota originale dell'utente e dalla trascrizione audio della lezione.
- **Fonte Primaria:** La nota originale e la trascrizione della lezione costituiscono l'asse portante, il filo conduttore e il perimetro tematico di ciò che è stato effettivamente affrontato.
- **Fonti di Supporto:** Le dispense, le slide PDF e gli altri appunti ausiliari hanno un ruolo rigorosamente ausiliario ("di supporto"): servono per verificare formule LaTeX, formalizzare definizioni, fornire la notazione corretta, arricchire con tabelle e schemi grafici, e ancorare i richiami di pagina (`\[[[file.pdf#page=N|Slide N]]]`), senza allargare indebitamente lo scope della lezione a interi capitoli o trattazioni enciclopediche non spiegate dal docente.

## Obiettivi
1. **Aggiornamento Prompt di Rielaborazione (`99 - Meta/Scripts/brain_ingest.py`):**
   - Esplicitare in modo categorico la gerarchia delle fonti: nota originale e trascrizione audio come asse primario vincolante, dispense/slide/altri appunti come supporto formale e visivo ausiliario.
   - Vietare divagazioni enciclopediche su argomenti presenti nelle slide/dispense ma non spiegati a lezione.
2. **Aggiornamento Etichettatura Sezioni in `resolve_inbox_dependencies` (`99 - Meta/Scripts/brain_ingest.py`):**
   - Etichettare chiaramente nei payload multi-sorgente la "NOTA ORIGINALE / CATTURA PRIMARIA", la "FONTE PRIMARIA: Trascrizione Audio Lezione", e le "FONTI DI SUPPORTO (Dispense / Slide PDF)" e "FONTI DI SUPPORTO (Altri Appunti / Note Ausiliarie)".
3. **Aggiornamento Documentazione e Regole di Sistema:**
   - `.agents/skills/brain-ingest/SKILL.md`: aggiungere la specifica della gerarchia delle fonti e ruolo di supporto.
   - `GEMINI.md`: integrare la regola di gerarchia fonti in `brain-ingest` e convenzioni operative.
   - `AGENTS.md`: riflettere la regola nel flusso operativo di ingestion e vincoli.
4. **Test Unitari di Verifica (`tests/test_brain_ingest.py`):**
   - Testare che i delimitatori delle fonti primarie e di supporto siano generati correttamente da `resolve_inbox_dependencies`.
   - Testare che il prompt di arricchimento AI contenga le istruzioni vincolanti sulla gerarchia delle fonti e sul ruolo ausiliario di dispense e slide.
5. **Completamento & Stato:**
   - Creare `260924-fdt-SUMMARY.md` e registrare il task in `.planning/STATE.md`.

## Tasks
- [x] Task 1: Aggiornare `resolve_inbox_dependencies` e prompt di `enrich_draft_with_ai` in `99 - Meta/Scripts/brain_ingest.py`
- [x] Task 2: Aggiornare la documentazione e i system prompts in `GEMINI.md`, `AGENTS.md`, `.agents/skills/brain-ingest/SKILL.md`
- [x] Task 3: Aggiungere test unitari in `tests/test_brain_ingest.py` e validare l'intera suite
- [x] Task 4: Creare `SUMMARY.md`, aggiornare `.planning/STATE.md` ed eseguire commit Git convenzionale
