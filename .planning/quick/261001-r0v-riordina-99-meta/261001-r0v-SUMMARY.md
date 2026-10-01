---
id: 261001-r0v
slug: riordina-99-meta
title: "Riorganizzazione Strutturale e Bonifica di 99 - Meta"
created: 2026-10-01T19:35:00+02:00
status: complete
---

# Quick Task Summary: Riorganizzazione Strutturale e Bonifica di 99 - Meta

## Sintesi Esecutiva
Riorganizzata integralmente la directory `99 - Meta/` secondo le convenzioni e gli standard del Vault:
1. **Dismissione di `School/` e creazione di `Reference/`**:
   - `Giovanni Pascoli.md` e `Gabriele d'Annunzio.md` spostati in `99 - Meta/Reference/` con frontmatter canonico a 10 campi (`status: reference`, `area: meta`) e breadcrumb normalizzati, preservandoli come campioni di stile per la frequenza e la gerarchia delle evidenziazioni HTML `<mark>`.
   - Rimosso il duplicato obsoleto `99 - Meta/School/Style Guide.md` e deallocata la directory `99 - Meta/School/`.
2. **Pulizia della radice e della cache**:
   - Spostato `.backfill_checkpoint.json` da `99 - Meta/` a `99 - Meta/Cache/.backfill_checkpoint.json` e aggiornati i path in `backfill_summaries.py` e `tests/test_backfill_summaries.py`.
   - Rimossa la cartella vuota residua in `Clipboard/` ed eliminati tutti i `.DS_Store`.
   - Corretto `.obsidian/app.json` impostando `"attachmentFolderPath": "99 - Meta/Clipboard"`.
3. **Normalizzazione di `99 - Meta/Guide/`**:
   - Rinominato `MOC'S.md` in `Guida MOC.md` e applicato il frontmatter canonico a 10 campi a tutte le guide (`Guida MOC.md`, `Obsidian Graph View.md`, `Ingest Automation Refactoring Design.md`).
4. **Bonifica dei 20 file in `99 - Meta/Prompt/`**:
   - Rimossi tutti i blocchi finali obsoleti `## Collegamenti`.
   - Sincronizzati i collegamenti interni in `related: [...]` nel frontmatter YAML canonico.
   - Normalizzati i breadcrumb in `[[Home MOC|Home]] / [[Prompts|Prompts MOC]] / [[<Titolo>]]`.
   - Bonificato l'indice `01 - Map of Content/Prompts.md` rimuovendo la sezione collegamenti isolata.
5. **Configurazioni e Suite di Test**:
   - Aggiornato `.obsidian/plugins/manual-sorting/data.json` per riflettere `99 - Meta/Reference/` e `Guida MOC.md`.
   - Aggiornato `AGENTS.md` epurando i riferimenti obsoleti al modulo dismesso ClasseViva.
   - Tutti i 269 test unitari passano con successo (`OK`).
   - Dashboard statica `Vault Health Dashboard.md` rigenerata.
