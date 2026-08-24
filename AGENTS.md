---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Agents"
date: '2026-08-24'
updated: 2026-08-24T17:09
tags: []
summary: "AI Second Brain — Obsidian PKM & Digital Garden"
---

<!-- GSD:project-start source:PROJECT.md -->

## Project

**AI Second Brain — Obsidian PKM & Digital Garden**

Un Second Brain e Personal Knowledge Management (PKM) su base Obsidian, trasformato in un digital garden intelligente e integrato con Antigravity CLI per operare come un "NotebookLM locale". Permette di raccogliere note, appunti universitari, articoli e video YouTube, organizzarli con una tassonomia semantica aperta e interrogarli via chat per recuperare ricordi, sintesi e connessioni interdisciplinari con citazioni dirette alle fonti.

**Core Value:** Rendere l'acquisizione, la manutenzione e l'interrogazione della conoscenza personale fluidi, immediati e a zero attrito, eliminando la frammentazione degli strumenti con fondamenta strutturali solide e pulite.

### Constraints

- **Puro Markdown Statico**: Nessun plugin runtime bloccante (tutti i dashboard e report sono generati in Markdown statico).
- **Naming Title Case Intelligente**: Nomi file in Title Case con spazi, senza emoji e senza kebab-case.
- **Topografia ACE a 6 Cartelle**: Contenuto confinato in `01 - Map of Content`, `02 - Atlas`, `03 - Inbox`, `04 - Calendar`, `05 - Blog`, `99 - Meta`.
- **Scrittura Diretta su Disco**: Tutte le modifiche e le note proposte devono essere scritte fisicamente nel file system con strumenti di persistenza.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->

## Technology Stack

## Languages

- Markdown (CommonMark / Obsidian Flavour) - Entire knowledge base, MOCs, Atlas notes, Blog posts, Templates, and Agent Memory (`01 - Map of Content/`, `02 - Atlas/`, `03 - Inbox/`, `04 - Calendar/`, `05 - Blog/`, `99 - Meta/Template/`, `.agents/MEMORY.md`).
- Python (3.10 - 3.13) - Automation scripts, data fetchers, linting utilities, and agent memory consolidation (`99 - Meta/Scripts/`, `.agents/skills/*/scripts/`, `99 - Meta/School/fetch-registro.py`).
- Bash / Shell Scripting - Daemon watchers, title extractors, and discovery scripts (`99 - Meta/Scripts/watch.sh`, `.agents/skills/dream/scripts/discover.sh`, `.agents/skills/link/scripts/get_vault_titles.sh`).
- YAML - Metadata frontmatter headers across all vault notes and agent skills configurations.
- JSON / JSONL - App configuration (`99 - Meta/School/config.json`, `.obsidian/*.json`), vector embeddings (`.smart-env/`), and conversation transcripts (`transcript.jsonl`).

## Runtime

- Python 3.13 Runtime (`/opt/homebrew/bin/python3`, `/usr/bin/python3`)
- Node.js Runtime (for `gsd-tools.cjs`, Quartz blog generator, and Obsidian plugin tooling)
- Obsidian Desktop (Electron) & Obsidian iOS Mobile App (iCloud synchronized)
- Antigravity / Gemini CLI Runtime (`/Users/lorenzo/.local/bin/agy`, `antigravity-cli`)
- pip (Python package manager for script dependencies)
- Homebrew (`brew` for system utilities like `ffmpeg`, `git`, `python3`)
- Lockfile: None committed for Python scripts (scripts use standard library or widely available packages)

## Frameworks

