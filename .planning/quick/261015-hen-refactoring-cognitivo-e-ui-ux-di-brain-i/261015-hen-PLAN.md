---
id: 261015-hen
slug: refactoring-cognitivo-e-ui-ux-di-brain-i
title: "Refactoring Cognitivo e UI/UX di brain-ingest (Scheletro Visivo & Co-Pilota Attivo)"
created: 2026-10-15T12:35:00+02:00
status: complete
---

# Quick Plan: Refactoring Cognitivo e UI/UX di `brain-ingest`

## Obiettivo
Trasformare il motore di elaborazione della conoscenza da "ghostwriter enciclopedico" prolisso a "scheletro visivo e co-pilota attivo":
1. **`99 - Meta/Scripts/brain_ingest.py`**:
   - Refactoring del prompt in `enrich_draft_with_ai()` introducendo l'architettura "Scheletro Esecutivo + Progressive Disclosure" (elenchi puntati/numerati telegrafici e densi stile `Gabriele d'Annunzio.md`, prosa continua limitata a max 3-4 righe per sezione).
   - Pattern Dual-Layer per teoremi e dimostrazioni: nel corpo/callout principale solo enunciato formale, LaTeX `$$...$$` e idea chiave/strategia in max 2-3 bullet sintetici; passaggi algebrici estesi incapsulati in `> [!abstract]- Dimostrazione Formale Passo-Passo`.
   - Struttura flessibile e condizionale: eliminazione dell'obbligo dei 5 sotto-bullet fissi per definizioni matematiche ordinarie (simboli con unità SI e condizioni di validità riservati a formule fisiche/multivariate).
   - Budget rigoroso evidenziazioni `<mark>`: max 1 giallo (`#cc8800`) e 2-3 viola (`#9a54c1`) per sotto-sezione.
   - Gestione attiva dei dubbi utente: risoluzione inline dei commenti `%% AI: non ho capito... %%` in callout `> [!question] Chiarimento sul tuo dubbio`.
2. **Documentazione & Normativa (`99 - Meta/Style Guide.md` e `.agents/skills/brain-ingest/SKILL.md`)**:
   - Aggiornamento della gerarchia evidenziatori con la regola di parsimonia estrema dell'AI e lo stile schematico/telegrafico.
   - Formalizzazione del pattern Dual-Layer per le dimostrazioni e dei chiarimenti dubbi in callout.
3. **Ergonomia UI/UX Obsidian (`.obsidian/app.json`, `.obsidian/appearance.json`, `.obsidian/snippets/study-ergonomics.css`)**:
   - Disattivazione `"showInlineTitle": false` in `app.json`.
   - Creazione dello snippet `study-ergonomics.css` con palette Style Guide per `mark, .cm-highlight`, tag `y, v, r`, classi colore, spaziatura `mjx-container` e padding callout collassati; registrazione in `appearance.json`.
4. **Verifica & Non-Regressione**:
   - Esecuzione completa della test suite `unittest` (273 test passati).
   - Ingestione e collaudo pratico su `03 - Inbox/08 FdM.md`.

## Task List

- [x] **Task 1: Refactoring Prompt AI in `99 - Meta/Scripts/brain_ingest.py`**
  - Aggiornare Regola 1 con Scheletro Esecutivo, elenchi telegrafici (stile `Gabriele d'Annunzio.md`) e limite prosa a max 3-4 righe.
  - Aggiornare Regola 2 con Pattern Dual-Layer per Teoremi/Dimostrazioni (`> [!abstract]- Dimostrazione Formale Passo-Passo`) ed eliminazione dei 5 sotto-bullet obbligatori ovunque.
  - Aggiornare Regola 3 con Budget rigoroso `<mark>` (max 1 giallo e 2-3 viola per sotto-sezione).
  - Aggiornare Regola 7 con generazione del callout `> [!question] Chiarimento sul tuo dubbio` per dubbi e perplessità espressi dall'utente.

- [x] **Task 2: Allineamento Documentazione in `Style Guide.md` e `SKILL.md`**
  - Aggiornare `99 - Meta/Style Guide.md` con parsimonia evidenziatori per l'AI, stile telegrafico e pattern Dual-Layer.
  - Aggiornare `.agents/skills/brain-ingest/SKILL.md` con le nuove direttive.

- [x] **Task 3: Configurazione Obsidian & Snippet CSS `study-ergonomics.css`**
  - Impostare `"showInlineTitle": false` in `.obsidian/app.json`.
  - Creare `.obsidian/snippets/study-ergonomics.css` (stili `mark`, `.cm-highlight`, `y`/`v`/`r`, palette completa, margini `mjx-container`, padding callout collassati).
  - Aggiungere `"study-ergonomics"` a `"enabledCssSnippets"` in `.obsidian/appearance.json`.

- [x] **Task 4: Verifica con Test Suite & Test Flusso su `03 - Inbox/08 FdM.md`**
  - Eseguire i test unitari (`python3 -m unittest discover -s tests`).
  - Testare il processing di `03 - Inbox/08 FdM.md` verificando la presenza del callout `> [!question]` e dei callout collassati delle dimostrazioni.
