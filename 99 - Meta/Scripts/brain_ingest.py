#!/usr/bin/env python3
"""brain_ingest.py - Unified Polymorphic Ingestion Pipeline for Second Brain.

Accepts YouTube URLs, web articles, pasted text, and local files.
Features per-note hash locking, contextual autolinking, Style Guide highlight sanitization,
processing depth options, protected staging in 03 - Inbox/, and tri-state Review Dashboard GTD review.
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
               target_dir: str = "02 - Atlas/Tech") -> str:
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
        target_dir=target_dir
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

{entry_line}"""

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def process_tri_state_approvals(vault_root: str) -> int:
    """Processes [x] (promote to permanent & move) or [-] (delete draft) in 03 - Inbox/Review Dashboard.md."""
    dashboard_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    if not os.path.exists(dashboard_path):
        return 0

    with open(dashboard_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    re_app = re.compile(r'^\s*-\s+\[x\]\s+Approva\s+\[\[(.*?)\]\](?:\s+\(.*target:\s*(.*?)\))?')
    re_rej = re.compile(r'^\s*-\s+\[-\]\s+Approva\s+\[\[(.*?)\]\]')

    updated_lines = []
    actions_count = 0
    inbox_dir = os.path.join(vault_root, "03 - Inbox")

    for line in lines:
        m_app = re_app.match(line)
        m_rej = re_rej.match(line)

        if m_app:
            note_name = m_app.group(1).strip()
            target_dest = m_app.group(2).strip() if m_app.group(2) else "02 - Atlas/Tech"

            src_file = os.path.join(inbox_dir, f"{note_name}.md")
            if os.path.exists(src_file):
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)
                yaml_engine = brain_health.build_yaml_engine()
                meta = brain_health.safe_load_frontmatter(fm_text, yaml_engine) if has_fm else {}

                meta['status'] = 'permanent'
                meta['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

                dest_dir = os.path.join(vault_root, target_dest)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, f"{note_name}.md")

                new_rel = os.path.relpath(dest_file, vault_root)
                new_breadcrumb = brain_health.get_breadcrumbs(new_rel, note_name)
                canonical_yaml = brain_health.format_canonical_frontmatter(meta, is_blog=new_rel.startswith("05 - Blog"))
                new_content = brain_health.assemble_markdown_note(canonical_yaml, new_breadcrumb, body)

                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                os.remove(src_file)
                print(f"[APPROVED] Promoted {note_name} -> {target_dest}/")
                actions_count += 1
            continue

        elif m_rej:
            note_name = m_rej.group(1).strip()
            src_file = os.path.join(inbox_dir, f"{note_name}.md")
            if os.path.exists(src_file):
                os.remove(src_file)

            # Clean clipboard images
            clipboard_dir = os.path.join(vault_root, "99 - Meta", "Clipboard")
            if os.path.exists(clipboard_dir):
                for f in os.listdir(clipboard_dir):
                    if note_name.lower() in f.lower():
                        try:
                            os.remove(os.path.join(clipboard_dir, f))
                        except Exception:
                            pass

            print(f"[REJECTED] Discarded staging draft {note_name}")
            actions_count += 1
            continue

        else:
            updated_lines.append(line)

    if actions_count > 0:
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

    return actions_count


def ingest_youtube_source(url: str, depth: str, extract_frames: bool, vault_root: str, target_dir: str) -> str:
    """Ingests YouTube video transcript and metadata via youtube_helper.py."""
    import youtube_helper
    data = youtube_helper.extract_youtube_data(url, extract_frames=extract_frames)

    title = brain_health.clean_title_str(data.get('title', 'Video YouTube'))
    channel = data.get('channel', 'YouTube')
    chapters = data.get('chapters', [])
    transcript = data.get('transcript', [])

    # Format transcript text
    text_blocks = []
    if chapters:
        for ch in chapters:
            ch_title = ch.get('title', 'Capitolo') if isinstance(ch, dict) else getattr(ch, 'title', 'Capitolo')
            start = ch.get('start_time', 0) if isinstance(ch, dict) else getattr(ch, 'start_time', 0)
            end = ch.get('end_time', 0) if isinstance(ch, dict) else getattr(ch, 'end_time', 0)
            ch_text = " ".join([
                getattr(t, 'text', t.get('text', '') if isinstance(t, dict) else str(t))
                for t in transcript
                if start <= (getattr(t, 'start', t.get('start', 0) if isinstance(t, dict) else 0)) < end
            ])
            text_blocks.append(f"### {ch_title}\n{ch_text}\n")
    else:
        text_blocks.append(" ".join([
            getattr(t, 'text', t.get('text', '') if isinstance(t, dict) else str(t))
            for t in transcript
        ]))

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


def ingest_web_source(url: str, depth: str, vault_root: str, target_dir: str) -> str:
    """Ingests Web article content."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', errors='ignore')

    # Basic title extraction
    m_title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    raw_title = m_title.group(1).strip() if m_title else "Web Article"
    clean_title = brain_health.clean_title_str(raw_title)

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


def ingest_file_or_text_source(source: str, input_type: str, depth: str, vault_root: str, target_dir: str) -> str:
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
    dest_dir = target_dir or "02 - Atlas/Tech"

    input_type = detect_input_type(source)

    with NoteLock(source):
        if input_type == "youtube":
            return ingest_youtube_source(source, depth, extract_frames, root, dest_dir)
        elif input_type == "web":
            return ingest_web_source(source, depth, root, dest_dir)
        else:
            return ingest_file_or_text_source(source, input_type, depth, root, dest_dir)


def build_arg_parser() -> argparse.ArgumentParser:
    """CLI argument parser for brain_ingest."""
    parser = argparse.ArgumentParser(
        description="brain_ingest.py - Unified Polymorphic Ingestion & Staging Engine."
    )
    parser.add_argument('source', nargs='?', default=None, help="Input source (YouTube URL, Web URL, file path, or text).")
    parser.add_argument('--depth', choices=['executive', 'sintesi', 'deep', 'approfondimento'], default='executive', help="Processing depth level (default: executive).")
    parser.add_argument('--extract-frames', action='store_true', help="Extract keyframe screenshots for visual YouTube videos.")
    parser.add_argument('--target-dir', default="02 - Atlas/Tech", help="Target permanent directory after GTD approval.")
    parser.add_argument('--process-approvals', action='store_true', help="Process approved [x] or rejected [-] notes in Review Dashboard.md.")
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
