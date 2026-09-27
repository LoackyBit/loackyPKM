---
id: 260927-pacrar-linked-tables
slug: pacrar-linked-tables
title: "Sincronizzazione Dinamica tra Tabelle PACRAR Figlie e Master MOC"
date: 2026-09-27
type: quick-summary
status: complete
---

# Quick Task 260927-pacrar-linked-tables: Sincronizzazione Dinamica tra Tabelle PACRAR Figlie e Master MOC

## Sintesi Esecutiva
Risolto il disallineamento tra le tabelle PACRAR dei singoli Course Hub (es. `Fondamenti di Matematica (Analisi 1) MOC.md`) e le tabelle aggregate presenti nel Master MOC (`Ingegneria Informatica 2026 - 27 MOC.md`). Ora le tabelle sono collegate in modo completamente dinamico e bidirezionale sia interattivamente in Obsidian (tramite il plugin `pacrar-tracker` e il rendering dei ring SVG reattivi) sia programmaticamente nel motore di automazione (`course_hub.py`).

## Azioni Eseguite

1. **Obsidian Micro-Plugin (`.obsidian/plugins/pacrar-tracker/main.js`)**:
   - Aggiunta la funzione `extractLessonKey(rawText)` per normalizzare wikilink e titoli di lezione rimuovendo formattazione markdown.
   - Creata la funzione `updatePacrarFile(file, lessonKey, cellIdx, nextState)` che identifica la riga corrispondente e aggiorna atomicamente la spunta su file disk via `app.vault.modify`.
   - Modificato `handleCheckboxClick`:
     - Oltre ad aggiornare il file MOC attivo, cerca e aggiorna proattivamente qualsiasi altro file in `01 - Map of Content/` contenente la medesima lezione (ad es. da MOC figlio a Master MOC o viceversa).
     - Aggiorna istantaneamente sia il disco che i nodi DOM visibili nell'interfaccia di Obsidian senza ricaricare la pagina.
     - Ricalcola dinamicamente gli anelli SVG di progresso per tutti i contenitori di tabella interessati.
   - Registrato il listener `app.vault.on('modify')` sui file MOC per garantire il re-scan in background.

2. **CSS Snippet (`.obsidian/snippets/pacrar.css`)**:
   - Risolto il problema del riquadro grigio duplicato aggiungendo la regola `.pacrar-progress-widget:empty, .pacrar-progress-widget:not(:has(.pacrar-ring-wrap)) { display: none !important; }`.

3. **Motore di Automazione Python (`99 - Meta/Scripts/course_hub.py`)**:
   - Esteso `RE_TABLE_HEADER` per accettare intestazioni con colonna opzionale `Sintesi` / `Stato / Sintesi` ed header generici.
   - Aggiornato `parse_pacrar_table` e `format_pacrar_table` per supportare tabelle a 7 e a 8 colonne mantenendo piena retrocompatibilità.
   - Implementata la funzione `sync_master_moc_with_children(master_moc_path, vault_root)`: analizza le sezioni con `*Hub dedicato:* [[<Course> MOC]]`, estrae i dati aggiornati dalle tabelle figlie e aggiorna le sezioni aggregate del Master MOC preservando commenti e sintesi.
   - Implementata `sync_master_mocs_for_course(course_name, vault_root)` e integrata in `update_course_pacrar_matrix` per cascata automatica al momento della promozione di nuove note o dell'aggiornamento dei corsi.
   - Aggiunto il flag CLI `--sync-master` a `course_hub.py`.

4. **Suite di Test & Garanzia di Regressione**:
   - Aggiunti i test unitari `test_sync_master_moc_with_children` e `test_sync_master_mocs_for_course_auto_cascades` in `tests/test_course_hub.py`.
   - Eseguita l'intera test suite (`python3 -m unittest discover tests`): tutti i 267 test completati con esito positivo (100% OK).
