#!/usr/bin/env python3
import os
import sys
import re
import unicodedata
import datetime
import subprocess
import argparse
import traceback

MINOR_WORDS = {"di", "del", "della", "da", "in", "su", "per", "con", "a", "o", "e", "la", "il", "lo", "i", "gli", "le", "to", "the", "and", "of", "on", "at", "for", "d", "l"}
PRESERVE_UPPER = {"MOC", "AI", "ENG", "ITA", "STEM", "TIL", "CS50", "DNA", "ENEA", "NP", "P", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "CLI", "LLM", "NLP", "PACRAR", "M1", "M2", "M3", "P1", "P2", "P3"}

def capitalize_word_with_apostrophe(word, is_first):
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

def clean_filename(filename):
    # Remove extension if present
    base = filename
    if filename.endswith(".md"):
        base = filename[:-3]
        
    # Replace curly apostrophe with straight apostrophe
    base = base.replace("’", "'")
    
    # Remove emojis
    clean_chars = []
    for c in base:
        cat = unicodedata.category(c)
        if cat in ('So', 'Cs'):
            continue
        if 0x1F000 <= ord(c) <= 0x1FFFF or 0x2600 <= ord(c) <= 0x27BF:
            continue
        clean_chars.append(c)
    base = "".join(clean_chars)
    
    # Remove accents
    nfd_form = unicodedata.normalize('NFD', base)
    base = "".join(c for c in nfd_form if unicodedata.category(c) != 'Mn')
    
    # Remove special characters: +, ?, !, (), []
    for spec in ['+', '?', '!', '(', ')', '[', ']']:
        base = base.replace(spec, ' ')
        
    # Clean up whitespace
    base = " ".join(base.split())
    
    # Apply title casing
    words = base.split()
    title_words = []
    for i, word in enumerate(words):
        is_first = (i == 0)
        is_last = (i == len(words) - 1)
        
        if "'" in word:
            formatted = capitalize_word_with_apostrophe(word, is_first)
            title_words.append(formatted)
            continue
            
        clean_word = "".join(c for c in word if c.isalnum())
        clean_upper = clean_word.upper()
        clean_lower = clean_word.lower()
        
        if clean_upper in PRESERVE_UPPER:
            title_words.append(word.upper())
        elif clean_lower in MINOR_WORDS and not is_first and not is_last:
            title_words.append(word.lower())
        else:
            # Check for mixed case
            has_upper = any(c.isupper() for c in word)
            has_lower = any(c.islower() for c in word)
            if has_upper and has_lower:
                title_words.append(word)
            else:
                title_words.append(word.capitalize())
                
    result = " ".join(title_words)
    return result

def parse_yaml_frontmatter(yaml_text):
    metadata = {}
    lines = yaml_text.split('\n')
    current_key = None
    list_items = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
            
        if (line.startswith('  - ') or line.startswith('    - ') or stripped.startswith('- ')) and current_key is not None:
            item_val = stripped.lstrip('-').strip()
            if (item_val.startswith('"') and item_val.endswith('"')) or (item_val.startswith("'") and item_val.endswith("'")):
                item_val = item_val[1:-1]
            list_items.append(item_val)
            metadata[current_key] = list_items
            i += 1
            continue
            
        match = re.match(r'^([\w_-]+)\s*:\s*(.*)$', line)
        if match:
            current_key = match.group(1).strip()
            val_part = match.group(2).strip()
            list_items = []
            
            if not val_part:
                metadata[current_key] = None
            elif val_part.startswith('[') and val_part.endswith(']'):
                items = [item.strip() for item in val_part[1:-1].split(',')]
                cleaned_items = []
                for item in items:
                    if not item:
                        continue
                    if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    cleaned_items.append(item)
                metadata[current_key] = cleaned_items
            else:
                if (val_part.startswith('"') and val_part.endswith('"')) or (val_part.startswith("'") and val_part.endswith("'")):
                    val_part = val_part[1:-1]
                if val_part.lower() == 'true':
                    val_part = True
                elif val_part.lower() == 'false':
                    val_part = False
                metadata[current_key] = val_part
        i += 1
        
    return metadata

