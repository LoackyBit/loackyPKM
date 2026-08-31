#!/usr/bin/env python3
"""backfill_summaries.py - AI Summary Backfill Pipeline with Atomic JSON Checkpointing.

Extracts and injects concise executive summaries (120-180 characters, max 200) into Obsidian Vault notes.
"""

import os
import sys
import re
import json
import time
import datetime
import argparse
import tempfile
import subprocess
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import brain_health as lint_yaml

CHECKPOINT_FILE = os.path.join("99 - Meta", ".backfill_checkpoint.json")

IGNORE_FOLDERS = {
    '.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode',
    '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy',
    'node_modules', 'tests', '.planning', '99 - Meta', 'Template'
}

class CheckpointManager:
    """Manages persistent JSON checkpointing with atomic replacement for bulk AI synthesis."""
    def __init__(self, root_dir: str = "."):
        self.root_dir = os.path.abspath(root_dir)
        self.checkpoint_path = os.path.join(self.root_dir, CHECKPOINT_FILE)
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "completed": {},
            "stats": {
                "total": 0,
                "processed": 0,
                "skipped": 0,
                "failed": 0,
                "last_run": None
            }
        }

    def is_completed(self, rel_path: str) -> bool:
        return rel_path in self.data["completed"]

    def record_success(self, rel_path: str, summary: str):
        self.data["completed"][rel_path] = {
            "summary": summary,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.data["stats"]["processed"] = len(self.data["completed"])
        self.data["stats"]["last_run"] = datetime.datetime.now().isoformat()
        self._save()

    def _save(self):
        dir_name = os.path.dirname(self.checkpoint_path)
        os.makedirs(dir_name, exist_ok=True)
        with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, encoding='utf-8') as tf:
            json.dump(self.data, tf, indent=2, ensure_ascii=False)
            temp_name = tf.name
        os.replace(temp_name, self.checkpoint_path)

def should_skip_path(rel_path: str) -> bool:
    """Returns True if the file should be excluded from summary backfilling."""
    path_lower = rel_path.lower()
    if '99 - meta/template' in path_lower or 'folder templates' in path_lower:
        return True
    if any(ig in path_lower for ig in ['.git', '.obsidian', '.agents', '.gemini', '.trash']):
        return True
    return False

def get_special_summary(rel_path: str, title: str, body_text: str) -> str | None:
    """Returns deterministic summary for special note types (MOCs, Daily Notes)."""
    path_lower = rel_path.lower()
    filename = os.path.basename(rel_path)
    
    if '01 - map of content' in path_lower or filename.endswith('MOC.md'):
        clean_name = title if title and title != "Untitled" else filename[:-3]
        return f"Indice e mappa concettuale per {clean_name}."
        
    if '04 - calendar' in path_lower or filename.startswith('DailyNote'):
        match = re.search(r'(\d{8}|\d{4}-\d{2}-\d{2})', filename)
        date_str = match.group(1) if match else "del giorno"
        return f"Diario giornaliero e tracciamento delle attività del {date_str}."
        
    return None

def detect_language(text: str) -> str:
    """Simple heuristic to detect Italian vs English text."""
    it_words = {'il', 'la', 'che', 'non', 'sono', 'delle', 'dello', 'nella', 'questo', 'questa', 'come', 'perché', 'perche', 'dati', 'nota', 'corso'}
    en_words = {'the', 'and', 'with', 'from', 'this', 'that', 'which', 'about', 'data', 'using', 'learning', 'guide'}
    
    tokens = set(re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()))
    it_count = len(tokens.intersection(it_words))
    en_count = len(tokens.intersection(en_words))
    
    return "it" if it_count >= en_count else "en"

