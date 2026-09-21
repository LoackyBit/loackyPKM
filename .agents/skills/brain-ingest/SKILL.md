---
name: brain-ingest
description: Polymorphic intake engine for YouTube videos, web articles, pasted text, and local documents with Title Case naming, 10-field YAML, contextual autolinking, raw/proposed lifecycle, and tri-state GTD review.
---
# Skill: /brain-ingest (Universal Ingestion Pipeline)

Pipeline universale di ingestione, arricchimento e trasformazione della conoscenza per il Second Brain.
Replicata in modo deterministico sia da invocazione diretta (`/brain-ingest`, `brain_ingest.py <source>`) sia dal watcher in background (`watch.sh`) all'aggiunta di note da template `Raw Inbox Note.md`.

---

## 🎯 Obiettivi e Flusso Operativo Unificato

1. **Routing Polimorfico dell'Input & Inizializzazione Raw Note:**
   - **YouTube URL:** Genera nota grezza strutturata secondo `99 - Meta/Template/Raw Inbox Note.md` con metadati video e `ready: true`. Tramite `youtube_helper.py` estrae trascrizione con capitoli e screenshot visivi opzionali 720p `-q:v 2` in `99 - Meta/Clipboard/`.
   - **Articoli Web / URL:** Scraping e conversione in Markdown pulito salvato in nota grezza `ready: true`.
   - **Testo Libero / Appunti:** Strutturazione di testi grezzi incollati in chat o catture veloci in formato `Raw Inbox Note.md`.
   - **File Locali & Inbox Scanner (`--scan-inbox`):** Rilevamento automatico di appunti grezzi in `03 - Inbox/` con `ready: true`.

2. **Ciclo di Vita Deterministico a 3 Macro-Fasi (`Draft/` & `Source/`):**
   - **Fase 1/3 (Estrazione Sorgente):** L'ingestione della risorsa viene eseguita sotto lock univoco SHA-256 (`/tmp/brain_ingest_<hash>.lock`). La dashboard `03 - Inbox/Review Dashboard.md` viene immediatamente aggiornata registrando la risorsa sotto `## ⏳ In Elaborazione` come `- ⏳ <URL|Titolo> (Fase 1/3: Estrazione Sorgente...)`. Il contenuto grezzo viene salvato in `03 - Inbox/Source/<Titolo>.md`. La nota è rigorosamente **esclusa** da `## 📥 Note in Attesa di Approvazione`.
   - **Fase 2/3 (Rielaborazione Concettuale AI):** La nota transita a `- ⏳ [[Draft/<Titolo>]] (Fase 2/3: Rielaborazione Concettuale AI...)`. L'agente AI esegue la rielaborazione concettuale approfondita (con filtro anti-sponsor/anti-slop ed estrazione principi primi), applica le evidenziazioni `<mark>` (giallo/viola) e genera la sintesi esecutiva (120-180 caratteri, max 200). La bozza intermedia è salvata in `03 - Inbox/Draft/<Titolo>.md` con `status: in-progress`.
   - **Fase 3/3 (Autolinking & Staging):** Autolinking semantico su titoli reali del Vault (max 2 per target), sincronizzazione di `related: [...]` nel frontmatter, passaggio a `status: draft` e rimozione da `In Elaborazione`. La nota transita in `## 📥 Note in Attesa di Approvazione`.

3. **Staging Protetto & Tri-State GTD Review:**
   - La proposta viene registrata in `03 - Inbox/Review Dashboard.md` come riga di revisione:
     `- [ ] Approva [[Draft/<Titolo>]] (fonte: [[Source/<Titolo>]])`
   - **Approvazione Utente (`[x]`):** Promozione di `Draft/<Titolo>.md` a `status: permanent`, spostamento nel percorso definitivo specificato in `target_path` (auto-classificato semanticamente nella sotto-cartella tematica appropriata di `02 - Atlas/...` come `Tech & AI/Agenti & Automazione`, `Finance/Fisco & Gestione Patrimoniale`, `Personal Growth & Health/Produttivita & Abitudini`, ecc., oppure `05 - Blog/`), aggiornamento breadcrumbs e autolinking semantico.
     - *Trascrizioni YouTube / Scraping Web:* Il file in `Source/` viene eliminato automaticamente per mantenere pulito il Vault.
     - *Appunti manuali dell'utente:* Il file in `Source/` viene archiviato permanentemente in `99 - Meta/Archive/<Titolo>.md`.
   - **Rifiuto Utente (`[-]`):** Cancellazione atomica e sicura sia di `Draft/<Titolo>.md` sia di `Source/<Titolo>.md`, con pulizia di eventuali screenshot associati in `99 - Meta/Clipboard/`.
   - Storico audit persistente salvato in `99 - Meta/logs/inbox_history.md`.

