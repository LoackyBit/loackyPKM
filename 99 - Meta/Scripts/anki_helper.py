#!/usr/bin/env python3
"""Anki Helper Module — Flashcard formatting, MathJax delimiter conversion,
AST card extraction, bi-phase semantic ID realignment, and vault-wide audit
(ANKI-01, ANKI-02, ANKI-03, D-01..D-18).
"""

import os
import sys
import re
import difflib
import argparse
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set

# Script directory injection for local module resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import brain_health
import course_hub


# Custom Exception Hierarchy
class AnkiHelperError(Exception):
    """Base exception for Anki helper errors."""
    pass


class AnkiParseError(AnkiHelperError):
    """Raised when an Anki flashcard block contains malformed syntax."""
    pass


class AnkiIntegrityError(AnkiHelperError):
    """Raised when an Anki ID is corrupted, lost, or duplicated during realignment."""
    pass


def get_vault_root(start_path: Optional[str] = None) -> str:
    """Dynamically resolves the root path of the Second Brain vault."""
    return brain_health.get_vault_root(start_path)


def convert_math_to_anki(text: str) -> str:
    """Converts Obsidian math ($...$ and $$...$$) to Anki MathJax ([$]...[/$] and [$$]...[/$$]).
    Enforces single-line compaction, bare pipe escaping (\\vert), and cloze spacing protection (D-05, D-06, D-07).
    """
    # 1. Mask existing Anki mathjax blocks to avoid double conversion
    protected: List[str] = []

    def mask_existing(m: re.Match) -> str:
        protected.append(m.group(0))
        return f"__ANKI_MATH_BLOCK_{len(protected)-1}__"

    masked = re.sub(r'\[\$\$\][\s\S]*?\[/\$\$\]', mask_existing, text)
    masked = re.sub(r'\[\$\][\s\S]*?\[/\$\]', mask_existing, masked)

    # Helper to replace bare pipes with \vert (only adding trailing space if followed by an alpha char)
    def replace_bare_pipes(formula: str) -> str:
        def repl(m: re.Match) -> str:
            idx = m.end()
            if idx < len(formula) and formula[idx].isalpha():
                return r"\vert "
            return r"\vert"
        return re.sub(r'(?<!\\)\|', repl, formula)

    # 2. Display math $$...$$ -> [$$]...[/$$]
    def display_repl(m: re.Match) -> str:
        formula = m.group(1).strip()
        formula = re.sub(r'\s*\n\s*', ' ', formula)
        formula = replace_bare_pipes(formula)
        return f"[$$]{formula}[/$$]"

    masked = re.sub(r'\$\$([\s\S]+?)\$\$', display_repl, masked)

    # 3. Inline math $...$ -> [$]...[/$] (avoiding currency signs and empty $$)
    def inline_repl(m: re.Match) -> str:
        formula = m.group(1).strip()
        formula = re.sub(r'\s*\n\s*', ' ', formula)
        formula = replace_bare_pipes(formula)
        return f"[$]{formula}[/$]"

    masked = re.sub(r'(?<!\$)\$(?!\$)([^\n$]+?)(?<!\$)\$(?!\$)', inline_repl, masked)

    # 4. Unmask protected blocks in reverse order
    for i in range(len(protected) - 1, -1, -1):
        masked = masked.replace(f"__ANKI_MATH_BLOCK_{i}__", protected[i])

    # 5. Cloze spacing protection inside math: { {{c1::...}} } per D-06
    # Ensure spaces between outer curly brackets and cloze tags
    masked = re.sub(r'\{(\{\{c\d+::)', r'{ \1', masked)
    masked = re.sub(r'(\}\})\s*\}', r'\1 }', masked)

    return masked