def build_summary_prompt(title: str, body_text: str, lang: str = "it") -> str:
    """Builds an optimized, concise prompt for AI executive summary generation."""
    truncated = body_text[:3500].strip()
    if lang == "it":
        return f"""Sei un assistente per un Second Brain Obsidian.
Genera un SUMMARY ESECUTIVO per la nota intitolata "{title}".

REGOLE RIGIDE:
1. Lunghezza: MASSIMO 1-2 frasi (tra 120 e 180 caratteri totali, mai oltre 200).
2. Contenuto: Condensa il takeaway principale, la tesi centrale o l'essenza operativa.
3. Stile: Diretto, denso, senza preamboli (MAI iniziare con "Questa nota parla di...", "Il documento illustra...", "Questa nota...").
4. Lingua: Rispondi rigorosamente in ITALIANO.
5. Output: RESTITUISCI ESCLUSIVAMENTE la frase di sintesi, senza virgolette e senza testo aggiuntivo.

TESTO DELLA NOTA:
{truncated}
"""
    else:
        return f"""You are an assistant for an Obsidian Second Brain PKM.
Generate an EXECUTIVE SUMMARY for the note titled "{title}".

STRICT RULES:
1. Length: MAXIMUM 1-2 sentences (between 120 and 180 characters, never exceeding 200).
2. Content: Condense the primary takeaway, central thesis, or operational essence.
3. Style: Direct, high-density, no fluff (NEVER start with "This note is about...", "The document describes...").
4. Language: Respond strictly in ENGLISH.
5. Output: RETURN ONLY the summary sentence, without quotes or conversational text.

NOTE TEXT:
{truncated}
"""

def generate_heuristic_fallback(title: str, body_text: str) -> str:
    """Generates a clean offline fallback summary from note content."""
    lines = body_text.splitlines()
    candidates = []
    
    for l in lines:
        stripped = l.strip()
        if not stripped:
            continue
        if stripped.startswith('#') or stripped.startswith('---') or stripped.startswith('<!--') or stripped.startswith('<') or stripped.startswith('!'):
            continue
        if stripped.startswith('[[') and stripped.endswith(']]'):
            continue
        if stripped.startswith('- [') or stripped.startswith('* ['):
            continue
        # Clean markdown
        cleaned = re.sub(r'\[\[(.*?)\]\]', r'\1', stripped)
        cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', cleaned)
        cleaned = re.sub(r'[*_`>]', '', cleaned).strip()
        cleaned = cleaned.lstrip('- ').lstrip('* ').strip()
        if len(cleaned) >= 20 and not cleaned.startswith('http'):
            candidates.append(cleaned)
            
    if candidates:
        best = candidates[0]
        if len(best) > 197:
            return best[:197] + "..."
        return best
        
    return f"Appunti concettuali e sintesi di studio per {title}." 

