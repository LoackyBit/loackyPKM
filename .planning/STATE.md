---
gsd_state_version: 1.0
milestone: v1.1.0-alpha
milestone_name: Academic Engine & Metacognitive Deep Ingestion
current_phase: 17
current_phase_name: Generazione Flashcard Anki Contestuali & Preservazione ID
status: complete
stopped_at: Completed Phase 17 — Milestone v1.1.0-alpha execution complete
last_updated: "2026-09-20T21:46:00.000Z"
last_activity: 2026-09-20
last_activity_desc: Completed Phase 17 Generazione Flashcard Anki Contestuali & Preservazione ID
state_head: 2cb22d9
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 10
  completed_plans: 10
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-15 with v1.1.0-alpha, v1.x.0-alpha, v1.0.0 roadmap)

**Core value:** Rendere l'acquisizione, la manutenzione e l'interrogazione della conoscenza personale fluidi, immediati e a zero attrito, eliminando la frammentazione degli strumenti con fondamenta strutturali solide, standardizzazione AST dei metadati e governance a puro Markdown statico.
**Current focus:** Phase 17 — Generazione Flashcard Anki Contestuali & Preservazione ID

## Current Position

Phase: 17 — Generazione Flashcard Anki Contestuali & Preservazione ID
Total Plans in Phase: 2
Completed Plans in Phase: 2
Status: Complete
Last activity: 2026-09-20 — Completed Phase 17 Generazione Flashcard Anki Contestuali & Preservazione ID

## Performance Metrics

**Velocity:**

- Total plans completed: 2
- Average duration: 15 min
- Total execution time: 2.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Fondamenta & Riorganizzazione | 2/2 | Complete | - |
| 2. Standardizzazione YAML | 2/2 | Complete | - |
| 3. Consolidamento Flussi AI | 2/2 | Complete | - |
| 4. Esperienza NotebookLM | 2/2 | Complete | - |
| 5. Pipeline Ingestion Background | 2/2 | Complete | - |
| 6. Verifica Generale & Collaudo Milestone | 2/2 | Complete | - |
| 06.1. Riprogettare da Zero brain-ingest | 2/2 | Complete | - |
| 06.2. Ristrutturazione sezioni note e fasi brain-ingest | 2/2 | Complete | - |
| 7. Sicurezza & Config Dinamica | 2/2 | Complete | 2026-09-03 |
| 8. Integrità Ingestion & Staging | 2/2 | Complete | 2026-09-03 |
| 9. Governance & Integrità YAML | 2/2 | Complete | 2026-09-03 |
| 10. Concorrenza & Performance | 2/2 | Complete | 2026-09-03 |
| 11. Test Suite & Copertura CLI | 2/2 | Complete | 2026-09-04 |
| 12. Clean Code & Audit Fixes | 2/2 | Complete | 2026-09-05 |
| 13. Course Hub & Matrice PACRAR | 2/2 | Complete | 2026-09-16 |
| 14. NotebookLM & Sinergia Metacognitiva | 2/2 | Complete | 2026-09-17 |
| 15. Tassonomia ADC & Formulari STEM | 2/2 | Complete | 2026-09-17 |
| 16. Academic Helper & Slide PDF | 2/2 | Complete | 2026-09-17 |
| 17. Flashcard Anki & Preservazione ID | 0/2 | Not started | - |
| 17 | 2 | - | - |

**Recent Trend:**

- Last 5 plans: Complete
- Trend: Stable

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table and `.agents/memory/corrections-log.md`.
Recent decisions affecting current work:

