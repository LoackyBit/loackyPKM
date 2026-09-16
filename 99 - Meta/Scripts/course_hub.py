#!/usr/bin/env python3
"""course_hub.py — Course Hub & Static PACRAR Matrix Management Engine for Obsidian Vault.

Provides CLI and programmatic interfaces for:
- Initializing university Course Hub MOCs in 01 - Map of Content/<Course> MOC.md (PACRAR-01)
- Creating dedicated course folders in 02 - Atlas/Education & Learning/University/<Course>/ (D-01)
- Auto-registering Course Hubs in 01 - Map of Content/University.md (D-12)
- Managing static Markdown PACRAR matrices with Append & Preserve non-destructive updates (PACRAR-02, PACRAR-03)
"""

import argparse
import datetime
import logging
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure Scripts directory is on sys.path for sibling imports
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import brain_health

logger = logging.getLogger("course_hub")

PACRAR_COLS = ["P", "A", "C", "R", "A", "R"]
RE_TABLE_HEADER = re.compile(
    r"^\s*\|\s*Argomento\s*\|\s*P\s*\|\s*A\s*\|\s*C\s*\|\s*R\s*\|\s*A\s*\|\s*R\s*\|\s*$",
    re.IGNORECASE,
)
RE_TABLE_ROW = re.compile(
    r"^\s*\|\s*(?P<arg>[^|]+)\s*\|\s*(?P<p>\[[ x\-]\])\s*\|\s*(?P<a>\[[ x\-]\])\s*\|\s*(?P<c>\[[ x\-]\])\s*\|\s*(?P<r1>\[[ x\-]\])\s*\|\s*(?P<a2>\[[ x\-]\])\s*\|\s*(?P<r2>\[[ x\-]\])\s*\|\s*$",
    re.IGNORECASE,
)
RE_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")
VALID_CHECKBOX_STATES = {"[ ]", "[-]", "[x]"}


def sanitize_course_name(course_name: str) -> str:
    """Sanitizes course name removing path traversal and illegal filesystem characters (T-13-01).

    Raises ValueError if the resulting name is empty or invalid.
    """
    if not course_name or not isinstance(course_name, str):
        raise ValueError("Course name must be a non-empty string.")

    # Strip HTML tags
    cleaned = re.sub(r"<[^>]+>", "", course_name)
    # Remove path traversal sequences
    cleaned = cleaned.replace("..", "").replace("/", "").replace("\\", "")
    # Remove illegal characters for files/markdown tables: : * ? " < > |
    cleaned = re.sub(r'[:*?"<>|]', "", cleaned)
    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    # Apply intelligent Title Case normalization
    cleaned = brain_health.clean_title_str(cleaned)

    if not cleaned:
        raise ValueError(f"Invalid course name '{course_name}' resulted in an empty string.")

    return cleaned


def natural_sort_key(title: str) -> List[Union[int, str]]:
    """Natural numeric sorting for course lessons (e.g. '01 - Lezione', '10 - Lezione') per D-10."""
    clean = re.sub(r"^\[\[|\]\]$", "", title).strip()
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", clean)]


