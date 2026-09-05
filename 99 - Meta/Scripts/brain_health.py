#!/usr/bin/env python3
"""brain_health.py - Unified Governance, AST YAML Linter, Link Auditor & Health Dashboard Engine.

Consolidates and replaces audit_vault.py, lint_yaml.py, tidy_vault.py, and update_dashboard.py
into a single high-performance engine for the Second Brain.
"""

import os
import sys
import re
import datetime
import unicodedata
import subprocess
import argparse
import tempfile
from io import StringIO
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, PlainScalarString

MINOR_WORDS = {
    'di', 'del', 'della', 'dello', 'dei', 'degli', 'delle', 'da', 'dal', 'dalla', 'in', 'su',
    'sul', 'sulla', 'per', 'con', 'a', 'al', 'alla', 'o', 'e', 'ed', 'la', 'il', 'lo', 'i',
    'gli', 'le', 'un', 'uno', 'una', 'to', 'the', 'and', 'of', 'on', 'at', 'for', 'with', 'by',
    'an', 'd', 'l'
}

PRESERVE_UPPER = {
    'MOC', 'AI', 'ENG', 'ITA', 'STEM', 'TIL', 'CS50', 'DNA', 'ENEA', 'NP', 'P', 'II', 'III', 'IV', 'V',
    'VI', 'VII', 'VIII', 'IX', 'X', 'CLI', 'LLM', 'NLP', 'RAG', 'AST', 'API', 'REST', 'GTD', 'PKM',
    'ZSH', 'CSS', 'HTML', 'JS', 'TS', 'SQL', 'UI', 'UX', 'OS', 'URL', 'JSON', 'YAML', 'IDE', 'SDK',
    'HTTP', 'HTTPS', 'TCP', 'IP', 'CPU', 'GPU', 'PACRAR', 'M1', 'M2', 'M3', 'P1', 'P2', 'P3'
}

CONTROLLED_TYPES = {
    'concept', 'video', 'article', 'lecture', 'book', 'project', 'moc', 'journal'
}

CONTROLLED_AREAS = {
    'tech', 'education', 'mentality', 'finance', 'projects', 'meta', 'calendar'
}

VAULT_DIRECTORIES = {
    '01 - Map of Content', '02 - Atlas', '03 - Inbox', '04 - Calendar', '05 - Blog'
}

IGNORE_FILES = {
    'GEMINI.md', 'AGENTS.md', 'README.md', 'SUMMARY.md', 'STATE.md', 'PLAN.md', 'LICENSE'
}

IGNORE_FOLDERS = {
    '.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode',
    '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy',
    'node_modules', 'tests', '.planning', '99 - Meta', 'Template'
}

TAG_HIERARCHY_MAP = {
    # Tech
    'ai': 'tech/ai', 'llm': 'tech/llm', 'rag': 'tech/rag', 'ml': 'tech/ml', 'nlp': 'tech/nlp',
    'python': 'tech/python', 'zsh': 'tech/zsh', 'terminal': 'tech/terminal', 'git': 'tech/git',
    'obsidian': 'tech/obsidian', 'web': 'tech/web', 'javascript': 'tech/web', 'typescript': 'tech/web',
    'frontend': 'tech/web', 'backend': 'tech/backend', 'database': 'tech/database', 'sql': 'tech/sql',
    'security': 'tech/security', 'agent': 'tech/agent', 'prompt': 'tech/prompt',
    'programming': 'tech/programming', 'coding': 'tech/programming', 'hardware': 'tech/hardware',
    'setup': 'tech/setup', 'til': 'tech/til', 'linux': 'tech/linux', 'mac': 'tech/mac',
    'transcript': 'tech/transcript',

    # Education
    'school': 'education/school', 'scuola': 'education/school', 'universita': 'education/university',
    'university': 'education/university', 'cs50': 'education/cs50', 'matematica': 'education/matematica',
    'fisica': 'education/fisica', 'informatica': 'education/informatica', 'storia': 'education/storia',
    'filosofia': 'education/filosofia', 'italiano': 'education/italiano', 'inglese': 'education/inglese',
    'latino': 'education/latino', 'scienze': 'education/scienze', 'arte': 'education/arte',
    'lecture': 'education/lecture', 'lezione': 'education/lecture', 'cornell': 'education/cornell',

    # Finance
    'finance': 'finance/finance', 'finanza': 'finance/finance', 'crypto': 'finance/crypto',
    'bitcoin': 'finance/crypto', 'trading': 'finance/trading', 'investimenti': 'finance/investments',
    'investing': 'finance/investments', 'fisco': 'finance/tax', 'tasse': 'finance/tax',
    'money': 'finance/money', 'business': 'finance/business',

    # Mentality
    'mentality': 'mentality/mindset', 'mindset': 'mentality/mindset', 'crescita': 'mentality/growth',
    'abitudini': 'mentality/habits', 'habits': 'mentality/habits', 'produttivita': 'mentality/productivity',
    'productivity': 'mentality/productivity', 'psicologia': 'mentality/psychology',
    'filosofia-di-vita': 'mentality/philosophy', 'palestra': 'mentality/fitness',
    'fitness': 'mentality/fitness', 'workout': 'mentality/fitness',

    # Calendar
    'daily': 'calendar/daily', 'journal': 'calendar/journal', 'weekly': 'calendar/weekly',
    'monthly': 'calendar/monthly', 'review': 'calendar/review',

    # Meta
    'meta': 'meta/meta', 'template': 'meta/template', 'script': 'meta/script',
    'log': 'meta/log', 'workflow': 'meta/workflow', 'gtd': 'meta/gtd', 'dashboard': 'meta/dashboard',
    'health': 'meta/health'
}


