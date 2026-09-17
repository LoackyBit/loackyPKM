# Milestone v1.0.1-alpha — Project Summary

**Generated:** 2026-09-05  
**Purpose:** Team onboarding and project review  
**Milestone:** `v1.0.1-alpha` (Code Review & Bug Fixing)  

---

## 1. Project Overview

- **What This Is:** Un Second Brain e Personal Knowledge Management (PKM) su base Obsidian, trasformato in un digital garden intelligente e integrato con Antigravity CLI per operare come un "NotebookLM locale". Permette di raccogliere note, appunti universitari (*Ingegneria Informatica*), articoli e video YouTube, organizzarli con una tassonomia semantica aperta (ACE Topography a 6 macro-cartelle) e interrogarli via chat per recuperare memorie, sintesi e connessioni interdisciplinari con citazioni dirette alle fonti.
- **Core Value Proposition:** Rendere l'acquisizione, la manutenzione e l'interrogazione della conoscenza personale fluidi, immediati e a zero attrito, eliminando la frammentazione degli strumenti con fondamenta strutturali solide, standardizzazione AST dei metadati e governance a puro Markdown statico.
- **Target Users & Context:** Studenti universitari, ricercatori e sviluppatori che necessitano di una base di conoscenza ad alta densità informativa, sincronizzata localmente, esportabile staticamente via Quartz Digital Garden, senza dipendenze da server vettoriali proprietari o plugin dinamici bloccanti (No Dataview).
- **Milestone Scope:** Risoluzione integrale delle criticità di sicurezza, dei bug logici di staging/ingestion, delle race condition di concorrenza, delle discrepanze diacritiche/APFS e del debito tecnico emersi dal Clean Code Audit Report del 2026-09-03.
- **Status:** Tutte le 6 fasi (Phases 07-12) e tutti i 12 piani pianificati sono stati eseguiti, verificati con esito `passed` e collaudati con 163/163 test unitari/integrazione passati con successo (100% green).

---

## 2. Architecture & Technical Decisions

Elenco ragionato delle decisioni ingegneristiche e architetturali introdotte in v1.0.1-alpha:

- **Decommissioning Modulo School & Bonifica Credenziali (Phase 07 - SEC-01, SEC-02):**
  - **Decisione:** Eliminazione totale da Git (`git rm -f`) di `config.json`, `fetch-registro.py` e `List.md` legati a ClasseViva; aggiornamento `.gitignore`; preservazione attiva di `Style Guide.md`.
  - **Motivazione:** Elimina alla radice il rischio di credential leak per un modulo dismesso senza aggiungere overhead di configurazione inutile.
  - **Fase:** Phase 07 (Sicurezza Credenziali & Configurazione Dinamica)

- **Risoluzione Dinamica Portabile degli Eseguibili e PATH (Phase 07 - SEC-03):**
  - **Decisione:** Sostituzione dei percorsi assoluti hardcoded `/Users/lorenzo/...` con `shutil.which("agy")` e `Path.home()`, parametrizzazione del template LaunchAgent con `__VAULT_PATH__` e comando `watch.sh install-service`.
  - **Motivazione:** Rende l'intera suite di script e demoni portabile su qualsiasi macchina macOS o container senza vincoli utente.
  - **Fase:** Phase 07 (Sicurezza Credenziali & Configurazione Dinamica)

- **Spostamento Atomico Preventivo in `Source/` e Salvaguardia Note Grezze (Phase 08 - INGEST-01):**
  - **Decisione:** Le note contrassegnate con `ready: true` in `03 - Inbox/` vengono spostate atomicamente in `03 - Inbox/Source/` prima di invocare le fasi AI, eliminando la cancellazione prematura su `file_path`.
  - **Motivazione:** Previene la perdita irrevocabile delle note manoscritte dell'utente in caso di crash o eccezioni del modello AI.
  - **Fase:** Phase 08 (Integrità Ingestion & Salvaguardia Staging)

- **Pulizia Sincronizzata 1:1 delle Bozze Post-AI con `old_title` (Phase 08 - INGEST-02):**
  - **Decisione:** Tracciamento preliminare di `old_title` prima della riassegnazione del titolo concettuale AI (`clean_title = cand_ai`), con rimozione fisica di `Draft/{old_title}.md` e ridenominazione atomica `Source/{old_title}.md` in `Source/{clean_title}.md`.
  - **Motivazione:** Elimina la condizione auto-annullante `clean_title != cand_ai` ed evita l'accumulo di bozze o sorgenti orfane in Inbox.
  - **Fase:** Phase 08 (Integrità Ingestion & Salvaguardia Staging)

