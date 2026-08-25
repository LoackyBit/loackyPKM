#!/usr/bin/env python3
"""brain_ingest.py - Unified Polymorphic Ingestion Pipeline for Second Brain.

Accepts YouTube URLs, web articles, pasted text, and local files.
Features per-note hash locking with stale auto-healing, global duplicate detection,
heuristic Atlas routing, contextual keyframe embedding, non-invasive raw note intake,
Style Guide highlight sanitization, processing depth options, protected staging in 03 - Inbox/,
pure static Review Dashboard GTD management, and append-only inbox history logging.
"""

import os
import sys
import re
import datetime
import hashlib
import argparse
import subprocess
import urllib.request
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Ensure local script directory is in path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import brain_health
import youtube_helper

# Regex for detecting URLs
YT_URL_REGEX = re.compile(r'(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})')
WEB_URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)


def is_pid_alive(pid: int) -> bool:
    """Checks if a process with given PID is alive."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


class NoteLock:
    """Fine-grained hash-based mutex lock preventing duplicate/concurrent runs per source with stale auto-healing."""
    def __init__(self, identifier: str, ttl_seconds: int = 600):
        slug = hashlib.sha256(identifier.encode('utf-8')).hexdigest()[:12]
        self.lock_file = f"/tmp/brain_ingest_{slug}.lock"
        self.ttl_seconds = ttl_seconds
        self.acquired = False

    def _clean_stale_lock_if_needed(self):
        if not os.path.exists(self.lock_file):
            return
        try:
            is_stale = False
            # Check file age (TTL: default 10 minutes)
            mtime = os.path.getmtime(self.lock_file)
            if (datetime.datetime.now().timestamp() - mtime) > self.ttl_seconds:
                is_stale = True

            # Check recorded PID liveness
            if not is_stale:
                with open(self.lock_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                m = re.search(r'pid:\s*(\d+)', content)
                if m:
                    pid = int(m.group(1))
                    if not is_pid_alive(pid):
                        is_stale = True
                else:
                    is_stale = True

            if is_stale:
                os.remove(self.lock_file)
        except Exception:
            pass

    def __enter__(self):
        self._clean_stale_lock_if_needed()
        try:
            fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid: {os.getpid()}\ntimestamp: {datetime.datetime.now().isoformat()}\n".encode('utf-8'))
            os.close(fd)
            self.acquired = True
            return self
        except FileExistsError:
            self._clean_stale_lock_if_needed()
            try:
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"pid: {os.getpid()}\ntimestamp: {datetime.datetime.now().isoformat()}\n".encode('utf-8'))
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                raise RuntimeError(f"Lock already active for target source ({self.lock_file}). Ingestion in progress.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired and os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
            except Exception:
                pass


def detect_input_type(raw_input: str) -> str:
    """Detects whether raw_input is a YouTube URL, Web URL, local file, or free text."""
    stripped = raw_input.strip()
    if YT_URL_REGEX.search(stripped):
        return "youtube"
    if WEB_URL_REGEX.match(stripped):
        return "web"
    if os.path.exists(stripped) and os.path.isfile(stripped):
        return "file"
    return "text"


def sanitize_style_highlights(text: str) -> str:
    """Strips backticks from HTML <mark> and <font> tags to guarantee valid Quartz and Obsidian visual rendering."""
    return brain_health.sanitize_style_highlights(text)


def autolink_content(vault_root: str, body_text: str, current_title: str) -> Tuple[str, List[str]]:
    """Scans real vault note titles and wraps 1st and 2nd occurrences in [[Target Note]]."""
    auditor = brain_health.VaultHealthAuditor(vault_root)
    all_titles = sorted(auditor.all_notes.keys(), key=lambda x: len(x), reverse=True)

    stopwords = {
        'home', 'daily', 'note', 'studio', 'guida', 'guide', 'indice', 'index',
        'atlas', 'moc', 'blog', 'meta', 'tech', 'inbox', 'school', 'appunti'
    }

    linked_body = body_text
    inserted_links = set()
    current_clean = current_title.lower().strip()

    for title in all_titles:
        title_lower = title.lower().strip()
        if title_lower == current_clean or len(title) < 4:
            continue
        if title_lower in stopwords:
            continue

        # Regex ensuring title is not already inside [[...]], [...](...), or headers
        pattern = re.compile(r'(?<!\[\[)(?<!/)(?<![\w#])(' + re.escape(title) + r')(?![\w])(?![^\[]*\]\])(?![^\(]*\))', re.IGNORECASE)
        matches = list(pattern.finditer(linked_body))
        if matches:
            linked_body = pattern.sub(f"[[{title}]]", linked_body, count=2)
            inserted_links.add(f"[[{title}]]")

    return linked_body, sorted(list(inserted_links))


def check_duplicate_resource(vault_root: str, source_url: str, title: str) -> Optional[Tuple[str, str]]:
    """Scans permanent notes in 02 - Atlas/ and 05 - Blog/ for matching source URL or title per D-11."""
    clean_target_title = brain_health.clean_title_str(title).lower().strip()
    norm_source = source_url.strip().rstrip('/') if source_url and source_url != "original" else None

    # Strip YouTube tracking params for canonical matching
    if norm_source and ("youtube.com" in norm_source or "youtu.be" in norm_source):
        vid_id = youtube_helper.get_video_id(norm_source)
        if vid_id:
            norm_source = f"https://www.youtube.com/watch?v={vid_id}"

    search_dirs = [
        os.path.join(vault_root, "02 - Atlas"),
        os.path.join(vault_root, "05 - Blog")
    ]

    yaml_engine = brain_health.build_yaml_engine()

    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for root, _, files in os.walk(sdir):
            for file in files:
                if not file.endswith(".md"):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(2048) # Read frontmatter portion

                    has_fm, fm_text, _, _ = brain_health.split_markdown_note(content)
                    if has_fm:
                        meta = brain_health.safe_load_frontmatter(fm_text, yaml_engine)
                        existing_source = str(meta.get("source", "")).strip().rstrip('/')
                        existing_title = brain_health.clean_title_str(str(meta.get("title", file[:-3]))).lower().strip()

                        if existing_source and ("youtube.com" in existing_source or "youtu.be" in existing_source):
                            ex_vid = youtube_helper.get_video_id(existing_source)
                            if ex_vid:
                                existing_source = f"https://www.youtube.com/watch?v={ex_vid}"

                        if norm_source and existing_source and existing_source != "original" and norm_source == existing_source:
                            return (file_path, "source_url")

                        if existing_title and clean_target_title and existing_title == clean_target_title:
                            return (file_path, "title")
                except Exception:
                    continue

    return None


def classify_target_directory(title: str, tags: Optional[List[str]] = None, content: str = '') -> str:
    """Heuristically classifies note into optimal Atlas/Blog destination based on title, tags, and content per D-10."""
    tags_list = tags or []
    tags_lower = [t.lower() for t in tags_list]
    combined_text = (title + " " + " ".join(tags_list) + " " + content[:1000]).lower()

    if any(t.startswith("blog") for t in tags_lower) or "blog" in tags_lower:
        return "05 - Blog"

    # Finance
    if any("financ" in t or "fisc" in t for t in tags_lower) or any(kw in combined_text for kw in ['fisco', 'tasse', 'invest', 'soldi', 'finanz', 'patrimonio', 'crypto', 'bitcoin']):
        return "02 - Atlas/Finance"

    # Education & Learning
    if any("educat" in t or "school" in t or "studio" in t for t in tags_lower) or any(kw in combined_text for kw in ['universit', 'esame', 'studio', 'lezione', 'corso', 'ingegneria', 'didattica']):
        return "02 - Atlas/Education & Learning"

    # Mentality / Personal Growth
    if any("mental" in t or "mindset" in t or "habit" in t for t in tags_lower) or any(kw in combined_text for kw in ['mindset', 'abitudini', 'produttivita', 'crescita personale', 'focus', 'disciplina']):
        return "02 - Atlas/Personal Growth & Health/Mentality"

    # Palestra
    if any("palestr" in t or "fitness" in t or "workout" in t for t in tags_lower) or any(kw in combined_text for kw in ['allenamento', 'palestra', 'workout', 'dieta', 'scheda']):
        return "02 - Atlas/Personal Growth & Health/Palestra"

    # Projects
    if any("project" in t for t in tags_lower):
        return "02 - Atlas/Projects"

    # AI / LLM
    if any("ai" in t or "llm" in t or "rag" in t for t in tags_lower) or any(kw in combined_text for kw in ['ai', 'artificial intelligence', 'llm', 'gpt', 'claude', 'gemini', 'rag', 'agente', 'agent', 'deep learning', 'neural', 'reti neurali', 'transformer']):
        return "02 - Atlas/Tech & AI/AI"

    # Programming
    if any("programm" in t or "code" in t or "dev" in t or "python" in t for t in tags_lower) or any(kw in combined_text for kw in ['python', 'javascript', 'typescript', 'react', 'coding', 'programmazione', 'git', 'backend', 'frontend', 'rust', 'golang']):
        return "02 - Atlas/Tech & AI/Programming"

    # Hacking / Security
    if any("secur" in t or "hack" in t for t in tags_lower) or any(kw in combined_text for kw in ['security', 'cybersecurity', 'vulnerabil', 'exploit', 'pentest', 'hacker']):
        return "02 - Atlas/Tech & AI/Hacking"

    # Prompt
    if any("prompt" in t for t in tags_lower) or any(kw in combined_text for kw in ['prompt engineering', 'system prompt']):
        return "02 - Atlas/Tech & AI/Prompt"

    return "02 - Atlas/Tech & AI"


def append_inbox_history(vault_root: str, action: str, note_title: str, target: str = '', source: str = ''):
    """Appends processed GTD actions to persistent audit log 99 - Meta/logs/inbox_history.md per D-14."""
    logs_dir = os.path.join(vault_root, "99 - Meta", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    history_file = os.path.join(logs_dir, "inbox_history.md")

    if not os.path.exists(history_file):
        with open(history_file, "w", encoding="utf-8") as f:
            f.write("# 📜 Inbox History & Audit Log\n\nRegistro cronologico delle azioni di approvazione, smistamento e scarto eseguite dal motore GTD.\n\n")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_line = f"- {timestamp} | [{action.upper()}] | [[{note_title}]] -> {target} | {source}\n"

    with open(history_file, "a", encoding="utf-8") as f:
        f.write(log_line)


def record_ingest_error(vault_root: str, source_or_url: str, reason: str):
    """Registers an acquisition error into Review Dashboard.md and history log per D-18, D-21."""
    append_inbox_history(vault_root, "ERROR", source_or_url, "Review Dashboard", reason)

    dashboard_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    error_entry = f"- [ ] [!] Riprova: {source_or_url} — Motivo: {reason}\n"

    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            content = f.read()

        if f"Riprova: {source_or_url}" in content:
            return

        if "## ⚠️ Errori di Acquisizione & Azioni Richieste" in content:
            parts = content.split("## ⚠️ Errori di Acquisizione & Azioni Richieste")
            header = parts[0] + "## ⚠️ Errori di Acquisizione & Azioni Richieste\n\n"
            rest = parts[1].replace("Nessun errore di acquisizione segnalato.\n", "").lstrip()
            new_content = header + error_entry + rest
        else:
            new_content = content.rstrip() + f"\n\n## ⚠️ Errori di Acquisizione & Azioni Richieste\n\n{error_entry}"
    else:
        today_iso = datetime.date.today().strftime("%Y-%m-%d")
        new_content = f"""---