def get_vault_root(start_path: Optional[str] = None) -> str:
    """Dynamically resolves the root path of the Second Brain vault."""
    if start_path:
        current = os.path.abspath(start_path)
        while current != os.path.dirname(current):
            if os.path.isdir(os.path.join(current, ".obsidian")) or (
                os.path.isdir(os.path.join(current, "02 - Atlas")) and os.path.isdir(os.path.join(current, "99 - Meta"))
            ):
                return current
            current = os.path.dirname(current)
        return os.path.abspath(start_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", ".."))


def capitalize_word_with_apostrophe(word: str, is_first: bool) -> str:
    """Capitalizes words containing apostrophes with acronym & minor word preservation."""
    parts = word.split("'")
    formatted_parts = []
    for j, part in enumerate(parts):
        if not part:
            formatted_parts.append("")
            continue
        clean_part = "".join(c for c in part if c.isalnum())
        clean_upper = clean_part.upper()
        clean_lower = clean_part.lower()

        if clean_upper in PRESERVE_UPPER:
            formatted_parts.append(part.upper())
        elif clean_lower in MINOR_WORDS and not (is_first and j == 0):
            formatted_parts.append(part.lower())
        else:
            formatted_parts.append(part.capitalize())
    return "'".join(formatted_parts)


def normalize_title_or_filename(text: str) -> str:
    """SSOT routine normalizing a title or filename string to intelligent Title Case in Unicode NFC.

    Preserves Templater syntax, Italian accented characters (à, è, é, ì, ò, ù, À, È, É, Ì, Ò, Ù),
    uppercase acronyms in PRESERVE_UPPER, and minor words in MINOR_WORDS.
    Sanitizes /, \\, : into ' - ', strips emojis, normalizes typographical apostrophes,
    and replaces forbidden special characters.
    """
    base = text.strip()
    if '<%' in base:
        return base
    if base.endswith('.md'):
        base = base[:-3]

    base = unicodedata.normalize('NFC', base)
    base = base.replace('’', "'").replace('‘', "'")

    for forbidden in ['/', '\\', ':']:
        base = base.replace(forbidden, ' - ')

    clean_chars = []
    for c in base:
        cat = unicodedata.category(c)
        if cat in ('So', 'Cs'):
            continue
        if 0x1F000 <= ord(c) <= 0x1FFFF or 0x2600 <= ord(c) <= 0x27BF:
            continue
        clean_chars.append(c)
    base = "".join(clean_chars)

    for spec in ['+', '?', '!', '(', ')', '[', ']', '_', '.', '|', '*', '"', '<', '>']:
        base = base.replace(spec, ' ')

    base = re.sub(r'\s*-\s*', ' - ', base)
    base = re.sub(r'(\s*-\s*)+', ' - ', base)
    base = ' '.join(base.split()).strip(' -.')

    words = base.split()
    title_words = []
    for i, word in enumerate(words):
        is_first = (i == 0)
        is_last = (i == len(words) - 1)

        if "'" in word:
            title_words.append(capitalize_word_with_apostrophe(word, is_first))
            continue

        clean_word = ''.join(c for c in word if c.isalnum())
        clean_upper = clean_word.upper()
        clean_lower = clean_word.lower()

        if clean_upper in PRESERVE_UPPER:
            title_words.append(word.upper())
        elif clean_lower in MINOR_WORDS and not is_first and not is_last:
            title_words.append(word.lower())
        else:
            has_upper = any(c.isupper() for c in word)
            has_lower = any(c.islower() for c in word)
            if has_upper and has_lower:
                title_words.append(word)
            else:
                title_words.append(word.capitalize())

    res = ' '.join(title_words)
    return unicodedata.normalize('NFC', res)


def clean_filename(filename: str) -> str:
    """Normalizes a filename to Title Case, stripping emojis and special characters while preserving NFC accents."""
    return normalize_title_or_filename(filename)


def clean_title_str(title: str) -> str:
    """Formats string to intelligent Title Case preserving Templater syntax, minor words, and acronyms in NFC."""
    return normalize_title_or_filename(title)


def get_breadcrumbs(filepath: str, clean_title: str) -> str:
    """Generates standard single-line breadcrumb link row."""
    parts = Path(filepath).parts
    if len(parts) < 2:
        return ""

    filename_base = Path(filepath).stem
    if clean_title == "Home MOC" or filename_base == "Home MOC":
        return ""

    path_str = "/".join(parts[:-1])

    if path_str.startswith("02 - Atlas/Finance"):
        parent_area = "[[Finanza MOC|Finance]]"
    elif path_str.startswith("02 - Atlas/Prompt"):
        parent_area = "[[Prompts MOC|Prompt]]"
    elif path_str.startswith("02 - Atlas/Corsi"):
        parent_area = "[[Corsi MOC|Corsi]]"
    elif path_str.startswith("03 - Inbox/School"):
        parent_area = "[[School MOC|School]]"
    elif path_str.startswith("05 - Blog"):
        parent_area = "[[Blog]]"
    elif path_str.startswith("02 - Atlas"):
        area = parts[1] if len(parts) > 2 else "Atlas"
        parent_area = f"[[{area}]]"
    elif path_str.startswith("99 - Meta"):
        area = parts[1] if len(parts) > 2 else "Meta"
        parent_area = f"[[{area}]]"
    elif path_str.startswith("01 - Map of Content"):
        parent_area = "[[Home MOC|Home]]"
        self_link = f"[[{filename_base}|{clean_title}]]" if filename_base != clean_title else f"[[{filename_base}]]"
        return f"{parent_area} / {self_link}"
    elif path_str.startswith("04 - Calendar"):
        parent_area = "[[Calendar]]"
    elif path_str.startswith("03 - Inbox"):
        parent_area = "[[Inbox]]"
    else:
        parent_area = "[[Atlas]]"

    self_link = f"[[{filename_base}|{clean_title}]]" if filename_base != clean_title else f"[[{filename_base}]]"
    return f"[[Home MOC|Home]] / {parent_area} / {self_link}"


def build_yaml_engine() -> ruamel.yaml.YAML:
    """Configures ruamel.yaml instance with RoundTripLoader/Dumper."""
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.width = 4096
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def normalize_tag(tag: str, area: str = 'tech') -> str:
    """Converts flat tag into hierarchical area/topic tag."""
    t = tag.strip().lstrip('#').strip()
    if not t:
        return ''
    t_lower = t.lower()

    if '/' in t_lower:
        parts = [p.strip() for p in t_lower.split('/') if p.strip()]
        return '/'.join(parts)

    if t_lower in TAG_HIERARCHY_MAP:
        return TAG_HIERARCHY_MAP[t_lower]

    valid_area = area if area in CONTROLLED_AREAS else 'tech'
    return f'{valid_area}/{t_lower}'


def strip_isolated_hashtag_lines(body: str) -> Tuple[str, List[str]]:
    """Strips lines consisting solely of hashtags from Markdown body while preserving headings."""
    lines = body.splitlines()
    cleaned_lines = []
    extracted_tags = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
            cleaned_lines.append(line)
            continue

        tokens = stripped.split()
        if tokens and all(tok.startswith('#') and len(tok) > 1 and not tok.startswith('#[') for tok in tokens):
            for tok in tokens:
                clean_t = tok.lstrip('#').strip()
                if clean_t:
                    extracted_tags.append(clean_t)
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines), extracted_tags


def sanitize_style_highlights(text: str) -> str:
    """Strips backticks from HTML <mark> and <font> tags to ensure valid rendering in Obsidian and Quartz."""
    cleaned = re.sub(r'`(<mark\s+style="[^"]*">.*?</mark>)`', r'\1', text)
    cleaned = re.sub(r'`(<font\s+color="[^"]*">.*?</font>)`', r'\1', cleaned)
    return cleaned


def split_markdown_note(content: str) -> Tuple[bool, str, Optional[str], str]:
    """Splits markdown into frontmatter text, breadcrumb line, and body."""
    lines = content.splitlines()
    has_frontmatter = False
    frontmatter_lines = []
    rest_lines = []

    if len(lines) > 0 and lines[0].strip() == '---':
        closing_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == '---':
                closing_idx = idx
                break
        if closing_idx != -1:
            has_frontmatter = True
            frontmatter_lines = lines[1:closing_idx]
            rest_lines = lines[closing_idx + 1:]
        else:
            rest_lines = lines
    else:
        rest_lines = lines

    breadcrumb = None
    body_start_idx = 0
    while body_start_idx < len(rest_lines) and not rest_lines[body_start_idx].strip():
        body_start_idx += 1

    if body_start_idx < len(rest_lines):
        candidate = rest_lines[body_start_idx].strip()
        if candidate.startswith('[[Home MOC') or (candidate.startswith('[[') and ' / ' in candidate):
            breadcrumb = candidate
            body_start_idx += 1

    body_lines = rest_lines[body_start_idx:]
    body_str = '\n'.join(body_lines).lstrip('\n')

    return has_frontmatter, '\n'.join(frontmatter_lines), breadcrumb, body_str


def assemble_markdown_note(frontmatter_yaml: str, breadcrumb: Optional[str], body: str) -> str:
    """Reassembles frontmatter, breadcrumb, and body with single blank line separations."""
    res = f'---\n{frontmatter_yaml}\n---'
    if breadcrumb:
        res += f'\n{breadcrumb}'
    if body.strip():
        res += f'\n\n{body.strip()}'
    return res + '\n'