def format_anki_card(
    concept_name: str,
    course_name: str,
    model: str,
    field1_content: str,
    field2_content: str,
    tags: Optional[List[str]] = None,
    card_id: Optional[int] = None
) -> str:
    """Formats a single atomic Anki card into an Obsidian collapsible callout block
    (D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-12).
    """
    clean_concept = brain_health.clean_title_str(concept_name)
    clean_course = course_hub.sanitize_course_name(course_name).replace(" ", "_") if course_name else "Generale"

    norm_model = model.strip()
    is_cloze = norm_model.lower() == "cloze"
    card_model = "Cloze" if is_cloze else ("Basic" if norm_model.lower() == "basic" else norm_model.capitalize())

    f1_label = "Text" if is_cloze else "Front"
    f2_label = "Extra" if is_cloze else "Back"

    # MathJax conversion on fields
    clean_f1 = convert_math_to_anki(field1_content.strip())
    clean_f2 = convert_math_to_anki(field2_content.strip())

    # Build tags line with hierarchy and underscores (D-12)
    clean_tags: List[str] = []
    if tags:
        for t in tags:
            # Replace whitespace within tag segments with underscore
            formatted_tag = t.strip().replace(" ", "_")
            if formatted_tag:
                clean_tags.append(formatted_tag)
    if not clean_tags:
        clean_tags = [f"{clean_course}::Generale"]
    tag_line = " ".join(clean_tags)

    # Format multi-line fields with blockquote prefix '> '
    f1_lines = clean_f1.splitlines() or [""]
    f2_lines = clean_f2.splitlines() or [""]

    f1_block = [f"> {f1_label}: {f1_lines[0]}"] + [f"> {l}" for l in f1_lines[1:]]
    f2_block = [f"> {f2_label}: {f2_lines[0]}"] + [f"> {l}" for l in f2_lines[1:]]

    lines = [
        f"> [!tip]- Flashcard: {clean_concept}",
        f"> %% TARGET DECK: University::{clean_course} %%",
        "> START",
        f"> {card_model}",
        *f1_block,
        *f2_block,
        f"> Tags: {tag_line}"
    ]
    if card_id is not None:
        lines.append(f"> <!--ID: {card_id}-->")
    lines.append("> END")

    return "\n".join(lines) + "\n"


START_END_PATTERN = re.compile(
    r'^[ \t]*(?:>[ \t]*)?START[ \t]*\n'
    r'^[ \t]*(?:>[ \t]*)?(?P<model>[A-Za-z0-9_-]+)[ \t]*\n'
    r'(?P<inner>(?:(?!^[ \t]*(?:>[ \t]*)?START[ \t]*\n)[\s\S])*?)'
    r'^[ \t]*(?:>[ \t]*)?END[ \t]*$',
    re.MULTILINE
)