- **Purge Frame YouTube su `video_id` e Immagini Markdown (Phase 08 - INGEST-03):**
  - **Decisione:** Al rifiuto `[-]` di una nota, lettura preventiva del documento per ricavare il `video_id` (11 caratteri) e cancellazione mirata di tutti i frame `{video_id}_*.jpg` e `{video_id}_*.png` in `99 - Meta/Clipboard/`, unita alla cancellazione di immagini incorporate nel corpo.
  - **Motivazione:** Azzeramento dei file orfani di screenshot indipendentemente da cambi di titolo post-inferenza.
  - **Fase:** Phase 08 (Integrità Ingestion & Salvaguardia Staging)

- **Supporto Pipe Alias nei Link Wiki della Dashboard & AI Fallback Directory (Phase 08 - INGEST-04):**
  - **Decisione:** Parsing difensivo dei wiki-link della dashboard isolando il basename prima della pipe `|` (`name.split('|')[0]`); rimozione dead code (doppio return); fallback AI leggero con `gemini-3.8-flash-low` e lista controllata di 19 cartelle.
  - **Motivazione:** Evita crash da `FileNotFoundError` su note con alias e classifica le note prive di keyword euristiche in modo intelligente.
  - **Fase:** Phase 08 (Integrità Ingestion & Salvaguardia Staging)

- **Audit YAML Non Distruttivo con Flag `--lint-only` (Phase 09 - HLTH-01):**
  - **Decisione:** Implementazione della routine Single-Source-of-Truth `diagnose_yaml_violations` con stampa a terminale ricca in modalità read-only e rigetto programmatico dei conflitti con `--auto-fix`.
  - **Motivazione:** Consente ispezioni diagnostiche continue senza rischio di mutazioni accidentali sul filesystem.
  - **Fase:** Phase 09 (Governance Vault & Integrità YAML Linter)

- **Preservazione Condizionale Metadati Video & Sincronizzazione Bidirezionale (Phase 09 - HLTH-02):**
  - **Decisione:** `infer_metadata` preserva `video_url` e `channel` per le note di `type: video` (rimuovendoli per le altre tipologie) e sincronizza bidirezionalmente `source` con `video_url` su link YouTube validi.
  - **Motivazione:** Mantiene intatta la tracciabilità delle fonti video durante i cicli di normalizzazione e linting canonico.
  - **Fase:** Phase 09 (Governance Vault & Integrità YAML Linter)

- **Simmetria Diacritica Unicode NFC tra Filename e YAML Title (Phase 09 - HLTH-03):**
  - **Decisione:** Riscritte `clean_filename` e `clean_title_str` per delegare alla funzione SSOT `normalize_title_or_filename`, eliminando la scomposizione distruttiva NFD e preservando le vocali accentate italiane in NFC.
  - **Motivazione:** Ristabilisce la corrispondenza 1:1 tra il nome file e il frontmatter `title`, prevenendo discrepanze di normalizzazione.
  - **Fase:** Phase 09 (Governance Vault & Integrità YAML Linter)

- **Protezione da Collisioni Omonime in `scan_vault` (Phase 09 - HLTH-04):**
  - **Decisione:** `VaultHealthAuditor.scan_vault` traccia i duplicati accidentali nella struttura `duplicate_notes` ed espone le anomalie nella diagnostica, senza sovrascrivere `all_notes` o azzerare `incoming_links`.
  - **Motivazione:** Rispetta l'assunzione fondamentale del Vault (nessuna omonimia) proteggendo l'integrità del grafo concettuale.
  - **Fase:** Phase 09 (Governance Vault & Integrità YAML Linter)

- **Sincronizzazione Dinamica Watcher PID & Panic Abort con Epuration Totale (Phase 10 - PERF-01):**
  - **Decisione:** Risoluzione del file PID tramite `$PID_FILE` -> `/tmp/brain_watcher_{vault_hash}.pid`; `trigger_panic_abort` termina i worker figli salvaguardando il PID del demone `watch.sh` ed eliminando lockfile, bozze parziali in `Draft/` e cancellando lo stato `In Elaborazione`.
  - **Motivazione:** Permette un arresto d'emergenza pulito senza abbattere il demone di sorveglianza e senza lasciare artefatti orfani sul disco.
  - **Fase:** Phase 10 (Retrieval, Concorrenza & Ottimizzazione Performance)