status: permanent
type: moc
area: meta
related: ["[[Home MOC]]", "[[Vault Health Dashboard]]"]
source: original
title: "Review Dashboard"
date: '{today_iso}'
updated: {datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}
tags: [meta/dashboard, meta/gtd]
summary: "Dashboard di revisione GTD per l'approvazione, smistamento o scarto delle note in Inbox."
---
[[Home MOC|Home]] / [[Meta]] / [[Review Dashboard]]

# 📥 Inbox Review Dashboard

Benvenuto nella **Dashboard di Revisione dell'Inbox**. Questo pannello ti permette di revisionare, approvare o scartare le note grezze elaborate dall'AI.

## ⚙️ Istruzioni per la Revisione
* **APPROVARE** una proposta: Sostituisci `[ ]` con `[x]` (la nota passerà a `status: permanent` e verrà spostata nella cartella target).
* **RIFIUTARE** una proposta: Sostituisci `[ ]` con `[-]` (la bozza e i file multimediali associati verranno eliminati).

## 📋 Note in Attesa di Approvazione

Tutte le note sono state elaborate con successo! Dashboard vuota.

## ⚠️ Errori di Acquisizione & Azioni Richieste

{error_entry}

## 📜 Ultime Azioni Elaborate

Nessuna azione recente.
"""

    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def format_structured_note(title: str, raw_content: str, depth: str = "executive",
                           source_type: str = "text", source_url: str = "original",
                           channel: Optional[str] = None) -> str:
    """Generates structured markdown note content adhering to depth level and Style Guide."""
    depth_norm = depth.lower().strip()
    is_deep = depth_norm in ('deep', 'approfondimento')

    header_meta = ""
    if source_type == "youtube":
        header_meta = f"- **Canale:** {channel or 'N/D'}\n- **Sorgente Video:** {source_url}\n"
    elif source_type == "web":
        header_meta = f"- **URL Articolo:** {source_url}\n"

    if is_deep:
        # Academic Study Breakdown (ex skill 'nota')
        body = f"""{header_meta}
