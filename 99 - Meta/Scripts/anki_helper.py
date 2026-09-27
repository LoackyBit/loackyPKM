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

    # Helper to replace derivative primes with \prime (D-19)
    def replace_primes(formula: str) -> str:
        def prime_repl(m: re.Match) -> str:
            base = m.group(1)
            primes = m.group(2)
            count = len(primes)
            if count == 1:
                return f"{base}^\\prime"
            return f"{base}^{{{'\\prime' * count}}}"
        return re.sub(r'([a-zA-Z0-9_\}\)])(\'+)', prime_repl, formula)

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
        formula = replace_primes(formula)
        formula = replace_bare_pipes(formula)
        return f"[$$]{formula}[/$$]"

    masked = re.sub(r'\$\$([\s\S]+?)\$\$', display_repl, masked)

    # 3. Inline math $...$ -> [$]...[/$] (avoiding currency signs and empty $$)
    def inline_repl(m: re.Match) -> str:
        formula = m.group(1).strip()
        formula = re.sub(r'\s*\n\s*', ' ', formula)
        formula = replace_primes(formula)
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


def replace_primes_in_formula(formula: str) -> str:
    r"""Replaces derivative apostrophes in LaTeX math with ^\prime notation (e.g. f'(x) -> f^\prime(x)).
    Prevents HTML entity mangling (&#039;) and tag collision (#039) in obsidian-to-anki-plugin.
    """
    def prime_repl(m: re.Match) -> str:
        base = m.group(1)
        primes = m.group(2)
        count = len(primes)
        if count == 1:
            return f"{base}^\\prime"
        return f"{base}^{{{'\\prime' * count}}}"
    return re.sub(r'([a-zA-Z0-9_\}\)])(\'+)', prime_repl, formula)


def sanitize_math_derivatives(text: str) -> str:
    r"""Normalizes all LaTeX derivative apostrophes to ^\prime within all math environments
    ($...$, $$...$$, \(...\), \[...\], [$]...[/$], [$$]...[/$$]).
    """
    text = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: f"$${replace_primes_in_formula(m.group(1))}$$", text)
    text = re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: f"\\[{replace_primes_in_formula(m.group(1))}\\]", text)
    text = re.sub(r'\[\$\$\]([\s\S]+?)\[/\$\$\]', lambda m: f"[$$]{replace_primes_in_formula(m.group(1))}[/$$]", text)
    text = re.sub(r'\[\$\]([\s\S]+?)\[/\$\]', lambda m: f"[$]{replace_primes_in_formula(m.group(1))}[/$]", text)
    text = re.sub(r'\\\(([\s\S]+?)\\\)', lambda m: f"\\({replace_primes_in_formula(m.group(1))}\\)", text)
    text = re.sub(r'(?<!\$)\$(?!\$)([^\n$]+?)(?<!\$)\$(?!\$)', lambda m: f"${replace_primes_in_formula(m.group(1))}$", text)
    return text


