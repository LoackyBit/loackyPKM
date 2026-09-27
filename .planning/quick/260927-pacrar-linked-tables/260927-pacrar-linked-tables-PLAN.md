---
status: complete
type: quick
slug: 260927-pacrar-linked-tables
date: '2026-09-27'
title: "Sincronizzazione Dinamica tra Tabelle PACRAR Figlie e Master MOC"
---

# Quick Task: Sincronizzazione Dinamica tra Tabelle PACRAR Figlie e Master MOC

## Obiettivo
Rendere `01 - Map of Content/Ingegneria Informatica 2026 - 27 MOC.md` dinamicamente collegato alle tabelle dei singoli MOC di corso (es. `Fondamenti di Matematica (Analisi 1) MOC.md`, `Introduzione alla Programmazione MOC.md`, `Probabilità e Statistica MOC.md`). Qualsiasi modifica apportata a una riga PACRAR in una tabella figlia si riflette istantaneamente nel Master Hub, e viceversa.

## Piano di Esecuzione

1. **Obsidian Micro-Plugin (`.obsidian/plugins/pacrar-tracker/main.js`):**
   - Aggiungere funzione di estrazione chiave di lezione normalizzata `extractLessonKey(rawText)`
   - In `handleCheckboxClick`, dopo aver aggiornato il file attivo, ricercare tutti gli altri file MOC in `01 - Map of Content/` che contengono la medesima lezione
   - Aggiornare atomicamente il file correlato tramite `app.vault.modify`
   - Se il file correlato è attualmente visibile nel DOM di Obsidian, aggiornare immediatamente anche il nodo DOM della cella e ricalcolare l'anello progressivo SVG

2. **Modulo Python (`99 - Meta/Scripts/course_hub.py`):**
   - Implementare `sync_master_moc_with_children(master_moc_name_or_path, vault_root)` che estrae i riferimenti `*Hub dedicato:* [[<Course> MOC]]`, legge le tabelle aggiornate dei MOC figli e aggiorna la sezione PACRAR del Master MOC
   - Connettere questa funzione al trigger di promozione in `register_lesson` / `sync_course_hub`
   - Aggiungere flag CLI `--sync-master` a `course_hub.py` per sincronizzazioni manuali o batch

3. **Verifica & Test Automatizzati:**
   - Aggiungere test unitari in `tests/test_course_hub.py` per la propagazione bidirezionale e la sincronizzazione master-figlio
   - Eseguire suite completa con `python3 -m unittest discover tests`
