---
name: brain-ingest
description: Polymorphic intake engine for YouTube videos, web articles, pasted text, and local documents with Title Case naming, 10-field YAML, contextual autolinking, and tri-state GTD review.
---
# Skill: /brain-ingest (Universal Ingestion Pipeline)

Pipeline universale di ingestione e trasformazione della conoscenza per il Second Brain.
Sostituisce e consolida le precedenti micro-skills `process-inbox`, `link` e `nota`.

---

## 🎯 Obiettivi e Flusso Operativo

1. **Routing Polimorfico dell'Input:**
   - **YouTube URL:** Estrazione metadati, trascrizione con timestamp cliccabili, capitoli e screenshot visivi opzionali in `99 - Meta/Clipboard/`.
   - **Articoli Web / URL:** Scraping e conversione in Markdown pulito privo di boilerplate/ads.
   - **Testo Libero / Appunti:** Strutturazione di testi grezzi incollati in chat o catture veloci.
   - **File Locali:** Elaborazione di file `.md`, `.txt` o documenti presenti in `03 - Inbox/`.
2. **Profondità Modulare di Elaborazione:**
   - **`sintesi` (Executive Summary):** Sintesi ad alta densità informativa, definizioni chiave e takeaway azionabili (~500-1000 parole).
   - **`approfondimento` (Studio Accademico / Deep Study):** Analisi dettagliata, meccanismi di funzionamento, tabelle comparative, callout ed esempi applicativi (>2000 parole, ex standard `nota`).
3. **Staging Protetto & Tri-State GTD Review:**
   - La nota generata atterra sempre in `03 - Inbox/<Titolo in Title Case>.md` con `status: draft`.
   - Viene registrata automaticamente in `03 - Inbox/Review Dashboard.md` come checkbox `- [ ] Approva [[Titolo]]`.
   - Approvazione utente (`[x]`) -> Promozione a `status: permanent` e smistamento in `02 - Atlas/` o `05 - Blog/`.
   - Rifiuto utente (`[-]`) -> Cancellazione sicura della bozza e pulizia degli screenshot temporanei.
4. **Autolinking Semantico Contestuale:**
   - Scansione automatica dell'indice dei titoli reali del Vault per collegare concetti chiave (`[[Nota Esistente]]`, max 2 occorrenze per target) senza allucinare note inesistenti.
   - Sincronizzazione automatica del campo `related: [...]` nel frontmatter YAML e della sezione `## Collegamenti`.
5. **Concorrenza & Locking per-Fonte:**
   - Lock fine-grained basato su SHA-256 (`/tmp/brain_ingest_<hash>.lock`) che consente l'ingestione simultanea di sorgenti diverse senza collisioni.

---

## 🛠️ CLI & Invocazione

Il motore Python sottostante è `99 - Meta/Scripts/brain_ingest.py`.

### Ingestione da CLI
```bash
# Ingestione YouTube (Sintesi esecutiva con timestamp)
python3 "99 - Meta/Scripts/brain_ingest.py" --url "https://www.youtube.com/watch?v=..." --depth sintesi

# Ingestione YouTube con estrazione screenshot in Clipboard
python3 "99 - Meta/Scripts/brain_ingest.py" --url "https://www.youtube.com/watch?v=..." --depth approfondimento --screenshots

# Ingestione Articolo Web
python3 "99 - Meta/Scripts/brain_ingest.py" --url "https://example.com/article" --area tech

# Ingestione File Locale in Inbox
python3 "99 - Meta/Scripts/brain_ingest.py" --file "03 - Inbox/raw-notes.md" --title "Calcolo Differenziale" --area education

# Ingestione Testo Diretto
python3 "99 - Meta/Scripts/brain_ingest.py" --text "Contenuto raw..." --title "Architettura Transformers" --area tech
```

### Processamento Approvazioni GTD
```bash
# Processa tutte le righe [x] e [-] segnate in Review Dashboard.md
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
3. **Sezione Finale di Rete:**
   ```markdown
   ---
   ## Collegamenti
   - [[Nota Correlata 1]]
   - [[Nota Correlata 2]]
   ```