def safe_load_frontmatter(frontmatter_text: str, yaml_engine: ruamel.yaml.YAML) -> Dict[str, Any]:
    """Safely loads frontmatter with fallback for unquoted wikilinks."""
    if not frontmatter_text or not frontmatter_text.strip():
        return {}
    try:
        parsed = yaml_engine.load(frontmatter_text)
        if parsed and isinstance(parsed, dict):
            return dict(parsed)
    except Exception:
        pass

    sanitized = re.sub(r'\[\[(.*?)\]\]', r'"[[\1]]"', frontmatter_text)
    try:
        parsed = yaml_engine.load(sanitized)
        if parsed and isinstance(parsed, dict):
            return dict(parsed)
    except Exception:
        pass

    metadata = {}
    lines = frontmatter_text.splitlines()
    current_key = None
    list_items = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if (line.startswith('  - ') or line.startswith('    - ') or stripped.startswith('- ')) and current_key:
            item_val = stripped.lstrip('-').strip().strip('"').strip("'")
            list_items.append(item_val)
            metadata[current_key] = list_items
            continue
        match = re.match(r'^([\w_ -]+)\s*:\s*(.*)$', line)
        if match:
            current_key = match.group(1).strip()
            val_part = match.group(2).strip()
            list_items = []
            if not val_part:
                metadata[current_key] = None
            elif '[[' in val_part:
                wikilinks = re.findall(r'\[\[(.*?)\]\]', val_part)
                metadata[current_key] = [f"[[{w.strip()}]]" for w in wikilinks if w.strip()]
            elif val_part.startswith('[') and val_part.endswith(']'):
                items = [item.strip().strip('"').strip("'") for item in val_part[1:-1].split(',')]
                metadata[current_key] = [i for i in items if i]
            else:
                val_part = val_part.strip('"').strip("'")
                if val_part.lower() == 'true':
                    metadata[current_key] = True
                elif val_part.lower() == 'false':
                    metadata[current_key] = False
                else:
                    metadata[current_key] = val_part
    return metadata