- **Mutex Lock Dedicato `DashboardLock` per `Review Dashboard.md` (Phase 10 - PERF-02):**
  - **Decisione:** Incapsulamento del ciclo read-modify-write di scansione e approvazione in `DashboardLock` con file `/tmp/brain_dashboard_{vault_hash}.lock`, auto-healing (TTL 60s), rientranza di processo e graceful skip per job in background.
  - **Motivazione:** Elimina le race condition e le sovrascritture di checkbox dovute ad accessi concorrenti tra watcher e utente.
  - **Fase:** Phase 10 (Retrieval, Concorrenza & Ottimizzazione Performance)

- **Compressione Cache `.recall_cache.json` a 728KB (<2.5MB) e Pruning Automatico (Phase 10 - PERF-03):**
  - **Decisione:** Sostituzione dell'array `tokens` con `doc_len` e `term_freq`; serializzazione JSON compatta con `separators=(',', ':')`; esclusione della cartella `03 - Inbox` da `IGNORE_FOLDERS`; pruning deterministico delle note eliminate e flag `--reindex`.
  - **Motivazione:** Riduce la dimensione della cache del 96.7% (da 22MB a 728KB), azzerando l'I/O overhead e mantenendo il tempo di lookup sub-millisecondo.
  - **Fase:** Phase 10 (Retrieval, Concorrenza & Ottimizzazione Performance)

- **Conformità Headings Style Guide (Zero Emoji nei Titoli H1-H3 & Rimozione `## Collegamenti`) (Phase 10 - PERF-04):**
  - **Decisione:** Ristrutturazione di `format_output` in 2 sole sezioni pulite (`### Sintesi Esecutiva`, `### Fonti & Citazioni`); eliminazione totale delle emoji da `recall_engine.py` e dai report di `brain_health.py`; eliminazione delle sezioni finali isolate `## Collegamenti`.
  - **Motivazione:** Piena aderenza alle convenzioni formali del Vault e integrazione organica dei collegamenti nella prosa.
  - **Fase:** Phase 10 (Retrieval, Concorrenza & Ottimizzazione Performance)

- **Governance Hardening, Protezione `IGNORE_FILES` & Ricalcolo Metriche (Phase 12 - CLEAN-01):**
  - **Decisione:** Protezione incondizionata di `GEMINI.md`, `AGENTS.md`, `README.md` durante `--auto-fix`; ricalcolo da zero delle metriche di audit prima di rigenerare il dashboard; deduplica `MINOR_WORDS`; breadcrumbs corretti per Calendar e Inbox; atomicità in `safe_rename` contro collisioni case-only su APFS.
  - **Motivazione:** Previene sovrascritture di file critici di configurazione e garantisce la veridicità delle statistiche del Vault.
  - **Fase:** Phase 12 (Clean Code Refactoring & Audit Fixes)

- **Precisione Semantica, Word Boundaries & Ricerca Densa su Query Libere (Phase 12 - CLEAN-02):**
  - **Decisione:** Token matching con word boundaries (`\b`) nello scoring YAML; esclusione dei blocchi di codice fenced prima dell'estrazione di snippet e titoli in recall; fallback a similarità densa vettoriale via pseudo-relevance feedback per query discorsive.
  - **Motivazione:** Elimina falsi positivi su acronimi brevi (`ai` dentro `main`), evita di interpretare commenti `#` come intestazioni ed estende il retrieval vettoriale anche a domande a linguaggio naturale.
  - **Fase:** Phase 12 (Clean Code Refactoring & Audit Fixes)

- **Resilienza Ingestion, Autolinking Protetto & Clean Architecture (Phase 12 - CLEAN-03, CLEAN-04):**
  - **Decisione:** Controllo fisico `os.path.isfile` in `detect_input_type`; protezione anticipata di link markdown `[text](url)` e domini web in `autolink_content`; eccezione tipizzata `VideoMetadataError`; routing directory tabellare `DIRECTORY_ROUTING_RULES` (OCP/SRP); modello AI parametrizzabile `DEFAULT_AI_MODEL`; decomposizione di `_process_tri_state_approvals_unlocked` in 4 sub-handler; consolidamento DRY di `split_markdown_note` e `get_vault_root`.
  - **Motivazione:** Rende l'ingestion immune a link corrotti o input errati, modularizza il codice eliminando catene `if/elif` monolitiche e garantisce riuso senza duplicazioni.
  - **Fase:** Phase 12 (Clean Code Refactoring & Audit Fixes)

---

## 3. Phases Delivered