## 🏛️ Quadro Concettuale & Fondamenti

{raw_content}

## ⚙️ Meccanica & Architettura di Dettaglio

- **Componenti Principali:** Analisi dettagliata dei singoli moduli e delle loro interazioni sistemiche.
- **Flusso Operativo:** Schema sequenziale delle operazioni e delle trasformazioni logiche.

## 🔬 Analisi Critica, Limiti & Casi d'Uso

- **Punti di Forza:** Vantaggi architetturali ed efficienza computazionale.
- **Trade-off & Limiti:** Potenziali colli di bottiglia, complessità di gestione e vincoli di scalabilità.

## 📊 Schemi & Confronti

| Dimensione | Approccio Standard | Approccio Proposto |
|---|---|---|
| Efficienza | Media | Elevata |
| Complessità | Bassa | Modulare |

## 💡 Note di Studio & Applicazioni Pratiche

Note operative ed integrazione all'interno del Second Brain.
"""
    else:
        # Executive Summary (Sintesi)
        body = f"""{header_meta}
## 🎯 Sintesi Esecutiva

{raw_content}

## 🔑 Concetti Chiave & Takeaway

- **Tesi Centrale:** Condensazione concettuale del messaggio primario della sorgente.
- **Punti Cardine:** Elementi operativi e concettuali fondamentali.

