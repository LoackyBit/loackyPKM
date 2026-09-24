---
id: 260924-orz
slug: non-salvare-in-memory-md-ma-integra-nel-
title: Integrare regole didattiche e visuali nel sistema Second Brain rimuovendole da MEMORY.md
date: 2026-09-24
type: quick-plan
status: planned
---

# Quick Plan: Integrare Regole nel Sistema Second Brain (senza salvarle in MEMORY.md)

L'utente ha espressamente richiesto: *"non salvare in MEMORY.md ma integra nel sistema di Second Brain"*.
Le direttive riguardanti:
1. Zero citazioni a trascrizioni audio (solo slide PDF e materiali di valore accademico/scientifico).
2. Densità strategica ed equilibrata delle citazioni slide con sintassi di escape `\[[[NomeFile.pdf#page=N|Slide N]]]`.
3. Divieto assoluto di diagrammi simbolici ASCII/Unicode complessi (`┌┐└┘`, `│`, `──►`) che non renderizzano coerentemente sui vari dispositivi/font; utilizzo preferenziale di transclusioni di slide ad alta risoluzione (PNG 2x Retina) o tabelle Markdown standard e callout.

Queste regole devono essere rimosse da `.agents/MEMORY.md` e integrate stabilmente nell'architettura permanente del Second Brain: `GEMINI.md`, `AGENTS.md`, `.agents/skills/brain-ingest/SKILL.md`, `99 - Meta/Style Guide.md` e nel prompt di `99 - Meta/Scripts/brain_ingest.py`.

## Tasks

### Task 1: Pulizia di `.agents/MEMORY.md`
- **Azione:** Rimuovere la Sezione 5 aggiunta in precedenza da `.agents/MEMORY.md`, mantenendo inalterati il profilo utente e le sezioni 1-4.
- **File coinvolti:** `.agents/MEMORY.md`
- **Verifica:** Il file termina alla fine della sezione 4 senza menzione della sezione 5.

### Task 2: Integrazione nel Sistema Second Brain (`GEMINI.md`, `AGENTS.md`, `.agents/skills/brain-ingest/SKILL.md`, `99 - Meta/Style Guide.md`, `99 - Meta/Scripts/brain_ingest.py`)
- **Azione:**
  1. Aggiornare `GEMINI.md` (Sezione 3 e Sezione 4): codificare le regole su fonti didattiche (no citazioni audio, solo slide/paper), densità citazioni slide con escape, e divieto diagrammi testuali ASCII a favore di render PNG o tabelle Markdown.
  2. Aggiornare `AGENTS.md`: riflettere i vincoli nella Style Guide e nelle convenzioni del sistema.
  3. Aggiornare `.agents/skills/brain-ingest/SKILL.md`: inserire le specifiche operative dettagliate nelle sezioni di intake e standard visivi.
  4. Aggiornare `99 - Meta/Style Guide.md`: aggiungere il divieto di diagrammi simbolici ASCII/Unicode e le convenzioni di citazione alle slide universitarie.
  5. Aggiornare `99 - Meta/Scripts/brain_ingest.py`: potenziare il prompt di sistema di rielaborazione (regola 6 e 3) con i divieti espliciti (no citazioni trascrizioni, densità calibrata slide, no diagrammi ASCII/Unicode).
- **File coinvolti:**
  - `GEMINI.md`
  - `AGENTS.md`
  - `.agents/skills/brain-ingest/SKILL.md`
  - `99 - Meta/Style Guide.md`
  - `99 - Meta/Scripts/brain_ingest.py`
- **Verifica:** Verificare la sintassi e la coerenza dei documenti e testare la corretta compilazione/funzionamento di `brain_ingest.py`.

### Task 3: Convalida, Documentazione e Aggiornamento Stato
- **Azione:** Eseguire test di validità di sintassi Python e generare il SUMMARY.md del quick task, aggiornando `.planning/STATE.md`.
- **File coinvolti:**
  - `.planning/quick/260924-orz-non-salvare-in-memory-md-ma-integra-nel-/260924-orz-SUMMARY.md`
  - `.planning/STATE.md`
- **Verifica:** Il repository è pulito e conforme.
