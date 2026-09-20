---
phase: "17"
plan: "02"
subsystem: anki_pipeline
tags: [anki, brain_ingest, brain_health, preservation, autolink, bitwise-guard]
date: "2026-09-20"
---

# Phase 17 Plan 02: Pipeline Ingestione, Prompt AI ADC, Protezione Autolink, Riallineamento Bi-Fase ID & Barriera Bitwise — Summary

Completata l'infrastruttura di generazione e preservazione Anki integrando arricchimento concettuale AI in `brain_ingest.py`, mascheramento in `autolink_content`, riallineamento semantico bi-fase in `anki_helper.reinject_anki_cards`, barriera di sicurezza bitwise in `brain_health.lint_file` e sezione diagnostica statica in `Vault Health Dashboard.md`.

## Risultati Raggiunti

1. **Iniezione Prompt AI & Flag CLI `--anki` (`brain_ingest.py`)**:
   - Aggiunto il flag `--anki` ad `argparse` e propagato in `ingest_source(...)`.
   - Attivazione automatica di Anki (`enable_anki`) per corsi universitari (`--course`), flag `--anki`, o note in area `education`.
   - Iniezione della Regola 7 nel prompt di `enrich_draft_with_ai`: generazione flashcard contestuali atomiche collocate a valle dei concetti cardine `<mark>`, callout collassabili `> [!tip]- Flashcard: [Nome Concetto]`, target deck `%% TARGET DECK: University::<Corso> %%`, euristica ADC (Basic per principi primi, Cloze per formule vincolate), delimitatori MathJax Anki `[$]...[/$]` compattati su riga singola e divieto di generare ID manuali.

2. **Mascheramento Autolinker di Sicurezza (`autolink_content`)**:
   - Schermatura preventiva con blocchi protetti per tutti i callout flashcard Anki (`> [!tip]- Flashcard:` ... `> END`), blocchi raw `START ... END`, e delimitatori MathJax (`[$]...[/$]`, `[$$]...[/$$]`, `$$...$$`).
   - Ripristino inverso dei blocchi protetti per prevenire corruzioni o inserimento accidentale di wikilink `[[...]]` nei campi domanda/risposta o nei tag Anki.

3. **Riallineamento Semantico Bi-Fase degli ID (`anki_helper.reinject_anki_cards`)**:
   - Algoritmo a due fasi:
     - **Fase 1 (Match Esatto Concetto):** matching case-insensitive sul nome del concetto normalizzato.
     - **Fase 2 (Fuzzy Text Match):** matching di somiglianza con `difflib.SequenceMatcher(None, o_text, n_text).ratio() >= 0.65` su campi Front/Text.
   - Re-iniezione dell'identificativo originale `> <!--ID: {matched_id}-->` prima di `> END`.
   - Preservazione assoluta al 100% delle card orfane con ID in un blocco dedicato in fondo alla nota: `## Flashcard Archiviate (Preservazione ID Anki)` (D-14).
   - Snapshot preventivo del target su disco in `ingest_source` e riallineamento trasparente a valle dell'arricchimento concettuale.

4. **Barriera di Sicurezza Bitwise Anti-Tampering (`brain_health.lint_file`)**:
   - Controllo bitwise invariante: confronto rigido dell'insieme degli ID pre-linting e post-elaborazione (`pre_anki_ids != post_anki_ids`).
   - Aborto immediato e blocco della scrittura su disco se anche un solo ID viene alterato, rimosso o introdotto abusivamente.

5. **Pannello Statico Health Dashboard (`generate_health_dashboard`)**:
   - Aggiunta della sezione static Markdown "Integrità Flashcard Anki": conteggio totale, suddivisione Basic/Cloze, carte sincronizzate, carte inedite, mazzi registrati e warning in caso di collisioni di ID (zero dipendenze da Dataview).

## File Modificati

- `99 - Meta/Scripts/anki_helper.py`: algoritmo di riallineamento bi-fase `reinject_anki_cards` e preservazione orfani con ID.
- `99 - Meta/Scripts/brain_ingest.py`: flag `--anki`, iniezione prompt AI Regola 7, mascheramento in `autolink_content`, snapshotting e riallineamento ID in `ingest_source`.
- `99 - Meta/Scripts/brain_health.py`: barriera bitwise in `lint_file` e sezione "Integrità Flashcard Anki" in `generate_health_dashboard`.
- `99 - Meta/Vault Health Dashboard.md`: dashboard rigenerata con monitoraggio Anki.
- `tests/test_anki_preservation.py`: aggiunte classi `TestAnkiGeneration` e `TestAnkiPreservation` con 10 nuovi test (24 test totali).

## Risultati dei Test

```text
python3 -m unittest tests/test_anki_preservation.py
Ran 24 tests in 0.021s - OK

python3 -m unittest discover tests
Ran 249 tests in 14.317s - OK
```

## Self-Check: PASSED
- [x] Tutte le modifiche al codice sono state integrate e testate.
- [x] Zero regressioni su tutti i 249 test di sistema.
- [x] Vault Health Dashboard rispetta la regola del Markdown statico senza Dataview.