4. **Rilevamento Globale Anti-Duplicati & Blocco Rielaborazioni:**
   - Se una risorsa (URL YouTube `video_url`/`source` o articolo web) o una nota con titolo non generico equivalente è **già presente** in `02 - Atlas/` o `05 - Blog/`, l'ingestione viene **bloccata immediatamente** sia da invocazione CLI/chat `/brain-ingest` sia dal watcher daemon `watch.sh`.
   - La richiesta bloccata viene registrata automaticamente sotto `## ⚠️ Errori di Acquisizione & Azioni Richieste` in `03 - Inbox/Review Dashboard.md` con la riga `- [ ] [!] Riprova: <URL> — Motivo: Duplicato rilevato: la risorsa esiste già in [[<Percorso>]]`.
   - Il flag `ready: true` della nota grezza in `03 - Inbox/` viene commutato in `ready: false` per impedire loop del demone watcher.
   - Protezione da collisioni omonime in Atlas e da duplicazione di sorgenti in fase di approvazione GTD finale.

5. **Autolinking Semantico Contestuale:**
   - Scansione automatica dell'indice dei titoli reali del Vault per collegare concetti chiave (`[[Nota Esistente]]`, max 2 occorrenze per target) senza allucinare note inesistenti.
   - I collegamenti sono incorporati organicamente nella prosa della nota e sincronizzati nel campo YAML `related: [...]` (senza sezione boilerplate `## Collegamenti`).

6. **Feedback Live in Dashboard (Layout a 4 Sezioni):**
   - `03 - Inbox/Review Dashboard.md` mantiene 4 sezioni statiche Markdown:
     1. `## ⏳ In Elaborazione`: traccia i processi attivi in tempo reale; include il pulsante `🛑 Interrompi elaborazioni attive (Panic Button)`.
     2. `## 📥 Note in Attesa di Approvazione`: righe di approvazione tri-state (`[ ]`, `[x]`, `[-]`) generate solo per bozze completate.
     3. `## ⚠️ Errori di Acquisizione & Azioni Richieste`: errori di trascrizione o duplicati con retry `[x]` o dismiss `[-]`.
     4. `## 📜 Storico Recente`: ultime 10 azioni elaborate sincronizzate con `inbox_history.md`.

---

## 🛠️ CLI & Invocazione

Il motore Python unificato è `99 - Meta/Scripts/brain_ingest.py`.

### Ingestione da CLI
```bash
# Ingestione YouTube (estrazione trascrizione, profondità approfondimento di default)
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..."

# Ingestione YouTube in modalità sintesi (compatta, 1-2 schermate)
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..." --depth sintesi

# Ingestione YouTube con estrazione forzata frame 720p in Clipboard/
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..." --depth approfondimento --extract-frames

# Ingestione Articolo Web con classificazione euristica automatica
python3 "99 - Meta/Scripts/brain_ingest.py" "https://example.com/article"

# Ingestione con Sinergia Metacognitiva NotebookLM (Alessandro de Concini)
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..." --course "Algoritmi e Strutture Dati" --nlm

# Ingestione File Locale o Testo Diretto con NLM
python3 "99 - Meta/Scripts/brain_ingest.py" "03 - Inbox/appunti.md" --course "Sistemi Operativi" --nlm

# Ingestione File Locale o Testo Diretto
python3 "99 - Meta/Scripts/brain_ingest.py" "03 - Inbox/appunti.md" --target-dir "02 - Atlas/Education & Learning"

# Scansione automatica appunti grezzi in Inbox (creati con Raw Inbox Note.md con ready: true)
python3 "99 - Meta/Scripts/brain_ingest.py" --scan-inbox
```

### Processamento Approvazioni GTD
```bash
# Processa tutte le righe [x] (promozione) e [-] (scarto) in Review Dashboard.md
python3 "99 - Meta/Scripts/brain_ingest.py" --process-approvals
```

---

## 🧠 Sinergia Metacognitiva & NotebookLM (`--nlm`)

Quando invocato con il flag esplicito `--nlm` (D-03), il sistema attiva una consultazione preliminare del notebook metodologico di **Alessandro de Concini** (ID: `b7534dad-1515-44c1-bcc5-c77992b5e416`) tramite la CLI `nlm` e opera secondo una **Sinergia Metacognitiva a Doppio Canale**:

1. **Canale 1 (Invisibile al Vault, Guida Attiva per l'LLM):**
   - Le direttive estratte vengono iniettate direttamente nel prompt di sistema di `agy` durante la *Fase 2/3 (Rielaborazione Concettuale AI)*.
   - Vincoli attivi:
     - **Schematizzazione causale:** Generazione obbligatoria di diagrammi logici Mermaid a cascata con nodi quotati `id["..."]` per modelli mentali o dipendenze concettuali (SYN-01).
     - **Densità e Principi Primi:** Distillazione rigorosa dei concetti cardine, eliminando riempitivi, frasi fatte e aneddoti superflui (SYN-01).
     - **Active Recall & Atomicità:** Formulazione di definizioni ed espressioni matematiche/tecniche con esplicitazione di ipotesi e condizioni di validità, favorendo l'atomicità semantica per la successiva generazione di flashcard Anki (SYN-02).

2. **Canale 2 (Permanente nel Vault):**
   - In calce alla nota permanente viene appesa la sezione pulita `## Direttive Metacognitive` (zero emoji nel titolo H2, conforme alle regole del vault) contenente le linee guida di de Concini elaborate da NotebookLM (D-06).
   - Meccanismo preventivo anti-duplicazione regex per evitare duplicazioni di titoli se l'LLM ha già incorporato una sezione analoga.

3. **Politica Fail-Fast Assoluta (D-04, NLM-02):**
   - Se `--nlm` è presente e l'interrogazione remota fallisce per token scaduto (`Authentication expired`), timeout (120s) o assenza di connessione, il processo si arresta immediatamente con exit code 1 e stampa:
     `ERRORE: Impossibile consultare NotebookLM. Esegui 'nlm login' o verifica la connessione.`
   - Nessun fallback silenzioso: l'utente viene avvisato esplicitamente di riautenticarsi tramite `nlm login` da terminale.

---

## 🎨 Standard Visivi & Style Guide del Vault

Ogni nota prodotta deve rispettare rigorosamente `99 - Meta/Style Guide.md`:

1. **Titoli e Intestazioni (H1, H2, H3):**
   - Zero emoji nei titoli (es. `# Titolo Nota`, `## Sintesi Esecutiva`, `## Quadro Concettuale`). Mai `# 🎯 Titolo` o `## 🔑 Takeaways`.
2. **Evidenziazioni HTML Valide (Senza Backtick):**
   - **Concetti Cardine (Giallo):** `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>`
   - **Concetti Secondari (Viola):** `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>`
   - *CRITICO:* Non racchiudere mai i tag HTML `<mark>` tra backtick markdown (`` `<mark...>` `` ❌).
3. **Diagrammi Mermaid:**
   - Includere sempre apici per i nodi con spazi o parentesi: `id["Etichetta (Dettaglio)"]`.
   - Nessun tag HTML all'interno dei nodi Mermaid.
4. **Formule Matematiche (LaTeX):**
   - Usare `$formula$` per formule inline o `$$formula$$` per blocchi matematici.
5. **Assorbimento Organico dei Collegamenti:**
   - I collegamenti semantici a note esistenti sono integrati nel testo (`[[Target Note]]`) e sincronizzati in `related: [...]` nel frontmatter YAML. Nessun blocco finale `## Collegamenti`.
6. **Flashcard Anki Contestuali (Conformità Doc Ufficiale Anki & obsidian-to-anki-plugin):**
   - Struttura a callout collassabile: `> [!tip]- Flashcard: [Concetto]`, seguita dal blocco racchiuso tra delimitatori `%% ... %%`.
   - Nessun carattere `>` sulle righe interne del commento `%%`.
   - Modelli conformi: `Basic` (Front:/Back:) per principi primi/spiegazioni causali; `Cloze` (Text:/Extra:) per teoremi e formule.
   - Cloze deletion: rigorosamente a doppio due punti `{{c1::contenuto}}`.
   - Formule MathJax: delimitatori standard `$..$` e `$$..$$`.
   - Derivate matematiche: usare SEMPRE `^\prime` o `^{\prime\prime}` (es. $f^\prime(\xi)$), MAI apostrofi `$f'(x)$`, per scongiurare collisioni con l'escape HTML del plugin (`&#039;` -> tag `039` -> formula corrotta in `f&;`).
   - Valori assoluti: usare `\vert` anziché `|`. Spaziare le graffe TeX nelle cloze (`{ {` o `\left\{...\right\}`).
   - Nessun `<!--ID: -->` manuale generato dall'AI.