## 💡 Applicazioni & Note Operative

Come applicare questi concetti all'interno dei progetti attivi nel Second Brain.
"""
    return body.strip()


def stage_note(vault_root: str, title: str, body: str, metadata: Optional[Dict[str, Any]] = None,
               target_dir: Optional[str] = None) -> str:
    """Writes note to 03 - Inbox/<Title>.md with status: draft and registers it in Review Dashboard.md."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    os.makedirs(inbox_dir, exist_ok=True)

    clean_title = brain_health.clean_title_str(title)
    file_path = os.path.join(inbox_dir, f"{clean_title}.md")

    meta = dict(metadata) if metadata else {}
    meta['title'] = clean_title
    meta['status'] = 'draft'
    meta['type'] = meta.get('type', 'concept')
    meta['area'] = meta.get('area', 'tech')
    meta['source'] = meta.get('source', 'original')
    meta['date'] = meta.get('date', datetime.date.today().strftime("%Y-%m-%d"))
    meta['updated'] = meta.get('updated', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"))
    meta['tags'] = meta.get('tags', [f"{meta['area']}/draft"])
    if 'summary' not in meta:
        meta['summary'] = f"Bozza di elaborazione e sintesi concettuale per {clean_title}."

    # Heuristic target directory determination
    resolved_target = target_dir or classify_target_directory(clean_title, meta.get('tags', []), body)

    # Autolink content against vault
    linked_body, inserted_links = autolink_content(vault_root, body, clean_title)
    existing_related = meta.get('related', [])
    if isinstance(existing_related, str):
        existing_related = [r.strip() for r in existing_related.split(',') if r.strip()]
    merged_related = list(set(existing_related + inserted_links))
    meta['related'] = merged_related

    # Sanitize Style Guide highlights
    sanitized_body = sanitize_style_highlights(linked_body)

    # Ensure Collegamenti section
    if "## Collegamenti" not in sanitized_body:
        sanitized_body = sanitized_body.rstrip() + "\n\n---\n## Collegamenti\n"
        for link in merged_related[:5]:
            sanitized_body += f"- {link}\n"

    canonical_yaml = brain_health.format_canonical_frontmatter(meta, is_blog=False)
    breadcrumb = f"[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{clean_title}]]"
    content = brain_health.assemble_markdown_note(canonical_yaml, breadcrumb, sanitized_body)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Update Review Dashboard
    update_review_dashboard_with_draft(
        vault_root=vault_root,
        note_title=clean_title,
        area=meta['area'],
        typ=meta['type'],
        target_dir=resolved_target
    )

    return file_path


def update_review_dashboard_with_draft(vault_root: str, note_title: str, area: str, typ: str, target_dir: str):
    """Appends newly staged note to 03 - Inbox/Review Dashboard.md under pending reviews."""
    dashboard_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    today_iso = datetime.date.today().strftime("%Y-%m-%d")

    entry_line = f"- [ ] Approva [[{note_title}]] (area: {area}, type: {typ}, target: {target_dir})\n"

    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if f"Approva [[{note_title}]]" in content:
            return

        if "## 📋 Note in Attesa di Approvazione" in content:
            parts = content.split("## 📋 Note in Attesa di Approvazione")
            header = parts[0] + "## 📋 Note in Attesa di Approvazione\n\n"
            rest = parts[1].replace("Tutte le note sono state elaborate con successo! Dashboard vuota.\n", "").lstrip()
            new_content = header + entry_line + rest
        else:
            new_content = content.rstrip() + f"\n\n## 📋 Note in Attesa di Approvazione\n\n{entry_line}"
    else:
        new_content = f"""---
status: permanent
type: moc
area: meta
related: ["[[Home MOC]]", "[[Vault Health Dashboard]]"]
source: original
title: "Review Dashboard"
date: '{today_iso}'
updated: {datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}
tags: [meta/dashboard, meta/gtd]
summary: "Dashboard di revisione GTD per l'approvazione, smistamento o scarto delle note in Inbox."
---
[[Home MOC|Home]] / [[Meta]] / [[Review Dashboard]]

# 📥 Inbox Review Dashboard

Benvenuto nella **Dashboard di Revisione dell'Inbox**. Questo pannello ti permette di revisionare, approvare o scartare le note grezze elaborate dall'AI.

## ⚙️ Istruzioni per la Revisione
* **APPROVARE** una proposta: Sostituisci `[ ]` con `[x]` (la nota passerà a `status: permanent` e verrà spostata nella cartella target).
* **RIFIUTARE** una proposta: Sostituisci `[ ]` con `[-]` (la bozza e i file multimediali associati verranno eliminati).

## 📋 Note in Attesa di Approvazione

{entry_line}

## ⚠️ Errori di Acquisizione & Azioni Richieste

Nessun errore di acquisizione segnalato.

## 📜 Ultime Azioni Elaborate

Nessuna azione recente.
"""

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def process_inbox_raw_notes(vault_root: str) -> List[str]:
    """Scans 03 - Inbox/ for notes with status: ready (or process) and transforms them to drafts per D-15, D-16."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    if not os.path.exists(inbox_dir):
        return []

    processed = []
    yaml_engine = brain_health.build_yaml_engine()

    for file in os.listdir(inbox_dir):
        if not file.endswith(".md") or file == "Review Dashboard.md":
            continue

        file_path = os.path.join(inbox_dir, file)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)
            if not has_fm:
                continue

            meta = brain_health.safe_load_frontmatter(fm_text, yaml_engine)
            status_val = str(meta.get("status", "")).lower().strip()

            if status_val in ("ready", "process"):
                title = meta.get("title") or file[:-3]
                clean_title = brain_health.clean_title_str(title)

                target_dir = classify_target_directory(clean_title, meta.get("tags", []), body)
                meta["status"] = "draft"
                meta["title"] = clean_title
                meta["updated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

                # Autolink body
                linked_body, inserted_links = autolink_content(vault_root, body, clean_title)
                existing_related = meta.get("related", [])
                if isinstance(existing_related, str):
                    existing_related = [r.strip() for r in existing_related.split(",") if r.strip()]
                meta["related"] = list(set(existing_related + inserted_links))

                sanitized_body = sanitize_style_highlights(linked_body)
                if "## Collegamenti" not in sanitized_body:
                    sanitized_body = sanitized_body.rstrip() + "\n\n---\n## Collegamenti\n"
                    for lk in meta["related"][:5]:
                        sanitized_body += f"- {lk}\n"

                canonical_yaml = brain_health.format_canonical_frontmatter(meta, is_blog=False)
                new_breadcrumb = f"[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{clean_title}]]"
                new_content = brain_health.assemble_markdown_note(canonical_yaml, new_breadcrumb, sanitized_body)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                update_review_dashboard_with_draft(
                    vault_root=vault_root,
                    note_title=clean_title,
                    area=meta.get("area", "tech"),
                    typ=meta.get("type", "concept"),
                    target_dir=target_dir
                )
                processed.append(file_path)
                print(f"[RAW INTAKE] Processed raw note {file} -> draft")
        except Exception as e:
            print(f"Warning: Failed to process raw note {file}: {e}", file=sys.stderr)

    return processed


def process_tri_state_approvals(vault_root: str) -> int:
    """Processes [x] (promote to permanent & move) or [-] (delete draft) in 03 - Inbox/Review Dashboard.md per D-07, D-12, D-13, D-14."""
    dashboard_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    if not os.path.exists(dashboard_path):
        return 0

    with open(dashboard_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    re_app = re.compile(r'^\s*-\s+\[x\]\s+Approva\s+\[\[(.*?)\]\](?:\s+\(.*target:\s*(.*?)\))?')
    re_rej = re.compile(r'^\s*-\s+\[-\]\s+Approva\s+\[\[(.*?)\]\]')

    updated_lines = []
    actions_count = 0
    recent_actions = []
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    yaml_engine = brain_health.build_yaml_engine()

    for line in lines:
        m_app = re_app.match(line)
        m_rej = re_rej.match(line)

        if m_app:
            note_name = m_app.group(1).strip()
            target_dest = m_app.group(2).strip() if m_app.group(2) else "02 - Atlas/Tech & AI"

            src_file = os.path.join(inbox_dir, f"{note_name}.md")
            if os.path.exists(src_file):
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)
                meta = brain_health.safe_load_frontmatter(fm_text, yaml_engine) if has_fm else {}

                dest_dir = os.path.join(vault_root, target_dest)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, f"{note_name}.md")

                # Collision check per D-12
                if os.path.exists(dest_file):
                    try:
                        with open(dest_file, "r", encoding="utf-8", errors="ignore") as df:
                            dest_content = df.read(2048)
                        _, df_fm, _, _ = brain_health.split_markdown_note(dest_content)
                        dest_meta = brain_health.safe_load_frontmatter(df_fm, yaml_engine)
                        if str(dest_meta.get("source", "")) != str(meta.get("source", "")):
                            print(f"[COLLISION] Filename collision for {note_name} in {target_dest}/ with differing source. Move blocked.")
                            updated_lines.append(f"- [!] Conflitto nome file: [[{note_name}]] esiste già in [[{target_dest}/{note_name}]] con sorgente diversa. Rinomina prima di approvare.\n")
                            continue
                    except Exception:
                        pass

                meta['status'] = 'permanent'
                meta['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

                new_rel = os.path.relpath(dest_file, vault_root)
                new_breadcrumb = brain_health.get_breadcrumbs(new_rel, note_name)
                canonical_yaml = brain_health.format_canonical_frontmatter(meta, is_blog=new_rel.startswith("05 - Blog"))
                new_content = brain_health.assemble_markdown_note(canonical_yaml, new_breadcrumb, body)

                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                os.remove(src_file)
                append_inbox_history(vault_root, "APPROVED", note_name, target_dest, meta.get("source", "original"))
                recent_actions.append(f"- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | [APPROVED] | [[{note_name}]] -> {target_dest}")
                print(f"[APPROVED] Promoted {note_name} -> {target_dest}/")
                actions_count += 1
            continue

        elif m_rej:
            note_name = m_rej.group(1).strip()
            src_file = os.path.join(inbox_dir, f"{note_name}.md")
            if os.path.exists(src_file):
                os.remove(src_file)

            # Clean clipboard images per D-07
            clipboard_dir = os.path.join(vault_root, "99 - Meta", "Clipboard")
            if os.path.exists(clipboard_dir):
                for f in os.listdir(clipboard_dir):
                    if note_name.lower() in f.lower():
                        try:
                            os.remove(os.path.join(clipboard_dir, f))
                        except Exception:
                            pass

            append_inbox_history(vault_root, "REJECTED", note_name, "Purged", "Clipboard assets cleaned")
            recent_actions.append(f"- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | [REJECTED] | [[{note_name}]] (Purged)")
            print(f"[REJECTED] Discarded staging draft {note_name}")
            actions_count += 1
            continue

        else:
            updated_lines.append(line)

    if updated_lines != lines or actions_count > 0:
        # Append recent actions to dashboard's recent actions section
        full_text = "".join(updated_lines)
        if recent_actions:
            new_actions_block = "\n".join(recent_actions) + "\n"
            if "## 📜 Ultime Azioni Elaborate" in full_text:
                parts = full_text.split("## 📜 Ultime Azioni Elaborate")
                header = parts[0] + "## 📜 Ultime Azioni Elaborate\n\n"
                rest = parts[1].replace("Nessuna azione recente.\n", "").lstrip()
                # Keep top 10 lines
                existing_lines = [l for l in rest.splitlines() if l.strip()]
                combined = (recent_actions + existing_lines)[:10]
                full_text = header + "\n".join(combined) + "\n"
            else:
                full_text = full_text.rstrip() + f"\n\n## 📜 Ultime Azioni Elaborate\n\n{new_actions_block}"

        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

    return actions_count


def ingest_youtube_source(url: str, depth: str, extract_frames: bool, vault_root: str, target_dir: Optional[str] = None) -> str:
    """Ingests YouTube video transcript and metadata via youtube_helper.py with duplicate detection and frame embedding per D-05, D-11, D-18."""
    # Check duplicate resource
    dup = check_duplicate_resource(vault_root, url, "")
    if dup:
        dup_path, reason = dup
        rel_dup = os.path.relpath(dup_path, vault_root)
        print(f"[DUPLICATE] Source URL already exists in {rel_dup}. Ingestion blocked.", file=sys.stderr)
        record_ingest_error(vault_root, url, f"Duplicato rilevato: la risorsa esiste già in [[{rel_dup}]].")
        return dup_path

    try:
        data = youtube_helper.extract_youtube_data(url, extract_frames=extract_frames, vault_root=vault_root)
    except youtube_helper.TranscriptUnavailableError as e:
        record_ingest_error(vault_root, url, f"Trascrizione non disponibile: {e}")
        raise
    except Exception as e:
        record_ingest_error(vault_root, url, f"Errore estrazione dati YouTube: {e}")
        raise

    title = brain_health.clean_title_str(data.get('title', 'Video YouTube'))
    channel = data.get('channel', 'YouTube')
    chapters = data.get('chapters', []) or []
    transcript = data.get('transcript', []) or []
    extracted_images = data.get('extracted_images', []) or []

    # Check title duplicate
    dup_t = check_duplicate_resource(vault_root, "", title)
    if dup_t:
        dup_path, _ = dup_t
        rel_dup = os.path.relpath(dup_path, vault_root)
        print(f"[DUPLICATE] Note with title '{title}' already exists in {rel_dup}. Ingestion blocked.", file=sys.stderr)
        record_ingest_error(vault_root, url, f"Duplicato rilevato: nota omonima in [[{rel_dup}]].")
        return dup_path

    # Format transcript text with contextual frame insertion per D-05
    text_blocks = []
    if chapters:
        for idx, ch in enumerate(chapters):
            ch_title = ch.get('title', f'Capitolo {idx + 1}') if isinstance(ch, dict) else f'Capitolo {idx + 1}'
            start = ch.get('start_time', 0) if isinstance(ch, dict) else 0
            end = ch.get('end_time', 0) if isinstance(ch, dict) else 0
            ch_text = " ".join([
                getattr(t, 'text', t.get('text', '') if isinstance(t, dict) else str(t))
                for t in transcript
                if start <= (getattr(t, 'start', t.get('start', 0) if isinstance(t, dict) else 0)) < end
            ])

            # Find matching frame for this chapter index
            frame_embed = ""
            if idx < len(extracted_images):
                img_name = os.path.basename(extracted_images[idx])
                frame_embed = f"![[{img_name}]]\n\n"

            text_blocks.append(f"### {ch_title}\n{frame_embed}{ch_text}\n")
    else:
        main_text = " ".join([
            getattr(t, 'text', t.get('text', '') if isinstance(t, dict) else str(t))
            for t in transcript
        ])
        if extracted_images:
            frames_block = "\n### 🖼️ Frame Salienti\n\n" + "\n".join([f"![[{os.path.basename(img)}]]" for img in extracted_images]) + "\n"
            main_text = main_text + frames_block
        text_blocks.append(main_text)

    raw_text = "\n".join(text_blocks)
    body = format_structured_note(title, raw_text, depth=depth, source_type="youtube", source_url=url, channel=channel)

    meta = {
        "title": title,
        "type": "video",
        "area": "tech",
        "source": url,
        "tags": ["tech/video", "tech/transcript"]
    }
    return stage_note(vault_root, title, body, meta, target_dir=target_dir)


def ingest_web_source(url: str, depth: str, vault_root: str, target_dir: Optional[str] = None) -> str:
    """Ingests Web article content with duplicate checking per D-11."""
    dup = check_duplicate_resource(vault_root, url, "")
    if dup:
        dup_path, _ = dup
        rel_dup = os.path.relpath(dup_path, vault_root)
        print(f"[DUPLICATE] Web article already exists in {rel_dup}. Ingestion blocked.", file=sys.stderr)
        record_ingest_error(vault_root, url, f"Duplicato rilevato: articolo già presente in [[{rel_dup}]].")
        return dup_path

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        record_ingest_error(vault_root, url, f"Errore download pagina web: {e}")
        raise

    # Basic title extraction
    m_title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    raw_title = m_title.group(1).strip() if m_title else "Web Article"
    clean_title = brain_health.clean_title_str(raw_title)

    # Check title duplicate
    dup_t = check_duplicate_resource(vault_root, "", clean_title)
    if dup_t:
        dup_path, _ = dup_t
        rel_dup = os.path.relpath(dup_path, vault_root)
        print(f"[DUPLICATE] Note with title '{clean_title}' already exists in {rel_dup}. Ingestion blocked.", file=sys.stderr)
        record_ingest_error(vault_root, url, f"Duplicato rilevato: nota omonima in [[{rel_dup}]].")
        return dup_path

    # Strip basic HTML tags
    clean_text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<style.*?</style>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
    clean_text = " ".join(clean_text.split())[:4000]

    body = format_structured_note(clean_title, clean_text, depth=depth, source_type="web", source_url=url)

    meta = {
        "title": clean_title,
        "type": "article",
        "area": "tech",
        "source": url,
        "tags": ["tech/web", "tech/article"]
    }
    return stage_note(vault_root, clean_title, body, meta, target_dir=target_dir)


def ingest_file_or_text_source(source: str, input_type: str, depth: str, vault_root: str, target_dir: Optional[str] = None) -> str:
    """Ingests local markdown/text file or pasted text."""
    if input_type == "file":
        with open(source, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        filename_title = Path(source).stem
        clean_title = brain_health.clean_title_str(filename_title)
        source_url = "original"
    else:
        content = source.strip()
        first_line = content.splitlines()[0] if content else "Appunto Ingest"
        clean_title = brain_health.clean_title_str(first_line[:40])
        source_url = "original"

    body = format_structured_note(clean_title, content, depth=depth, source_type="text", source_url=source_url)
    meta = {
        "title": clean_title,
        "type": "concept",
        "area": "tech",
        "source": source_url,
        "tags": ["tech/concept"]
    }
    return stage_note(vault_root, clean_title, body, meta, target_dir=target_dir)


def ingest_source(source: str, depth: str = "executive", extract_frames: bool = False,
                  vault_root: Optional[str] = None, target_dir: Optional[str] = None) -> str:
    """Main entrypoint routing polymorphic inputs through per-note lock and staging."""
    root = brain_health.get_vault_root(vault_root)
    input_type = detect_input_type(source)

    with NoteLock(source):
        if input_type == "youtube":
            return ingest_youtube_source(source, depth, extract_frames, root, target_dir)
        elif input_type == "web":
            return ingest_web_source(source, depth, root, target_dir)
        else:
            return ingest_file_or_text_source(source, input_type, depth, root, target_dir)


def build_arg_parser() -> argparse.ArgumentParser:
    """CLI argument parser for brain_ingest."""
    parser = argparse.ArgumentParser(
        description="brain_ingest.py - Unified Polymorphic Ingestion & Staging Engine."
    )
    parser.add_argument('source', nargs='?', default=None, help="Input source (YouTube URL, Web URL, file path, or text).")
    parser.add_argument('--depth', choices=['executive', 'sintesi', 'deep', 'approfondimento'], default='executive', help="Processing depth level (default: executive).")
    parser.add_argument('--extract-frames', action='store_true', help="Extract keyframe screenshots for visual YouTube videos.")
    parser.add_argument('--target-dir', default=None, help="Target permanent directory after GTD approval (auto-classified if omitted).")
    parser.add_argument('--process-approvals', action='store_true', help="Process approved [x] or rejected [-] notes in Review Dashboard.md.")
    parser.add_argument('--scan-inbox', action='store_true', help="Scan 03 - Inbox/ for notes with status: ready and convert to drafts.")
    parser.add_argument('--vault-root', type=str, default=None, help="Custom vault root directory.")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    vault_root = brain_health.get_vault_root(args.vault_root)

    if args.process_approvals:
        processed = process_tri_state_approvals(vault_root)
        print(f"Processed {processed} review dashboard actions.")
        return

    if args.scan_inbox:
        processed_raw = process_inbox_raw_notes(vault_root)
        print(f"Processed {len(processed_raw)} raw notes in Inbox.")
        return

    if not args.source:
        parser.print_help()
        sys.exit(1)

    staged_path = ingest_source(
        source=args.source,
        depth=args.depth,
        extract_frames=args.extract_frames,
        vault_root=vault_root,
        target_dir=args.target_dir
    )
    print(f"Successfully staged note: {staged_path}")


if __name__ == '__main__':
    main()