def atomic_write_file(filepath: str, content: str) -> None:
    """Safely writes content to target file via temporary file and atomic replace (T-13-02)."""
    dir_name = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(dir_name, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
        tf.write(content)
        temp_name = tf.name
    os.replace(temp_name, filepath)


def split_table_row_cells(line: str) -> List[str]:
    r"""Splits a markdown table row by '|' ignoring pipes inside [[...]] wikilinks and escaped pipes \|."""
    cells = []
    current = []
    inside_link = False
    for i, char in enumerate(line):
        if char == "[" and i + 1 < len(line) and line[i + 1] == "[":
            inside_link = True
        elif char == "]" and i > 0 and line[i - 1] == "]":
            inside_link = False

        if char == "|" and not inside_link and (i == 0 or line[i - 1] != "\\"):
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def _escape_pipes_outside_wikilinks(text: str) -> str:
    """Escapes '|' characters outside [[...]] to avoid corrupting Markdown table layout (T-13-03)."""
    result = []
    inside_link = False
    for i, char in enumerate(text):
        if char == "[" and i + 1 < len(text) and text[i + 1] == "[":
            inside_link = True
        elif char == "]" and i > 0 and text[i - 1] == "]":
            inside_link = False

        if char == "|" and not inside_link and (i == 0 or text[i - 1] != "\\"):
            result.append("\\|")
        else:
            result.append(char)
    return "".join(result)


def parse_pacrar_table(body_lines: List[str]) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Parses PACRAR table from markdown body lines per D-05, D-07, D-09.

    Returns (start_idx, end_idx, rows) where rows is a list of dicts with:
    {'key': lookup_key, 'argomento': raw_arg, 'states': [p, a, c, r, a, r]}.
    """
    start_idx = -1
    for i, line in enumerate(body_lines):
        if RE_TABLE_HEADER.match(line.strip()):
            start_idx = i
            break

    if start_idx == -1:
        return -1, -1, []

    idx = start_idx + 1
    # Check if next line is divider | :--- | :---: | ...
    if idx < len(body_lines) and re.match(r"^\s*\|\s*:?-+:?\s*\|", body_lines[idx]):
        idx += 1

    rows = []
    while idx < len(body_lines):
        line = body_lines[idx].strip()
        if not line.startswith("|") or line == "":
            break

        cells = split_table_row_cells(line)
        if len(cells) >= 7:
            arg = cells[0]
            checkboxes = cells[1:7]
            states = []
            for cb in checkboxes:
                cb_clean = cb.strip()
                if cb_clean in VALID_CHECKBOX_STATES:
                    states.append(cb_clean)
                else:
                    states.append("[ ]")
            while len(states) < 6:
                states.append("[ ]")

            # Extract lookup key: if wikilink target, use stripped lowercase target; else lowercase arg
            m = RE_WIKILINK.search(arg)
            if m:
                key = m.group(1).strip().lower()
            else:
                key = arg.strip().lower()

            rows.append({
                "key": key,
                "argomento": arg,
                "states": states
            })
        idx += 1

    end_idx = idx
    return start_idx, end_idx, rows


def merge_lessons_into_rows(existing_rows: List[Dict[str, Any]], lesson_titles: List[str]) -> List[Dict[str, Any]]:
    """Performs non-destructive Append & Preserve merge of course lessons (D-07, D-08, D-09, D-10).

    Preserves 100% of existing checkbox ticks and manual unwritten lesson rows.
    """
    existing_by_key: Dict[str, Dict[str, Any]] = {}
    for r in existing_rows:
        existing_by_key[r["key"]] = r

    seen_keys = set()
    merged: List[Dict[str, Any]] = []

    for title in lesson_titles:
        clean = brain_health.clean_title_str(title)
        key = clean.lower()
        seen_keys.add(key)
        target_link = f"[[{clean}]]"

        if key in existing_by_key:
            # Preserve existing row (including 100% of custom checkbox states and manual aliases)
            merged.append(existing_by_key[key])
        else:
            # New lesson row
            merged.append({
                "key": key,
                "argomento": target_link,
                "states": ["[ ]"] * 6
            })

    # Preserve manual unwritten rows (D-08)
    for key, r in existing_by_key.items():
        if key not in seen_keys:
            merged.append(r)

    # Sort using Natural Numeric Sort
    merged.sort(key=lambda r: natural_sort_key(r.get("argomento", "")))
    return merged


def format_pacrar_table(rows: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    """Formats PACRAR table rows into clean GFM Markdown lines per D-05 and T-13-03."""
    lines = [
        "| Argomento | P | A | C | R | A | R |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    if not rows:
        return lines

    # Sort rows using Natural Numeric Sort
    sorted_rows = sorted(rows, key=lambda r: natural_sort_key(r.get("argomento", "")))

    for r in sorted_rows:
        arg = r.get("argomento", "").strip()
        escaped_arg = _escape_pipes_outside_wikilinks(arg)
        states = r.get("states", ["[ ]"] * 6)
        if len(states) < 6:
            states = states + ["[ ]"] * (6 - len(states))
        line = f"| {escaped_arg} | {states[0]} | {states[1]} | {states[2]} | {states[3]} | {states[4]} | {states[5]} |"
        lines.append(line)

    return lines


def build_course_moc_content(course_name: str, rows: Optional[List[Dict[str, Any]]] = None) -> str:
    """Generates canonical 10-field frontmatter and body per D-04, D-05, D-13."""
    clean_name = brain_health.clean_title_str(course_name)
    now_date = datetime.date.today().isoformat()
    now_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    metadata = {
        "status": "permanent",
        "type": "moc",
        "area": "education",
        "related": ['[[University]]'],
        "aliases": [],
        "source": "original",
        "title": f"{clean_name} MOC",
        "date": now_date,
        "updated": now_updated,
        "tags": ["education/university", "education/moc"],
        "summary": f"Hub di corso universitario e matrice di avanzamento dello studio PACRAR per {clean_name}."
    }

    canonical_fm = brain_health.format_canonical_frontmatter(metadata, is_blog=False)
    breadcrumb = f"[[Home MOC|Home]] / [[University|University MOC]] / [[{clean_name} MOC]]"

    table_lines = format_pacrar_table(rows or [])
    table_block = "\n".join(table_lines)

    body = f"""# {clean_name} — Course Hub & Matrice PACRAR

## Informazioni Corso
- **Docente:** [Nome Docente]
- **CFU:** [CFU]
- **Materiali & Testi:** [Testi consigliati o link slide]
- **Cartella Vault:** `02 - Atlas/Education & Learning/University/{clean_name}/`

## Matrice PACRAR

<div class="pacrar-progress-widget" data-course="{clean_name}"></div>

{table_block}

## Formulari & Risorse Chiave
- Nessuna risorsa ancora collegata."""

    return brain_health.assemble_markdown_note(canonical_fm, breadcrumb, body)


def init_course(course_name: str, vault_root: Optional[str] = None, force: bool = False) -> bool:
    """Initializes university Course Hub MOC and Atlas directory (D-01, D-02, D-03, D-04, D-12, D-13).

    Returns True if created/updated, False if skipped due to existing MOC without force.
    """
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    clean_name = sanitize_course_name(course_name)

    moc_path = os.path.join(vault_root, "01 - Map of Content", f"{clean_name} MOC.md")
    course_dir = os.path.join(vault_root, "02 - Atlas", "Education & Learning", "University", clean_name)

    # Security check: resolve paths to ensure no folder escape (T-13-01)
    vault_path_obj = Path(vault_root).resolve()
    moc_path_obj = Path(moc_path).resolve()
    course_dir_obj = Path(course_dir).resolve()

    if not moc_path_obj.is_relative_to(vault_path_obj) or not course_dir_obj.is_relative_to(vault_path_obj):
        raise ValueError(f"Security error: Course path escaped vault boundaries for '{course_name}'.")

    if os.path.exists(moc_path) and not force:
        logger.warning("Hub per '%s' già esistente in '%s'. Nessuna modifica apportata.", clean_name, moc_path)
        return False

    # Create Atlas permanent folder
    os.makedirs(course_dir, exist_ok=True)

    # Build and write MOC
    content = build_course_moc_content(clean_name)
    atomic_write_file(moc_path, content)
    logger.info("Course Hub MOC creato in '%s'.", moc_path)

    # Register in University.md
    register_in_university_moc(clean_name, vault_root=vault_root)

    return True


def ensure_course_hub(course_name: str, vault_root: Optional[str] = None) -> bool:
    """Ensures Course Hub MOC, Atlas folder, and University.md registration exist (idempotent)."""
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    clean_name = sanitize_course_name(course_name)
    moc_path = os.path.join(vault_root, "01 - Map of Content", f"{clean_name} MOC.md")
    course_dir = os.path.join(vault_root, "02 - Atlas", "Education & Learning", "University", clean_name)

    os.makedirs(course_dir, exist_ok=True)

    if not os.path.exists(moc_path):
        init_course(clean_name, vault_root=vault_root, force=False)
    else:
        register_in_university_moc(clean_name, vault_root=vault_root)

    return True


def register_in_university_moc(course_name: str, vault_root: Optional[str] = None) -> bool:
    """Registers course link in 01 - Map of Content/University.md under ## Corsi Universitari (D-11, D-12).

    Idempotent: preserves all existing content and avoids duplicating links.
    """
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    uni_path = os.path.join(vault_root, "01 - Map of Content", "University.md")
    if not os.path.exists(uni_path):
        logger.warning("File University.md non trovato in '%s'. Impossibile registrare il corso.", uni_path)
        return False

    with open(uni_path, "r", encoding="utf-8") as f:
        content = f.read()

    clean_name = brain_health.clean_title_str(course_name)
    target_link = f"[[{clean_name} MOC]]"

    # If link is already present, return True
    if target_link in content:
        return True

    has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)

    section_header = "## Corsi Universitari"
    item_line = f"- {target_link}"

    if section_header in body:
        # Section exists: insert in alphabetical order or append to section list
        lines = body.split("\n")
        header_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == section_header:
                header_idx = i
                break

        # Collect existing course items under this header
        insert_idx = header_idx + 1
        course_items = []
        next_section_idx = len(lines)

        for j in range(header_idx + 1, len(lines)):
            line_str = lines[j]
            if line_str.startswith("## ") or line_str.startswith("# ") or line_str == "---":
                next_section_idx = j
                break
            if line_str.strip().startswith("- [["):
                course_items.append((j, line_str.strip()))

        # Determine insertion point
        inserted = False
        for line_j, item_str in course_items:
            if item_str.lower() > item_line.lower():
                lines.insert(line_j, item_line)
                inserted = True
                break
        if not inserted:
            lines.insert(next_section_idx, item_line)

        body = "\n".join(lines)
    else:
        # Section does not exist: insert before ## Collegamenti or before final separator
        lines = body.split("\n")
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.strip() == "## Collegamenti" or (line.strip() == "---" and i > len(lines) // 2):
                insert_idx = i
                break

        new_section_block = f"\n{section_header}\n{item_line}\n"
        lines.insert(insert_idx, new_section_block)
        body = "\n".join(lines)

    new_content = brain_health.assemble_markdown_note(fm_text, breadcrumb, body)
    atomic_write_file(uni_path, new_content)
    logger.info("Corso '%s' registrato con successo in '%s'.", clean_name, uni_path)
    return True


def sync_course_hub(course_name: str, vault_root: Optional[str] = None) -> bool:
    """Synchronizes course lessons from disk into the PACRAR matrix of the Course Hub MOC.

    Non-destructive (Append & Preserve): preserves all existing checkbox states and manual rows.
    """
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    clean_name = sanitize_course_name(course_name)
    moc_path = os.path.join(vault_root, "01 - Map of Content", f"{clean_name} MOC.md")
    course_dir = os.path.join(vault_root, "02 - Atlas", "Education & Learning", "University", clean_name)

    os.makedirs(course_dir, exist_ok=True)

    if not os.path.exists(moc_path):
        init_course(clean_name, vault_root=vault_root, force=False)

    # Gather lesson files from course directory
    lesson_titles = []
    if os.path.isdir(course_dir):
        for fname in os.listdir(course_dir):
            if fname.endswith(".md") and not fname.startswith("."):
                lesson_titles.append(fname[:-3])

    with open(moc_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)
    yaml_engine = brain_health.build_yaml_engine()
    meta = brain_health.safe_load_frontmatter(fm_text, yaml_engine) if has_fm else {}

    body_lines = body.split("\n")
    start_idx, end_idx, existing_rows = parse_pacrar_table(body_lines)

    merged_rows = merge_lessons_into_rows(existing_rows, lesson_titles)
    table_lines = format_pacrar_table(merged_rows)

    if start_idx != -1:
        new_body_lines = body_lines[:start_idx] + table_lines + body_lines[end_idx:]
    else:
        # If no table header found, inject under ## Matrice PACRAR or at end
        pacrar_header_idx = -1
        for i, line in enumerate(body_lines):
            if line.strip().lower() == "## matrice pacrar":
                pacrar_header_idx = i
                break
        if pacrar_header_idx != -1:
            widget_line = f'<div class="pacrar-progress-widget" data-course="{clean_name}"></div>'
            new_body_lines = (
                body_lines[: pacrar_header_idx + 1]
                + ["", widget_line, ""]
                + table_lines
                + body_lines[pacrar_header_idx + 1 :]
            )
        else:
            new_body_lines = body_lines + [
                "",
                "## Matrice PACRAR",
                "",
                f'<div class="pacrar-progress-widget" data-course="{clean_name}"></div>',
                "",
            ] + table_lines

    new_body = "\n".join(new_body_lines)
    meta["status"] = meta.get("status", "permanent")
    meta["type"] = "moc"
    meta["area"] = "education"
    meta["updated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if "related" not in meta or not meta["related"]:
        meta["related"] = ['[[University]]']

    canonical_fm = brain_health.format_canonical_frontmatter(meta, is_blog=False)
    final_bc = breadcrumb or f"[[Home MOC|Home]] / [[University|University MOC]] / [[{clean_name} MOC]]"
    new_content = brain_health.assemble_markdown_note(canonical_fm, final_bc, new_body)

    atomic_write_file(moc_path, new_content)
    logger.info("Matrice PACRAR sincronizzata per '%s' con %d lezioni.", clean_name, len(merged_rows))
    return True


def register_lesson(course_name: str, lesson_title: str, vault_root: Optional[str] = None) -> bool:
    """Registers a lesson title into the Course Hub PACRAR matrix (idempotent)."""
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    clean_name = sanitize_course_name(course_name)
    ensure_course_hub(clean_name, vault_root=vault_root)
    return sync_course_hub(clean_name, vault_root=vault_root)


def sync_all_courses(vault_root: Optional[str] = None) -> int:
    """Synchronizes PACRAR tables across all university courses found in the vault."""
    if vault_root is None:
        vault_root = brain_health.get_vault_root()

    uni_dir = os.path.join(vault_root, "02 - Atlas", "Education & Learning", "University")
    synced = 0
    if os.path.isdir(uni_dir):
        for course_folder in os.listdir(uni_dir):
            cpath = os.path.join(uni_dir, course_folder)
            if os.path.isdir(cpath) and not course_folder.startswith("."):
                sync_course_hub(course_folder, vault_root=vault_root)
                synced += 1
    return synced


def main():
    parser = argparse.ArgumentParser(
        description="Course Hub & Static PACRAR Matrix Management Engine for Obsidian PKM."
    )
    parser.add_argument("--init-course", metavar="NOME", help="Initialize university Course Hub MOC and Atlas directory")
    parser.add_argument("--sync-course", metavar="NOME", help="Synchronize PACRAR table for specified course")
    parser.add_argument("--sync-all", action="store_true", help="Synchronize PACRAR tables across all university course hubs")
    parser.add_argument("--vault-root", metavar="DIR", help="Specify custom vault root path")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing Course Hub MOC")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    vault_root = args.vault_root or brain_health.get_vault_root()

    if args.init_course:
        success = init_course(args.init_course, vault_root=vault_root, force=args.force)
        sys.exit(0 if success else 1)
    elif args.sync_course:
        success = sync_course_hub(args.sync_course, vault_root=vault_root)
        sys.exit(0 if success else 1)
    elif args.sync_all:
        count = sync_all_courses(vault_root=vault_root)
        print(f"Sincronizzati {count} Hub di corso universitari.")
        sys.exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