def sanitize_flashcard_text(block: str) -> str:
    r"""Sanitizes an Anki flashcard block according to official Anki and obsidian-to-anki-plugin standards:
    - Normalizes derivative primes in math mode ($f'(x)$ -> $f^\prime(x)$).
    - Enforces double-colon cloze syntax ({{c1::...}}).
    - Ensures outer curly bracket spacing around clozes.
    - Normalizes bare pipes to \vert in math formulas.
    - Cleans leading '>' quote markers on lines within the %% comment block.
    - Normalizes Model (Basic, Cloze) and Field names (Front:, Back:, Text:, Extra:) casing.
    """
    # 1. Fix single colon in cloze syntax {{c1:...}} -> {{c1::...}}
    block = re.sub(r'\{\{c(\d+):([^\:])', r'{{c\1::\2', block)

    # 2. Spacing protection for outer curly braces around clozes
    block = re.sub(r'\{(\{\{c\d+::)', r'{ \1', block)
    block = re.sub(r'(\}\})\s*\}', r'\1 }', block)

    # 3. Bare pipes in math mode
    def replace_bare_pipes(formula: str) -> str:
        def pipe_repl(m: re.Match) -> str:
            idx = m.end()
            if idx < len(formula) and formula[idx].isalpha():
                return r"\vert "
            return r"\vert"
        return re.sub(r'(?<!\\)\|', pipe_repl, formula)

    # 4. Process math derivatives and bare pipes in all math delimiters
    def math_processor(formula: str) -> str:
        f = replace_primes_in_formula(formula)
        f = replace_bare_pipes(f)
        return f

    block = re.sub(r'\$\$([\s\S]+?)\$\$', lambda m: f"$${math_processor(m.group(1))}$$", block)
    block = re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: f"\\[{math_processor(m.group(1))}\\]", block)
    block = re.sub(r'\[\$\$\]([\s\S]+?)\[/\$\$\]', lambda m: f"[$$]{math_processor(m.group(1))}[/$$]", block)
    block = re.sub(r'\[\$\]([\s\S]+?)\[/\$\]', lambda m: f"[$]{math_processor(m.group(1))}[/$]", block)
    block = re.sub(r'\\\(([\s\S]+?)\\\)', lambda m: f"\\({math_processor(m.group(1))}\\)", block)
    block = re.sub(r'(?<!\$)\$(?!\$)([^\n$]+?)(?<!\$)\$(?!\$)', lambda m: f"${math_processor(m.group(1))}$", block)

    # 5. Clean leading '>' on inner lines (only header has '>')
    lines = block.splitlines()
    cleaned_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped.startswith(">"):
            cleaned_lines.append(line)
            continue
        if stripped.startswith(">"):
            cleaned_lines.append(re.sub(r'^[ \t]*>[ \t]?', '', line))
        else:
            cleaned_lines.append(line)
    block = "\n".join(cleaned_lines)

    # 6. Fix model and field casing
    block = re.sub(r'(?m)^[ \t]*basic[ \t]*$', 'Basic', block)
    block = re.sub(r'(?m)^[ \t]*cloze[ \t]*$', 'Cloze', block)
    block = re.sub(r'(?m)^[ \t]*front:[ \t]*', 'Front: ', block)
    block = re.sub(r'(?m)^[ \t]*back:[ \t]*', 'Back: ', block)
    block = re.sub(r'(?m)^[ \t]*text:[ \t]*', 'Text: ', block)
    block = re.sub(r'(?m)^[ \t]*extra:[ \t]*', 'Extra: ', block)
    block = re.sub(r'(?m)^[ \t]*tags:[ \t]*', 'Tags: ', block)

    return block


def validate_flashcard_text(block: str) -> List[str]:
    """Validates an Anki flashcard block against official Anki specifications.
    Returns a list of error descriptions (empty if valid).
    """
    errors: List[str] = []
    lines = [l.strip().lstrip('>').strip() for l in block.splitlines()]
    joined = "\n".join(lines)

    if "START" not in lines:
        errors.append("Missing START directive")
    if "END" not in lines:
        errors.append("Missing END directive")

    deck_m = re.search(r'TARGET DECK:\s*([^\n%]+)', block)
    if not deck_m or not deck_m.group(1).strip():
        errors.append("Missing or empty TARGET DECK directive")

    model = None
    start_idx = -1
    for i, l in enumerate(lines):
        if l == "START":
            start_idx = i
            break
    if start_idx != -1 and start_idx + 1 < len(lines):
        model_line = lines[start_idx + 1]
        if model_line in ("Basic", "Cloze"):
            model = model_line
        else:
            errors.append(f"Invalid model '{model_line}'. Must be 'Basic' or 'Cloze'")
    else:
        errors.append("Cannot determine note model after START")

    if model == "Basic":
        if not re.search(r'(?:^|\n)\s*Front:', joined):
            errors.append("Missing 'Front:' field for Basic note")
        if not re.search(r'(?:^|\n)\s*Back:', joined):
            errors.append("Missing 'Back:' field for Basic note")
    elif model == "Cloze":
        if not re.search(r'(?:^|\n)\s*Text:', joined):
            errors.append("Missing 'Text:' field for Cloze note")
        else:
            cloze_matches = re.findall(r'\{\{c(\d+)::([\s\S]+?)\}\}', block)
            if not cloze_matches:
                errors.append("Cloze note missing valid {{c1::...}} cloze deletions")
            single_colon = re.findall(r'\{\{c\d+:[^:].*?\}\}', block)
            if single_colon:
                errors.append(f"Found invalid single-colon cloze deletion: {single_colon}")

    # Check math for unescaped primes
    math_blocks = re.findall(r'\$(.+?)\$', block)
    for mb in math_blocks:
        if re.search(r'[a-zA-Z0-9_\}\)]\'', mb):
            errors.append(f"Found unescaped derivative prime in math: '{mb}'. Use ^\\prime instead of '")

    return errors