def extract_anki_cards_from_text(content: str) -> List[Dict[str, Any]]:
    """Extracts all structured Anki flashcards from note markdown text (D-01, D-04, D-12, D-15, D-16).
    Supports callouts (> [!tip]- Flashcard: ...), variants (> [!question]), and raw unquoted cards.
    """
    cards: List[Dict[str, Any]] = []

    for m in START_END_PATTERN.finditer(content):
        model_raw = m.group("model").strip()
        model = "Cloze" if model_raw.lower() == "cloze" else ("Basic" if model_raw.lower() == "basic" else model_raw.capitalize())
        inner = m.group("inner")
        card_start = m.start()
        card_end = m.end()

        concept_name = ""
        deck = ""

        # Check preceding lines for callout header or TARGET DECK directive
        pre_text = content[:card_start]
        pre_lines = pre_text.splitlines()

        callout_start_pos = None

        # Look backwards up to 8 lines
        search_limit = max(0, len(pre_lines) - 8)
        for i in range(len(pre_lines) - 1, search_limit - 1, -1):
            line = pre_lines[i]

            # Check for TARGET DECK directive
            deck_m = re.match(r'^[ \t]*(?:>[ \t]*)?%%[ \t]*TARGET DECK:[ \t]*(?P<deck>[^\n%]+?)[ \t]*%%[ \t]*$', line)
            if deck_m and not deck:
                deck = deck_m.group("deck").strip()
                continue

            # Check for Callout header
            callout_m = re.match(r'^[ \t]*>[ \t]*\[!(?P<ctype>[a-zA-Z0-9_-]+)\]-?[ \t]*(?:Flashcard:[ \t]*)?(?P<title>[^\n]*)$', line)
            if callout_m:
                callout_title = callout_m.group("title").strip()
                if callout_title:
                    concept_name = brain_health.clean_title_str(callout_title)
                # Calculate character index of this callout header line
                # Sum lengths of all lines up to i plus newlines
                callout_start_pos = sum(len(l) + 1 for l in pre_lines[:i])
                break

            # If line is completely empty or plain non-quote text and not %% line, stop looking backwards
            clean_strip = line.strip()
            if not clean_strip or (not line.startswith(">") and not clean_strip.startswith("%%")):
                break

        # If a callout header was found, expand card span and raw block to include it
        final_start = callout_start_pos if callout_start_pos is not None else card_start
        final_end = card_end
        # Include trailing newline if present
        if final_end < len(content) and content[final_end] == '\n':
            final_end += 1

        raw_block = content[final_start:final_end]

        # Parse fields, tags, ID from inner content
        fields: Dict[str, str] = {}
        curr_field = None
        tags: List[str] = []
        card_id: Optional[int] = None

        for line in inner.splitlines():
            clean_l = re.sub(r'^[ \t]*>[ \t]?', '', line)

            # Check for ID comment
            id_m = re.search(r'<!--ID:[ \t]*(\d+)-->', clean_l)
            if id_m:
                card_id = int(id_m.group(1))
                clean_l = re.sub(r'<!--ID:[ \t]*\d+-->', '', clean_l).strip()
                if not clean_l:
                    continue

            # Check for TARGET DECK in inner
            inner_deck_m = re.search(r'%%[ \t]*TARGET DECK:[ \t]*(?P<deck>[^\n%]+?)[ \t]*%%', clean_l)
            if inner_deck_m and not deck:
                deck = inner_deck_m.group("deck").strip()
                continue

            # Check for Tags line
            tags_m = re.match(r'^[ \t]*Tags:[ \t]*(.*)$', clean_l, re.IGNORECASE)
            if tags_m:
                tags.extend(tags_m.group(1).split())
                continue

            # Check for explicit field labels (Front:, Back:, Text:, Extra:)
            f_m = re.match(r'^(Front|Back|Text|Extra):[ \t]*(.*)$', clean_l, re.IGNORECASE)
            if f_m:
                f_name = f_m.group(1).capitalize()
                f_val = f_m.group(2)
                curr_field = f_name
                fields[curr_field] = f_val
            else:
                if curr_field is not None:
                    if fields[curr_field]:
                        fields[curr_field] += "\n" + clean_l
                    else:
                        fields[curr_field] = clean_l
                else:
                    if clean_l.strip():
                        default_field = "Text" if model.lower() == "cloze" else "Front"
                        curr_field = default_field
                        fields[curr_field] = clean_l

        # Strip fields
        fields = {k: v.strip() for k, v in fields.items()}

        # If concept_name not in callout header, infer from Front/Text
        if not concept_name:
            cand = fields.get("Front") or fields.get("Text") or "Anki Card"
            first_line = cand.splitlines()[0] if cand else "Anki Card"
            # Remove markdown formatting for concept name
            first_line = re.sub(r'[*_`#\[\]]', '', first_line).strip()
            concept_name = brain_health.clean_title_str(first_line[:80])

        cards.append({
            "concept_name": concept_name,
            "deck": deck,
            "model": model,
            "fields": fields,
            "tags": tags,
            "card_id": card_id,
            "raw_block": raw_block,
            "span": (final_start, final_end)
        })

    return cards


