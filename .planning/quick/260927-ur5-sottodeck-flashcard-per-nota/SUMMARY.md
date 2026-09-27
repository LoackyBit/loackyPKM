---
id: 260927-ur5
slug: sottodeck-flashcard-per-nota
title: "Creazione Generale Sottodeck Flashcard Anki per Singola Nota"
created: 2026-09-27T22:15:00+02:00
status: complete
---

# Quick Task Summary: Creazione Generale Sottodeck Flashcard Anki per Singola Nota

## Sintesi Esecutiva
Implementata l'organizzazione gerarchica generale delle flashcard Anki per il Second Brain, creando un sottodeck dedicato per ciascuna nota (formato `University::<Corso>::<Titolo Nota>`), conservando scrupolosamente i prefissi numerici delle lezioni (es. `01`, `02`, ecc.).

Fondamenti di Matematica (FdM) dispone ora di due sottodeck separati per le due lezioni create:
- `University::Fondamenti di Matematica (Analisi 1)::01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione`
- `University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi`

## Modifiche Chiave
1. **Regole di Sistema & Memoria Permanente:**
   - `.agents/MEMORY.md`: stabilita la regola tassativa del sottodeck dedicato per ogni nota/lezione (`TARGET DECK: University::<Nome Corso>::<Titolo Nota>`).
   - `GEMINI.md`, `AGENTS.md` e `.agents/skills/brain-ingest/SKILL.md`: allineata la sintassi di TARGET DECK con sottodeck gerarchico per singola nota.
2. **Motore di Ingestion & Script Helper Python:**
   - `99 - Meta/Scripts/brain_ingest.py`: aggiornato il prompt AI per richiedere esplicitamente il sottodeck gerarchico per nota `TARGET DECK: University::{clean_deck}::{c_title}`, e aggiunta la normalizzazione automatica post-arricchimento e post-rinomina titolo.
   - `99 - Meta/Scripts/anki_helper.py`: estesa la funzione `format_anki_card` con supporto al parametro `note_title`; aggiunte le funzioni `update_note_flashcard_subdecks` e `update_file_flashcard_subdecks`, nonché le opzioni CLI `--update-subdecks` e `--update-all-subdecks` per aggiornamenti batch preservando tutti gli ID Anki preesistenti.
3. **Migrazione Note Esistenti nel Vault:**
   - Aggiornate tutte le note del Vault contenenti flashcard Anki:
     - `01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione.md` -> sottodeck `01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione`
     - `02 - Teoria degli Insiemi.md` -> sottodeck `02 - Teoria degli Insiemi`
     - `01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python.md` -> sottodeck `01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python` (tutti gli ID `<!--ID: ...-->` preservati)
     - `01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità.md` -> sottodeck `01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità`
     - `Metodo di Studio - PACRAR.md` -> sottodeck `Metodo di Studio - PACRAR`
4. **Verifica & Test:**
   - Aggiunti test dedicati in `tests/test_anki_preservation.py` (`test_format_anki_card_with_note_subdeck`, `test_update_note_flashcard_subdecks_and_id_preservation`).
   - Eseguiti con successo 269 test unitari (`OK`).
   - Audit `anki_helper.py --audit` con 65 card totali e 5 deck gerarchici registrati senza duplicati.