- Obsidian (v1.x) - Graph-based Personal Knowledge Management (PKM) platform with local-first file storage and bi-directional linking.
- Quartz (v4.x) - Static Site Generator converting Obsidian Markdown into a fast web-accessible digital garden for `05 - Blog/`.
- Antigravity Agent Runtime - Autonomous multi-agent framework orchestrating GSD workflows, memory consolidation (`dream`), and note processing (`process-inbox`, `nota`).
- Python built-in `argparse` dry-run testing suites (`--dry-run` vs `--execute` in `99 - Meta/Scripts/tidy_vault.py` and `.agents/skills/meta/scripts/lint_yaml.py`).
- Static diagnostic testing via custom AST/regex linters (`.agents/skills/audit/scripts/audit_vault.py`).
- Git - Version control and file tracking integration (`.gitignore`, `obsidian-git` plugin).

## Key Dependencies

- `requests` (Python HTTP library) - Communicates with ClasseViva API in `99 - Meta/School/fetch-registro.py`.
- `youtube-transcript-api` (Python) - Extracts subtitles and transcripts in `99 - Meta/Scripts/youtube_helper.py`.
- `yt-dlp` (Python CLI / library) - Retrieves video metadata and media stream URLs in `99 - Meta/Scripts/youtube_helper.py`.
- `ffmpeg` (System binary) - Extracts keyframe screenshots from YouTube streams in `99 - Meta/Scripts/youtube_helper.py`.
- `extended-graph` (`.obsidian/plugins/extended-graph/`): Advanced graph visualization.
- `obsidian-latex-suite` (`.obsidian/plugins/obsidian-latex-suite/`): Math and LaTeX snippet acceleration.
- `markdown-prettifier` (`.obsidian/plugins/markdown-prettifier/`): Table and Markdown formatting.
- `flexplorer` (`.obsidian/plugins/flexplorer/`): Enhanced file explorer for vault hierarchy.
- `dragger` (`.obsidian/plugins/dragger/`): Block and element drag-and-drop.
- `custom-commands` (`.obsidian/plugins/custom-commands/`): Custom command chains.
- `obsidian-focus-mode` (`.obsidian/plugins/obsidian-focus-mode/`): Distraction-free writing interface.
- `automatic-linker` (`.obsidian/plugins/automatic-linker/`): Automated internal link generation.
- `obsidian-completr` (`.obsidian/plugins/obsidian-completr/`): Auto-completion for vocabulary and LaTeX.
- `obsidian-auto-link-title` (`.obsidian/plugins/obsidian-auto-link-title/`): URL page title fetching.
- `obsidian-icon-folder` (`.obsidian/plugins/obsidian-icon-folder/`): Folder icons in file explorer.
- `obisidian-note-linker` (`.obsidian/plugins/obisidian-note-linker/`): Automated cross-linking.
- `obsidian-outliner` (`.obsidian/plugins/obsidian-outliner/`): Outliner-style list handling.
- `settings-search` (`.obsidian/plugins/settings-search/`): Search filter within Obsidian settings.
- `obsidian-text-format` (`.obsidian/plugins/obsidian-text-format/`): Text transformations and casing.
- `templater-obsidian` (`.obsidian/plugins/templater-obsidian/`): Dynamic note templating engine.
- `manual-sorting` (`.obsidian/plugins/manual-sorting/`): Custom note and folder ordering.
- `pseudo-mica` (`.obsidian/plugins/pseudo-mica/`): Visual theme enhancement.
- `terminal` (`.obsidian/plugins/terminal/`): Embedded terminal emulator inside Obsidian.
- `obsidian-style-settings` (`.obsidian/plugins/obsidian-style-settings/`): Custom CSS variable controls.
- `obsidian-git` (`.obsidian/plugins/obsidian-git/`): Automated git backup, commit, and push.
- `editing-toolbar` (`.obsidian/plugins/editing-toolbar/`): Visual MS-Word style editing toolbar.
- `autosave-control` (`.obsidian/plugins/autosave-control/`): Configurable autosave intervals.
- `in-progress-checkbox` (`.obsidian/plugins/in-progress-checkbox/`): Tri-state markdown checkboxes (`[ ]`, `[-]`, `[x]`).

## Configuration