- [Phase 06.2]: Schema sezioni flessibile guidato al 100% dal contenuto dell'AI (D-01).
- [Phase 06.2]: Divieto assoluto di emoji nei titoli H1, H2, H3 (D-02).
- [Phase 06.2]: Assorbimento organico dei collegamenti nella prosa senza sezione finale `## Collegamenti` e con sync frontmatter `related: [...]` (D-03).
- [Phase 06.2]: Arricchimento visivo organico: `<mark>` (giallo #cc8800 / viola #9a54c1), Mermaid quotato `id["..."]`, LaTeX (D-04).
- [Phase 06.2]: Ciclo di vita a 3 macro-fasi snelle (`1/3 Estrazione Sorgente`, `2/3 Rielaborazione Concettuale AI`, `3/3 Autolinking & Staging`) (D-05).
- [Phase 06.2]: Filtro anti-sponsor e anti-slop aggressivo con estrazione principi primi (D-07).
- [Phase 06.2]: Modalità `--depth approfondimento` di default (con `--depth sintesi` opzionale) (D-10, D-11).
- [Phase 06.2]: Razionalizzazione a 2 soli template universali (`Nota Vault.md` e `Articolo Blog.md`) + `Raw Inbox Note.md` e purge di 9 template legacy e `Folder Templates/` (D-12).
- [Phase 06.2]: Sincronizzazione globale del set normativo (`Style Guide.md`, `GEMINI.md`, `AGENTS.md`, `SKILL.md`) (D-13).
- [Phase 13]: Natural Numeric Sort per lezioni e argomenti PACRAR (evita disallineamento `Lezione 10` prima di `Lezione 2`) (13-01).
- [Phase 13]: Algoritmo non-distruttivo Append & Preserve in `course_hub.py` (preserva al 100% spunte manuali `[ ]`, `[-]`, `[x]` e righe personalizzate di syllabus) (13-01, 13-02).
- [Phase 13]: Micro-plugin Obsidian CommonJS `pacrar-tracker` e CSS snippet per cicli tri-state al click e visual progress rings SVG (13-02).
- [Phase 13]: Integrazione flag `--course "<NomeCorso>"` e autolinking breadcrumbs accademici in `brain_ingest.py` e `brain_health.py` (13-01, 13-02).

### Roadmap Evolution

- Phase 6 added: Verifica Generale & Collaudo Milestone (completed 2026-08-25).
- Phase 06.1 inserted and completed: Riprogettazione da zero brain-ingest (completed 2026-08-29).
- Phase 06.2 inserted and completed: Ristrutturazione sezioni note e fasi di rielaborazione brain-ingest (completed 2026-08-29).
- Milestone v1.0.1-alpha initialized: 5 phases planned (Phases 7-11) addressing Clean Code Audit Report 2026-09-03.
- Phase 12 added: Clean Code Refactoring & Audit Fixes (implementazione dei consigli 1.5, 2.1, 2.2, 2.4, 2.5, 2.7, 3.1, 3.2, 3.3, 4.1, 4.3, 4.4, 5).
- Roadmap & Goals re-alignment (2026-09-15): Defined v1.1.0-alpha (NotebookLM CLI + Academic PACRAR Ingest), v1.x.0-alpha (Playlist YouTube, Privacy Folder, Mobile UX), and v1.0.0 (Open Source Setup Wizard, Style Mimicking, Framework Universale).

### Pending Todos

None.

### Blockers/Concerns

None.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260921-vbo | Standardizzazione e Validazione Formato Flashcard Anki Conforme a Doc Ufficiale | 2026-09-21 | 62d0bc3 | [260921-vbo-assicurati-che-le-prossime-flashcard-ris](./quick/260921-vbo-assicurati-che-le-prossime-flashcard-ris/) |
| 260923-uv9 | Integrazione direttive inline AI %% AI: ... %% | 2026-09-23 | 053d4a9 | [260923-uv9-integrazione-direttive-inline-ai-ai](./quick/260923-uv9-integrazione-direttive-inline-ai-ai/) |
| 260924-n6q | Implementazione Opzione B: Deep Ingestion e Link-Resolution per brain-ingest | 2026-09-24 | 23659a3 | [260924-n6q-implementazione-opzione-b-deep-ingestion](./quick/260924-n6q-implementazione-opzione-b-deep-ingestion/) |
| 260924-orz | Integrazione regole didattiche e visuali nel sistema Second Brain | 2026-09-24 | 123b699 | [260924-orz-non-salvare-in-memory-md-ma-integra-nel-](./quick/260924-orz-non-salvare-in-memory-md-ma-integra-nel-/) |
| 260924-qtr | Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/ | 2026-09-24 | a6784d9 | [260924-qtr-cleanup-audio-transcripts-inbox-source](./quick/260924-qtr-cleanup-audio-transcripts-inbox-source/) |

## Deferred Items

| Category | Item | Status | Deferred At | Milestone |
|----------|------|--------|-------------|-----------|
| *(none)* | | | | |

## Session Continuity

**Resume file:** .planning/phases/17-generazione-flashcard-anki-contestuali-preservazione-id/17-CONTEXT.md

Last activity: 2026-09-24 - Completed quick task 260924-qtr: Pulizia automatica trascrizioni audio orfane in 03 - Inbox/Source/
Last session: 2026-09-24T18:20:00+02:00
Stopped at: Quick task 260924-qtr complete, ready for next task

## Operator Next Steps

- Start the next milestone with /gsd-new-milestone
