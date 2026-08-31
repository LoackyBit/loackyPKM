---
status: permanent
type: concept
area: tech
related: ["[[Home]]", "[[Gemini]]", "[[Vault Health Dashboard]]"]
source: original
title: "Agents"
date: '2026-08-24'
updated: 2026-08-25T00:10
tags: [meta/system, tech/ai]
summary: "AI Second Brain — Obsidian PKM & Digital Garden system architecture, skills definition, and runtime conventions."
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
- Python (3.10 - 3.13) - Automation scripts, data fetchers, linting utilities, and health governance (`99 - Meta/Scripts/brain_health.py`, `99 - Meta/Scripts/brain_ingest.py`, `99 - Meta/Scripts/youtube_helper.py`, `99 - Meta/School/fetch-registro.py`).
- Bash / Shell Scripting - Daemon watchers (`99 - Meta/Scripts/watch.sh`).
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
- Antigravity Agent Runtime - Autonomous multi-agent framework orchestrating GSD workflows, macro-skills (`brain-health`, `brain-ingest`, `brain-recall`), and note processing.
- Python built-in `argparse` dry-run testing suites (`--dry-run` vs `--auto-fix` in `99 - Meta/Scripts/brain_health.py`).
- Python `unittest` automated test suite (`tests/test_brain_health.py`, `tests/test_brain_ingest.py`).
- Git - Version control and file tracking integration (`.gitignore`, `obsidian-git` plugin).

## Key Dependencies

- `ruamel.yaml` (Python RoundTrip YAML parser) - Lossless AST YAML parsing and formatting in `99 - Meta/Scripts/brain_health.py`.
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

- PATH requirements: `/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin` (configured in `99 - Meta/Scripts/watch.sh`).
- Agent Memory: `.agents/MEMORY.md` and `.agents/memory/*.md` for user context, project status, and strict rules.
- System Prompt: `GEMINI.md` at repo root defining vault topology, 3 macro-skills, and constraints.
- `.gitignore`: Configured to ignore `.gemini/`, `.obsidian/*`, `.trash/`, `.DS_Store`, `.vscode/`, `.antigravitycli/`, `.makemd/`, `.smart-env/`, `.space/`.
- Obsidian Settings: `.obsidian/app.json`, `.obsidian/community-plugins.json`, `.obsidian/core-plugins.json`, `.obsidian/appearance.json`.
- ClasseViva Config: `99 - Meta/School/config.json`.

## Platform Requirements

- macOS (Darwin) with Zsh / Bash
- Python 3.10+ with standard packages (`requests`, `youtube_transcript_api`, `yt_dlp`, `ruamel.yaml`)
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
- **Python Scripts:** `snake_case.py` (e.g. `brain_health.py`, `brain_ingest.py`, `youtube_helper.py`).
- **Shell Scripts:** `kebab-case.sh` or `snake_case.sh` (e.g. `watch.sh`).
- **Directories:** Two-digit numeric prefix for root folders (`01 - Map of Content`, `02 - Atlas`, `03 - Inbox`, `04 - Calendar`, `05 - Blog`, `99 - Meta`). Subdirectories use Title Case (`Technology/Programming/AI`).
- **Functions:** `snake_case` (e.g. `format_canonical_frontmatter()`, `autolink_content()`, `audit_file_links()`).
- **Variables:** `snake_case` (e.g. `vault_root`, `metadata_existing`, `tracked_files`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g. `MINOR_WORDS`, `PRESERVE_UPPER`, `CONTROLLED_TYPES`, `CONTROLLED_AREAS`).
- **Classes:** `PascalCase` (e.g. `VaultHealthAuditor`, `NoteLock`).

## Code Style

