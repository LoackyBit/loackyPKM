---
title: "Corrections Log"
date: 2026-07-17
updated: 2026-08-25T00:10
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY|Memory Index]]

# 🧠 Memory Topic: Corrections Log

## Regole Critiche & Correzioni Rilevate

- **[STRICT] No Dataview in Dashboard (D-03):** Non utilizzare blocchi ```dataview. La dashboard deve essere scritta in puro Markdown statico autogenerato per massima compatibilità con Quartz e mobile (`99 - Meta/Vault Health Dashboard.md`).
- **[STRICT] 3 Macro-Skills Consolidate (D-14):** Utilizzare esclusivamente le 3 macro-skills `brain-health`, `brain-ingest`, e `brain-recall`. Tutte le micro-skills legacy (`audit`, `meta`, `tidy`, `link`, `process-inbox`, `nota`, `dream`) sono state eliminate.
- **[STRICT] Preservazione Forward-Links (D-02):** I wiki-link verso note future pianificate in Title Case "da creare" (`[FORWARD-LINK]`) non devono essere eliminati o trattati come errori bloccanti durante le operazioni di auto-fix.
- **[STRICT] Evidenziazioni Senza Backtick (D-10):** Non racchiudere mai i tag HTML `<mark style="..."><b>...</b></mark>` tra backtick markdown (`` `<mark...>` `` ❌). Devono essere renderizzati come HTML inline puro.
- **[STRICT] Zero-Hallucination Guard in Recall (D-19):** Se un concetto cercato non è presente nel Vault, notificare esplicitamente l'assenza all'utente senza allucinare o integrare conoscenza esterna generica.
- **[STRICT] Concorrenza con Lock per-Fonte (D-12):** Utilizzare lock atomici per-sorgente (`/tmp/brain_ingest_<sha256>.lock`) per consentire ingestioni concorrenti senza bloccare l'intero sistema.
- **[STRICT] Human-in-the-Loop Staging & Tri-State GTD (D-06, D-11):** Tutte le note generate da AI atterrano in `03 - Inbox/` con `status: draft` e vengono registrate in `03 - Inbox/Review Dashboard.md` per approvazione (`[x]`) o rifiuto (`[-]`).
- **[STRICT] Schema Frontmatter a 10 Campi (D-04, D-10):** Sequenza fissa ordinata: `status` (o `stage`+`draft`), `type`, `area`, `related`, `aliases`, `source`, `title`, `date`, `updated`, `tags`, `summary`.
- **[STRICT] Quartz Blog Stages:** Mantenere i livelli di `stage` personalizzati (es. `seed 🌱`, `growing 🌿`, `fine-tuned 🧠`) nel frontmatter del Blog.
- **[STRICT] Naming Title Case (D-13):** Non usare mai trattini (kebab-case) o snake_case nei nomi dei file nel vault. Utilizzare sempre il **Title Case intelligente** con spazi, mantenendo articoli, congiunzioni e preposizioni in minuscolo (es. `Nome della Nota.md`).
- **[STRICT] No Convenzioni GitHub/Sviluppo:** Ignorare completamente le convenzioni globali di sviluppo software/GitHub (es. regole di branch naming `type/scope/desc`, commit messages in formato conventional commits per note, o kebab-case per i nomi di file/cartelle) all'interno di questo vault. Attenersi unicamente alle convenzioni locali del Vault.
- **[STRICT] Scrittura Obbligatoria su Disco:** Quando si elaborano note o proposte, l'agente deve **SEMPRE eseguire la scrittura effettiva sul file system usando lo strumento `write_to_file`**, e non limitarsi mai a mostrare il testo generato solo nella chat.

---

## Storico Segnali ed Espressioni Rilevate nei Transcript
- *Rilevato:* "<USER_REQUEST> perché non vedo hooks presenti? </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> però nei metadati di @[03 - Inbox] non c'è video_url </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> riprendi, non sono riuscito a rispondere all'ultima domanda, riproponimela </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> non funziona, non vedo gli hooks, controlla la documentazione </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> il mio obiettivo, come già sai, è costruire un PKM AI system autonomo. una volta soddisfatto vorrei però pubblicarlo su github personalizzabile... </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> cancella tutti i file che non sono foto o video </USER_REQUEST>"
- *Rilevato:* "<USER_REQUEST> ok no cambiamo prospettiva: io inserisco il contenuto raw brutale, e tu rielabori e applichi propriamente uno dei template disponibili... </USER_REQUEST>"
