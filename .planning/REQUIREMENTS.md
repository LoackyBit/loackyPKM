# Requirements: AI Second Brain — Obsidian PKM & Digital Garden

**Defined:** 2026-09-15  
**Milestone:** v1.1.0-alpha Academic Engine & Metacognitive Deep Ingestion  
**Core Value:** Rendere l'acquisizione, la manutenzione e l'interrogazione della conoscenza personale fluidi, immediati e a zero attrito, eliminando la frammentazione degli strumenti con fondamenta strutturali solide, standardizzazione AST dei metadati e governance a puro Markdown statico.

## v1 Requirements

Requisiti pianificati per la Milestone v1.1.0-alpha, ordinati secondo la sequenza architetturale approvata.

### Course Hub & Static PACRAR Matrix (PACRAR)

- [x] **PACRAR-01**: L'utente può generare o aggiornare automaticamente l'hub di corso `01 - Map of Content/<NomeCorso> MOC.md` con frontmatter canonico a 10 campi (`type: moc`, `area: education`, `related: [...]`).
- [x] **PACRAR-02**: L'utente visualizza nella MOC di corso la Matrice di Avanzamento PACRAR in tabella Markdown statica con le colonne: *Lezione / Argomento*, *Preparazione `[ ]`*, *Acquisizione `[ ]`*, *Comprensione `[ ]`*, *Rielaborazione `[ ]`*, *Applicazione `[ ]`*, *Ricordo `[ ]`*, *Nota Vault `[[...]]`*.
- [x] **PACRAR-03**: Il sistema preserva immutato lo stato delle checkbox manuali (`[x]`/`[ ]`) per ciascuna riga di lezione esistente durante successivi aggiornamenti dell'hub o ingestione di nuovi argomenti.

### NotebookLM CLI Integration (NLM)

- [x] **NLM-01**: L'agente AI interroga tramite subprocess la CLI `nlm query notebook` per il notebook di Alessandro de Concini (`b7534dad-1515-44c1-bcc5-c77992b5e416`) in formato JSON con timeout vincolato a 120s.
- [x] **NLM-02**: Il sistema intercetta tempestivamente errori di rete, timeout o token scaduti (`Authentication expired`) ed esegue un fallback automatico trasparente sulle euristiche metodologiche ADC incorporate, emettendo un avviso diagnostico senza bloccare l'ingestione.

### Metacognitive Synergy Engine (SYN)

- [x] **SYN-01**: L'AI estrae e converte le direttive metodologiche restituite da NotebookLM in vincoli attivi di schematizzazione e densità concettuale per la stesura in modalità `--depth approfondimento`.
- [x] **SYN-02**: L'AI calibra la generazione delle flashcard Anki sui principi di de Concini (principio di atomicità, non ambiguità semantica, comprensione causale preliminare anziché nozionismo mnemonico).

### ADC Didactic Taxonomy & STEM Formularies (TAX)

- [x] **TAX-01**: L'AI struttura organicamente la nota permanente secondo la sequenza logico-temporale della lezione universitaria, eliminando sezioni generiche fisse e senza emoji nei titoli H1-H3.
- [x] **TAX-02**: L'AI formatta ogni formula matematica o ingegneristica rilevante in blocchi LaTeX dedicati, esplicitando obbligatoriamente ipotesi, condizioni di validità, significato dei simboli ed esempi d'uso.
- [x] **TAX-03**: L'AI arricchisce la trattazione con diagrammi causali a cascata Mermaid (con nodi quotati `id["..."]`), tabelle comparative concettuali ed evidenziazioni organiche Style Guide (`<mark>`).

### PDF Slide Ingestion & Academic Helper (PDF)

- [x] **PDF-01**: Il sistema supporta l'opzione CLI `brain_ingest.py --course "<NomeCorso>"` ed invoca il modulo dedicato `99 - Meta/Scripts/academic_helper.py`.
- [x] **PDF-02**: Il modulo `academic_helper.py` estrae il testo strutturato da file PDF (slide universitarie) tramite `pypdf`, eseguendo il backup preventivo del file in `03 - Inbox/Source/`.
- [x] **PDF-03**: Il modulo estrae selettivamente figure e diagrammi significativi (filtrando per dimensione >150px e peso >10KB), deduplica gli asset ripetuti tramite hash SHA-256 e li salva in `99 - Meta/Clipboard/<NomeCorso>/`.

