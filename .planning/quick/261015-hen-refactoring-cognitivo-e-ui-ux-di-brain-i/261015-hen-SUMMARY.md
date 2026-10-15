---
id: 261015-hen
slug: refactoring-cognitivo-e-ui-ux-di-brain-i
title: "Refactoring Cognitivo e UI/UX di brain-ingest (Scheletro Visivo & Co-Pilota Attivo)"
type: quick-task
status: complete
date: 2026-10-15
---

# Quick Task 261015-hen: Refactoring Cognitivo e UI/UX di `brain-ingest` — Summary

## Sintesi Risultati
Completata con successo la transizione architetturale del motore di elaborazione della conoscenza (`99 - Meta/Scripts/brain_ingest.py`) da "ghostwriter enciclopedico" prolisso a "scheletro visivo e co-pilota attivo".

### 1. Refactoring Prompt AI (`99 - Meta/Scripts/brain_ingest.py`)
- **Architettura "Scheletro Esecutivo + Progressive Disclosure":**
  - Preservata fedelmente la struttura, la numerazione e l'ordine logico degli appunti grezzi dell'utente (`NOTA ORIGINALE`).
  - Sostituiti i muri di prosa continua accademica con elenchi puntati o numerati telegrafici, densi e schematici (ispirati al modello stilistico di `99 - Meta/Reference/Gabriele d'Annunzio.md`), limitando la prosa continua a massimo 3-4 righe di introduzione contestuale per sezione.
- **Pattern Dual-Layer per Teoremi e Dimostrazioni:**
  - Nel flusso principale o nel callout del teorema vengono mostrati **solo** l'enunciato formale, la formula LaTeX centrale `$$...$$` e l'**Idea chiave / Strategia della dimostrazione** in massimo 2-3 bullet sintetici che spiegano il *perché* logico funziona.
  - I passaggi algebrici estesi e le derivazioni dettagliate sono racchiusi in un **callout collassato di default**:
    `> [!abstract]- Dimostrazione Formale Passo-Passo` (con tutte le righe interne prefissate da `> ` affinché rimanga realmente chiuso in Obsidian).
- **Eliminazione dei 5 Sotto-Bullet Fissi Ovunque:**
  - Rimosso l'obbligo rigido dei 5 punti fissi per ogni proposizione o lemma matematico elementare.
  - Resi condizionali `Significato dei simboli (con unità SI)` e `Condizioni di validità` solo per formule fisiche, ingegneristiche o multivariate con parametri non auto-evidenti.
- **Budget Rigoroso delle Evidenziazioni HTML (`<mark>`):**
  - Limitazione stringente: **al massimo 1 evidenziazione gialla (`#cc8800`) per sotto-sezione (concetto cardine)** e **massimo 2-3 evidenziazioni viola (`#9a54c1`) per sotto-sezione**.
  - Resto del testo pulito e leggero con normale `**grassetto**` e `*corsivo*` Markdown per non affaticare la lettura in Live Preview e consentire l'evidenziazione manuale dello studente in fase di studio attivo.
- **Risoluzione Attiva dei Dubbi Utente:**
  - I commenti o perplessità espressi dall'utente negli appunti grezzi (es. `%% AI: non ho capito... %%`) vengono risolti puntualmente nel punto esatto del testo tramite callout dedicato:
    `> [!question] Chiarimento sul tuo dubbio`
    mentre i marcatori di commento originali vengono ripuliti dal corpo finale.

### 2. Allineamento Documentazione & Normativa
- **`99 - Meta/Style Guide.md`**:
  - Aggiornata la sezione "Gerarchia evidenziatori" con il budget di parsimonia per l'AI e lo stile schematico/telegrafico a scheletro esecutivo.
  - Formalizzato il pattern Dual-Layer per teoremi e dimostrazioni in "Anatomia delle Note e Tipografia".
  - Documentati i callout `> [!question] Chiarimento sul tuo dubbio` per i dubbi inline.
- **`.agents/skills/brain-ingest/SKILL.md`**:
  - Aggiornati gli standard visivi con budget evidenziatori, progressive disclosure per teoremi/dimostrazioni e risoluzione dubbi utente.

### 3. Ergonomia UI/UX Obsidian & Snippet CSS
- **`.obsidian/app.json`**:
  - Impostato `"showInlineTitle": false` eliminando la duplicazione del titolo nativo sopra l'`# H1` della nota.
- **`.obsidian/appearance.json`**:
  - Registrato lo snippet `"study-ergonomics"` in `"enabledCssSnippets"`.
- **`.obsidian/snippets/study-ergonomics.css`**:
  - Creato lo snippet con la palette completa della Style Guide per `mark, .cm-highlight`, tag rapidi di studio `<y>`, `<v>`, `<r>` e classi colore (`.yellow`, `.purple`, `.red`, `.viola`, `.rosso`, `.giallo`).
  - Spaziatura aumentata per blocchi display MathJax (`mjx-container[display="true"]`).
  - Padding compatto ridotto per i callout collassati (`.callout.is-collapsed`), garantendo l'ordine visivo pulito di una dispensa LaTeX.

### 4. Verifica, Non-Regressione e Collaudo
- **Test Suite Automatica**:
  - Aggiunto il test di validazione `test_enrich_draft_with_ai_cognitive_skeleton_and_ergonomics` in `tests/test_brain_ingest.py`.
  - Eseguita l'intera test suite: **273 test passati con successo (0 fallimenti, 0 errori)**.
- **Collaudo su `03 - Inbox/08 FdM.md`**:
  - La bozza prodotta in `03 - Inbox/Draft/08 FdM.md` ha una dimensione snella di 33 KB (rispetto ai precedenti 65 KB).
  - Il dubbio dell'utente `%% AI: non ho capito il passaggio dove si introduce l'insieme k appartenente a Z tale che n*a < k %%` ha generato il callout dedicato `> [!question] Chiarimento sul tuo dubbio: Introduzione dell'insieme $A = \{k \in \mathbb{Z} \mid n a < k\}$` con spiegazione logico-costruttiva dettagliata.
  - I teoremi e le proposizioni (Archimede, densità di $\mathbb{Q}$ in $\mathbb{R}$, minimo in $\mathbb{Z}$, binomio) implementano il pattern Dual-Layer: idea chiave visibile e passaggi algebrici racchiusi in `> [!abstract]- Dimostrazione Formale Passo-Passo` collassati.