def sanitize_all_flashcards(content: str) -> str:
    """Finds all Anki flashcard blocks in a markdown document, sanitizes their syntax,
    and updates the content in-place (processing spans in reverse order).
    """
    cards = extract_anki_cards_from_text(content)
    if not cards:
        return content
    cards_sorted = sorted(cards, key=lambda c: c["span"][0], reverse=True)
    res = content
    for c in cards_sorted:
        start, end = c["span"]
        sanitized = sanitize_flashcard_text(c["raw_block"])
        res = res[:start] + sanitized + res[end:]
    return res


def format_anki_card(
    concept_name: str,
    course_name: str,
    model: str,
    field1_content: str,
    field2_content: str,
    tags: Optional[List[str]] = None,
    card_id: Optional[int] = None,
    note_title: Optional[str] = None
) -> str:
    """Formats a single atomic Anki card into an Obsidian collapsible callout block
    (D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-12).
    Supports hierarchical subdecks per note (TARGET DECK: University::<Course>::<Note Title>).
    """
    clean_concept = brain_health.clean_title_str(concept_name)
    if course_name:
        raw_course = course_name.strip()
        if raw_course.startswith("University::"):
            raw_course = raw_course[12:].strip()
        clean_course = re.sub(r'[\r\n\t]', ' ', raw_course).strip() if raw_course else "Generale"
    else:
        clean_course = "Generale"

    if note_title:
        clean_note = note_title.strip()
        if not clean_course.endswith(f"::{clean_note}") and clean_course != clean_note:
            target_deck = f"University::{clean_course}::{clean_note}"
        else:
            target_deck = f"University::{clean_course}"
    else:
        target_deck = f"University::{clean_course}"

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
        clean_course_tag = clean_course.split("::")[0].replace(" ", "_").replace("(", "").replace(")", "")
        clean_tags = [f"University::{clean_course_tag}::Generale"]
    tag_line = " ".join(clean_tags)

    # Format multi-line fields without blockquote prefix (only callout header has '>')
    f1_lines = clean_f1.splitlines() or [""]
    f2_lines = clean_f2.splitlines() or [""]

    f1_block = [f"{f1_label}: {f1_lines[0]}"] + [f"{l}" for l in f1_lines[1:]]
    f2_block = [f"{f2_label}: {f2_lines[0]}"] + [f"{l}" for l in f2_lines[1:]]

    lines = [
        f"> [!tip]- Flashcard: {clean_concept}",
        "%%",
        f"TARGET DECK: {target_deck}",
        "START",
        f"{card_model}",
        *f1_block,
        *f2_block,
        f"Tags: {tag_line}"
    ]
    if card_id is not None:
        lines.append(f"<!--ID: {card_id}-->")
    lines.append("END")
    lines.append("%%")

    return "\n".join(lines) + "\n"


