#!/usr/bin/env python3
# update_dashboard.py - Genera la Vault Health Dashboard in puro Markdown statico.
# Evita l'uso di query dinamiche Dataview per garantire la massima portabilità del file.

import os
import re
import sys
import datetime

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

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    
    ignore_folders = {'.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode', '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy'}
    
    notes_data = []
    
    # 1. Scansiona tutte le note
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_folders and not d.startswith('.')]
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, vault_root)
                
                try:
                    mtime = os.path.getmtime(abs_path)
                    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except Exception:
                    continue
                    
                metadata = parse_yaml(content)
                notes_data.append({
                    'name': file[:-3],
                    'rel_path': rel_path,
                    'mtime': mtime,
                    'metadata': metadata
                })
                
    # 2. Filtra "Note in Staging" (draft o in-progress)
    staging_notes = []
    for note in notes_data:
        status = str(note['metadata'].get('status', '')).lower()
        if status in ('draft', 'in-progress'):
            # Salta i report di audit
            if not note['name'].startswith("Audit Report"):
                staging_notes.append(note)
    staging_notes.sort(key=lambda x: x['metadata'].get('date', ''), reverse=True)
    
    # 3. Filtra "Semi del Blog"
    blog_seeds = []
    for note in notes_data:
        if note['rel_path'].startswith("05 - Blog"):
            stage = str(note['metadata'].get('stage', ''))
            draft = note['metadata'].get('draft', True)
            if 'seed 🌱' in stage or 'growing 🌿' in stage or draft is True:
                # Escludi file di indice generici del blog
                if note['name'] != "Index":
                    blog_seeds.append(note)
    blog_seeds.sort(key=lambda x: x['metadata'].get('date', ''), reverse=True)
    
    # 4. Filtra "Note Modificate di Recente"
    recent_notes = [n for n in notes_data if not n['rel_path'].startswith("04 - Calendar") and n['name'] != "Vault Health Dashboard"]
    recent_notes.sort(key=lambda x: x['mtime'], reverse=True)
    recent_notes = recent_notes[:10]
    
    # 5. Costruisci le tabelle Markdown
    
    # Tabella Staging
    if staging_notes:
        staging_table = "| Nota | Creazione | Macro Area | Stato |\n|---|---|---|---|\n"
        for n in staging_notes:
            date_str = n['metadata'].get('date', 'N/D')
            area = n['metadata'].get('macro_area', 'N/D')
            status = n['metadata'].get('status', 'N/D')
            staging_table += f"| [[{n['name']}]] | {date_str} | {area} | `{status}` |\n"
    else:
        staging_table = "*Nessuna nota in staging.*"
        
    # Tabella Blog
    if blog_seeds:
        blog_table = "| Articolo | Data | Stadio | Stato |\n|---|---|---|---|\n"
        for n in blog_seeds:
            date_str = n['metadata'].get('date', 'N/D')
            stage = n['metadata'].get('stage', 'N/D')
            draft_status = "Bozza" if n['metadata'].get('draft', True) else "Pronto"
            blog_table += f"| [[{n['name']}]] | {date_str} | {stage} | `{draft_status}` |\n"
    else:
        blog_table = "*Nessuna bozza attiva nel blog.*"
        
    # Tabella Recent
    recent_table = "| Nota | Ultima Modifica | Macro Area |\n|---|---|---|\n"
    for n in recent_notes:
        mtime_dt = datetime.datetime.fromtimestamp(n['mtime']).strftime("%Y-%m-%d %H:%M")
        area = n['metadata'].get('macro_area', 'N/D')
        recent_table += f"| [[{n['name']}]] | {mtime_dt} | {area} |\n"
        
    # 6. Scrivi il file finale Vault Health Dashboard.md
    today_str = datetime.date.today().strftime("%Y-%m-%d %H:%M")
    
    dashboard_content = f"""---
title: "Vault Health Dashboard"
date: 2026-07-12
updated: {datetime.date.today().strftime("%Y-%m-%dT%H:%M")}
tags: [meta, dashboard, system-health]
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[Obsidian Second Brain]] / [[Vault Health Dashboard]]

# 📊 Vault Health Dashboard

Pannello di controllo in **puro Markdown** per monitorare lo stato delle note, delle bozze e della qualità dei metadati.

*Ultimo aggiornamento automatico:* `{today_str}`

---

## 📥 Note in Staging (Inbox / Bozze)
Elenco delle note attualmente nello stato di `draft` o `in-progress` che richiedono rielaborazione o smistamento definitivo.

{staging_table}

---

## 🌱 Semi del Blog (Bozze Quartz)
Bozze di articoli contrassegnate come `seed 🌱` o `growing 🌿` destinate a essere rifinite e pubblicate.

{blog_table}

---

## 🕒 Note Modificate di Recente
Le ultime 10 note modificate nel Vault (escluse le note del calendario).

{recent_table}

---

## 🛠️ Diagnostica Statica (/audit)
Per eseguire un check-up completo del grafo (note orfane, link interrotti, frontmatter mancanti), chiedi all'agente AI di eseguire il comando `/audit` o lancia manualmente lo script:

```bash
python3 .agents/skills/audit/scripts/audit_vault.py
```

*Il report statico generato sarà disponibile in:* `03 - Inbox/Audit Report - YYYY-MM-DD.md`.

---
## Collegamenti
- [[Home MOC]]
- [[AI Second Brain System]]
"""

    dashboard_path = os.path.join(vault_root, "02 - Atlas/Obsidian Second Brain/Vault Health Dashboard.md")
    try:
        with open(dashboard_path, 'w', encoding='utf-8') as fw:
            fw.write(dashboard_content)
        print(f"Vault Health Dashboard aggiornata con successo in puro Markdown.")
    except Exception as e:
        print(f"Errore durante la scrittura della dashboard: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