| Phase | Name | Status | Key Accomplishments & Deliverables |
|---|---|---|---|
| **07** | Sicurezza Credenziali & Configurazione Dinamica | Complete | Decommissioning e rimozione da Git di `99 - Meta/School/config.json`, `fetch-registro.py` e `List.md`; `.gitignore` rafforzato per file `config.json`; risoluzione dinamica di `agy` e `PATH` via `shutil.which` e `Path.home()`; parametrizzazione LaunchAgent macOS `com.loackypkm.watcher.plist` con token `__VAULT_PATH__` e comando CLI `watch.sh install-service`; 110/110 test green. |
| **08** | Integrità Ingestion & Salvaguardia Staging | Complete | Spostamento atomico preventivo in `03 - Inbox/Source/` per note con `ready: true`; gestione errori con retry `[x]` e dismissione `[-]`; tracciamento `old_title` post-AI ed eliminazione della condizione `clean_title != cand_ai`; purge frame YouTube in `99 - Meta/Clipboard/` su `video_id` (11 caratteri) e immagini markdown; supporto pipe alias (`[[Draft/Titolo\|Alias]]`); pulizia dead code e fallback AI per target directory; upgrade a `gemini-3.8-flash-low`; 120/120 test green. |
| **09** | Governance Vault & Integrità YAML Linter | Complete | Implementazione della modalità diagnostica non distruttiva `--lint-only` con `diagnose_yaml_violations` e mutua esclusione con `--auto-fix`; conservazione condizionale di `video_url` e `channel` per `type: video` con sync bidirezionale YouTube; unificazione della pipeline di normalizzazione stringhe in `normalize_title_or_filename` con simmetria Unicode NFC per vocali accentate; protezione da omonimie e collisioni in `VaultHealthAuditor.scan_vault`; 129/129 test green. |
| **10** | Retrieval, Concorrenza & Ottimizzazione Performance | Complete | Risoluzione dinamica del percorso PID watcher (`get_watcher_pid_file`) ed esportazione in `watch.sh`; Panic Abort con salvaguardia del demone watcher ed epurazione completa di lock e bozze parziali in `Draft/`; introduzione del mutex lock `DashboardLock` con TTL 60s per accessi atomici a `Review Dashboard.md`; compressione della cache `.recall_cache.json` a 728KB (eliminazione `tokens` a favore di `doc_len`/`term_freq`, `separators=(',', ':')`, esclusione `03 - Inbox` e flag `--reindex`); sanificazione headings H1-H3 senza emoji e rimozione sezioni `## Collegamenti` in `recall_engine.py` e `brain_health.py`; 139/139 test green. |
| **11** | Riallineamento Test Suite & Copertura CLI | Complete | Eliminazione delle asserzioni contraddittorie sui metadati video in `tests/test_lint_yaml.py`; mock PID dinamico su hash vault nei test del Panic Button in `tests/test_brain_ingest.py`; asserzioni di conformità Style Guide senza emoji e link organici in `tests/test_recall_engine.py`; copertura completa dei rami CLI di governance (`--lint-only`, `--dry-run`, `--auto-fix`, `--dashboard-only`, interactive EOF) in `tests/test_brain_health.py`; 151/151 test green. |
| **12** | Clean Code Refactoring & Audit Fixes | Complete | Implementazione di tutti i 13 punti del Clean Code Audit: protezione `IGNORE_FILES` root (`GEMINI.md`, `AGENTS.md`, `README.md`) in `--auto-fix`; ricalcolo metriche post-fix prima della generazione dashboard; deduplica `MINOR_WORDS`; breadcrumbs corretti Calendar/Inbox; atomicità `safe_rename` su filesystem APFS case-insensitive; token matching con word boundary (`\b`) nello scoring YAML; esclusione blocchi di codice fenced in recall; fallback semantico denso su query libere; gestione `VideoMetadataError` in `youtube_helper.py`; nome vault dinamico in `watch.sh`; gestione percorsi inesistenti in `detect_input_type`; protezione link markdown e domini in `autolink_content`; disaccoppiamento OCP/SRP con `DIRECTORY_ROUTING_RULES`; modello AI parametrizzabile `DEFAULT_AI_MODEL`; decomposizione `_handle_*` per approvazioni; consolidamento DRY di `split_markdown_note` e `get_vault_root`; 163/163 test green. |

---

## 4. Requirements Coverage

Tutti i 23 requisiti specificati per la milestone v1.0.1-alpha sono stati completati, convalidati e certificati nel Milestone Audit Report (`v1.0.1-alpha-MILESTONE-AUDIT.md`):