def get_file_dates(filepath, metadata_existing=None):
    date_val = None
    updated_val = None
    
    if metadata_existing:
        for k, v in metadata_existing.items():
            k_lower = k.lower()
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
        date_val = ctime.strftime("%Y-%m-%d")
    else:
        match = re.match(r'^(\d{4}-\d{2}-\d{2})', date_val)
        if match:
            date_val = match.group(1)
            
    if not updated_val:
        updated_val = mtime.strftime("%Y-%m-%dT%H:%M")
    else:
        updated_val = updated_val.replace(" ", "T")
        match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', updated_val)
        if match:
            updated_val = match.group(1)
        else:
            updated_val = mtime.strftime("%Y-%m-%dT%H:%M")
            
    return date_val, updated_val

def extract_inline_tags(text):
    tags = []
    in_code_block = False
    for line in text.split('\n'):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if line.strip().startswith('#'):
            match_header = re.match(r'^#\s+', line)
            if match_header:
                continue
        
        found = re.findall(r'(?<!\S)#([a-zA-Z0-9_-]+)', line)
        for tag in found:
            if tag and not tag.isdigit():
                tags.append(tag.lower())
    return tags

def clean_tags(tags_list, extra_tags=None):
    cleaned = []
    seen = set()
    
    if extra_tags:
        for t in extra_tags:
            if t is None:
                continue
            t_clean = str(t).strip().lower().lstrip('#')
            if t_clean and t_clean not in seen:
                cleaned.append(t_clean)
                seen.add(t_clean)
                
    if tags_list:
        for t in tags_list:
            if t is None:
                continue
            t_clean = str(t).strip().lower().lstrip('#')
            if t_clean and t_clean not in seen:
                cleaned.append(t_clean)
                seen.add(t_clean)
            
    return cleaned

def get_summary(content, metadata_existing=None):
    if metadata_existing:
        for k, v in metadata_existing.items():
            if k.lower() in ('summary', 'description') and v:
                return str(v).strip()
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    for line in lines:
        if line.startswith('#') or line.startswith('---') or line.startswith('[['):
            continue
        clean_line = re.sub(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]', r'\1', line)
        clean_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_line)
        clean_line = clean_line.replace('**', '').replace('==', '').replace('_', '')
        if len(clean_line) > 100:
            return clean_line[:97] + "..."
        return clean_line
    return ""

def ensure_collegamenti_section(content):
    match = re.search(r'##\s+Collegamenti', content, re.IGNORECASE)
    if match:
        pos = match.start()
        before = content[:pos].rstrip()
        if not before.endswith('---'):
            content = content[:pos] + "---\n" + content[pos:]
        return content
    else:
        match_related = re.search(r'##\s+(Related|Link)', content, re.IGNORECASE)
        if match_related:
            pos = match_related.start()
            end = match_related.end()
            before = content[:pos].rstrip()
            if not before.endswith('---'):
                prefix = "---\n"
            else:
                prefix = ""
            content = content[:pos] + prefix + "## Collegamenti" + content[end:]
            return content
            
        content = content.rstrip()
        content += "\n\n---\n## Collegamenti\n"
        return content

def strip_old_navigation(content_lines):
    new_lines = []
    i = 0
    while i < len(content_lines) and not content_lines[i].strip():
        i += 1
        
    skip_indices = set()
    j = i
    while j < min(i + 8, len(content_lines)):
        line = content_lines[j].strip()
        
        if line.startswith('[[') and line.endswith(']]') and '/' in line:
            skip_indices.add(j)
            j += 1
            continue
            
        if line.startswith('Up:') or line.startswith('up:'):
            skip_indices.add(j)
            j += 1
            continue
            
        if line.startswith('Related:') or line.startswith('related:'):
            skip_indices.add(j)
            j += 1
            while j < len(content_lines):
                sub_line = content_lines[j].strip()
                if sub_line == '-' or sub_line.startswith('- ') or not sub_line:
                    skip_indices.add(j)
                    j += 1
                else:
                    break
            continue
            
        j += 1
        
    for idx, line in enumerate(content_lines):
        if idx in skip_indices:
            continue
        new_lines.append(line)
        
    return new_lines

