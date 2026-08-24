#!/usr/bin/env python3
"""lint_yaml.py - Definitive AST frontmatter YAML linter and normalizer for Obsidian Vault.

Enforces the canonical 10-field YAML schema:
status (or stage + draft) -> type -> area -> related -> aliases (opt) -> source -> title -> date -> updated -> tags -> summary
"""

import os
import sys
import re
import datetime
import argparse
import tempfile
from io import StringIO

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, PlainScalarString

MINOR_WORDS = {
    'di', 'del', 'della', 'dello', 'dei', 'degli', 'delle', 'da', 'dal', 'dalla', 'in', 'su',
    'sul', 'sulla', 'per', 'con', 'a', 'al', 'alla', 'o', 'e', 'ed', 'la', 'il', 'lo', 'i',
    'gli', 'le', 'un', 'uno', 'una', 'to', 'the', 'and', 'of', 'on', 'at', 'for', 'with', 'by', 'in', 'an', 'a'
}

PRESERVE_UPPER = {
    'MOC', 'AI', 'ENG', 'ITA', 'STEM', 'TIL', 'CS50', 'DNA', 'ENEA', 'NP', 'P', 'II', 'III', 'IV', 'V',
    'CLI', 'LLM', 'NLP', 'RAG', 'AST', 'API', 'REST', 'GTD', 'PKM', 'ZSH', 'CSS', 'HTML', 'JS', 'TS',
    'SQL', 'UI', 'UX', 'OS', 'URL', 'JSON', 'YAML', 'IDE', 'SDK', 'HTTP', 'HTTPS', 'TCP', 'IP', 'CPU', 'GPU'
}

CONTROLLED_TYPES = {
    'concept', 'video', 'article', 'lecture', 'book', 'project', 'moc', 'journal'
}

CONTROLLED_AREAS = {
    'tech', 'education', 'mentality', 'finance', 'projects', 'meta', 'calendar'
}

IGNORE_FOLDERS = {
    '.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode',
    '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy', 'node_modules', 'tests'
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
    'log': 'meta/log', 'workflow': 'meta/workflow', 'gtd': 'meta/gtd'
}

def clean_title_str(title: str) -> str:
    """Format string to intelligent Title Case, preserving Templater syntax."""
    base = title.strip()
    if '<%' in base:
        return base
    if base.endswith('.md'):
        base = base[:-3]
    base = base.replace('’', "'")
    base = ''.join(c for c in base if ord(c) < 128 or c.isalnum() or c.isspace() or c == "'")
    for spec in ['+', '?', '!', '(', ')', '[', ']', '_']:
        base = base.replace(spec, ' ')
    base = ' '.join(base.split())
    
    words = base.split()
    title_words = []
    for i, word in enumerate(words):
        is_first = (i == 0)
        clean_word = ''.join(c for c in word if c.isalnum()).upper()
        if clean_word in PRESERVE_UPPER:
            title_words.append(word.upper())
        elif clean_word.lower() in MINOR_WORDS and not is_first:
            title_words.append(word.lower())
        else:
            title_words.append(word.capitalize())
    return ' '.join(title_words)

def build_yaml_engine() -> ruamel.yaml.YAML:
    """Returns a configured ruamel.yaml instance with RoundTripLoader/Dumper."""
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.width = 4096
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml

def normalize_tag(tag: str, area: str = 'tech') -> str:
    """Converts a flat tag into a hierarchical area/topic tag."""
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

def strip_isolated_hashtag_lines(body: str) -> tuple[str, list[str]]:
    """Strips lines that contain only hashtags from the Markdown body while preserving headings."""
    lines = body.splitlines()
    cleaned_lines = []
    extracted_tags = []
    
    for line in lines:
        stripped = line.strip()
        # Do not strip markdown headings (# Heading, ## Heading, etc.)
        if stripped.startswith('# ') or stripped.startswith('## ') or stripped.startswith('### ') or \
           stripped.startswith('#### ') or stripped.startswith('##### ') or stripped.startswith('###### '):
            cleaned_lines.append(line)
            continue
            
        # Check if entire line is composed of #tags (e.g. #ai #tech or #tag/subtag)
        tokens = stripped.split()
        if tokens and all(tok.startswith('#') and len(tok) > 1 and not tok.startswith('#[') for tok in tokens):
            for tok in tokens:
                clean_tag = tok.lstrip('#').strip()
                if clean_tag:
                    extracted_tags.append(clean_tag)
            continue
            
        cleaned_lines.append(line)
        
    return '\n'.join(cleaned_lines), extracted_tags

def split_markdown_note(content: str) -> tuple[bool, str, str | None, str]:
    """Splits markdown into frontmatter, breadcrumb, and body."""
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

def assemble_markdown_note(frontmatter_yaml: str, breadcrumb: str | None, body: str) -> str:
    """Reassembles frontmatter, breadcrumb, and body with single empty line separations."""
    res = f'---\n{frontmatter_yaml}\n---'
    if breadcrumb:
        res += f'\n{breadcrumb}'
    if body.strip():
        res += f'\n\n{body.strip()}'
    return res + '\n'

def safe_load_frontmatter(frontmatter_text: str, yaml_engine: ruamel.yaml.YAML) -> dict:
    """Safely loads frontmatter with unquoted wikilink repairs and regex fallback."""
    if not frontmatter_text or not frontmatter_text.strip():
        return {}
    try:
        parsed = yaml_engine.load(frontmatter_text)
        if parsed and isinstance(parsed, dict):
            return dict(parsed)
    except Exception:
        pass
        
    # Pre-process unquoted wikilinks and retry
    sanitized = re.sub(r'\[\[(.*?)\]\]', r'"[[\1]]"', frontmatter_text)
    try:
        parsed = yaml_engine.load(sanitized)
        if parsed and isinstance(parsed, dict):
            return dict(parsed)
    except Exception:
        pass
        
    # Regex fallback parser
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