- PATH requirements: `/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin` (configured in `99 - Meta/Scripts/watch.sh` and `99 - Meta/Scripts/ingest_manager.py`).
- Agent Memory: `.agents/MEMORY.md` and `.agents/memory/*.md` for user context, project status, and strict rules.
- System Prompt: `GEMINI.md` at repo root defining vault topology and constraints.
- `.gitignore`: Configured to ignore `.gemini/`, `.obsidian/*`, `.trash/`, `.DS_Store`, `.vscode/`, `.antigravitycli/`, `.makemd/`, `.smart-env/`, `.space/`.
- Obsidian Settings: `.obsidian/app.json`, `.obsidian/community-plugins.json`, `.obsidian/core-plugins.json`, `.obsidian/appearance.json`.
- ClasseViva Config: `99 - Meta/School/config.json`.

## Platform Requirements

- macOS (Darwin) with Zsh / Bash
- Python 3.10+ with standard packages (`requests`, `youtube_transcript_api`, `yt_dlp`)
- `ffmpeg` binary on PATH for multimedia extraction
- Obsidian Desktop application
- Quartz static site hosting (GitHub Pages / Vercel) for `05 - Blog/`
- iCloud Drive or Git synchronization for Obsidian mobile and desktop vault parity

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

## Naming Patterns

- **Markdown Notes:** Intelligent Title Case with spaces (e.g. `Evoluzione dell'Agente AI.md`, `Come Evadere il Fisco Legalmente.md`).
- **MOC Hub Notes:** `* MOC.md` (e.g. `Home MOC.md`, `Tech MOC.md`, `Corsi MOC.md`).
- **Daily Notes:** `DailyNote - YYYYMMDD.md` (e.g. `DailyNote - 20260104.md`).
- **Python Scripts:** `snake_case.py` (e.g. `tidy_vault.py`, `auto_sort_inbox.py`, `ingest_manager.py`).
- **Shell Scripts:** `kebab-case.sh` or `snake_case.sh` (e.g. `watch.sh`, `get_vault_titles.sh`).
- **Directories:** Two-digit numeric prefix for root folders (`01 - Map of Content`, `02 - Atlas`, `03 - Inbox`, `04 - Calendar`, `05 - Blog`, `99 - Meta`). Subdirectories use Title Case (`Technology/Programming/AI`).
- **Functions:** `snake_case` (e.g. `parse_yaml_frontmatter()`, `clean_filename()`, `ensure_collegamenti_section()`).
- **Variables:** `snake_case` (e.g. `vault_root`, `metadata_existing`, `tracked_files`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g. `MINOR_WORDS`, `PRESERVE_UPPER`, `BASE_URL`, `API_KEY`).
- **Classes:** `PascalCase` (e.g. `ProcessTerminator`).

## Code Style

