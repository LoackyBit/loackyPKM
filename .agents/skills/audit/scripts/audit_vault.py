#!/usr/bin/env python3
# audit_vault.py - Health check linter per l'AI Second Brain.
# Rileva note orfane, link interrotti, tag inconsistenti e frontmatter mancanti.

import os
import re
import datetime
import sys

def parse_yaml_frontmatter(content):
    metadata = {}
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return None
    
    closing_idx = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            closing_idx = idx
            break
            
    if closing_idx == -1:
        return None
        
    fm_text = "\n".join(lines[1:closing_idx])
    
    # Parsing basilare dello YAML
    current_key = None
    list_items = []
    for line in fm_text.split('\n'):
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
    vault_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..'))
    
    ignore_folders = {'.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode', '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy'}
    
    # 1. Trova tutte le note esistenti
    all_notes = {}  # {clean_name: relative_path}
    note_paths = set()  # relative_paths
    
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_folders and not d.startswith('.')]
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, vault_root)
                clean_name = file[:-3]
                all_notes[clean_name] = rel_path
                note_paths.add(rel_path)
                
    # 2. Analizza i link e il frontmatter
    incoming_links = {name: set() for name in all_notes} # {clean_name: {clean_names_of_sources}}
    broken_links = {} # {relative_path: [broken_targets]}
    missing_frontmatter = []
    malformed_frontmatter = []
    
    link_pattern = re.compile(r'\[\[([^|#\]]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]')
    
    for clean_name, rel_path in all_notes.items():
        abs_path = os.path.join(vault_root, rel_path)
        try:
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
            
        # Controlla Frontmatter
        metadata = parse_yaml_frontmatter(content)
        is_calendar = rel_path.startswith("04 - Calendar")
        
        if not is_calendar:
            if metadata is None:
                missing_frontmatter.append(rel_path)
            else:
                required = ['title', 'date', 'tags']
                if not rel_path.startswith("05 - Blog"):
                    required.extend(['status', 'macro_area'])
                else:
                    required.extend(['stage', 'draft'])
                    
                missing_fields = [field for field in required if field not in metadata or not metadata[field]]
                if missing_fields:
                    malformed_frontmatter.append((rel_path, missing_fields))
                    
        # Cerca link nel corpo (escludendo il frontmatter)
        body_content = content
        if content.startswith('---'):
            end_fm = content.find('---', 3)
            if end_fm != -1:
                body_content = content[end_fm+3:]
                
        # Estrai tutti i link wiki
        links = link_pattern.findall(body_content)
        for link in links:
            target = link.strip()
            if not target:
                continue
            if target in all_notes:
                if target != clean_name: # evita self-links
                    incoming_links[target].add(clean_name)
            else:
                # Gestione caso speciale: link a file fisici completi di estensione o link ad allegati
                if not (target.endswith('.png') or target.endswith('.jpg') or target.endswith('.pdf')):
                    if rel_path not in broken_links:
                        broken_links[rel_path] = []
                    broken_links[rel_path].append(target)
                    
    # 3. Identifica note orfane
    orphan_notes = []
    for clean_name, rel_path in all_notes.items():
        # Escludi le note in 99 - Meta, 04 - Calendar, 01 - Map of Content
        if rel_path.startswith("99 - Meta") or rel_path.startswith("04 - Calendar") or rel_path.startswith("01 - Map of Content") or clean_name == "Home MOC":
            continue
        
        # Una nota è orfana se non ha link entranti
        if not incoming_links[clean_name]:
            orphan_notes.append(rel_path)
            
    # Ordina i risultati
    orphan_notes.sort()
    missing_frontmatter.sort()
    malformed_frontmatter.sort(key=lambda x: x[0])
    
    # 4. Scrivi il report in 03 - Inbox/
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    report_filename = f"Audit Report - {today_str}.md"
    report_rel_path = os.path.join("03 - Inbox", report_filename)
    report_abs_path = os.path.join(vault_root, report_rel_path)
    
    os.makedirs(os.path.dirname(report_abs_path), exist_ok=True)
    
    report = []
    report.append(f"""---
title: "Audit Report - {today_str}"
date: {today_str}
tags: [audit, meta, system-health]
status: draft
macro_area: meta
---
[[Home MOC|Home]] / [[Tech & AI MOC|Tech & AI]] / [[{report_filename[:-3]}]]

# 📊 Report di Audit della Salute del Vault — {today_str}

Diagnostica automatica dello stato di coerenza e integrità semantica del Second Brain.

## 📈 Riepilogo Diagnostico

- **Note totali scansionate:** {len(all_notes)}
- **Note orfane rilevate:** {len(orphan_notes)}
- **File con link interrotti (broken links):** {len(broken_links)}
- **File con frontmatter YAML mancante:** {len(missing_frontmatter)}
- **File con frontmatter YAML malformato/incompleto:** {len(malformed_frontmatter)}

---

## 🔴 Criticità Elevate

""")

    if not broken_links and not missing_frontmatter and not malformed_frontmatter:
        report.append("✅ **Nessuna criticità elevata rilevata!** Il frontmatter e i collegamenti del Vault sono integri.\n\n")
    else:
        if broken_links:
            report.append("### 🔗 Link Interrotti (Broken Links)\n")
            report.append("Wiki-links che fanno riferimento a note o file inesistenti:\n\n")
            for source, targets in sorted(broken_links.items()):
                report.append(f"- [[{os.path.basename(source)[:-3]}]] (in `{source}`):\n")
                for t in targets:
                    report.append(f"  - Punta a: `{t}`\n")
            report.append("\n")
            
        if missing_frontmatter:
            report.append("### 📝 Frontmatter YAML Mancante\n")
            report.append("File sprovvisti di intestazione metadati `---`:\n\n")
            for f in missing_frontmatter:
                report.append(f"- [[{os.path.basename(f)[:-3]}]] (`{f}`)\n")
            report.append("\n")
            
        if malformed_frontmatter:
            report.append("### ⚠️ Frontmatter YAML Incompleto\n")
            report.append("File che hanno campi mancanti o vuoti nello YAML:\n\n")
            for f, fields in malformed_frontmatter:
                fields_str = ", ".join([f"`{field}`" for field in fields])
                report.append(f"- [[{os.path.basename(f)[:-3]}]] (`{f}`) — Campi mancanti: {fields_str}\n")
            report.append("\n")
            
    report.append("---\n\n## 🟡 Attenzioni (Warning)\n\n")
    
    if not orphan_notes:
        report.append("✅ **Nessuna nota orfana rilevata!** Tutte le note del Vault sono connesse a MOC o ad altre note.\n\n")
    else:
        report.append("### 🕸️ Note Orfane (Isolate)\n")
        report.append("Note attive che non hanno nessun link entrante (inbound) e non sono collegate alle MOC:\n\n")
        for f in orphan_notes:
            report.append(f"- [[{os.path.basename(f)[:-3]}]] (`{f}`)\n")
        report.append("\n")
        
    report.append("""
---
## Collegamenti
- [[Home MOC]]
- [[AI Second Brain System]]
""")

    try:
        with open(report_abs_path, 'w', encoding='utf-8') as fw:
            fw.write("".join(report))
        print(f"Audit completato con successo. Report salvato in: {report_rel_path}")
        print(f"Statistiche: Note: {len(all_notes)} | Orfane: {len(orphan_notes)} | Rotti: {len(broken_links)} | Mancanti YAML: {len(missing_frontmatter)}")
    except Exception as e:
        print(f"Errore durante il salvataggio del report: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
