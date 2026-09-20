---
phase: "17"
plan: "01"
subsystem: anki_helper
tags: [anki, mathjax, flashcards, audit, ast]
date: "2026-09-20"
---

# Phase 17 Plan 01: Modulo Fondativo anki_helper & Test Harness Sintattico — Summary

Implementato il modulo fondativo `99 - Meta/Scripts/anki_helper.py` e la test suite dedicata `tests/test_anki_preservation.py` a supporto dell'intero ciclo di vita delle flashcard Anki nel Second Brain.

## Risultati Raggiunti

1. **Conversione MathJax Anki (`convert_math_to_anki`)**:
   - Trasformazione automatica da formule Markdown `$inline$` e `$$display$$` nei delimitatori nativi Anki `[$]...[/$]` e `[$$]...[/$$]`.
   - Mascheramento preventivo per prevenire conversioni doppie.
   - Compattazione su riga singola senza newline nudi che spezzerebbero il parser di `obsidian-to-anki-plugin`.
   - Sanitizzazione intelligente dei pipe nudi `|` in `\vert` senza alterare spaziatura o formule esistenti.
   - Protezione spaziatura per cloze deletion annidate in formule LaTeX: `{ {{c1::...}} }` (D-05, D-06, D-07).

2. **Formattazione Callout Flashcard (`format_anki_card`)**:
   - Generazione conforme allo standard `> [!tip]- Flashcard: [Nome Concetto]` (D-03).
   - Iniezione della direttiva `> %% TARGET DECK: University::<NomeCorso> %%` a inizio blocco (D-02).
   - Supporto per modelli internazionali `Basic` (Front/Back) e `Cloze` (Text/Extra) (D-04).
   - Generazione tag gerarchici Anki (`Tags: Materia::Argomento::Dettaglio`) con separatori underscore (D-12).
   - Inclusione opzionale del commento identificativo `> <!--ID: \d+-->` prima di `> END`.

3. **Parser AST Flashcard (`extract_anki_cards_from_text`)**:
   - Estrazione accurata e deterministica di campi, modelli, tag gerarchici, deck e ID.
   - Piena retrocompatibilità con callout `> [!tip]-`, callout generici (`> [!question]`) e blocchi unquoted storici presenti in `test.md`.
   - Gestione robusta di campi multiline e campi impliciti.

4. **Motore di Audit del Vault & CLI (`audit_anki_cards` & CLI)**:
   - Scansione ricorsiva di tutti i file Markdown del vault ignorando cartelle di sistema.
   - Calcolo metriche: flashcard totali, sincronizzate (con ID), inedite (senza ID), mazzi unici registrati.
   - Rilevamento collisioni e duplicati di ID Anki con exit code 1 in caso di anomalie.
   - Supporto CLI standalone con `--audit`, `--check-file <path>` e `--vault-root <path>`.

## File Creati / Modificati

- `99 - Meta/Scripts/anki_helper.py`: modulo autonomo per formattazione, conversione MathJax, estrazione e audit.
- `tests/test_anki_preservation.py`: test harness contenente le classi `TestAnkiSyntax`, `TestAnkiExtraction` e `TestAnkiAudit`.

## Risultati dei Test

```text
python3 -m unittest tests/test_anki_preservation.py
Ran 14 tests in 0.006s - OK

python3 "99 - Meta/Scripts/anki_helper.py" --audit
Total Cards: 3 (Basic: 3, Cloze: 0)
Synced Cards (with ID): 3
Pending Cards (without ID): 0
Registered Decks: 0
All Anki IDs are unique and consistent.
```

## Self-Check: PASSED
- [x] `99 - Meta/Scripts/anki_helper.py` creato e importabile.
- [x] `tests/test_anki_preservation.py` creato con 14 test superati.
- [x] Nessuna dipendenza esterna non gestita.