def update_note_flashcard_subdecks(content: str, note_title: str, course_name: Optional[str] = None) -> str:
    """Ensures all Anki flashcard blocks in a note use a hierarchical subdeck named after the note title:
    TARGET DECK: University::<Course>::<Note Title>
    Preserves all existing <!--ID: ...--> comments, fields, formatting, and tags.
    """
    clean_note = note_title.strip() if note_title else ""
    if not clean_note:
        return content

    def repl(m: re.Match) -> str:
        lead = m.group("lead") or ""
        deck = m.group("deck").strip()
        trail = m.group("trail") or ""

        # Normalize University prefix
        if not deck.startswith("University::"):
            if deck.startswith("University"):
                deck_inner = deck[10:].lstrip(':').strip()
                deck = f"University::{deck_inner}" if deck_inner else f"University::{course_name.strip() if course_name else 'Generale'}"
            else:
                deck = f"University::{deck}"

        # If it already ends with ::{clean_note}, return as is
        if deck.endswith(f"::{clean_note}"):
            return f"{lead}TARGET DECK: {deck}{trail}"

        # If course_name is explicitly provided and deck is just University:: or University::Generale
        if course_name and deck in ("University::", "University::Generale"):
            deck = f"University::{course_name.strip()}"

        new_deck = f"{deck}::{clean_note}"
        return f"{lead}TARGET DECK: {new_deck}{trail}"

    pattern = re.compile(
        r'^(?P<lead>[ \t]*(?:>[ \t]*)?(?:%%[ \t]*)?)TARGET DECK:[ \t]*(?P<deck>[^\n%]+?)(?P<trail>(?:[ \t]*%%)?[ \t]*)$',
        re.MULTILINE
    )
    return pattern.sub(repl, content)


def update_file_flashcard_subdecks(file_path: str, course_name: Optional[str] = None) -> bool:
    """Updates all TARGET DECK lines in a markdown file to include note title subdeck.
    Returns True if file was modified, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Determine note title: from frontmatter 'title:' or file basename without extension
    title = None
    m_title = re.search(r'(?m)^title:\s*["\']?(.*?)["\']?\s*$', content[:2000])
    if m_title:
        title = m_title.group(1).strip()
    if not title:
        title = Path(file_path).stem

    updated = update_note_flashcard_subdecks(content, title, course_name=course_name)
    if updated != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


START_END_PATTERN = re.compile(
    r'^[ \t]*(?:>[ \t]*)?START[ \t]*\n'
    r'^[ \t]*(?:>[ \t]*)?(?P<model>[A-Za-z0-9_-]+)[ \t]*\n'
    r'(?P<inner>(?:(?!^[ \t]*(?:>[ \t]*)?START[ \t]*\n)[\s\S])*?)'
    r'^[ \t]*(?:>[ \t]*)?END[ \t]*(?:%%)?[ \t]*$',
    re.MULTILINE
)


def extract_anki_cards_from_text(content: str) -> List[Dict[str, Any]]:
    """Extracts all structured Anki flashcards from note markdown text (D-01, D-04, D-12, D-15, D-16).
    Supports callouts (> [!tip]- Flashcard: ...), variants (> [!question]), multi-line Obsidian comments (%% ... %%),
    and raw unquoted cards.
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
            clean_strip = line.strip()

            # Check for TARGET DECK directive
            deck_m = re.match(r'^[ \t]*(?:>[ \t]*)?(?:%%[ \t]*)?TARGET DECK:[ \t]*(?P<deck>[^\n%]+?)(?:[ \t]*%%)?[ \t]*$', line)
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
                callout_start_pos = sum(len(l) + 1 for l in pre_lines[:i])
                break

            if clean_strip in ('', '%%') or 'TARGET DECK:' in line or line.startswith(">"):
                continue
            break

        # If a callout header was found, expand card span and raw block to include it
        final_start = callout_start_pos if callout_start_pos is not None else card_start
        final_end = card_end

        # Check if following line is closing %%
        post_text = content[card_end:]
        close_m = re.match(r'^[ \t]*\n[ \t]*%%[ \t]*', post_text)
        if close_m:
            final_end = card_end + close_m.end()

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