| Req ID | Category | Status | Verification Evidence |
|---|---|---|---|
| **SEC-01** | Security & Config | ✅ Met | Decommissioning `config.json` da Git (`git rm --cached`), inserimento in `.gitignore` e pulizia riferimenti obsoleti. |
| **SEC-02** | Security & Config | ✅ Met | Rimozione completa di `fetch-registro.py` ed epurazione credenziali in chiaro e API key scolastica. |
| **SEC-03** | Security & Config | ✅ Met | Risoluzione dinamica `shutil.which("agy")` e `Path.home()`, parametrizzazione LaunchAgent con `__VAULT_PATH__` e `watch.sh install-service`. |
| **INGEST-01** | Ingestion & Staging | ✅ Met | Spostamento preventivo atomico in `03 - Inbox/Source/` e rimozione della cancellazione anticipata di note grezze su eccezione. |
| **INGEST-02** | Ingestion & Staging | ✅ Met | Tracciamento di `old_title` post-AI, rimozione di `Draft/{old_title}.md` e rename di `Source/{old_title}.md`, eliminazione condizione `clean_title != cand_ai`. |
| **INGEST-03** | Ingestion & Staging | ✅ Met | Purge frame YouTube in `Clipboard/` tramite matching sul `video_id` (11 caratteri) e pulizia immagini incorporate nel markdown al rifiuto `[-]`. |
| **INGEST-04** | Ingestion & Staging | ✅ Met | Supporto trasparente caratteri pipe `|` negli alias wiki-link della dashboard, eliminazione dead code (doppio return) e fallback AI per target directory. |
| **HLTH-01** | Health & YAML | ✅ Met | Flag CLI `--lint-only` attivo in `brain_health.py` per audit diagnostico non distruttivo e mutua esclusione verificata con `--auto-fix`. |
| **HLTH-02** | Health & YAML | ✅ Met | Conservazione condizionale di `video_url` e `channel` per `type: video` in `infer_metadata` e sync bidirezionale con `source`. |
| **HLTH-03** | Health & YAML | ✅ Met | Normalizzazione unificata in `normalize_title_or_filename` con simmetria Unicode NFC per caratteri accentati italiani tra filename e title. |
| **HLTH-04** | Health & YAML | ✅ Met | Gestione omonimie accidentali in `VaultHealthAuditor.scan_vault` senza sovrascrittura di nodi o azzeramento link, con tracciamento in `duplicate_notes`. |
| **PERF-01** | Retrieval & Concurrency | ✅ Met | Sincronizzazione dinamica PID tra `watch.sh` e `brain_ingest.py` per Panic Button, salvaguardia del demone ed epurazione totale delle bozze interrotte. |
| **PERF-02** | Retrieval & Concurrency | ✅ Met | Mutex `DashboardLock` dedicato su `/tmp/brain_dashboard_{vault_hash}.lock` per accessi concorrenti atomici su `Review Dashboard.md`. |
| **PERF-03** | Retrieval & Concurrency | ✅ Met | Compressione `.recall_cache.json` a 728KB (<2.5MB), rimozione lista `tokens` per `doc_len`/`term_freq`, esclusione `03 - Inbox` e flag `--reindex`. |
| **PERF-04** | Retrieval & Concurrency | ✅ Met | Eliminazione completa delle emoji nelle intestazioni H1-H3 e rimozione delle sezioni finali `## Collegamenti` in `recall_engine.py` e `brain_health.py`. |
| **TEST-01** | Test Realignment | ✅ Met | Risoluzione asserzioni contraddittorie in `tests/test_lint_yaml.py` e verifica coerenza metadati video tra `lint_file` e serializzazione canonica. |
| **TEST-02** | Test Realignment | ✅ Met | Correzione mock PID watcher basato sull'hash del vault in `tests/test_brain_ingest.py` per Panic Button. |
| **TEST-03** | Test Realignment | ✅ Met | Asserzioni aggiornate in `tests/test_recall_engine.py` per validare l'assenza di emoji nei titoli e l'assorbimento organico dei link nella prosa. |
| **TEST-04** | Test Realignment | ✅ Met | Copertura dei rami di esecuzione CLI in `tests/test_brain_health.py` (`--lint-only`, `--dry-run`, `--auto-fix`, `--dashboard-only`, interactive EOF). |
| **CLEAN-01** | Clean Code & Audit | ✅ Met | Salvaguardia `IGNORE_FILES` (`GEMINI.md`, `AGENTS.md`, `README.md`), ricalcolo metriche post-fix, deduplica `MINOR_WORDS`, fix breadcrumbs Calendar/Inbox e atomicità APFS `safe_rename`. |
| **CLEAN-02** | Clean Code & Audit | ✅ Met | Fallback semantico denso su query libere via pseudo-relevance feedback, word boundaries (`\b`) nello scoring YAML ed esclusione blocchi di codice fenced in recall. |
| **CLEAN-03** | Clean Code & Audit | ✅ Met | `detect_input_type` con verifica fisica `os.path.isfile`, autolink protetto per link markdown e domini web, eccezione `VideoMetadataError`, nome vault dinamico in `watch.sh`. |
| **CLEAN-04** | Clean Code & Audit | ✅ Met | Routing dichiarativo `DIRECTORY_ROUTING_RULES`, modello AI configurabile con `DEFAULT_AI_MODEL` e env var, decomposizione `_handle_*` approvazioni, consolidamento DRY `split_markdown_note`/`get_vault_root`. |

