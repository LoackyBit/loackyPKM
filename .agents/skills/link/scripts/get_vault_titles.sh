#!/bin/bash
# get_vault_titles.sh - Ottiene tutti i titoli delle note del Vault per la skill /link.
# Legge sia i nomi dei file che il campo 'title' dal frontmatter YAML.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

python3 -c "
import os, re, sys

vault_root = '$VAULT_ROOT'
titles = set()

# Definiamo cartelle da ignorare
ignore_folders = {'.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode', '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy'}

# Regex per estrarre il title dal frontmatter
yaml_title_re = re.compile(r'^title\s*:\s*\"([^\"]+)\"|^title\s*:\s*\'([^\'\"]+)\'|^title\s*:\s*([^\"\'\s][^\n]*)', re.IGNORECASE)

for root, dirs, files in os.walk(vault_root):
    # Salta le cartelle da ignorare
    dirs[:] = [d for d in dirs if d not in ignore_folders and not d.startswith('.')]
    
    for file in files:
        if file.endswith('.md') and not file.startswith('.'):
            filepath = os.path.join(root, file)
            # Aggiungi nome del file (senza estensione)
            basename = file[:-3]
            titles.add(basename)
            
            # Leggi il frontmatter per trovare titoli personalizzati
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1024) # Leggi solo l'inizio per efficienza (il frontmatter è all'inizio)
                    if content.startswith('---'):
                        end_fm = content.find('---', 3)
                        if end_fm != -1:
                            frontmatter = content[3:end_fm]
                            for line in frontmatter.split('\n'):
                                line = line.strip()
                                match = yaml_title_re.match(line)
                                if match:
                                    # Estrai il titolo catturato dal gruppo corretto
                                    val = next(g for g in match.groups() if g is not None)
                                    titles.add(val.strip())
            except Exception as e:
                pass

for t in sorted(list(titles)):
    if t.strip():
        print(t)
"
