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
   - **YouTube URL:** Genera nota grezza strutturata secondo `99 - Meta/Template/Raw Inbox Note.md` con metadati video e `ready: true`. Tramite `youtube_helper.py` estrae trascrizione con capitoli e screenshot visivi 720p `-q:v 2` in `99 - Meta/Clipboard/`.
   - **Articoli Web / URL:** Scraping e conversione in Markdown pulito salvato in nota grezza `ready: true`.
   - **Testo Libero / Appunti:** Strutturazione di testi grezzi incollati in chat o catture veloci in formato `Raw Inbox Note.md`.
   - **File Locali & Inbox Scanner (`--scan-inbox`):** Rilevamento automatico di appunti grezzi in `03 - Inbox/` con `ready: true`.

2. **Ciclo di Vita Deterministico (`seen-` ➔ `raw-` + `proposed-`):**
   - **Fase 1 (Acquisizione & Lock):** La nota grezza viene rinominata in `03 - Inbox/seen-<Titolo>.md` sotto lock univoco SHA-256 (`/tmp/brain_ingest_<hash>.lock`).
   - **Fase 2 (Estrazione Dati):** Se video YouTube, `youtube_helper.py` arricchisce `seen-<Titolo>.md` con trascrizione integrale ed embedding delle immagini `![[screenshot.jpg]]`.
   - **Fase 3 (Rielaborazione AI Strutturata):** Vengono applicati i template dedicati (`99 - Meta/Template/AI YouTube Transcript.md`, `AI Activity Log.md`, `Global AI Note.md`), i principi di `02 - Atlas/Prompt/Content Memory.md` e le regole di `99 - Meta/Style Guide.md` (evidenziazioni HTML `<mark>` giallo/viola e diagrammi Mermaid quotati).
   - **Fase 4 (Scrittura Proposta & Archiviazione Raw):** Viene salvata la nota elaborata in `03 - Inbox/proposed-<Titolo>.md` con `target_path: "<cartella_destinazione>/<Titolo>.md"` e frontmatter canonico a 10 campi. La nota grezza originale viene rinominata in `03 - Inbox/raw-<Titolo>.md`.

3. **Staging Protetto & Tri-State GTD Review:**
   - La proposta viene registrata in `03 - Inbox/Review Dashboard.md` come riga di revisione:
     `- [ ] Approva [[proposed-<Titolo>]] (originale: [[raw-<Titolo>]])`
   - **Approvazione Utente (`[x]`):** Promozione di `proposed-<Titolo>.md` a `status: permanent`, spostamento nel percorso definitivo specificato in `target_path` (o auto-classificato in `02 - Atlas/` o `05 - Blog/`), aggiornamento breadcrumbs, autolinking semantico ed eliminazione di `raw-<Titolo>.md`.
   - **Rifiuto Utente (`[-]`):** Cancellazione sicura sia della proposta `proposed-<Titolo>.md` sia dell'originale `raw-<Titolo>.md`, con pulizia degli screenshot associati in `99 - Meta/Clipboard/`.
   - Storico audit persistente salvato in `99 - Meta/logs/inbox_history.md`.

4. **Rilevamento Globale Anti-Duplicati & Blocco Rielaborazioni:**
   - Se una risorsa (URL YouTube `video_url`/`source` o articolo web) o una nota con titolo non generico equivalente è **già presente** in `02 - Atlas/` o `05 - Blog/`, l'ingestione viene **bloccata immediatamente** sia da invocazione CLI/chat `/brain-ingest` sia dal watcher daemon `watch.sh` su note da template `Raw Inbox Note.md`.
   - La richiesta viene bloccata e registrata automaticamente sotto `## ⚠️ Errori di Acquisizione & Azioni Richieste` in `03 - Inbox/Review Dashboard.md` con la riga `- [ ] [!] Riprova: <URL> — Motivo: Duplicato rilevato: la risorsa esiste già in [[<Percorso>]]`.
   - Il flag `ready: true` della nota grezza in `03 - Inbox/` viene commutato in `ready: false` per impedire loop del demone watcher.
   - Protezione da collisioni omonime in Atlas e da duplicazione di sorgenti in fase di approvazione GTD finale.

5. **Autolinking Semantico Contestuale:**
   - Scansione automatica dell'indice dei titoli reali del Vault per collegare concetti chiave (`[[Nota Esistente]]`, max 2 occorrenze per target) senza allucinare note inesistenti.
   - Sincronizzazione automatica del campo `related: [...]` nel frontmatter YAML e della sezione `## Collegamenti`.

6. **Feedback Live in Dashboard (`## ⏳ In Elaborazione`):**
   - Durante il processamento, la dashboard mostra l'avanzamento trasparente:
     `Fase 1/4: Lettura nota grezza & template...` ➔ `Fase 2/4: Ricerca contesto nel Second Brain...` ➔ `Fase 3/4: Rielaborazione concettuale & Style Guide...` ➔ `Fase 4/4: Scrittura della nota proposta...`.

---

## 🛠️ CLI & Invocazione

Il motore Python unificato è `99 - Meta/Scripts/brain_ingest.py`.

### Ingestione da CLI
```bash
# Ingestione YouTube (estrazione trascrizione, raw + proposed staging)
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..." --depth sintesi

# Ingestione YouTube con estrazione forzata frame 720p in Clipboard/
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..." --depth approfondimento --extract-frames

# Ingestione Articolo Web con classificazione euristica automatica
python3 "99 - Meta/Scripts/brain_ingest.py" "https://example.com/article"

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

## 🎨 Standard Visivi & Style Guide del Vault

Ogni nota prodotta deve rispettare rigorosamente `99 - Meta/Style Guide.md`:

1. **Evidenziazioni HTML Valide (Senza Backtick):**
   - **Concetti Cardine (Giallo):** `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>`
   - **Concetti Secondari (Viola):** `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>`
   - *CRITICO:* Non racchiudere mai i tag HTML `<mark>` tra backtick markdown (`` `<mark...>` `` ❌).
2. **Diagrammi Mermaid:**
   - Includere sempre apici per i nodi con spazi o parentesi: `id["Etichetta (Dettaglio)"]`.
   - Nessun tag HTML all'interno dei nodi Mermaid.
3. **Sezione Finale di Rete:**
   ```markdown
   ---
   ## Collegamenti
   - [[Nota Correlata 1]]
   - [[Nota Correlata 2]]
   ```