**Audit Verdict:** **PASSED (23/23 Requirements Satisfied, 0 Gaps, 0 Orphaned, 163/163 Tests Green)**.

---

## 5. Key Decisions Log

Registro cronologico delle decisioni prese nel corso di v1.0.1-alpha:

| ID | Fase | Decisione | Motivazione & Impatto |
|---|---|---|---|
| **D-01 (P7)** | Phase 07 | Decommissioning completo modulo School (`config.json`, `fetch-registro.py`, `List.md`) | Elimina alla radice il rischio di credential leak per integrazione dismessa. |
| **D-02 (P7)** | Phase 07 | Preservazione attiva di `99 - Meta/School/Style Guide.md` | Mantiene intatta la guida di stile cromatica per le evidenziazioni HTML `<mark>`. |
| **D-04 (P7)** | Phase 07 | Risoluzione dinamica `shutil.which("agy")` e `Path.home()` in `brain_ingest.py` e `backfill_summaries.py` | Rende gli script portabili ed elimina i path assoluti legati all'utente locale. |
| **D-05 (P7)** | Phase 07 | Parametrizzazione LaunchAgent macOS con placeholder `__VAULT_PATH__` e `watch.sh install-service` | Consente l'installazione automatica del servizio demone in `~/Library/LaunchAgents/`. |
| **D-01 (P8)** | Phase 08 | Spostamento atomico preventivo delle note grezze in `03 - Inbox/Source/` | Protegge le note manoscritte dell'utente contro crash improvvisi o eccezioni AI. |
| **D-03 (P8)** | Phase 08 | Pulizia sincronizzata 1:1 delle bozze post-AI tramite memorizzazione di `old_title` | Elimina la condizione auto-annullante `clean_title != cand_ai` ed evita file orfani. |
| **D-04 (P8)** | Phase 08 | Purge selettivo dei frame YouTube in `Clipboard/` basato su `video_id` (11 caratteri) | Garantisce la pulizia completa dei file immagine al rifiuto `[-]` indipendentemente dal titolo. |
| **D-05 (P8)** | Phase 08 | Isolamento del nome effettivo prima della pipe `|` nei wiki-link della dashboard | Evita errori `FileNotFoundError` su note con alias di visualizzazione. |
| **D-06 (P8)** | Phase 08 | Eliminazione codice morto e fallback AI mirato per la target directory in `classify_target_directory` | Rimuove doppio return e classifica intelligentemente con `gemini-3.8-flash-low`. |
| **D-07 (P8)** | Phase 08 | Upgrade globale del modello di inferenza a `gemini-3.8-flash-low` | Adotta il modello più recente e prestante per tutte le pipeline di elaborazione. |
| **D-01 (P9)** | Phase 09 | Modalità diagnostica read-only `--lint-only` con prospetto CLI ricco | Consente verifiche di conformità YAML sicure e non distruttive a terminale. |
| **D-02 (P9)** | Phase 09 | Rigetto difensivo dell'invocazione combinata `--lint-only` + `--auto-fix` | Protegge la semantica di sola lettura evitando mutazioni contrastanti. |
| **D-03 (P9)** | Phase 09 | Preservazione simmetrica dei caratteri accentati italiani in forma Unicode NFC | Elimina la rimozione dei diacritici e garantisce parità 1:1 tra filename e frontmatter `title`. |
| **D-06 (P9)** | Phase 09 | Tracciamento collisioni omonime in `duplicate_notes` senza sovrascrivere `all_notes` | Preserva la coerenza del grafo e segnala le anomalie di unicità nel dashboard. |
| **D-07 (P9)** | Phase 09 | Conservazione condizionale di `video_url` e `channel` per `type: video` e sync con `source` | Protegge i metadati multimediali specifici durante i cicli di normalizzazione. |
| **D-01 (P10)** | Phase 10 | Risoluzione dinamica del percorso PID watcher tramite hash vault (`/tmp/brain_watcher_{hash}.pid`) | Sincronizza `watch.sh` e `brain_ingest.py` per l'arresto d'emergenza affidabile. |
| **D-02 (P10)** | Phase 10 | Preservazione del demone watcher ed eliminazione totale bozze parziali su Panic Abort | Arresta i worker e ripulisce le bozze corrotte lasciando vigile il servizio di monitoraggio. |
| **D-05 (P10)** | Phase 10 | Mutex lock dedicato `DashboardLock` per `03 - Inbox/Review Dashboard.md` | Previene collisioni concorrenti e perdita di checkbox tra scanner e approvazioni. |
| **D-09 (P10)** | Phase 10 | Serializzazione compatta JSON `separators=(',', ':')` per `.recall_cache.json` | Riduce il peso su disco della cache del 96.7% (da 22MB a 728KB) azzerando l'I/O. |
| **D-10 (P10)** | Phase 10 | Eliminazione dell'array ridondante `tokens` a favore di `doc_len` e `term_freq` | Ottimizza memoria e disco mantenendo inalterato lo scoring Okapi BM25. |
| **D-12 (P10)** | Phase 10 | Esclusione della cartella `03 - Inbox` dal perimetro di indicizzazione di recall | Previene falsi positivi ed elimina rumore da bozze temporanee o note grezze. |
| **D-13 (P10)** | Phase 10 | Ristrutturazione di `recall_engine.py` in 2 sezioni senza emoji con assorbimento organico dei link | Allinea l'output alla Style Guide del Vault integrando le connessioni nella prosa. |
| **D-14 (P10)** | Phase 10 | Rimozione emoji da tutte le intestazioni H1-H3 nei report di `brain_health.py` | Standardizza tutti i report Markdown su layout pulito e sobrio. |
| **CLEAN-01** | Phase 12 | Salvaguardia `IGNORE_FILES` root, ricalcolo metriche post-fix, atomicità APFS `safe_rename` | Protegge i file di configurazione di sistema e risolve conflitti case-only su macOS. |
| **CLEAN-02** | Phase 12 | Word boundaries (`\b`) nello scoring YAML, esclusione codice fenced e fallback semantico denso | Elimina falsi positivi lessicali su acronimi ed estende la ricerca vettoriale alle query libere. |
| **CLEAN-03** | Phase 12 | Verifica `os.path.isfile` per tipo input, autolink protetto per URL/markdown, `VideoMetadataError` | Previene errori di parsing su file inesistenti e blocca la creazione di note video fittizie. |
| **CLEAN-04** | Phase 12 | Routing dichiarativo tabellare OCP/SRP, modello AI configurabile, decomposizione handler | Snellisce le funzioni monolitiche e consolida le funzioni duplicate DRY nel codebase. |