def generate_ai_summary(title: str, body_text: str, rel_path: str = "", agy_path: str = "/Users/lorenzo/.local/bin/agy", timeout: int = 30) -> str:
    """Generates an executive summary via agy CLI or heuristic fallback."""
    special = get_special_summary(rel_path, title, body_text)
    if special:
        return special
        
    lang = detect_language(body_text)
    prompt = build_summary_prompt(title, body_text, lang)
    
    # Check if agy binary is available
    agy_cmd = agy_path if os.path.exists(agy_path) else "agy"
    
    env = os.environ.copy()
    env['PATH'] = f"/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env.get('PATH', '')}"
    env['PYTHONUNBUFFERED'] = '1'
    
    try:
        proc = subprocess.run(
            [agy_cmd, "--model", "gemini-3.7-flash-low", "--print", "--dangerously-skip-permissions", "--disable-slash-commands", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        if proc.returncode == 0:
            summary = proc.stdout.strip()
            summary = summary.replace('\n', ' ').strip().strip('"').strip("'")
            # Strip common fluff
            for prefix in ["Questa nota descrive ", "Questa nota illustra ", "Questo appunto ", "This note discusses "]:
                if summary.startswith(prefix):
                    summary = summary[len(prefix):].capitalize()
            if len(summary) > 200:
                summary = summary[:197] + "..."
            if summary:
                return summary
    except Exception:
        pass
        
    return generate_heuristic_fallback(title, body_text)

def inject_summary_into_note(filepath: str, summary_text: str, vault_root: str = ".", execute: bool = False) -> tuple[bool, str]:
    """Injects or updates the summary field in the note's YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    has_frontmatter, frontmatter_text, breadcrumb, body = lint_yaml.split_markdown_note(content)
    yaml_engine = lint_yaml.build_yaml_engine()
    existing_meta = lint_yaml.safe_load_frontmatter(frontmatter_text, yaml_engine) if has_frontmatter else {}
    
    rel_path = os.path.relpath(filepath, vault_root)
    filename = os.path.basename(filepath)
    is_blog = rel_path.startswith("05 - Blog") or "/05 - blog" in rel_path.lower()
    
    cleaned_body, extracted_tags = lint_yaml.strip_isolated_hashtag_lines(body)
    meta = lint_yaml.infer_metadata(rel_path, existing_meta, cleaned_body, filename)
    
    current_tags = meta.get('tags', [])
    if isinstance(current_tags, str):
        current_tags = [t.strip() for t in current_tags.split(',') if t.strip()]
    elif not isinstance(current_tags, list):
        current_tags = []
        
    for et in extracted_tags:
        if et not in current_tags:
            current_tags.append(et)
    meta['tags'] = current_tags
    
    date_val, updated_val = lint_yaml.get_file_dates(filepath, existing_meta)
    meta['date'] = date_val
    meta['updated'] = updated_val
    
    # Set summary
    meta['summary'] = summary_text
    
    canonical_yaml = lint_yaml.format_canonical_frontmatter(meta, is_blog=is_blog)
    new_content = lint_yaml.assemble_markdown_note(canonical_yaml, breadcrumb, cleaned_body)
    
    if content.strip() != new_content.strip():
        if execute:
            dir_name = os.path.dirname(os.path.abspath(filepath))
            with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, encoding='utf-8') as tf:
                tf.write(new_content)
                temp_name = tf.name
            os.replace(temp_name, filepath)
        return True, new_content
        
    return False, content

def main():
    parser = argparse.ArgumentParser(description="Backfill AI executive summaries into Obsidian Vault frontmatter.")
    parser.add_argument('path', nargs='?', default='.', help="Target file or directory path (default: current directory).")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', default=True, help="Preview summary backfilling without modifying files (default).")
    group.add_argument('--execute', action='store_true', help="Apply generated summaries directly to note frontmatter.")
    parser.add_argument('--batch-size', type=int, default=0, help="Maximum number of notes to process in this run (0 = unlimited).")
    parser.add_argument('--delay', type=float, default=0.0, help="Delay in seconds between note synthesis requests.")
    args = parser.parse_args()
    
    vault_root = os.path.abspath(".")
    target_path = os.path.abspath(args.path)
    is_execute = args.execute
    mode_str = "[EXECUTE]" if is_execute else "[DRY-RUN]"
    
    if not os.path.exists(target_path):
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(1)
        
    checkpoint_mgr = CheckpointManager(vault_root)
    
    notes_to_process = []
    if os.path.isfile(target_path):
        if target_path.endswith('.md'):
            rel_path = os.path.relpath(target_path, vault_root)
            if not should_skip_path(rel_path):
                notes_to_process.append((target_path, rel_path))
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')]
            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    fpath = os.path.join(root, file)
                    rel_path = os.path.relpath(fpath, vault_root)
                    if not should_skip_path(rel_path):
                        notes_to_process.append((fpath, rel_path))
                        
    print(f"Discovered {len(notes_to_process)} candidate notes for summary backfill.")
    
    processed_count = 0
    skipped_count = 0
    modified_count = 0
    
    for fpath, rel_path in notes_to_process:
        if args.batch_size > 0 and processed_count >= args.batch_size:
            print(f"Batch size limit ({args.batch_size}) reached.")
            break
            
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        has_fm, fm_text, breadcrumb, body = lint_yaml.split_markdown_note(content)
        existing_meta = lint_yaml.safe_load_frontmatter(fm_text, lint_yaml.build_yaml_engine()) if has_fm else {}
        
        # Check if note already has an authentic summary and is recorded in checkpoint
        existing_summary = existing_meta.get('summary')
        if existing_summary and str(existing_summary).strip() and checkpoint_mgr.is_completed(rel_path):
            skipped_count += 1
            continue
            
        title = existing_meta.get('title') or lint_yaml.clean_title_str(os.path.basename(fpath))
        summary = generate_ai_summary(str(title), body, rel_path=rel_path)
        
        changed, _ = inject_summary_into_note(fpath, summary, vault_root=vault_root, execute=is_execute)
        
        if is_execute:
            checkpoint_mgr.record_success(rel_path, summary)
            
        if changed:
            modified_count += 1
            print(f"{mode_str} {rel_path} -> {summary[:60]}...")
            
        processed_count += 1
        if args.delay > 0:
            time.sleep(args.delay)
            
    print(f"\n{mode_str} Backfill complete. Total scanned: {len(notes_to_process)} | Processed: {processed_count} | Modified: {modified_count} | Skipped (already had summary): {skipped_count}")

if __name__ == '__main__':
    main()
