# Roadmap: AI Second Brain & Digital Garden

## Milestones

- ✅ **v1.0.0-alpha AI Second Brain MVP** — Phases 1-06.2 (shipped 2026-09-01)
- ✅ **v1.0.1-alpha Code Review & Bug Fixing** — Phases 7-12 (shipped 2026-09-05)
- 🚧 **v1.1.0-alpha Academic Engine & Metacognitive Deep Ingestion** — Phases 13-17 (in progress)
- 📅 **v1.x.0-alpha Automation, Privacy & Cross-Device UX** — Future Milestone
- 🎯 **v1.0.0 Open Source Second Brain Platform** — Major Release Target

## Phases

<details>
<summary>✅ v1.0.0-alpha AI Second Brain MVP (Phases 1-06.2) — SHIPPED 2026-09-01</summary>

- [x] Phase 1: Fondamenta & Riorganizzazione Strutturale (2/2 plans) — completed 2026-08-24
- [x] Phase 2: Standardizzazione YAML & Frontmatter Funzionale (2/2 plans) — completed 2026-08-24
- [x] Phase 3: Consolidamento Flussi AI & Riduzione Frammentazione (2/2 plans) — completed 2026-08-25
- [x] Phase 4: Esperienza NotebookLM & Retrieval Conversazionale (2/2 plans) — completed 2026-08-25
- [x] Phase 5: Pipeline Ingestion Background & Multimedia Watcher (2/2 plans) — completed 2026-08-25
- [x] Phase 6: Verifica Generale & Collaudo Milestone (2/2 plans) — completed 2026-08-25
- [x] Phase 06.1: Riprogettare da Zero brain-ingest (2/2 plans) — completed 2026-08-29
- [x] Phase 06.2: Ristrutturazione sezioni note e fasi di rielaborazione brain-ingest (2/2 plans) — completed 2026-08-29

</details>

<details>
<summary>✅ v1.0.1-alpha Code Review & Bug Fixing (Phases 7-12) — SHIPPED 2026-09-05</summary>

- [x] Phase 7: Sicurezza Credenziali & Configurazione Dinamica (2/2 plans) — completed 2026-09-03
- [x] Phase 8: Integrità Ingestion & Salvaguardia Staging (2/2 plans) — completed 2026-09-03
- [x] Phase 9: Governance Vault & Integrità YAML Linter (2/2 plans) — completed 2026-09-03
- [x] Phase 10: Retrieval, Concorrenza & Ottimizzazione Performance (2/2 plans) — completed 2026-09-03
- [x] Phase 11: Riallineamento Test Suite & Copertura CLI (2/2 plans) — completed 2026-09-04
- [x] Phase 12: Clean Code Refactoring & Audit Fixes (2/2 plans) — completed 2026-09-05

</details>

<details open>
<summary>🚧 v1.1.0-alpha Academic Engine & Metacognitive Deep Ingestion (Phases 13-17) — IN PROGRESS</summary>

- [x] **Phase 13: Course Hub & Matrice PACRAR Statica** — MOC di corso e matrice di studio PACRAR a spunta manuale in puro Markdown statico (completed 2026-09-16)
- [x] **Phase 14: NotebookLM CLI Integration & Sinergia Metacognitiva** — Interrogazione CLI de Concini con timeout/fallback e guida alla schematizzazione (completed 2026-09-17)
- [x] **Phase 15: Tassonomia Didattica ADC & Formulari STEM Vincolati** — Sequenza cronologica lezione, formulari con ipotesi esplicite e diagrammi Mermaid quotati (completed 2026-09-17)
- [ ] **Phase 16: Academic Helper & Pipeline Ingestione Slide PDF** — Modulo `academic_helper.py`, estrazione testo/figure con deduplica e flag `--course`
- [x] **Phase 17: Generazione Flashcard Anki Contestuali & Preservazione ID** — Card `Basic`/`Cloze` in callout `>[!tip]`, target deck e tutela assoluta ID Anki (completed 2026-09-20)

</details>

<details>
<summary>📅 v1.x.0-alpha Automation, Privacy & Cross-Device UX — UPCOMING</summary>

- [ ] Automazione Ingestione Playlist YouTube (YT-01)
- [ ] Cartella Privacy & Architettura AI Ibrida Cloud/Locale (PRIV-01)
- [ ] Flusso Quick Capture & Recall Semplificato per Obsidian Mobile (MOB-01)

</details>

<details>
<summary>🎯 v1.0.0 Open Source Second Brain Platform — MAJOR TARGET</summary>

- [ ] Setup Wizard Interattivo per Onboarding e Scopo d'Uso (OS-01)
- [ ] Cloner dello Stile di Scrittura AI da Note Reali Utente (OS-02)
- [ ] Framework Universale Open Source & Community Extensibility (OS-03)

</details>

---

## Phase Details

### Phase 13: Course Hub & Matrice PACRAR Statica