---

## 6. Tech Debt & Deferred Items

### Debito Tecnico Risolto in v1.0.1-alpha:
- **Vulnerabilità di Sicurezza:** Epurate definitivamente credenziali ClasseViva e API key hardcoded; rimossi file tracciati da Git; percorsi assoluti utente dinamizzati.
- **Data-Loss Hazards:** Eliminato il rischio di cancellazione prematura delle note grezze dell'Inbox grazie allo staging preventivo in `Source/`.
- **Ghost Drafts & Orphan Frames:** Risolti i bug di ridenominazione post-AI e implementato il purge dei frame YouTube mirato su `video_id`.
- **Race Conditions:** Serializzate le operazioni su `Review Dashboard.md` tramite `DashboardLock` con timeout e gestione non bloccante.
- **Cache Bloat:** Compressa la cache di retrieval vettoriale/BM25 da 22MB a 728KB, con pruning deterministico delle note rimosse.
- **Discrepanze Diacritiche e Conflitti APFS:** Standardizzata la normalizzazione Unicode NFC simmetrica tra filename e YAML title; gestita la ridenominazione case-only su filesystem macOS APFS.
- **Test Inconsistencies:** Risolte le asserzioni contraddittorie sui metadati video e mockati i test di rete YouTube; copertura estesa a 163 test green.
- **Codice Monolitico e Duplicazioni DRY:** Decomposte le funzioni monolitiche di approvazione e classificazione; centralizzate le utility duplicate `split_markdown_note` e `get_vault_root`.

### Elementi Differiti alle Future Versioni (Roadmap v2):
- **EXT-01 (v2):** Sincronizzazione automatica bidirezionale con Kindle / Readwise per highlight da ebook e articoli.
- **EXT-02 (v2):** Voice-to-text capture mobile con trascrizione Whisper automatica e staging in Inbox.
- **GRAPH-01 (v2):** Algoritmo di clustering concettuale basato sui vettori del Vault per suggerire la creazione proattiva di Sub-MOC.

---

## 7. Getting Started

Guida rapida operativa aggiornata con le nuove funzionalità di v1.0.1-alpha:

### 1. Gestione del Demone Watcher & Installazione Servizio macOS:
```bash
# Avvia il watcher in background
./"99 - Meta/Scripts/watch.sh" start

# Verifica lo stato e il PID sincronizzato con hash vault
./"99 - Meta/Scripts/watch.sh" status

# Arresta il demone
./"99 - Meta/Scripts/watch.sh" stop

# Riavvia il demone
./"99 - Meta/Scripts/watch.sh" restart

# Installa il demone permanente come LaunchAgent utente macOS
./"99 - Meta/Scripts/watch.sh" install-service
```

### 2. Ingestione Universale & Gestione Staging (`brain-ingest`):
```bash
# Ingestione standard (approfondimento) con modello gemini-3.8-flash-low
python3 "99 - Meta/Scripts/brain_ingest.py" "https://www.youtube.com/watch?v=..."

# Ingestione sintetica compatta
python3 "99 - Meta/Scripts/brain_ingest.py" "https://..." --depth sintesi

# Elaborazione approvazioni interattive dalla Review Dashboard (con mutex DashboardLock)
python3 "99 - Meta/Scripts/brain_ingest.py" --process-approvals

# Arresto di emergenza / Panic Button via CLI
python3 "99 - Meta/Scripts/brain_ingest.py" --panic
```

### 3. Consultazione e Retrieval Ibrido (`brain-recall`):
```bash
# Ricerca ibrida (BM25 + Vettori + YAML con fallback semantico denso)
python3 "99 - Meta/Scripts/recall_engine.py" "Come funziona l'algoritmo di attenzione nei Transformer?"

# Ricerca strutturata con filtri controllati
python3 "99 - Meta/Scripts/recall_engine.py" "Reti Neurali" --area tech --type concept

# Formato Markdown conforme alla Style Guide (2 sezioni pulite, 0 emoji, link organici)
python3 "99 - Meta/Scripts/recall_engine.py" "Gestione della memoria" --format markdown

# Ricostruzione forzata della cache compressa (<750KB)
python3 "99 - Meta/Scripts/recall_engine.py" --reindex
```

### 4. Governance, Linting & Salute del Vault (`brain-health`):
```bash
# Ispezione diagnostica in SOLA LETTURA (nessuna modifica su disco)
python3 "99 - Meta/Scripts/brain_health.py" --lint-only

# Anteprima delle modifiche e ridenominazioni Title Case
python3 "99 - Meta/Scripts/brain_health.py" --dry-run

# Applicazione correzioni automatiche (normalizzazione YAML, Title Case, breadcrumbs, IGNORE_FILES protetti)
python3 "99 - Meta/Scripts/brain_health.py" --auto-fix

# Rigenerazione rapida della dashboard statica Markdown
python3 "99 - Meta/Scripts/brain_health.py" --dashboard-only
```

### 5. Esecuzione Suite di Test:
```bash
# Esecuzione completa dei 163 unit e integration tests
python3 -m unittest discover tests -v
```

### 6. Mappa delle Risorse di Riferimento:
- [GEMINI.md](file:///Users/lorenzo/Documents/GitHub/loackyPKM/GEMINI.md) — Memoria di sistema e convenzioni permanenti del Vault.
- [AGENTS.md](file:///Users/lorenzo/Documents/GitHub/loackyPKM/AGENTS.md) — Architettura del Second Brain e runtime conventions.
- [Review Dashboard.md](file:///Users/lorenzo/Documents/GitHub/loackyPKM/03%20-%20Inbox/Review%20Dashboard.md) — Interfaccia GTD di revisione e approvazione note.
- [Vault Health Dashboard.md](file:///Users/lorenzo/Documents/GitHub/loackyPKM/99%20-%20Meta/Vault%20Health%20Dashboard.md) — Report diagnostico statico del Vault.
- [Style Guide.md](file:///Users/lorenzo/Documents/GitHub/loackyPKM/99%20-%20Meta/School/Style%20Guide.md) — Guida di stile per evidenziazioni cromatiche `<mark>`, diagrammi Mermaid e formule LaTeX.

---

## Stats

- **Timeline:** 2026-09-01 → 2026-09-05 (4 giorni di sviluppo attivo)
- **Phases:** 6 / 6 Completate (Phases 07-12, 12 piani eseguiti al 100%)
- **Tasks Executed:** 29 task implementativi e di collaudo
- **Commits:** 38 commit
- **Files changed:** 77 file (+10,509 / -6,812)
- **Automated Tests:** 163 unit/integration tests (100% green pass rate)
- **Cache Footprint:** Ridotta da 22MB a 728KB (-96.7%)
- **Contributors:** Loacky <lorenzoadacher@gmail.com>