def get_breadcrumbs(filepath, clean_title):
    parts = filepath.split('/')
    if len(parts) < 2:
        return ""
    
    filename_base = parts[-1]
    if filename_base.endswith(".md"):
        filename_base = filename_base[:-3]
        
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
    else:
        parent_area = "[[Atlas]]"
        
    self_link = f"[[{filename_base}|{clean_title}]]" if filename_base != clean_title else f"[[{filename_base}]]"
    return f"[[Home MOC|Home]] / {parent_area} / {self_link}"

def serialize_atlas_yaml(metadata):
    lines = ["---"]
    title = metadata.get("title", "") or ""
    lines.append(f'title: "{title}"')
    
    date = metadata.get("date", "") or ""
    lines.append(f'date: {date}')
    
    updated = metadata.get("updated", "") or ""
    lines.append(f'updated: {updated}')
    
    tags = metadata.get("tags", [])
    if tags is None:
        tags = []
    elif isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    tags_str = ", ".join(tags)
    lines.append(f'tags: [{tags_str}]')
    
    status = metadata.get("status", "permanent") or "permanent"
    lines.append(f'status: {status}')
    
    macro_area = metadata.get("macro_area", "tech") or "tech"
    lines.append(f'macro_area: {macro_area}')
    lines.append("---")
    return "\n".join(lines)

def serialize_blog_yaml(metadata):
    lines = ["---"]
    title = metadata.get("title", "") or ""
    lines.append(f'title: "{title}"')
    
    date = metadata.get("date", "") or ""
    lines.append(f'date: {date}')
    
    tags = metadata.get("tags", [])
    if tags is None:
        tags = []
    elif isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    tags_str = ", ".join(tags)
    lines.append(f'tags: [{tags_str}]')
    
    stage = metadata.get("stage", "fine-tuned 🧠") or "fine-tuned 🧠"
    lines.append(f'stage: {stage}')
    
    summary = metadata.get("summary", "") or ""
    summary = re.sub(r'\\+"', '"', summary)
    summary = summary.replace('"', '\\"')
    lines.append(f'summary: "{summary}"')
    
    draft_val = metadata.get("draft", False)
    draft_str = 'true' if draft_val else 'false'
    lines.append(f'draft: {draft_str}')
    lines.append("---")
    return "\n".join(lines)

def serialize_school_yaml(metadata):
    lines = ["---"]
    title = metadata.get("title", "") or ""
    lines.append(f'title: "{title}"')
    
    date = metadata.get("date", "") or ""
    lines.append(f'date: {date}')
    
    updated = metadata.get("updated", "") or ""
    lines.append(f'updated: {updated}')
    
    tags = metadata.get("tags", [])
    if tags is None:
        tags = []
    elif isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    tags_str = ", ".join(tags)
    lines.append(f'tags: [{tags_str}]')
    
    status = metadata.get("status", "draft") or "draft"
    lines.append(f'status: {status}')
    
    macro_area = metadata.get("macro_area", "school") or "school"
    lines.append(f'macro_area: {macro_area}')
    lines.append("---")
    return "\n".join(lines)

def get_git_tracked_files(root_dir):
    if not os.path.exists(os.path.join(root_dir, '.git')):
        return set()
    try:
        res = subprocess.run(['git', 'ls-files'], cwd=root_dir, capture_output=True, text=True, check=True)
        tracked = set()
        for line in res.stdout.splitlines():
            tracked.add(os.path.normpath(line))
        return tracked
    except Exception:
        return set()