def audit_anki_cards(vault_root: Optional[str] = None) -> Dict[str, Any]:
    """Scans all markdown notes in the vault for Anki flashcards,
    detecting total count, synced IDs, duplicate IDs, and decks (D-13, D-15, D-16).
    """
    root = get_vault_root(vault_root)
    total_cards = 0
    synced_cards = 0
    pending_cards = 0
    basic_count = 0
    cloze_count = 0
    decks: Set[str] = set()
    id_locations: Dict[int, List[str]] = {}
    malformed_cards: List[Dict[str, str]] = []

    ignore_dirs = {
        '.git', '.obsidian', '.trash', '.planning',
        '99 - Meta/Template', '99 - Meta/Templates',
        'node_modules', '.agents', '.gemini', '.antigravitycli'
    }

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        if any(rel_dir == ign or rel_dir.startswith(ign + os.sep) or f"{os.sep}{ign}" in rel_dir for ign in ignore_dirs):
            continue

        for f in filenames:
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, f)
            rel_file = os.path.relpath(fpath, root)

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
            except Exception:
                continue

            cards = extract_anki_cards_from_text(content)
            for c in cards:
                total_cards += 1
                if c["model"].lower() == "cloze":
                    cloze_count += 1
                else:
                    basic_count += 1

                if c.get("deck"):
                    decks.add(c["deck"])

                cid = c.get("card_id")
                if cid is not None:
                    synced_cards += 1
                    id_locations.setdefault(cid, []).append(rel_file)
                else:
                    pending_cards += 1

    duplicates = {cid: locs for cid, locs in id_locations.items() if len(locs) > 1}

    return {
        "total_cards": total_cards,
        "synced_cards": synced_cards,
        "pending_cards": pending_cards,
        "basic_count": basic_count,
        "cloze_count": cloze_count,
        "decks": sorted(list(decks)),
        "id_locations": id_locations,
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
        "malformed_count": len(malformed_cards),
        "malformed": malformed_cards
    }


def build_arg_parser() -> argparse.ArgumentParser:
    """Builds argument parser for Anki helper CLI."""
    parser = argparse.ArgumentParser(description="Anki Helper — Flashcard syntax, MathJax conversion & ID preservation.")
    parser.add_argument("--audit", action="store_true", help="Run vault-wide Anki card integrity audit.")
    parser.add_argument("--check-file", type=str, default=None, help="Check Anki cards within a single file.")
    parser.add_argument("--vault-root", type=str, default=None, help="Custom vault root directory.")
    return parser


def main(cli_args: Optional[List[str]] = None) -> int:
    """Main CLI entry point for anki_helper."""
    parser = build_arg_parser()
    args = parser.parse_args(cli_args)
    root = get_vault_root(args.vault_root)

    if args.audit:
        stats = audit_anki_cards(root)
        print("=" * 60)
        print("📇 Anki Flashcards Integrity Audit")
        print("=" * 60)
        print(f"Total Cards: {stats['total_cards']} (Basic: {stats['basic_count']}, Cloze: {stats['cloze_count']})")
        print(f"Synced Cards (with ID): {stats['synced_cards']}")
        print(f"Pending Cards (without ID): {stats['pending_cards']}")
        print(f"Registered Decks ({len(stats['decks'])}):")
        for d in stats['decks']:
            print(f"  • {d}")

        if stats['duplicate_count'] > 0:
            print(f"\n⚠️  WARNING: Found {stats['duplicate_count']} duplicate Anki IDs!")
            for cid, locs in stats['duplicates'].items():
                print(f"  • ID {cid}: {', '.join(locs)}")
            print("=" * 60)
            return 1

        print("=" * 60)
        print("✅ All Anki IDs are unique and consistent.")
        return 0

    if args.check_file:
        fpath = os.path.abspath(args.check_file)
        if not os.path.exists(fpath):
            print(f"File not found: {fpath}", file=sys.stderr)
            return 1
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            cards = extract_anki_cards_from_text(f.read())
        print(f"Found {len(cards)} card(s) in {fpath}:")
        for i, c in enumerate(cards, 1):
            id_str = f"ID: {c['card_id']}" if c['card_id'] else "NO ID"
            deck_str = f"Deck: {c['deck']}" if c['deck'] else "No deck"
            print(f"  {i}. [{c['model']}] {c['concept_name']} ({deck_str}) — {id_str}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

