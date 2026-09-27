---
id: 260927-ur5
slug: sottodeck-flashcard-per-nota
title: "Creazione Generale Sottodeck Flashcard Anki per Singola Nota"
created: 2026-09-27T22:10:00+02:00
---

# Quick Plan: Creazione Generale Sottodeck Flashcard Anki per Singola Nota

## Obiettivo
Generalizzare l'organizzazione gerarchica delle flashcard Anki nel Vault implementando un sottodeck dedicato per ciascuna nota (formato `University::<Nome Corso>::<Titolo Nota>`, conservando prefissi numerici come `01`, `02`, ecc.). Aggiornare le regole di sistema, le istruzioni prompt di `brain_ingest.py`, gli helper di formattazione in `anki_helper.py`, e allineare tutte le note esistenti (a partire da Fondamenti di Matematica con due sottodeck distinti per le due lezioni create).

## Task List
- [ ] **Task 1: Allineamento Normativo e Regole di Sistema**
  - Aggiornare `.agents/MEMORY.md`, `GEMINI.md`, `AGENTS.md` e `.agents/skills/brain-ingest/SKILL.md` definendo la convenzione tassativa del sottodeck per singola nota: `TARGET DECK: University::<Nome Corso>::<Titolo Nota>`.
- [ ] **Task 2: Aggiornamento Prompt AI e Helper Python**
  - Modificare `99 - Meta/Scripts/brain_ingest.py` (sezione `enrich_draft_with_ai`) affinché il prompt di generazione flashcard imponga la gerarchia con sottodeck nominato esattamente come la nota (`TARGET DECK: University::{clean_deck}::{c_title}`).
  - Modificare `99 - Meta/Scripts/anki_helper.py` per supportare `note_title` in `format_anki_card` e aggiungere una funzione universale di normalizzazione/aggiornamento dei sottodeck delle note preservando scrupolosamente gli ID Anki preesistenti.
- [ ] **Task 3: Migrazione Note Esistenti (FdM e Corsi Universitari)**
  - Aggiornare le due note di Fondamenti di Matematica (FdM):
    - `01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione.md` -> `University::Fondamenti di Matematica (Analisi 1)::01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione`
    - `02 - Teoria degli Insiemi.md` -> `University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi`
  - Aggiornare le restanti note del Vault con flashcard (`Introduzione alla Programmazione`, `Probabilità e Statistica`, `Metodo di Studio - PACRAR`) con i rispettivi sottodeck per nota, preservando tutti gli `<!--ID: ...-->`.
- [ ] **Task 4: Test Unitari e Verifica Integrità Vault**
  - Aggiungere test in `tests/test_anki_preservation.py` per verificare la corretta composizione e normalizzazione del sottodeck con titolo nota.
  - Eseguire la suite di test completa (`python3 -m unittest discover tests`) e l'audit Anki (`anki_helper.py --audit`).
  - Verificare la conformità del Vault con `brain_health.py --dry-run`.
- [ ] **Task 5: Finalizzazione Documentazione Quick Task & State**
  - Creare `SUMMARY.md` e aggiornare `.planning/STATE.md`.