def safe_rename(root_dir, old_rel_path, new_rel_path, is_tracked, dry_run=False):
    old_abs = os.path.join(root_dir, old_rel_path)
    new_abs = os.path.join(root_dir, new_rel_path)
    
    if old_abs == new_abs:
        return
        
    print(f"Renaming: {old_rel_path} -> {new_rel_path}")
    
    if dry_run:
        return
        
    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
    case_only = (old_abs.lower() == new_abs.lower())
    
    if is_tracked:
        try:
            if case_only:
                temp_rel_path = old_rel_path + ".tmp_rename"
                subprocess.run(['git', 'mv', old_rel_path, temp_rel_path], cwd=root_dir, check=True, capture_output=True)
                subprocess.run(['git', 'mv', temp_rel_path, new_rel_path], cwd=root_dir, check=True, capture_output=True)
            else:
                subprocess.run(['git', 'mv', old_rel_path, new_rel_path], cwd=root_dir, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            try:
                if case_only:
                    temp_abs = old_abs + ".tmp_rename"
                    os.rename(old_abs, temp_abs)
                    os.rename(temp_abs, new_abs)
                else:
                    os.rename(old_abs, new_abs)
            except Exception as ex:
                print(f"Error: Fallback rename failed for {old_rel_path}: {ex}")
    else:
        try:
            if case_only:
                temp_abs = old_abs + ".tmp_rename"
                os.rename(old_abs, temp_abs)
                os.rename(temp_abs, new_abs)
            else:
                os.rename(old_abs, new_abs)
        except Exception as e:
            print(f"Error: rename failed for {old_rel_path}: {e}")

def process_file_content(filepath, rel_path, renamed_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    has_frontmatter = False
    frontmatter_content = []
    body_lines = []
    
    if len(lines) > 0 and lines[0].strip() == '---':
        closing_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == '---':
                closing_idx = idx
                break
        if closing_idx != -1:
            has_frontmatter = True
            frontmatter_content = lines[1:closing_idx]
            body_lines = lines[closing_idx+1:]
        else:
            body_lines = lines
    else:
        body_lines = lines
        
    metadata_existing = {}
    if has_frontmatter:
        metadata_existing = parse_yaml_frontmatter("\n".join(frontmatter_content))
        
    filename = os.path.basename(filepath)
    clean_title = clean_filename(filename)
    if 'title' in metadata_existing and metadata_existing['title']:
        clean_title = clean_filename(str(metadata_existing['title']))
        
    date_val, updated_val = get_file_dates(filepath, metadata_existing)
    body_text = "\n".join(body_lines)
    inline_tags = extract_inline_tags(body_text)
    
    # Replace wiki-links
    def replace_link(match):
        link_target = match.group(1).strip()
        rest = match.group(2)
        new_target = renamed_map.get(link_target)
        if not new_target:
            cleaned_target = clean_filename(link_target)
            new_target = renamed_map.get(cleaned_target)
            
        if new_target:
            return f"[[{new_target}{rest}]]"
        return match.group(0)
        
    body_text = re.sub(r'\[\[([^|#\]]+)([^\]]*)\]\]', replace_link, body_text)
    
    body_lines = body_text.split('\n')
    body_lines = strip_old_navigation(body_lines)
    
    body_text = "\n".join(body_lines)
    body_text = ensure_collegamenti_section(body_text)
    
    parts = rel_path.split('/')
    parent_dir = parts[0]
    
    existing_tags = metadata_existing.get('tags', [])
    if existing_tags is None:
        existing_tags = []
    elif isinstance(existing_tags, str):
        existing_tags = [t.strip() for t in existing_tags.split(",") if t.strip()]
        
    path_lower = rel_path.lower()
    
    if parent_dir == "02 - Atlas" or rel_path.startswith("99 - Meta"):
        if "mentality" in path_lower:
            macro_area = "mentality"
        elif "finance" in path_lower:
            macro_area = "finance"
        elif "tecnology" in path_lower or "prompt" in path_lower or "animator2d" in path_lower:
            macro_area = "tech"
        elif "corsi" in path_lower or "education" in path_lower:
            macro_area = "university"
        elif "99 - Meta" in rel_path or "99 - meta" in path_lower:
            macro_area = "meta"
        else:
            macro_area = metadata_existing.get('macro_area', 'tech')
            
        status_val = metadata_existing.get('status', 'permanent')
        if status_val not in ('draft', 'in-progress', 'permanent', 'reference'):
            status_val = 'permanent'
            
        tags = clean_tags(existing_tags, extra_tags=inline_tags)
        
        metadata_new = {
            'title': clean_title,
            'date': date_val,
            'updated': updated_val,
            'tags': tags,
            'status': status_val,
            'macro_area': macro_area
        }
        frontmatter_str = serialize_atlas_yaml(metadata_new)
        
    elif rel_path.startswith("05 - Blog"):
        tags = clean_tags(existing_tags, extra_tags=inline_tags)
        summary_val = get_summary(body_text, metadata_existing)
        stage_val = metadata_existing.get('stage', 'fine-tuned 🧠')
        draft_val = metadata_existing.get('draft', False)
        
        metadata_new = {
            'title': clean_title,
            'date': date_val,
            'tags': tags,
            'stage': stage_val,
            'summary': summary_val,
            'draft': draft_val
        }
        frontmatter_str = serialize_blog_yaml(metadata_new)
        
    elif rel_path.startswith("03 - Inbox/School"):
        sub_tags = []
        if len(parts) > 2:
            for p in parts[2:-1]:
                sub_tags.append(p.lower())
        tags = clean_tags(existing_tags, extra_tags=['school'] + sub_tags + inline_tags)
        
        metadata_new = {
            'title': clean_title,
            'date': date_val,
            'updated': updated_val,
            'tags': tags,
            'status': 'draft',
            'macro_area': 'school'
        }
        frontmatter_str = serialize_school_yaml(metadata_new)
    else:
        tags = clean_tags(existing_tags, extra_tags=['moc'] + inline_tags)
        metadata_new = {
            'title': clean_title,
            'date': date_val,
            'updated': updated_val,
            'tags': tags,
            'status': 'permanent',
            'macro_area': 'meta'
        }
        frontmatter_str = serialize_atlas_yaml(metadata_new)
        
    breadcrumbs = get_breadcrumbs(rel_path, clean_title)
    
    if breadcrumbs:
        final_content = f"{frontmatter_str}\n{breadcrumbs}\n\n{body_text.lstrip()}"
    else:
        final_content = f"{frontmatter_str}\n\n{body_text.lstrip()}"
        
    return final_content

def main():
    parser = argparse.ArgumentParser(description="Tidy Obsidian Vault markdown files.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true', help="Scan and show changes without writing.")
    group.add_argument('--execute', action='store_true', help="Execute the changes (rename and format).")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    
    target_folders = [
        "01 - Map of Content",
        "02 - Atlas",
        "03 - Inbox/School",
        "05 - Blog",
        "99 - Meta"
    ]
    
    print(f"Scanning target folders in vault: {root_dir}")
    
    md_files = []
    for folder in target_folders:
        folder_abs = os.path.join(root_dir, folder)
        if not os.path.exists(folder_abs):
            continue
        for dirpath, dirnames, filenames in os.walk(folder_abs):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('.trash', '.git', '.obsidian')]
            for f in filenames:
                if f.endswith('.md') and not f.startswith('.'):
                    abs_path = os.path.join(dirpath, f)
                    rel_path = os.path.relpath(abs_path, root_dir)
                    md_files.append(rel_path)
                    
    print(f"Found {len(md_files)} markdown files.")
    
    renamed_files = []
    renamed_map = {}
    used_lower_paths = {}
    
    for rel_path in md_files:
        used_lower_paths[rel_path.lower()] = rel_path
        
    for rel_path in md_files:
        parts = rel_path.split('/')
        old_filename = parts[-1]
        old_base = old_filename[:-3]
        
        new_base = clean_filename(old_filename)
        new_filename = new_base + ".md"
        
        if old_filename != new_filename:
            new_rel_path = "/".join(parts[:-1] + [new_filename])
            
            if new_rel_path.lower() in used_lower_paths and used_lower_paths[new_rel_path.lower()] != rel_path:
                suffix = 1
                while True:
                    candidate_base = f"{new_base} {suffix}"
                    candidate_filename = candidate_base + ".md"
                    candidate_rel_path = "/".join(parts[:-1] + [candidate_filename])
                    if candidate_rel_path.lower() not in used_lower_paths:
                        new_base = candidate_base
                        new_filename = candidate_filename
                        new_rel_path = candidate_rel_path
                        break
                    suffix += 1
            
            if rel_path.lower() in used_lower_paths:
                del used_lower_paths[rel_path.lower()]
            used_lower_paths[new_rel_path.lower()] = new_rel_path
            
            renamed_files.append((rel_path, new_rel_path))
            renamed_map[old_base] = new_base
            
    if renamed_files:
        print(f"\nPlanned renames ({len(renamed_files)} files):")
        for old, new in renamed_files:
            print(f"  [RENAME] {old} -> {os.path.basename(new)}")
    else:
        print("\nNo files violate naming conventions.")
        
    tracked_files = get_git_tracked_files(root_dir)
    
    if args.execute and renamed_files:
        print("\nPerforming renaming...")
        for old_rel, new_rel in renamed_files:
            is_tracked = old_rel in tracked_files
            safe_rename(root_dir, old_rel, new_rel, is_tracked, dry_run=False)
        print("Renaming completed.")
        
    current_files = []
    path_mapping = {}
    
    if args.execute:
        for folder in target_folders:
            folder_abs = os.path.join(root_dir, folder)
            if not os.path.exists(folder_abs):
                continue
            for dirpath, dirnames, filenames in os.walk(folder_abs):
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('.trash', '.git', '.obsidian')]
                for f in filenames:
                    if f.endswith('.md') and not f.startswith('.'):
                        abs_path = os.path.join(dirpath, f)
                        rel_path = os.path.relpath(abs_path, root_dir)
                        current_files.append(rel_path)
                        path_mapping[rel_path] = rel_path
    else:
        current_files = md_files.copy()
        rename_dict = {old: new for old, new in renamed_files}
        for path in current_files:
            path_mapping[path] = rename_dict.get(path, path)
            
    formatted_count = 0
    format_list = []
    
    print("\nAnalyzing file contents and formatting...")
    for read_path in current_files:
        final_rel_path = path_mapping[read_path]
        abs_read_path = os.path.join(root_dir, read_path)
        
        try:
            with open(abs_read_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            formatted_content = process_file_content(abs_read_path, final_rel_path, renamed_map)
            
            if original_content != formatted_content:
                format_list.append((read_path, final_rel_path))
                if args.execute:
                    with open(abs_read_path, 'w', encoding='utf-8') as fw:
                        fw.write(formatted_content)
                    formatted_count += 1
                else:
                    formatted_count += 1
        except Exception as e:
            print(f"Error processing {read_path}: {e}")
            traceback.print_exc()
            
    if format_list:
        print(f"\nPlanned formatting ({len(format_list)} files):")
        for orig, final in format_list[:50]:
            print(f"  [FORMAT] {orig}")
        if len(format_list) > 50:
            print(f"  ... and {len(format_list) - 50} more files.")
    else:
        print("\nNo files need formatting updates.")
        
    print(f"\nSummary:")
    if args.dry_run:
        print(f"  [DRY RUN] Would rename {len(renamed_files)} files.")
        print(f"  [DRY RUN] Would format {formatted_count} files.")
    else:
        print(f"  Renamed {len(renamed_files)} files.")
        print(f"  Formatted {formatted_count} files.")

if __name__ == '__main__':
    main()