def get_file_dates(filepath: str, metadata_existing: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    """Extracts authentic date and updated timestamps from metadata or filesystem."""
    date_val = None
    updated_val = None

    if metadata_existing:
        for k, v in metadata_existing.items():
            k_lower = str(k).lower()
            if k_lower == 'date' and v:
                date_val = str(v).strip()
            elif k_lower in ('updated', 'last modified', 'last_modified') and v:
                updated_val = str(v).strip()

    try:
        stat = os.stat(filepath)
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        try:
            ctime = datetime.datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
    except Exception:
        now = datetime.datetime.now()
        mtime = now
        ctime = now

    if not date_val:
        date_val = ctime.strftime('%Y-%m-%d')
    elif '<%' in date_val:
        pass
    else:
        match = re.match(r'^(\d{4}-\d{2}-\d{2})', date_val)
        if match:
            date_val = match.group(1)
        else:
            date_val = ctime.strftime('%Y-%m-%d')

    if not updated_val:
        updated_val = mtime.strftime('%Y-%m-%dT%H:%M')
    elif '<%' in updated_val:
        pass
    else:
        updated_val = updated_val.replace(' ', 'T')
        match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', updated_val)
        if match:
            updated_val = match.group(1)
        else:
            updated_val = mtime.strftime('%Y-%m-%dT%H:%M')

    return date_val, updated_val


def format_canonical_frontmatter(metadata: Dict[str, Any], is_blog: bool = False) -> str:
    """Formats metadata into canonical 10-field YAML sequence with flow-style arrays."""
    yaml = build_yaml_engine()
    doc = CommentedMap()

    # 1. status (Atlas) or stage + draft (Blog)
    if is_blog:
        doc['stage'] = metadata.get('stage', 'seed 🌱')
        doc['draft'] = bool(metadata.get('draft', True))
    else:
        status_val = metadata.get('status', 'permanent')
        if status_val not in ('draft', 'in-progress', 'permanent', 'reference'):
            status_val = 'permanent'
        doc['status'] = status_val

    # 2. type & 3. area
    doc['type'] = metadata.get('type', 'concept')
    doc['area'] = metadata.get('area', 'tech')

    # 4. related (Flow-style seq of quoted wikilinks)
    related_raw = metadata.get('related', [])
    if isinstance(related_raw, str):
        items = re.findall(r'\[\[(.*?)\]\]', related_raw)
        if items:
            related_raw = [f'[[{i.strip()}]]' for i in items if i.strip()]
        else:
            related_raw = [r.strip() for r in related_raw.split(',') if r.strip()]

    normalized_related = []
    for r in related_raw:
        r_str = str(r).strip().strip('"').strip("'")
        if not r_str:
            continue
        if not r_str.startswith('[['):
            r_str = f'[[{r_str}]]'
        normalized_related.append(DoubleQuotedScalarString(r_str))

    related_seq = CommentedSeq(normalized_related)
    related_seq.fa.set_flow_style()
    doc['related'] = related_seq

    # 5. aliases (Optional)
    if 'aliases' in metadata and metadata['aliases'] is not None:
        aliases_raw = metadata['aliases']
        if isinstance(aliases_raw, str):
            aliases_raw = [a.strip() for a in aliases_raw.split(',') if a.strip()]
        alias_seq = CommentedSeq([DoubleQuotedScalarString(str(a).strip().strip('"')) for a in aliases_raw if str(a).strip()])
        alias_seq.fa.set_flow_style()
        doc['aliases'] = alias_seq

    # 6. source & 7. title
    source_val = metadata.get('source', 'original')
    if not source_val:
        source_val = 'original'
    if str(source_val).startswith(('http://', 'https://')):
        doc['source'] = DoubleQuotedScalarString(str(source_val))
    else:
        doc['source'] = source_val
    doc['title'] = DoubleQuotedScalarString(str(metadata.get('title', '')).strip().strip('"'))

    # 8. date & updated
    doc['date'] = PlainScalarString(str(metadata.get('date', '')))
    if 'updated' in metadata and metadata['updated']:
        doc['updated'] = PlainScalarString(str(metadata['updated']))

    # 9. tags (Flow-style seq)
    tags_raw = metadata.get('tags', [])
    if isinstance(tags_raw, str):
        tags_raw = [t.strip() for t in tags_raw.split(',') if t.strip()]
    normalized_tags = []
    area_val = doc['area']
    for t in tags_raw:
        if not t:
            continue
        norm_t = normalize_tag(str(t), area_val)
        if norm_t and norm_t not in normalized_tags:
            normalized_tags.append(norm_t)

    tags_seq = CommentedSeq(normalized_tags)
    tags_seq.fa.set_flow_style()
    doc['tags'] = tags_seq

    # 10. summary (Quoted string)
    if 'summary' in metadata and metadata['summary']:
        sum_str = str(metadata['summary']).strip().replace('\n', ' ').strip('"').strip("'")
        if sum_str:
            doc['summary'] = DoubleQuotedScalarString(sum_str)

    # 11. Extra optional metadata based on type and staging (e.g. video_url, channel, target_path)
    if 'target_path' in metadata and metadata['target_path']:
        doc['target_path'] = DoubleQuotedScalarString(str(metadata['target_path']).strip().strip('"'))

    type_val = str(doc.get('type', '')).lower()
    if type_val == 'video':
        if 'video_url' in metadata and metadata['video_url']:
            doc['video_url'] = DoubleQuotedScalarString(str(metadata['video_url']).strip().strip('"'))
        if 'channel' in metadata and metadata['channel']:
            doc['channel'] = DoubleQuotedScalarString(str(metadata['channel']).strip().strip('"'))
    elif type_val in ('lecture', 'lesson'):
        if 'subject' in metadata and metadata['subject']:
            doc['subject'] = DoubleQuotedScalarString(str(metadata['subject']).strip().strip('"'))
        if 'professor' in metadata and metadata['professor']:
            doc['professor'] = DoubleQuotedScalarString(str(metadata['professor']).strip().strip('"'))

    stream = StringIO()
    yaml.dump(doc, stream)
    return stream.getvalue().strip()


def is_youtube_url(url: Optional[str]) -> bool:
    """Returns True if string contains a standard YouTube video link."""
    if not url:
        return False
    u = str(url).strip()
    return bool(re.search(r'(https?://)?(www\.)?(youtube\.com/(watch\?|shorts/|live/|embed/|v/)|youtu\.be/)', u, re.IGNORECASE))


def infer_metadata(rel_path: str, existing_meta: Dict[str, Any], body: str, filename: str,
                   force_type: Optional[str] = None, force_area: Optional[str] = None) -> Dict[str, Any]:
    """Infers metadata fields conforming to controlled vocabularies and vault rules."""
    meta = dict(existing_meta) if existing_meta else {}
    path_lower = rel_path.lower()
    is_blog = rel_path.startswith('05 - Blog') or '/05 - blog' in path_lower

    # 1. Area resolution
    if force_area:
        area = force_area
    elif 'macro_area' in meta and meta['macro_area']:
        macro = str(meta['macro_area']).strip().lower()
        if macro in ('school', 'scuola', 'education'):
            area = 'education'
        elif macro in ('tech', 'tecnology', 'technology'):
            area = 'tech'
        elif macro == 'mentality':
            area = 'mentality'
        elif macro in ('finance', 'finanza'):
            area = 'finance'
        elif macro == 'projects':
            area = 'projects'
        elif macro == 'meta':
            area = 'meta'
        elif macro == 'calendar':
            area = 'calendar'
        else:
            area = 'tech'
    elif 'area' in meta and meta['area'] in CONTROLLED_AREAS:
        area = meta['area']
    else:
        if '01 - map of content' in path_lower:
            if any(k in path_lower for k in ['tech', 'ai', 'programmazione']):
                area = 'tech'
            elif any(k in path_lower for k in ['finanza', 'finance', 'soldi']):
                area = 'finance'
            elif any(k in path_lower for k in ['mentality', 'mindset', 'crescita', 'palestra']):
                area = 'mentality'
            elif any(k in path_lower for k in ['corsi', 'scuola', 'education']):
                area = 'education'
            else:
                area = 'meta'
        elif 'education' in path_lower or 'school' in path_lower or 'corsi' in path_lower:
            area = 'education'
        elif 'finance' in path_lower:
            area = 'finance'
        elif 'mentality' in path_lower or 'palestra' in path_lower:
            area = 'mentality'
        elif 'calendar' in path_lower:
            area = 'calendar'
        elif 'meta' in path_lower:
            area = 'meta'
        else:
            area = 'tech'
    meta['area'] = area

    # 2. Type resolution
    if force_type:
        typ = force_type
    elif 'type' in meta and meta['type'] in CONTROLLED_TYPES:
        typ = meta['type']
    else:
        if '01 - map of content' in path_lower or filename.endswith('MOC.md'):
            typ = 'moc'
        elif '04 - calendar' in path_lower or filename.startswith('DailyNote'):
            typ = 'journal'
        elif is_blog:
            typ = 'article'
        elif 'video_url' in meta or is_youtube_url(meta.get('source')) or 'youtube' in path_lower or 'trascrizione' in path_lower or 'trascrizione' in body[:300].lower():
            typ = 'video'
        elif 'lecture' in path_lower or 'cornell' in path_lower or 'sc ' in filename.lower() or 'lezione' in path_lower:
            typ = 'lecture'
        elif 'book' in path_lower or 'libro' in path_lower:
            typ = 'book'
        elif 'project' in path_lower or 'progetto' in path_lower:
            typ = 'project'
        else:
            typ = 'concept'
    meta['type'] = typ

    # 3. Source and Video resolution
    source_val = str(meta.get('source') or '').strip()
    video_val = str(meta.get('video_url') or '').strip()

    if typ == 'video':
        if not video_val and is_youtube_url(source_val):
            video_val = source_val
            meta['video_url'] = video_val
        elif video_val and (not source_val or source_val in ('original', '')):
            source_val = video_val
            meta['source'] = source_val

    if not source_val:
        source_val = video_val if (typ == 'video' and video_val) else 'original'
    meta['source'] = source_val

    # 4. Status / Stage resolution
    if is_blog:
        meta['stage'] = meta.get('stage', 'seed 🌱')
        meta['draft'] = bool(meta.get('draft', True))
        if 'status' in meta:
            del meta['status']
    else:
        if '03 - inbox' in path_lower:
            meta['status'] = 'draft'
        else:
            meta['status'] = meta.get('status', 'permanent')
            if meta['status'] not in ('draft', 'in-progress', 'permanent', 'reference'):
                meta['status'] = 'permanent'

    # 5. Title resolution
    if 'title' not in meta or not meta['title'] or meta['title'] == 'Untitled':
        base_name = filename[:-3] if filename.endswith('.md') else filename
        meta['title'] = clean_title_str(base_name)
    else:
        meta['title'] = clean_title_str(str(meta['title']))

    obsolete_keys = ['macro_area', 'last_modified', 'date created', 'ready', 'cssclasses', 'tags_string']
    if meta.get('type') != 'video':
        obsolete_keys.extend(['video_url', 'channel'])

    for obsolete in obsolete_keys:
        if obsolete in meta:
            del meta[obsolete]

    return meta


def lint_file(filepath: str, vault_root: str = '.', execute: bool = False,
              force_type: Optional[str] = None, force_area: Optional[str] = None) -> Tuple[bool, str]:
    """Lints and standardizes a single markdown file frontmatter and formatting."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    has_frontmatter, frontmatter_text, breadcrumb, body = split_markdown_note(content)
    yaml_engine = build_yaml_engine()
    existing_meta = safe_load_frontmatter(frontmatter_text, yaml_engine) if has_frontmatter else {}

    rel_path = os.path.relpath(filepath, vault_root)
    filename = os.path.basename(filepath)
    is_blog = rel_path.startswith('05 - Blog') or '/05 - blog' in rel_path.lower()

    cleaned_body, extracted_tags = strip_isolated_hashtag_lines(body)
    cleaned_body = sanitize_style_highlights(cleaned_body)

    meta = infer_metadata(rel_path, existing_meta, cleaned_body, filename, force_type, force_area)

    current_tags = meta.get('tags', [])
    if isinstance(current_tags, str):
        current_tags = [t.strip() for t in current_tags.split(',') if t.strip()]
    elif not isinstance(current_tags, list):
        current_tags = []

    for et in extracted_tags:
        if et not in current_tags:
            current_tags.append(et)
    meta['tags'] = current_tags

    date_val, updated_val = get_file_dates(filepath, existing_meta)
    meta['date'] = date_val
    meta['updated'] = updated_val

    canonical_yaml = format_canonical_frontmatter(meta, is_blog=is_blog)

    # Sync breadcrumb
    new_breadcrumb = get_breadcrumbs(rel_path, meta['title'])
    final_breadcrumb = new_breadcrumb if new_breadcrumb else breadcrumb

    new_content = assemble_markdown_note(canonical_yaml, final_breadcrumb, cleaned_body)

    if content.strip() != new_content.strip():
        if execute:
            dir_name = os.path.dirname(os.path.abspath(filepath))
            with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, encoding='utf-8') as tf:
                tf.write(new_content)
                temp_name = tf.name
            os.replace(temp_name, filepath)
        return True, new_content

    return False, content


class VaultHealthAuditor:
    """Graph analyzer and link auditor discovering broken links, forward-references, and orphans."""
    def __init__(self, vault_root: str):
        self.vault_root = os.path.abspath(vault_root)
        self.all_notes: Dict[str, str] = {}
        self.incoming_links: Dict[str, Set[str]] = {}
        self.duplicate_notes: Dict[str, List[str]] = {}
        self.scan_vault()

    def scan_vault(self):
        self.all_notes.clear()
        self.incoming_links.clear()
        self.duplicate_notes.clear()
        for root, dirs, files in os.walk(self.vault_root):
            dirs[:] = sorted([d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')])
            for file in sorted(files):
                if file.endswith('.md') and not file.startswith('.') and file not in IGNORE_FILES:
                    rel = os.path.relpath(os.path.join(root, file), self.vault_root)
                    if not any(rel.startswith(vd) for vd in VAULT_DIRECTORIES) and root == self.vault_root:
                        continue
                    clean_name = file[:-3]
                    if clean_name in self.all_notes:
                        if clean_name not in self.duplicate_notes:
                            self.duplicate_notes[clean_name] = [self.all_notes[clean_name], rel]
                        else:
                            self.duplicate_notes[clean_name].append(rel)
                        continue
                    self.all_notes[clean_name] = rel
                    self.incoming_links[clean_name] = set()

    def audit_file_links(self, rel_path: str, content: str) -> Tuple[List[str], List[str], List[str]]:
        """Audits wiki-links in note body and categorizes into (valid, forward, broken)."""
        link_pattern = re.compile(r'\[\[([^|#\]]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]')

        body = content
        if content.startswith('---'):
            end_fm = content.find('---', 3)
            if end_fm != -1:
                body = content[end_fm + 3:]

        # Strip fenced code blocks (```...``` or ~~~...~~~) and inline code (`...`)
        body = re.sub(r'```[\s\S]*?```', '', body)
        body = re.sub(r'~~~[\s\S]*?~~~', '', body)
        body = re.sub(r'`[^`\n]*`', '', body)

        valid_links = []
        forward_links = []
        broken_links = []
        clean_source = Path(rel_path).stem

        for raw_target in link_pattern.findall(body):
            target = raw_target.strip()
            if not target or target.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.svg', '.gif', '.mp4')):
                continue

            if target in self.all_notes:
                if target != clean_source:
                    valid_links.append(target)
                    if target in self.incoming_links:
                        self.incoming_links[target].add(clean_source)
            else:
                # Forward link heuristic: conceptual Title Cased target planned for future creation
                has_bad_chars = any(c in target for c in ['/', '\\', 'http:', 'https:'])
                if target[0].isupper() and len(target) > 2 and not has_bad_chars:
                    forward_links.append(target)
                else:
                    broken_links.append(target)

        return valid_links, forward_links, broken_links

    def detect_orphans(self) -> List[str]:
        """Identifies notes in 02 - Atlas with 0 incoming links and missing from 01 - Map of Content."""
        orphans = []
        for clean_name, rel_path in self.all_notes.items():
            if rel_path.startswith("02 - Atlas") and not self.incoming_links.get(clean_name):
                orphans.append(rel_path)
        return sorted(orphans)


def generate_health_dashboard(vault_root: str, notes_data: List[Dict[str, Any]], audit_stats: Dict[str, Any]) -> str:
    """Renders the Vault Health Dashboard in 100% static Markdown (no Dataview blocks)."""
    today_iso = datetime.datetime.now().strftime("%Y-%m-%d")
    today_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Staging notes (draft or in-progress)
    staging_notes = [
        n for n in notes_data
        if str(n.get('metadata', {}).get('status', '')).lower() in ('draft', 'in-progress')
        and not n.get('name', '').startswith("Audit Report")
    ]
    staging_notes.sort(key=lambda x: str(x.get('metadata', {}).get('date', '')), reverse=True)

    if staging_notes:
        staging_table = "| Nota | Creazione | Area | Stato |\n|---|---|---|---|\n"
        for n in staging_notes:
            meta = n.get('metadata', {})
            staging_table += f"| [[{n['name']}]] | {meta.get('date', 'N/D')} | {meta.get('area', meta.get('macro_area', 'N/D'))} | `{meta.get('status', 'draft')}` |\n"
    else:
        staging_table = "*Nessuna nota in staging.*"

    # Blog seeds
    blog_seeds = [
        n for n in notes_data
        if n.get('rel_path', '').startswith("05 - Blog")
        and (n.get('metadata', {}).get('draft') is True or any(k in str(n.get('metadata', {}).get('stage', '')) for k in ['seed', 'growing']))
        and n.get('name') != "Index"
    ]
    blog_seeds.sort(key=lambda x: str(x.get('metadata', {}).get('date', '')), reverse=True)

    if blog_seeds:
        blog_table = "| Articolo | Data | Stadio | Stato |\n|---|---|---|---|\n"
        for n in blog_seeds:
            meta = n.get('metadata', {})
            draft_lbl = "Bozza" if meta.get('draft', True) else "Pronto"
            blog_table += f"| [[{n['name']}]] | {meta.get('date', 'N/D')} | {meta.get('stage', 'seed 🌱')} | `{draft_lbl}` |\n"
    else:
        blog_table = "*Nessuna bozza attiva nel blog.*"

    # Recent notes (last 10 non-calendar)
    recent_notes = [
        n for n in notes_data
        if not n.get('rel_path', '').startswith("04 - Calendar")
        and n.get('name') != "Vault Health Dashboard"
    ]
    recent_notes.sort(key=lambda x: x.get('mtime', 0), reverse=True)
    recent_notes = recent_notes[:10]

    recent_table = "| Nota | Ultima Modifica | Area |\n|---|---|---|\n"
    for n in recent_notes:
        mtime_str = datetime.datetime.fromtimestamp(n.get('mtime', 0)).strftime("%Y-%m-%d %H:%M")
        meta = n.get('metadata', {})
        area_str = meta.get('area', meta.get('macro_area', 'N/D'))
        recent_table += f"| [[{n['name']}]] | {mtime_str} | {area_str} |\n"

    duplicate_line = ""
    if audit_stats.get('duplicate_count', 0) > 0:
        duplicate_line = f"\n- **Collisioni Omonime (Note Duplicate):** {audit_stats.get('duplicate_count', 0)}"

    return f"""---
status: permanent
type: moc
area: meta
related: ["[[Home MOC]]", "[[Review Dashboard]]"]
source: original
title: "Vault Health Dashboard"
date: '{today_iso}'
updated: {datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}
tags: [meta/dashboard, meta/health]
summary: "Pannello di controllo statico del Second Brain: monitoraggio dello stato di salute, note in staging, bozze del blog e diagnostica del grafo."
---
[[Home MOC|Home]] / [[Meta]] / [[Vault Health Dashboard]]

# Vault Health Dashboard

Pannello di controllo in **puro Markdown statico** per monitorare la salute del Vault, le note in staging e l'integrità del grafo semantico.

*Ultimo aggiornamento:* `{today_time}`

---

## Metriche Generali del Vault
- **Note Totali:** {audit_stats.get('total_notes', 0)}
- **Note in Staging (Inbox):** {len(staging_notes)}
- **Bozze Blog:** {len(blog_seeds)}
- **Note Orfane:** {audit_stats.get('orphan_count', 0)}
- **Link Interrotti:** {audit_stats.get('broken_link_count', 0)}
- **Forward-Links Pianificati:** {audit_stats.get('forward_link_count', 0)}{duplicate_line}

---

## Note in Staging (Inbox / Bozze)
{staging_table}

---

## Semi del Blog (Bozze Quartz)
{blog_table}

---

## Note Modificate di Recente
{recent_table}

---

## Comandi di Governance
Per eseguire un audit interattivo o applicare correzioni automatiche:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --interactive
```
"""


def write_health_dashboard(vault_root: str, notes_data: List[Dict[str, Any]], audit_stats: Dict[str, Any]) -> str:
    """Renders and writes the Vault Health Dashboard to 99 - Meta/Vault Health Dashboard.md."""
    dashboard_content = generate_health_dashboard(vault_root, notes_data, audit_stats)
    dest_path = os.path.join(vault_root, "99 - Meta", "Vault Health Dashboard.md")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(dashboard_content)
    return dest_path


def write_audit_report(vault_root: str, all_notes_count: int, orphan_notes: List[str],
                       broken_links: Dict[str, List[str]], forward_links: Dict[str, List[str]],
                       lint_issues: List[Tuple[str, List[str]]]) -> str:
    """Generates and writes an audit report to 03 - Inbox/Audit Report - YYYY-MM-DD.md."""
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    report_filename = f"Audit Report - {today_str}.md"
    report_rel_path = os.path.join("03 - Inbox", report_filename)
    report_abs_path = os.path.join(vault_root, report_rel_path)

    os.makedirs(os.path.dirname(report_abs_path), exist_ok=True)

    total_forward = sum(len(v) for v in forward_links.values())
    total_broken = sum(len(v) for v in broken_links.values())

    report = [f"""---
status: draft
type: article
area: meta
related: ["[[Home MOC]]", "[[Vault Health Dashboard]]"]
source: original
title: "Audit Report - {today_str}"
date: '{today_str}'
updated: {datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")}
tags: [meta/audit, meta/health]
summary: "Report diagnostico della salute del Vault: note orfane, collegamenti interrotti, forward-references e conformità metadati."
---
[[Home MOC|Home]] / [[Meta]] / [[{report_filename[:-3]}]]

# Report di Audit della Salute del Vault — {today_str}

Diagnostica automatica dello stato di coerenza e integrità semantica del Second Brain.

## Riepilogo Diagnostico

- **Note totali scansionate:** {all_notes_count}
- **Note orfane rilevate:** {len(orphan_notes)}
- **Link interrotti (broken links):** {total_broken}
- **Forward-links pianificati:** {total_forward}
- **File con anomalie YAML:** {len(lint_issues)}

---

## Criticità Elevate

"""]

    if broken_links:
        report.append("### Link Interrotti (Broken Links)\n")
        for source, targets in sorted(broken_links.items()):
            report.append(f"- [[{Path(source).stem}]] (in `{source}`):\n")
            for t in targets:
                report.append(f"  - ❌ `{t}`\n")
        report.append("\n")
    else:
        report.append("✅ **Nessun link interrotto rilevato!**\n\n")

    if lint_issues:
        report.append("### Anomalie Frontmatter YAML\n")
        for f, issues in lint_issues:
            report.append(f"- [[{Path(f).stem}]] (`{f}`): {', '.join(issues)}\n")
        report.append("\n")

    report.append("---\n\n## Note Orfane & Forward Links\n\n")

    if orphan_notes:
        report.append("### Note Orfane (0 Inbound Links)\n")
        for f in orphan_notes:
            report.append(f"- [[{Path(f).stem}]] (`{f}`)\n")
        report.append("\n")
    else:
        report.append("✅ **Nessuna nota orfana in Atlas!**\n\n")

    if forward_links:
        report.append("### Forward Links Pianificati (Da Creare)\n")
        for src, fwd_list in sorted(forward_links.items()):
            report.append(f"- In [[{Path(src).stem}]]: {', '.join([f'[[{target}]]' for target in fwd_list])}\n")
        report.append("\n")

    with open(report_abs_path, 'w', encoding='utf-8') as f:
        f.write("".join(report))

    return report_abs_path


def get_git_tracked_files(root_dir: str) -> Set[str]:
    """Returns set of git-tracked files in the vault."""
    if not os.path.exists(os.path.join(root_dir, '.git')):
        return set()
    try:
        res = subprocess.run(['git', 'ls-files'], cwd=root_dir, capture_output=True, text=True, check=True)
        return {os.path.normpath(line) for line in res.stdout.splitlines()}
    except Exception:
        return set()


def safe_rename(root_dir: str, old_rel: str, new_rel: str, is_tracked: bool, dry_run: bool = False):
    """Safely renames a file with git mv support and case-sensitivity handling."""
    old_abs = os.path.join(root_dir, old_rel)
    new_abs = os.path.join(root_dir, new_rel)

    if old_abs == new_abs or dry_run:
        return

    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
    case_only = (old_abs.lower() == new_abs.lower())

    if is_tracked:
        temp_rel = old_rel + ".tmp_rename"
        temp_abs = os.path.join(root_dir, temp_rel)
        try:
            if case_only:
                subprocess.run(['git', 'mv', old_rel, temp_rel], cwd=root_dir, check=True, capture_output=True)
                subprocess.run(['git', 'mv', temp_rel, new_rel], cwd=root_dir, check=True, capture_output=True)
            else:
                subprocess.run(['git', 'mv', old_rel, new_rel], cwd=root_dir, check=True, capture_output=True)
            return
        except Exception:
            if case_only and os.path.exists(temp_abs) and not os.path.exists(old_abs):
                try:
                    subprocess.run(['git', 'mv', temp_rel, old_rel], cwd=root_dir, capture_output=True)
                except Exception:
                    pass

    try:
        if case_only:
            temp_abs = old_abs + ".tmp_rename"
            os.rename(old_abs, temp_abs)
            try:
                os.rename(temp_abs, new_abs)
            except Exception:
                if os.path.exists(temp_abs) and not os.path.exists(old_abs):
                    os.rename(temp_abs, old_abs)
                raise
        else:
            os.rename(old_abs, new_abs)
    except Exception as e:
        print(f"Rename error {old_rel} -> {new_rel}: {e}", file=sys.stderr)


def diagnose_yaml_violations(filepath: str, vault_root: str = '.') -> List[str]:
    """Diagnoses YAML frontmatter violations for a single markdown file in read-only mode."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return [f"Impossibile leggere il file: {e}"]

    has_fm, fm_text, breadcrumb, body = split_markdown_note(content)
    if not has_fm:
        return ["Frontmatter YAML mancante (nessun blocco --- iniziale)"]

    yaml_engine = build_yaml_engine()
    existing_meta = safe_load_frontmatter(fm_text, yaml_engine)
    if existing_meta is None or not isinstance(existing_meta, dict):
        return ["Errore sintassi o parsing YAML nel frontmatter"]

    rel_path = os.path.relpath(filepath, vault_root)
    is_blog = rel_path.startswith('05 - Blog') or '/05 - blog' in rel_path.lower()

    # Check required fields
    if is_blog:
        required_fields = ['stage', 'draft', 'type', 'area', 'title', 'date', 'tags']
        canonical_seq = [
            'stage', 'draft', 'type', 'area', 'related', 'aliases', 'source', 'title',
            'date', 'updated', 'tags', 'summary', 'target_path', 'video_url', 'channel',
            'subject', 'professor'
        ]
    else:
        required_fields = ['status', 'type', 'area', 'title', 'date', 'tags']
        canonical_seq = [
            'status', 'type', 'area', 'related', 'aliases', 'source', 'title',
            'date', 'updated', 'tags', 'summary', 'target_path', 'video_url', 'channel',
            'subject', 'professor'
        ]

    for req in required_fields:
        if req not in existing_meta or existing_meta[req] is None or existing_meta[req] == '':
            issues.append(f"Campo obbligatorio mancante: {req}")

    # Check canonical sequence
    keys_present = [k for k in existing_meta.keys() if k in canonical_seq]
    expected_order = sorted(keys_present, key=lambda k: canonical_seq.index(k))
    if keys_present != expected_order:
        issues.append("Ordinamento non canonico delle chiavi")

    # Check deprecated fields
    deprecated_fields = ['macro_area', 'last_modified', 'date created', 'ready', 'cssclasses', 'tags_string']
    for dep in deprecated_fields:
        if dep in existing_meta:
            issues.append(f"Campo deprecato presente: {dep}")

    # Check video fields for non-video types
    if existing_meta.get('type') != 'video':
        for vf in ['video_url', 'channel']:
            if vf in existing_meta:
                issues.append(f"Campo video non consentito per type non-video: {vf}")

    # Check tags format and hierarchy
    tags_raw = existing_meta.get('tags')
    if tags_raw is not None:
        if not isinstance(tags_raw, list):
            issues.append("Formato tags non valido (deve essere un array)")
        else:
            area_val = existing_meta.get('area', '')
            for t in tags_raw:
                t_str = str(t).strip().lstrip('#')
                norm_t = normalize_tag(t_str, area_val)
                if norm_t != t_str and t_str not in TAG_HIERARCHY_MAP.values():
                    issues.append(f"Tag non canonico o gerarchico: #{t_str} (suggerito: {norm_t})")

    # Check formatting alignment with lint_file preview
    changed, _ = lint_file(filepath, vault_root=vault_root, execute=False)
    if changed and not issues:
        issues.append("Formattazione frontmatter o breadcrumb disallineata rispetto allo standard canonico")

    return issues


def collect_vault_data(vault_root: str) -> Tuple[List[Dict[str, Any]], VaultHealthAuditor]:
    """Scans all notes and metadata across the vault."""
    auditor = VaultHealthAuditor(vault_root)
    notes_data = []

    for clean_name, rel_path in auditor.all_notes.items():
        abs_path = os.path.join(vault_root, rel_path)
        try:
            mtime = os.path.getmtime(abs_path)
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        has_fm, fm_text, breadcrumb, body = split_markdown_note(content)
        yaml_engine = build_yaml_engine()
        metadata = safe_load_frontmatter(fm_text, yaml_engine) if has_fm else {}

        notes_data.append({
            'name': clean_name,
            'rel_path': rel_path,
            'mtime': mtime,
            'content': content,
            'metadata': metadata
        })

    return notes_data, auditor


def run_governance_engine(vault_root: str, dry_run: bool = False, auto_fix: bool = False,
                          interactive: bool = False, dashboard_only: bool = False,
                          audit_only: bool = False, lint_only: bool = False) -> Dict[str, Any]:
    """Executes the governance scan and applies fixes according to CLI modes."""
    if lint_only and auto_fix:
        print("\n❌ ERRORE: La modalità --lint-only è un audit diagnostico strettamente in SOLA LETTURA.", file=sys.stderr)
        print("   Per applicare le correzioni al vault, eseguire il comando con --auto-fix senza --lint-only.\n", file=sys.stderr)
        return {'error': 'lint_only_read_only_conflict'}

    if lint_only:
        print("=" * 60)
        print("🔍 Second Brain YAML Frontmatter Linter (Read-Only Audit)")
        print("=" * 60)
        total_notes_scanned = 0
        misaligned_notes: List[Tuple[str, List[str]]] = []

        for root, dirs, files in os.walk(vault_root):
            dirs[:] = sorted([d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')])
            for file in sorted(files):
                if file.endswith('.md') and not file.startswith('.') and file not in IGNORE_FILES:
                    rel = os.path.relpath(os.path.join(root, file), vault_root)
                    if not any(rel.startswith(vd) for vd in VAULT_DIRECTORIES) and root == vault_root:
                        continue
                    total_notes_scanned += 1
                    abs_p = os.path.join(root, file)
                    issues = diagnose_yaml_violations(abs_p, vault_root=vault_root)
                    if issues:
                        misaligned_notes.append((rel, issues))

        compliant_count = total_notes_scanned - len(misaligned_notes)
        print(f"Note Totali Scansionate: {total_notes_scanned}")
        print(f"Note Conformi allo Standard: {compliant_count}")
        print(f"Note con Disallineamenti YAML: {len(misaligned_notes)}")
        print("=" * 60)

        if misaligned_notes:
            print("\n📋 Dettaglio Disallineamenti:")
            for rel, issues in misaligned_notes:
                print(f"  • [[{Path(rel).stem}]] (`{rel}`):")
                for iss in issues:
                    print(f"      - {iss}")
        else:
            print("\n✨ Tutte le note sono pienamente conformi allo standard YAML canonico!")

        print("\n💡 Nota: Nessuna modifica è stata apportata su disco (modalità sola lettura).")
        print("   Per applicare le normalizzazioni eseguire: python3 \"99 - Meta/Scripts/brain_health.py\" --auto-fix\n")

        return {
            'total_notes': total_notes_scanned,
            'compliant_notes': compliant_count,
            'misaligned_notes': len(misaligned_notes),
            'issues': misaligned_notes
        }

    notes_data, auditor = collect_vault_data(vault_root)

    broken_links_map: Dict[str, List[str]] = {}
    forward_links_map: Dict[str, List[str]] = {}
    total_valid_links = 0

    for note in notes_data:
        valid, forward, broken = auditor.audit_file_links(note['rel_path'], note['content'])
        total_valid_links += len(valid)
        if forward:
            forward_links_map[note['rel_path']] = forward
        if broken:
            broken_links_map[note['rel_path']] = broken

    orphan_notes = auditor.detect_orphans()

    audit_stats = {
        'total_notes': len(notes_data),
        'orphan_count': len(orphan_notes),
        'broken_link_count': sum(len(v) for v in broken_links_map.values()),
        'forward_link_count': sum(len(v) for v in forward_links_map.values()),
        'duplicate_count': len(auditor.duplicate_notes),
        'duplicate_notes': auditor.duplicate_notes
    }

    if auditor.duplicate_notes:
        print(f"\n⚠️  ATTENZIONE: Rilevate {len(auditor.duplicate_notes)} note omonime duplicate tra cartelle differenti:")
        for stem, paths in auditor.duplicate_notes.items():
            print(f"   • [[{stem}]]: {', '.join(paths)}")

    if dashboard_only:
        out_dash = write_health_dashboard(vault_root, notes_data, audit_stats)
        print(f"Vault Health Dashboard regenerated: {out_dash}")
        return audit_stats

    # Check Title Case renames
    planned_renames = []
    for note in notes_data:
        old_base = note['name']
        new_base = clean_filename(old_base)
        if old_base != new_base:
            parts = Path(note['rel_path']).parts
            new_rel = str(Path(*parts[:-1]) / (new_base + ".md"))
            planned_renames.append((note['rel_path'], new_rel, old_base, new_base))

    # Check Lint issues
    lint_modified = []
    for note in notes_data:
        abs_p = os.path.join(vault_root, note['rel_path'])
        changed, _ = lint_file(abs_p, vault_root=vault_root, execute=False)
        if changed:
            lint_modified.append(note['rel_path'])

    # Print diagnostic summary
    print("=" * 60)
    print("🧠 Second Brain Vault Health Engine")
    print("=" * 60)
    print(f"Total Notes: {audit_stats['total_notes']}")
    print(f"Orphan Notes: {audit_stats['orphan_count']}")
    print(f"Broken Links: {audit_stats['broken_link_count']}")
    print(f"Forward Links: {audit_stats['forward_link_count']}")
    print(f"Title Case Renames Pending: {len(planned_renames)}")
    print(f"YAML Lint Fixes Pending: {len(lint_modified)}")
    print("=" * 60)

    if audit_only:
        rep_path = write_audit_report(
            vault_root, len(notes_data), orphan_notes,
            broken_links_map, forward_links_map,
            [(f, ['Frontmatter formatting out of sync']) for f in lint_modified]
        )
        print(f"Audit report written to: {rep_path}")
        return audit_stats

    if dry_run:
        print("\n[DRY-RUN] No changes were written to disk.")
        if planned_renames:
            print("\nPlanned Renames:")
            for old, new, _, _ in planned_renames[:10]:
                print(f"  {old} -> {new}")
            if len(planned_renames) > 10:
                print(f"  ... and {len(planned_renames) - 10} more.")
        if lint_modified:
            print("\nNotes needing YAML formatting:")
            for f in lint_modified[:10]:
                print(f"  {f}")
            if len(lint_modified) > 10:
                print(f"  ... and {len(lint_modified) - 10} more.")
        return audit_stats

    apply_fixes = auto_fix

    if interactive and not auto_fix and not dry_run:
        if planned_renames or lint_modified:
            try:
                ans = input(f"\nApply fixes for {len(planned_renames)} renames and {len(lint_modified)} YAML lints? [y/N]: ")
                if ans.strip().lower() in ('y', 'yes'):
                    apply_fixes = True
            except EOFError:
                apply_fixes = False

    if apply_fixes:
        tracked_files = get_git_tracked_files(vault_root)

        # 1. Execute renames and update inbound wikilinks
        rename_map = {}
        for old_rel, new_rel, old_base, new_base in planned_renames:
            is_tracked = old_rel in tracked_files
            safe_rename(vault_root, old_rel, new_rel, is_tracked, dry_run=False)
            rename_map[old_base] = new_base

        # 2. Update inbound wikilinks if renames occurred
        if rename_map:
            for root, dirs, files in os.walk(vault_root):
                dirs[:] = sorted([d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')])
                for file in sorted(files):
                    if file.endswith('.md') and not file.startswith('.') and file not in IGNORE_FILES:
                        rel = os.path.relpath(os.path.join(root, file), vault_root)
                        if not any(rel.startswith(vd) for vd in VAULT_DIRECTORIES) and root == vault_root:
                            continue
                        f_abs = os.path.join(root, file)
                        with open(f_abs, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()

                        def replace_target(m):
                            target = m.group(1).strip()
                            rest = m.group(2)
                            if target in rename_map:
                                return f"[[{rename_map[target]}{rest}]]"
                            return m.group(0)

                        new_text = re.sub(r'\[\[([^|#\]]+)([^\]]*)\]\]', replace_target, text)
                        if new_text != text:
                            with open(f_abs, 'w', encoding='utf-8') as f:
                                f.write(new_text)

        # 3. Apply YAML linting
        for root, dirs, files in os.walk(vault_root):
            dirs[:] = sorted([d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')])
            for file in sorted(files):
                if file.endswith('.md') and not file.startswith('.') and file not in IGNORE_FILES:
                    rel = os.path.relpath(os.path.join(root, file), vault_root)
                    if not any(rel.startswith(vd) for vd in VAULT_DIRECTORIES) and root == vault_root:
                        continue
                    f_abs = os.path.join(root, file)
                    lint_file(f_abs, vault_root=vault_root, execute=True)

        # 4. Refresh data and write dashboard
        fresh_data, fresh_auditor = collect_vault_data(vault_root)
        fresh_broken = {}
        fresh_forward = {}
        for note in fresh_data:
            _, fwd, brk = fresh_auditor.audit_file_links(note['rel_path'], note['content'])
            if fwd:
                fresh_forward[note['rel_path']] = fwd
            if brk:
                fresh_broken[note['rel_path']] = brk
        fresh_orphans = fresh_auditor.detect_orphans()
        fresh_stats = {
            'total_notes': len(fresh_data),
            'orphan_count': len(fresh_orphans),
            'broken_link_count': sum(len(v) for v in fresh_broken.values()),
            'forward_link_count': sum(len(v) for v in fresh_forward.values()),
            'duplicate_count': len(fresh_auditor.duplicate_notes),
            'duplicate_notes': fresh_auditor.duplicate_notes
        }
        write_health_dashboard(vault_root, fresh_data, fresh_stats)
        print("Vault health governance fixes applied successfully and dashboard updated.")
        return fresh_stats

    return audit_stats


class HealthArgParser(argparse.ArgumentParser):
    """Custom parser ensuring interactive mode is the default when no other exclusive mode is selected."""
    def parse_args(self, args=None, namespace=None):
        parsed = super().parse_args(args, namespace)
        if not (parsed.dry_run or parsed.auto_fix or parsed.dashboard_only or parsed.audit_only or parsed.lint_only):
            parsed.interactive = True
        else:
            if not getattr(parsed, 'interactive', False):
                parsed.interactive = False
        return parsed


def build_arg_parser() -> argparse.ArgumentParser:
    """Builds CLI argument parser with mutually exclusive flags."""
    parser = HealthArgParser(
        description="brain_health.py - Unified Second Brain Governance, AST Linter & Health Auditor."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', help="Preview findings and fixes without modifying disk.")
    group.add_argument('--auto-fix', action='store_true', help="Automatically apply Title Case, YAML normalizations, and rebuild dashboard.")
    group.add_argument('--interactive', action='store_true', default=False, help="Interactive step-by-step confirmation mode (default).")
    group.add_argument('--dashboard-only', action='store_true', help="Regenerate 99 - Meta/Vault Health Dashboard.md only.")
    group.add_argument('--audit-only', action='store_true', help="Generate diagnostic report in 03 - Inbox/.")
    group.add_argument('--lint-only', action='store_true', help="Validate YAML frontmatter without modifying disk (read-only audit).")
    parser.add_argument('--vault-root', type=str, default=None, help="Custom vault root directory.")
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    interactive_mode = args.interactive
    if not (args.dry_run or args.auto_fix or args.dashboard_only or args.audit_only or args.lint_only):
        interactive_mode = True

    vault_root = get_vault_root(args.vault_root)

    run_governance_engine(
        vault_root=vault_root,
        dry_run=args.dry_run,
        auto_fix=args.auto_fix,
        interactive=interactive_mode,
        dashboard_only=args.dashboard_only,
        audit_only=args.audit_only,
        lint_only=args.lint_only
    )


if __name__ == '__main__':
    main()