def reinject_anki_cards(original_content: str, new_content: str) -> str:
    """Realigns pre-existing Anki card IDs onto newly generated cards using bi-phase matching (ANKI-03, D-14).
    Phase 1: Exact concept name match.
    Phase 2: difflib SequenceMatcher similarity (>= 0.65) on Front/Text field.
    Appends unmatched legacy cards with IDs in an appendix block to prevent data loss.
    """
    orig_cards = extract_anki_cards_from_text(original_content)
    new_cards = extract_anki_cards_from_text(new_content)

    if not orig_cards or not new_cards:
        return new_content

    # Pool of original cards that have an ID
    id_pool = [c for c in orig_cards if c.get("card_id") is not None]
    if not id_pool:
        return new_content

    matched_orig_ids: Set[int] = set()
    replacements: List[Tuple[Tuple[int, int], str]] = []

    for n_card in new_cards:
        norm_new_concept = re.sub(r'\s+', ' ', n_card["concept_name"].lower()).strip()
        matched_orig = None

        # 1. Exact Concept Match
        for o_card in id_pool:
            if o_card["card_id"] in matched_orig_ids:
                continue
            norm_orig_concept = re.sub(r'\s+', ' ', o_card["concept_name"].lower()).strip()
            if norm_new_concept == norm_orig_concept:
                matched_orig = o_card
                break

        # 2. Fuzzy Text Match on Front/Text
        if not matched_orig:
            n_text = n_card["fields"].get("Front") or n_card["fields"].get("Text") or ""
            best_ratio = 0.0
            best_cand = None
            for o_card in id_pool:
                if o_card["card_id"] in matched_orig_ids:
                    continue
                o_text = o_card["fields"].get("Front") or o_card["fields"].get("Text") or ""
                ratio = difflib.SequenceMatcher(None, o_text, n_text).ratio()
                if ratio > best_ratio and ratio >= 0.65:
                    best_ratio = ratio
                    best_cand = o_card
            matched_orig = best_cand

        # If matched, transplant the ID comment right before "> END" or "END"
        if matched_orig and matched_orig.get("card_id"):
            matched_id = matched_orig["card_id"]
            matched_orig_ids.add(matched_id)
            raw = n_card["raw_block"]
            # Remove existing ID comment if any
            raw = re.sub(r'^[ \t]*(?:>[ \t]*)?<!--ID:[ \t]*\d+-->\n?', '', raw, flags=re.MULTILINE)

            # Inject before END line
            def inject_id(m: re.Match) -> str:
                end_line = m.group(0)
                prefix = "> " if end_line.lstrip().startswith(">") else ""
                return f"{prefix}<!--ID: {matched_id}-->\n{end_line}"

            updated_raw = re.sub(r'^[ \t]*(?:>[ \t]*)?END[ \t]*$', inject_id, raw, flags=re.MULTILINE)
            replacements.append((n_card["span"], updated_raw))

    # Apply span replacements in reverse order
    realigned = new_content
    for span, repl in sorted(replacements, key=lambda x: x[0][0], reverse=True):
        realigned = realigned[:span[0]] + repl + realigned[span[1]:]

    # Preserve unmatched orphan cards with IDs in an appendix (D-14)
    orphans = [c for c in id_pool if c["card_id"] not in matched_orig_ids]
    if orphans:
        appendix_lines = ["\n\n## Flashcard Archiviate (Preservazione ID Anki)\n"]
        for o in orphans:
            appendix_lines.append(o["raw_block"].strip() + "\n")
        realigned = realigned.rstrip() + "\n" + "\n".join(appendix_lines)

    return realigned


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
    parser.add_argument("--update-subdecks", type=str, default=None, help="Update TARGET DECK in file to include note title subdeck.")
    parser.add_argument("--update-all-subdecks", action="store_true", help="Update TARGET DECK across all vault notes to include note title subdecks.")
    parser.add_argument("--course", type=str, default=None, help="Course name to use when updating subdecks.")
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

    if args.update_subdecks:
        target_file = os.path.abspath(args.update_subdecks)
        if not os.path.exists(target_file):
            print(f"File not found: {target_file}", file=sys.stderr)
            return 1
        changed = update_file_flashcard_subdecks(target_file, course_name=args.course)
        if changed:
            print(f"✅ Updated flashcard subdecks in: {target_file}")
        else:
            print(f"ℹ️  No changes needed in: {target_file}")
        return 0

    if args.update_all_subdecks:
        modified_count = 0
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
                if update_file_flashcard_subdecks(fpath, course_name=args.course):
                    modified_count += 1
                    print(f"  • Updated subdecks in: {os.path.relpath(fpath, root)}")
        print(f"✅ Vault subdecks update complete: {modified_count} file(s) modified.")
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

