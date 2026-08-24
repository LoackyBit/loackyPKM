#!/usr/bin/env python3
# auto_sort_inbox.py - Motore di smistamento GTD automatico per il Second Brain.
# Analizza, valida lo YAML, e sposta i file da 03 - Inbox alle cartelle finali di Atlas/Blog/MOC.

import os
import re
import sys
import subprocess

def get_git_tracked_files(root_dir):
    if not os.path.exists(os.path.join(root_dir, '.git')):
        return set()
    try:
        res = subprocess.run(['git', 'ls-files'], cwd=root_dir, capture_output=True, text=True, check=True)
        return {os.path.normpath(line) for line in res.stdout.splitlines()}
    except Exception:
        return set()

def parse_yaml(content):
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return {}
    closing_idx = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            closing_idx = idx
            break
    if closing_idx == -1:
        return {}
    
    metadata = {}
    current_key = None
    list_items = []
    for line in lines[1:closing_idx]:
        stripped = line.strip()
        if not stripped:
            continue
        if (line.startswith('  - ') or line.startswith('    - ') or stripped.startswith('- ')) and current_key:
            item_val = stripped.lstrip('-').strip().strip('"').strip("'")
            list_items.append(item_val)
            metadata[current_key] = list_items
            continue
        match = re.match(r'^([\w_-]+)\s*:\s*(.*)$', line)
        if match:
            current_key = match.group(1).strip()
            val_part = match.group(2).strip()
            list_items = []
            if not val_part:
                metadata[current_key] = None
            elif val_part.startswith('[') and val_part.endswith(']'):
                items = [item.strip().strip('"').strip("'") for item in val_part[1:-1].split(',')]
                metadata[current_key] = [i for i in items if i]
            else:
                val_part = val_part.strip('"').strip("'")
                metadata[current_key] = val_part
    return metadata

def decide_destination(filename, content, metadata, filepath_rel):
    content_lower = content.lower()
    path_lower = filepath_rel.lower()
    
    # Estrai tag
    tags = metadata.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip().lower() for t in tags.split(',')]
    else:
        tags = [str(t).lower() for t in tags]
        
    macro_area = str(metadata.get('macro_area', '')).lower()
    
    # 1. Map of Content (MOC)
    if 'moc' in tags or filename.endswith('MOC.md') or macro_area == 'meta' and 'moc' in content_lower:
        return "01 - Map of Content"
        
    # 2. Blog (Quartz)
    if 'blog' in tags or 'draft' in metadata and metadata['draft'] is False or path_lower.startswith('05 - blog'):
        return "05 - Blog"
        
    # 3. Atlas / Prompts
    if 'prompt' in tags or 'prompting' in content_lower or '02 - atlas/prompt' in path_lower:
        return "02 - Atlas/Prompt"
        
    # 4. Atlas / Finance
    if 'finance' in tags or macro_area == 'finance' or any(w in content_lower for w in ['investimenti', 'fisco', 'cripto', 'bitcoin', 'economia']):
        return "02 - Atlas/Finance"
        
    # 5. Atlas / Mentality
    if 'mentality' in tags or macro_area == 'mentality' or any(w in content_lower for w in ['mindset', 'goggins', 'dopamine', 'studio', 'psicologia', 'skincare', 'abitudini']):
        return "02 - Atlas/Mentality"
        
    # 6. Atlas / Corsi (University)
    if 'university' in tags or macro_area == 'university' or any(w in content_lower for w in ['cs50', 'stem', 'universitario', 'algoritmi', 'fisica', 'analisi']):
        return "02 - Atlas/Corsi"
        
    # 7. Atlas / Technology (Default fallback per file tecnici)
    if 'tech' in tags or macro_area == 'tech' or any(w in content_lower for w in ['python', 'javascript', 'coding', 'agente', 'cursor', 'api', 'docker', 'terminale']):
        return "02 - Atlas/Tecnology"
        
    # Default fallback a Mentality o Tecnology se generico
    return "02 - Atlas/Mentality"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    if not os.path.exists(inbox_dir):
        print(f"Inbox non trovata: {inbox_dir}")
        sys.exit(1)
        
    # Trova i file in Inbox (escludendo cartelle strutturate come School/ o file nascosti)
    files_to_sort = []
    for f in os.listdir(inbox_dir):
        f_path = os.path.join(inbox_dir, f)
        if os.path.isfile(f_path) and f.endswith('.md') and not f.startswith('.'):
            # Salta i report di audit, le proposte temporanee, i file grezzi in elaborazione e la dashboard
            if not f.startswith("Audit Report") and not f.startswith("proposed-") and not f.startswith("raw-") and not f.startswith("seen-") and f != "Review Dashboard.md":
                files_to_sort.append(f)
                
    if not files_to_sort:
        print("Inbox vuota. Nessun file da smistare.")
        sys.exit(0)
        
    tracked_files = get_git_tracked_files(vault_root)
    moved_count = 0
    
    print(f"Trovati {len(files_to_sort)} file da smistare in Inbox...")
    
    for f in files_to_sort:
        old_abs = os.path.join(inbox_dir, f)
        old_rel = os.path.relpath(old_abs, vault_root)
        
        # Correggi prima lo YAML frontmatter tramite lint_yaml
        lint_script = os.path.join(vault_root, ".agents/skills/meta/scripts/lint_yaml.py")
        if os.path.exists(lint_script):
            subprocess.run([sys.executable, lint_script, old_abs, "--execute"], capture_output=True)
            
        with open(old_abs, 'r', encoding='utf-8', errors='ignore') as file_obj:
            content = file_obj.read()
            
        metadata = parse_yaml(content)
        
        # Salta i file non ancora pronti per lo smistamento
        if metadata.get('ready') is not True:
            print(f"[SKIP] Nota non pronta (ready: true non presente o impostato a false): {f}")
            continue
            
        dest_folder = decide_destination(f, content, metadata, old_rel)
        
        new_dir_abs = os.path.join(vault_root, dest_folder)
        os.makedirs(new_dir_abs, exist_ok=True)
        
        new_abs = os.path.join(new_dir_abs, f)
        new_rel = os.path.relpath(new_abs, vault_root)
        
        print(f"[SORT] Smistamento: {f} -> {dest_folder}/")
        
        is_tracked = old_rel in tracked_files
        
        if is_tracked:
            try:
                subprocess.run(['git', 'mv', old_rel, new_rel], cwd=vault_root, check=True, capture_output=True)
            except Exception:
                os.rename(old_abs, new_abs)
        else:
            os.rename(old_abs, new_abs)
            
        moved_count += 1
        
    # Esegui tidy_vault alla fine per formattare e aggiornare i breadcrumbs delle note spostate
    tidy_script = os.path.join(vault_root, "99 - Meta/Scripts/tidy_vault.py")
    if os.path.exists(tidy_script) and moved_count > 0:
        print("\nAvvio di tidy_vault per allineare i breadcrumbs dei file spostati...")
        subprocess.run([sys.executable, tidy_script, "--execute"])
        
    print(f"\nSmistamento completato. Spostati {moved_count} file.")

if __name__ == '__main__':
    main()
