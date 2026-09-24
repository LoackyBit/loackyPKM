---
id: 260924-qtr
slug: cleanup-audio-transcripts-inbox-source
title: "Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/ durante l'approvazione GTD"
date: 2026-09-24
type: quick-summary
status: complete
---

# Quick Task 260924-qtr: Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/ durante l'approvazione GTD

## Sintesi Esecutiva
Risolto il cortocircuito tra la regola di qualità che impone il **divieto assoluto di citare trascrizioni audio nel frontmatter (`sources: [...]`)** e la logica di pulizia GTD di `brain_ingest.py`. Precedentemente, `_handle_promote_item` e `_handle_purge_item` pulivano le dipendenze secondarie scansionando unicamente i riferimenti in `sources`, lasciando orfane le trascrizioni audio temporanee in `03 - Inbox/Source/` se omesse dal frontmatter.

## Azioni Eseguite
1. **Modifica `_handle_promote_item` in `99 - Meta/Scripts/brain_ingest.py`**:
   - Estrazione preventiva di tutti i wikilink `[[...]]` dal file sorgente master `source_path` prima dell'archiviazione/rimozione, unendoli a `all_targets`.
   - Scansione proattiva di `03 - Inbox/Source/` per individuare qualsiasi file markdown con caratteristiche di trascrizione (`is_tr`) correlato al corso (`course`), al titolo della nota (`real_name`) o alla sorgente (`src_name`), eliminandolo automaticamente.
2. **Modifica `_handle_purge_item` in `99 - Meta/Scripts/brain_ingest.py`**:
   - Estrazione di tutti i riferimenti dal contenuto della bozza e scansione proattiva di `03 - Inbox/Source/` per eliminare trascrizioni audio e file temporanei collegati in caso di scarto (`[-]`).
3. **Bonifica del file residuo**:
   - Eliminato `03 - Inbox/Source/Introduzione alla Programmazione - Trascrizione Audio.md`, ripristinando lo stato di zero residui in `03 - Inbox/Source/`.
4. **Test & Garanzia di Regressione**:
   - Aggiunti i test unitari `test_promote_cleans_unlisted_transcripts_matching_course` e `test_purge_cleans_unlisted_transcripts_matching_course` in `tests/test_brain_ingest.py`.
   - Eseguita l'intera test suite (`python3 -m unittest discover -s tests`): 263 test eseguiti con 100% OK.