- Adhere to PEP 8 standard conventions with 4-space indentation.
- Explicit type annotations on public API helpers and CLI utilities (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Tuple`).
- UTF-8 encoding specified explicitly on all file I/O operations (`open(..., encoding='utf-8')`).
- Use `#!/bin/bash` with explicit PATH export at script startup.
- Guard against null globs using `shopt -s nullglob`.
- Manage locks and exit traps safely (`rm -f "$LOCK_FILE"`, `atexit.register(release_lock)`).

## Markdown & Frontmatter Conventions

### 1. Atlas Permanent Notes (`02 - Atlas/`)

## Sezione Principale

## Collegamenti

- [[Nota Correlata 1]]
- [[Nota Correlata 2]]

### 2. Blog Notes (`05 - Blog/`)

### 3. Visual Formatting & Highlights (Style Guide)

- **Primary Concepts (Yellow Highlight):** `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>`
- **Secondary Concepts (Purple Highlight):** `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>`
- **CRITICAL Highlight Rule:** Never wrap `<mark>` HTML tags in markdown backticks (e.g. `` `<mark...>` `` ❌). They must be rendered as raw HTML inline.
- **Mermaid Diagrams:** Always quote node labels containing spaces or parentheses (e.g. `A["Nodo Principale (dettaglio)"]`), start blocks immediately with diagram header (`flowchart TD`), and never use raw HTML tags inside mermaid node labels.

## Import Organization

## Error Handling

- Wrap file reads with `errors='ignore'` or fallback handling to prevent crashes on non-text binary assets.
- Use `safe_rename()` with `git mv` fallbacks to standard `os.rename()` when modifying files in git-tracked environments.
- Check return codes or capture errors using `subprocess.run(..., check=True)` or `subprocess.Popen` with daemon monitoring (`ProcessTerminator`).

## Logging

## Comments & Docstrings

- Header docstrings explaining script purpose and CLI usage (`#!/usr/bin/env python3\n"""Module docstring..."""`).
- Inline comments explaining non-obvious regex transformations or edge cases in Title Case casing.
- Documenting strict vault rules (`[STRICT]` tags in memory files).

## Module & Script Design

- Provide `--dry-run` vs `--execute` flags on all file-mutating scripts to enable preview before mutation.
- Use standard `argparse` with descriptive `--help` output.
- Guard script execution with `if __name__ == '__main__': main()`.

<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

## System Overview

```text

```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Ingestion Watcher | Continuously polls `03 - Inbox/` for new raw notes or user approvals in `Review Dashboard.md` | `99 - Meta/Scripts/watch.sh` |
| Ingest Manager | Orchestrates single-note AI transformation, manages lockfiles, terminates aborted runs, updates dashboard | `99 - Meta/Scripts/ingest_manager.py` |
| YouTube Media Helper | Fetches transcripts and extracts visual screenshots into `99 - Meta/Clipboard/` via `yt-dlp` and `ffmpeg` | `99 - Meta/Scripts/youtube_helper.py` |
| Vault Tidy Linter | Standardizes Title Case filenames, normalizes YAML frontmatter, updates breadcrumbs, and aligns wiki-links | `99 - Meta/Scripts/tidy_vault.py` |
| GTD Auto-Sorter | Analyzes metadata and auto-routes staging notes from `03 - Inbox/` to final Atlas/Blog destinations | `99 - Meta/Scripts/auto_sort_inbox.py` |
| Health Dashboard Generator | Rebuilds `Vault Health Dashboard.md` in pure static Markdown (without Dataview) | `99 - Meta/Scripts/update_dashboard.py` |
| ClasseViva Exporter | Fetches school agenda, lesson subjects, and didactics materials via REST API | `99 - Meta/School/fetch-registro.py` |
| Vault Health Auditor | Scans for broken wiki-links, orphan notes without inbound links, and malformed frontmatter | `.agents/skills/audit/scripts/audit_vault.py` |
| YAML Frontmatter Linter | Validates and fixes mandatory YAML fields across vault directories | `.agents/skills/meta/scripts/lint_yaml.py` |
| Memory Dream Engine | Analyzes Antigravity conversation transcripts to consolidate user preferences and corrections | `.agents/skills/dream/scripts/dream_consolidate.py` |
| Agent System Prompt | Root definition of vault rules, folder roles, and operating conventions | `GEMINI.md` |
| Persistent Agent Memory | Master memory file storing user profile, project states, and strict rules | `.agents/MEMORY.md` |

## Pattern Overview

- **Local-First Graph Architecture:** Markdown notes interconnected via bidirectional wiki-links `[[Target Note]]`.
- **Tri-State Interactive Dashboard:** Human-in-the-loop review workflow in `03 - Inbox/Review Dashboard.md` (`[ ]` Pending, `[x]` Approved -> Relocate to Atlas/Blog, `[-]` Rejected -> Delete).
- **Static Diagnostic Governance:** Pure static Markdown dashboards avoiding runtime dependencies on dynamic query plugins (e.g. Dataview).
- **Encapsulated Agent Skills:** Self-contained skill definitions in `.agents/skills/<name>/SKILL.md` with supporting helper scripts.

## Layers

- Purpose: Temporary landing zone for raw ideas, lecture dumps, YouTube transcripts, and audit reports.
- Location: `03 - Inbox/`
- Contains: `Review Dashboard.md`, `proposed-*.md`, `raw-*.md`, `seen-*.md`.
- Depends on: `99 - Meta/Template/` for structure.
- Used by: User and Ingestion Watcher.
- Purpose: Background monitoring, multimedia extraction, AI enrichment, formatting, and file relocation.
- Location: `99 - Meta/Scripts/`, `.agents/skills/`
- Contains: Python scripts, shell scripts, and agent prompt templates.
- Depends on: External tools (`ffmpeg`, `yt-dlp`, `requests`, `agy`).
- Used by: System watcher daemon and agent slash commands (`/audit`, `/tidy`, `/meta`, `/dream`, `/process-inbox`, `/nota`).
- Purpose: Semantic indexes, topic aggregators, and high-level structural navigation.
- Location: `01 - Map of Content/`
- Key files: `Home MOC.md`, `Tech MOC.md`, `Corsi MOC.md`, `Finanza MOC.md`, `Mentality MOC.md`, `Blog MOC.md`.
- Depends on: Atlas and Blog notes for outbound references.
- Purpose: Consolidated, permanent study notes, course notes, mindset articles, and public blog posts.
- Location: `02 - Atlas/` (subdivided into `Animator2D`, `Corsi`, `Education`, `Finance`, `Mentality`, `Obsidian Second Brain`, `Palestra`, `Prompt`, `Technology`), `05 - Blog/`.
- Contains: Long-form permanent notes with standardized YAML frontmatter, breadcrumbs, and `## Collegamenti`.
- Purpose: Vault configurations, style guides, templates, system memory, and plugins.
- Location: `99 - Meta/`, `.agents/`, `.obsidian/`

## Data Flow

### Primary Request Path (Raw Note Ingestion Pipeline)

### Secondary Flow: Memory Consolidation (Dream Cycle)

### State Management:

- Note lifecycle state is stored directly in YAML frontmatter (`status: draft | in-progress | permanent | reference` or `stage: seed 🌱 | growing 🌿 | fine-tuned 🧠`).
- Ingestion lifecycle state is managed via filename prefixes (`seen-`, `raw-`, `proposed-`) and `03 - Inbox/Review Dashboard.md`.

## Key Abstractions

- Purpose: Topic index node providing structured entry points into clusters of notes.
- Examples: `01 - Map of Content/Home MOC.md`, `01 - Map of Content/Tech MOC.md`, `01 - Map of Content/Finanza MOC.md`.
- Pattern: Navigational index with grouped wiki-links and short section overviews.
- Purpose: Atomic or comprehensive conceptual note with high information density, standard breadcrumbs, and outbound connections.
- Examples: `02 - Atlas/Technology/AI/Costruire Knowledge Base per AI con LLM Wiki.md`, `02 - Atlas/Finance/Come Evadere il Fisco Legalmente.md`.
- Pattern: Frontmatter + Single-line Breadcrumb + Structured H2/H3 body with color highlights + `---` + `## Collegamenti`.
- Purpose: Encapsulated operational capability defining workflows, rules, and scripts for specific tasks.
- Examples: `.agents/skills/audit/SKILL.md`, `.agents/skills/tidy/SKILL.md`, `.agents/skills/nota/SKILL.md`.
- Pattern: YAML frontmatter metadata + step-by-step markdown protocol + helper scripts in `scripts/`.

## Entry Points

- Triggers: Background execution on user login / terminal start.
- Responsibilities: Monitors `03 - Inbox/` for changes, triggers `ingest_manager.py`, and launches Obsidian Review Dashboard.
- Triggers: Called by `watch.sh` or manual CLI invocation.
- Responsibilities: Manages ingestion lifecycle, AI dispatch, lockfiles, and interactive approvals.
- Triggers: Manual CLI execution or called via `/tidy` skill.
- Responsibilities: Scans vault, sanitizes filenames to Title Case, repairs YAML, and updates breadcrumb headers.
- Triggers: Scheduled execution, post-ingest hook, or manual run.
- Responsibilities: Re-generates `02 - Atlas/Obsidian Second Brain/Vault Health Dashboard.md`.

## Architectural Constraints

- **STRICT - No Dataview in Dashboards:** All dashboards (`Review Dashboard.md`, `Vault Health Dashboard.md`) must use pure static Markdown tables generated by Python scripts.
- **STRICT - Intelligent Title Case Filenames:** No kebab-case, snake_case, or emoji in file names (e.g. `Nome della Nota.md`).
- **STRICT - Six Root Directory Topography:** All content must reside in `01 - Map of Content`, `02 - Atlas`, `03 - Inbox`, `04 - Calendar`, `05 - Blog`, or `99 - Meta`.
- **STRICT - Wiki-Link Resolution:** Wiki-links must only target existing notes in the vault (`[[Nota Esistente]]`).
- **STRICT - Disk Persistence:** Agent changes must be written directly to the file system using file modification tools.

## Anti-Patterns

### Anti-Pattern 1: Injecting Dataview Query Blocks

### Anti-Pattern 2: Kebab-Case or Emoji-Prefixed Note Names

### Anti-Pattern 3: Unlinked Orphan Notes

## Error Handling

- Process Termination Watcher: `ProcessTerminator` in `99 - Meta/Scripts/ingest_manager.py:58` monitors the raw note file and kills running `agy`/`ffmpeg` processes if the user deletes the raw file during processing.
- Mutex Lock Guard: `acquire_lock()` and `release_lock()` in `99 - Meta/Scripts/ingest_manager.py:31` prevent race conditions using `/tmp/secondbrain_ingest.lock`.
- Dry-Run Flags: All formatting and restructuring scripts support `--dry-run` to preview file mutations before executing writes.

## Cross-Cutting Concerns

<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

| Skill | Description | Path |
|-------|-------------|------|
| audit | Health linter per il Vault. Scansiona il Second Brain per individuare note orfane, wiki-link rotti, note prive di YAML frontmatter e anomalie nei tag. | `.agents/skills/audit/SKILL.md` |
| dream | > Consolidamento autonomo della memoria dell'agente AI, ispirato a Claude Code Dreams. Analizza i transcript delle conversazioni passate di Antigravity CLI, estrae preferenze, correzioni e decisioni dell'utente, e aggiorna il file MEMORY.md persistente nel Vault. L'obiettivo è eliminare la necessità per l'utente di ripetere contesto ad ogni sessione. | `.agents/skills/dream/SKILL.md` |
| link | Scansiona una nota target e converte le occorrenze testuali di concetti e titoli del Vault in wiki-links funzionanti [[Nome Nota]]. | `.agents/skills/link/SKILL.md` |
| meta | Frontmatter Linter per verificare, correggere e standardizzare i metadati YAML nei file Markdown del Vault. | `.agents/skills/meta/SKILL.md` |
| nota | "Crea note Obsidian per la cartella 'Atlas/School/' interrogando NotebookLM come fonte primaria. Estrae contenuti da lezioni, libri di testo e approfondimenti seguendo lo stile e la densità di Lorenzo." | `.agents/skills/nota/SKILL.md` |
| process-inbox | Orchestratore GTD per analizzare, classificare e smistare automaticamente le note da 03 - Inbox alle cartelle di destinazione. | `.agents/skills/process-inbox/SKILL.md` |
| tidy | Standardizzatore e linter automatico del Vault. Pulisce la Naming Convention, valida e arricchisce lo YAML frontmatter, struttura la navigazione interna delle note e smista i file da Inbox. | `.agents/skills/tidy/SKILL.md` |
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