**Goal**: Strutturare l'hub del corso (`01 - Map of Content/<NomeCorso> MOC.md`) con frontmatter canonico e matrice di avanzamento dello studio PACRAR a 6 fasi in puro Markdown statico, con tracciamento manuale e salvaguardia delle spunte.
**Depends on**: Phase 12
**Requirements**: PACRAR-01, PACRAR-02, PACRAR-03
**Success Criteria** (what must be TRUE):

1. L'utente può generare o aggiornare `01 - Map of Content/<NomeCorso> MOC.md` con frontmatter canonico a 10 campi (`type: moc`, `area: education`).
2. La MOC contiene la tabella Markdown statica Matrice PACRAR con colonne: *Lezione / Argomento*, *Preparazione `[ ]`*, *Acquisizione `[ ]`*, *Comprensione `[ ]`*, *Rielaborazione `[ ]`*, *Applicazione `[ ]`*, *Ricordo `[ ]`*, *Nota Vault `[[...]]`*.
3. L'aggiornamento dell'hub di corso o l'aggiunta di nuove lezioni preserva immutato lo stato delle checkbox manuali (`[x]`/`[ ]`) già registrate.

**Plans**: 2 plans

Plans:

- [x] 13-01: Generatore MOC di corso e template statico PACRAR con validazione frontmatter canonico
- [x] 13-02: Logica di parsing e aggiornamento incrementale non distruttivo della tabella PACRAR con test unitari

---

### Phase 14: NotebookLM CLI Integration & Sinergia Metacognitiva

**Goal**: Integrare la CLI `nlm` per consultare programmaticamente il notebook di Alessandro de Concini in modalità `--depth approfondimento`, implementando timeout, cattura JSON, fallback graceful in caso di auth expired o errore di rete, e conversione delle direttive in vincoli metacognitivi.
**Depends on**: Phase 13
**Requirements**: NLM-01, NLM-02, SYN-01, SYN-02
**Success Criteria** (what must be TRUE):

1. L'agente esegue la query subprocess a `nlm query notebook b7534dad-1515-44c1-bcc5-c77992b5e416` catturando la risposta JSON entro il timeout di 120s.
2. In caso di errore CLI (`Authentication expired`, assenza di rete o timeout), il sistema attiva un fallback automatico su euristiche incorporate emettendo un avviso chiaro senza interrompere l'ingestione.
3. Le direttive metodologiche estratte vengono tradotte in vincoli attivi di schematizzazione e principi guida per l'active recall.

**Plans**: 2/2 plans executed

Plans:

- [x] 14-01-PLAN.md
- [x] 14-02-PLAN.md

**Wave 1**

- [x] 14-01: Client wrapper subprocess per `nlm query notebook` con timeout, gestione JSON, e rilevamento auth failure/graceful fallback

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 14-02: Motore di sinergia metacognitiva: parsing delle direttive NLM ed integrazione nel prompt AI per `--depth approfondimento`

---

### Phase 15: Tassonomia Didattica ADC & Formulari STEM Vincolati

**Goal**: Applicare sistematicamente la tassonomia ADC alle note di lezione: rispetto della sequenza cronologica della lezione, formulari operativi vincolati in LaTeX con ipotesi e condizioni di validità esplicite, schemi causali a cascata Mermaid e tabelle comparative senza template rigidi.
**Depends on**: Phase 14
**Requirements**: TAX-01, TAX-02, TAX-03
**Success Criteria** (what must be TRUE):

1. La nota permanente segue l'ordine logico-temporale della lezione universitaria, senza sezioni fisse vuote e senza emoji nei titoli H1-H3.
2. Tutte le formule matematiche o ingegneristiche in LaTeX esplicitano obbligatoriamente ipotesi, condizioni di validità e significato dei simboli.
3. La trattazione include diagrammi causali Mermaid quotati `id["..."]`, tabelle comparative ed evidenziazioni Style Guide `<mark>` organiche.

**Plans**: 2 plans

Plans:
**Wave 1**

- [x] 15-01-PLAN.md — Regole di arricchimento didattico ADC per formule STEM vincolate (LaTeX, ipotesi, condizioni di validità) e diagrammi Mermaid quotati

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 15-02-PLAN.md — Validatore e test di conformità per note accademiche (zero emoji, titoli puliti, Style Guide highlights, link organici)

---

### Phase 16: Academic Helper & Pipeline Ingestione Slide PDF

**Goal**: Implementare `99 - Meta/Scripts/academic_helper.py` e il flag `brain_ingest.py --course "<NomeCorso>"`, estraendo testo strutturato da slide universitarie con `pypdf`, isolando e deduplicando figure e diagrammi in `99 - Meta/Clipboard/<NomeCorso>/` con backup preventivo in `Source/`.
**Depends on**: Phase 15
**Requirements**: PDF-01, PDF-02, PDF-03
**Success Criteria** (what must be TRUE):