### Contextual Anki Flashcard Generation (ANKI)

- [x] **ANKI-01**: L'AI genera flashcard contestuali atomiche di tipo `Basic` e `Cloze`, posizionate immediatamente a valle della trattazione del rispettivo concetto cardine.
- [x] **ANKI-02**: Le flashcard sono formattate con sintassi nativa `obsidian-to-anki-plugin` tramite callout `>[!tip]` e tag di destinazione `%% TARGET DECK: University::<NomeCorso> %%`.
- [x] **ANKI-03**: Il sistema preserva rigorosamente immutati tutti i commenti identificativi esistenti (`<!--ID: \d+-->`) durante qualsiasi operazione di rielaborazione o linting, prevenendo la duplicazione di carte in Anki.

---

## v2 Requirements

Funzionalità pianificate per future milestone (v1.x.0-alpha e v1.0.0):

### Automation & Batch Pipeline (YT)

- **YT-01**: Importazione batch e sincronizzazione automatica di intere playlist di corsi YouTube tramite `youtube_helper.py`.

### Privacy & Hybrid Local AI (PRIV)

- **PRIV-01**: Cartella protetta con barriera rigida per AI cloud ed elaborazione delegata in esclusiva a LLM locali on-device.

### Mobile Experience (MOB)

- **MOB-01**: Quick Capture e consultazione fluida ottimizzati per l'applicazione Obsidian Mobile.

### Open Source Platform (OS)

- **OS-01**: Setup Wizard interattivo da CLI per la configurazione modulare di nuovi vault e corsi.
- **OS-02**: Style Mimicking per profilare lo stile dell'utente da note reali.
- **OS-03**: Generalizzazione open source disaccoppiata e documentazione `CONTRIBUTING.md`.

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| Plugin runtime Dataview (`dataview`, `dataviewjs`) | Rigorosamente vietato da `GEMINI.md` e `AGENTS.md`: compromette la portabilità su Quartz blog statico e introduce lock-in. |
| Emoji nei titoli dei file e nei tag H1-H3 | Vietato dalle convenzioni del vault per garantire URL puliti ed estetica editoriale coerente. |
| OCR pesante su GPU per slide (Tesseract) | Overhead non necessario: le slide universitarie sono PDF digitali già dotati di layer testuale leggibile con `pypdf`. |
| Sincronizzazione automatica cloud AnkiWeb diretta via API | Complessità e fragilità crittografica; il flusso consolidato dell'utente utilizza `obsidian-to-anki-plugin` locale. |
| Sezioni finali isolate `## Collegamenti` o `## Note Correlate` | Vietate dalla Style Guide: tutti i wiki-link sono integrati organicamente nella prosa e sincronizzati in `related: [...]`. |

---

## Traceability

Mappatura dei requisiti di v1.1.0-alpha sulle fasi della roadmap (popolata durante la creazione della roadmap).

| Requirement | Phase | Status |
|-------------|-------|--------|
| PACRAR-01 | Phase 13 | Complete |
| PACRAR-02 | Phase 13 | Complete |
| PACRAR-03 | Phase 13 | Complete |
| NLM-01 | Phase 14 | Complete |
| NLM-02 | Phase 14 | Complete |
| SYN-01 | Phase 14 | Complete |
| SYN-02 | Phase 14 | Complete |
| TAX-01 | Phase 15 | Complete |
| TAX-02 | Phase 15 | Complete |
| TAX-03 | Phase 15 | Complete |
| PDF-01 | Phase 16 | Complete |
| PDF-02 | Phase 16 | Complete |
| PDF-03 | Phase 16 | Complete |
| ANKI-01 | Phase 17 | Complete |
| ANKI-02 | Phase 17 | Complete |
| ANKI-03 | Phase 17 | Complete |

**Coverage:**

- v1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-15*  
*Last updated: 2026-09-20 after Phase 17 completion*
