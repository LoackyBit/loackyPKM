---
name: process-inbox
description: Orchestratore GTD per analizzare, classificare e smistare automaticamente le note da 03 - Inbox alle cartelle di destinazione.
---
# Skill: /process-inbox (Orchestratore GTD)

Questa skill agisce da motore di smistamento del Second Brain, svuotando regolarmente la cartella `03 - Inbox/` e ricollocando ogni nota nella cartella tematica più idonea dell'architettura.

## Workflow Esecutivo

1. **Scansione Inbox:**
   - Esegui lo script helper `scripts/inbox_scanner.sh` (o elenca i file in `03 - Inbox/`) per vedere le note in attesa di smistamento.
2. **Pre-trattamento (Linter & Linking):**
   - Per ogni nota, verifica prima che il frontmatter sia completo (invocando la logica di `/meta`). Assicurati che lo `status` passi da `draft` a `permanent` (o `in-progress`).
   - Se il campo `macro_area` nel frontmatter è vuoto (`""`), inferiscilo **automaticamente** dal contenuto della nota senza chiedere conferma all'utente. Usa questa logica:
     - `tech` → note su informatica, programmazione, AI, tool, configurazioni, video YouTube tecnici
     - `mentality` → crescita personale, psicologia, metodi, riflessioni, filosofia
     - `university` → appunti di materie universitarie o scolastiche
     - `finance` → investimenti, economia, mercati, finanza personale
     - `meta` → note sul vault stesso, template, automazioni, workflow
   - Dopo aver inferito il valore, aggiorna il frontmatter del file con `macro_area: <valore>` prima di procedere.
3. **Classificazione Semantica:**
   - Leggi il contenuto della nota e determina la destinazione ideale nella struttura corrente:
     - **`01 - Map of Content/`:** Se la nota è un indice, un hub semantico o una mappa concettuale (MOC).
     - **`02 - Atlas/Corsi/`:** Appunti universitari, Ingegneria Informatica, algoritmi, linguaggi (es. `esercizio + appunti R.md`, `Guida Completa a Cursor.md`, `Python`).
     - **`02 - Atlas/Mentality/` / `Education/`:** Crescita personale, psicologia, metodi di studio, riflessioni (es. `Learning to Learn (ITA).md`, `Cancel Culture.md`, `Echochamber.md`, `Skincare.md`).
     - **`02 - Atlas/Finance/`:** Note su investimenti, economia, mercati (es. `Guida Investimenti 2025.md`).
     - **`02 - Atlas/Tecnology/` / `Prompt/`:** Prompt engineering, tool AI, vibe coding (es. `Evoluzione dell'agente AI.md`, `Mastering AI Prompting.md`, `L’Evoluzione del Vibe Coding.md`).
     - **`05 - Blog/`:** Articoli completi, saggi o bozze destinate alla pubblicazione web.
4. **Esecuzione Smistamento:**
   - Proponi all'utente il piano di smistamento dettagliato o esegui direttamente i comandi `mv` su terminale per spostare i file nella loro nuova casa:
     ```bash
     mv "03 - Inbox/Nome Nota.md" "02 - Atlas/Cartella Destinazione/"
     ```
   - Restituisci un report finale riassuntivo con le note spostate e le relative destinazioni.
