---
name: audit
description: Health linter per il Vault. Scansiona il Second Brain per individuare note orfane, wiki-link rotti, note prive di YAML frontmatter e anomalie nei tag.
---
# Skill: /audit (Vault Health Diagnostics)

Questa skill scansiona l'intero Vault Obsidian per eseguire una diagnostica di integrità del grafo e dei file, aiutando l'utente a mantenere l'ordine entropico del Second Brain.

## Workflow Esecutivo

1. **Esecuzione Diagnostica:**
   - Esegui lo script helper `scripts/audit_vault.py` tramite terminale:
     ```bash
     python3 scripts/audit_vault.py
     ```
2. **Analisi delle Anomalie:**
   - **Note Orfane:** File `.md` (esclusi quelli in `Meta` o `04 - Calendar`) che non hanno alcun wiki-link entrante da altre note e non sono inseriti in alcuna MOC in `Map of Content/`.
   - **Broken Links:** Wiki-link del tipo `[[Nome Nota]]` presenti nel testo che puntano a note inesistenti nel filesystem.
   - **Missing Frontmatter:** File `.md` (esclusi quelli in `04 - Calendar`) che non presentano il blocco iniziale `---` o che mancano di campi obbligatori (`title`, `date`, `tags`, `status`, `macro_area`).
   - **Tag Anomalies:** Note con tag non standard o non associati alla macroarea indicata.
3. **Generazione del Report:**
   - Lo script scrive automaticamente un report in formato markdown salvandolo in `Inbox/Audit Report - <Data>.md`.
   - Il report deve contenere:
     - **📊 Riepilogo Statistiche:** Numero totale note, note orfane, link rotti, note senza frontmatter.
     - **🔴 Criticità (Broken Links & Missing Frontmatter):** Elenco dettagliato dei file con i relativi problemi.
     - **🟡 Warning (Note Orfane & Tag Inconsistenti):** Elenco delle note isolate da collegare o ricatalogare.
4. **Output Utente:**
   - Presenta un riassunto dell'audit all'utente e fornisci il link all'audit file generato in Inbox per consentire un intervento manuale o automatico.