def get_file_dates(filepath: str, metadata_existing: dict = None) -> tuple[str, str]:
    """Extracts authentic date and updated timestamps from metadata or filesystem, preserving Templater tags."""
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

def format_canonical_frontmatter(metadata: dict, is_blog: bool = False) -> str:
    """Formats metadata into canonical 10-field YAML string using ruamel.yaml AST."""
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
    if source_val.startswith('http://') or source_val.startswith('https://'):
        doc['source'] = DoubleQuotedScalarString(source_val)
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
        
    stream = StringIO()
    yaml.dump(doc, stream)
    return stream.getvalue().strip()

def infer_metadata(rel_path: str, existing_meta: dict, body: str, filename: str, force_type: str = None, force_area: str = None) -> dict:
    """Resolves and infers metadata against controlled vocabularies and vault rules."""
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
        # Infer from path
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
        elif 'video_url' in meta or 'youtube' in path_lower or 'trascrizione' in path_lower or 'trascrizione' in body[:300].lower():
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
    
    # 3. Source resolution
    if 'source' in meta and meta['source']:
        source = str(meta['source']).strip()
    elif 'video_url' in meta and meta['video_url']:
        source = str(meta['video_url']).strip()
    else:
        source = 'original'
    meta['source'] = source
    
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
        
    # Clean obsolete properties
    for obsolete in ['macro_area', 'video_url', 'channel', 'last_modified', 'date created', 'ready', 'cssclasses', 'tags_string']:
        if obsolete in meta:
            del meta[obsolete]
            
    return meta

def lint_file(filepath: str, vault_root: str = '.', execute: bool = False, force_type: str = None, force_area: str = None) -> tuple[bool, str]:
    """Lints and standardizes a single markdown file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    has_frontmatter, frontmatter_text, breadcrumb, body = split_markdown_note(content)
    
    yaml_engine = build_yaml_engine()
    existing_meta = safe_load_frontmatter(frontmatter_text, yaml_engine) if has_frontmatter else {}
            
    rel_path = os.path.relpath(filepath, vault_root)
    filename = os.path.basename(filepath)
    is_blog = rel_path.startswith('05 - Blog') or '/05 - blog' in rel_path.lower()
    
    # Strip isolated body hashtags and merge
    cleaned_body, extracted_tags = strip_isolated_hashtag_lines(body)
    
    # Resolve metadata
    meta = infer_metadata(rel_path, existing_meta, cleaned_body, filename, force_type, force_area)
    
    # Merge existing tags with extracted tags
    current_tags = meta.get('tags', [])
    if isinstance(current_tags, str):
        current_tags = [t.strip() for t in current_tags.split(',') if t.strip()]
    elif not isinstance(current_tags, list):
        current_tags = []
        
    for et in extracted_tags:
        if et not in current_tags:
            current_tags.append(et)
    meta['tags'] = current_tags
    
    # Extract authentic dates
    date_val, updated_val = get_file_dates(filepath, existing_meta)
    meta['date'] = date_val
    meta['updated'] = updated_val
    
    # Format canonical YAML
    canonical_yaml = format_canonical_frontmatter(meta, is_blog=is_blog)
    new_content = assemble_markdown_note(canonical_yaml, breadcrumb, cleaned_body)
    
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
    parser = argparse.ArgumentParser(description='Lint and standardize frontmatter YAML across Obsidian Vault.')
    parser.add_argument('path', nargs='?', default='.', help='Target file or directory path (default: current directory).')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', default=True, help='Preview changes without modifying files (default).')
    group.add_argument('--execute', action='store_true', help='Apply formatting and frontmatter mutations directly to files.')
    parser.add_argument('--type', choices=list(CONTROLLED_TYPES), help='Force specific note type.')
    parser.add_argument('--area', choices=list(CONTROLLED_AREAS), help='Force specific area.')
    args = parser.parse_args()
    
    target_path = os.path.abspath(args.path)
    is_execute = args.execute
    
    if not os.path.exists(target_path):
        print(f'Error: Path does not exist: {target_path}')
        sys.exit(1)
        
    vault_root = os.path.abspath('.')
    
    if os.path.isfile(target_path):
        if target_path.endswith('.md'):
            changed, _ = lint_file(target_path, vault_root, execute=is_execute, force_type=args.type, force_area=args.area)
            mode_str = '[EXECUTE]' if is_execute else '[DRY-RUN]'
            if changed:
                print(f'{mode_str} Modified: {os.path.relpath(target_path, vault_root)}')
            else:
                print(f'{mode_str} Clean: {os.path.relpath(target_path, vault_root)}')
    else:
        count_changed = 0
        count_clean = 0
        mode_str = '[EXECUTE]' if is_execute else '[DRY-RUN]'
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')]
            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    fpath = os.path.join(root, file)
                    changed, _ = lint_file(fpath, vault_root, execute=is_execute, force_type=args.type, force_area=args.area)
                    if changed:
                        count_changed += 1
                        print(f'{mode_str} Modified: {os.path.relpath(fpath, vault_root)}')
                    else:
                        count_clean += 1
                        
        print(f'\n{mode_str} Finished. Total scanned: {count_changed + count_clean} | Modified/Pending: {count_changed} | Clean: {count_clean}')

if __name__ == '__main__':
    main()
