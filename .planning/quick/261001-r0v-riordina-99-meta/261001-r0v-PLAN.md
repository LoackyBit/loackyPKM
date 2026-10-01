---
id: 261001-r0v
slug: riordina-99-meta
title: "Riorganizzazione Strutturale e Bonifica di 99 - Meta"
created: 2026-10-01T19:28:00+02:00
status: in-progress
---

# Quick Plan: Riorganizzazione Strutturale e Bonifica di 99 - Meta

## Obiettivo
Riorganizzare e bonificare la directory `99 - Meta/` secondo le convenzioni e gli standard del Vault:
1. Migrare `99 - Meta/School/` in `99 - Meta/Reference/` preservando `Giovanni Pascoli.md` e `Gabriele d'Annunzio.md` come campioni di evidenziazione Style Guide, eliminando il vecchio duplicato `Style Guide.md` e la cartella obsoleta `School/`.
2. Pulire la radice di `99 - Meta/` spostando `.backfill_checkpoint.json` in `99 - Meta/Cache/`, rimuovere cartelle vuote residue (`Clipboard/Fondamenti di Matematica (Analisi 1)`), correggere il percorso allegati in `.obsidian/app.json` (`99 - Meta/Clipboard`), ed epurare i file `.DS_Store`.
3. Normalizzare `99 - Meta/Guide/`: rinominare `MOC'S.md` in `Guida MOC.md` e dotare tutte le guide di frontmatter canonico e breadcrumb.
4. Bonificare i 20 file in `99 - Meta/Prompt/`: eliminare le sezioni deprecate `## Collegamenti`, sincronizzare `related: [...]` nel frontmatter, e allineare i breadcrumb a `[[Prompts MOC]]`.
5. Aggiornare le configurazioni di Obsidian (`manual-sorting/data.json`), i riferimenti di sistema (`AGENTS.md`, `GEMINI.md`) ed eseguire la suite di test completa (269 test).

## Task List

- [ ] **Task 1: Migrazione da School a Reference ed epurazione duplicati**
  - Creare `99 - Meta/Reference/`.
  - Spostare `Giovanni Pascoli.md` e `Gabriele d'Annunzio.md` in `99 - Meta/Reference/`.
  - Aggiornare frontmatter e breadcrumb (`[[Home MOC|Home]] / [[Meta]] / [[Reference]] / ...`).
  - Rimuovere `99 - Meta/School/Style Guide.md` (duplicato obsoleto) e la directory `99 - Meta/School/`.
  - Aggiornare i riferimenti in `99 - Meta/Style Guide.md`, `AGENTS.md`, `GEMINI.md`, e `.obsidian/plugins/manual-sorting/data.json`.

- [ ] **Task 2: Pulizia root, Cache, Clipboard config e normalizzazione Guide**
  - Spostare `.backfill_checkpoint.json` in `99 - Meta/Cache/.backfill_checkpoint.json`.
  - Rimuovere la directory vuota `99 - Meta/Clipboard/Fondamenti di Matematica (Analisi 1)/` e i file `.DS_Store`.
  - Aggiornare `.obsidian/app.json` per impostare `"attachmentFolderPath": "99 - Meta/Clipboard"`.
  - Rinominare `99 - Meta/Guide/MOC'S.md` in `99 - Meta/Guide/Guida MOC.md`.
  - Inserire frontmatter canonico e breadcrumb in `Guida MOC.md`, `Obsidian Graph View.md` e `Ingest Automation Refactoring Design.md`.
  - Aggiornare `.obsidian/plugins/manual-sorting/data.json`.

- [ ] **Task 3: Bonifica dei 20 file in Prompt e sincronizzazione MOC**
  - Per ciascuno dei 20 file in `99 - Meta/Prompt/`:
    - Rimuovere il blocco finale `## Collegamenti` / `## Collegamenti utili`.
    - Sincronizzare i link wiki estratti nel campo `related: [...]` del frontmatter YAML canonico.
    - Aggiornare i breadcrumb in `[[Home MOC|Home]] / [[Prompts|Prompts MOC]] / [[<Title>]]`.
  - Verificare e aggiornare `01 - Map of Content/Prompts.md` per coerenza.
  - Aggiornare `.obsidian/plugins/manual-sorting/data.json`.

- [ ] **Task 4: Verifica integrità, Test Suite e Dashboard Governance**
  - Eseguire tutti i test (`python3 -m unittest discover -s tests -p "test_*.py"`).
  - Rigenerare la dashboard statica (`python3 "99 - Meta/Scripts/brain_health.py" --dashboard-only`).
  - Creare `SUMMARY.md` e aggiornare `.planning/STATE.md`.