1. Il flag `--course "<NomeCorso>"` in `brain_ingest.py` attiva il routing accademico instradando le slide PDF verso `academic_helper.py`.
2. Il modulo estrae il testo completo delle slide con `pypdf` e garantisce il backup preventivo del PDF in `03 - Inbox/Source/`.
3. Le immagini e i grafici delle slide vengono filtrati per dimensione (>150px, >10KB), deduplicati tramite hash SHA-256 e salvati in `99 - Meta/Clipboard/<NomeCorso>/`.

**Plans**: 2/2 plans complete

Plans:

- [x] 16-01-PLAN.md
- [x] 16-02-PLAN.md

**Wave 1**

- [x] 16-01: Modulo `academic_helper.py` con estrattore PDF, filtraggio selettivo delle immagini e deduplica SHA-256 in `Clipboard/<NomeCorso>/`

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 16-02: Integrazione in `brain_ingest.py` del flag `--course`, lifecycle a 3 fasi e staging con Review Dashboard

---

### Phase 17: Generazione Flashcard Anki Contestuali & Preservazione ID

**Goal**: Generare automaticamente flashcard Anki atomiche (`Basic` e `Cloze`) contestuali ai concetti chiave con callout `>[!tip]` e tag deck `%% TARGET DECK: University::<NomeCorso> %%`, garantendo la preservazione assoluta dei commenti ID `<!--ID: \d+-->`.
**Depends on**: Phase 16
**Requirements**: ANKI-01, ANKI-02, ANKI-03
**Success Criteria** (what must be TRUE):

1. Flashcard atomiche `Basic` e `Cloze` posizionate immediatamente dopo i concetti cardine, formulate secondo i principi di active recall ADC.
2. Blocco callout `>[!tip]` formattato secondo la sintassi di `obsidian-to-anki-plugin` con mazzo target `%% TARGET DECK: University::<NomeCorso> %%`.
3. Il 100% degli ID univoci preesistenti `<!--ID: \d+-->` viene preservato immutato durante riscritture della nota o scansioni di `brain_health.py`.

**Plans**: 2 plans

Plans:
**Wave 1**

- [x] 17-01: Generatore di flashcard contestuali `>[!tip]` (`Basic` e `Cloze`) con associazione al mazzo di materia

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 17-02: Parser di preservazione per commenti `<!--ID: \d+-->`, protezione in `brain_health.py` e test suite di sincronizzazione Anki

---

## Progress

**Execution Order:**
Phases execute in numeric order: 13 → 14 → 15 → 16 → 17

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Fondamenta & Riorganizzazione | v1.0.0-alpha | 2/2 | Complete | 2026-08-24 |
| 2. Standardizzazione YAML | v1.0.0-alpha | 2/2 | Complete | 2026-08-24 |
| 3. Consolidamento Flussi AI | v1.0.0-alpha | 2/2 | Complete | 2026-08-25 |
| 4. Esperienza NotebookLM | v1.0.0-alpha | 2/2 | Complete | 2026-08-25 |
| 5. Pipeline Ingestion Background | v1.0.0-alpha | 2/2 | Complete | 2026-08-25 |
| 6. Verifica Generale & Collaudo | v1.0.0-alpha | 2/2 | Complete | 2026-08-25 |
| 06.1. Riprogettare brain-ingest | v1.0.0-alpha | 2/2 | Complete | 2026-08-29 |
| 06.2. Ristrutturazione sezioni note | v1.0.0-alpha | 2/2 | Complete | 2026-08-29 |
| 7. Sicurezza & Config Dinamica | v1.0.1-alpha | 2/2 | Complete | 2026-09-03 |
| 8. Integrità Ingestion & Staging | v1.0.1-alpha | 2/2 | Complete | 2026-09-03 |
| 9. Governance & Integrità YAML | v1.0.1-alpha | 2/2 | Complete | 2026-09-03 |
| 10. Concorrenza & Performance | v1.0.1-alpha | 2/2 | Complete | 2026-09-03 |
| 11. Test Suite & Copertura CLI | v1.0.1-alpha | 2/2 | Complete | 2026-09-04 |
| 12. Clean Code & Audit Fixes | v1.0.1-alpha | 2/2 | Complete | 2026-09-05 |
| 13. Course Hub & Matrice PACRAR | v1.1.0-alpha | 2/2 | Complete    | 2026-09-16 |
| 14. NotebookLM & Sinergia Metacognitiva | v1.1.0-alpha | 2/2 | Complete    | 2026-09-17 |
| 15. Tassonomia ADC & Formulari STEM | v1.1.0-alpha | 2/2 | Complete    | 2026-09-17 |
| 16. Academic Helper & Slide PDF | v1.1.0-alpha | 2/2 | Complete   | 2026-09-17 |
| 17. Flashcard Anki & Preservazione ID | v1.1.0-alpha | 2/2 | Complete    | 2026-09-20 |

---
*Roadmap updated: 2026-09-15 after milestone v1.1.0-alpha definition (Phases 13-17)*
