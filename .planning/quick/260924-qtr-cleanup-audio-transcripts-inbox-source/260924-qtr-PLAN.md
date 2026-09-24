---
id: 260924-qtr
slug: cleanup-audio-transcripts-inbox-source
title: "Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/ durante l'approvazione GTD"
date: 2026-09-24
type: quick-plan
status: completed
---

# Quick Plan 260924-qtr: Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/ durante l'approvazione GTD

## Contesto & Problema
A seguito dell'introduzione della regola tassativa di divieto di citare o indicizzare trascrizioni audio nel frontmatter (`sources: [...]`) o nel testo delle note permanenti per non creare ghost-links nel grafo del Vault, le trascrizioni audio temporanee vengono giustamente omesse da `sources: [...]`.
Tuttavia, `_handle_promote_item` e `_handle_purge_item` in `brain_ingest.py` scansionavano esclusivamente i riferimenti contenuti nell'array frontmatter `sources`.
Di conseguenza, quando la nota master ha un nome diverso dalla trascrizione (es. `Introduzione alla Programmazione - 1.md` -> bozza `01 - Elaborazione delle Informazioni...`), i file di trascrizione audio (come `Introduzione alla Programmazione - Trascrizione Audio.md`) restavano orfani in `03 - Inbox/Source/` violando il vincolo di "zero residui in Inbox".

## Obiettivi
1. Aggiornare `_handle_promote_item` e `_handle_purge_item` in `99 - Meta/Scripts/brain_ingest.py`:
   - Estrarre le dipendenze locali direttamente dal contenuto del file master `source_path` prima della sua eliminazione/archiviazione;
   - Scansionare `03 - Inbox/Source/` per eliminare qualsiasi file `.md` classificato come trascrizione (`is_transcript`) associato al corso (`meta.get('course')`) o alla lezione/nota approvata (`name`/`src_name`), anche se escluso dal frontmatter `sources: [...]`.
2. Bonificare il file orfano rimasto `03 - Inbox/Source/Introduzione alla Programmazione - Trascrizione Audio.md`.
3. Aggiungere test unitari specifici in `tests/test_brain_ingest.py` a copertura del caso in cui la trascrizione è omessa da `sources: [...]`.
4. Documentare e aggiornare `.planning/STATE.md` e produrre `SUMMARY.md`.

## Tasks

### Task 1: Potenziamento logica di cleanup in `99 - Meta/Scripts/brain_ingest.py`
- **File**: `99 - Meta/Scripts/brain_ingest.py`
- **Azione**:
  1. In `_handle_promote_item`:
     - Prima di rimuovere/archiviare `source_path`, estrarre tutti i wikilink `[[...]]` presenti nel suo testo e aggiungerli alla lista di candidati da verificare.
     - Ispezionare `03 - Inbox/Source/` alla ricerca di file di trascrizione (`kind == 'transcript'`) il cui nome o contenuto correli con il corso (`course`), con `name`, o con `src_name`, ed eliminarli.
  2. In `_handle_purge_item`:
     - Applicare la medesima pulizia proattiva su `03 - Inbox/Source/` per cancellare le trascrizioni correlate in caso di scarto `[-]`.
- **Verifica**: Test manuale ed esecuzione dei test unitari.

### Task 2: Eliminazione del file orfano residuo
- **File**: `03 - Inbox/Source/Introduzione alla Programmazione - Trascrizione Audio.md`
- **Azione**: Rimuovere il file residuo da `03 - Inbox/Source/`, lasciando la directory pulita.
- **Verifica**: `ls "03 - Inbox/Source"` non contiene più la trascrizione.

### Task 3: Test unitari e validazione regressione
- **File**: `tests/test_brain_ingest.py`
- **Azione**:
  - Aggiungere un test `test_promote_cleans_unlisted_transcripts_matching_course` che simula una bozza senza trascrizione in `sources` ma con trascrizione in `03 - Inbox/Source/` correlata al corso.
  - Verificare che tutti i test in `tests/test_brain_ingest.py` passino con 100% OK.
- **Verifica**: `python3 -m unittest tests/test_brain_ingest.py` passa senza errori.

### Task 4: Aggiornamento Stato e Sintesi Finale
- **File**: `.planning/quick/260924-qtr-cleanup-audio-transcripts-inbox-source/260924-qtr-SUMMARY.md`, `.planning/STATE.md`
- **Azione**: Creare `SUMMARY.md`, aggiornare la tabella Quick Tasks in `STATE.md`, ed eseguire commit convenzionale.
