---
id: 260927-hfd
slug: alta-densita-flashcard-note
title: "Alta Densità Flashcard Anki su Note Universitarie e Integrazione Regole Second Brain"
created: 2026-09-27T21:49:00+02:00
---

# Quick Plan: Alta Densità Flashcard Anki su Note Universitarie e Integrazione Regole Second Brain

## Obiettivo
Aumentare drasticamente la densità di flashcard Anki contestuali e inline in tutte le note create nel Vault (`Fondamenti di Matematica`, `Probabilità e Statistica`, `Introduzione alla Programmazione`), eliminando il limite restrittivo previgente (5-10 card per lezione) e integrando questa modifica come regola permanente nel Second Brain (`.agents/MEMORY.md`, `GEMINI.md`, `AGENTS.md`, `SKILL.md`, `brain_ingest.py`).

## Task List
- [ ] **Task 1: Integrazione Regole Second Brain & Memoria Permanente**
  - Aggiornare `.agents/MEMORY.md` sancendo la regola permanente dell'alta densità di flashcard (copertura esaustiva di ogni concetto cardine, definizione, assioma, teorema e proprietà).
  - Aggiornare `GEMINI.md`, `AGENTS.md`, `.agents/skills/brain-ingest/SKILL.md` e `99 - Meta/Scripts/brain_ingest.py` rimuovendo il limite "5-10 card" in favore dell'alta densità sistematica.
- [ ] **Task 2: Aumento Densità Flashcard in Fondamenti di Matematica (Lezione 01 & 02)**
  - Inserire le flashcard mancanti in `01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione.md` (terzo escluso, dimostrazione per assurdo, congiunzione/disgiunzione inclusiva, bicondizionale, predicato/variabili libere-legate, quantificatori multipli, parità del quadrato).
  - Inserire le flashcard mancanti in `02 - Teoria degli Insiemi.md` (assioma della coppia non ordinata, doppia inclusione, intersezione di famiglie, algebra insiemistica/distributività, dimostrazione De Morgan, insiemi per elencazione, assioma di fondazione ed esclusione $x \in x$).
- [ ] **Task 3: Aumento Densità Flashcard in Probabilità e Statistica & Introduzione alla Programmazione**
  - Inserire flashcard ad alta densità per concetti cardine, dimostrazioni e proprietà scoperte.
- [ ] **Task 4: Validazione, Sanitizzazione & Test Suite**
  - Eseguire `anki_helper.py` per sanitizzare e validare la sintassi delle nuove card.
  - Eseguire i test unitari con `python3 -m unittest discover tests` e audit `brain_health.py --dry-run`.
- [ ] **Task 5: Finalizzazione Documentazione Quick Task & State**
  - Creare `SUMMARY.md` e aggiornare `.planning/STATE.md`.
  - Eseguire commit atomico convenzionale.