- Adhere to PEP 8 standard conventions with 4-space indentation.
- Explicit type annotations on public API helpers and CLI utilities (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Tuple`).
- UTF-8 encoding specified explicitly on all file I/O operations (`open(..., encoding='utf-8')`).
- Use `#!/bin/bash` with explicit PATH export at script startup.
- Guard against null globs using `shopt -s nullglob`.
- Manage locks and exit traps safely (`rm -f "$LOCK_FILE"`, `NoteLock` context managers).

## Markdown & Frontmatter Conventions

### 1. Atlas Permanent Notes (`02 - Atlas/`)

```yaml
---
status: permanent           # draft | in-progress | permanent | reference
type: concept               # concept | video | article | lecture | book | project | moc | journal
area: tech                  # tech | education | mentality | finance | projects | meta | calendar
related: ["[[Nota A]]", "[[Nota B]]"]
aliases: ["Alias Nota"]
source: original            # URL/citazione o "original"
title: "Titolo della Nota in Title Case"
date: '2026-02-01'
updated: 2026-02-01T20:32
tags: [tech/ai, tech/rag]   # Tassonomia gerarchica
summary: "Sintesi concettuale esecutiva (120-180 caratteri, max 200) per retrieval sub-secondo."
---
## Sezione Principale

Trattazione concettuale arricchita con evidenziazioni Style Guide ed eventuali diagrammi o formule LaTeX. I collegamenti semantici a [[Nota Correlata 1]] e [[Nota Correlata 2]] sono integrati direttamente nel discorso e sincronizzati nel frontmatter YAML `related: [...]`.

### 2. Blog Notes (`05 - Blog/`)

### 3. Visual Formatting & Highlights (Style Guide)

- **Primary Concepts (Yellow Highlight):** <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>
- **Secondary Concepts (Purple Highlight):** <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>
- **CRITICAL Highlight Rule:** Never wrap `<mark>` HTML tags in markdown backticks (e.g. `` `<mark...>` `` ❌). They must be rendered as raw HTML inline.
- **Mermaid Diagrams:** Always quote node labels containing spaces or parentheses (e.g. `A["Nodo Principale (dettaglio)"]`), start blocks immediately with diagram header (`flowchart TD`), and never use raw HTML tags inside mermaid node labels.

## Error Handling

- Wrap file reads with `errors='ignore'` or fallback handling to prevent crashes on non-text binary assets.
- Use atomic writing patterns and per-note lock mutexes (`/tmp/brain_ingest_<hash>.lock`) to prevent ingestion collisions.
- Check return codes or capture errors using `subprocess.run(..., check=True)` or `subprocess.Popen`.

## Module & Script Design

- Provide `--dry-run` vs `--auto-fix` flags on all file-mutating scripts to enable preview before mutation.
- Use standard `argparse` with descriptive `--help` output.
- Guard script execution with `if __name__ == '__main__': main()`.

<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

## System Overview

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                           External Inputs                               │
├──────────────────┬──────────────────────┬───────────────────────────────┤
│ YouTube Videos   │  ClasseViva (School) │  Web Articles / Raw Notes     │
│ `youtube_helper` │  `fetch-registro.py` │  `03 - Inbox/` Staging Notes  │
└────────┬─────────┴──────────┬───────────┴──────────────┬────────────────┘
         │                    │                          │
         ▼                    ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Ingestion & Automation Layer                         │
│  `99 - Meta/Scripts/watch.sh` (Daemon Watcher)                          │
│  `99 - Meta/Scripts/brain_ingest.py` (Polymorphic Intake & GTD Router)  │
│  `99 - Meta/Scripts/youtube_helper.py` (Transcript & Screenshot Helper) │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Review & Feedback Interface                         │
│  `03 - Inbox/Review Dashboard.md` (Tri-State Approvals `[ ]/[x]/[-]`)   │
│  `99 - Meta/Vault Health Dashboard.md` (Static Diagnostic Governance)   │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Core Knowledge Repository (ACE)                     │
│  `01 - Map of Content/` │ `02 - Atlas/`    │ `05 - Blog/` (Quartz)      │
│  `04 - Calendar/`       │ `99 - Meta/`     │ `.agents/` (Agent Memory)  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Vault Governance & Health Skills                    │
│  `brain-health` (`brain_health.py` - AST Linter & Smart Link Auditor)   │
│  `brain-ingest` (`brain_ingest.py` - Universal Intake & GTD Engine)     │
│  `brain-recall` (`recall_engine.py` - NotebookLM Retrieval Interface)   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Ingestion Watcher | Continuously polls `03 - Inbox/Review Dashboard.md` for user approvals (`[x]`/`[-]`) | `99 - Meta/Scripts/watch.sh` |
| Brain Ingest Engine | Polymorphic intake router, per-note lock mutex, autolinking, Style Guide highlights, staging in Inbox, tri-state GTD promotion | `99 - Meta/Scripts/brain_ingest.py` |
| YouTube Media Helper | Fetches transcripts and extracts visual screenshots into `99 - Meta/Clipboard/` via `yt-dlp` and `ffmpeg` | `99 - Meta/Scripts/youtube_helper.py` |
| Brain Health Engine | AST 10-field YAML normalizer, Title Case linter, smart forward/broken link auditor, orphan note detector, static dashboard builder | `99 - Meta/Scripts/brain_health.py` |
| Health Dashboard Generator | Rebuilds `Vault Health Dashboard.md` in pure static Markdown (without Dataview) | `99 - Meta/Scripts/brain_health.py` |
| ClasseViva Exporter | Fetches school agenda, lesson subjects, and didactics materials via REST API | `99 - Meta/School/fetch-registro.py` |
| Agent System Prompt | Root definition of vault rules, folder roles, 3 macro-skills, and operating conventions | `GEMINI.md` |
| Persistent Agent Memory | Master memory file storing user profile, project states, and strict rules | `.agents/MEMORY.md` |

## Pattern Overview

- **Local-First Graph Architecture:** Markdown notes interconnected via bidirectional wiki-links `[[Target Note]]`.
- **Tri-State Interactive Dashboard:** Human-in-the-loop review workflow in `03 - Inbox/Review Dashboard.md` (`[ ]` Pending, `[x]` Approved -> Relocate to Atlas/Blog, `[-]` Rejected -> Delete).
- **Static Diagnostic Governance:** Pure static Markdown dashboards avoiding runtime dependencies on dynamic query plugins (e.g. Dataview).
- **Encapsulated Macro-Skills:** Exactly 3 consolidated macro-skills in `.agents/skills/` (`brain-health`, `brain-ingest`, `brain-recall`).

## Layers

- Purpose: Temporary landing zone for raw ideas, lecture dumps, YouTube transcripts, and staging notes.
- Location: `03 - Inbox/`
- Contains: `Review Dashboard.md`, `<Title>.md` (with `status: draft`).
- Depends on: `99 - Meta/Template/` for structure.
- Used by: User, Ingestion Watcher, and `brain_ingest.py`.
- Purpose: Background monitoring, multimedia extraction, AI enrichment, formatting, and file relocation.
- Location: `99 - Meta/Scripts/`, `.agents/skills/`
- Contains: Python scripts, shell scripts, and agent skill protocols.
- Depends on: External tools (`ffmpeg`, `yt-dlp`, `requests`, `ruamel.yaml`).
- Used by: System watcher daemon and agent slash commands (`/brain-health`, `/brain-ingest`, `/brain-recall`).
- Purpose: Semantic indexes, topic aggregators, and high-level structural navigation.
- Location: `01 - Map of Content/`
- Key files: `Home MOC.md`, `Tech MOC.md`, `Corsi MOC.md`, `Finanza MOC.md`, `Mentality MOC.md`, `Blog MOC.md`.
- Depends on: Atlas and Blog notes for outbound references.
- Purpose: Consolidated, permanent study notes, course notes, mindset articles, and public blog posts.
- Location: `02 - Atlas/` (subdivided into `Animator2D`, `Corsi`, `Education`, `Finance`, `Mentality`, `Obsidian Second Brain`, `Palestra`, `Prompt`, `Technology`), `05 - Blog/`.
- Contains: Long-form permanent notes with standardized YAML frontmatter, breadcrumbs, and organic inline wiki-links synchronized in `related: [...]`.
- Purpose: Vault configurations, style guides, templates, system memory, and plugins.
- Location: `99 - Meta/`, `.agents/`, `.obsidian/`

## Data Flow

### Primary Request Path (Raw Note Ingestion Pipeline)

1. User ingests URL, raw text, or file via `brain-ingest` (`python3 "99 - Meta/Scripts/brain_ingest.py" "<Sorgente>" --depth approfondimento`).
2. `brain_ingest.py` acquires per-source lock `/tmp/brain_ingest_<hash>.lock`.
3. If YouTube URL: `youtube_helper.py` fetches transcripts and optional screenshots into `99 - Meta/Clipboard/`.
4. `brain_ingest.py` applies Style Guide formatting, autolinks concepts organically in prose, and writes `03 - Inbox/Draft/<Title>.md` with `status: draft`.
5. `brain_ingest.py` registers the draft in `03 - Inbox/Review Dashboard.md` with checkbox `- [ ] Approva [[Draft/<Title>]]`.
6. User checks checkbox to `- [x] Approva`: `watch.sh` or `brain_ingest.py --process-approvals` sets `status: permanent` and moves file to `02 - Atlas/...` or `05 - Blog/`.
7. User checks checkbox to `[-] Approva`: `brain_ingest.py --process-approvals` deletes the staging draft, source note, and associated clipboard screenshots.

### State Management:

- Note lifecycle state is stored directly in YAML frontmatter (`status: draft | in-progress | permanent | reference` or `stage: seed 🌱 | growing 🌿 | fine-tuned 🧠`).
- Ingestion lifecycle state is managed via `03 - Inbox/Review Dashboard.md`.

## Key Abstractions

- Purpose: Topic index node providing structured entry points into clusters of notes.
- Examples: `01 - Map of Content/Home MOC.md`, `01 - Map of Content/Tech MOC.md`, `01 - Map of Content/Finanza MOC.md`.
- Pattern: Navigational index with grouped wiki-links and short section overviews.
- Purpose: Atomic or comprehensive conceptual note with high information density, standard breadcrumbs, and outbound connections.
- Examples: `02 - Atlas/Technology/AI/Costruire Knowledge Base per AI con LLM Wiki.md`, `02 - Atlas/Finance/Come Evadere il Fisco Legalmente.md`.
- Pattern: Frontmatter + Single-line Breadcrumb + Structured H2/H3 body with color highlights + organic inline wiki-links.
- Purpose: Encapsulated operational capability defining workflows, rules, and scripts for the 3 macro-flows.
- Examples: `.agents/skills/brain-health/SKILL.md`, `.agents/skills/brain-ingest/SKILL.md`, `.agents/skills/brain-recall/SKILL.md`.
- Pattern: YAML frontmatter metadata + step-by-step markdown protocol + helper scripts in `99 - Meta/Scripts/`.

## Entry Points

- Triggers: Background execution on user login / terminal start.
- Responsibilities: Monitors `03 - Inbox/Review Dashboard.md` for pending approvals/rejections and triggers `brain_ingest.py --process-approvals`.
- Triggers: Manual CLI invocation or slash command `/brain-ingest`.
- Responsibilities: Manages polymorphic ingestion lifecycle, AI dispatch, lockfiles, and interactive approvals.
- Triggers: Manual CLI execution or slash command `/brain-health`.
- Responsibilities: Scans vault, sanitizes filenames to Title Case, validates YAML frontmatter, audits links/orphans, and updates static `Vault Health Dashboard.md`.
- Triggers: Manual CLI slash command `/brain-recall <query>` or natural language query in chat.
- Responsibilities: Retrieves relevant notes, generates executive summary with exact `[[Note]]` citations and zero hallucinations.

## Architectural Constraints

- **STRICT - No Dataview in Dashboards:** All dashboards (`Review Dashboard.md`, `Vault Health Dashboard.md`) must use pure static Markdown tables generated by Python scripts.
- **STRICT - Intelligent Title Case Filenames:** No kebab-case, snake_case, or emoji in file names (e.g. `Nome della Nota.md`).
- **STRICT - Six Root Directory Topography:** All content must reside in `01 - Map of Content`, `02 - Atlas`, `03 - Inbox`, `04 - Calendar`, `05 - Blog`, or `99 - Meta`.
- **STRICT - Wiki-Link Resolution:** Wiki-links must only target existing notes in the vault (`[[Nota Esistente]]`). Forward-links are recognized and preserved.
- **STRICT - Disk Persistence:** Agent changes must be written directly to the file system using file modification tools.

## Anti-Patterns

### Anti-Pattern 1: Injecting Dataview Query Blocks

### Anti-Pattern 2: Kebab-Case or Emoji-Prefixed Note Names

### Anti-Pattern 3: Unlinked Orphan Notes

## Error Handling

- Mutex Lock Guard: `NoteLock` in `99 - Meta/Scripts/brain_ingest.py` prevents race conditions using fine-grained `/tmp/brain_ingest_<hash>.lock`.
- Dry-Run Flags: `brain_health.py` supports `--dry-run` to preview file mutations before executing writes.

## Cross-Cutting Concerns

<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

| Skill | Description | Path |
|-------|-------------|------|
| brain-health | Vault health governance, 10-field YAML linting, Title Case normalization, smart forward/broken link audit, and static Health Dashboard generation. | `.agents/skills/brain-health/SKILL.md` |
| brain-ingest | Polymorphic intake engine for YouTube videos, web articles, pasted text, and local documents with Title Case naming, 10-field YAML, contextual autolinking, and tri-state GTD review. | `.agents/skills/brain-ingest/SKILL.md` |
| brain-recall | Retrieval and synthesis interface modeled after NotebookLM. Provides executive answers backed by exact [[Note]] citations and strict zero-hallucination guards. | `.agents/skills/brain-recall/SKILL.md` |
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
