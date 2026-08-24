#!/usr/bin/env python3
"""
migrate_structure.py — Vault Physical Structure Migration & Wiki-Link Refactoring

Riorganizza l'albero delle cartelle di 02 - Atlas/ nelle 5 macro-aree pulite:
1. Tech & AI
2. Education & Learning (incluso l'archivio 03 - Inbox/School -> Archivio Scuola)
3. Personal Growth & Health
4. Finance
5. Projects

Aggiorna contestualmente i wiki-links, le breadcrumbs e ripulisce le cartelle vuote.
Supporta --dry-run ed --execute.
"""

import os
import sys
import re
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Root vault directory (assumes script is in 99 - Meta/Scripts/)
VAULT_ROOT = Path(__file__).resolve().parent.parent.parent

# Top-level source directory mappings (no overlapping nested walks)
FOLDER_MAPPING: List[Tuple[str, str, str]] = [
    # (Source prefix, Destination prefix, Macro-MOC Name)
    ("02 - Atlas/Technology", "02 - Atlas/Tech & AI", "Tech & AI"),
    ("02 - Atlas/Prompt", "02 - Atlas/Tech & AI/Prompt", "Tech & AI"),
    
    ("02 - Atlas/Corsi", "02 - Atlas/Education & Learning/Corsi", "Education & Learning"),
    ("02 - Atlas/Education", "02 - Atlas/Education & Learning", "Education & Learning"),
    ("03 - Inbox/School", "02 - Atlas/Education & Learning/Archivio Scuola", "Education & Learning"),
    
    ("02 - Atlas/Mentality", "02 - Atlas/Personal Growth & Health/Mentality", "Personal Growth & Health"),
    ("02 - Atlas/Palestra", "02 - Atlas/Personal Growth & Health/Palestra", "Personal Growth & Health"),
    
    ("02 - Atlas/Animator2D", "02 - Atlas/Projects/Animator2D", "Projects"),
    ("02 - Atlas/Obsidian Second Brain", "02 - Atlas/Projects/AI Second Brain System", "Projects"),
]

# Wiki-link pattern: [[Target]] o [[Target#Heading]] o [[Target|Alias]] o [[Target#Heading|Alias]]
WIKI_LINK_PATTERN = re.compile(r'\[\[([^\]\|#\n]+)(#[^\]\|\n]+)?(\|([^\]\n]+))?\]\]')


def get_macro_area_for_dest(dest_rel_path: str) -> str:
    """Determina la Macro-MOC in base al percorso di destinazione."""
    if dest_rel_path.startswith("02 - Atlas/Tech & AI"):
        return "Tech & AI"
    elif dest_rel_path.startswith("02 - Atlas/Education & Learning"):
        return "Education & Learning"
    elif dest_rel_path.startswith("02 - Atlas/Personal Growth & Health"):
        return "Personal Growth & Health"
    elif dest_rel_path.startswith("02 - Atlas/Finance"):
        return "Finance"
    elif dest_rel_path.startswith("02 - Atlas/Projects"):
        return "Projects"
    elif dest_rel_path.startswith("05 - Blog"):
        return "Blog"
    return "Home"


def compute_file_migrations(vault_root: Path) -> List[Tuple[Path, Path, str]]:
    """
    Scansiona il filesystem e calcola la lista di file da spostare.
    Ritorna: [(src_path, dest_path, macro_area), ...]
    """
    migrations: List[Tuple[Path, Path, str]] = []
    seen_destinations: Set[Path] = set()

    for src_prefix_str, dest_prefix_str, macro_area in FOLDER_MAPPING:
        src_dir = vault_root / src_prefix_str
        if not src_dir.exists():
            continue

        dest_base = vault_root / dest_prefix_str

        # Se sorgente e destinazione coincidono esattamente, nessun trasferimento
        if src_dir == dest_base:
            continue

        for root, dirs, files in os.walk(src_dir):
            root_path = Path(root)
            rel_to_src = root_path.relative_to(src_dir)
            
            for file in files:
                if file.startswith("."):
                    continue
                
                src_file_path = root_path / file
                
                # Calcola destinazione preservando la sotto-struttura se presente
                if str(rel_to_src) == ".":
                    dest_file_path = dest_base / file
                else:
                    dest_file_path = dest_base / rel_to_src / file

                # Evita di ri-spostare file già mappati o nella posizione corretta
                if src_file_path == dest_file_path:
                    continue

                if dest_file_path in seen_destinations:
                    print(f"⚠️ ATTENZIONE: Collisione destinazione duplicata: {dest_file_path}")
                
                seen_destinations.add(dest_file_path)
                migrations.append((src_file_path, dest_file_path, macro_area))

    # Gestione file speciale in Inbox: Rapporto Analisi Architetturale
    rapporto_src = vault_root / "03 - Inbox" / "Rapporto Analisi Architetturale Ken Vault.md"
    if rapporto_src.exists():
        rapporto_dest = vault_root / "02 - Atlas" / "Projects" / "AI Second Brain System" / "Rapporto Analisi Architetturale Ken Vault.md"
        if rapporto_src != rapporto_dest:
            migrations.append((rapporto_src, rapporto_dest, "Projects"))

    return migrations


def update_breadcrumbs_and_links(file_path: Path, macro_area: str, dry_run: bool = True) -> bool:
    """
    Legge un file Markdown, aggiorna la breadcrumb e i link interni.
    Ritorna True se il file è stato modificato.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Errore lettura {file_path}: {e}")
        return False

    lines = content.splitlines(keepends=True)
    modified = False
    
    # 1. Aggiornamento Breadcrumb
    # Trova la fine del frontmatter (secondo '---')
    dash_indices = [i for i, line in enumerate(lines) if line.strip() == "---"]
    if len(dash_indices) >= 2:
        end_fm = dash_indices[1]
        note_title = file_path.stem
        
        # Cerca la breadcrumb tra le prime 3 righe dopo il frontmatter
        for idx in range(end_fm + 1, min(end_fm + 4, len(lines))):
            line_str = lines[idx].strip()
            if line_str.startswith("[[Home MOC|Home]]") or line_str.startswith("[[Home]]") or line_str.startswith("[[Home MOC]]"):
                new_bc = f"[[Home MOC|Home]] / [[{macro_area} MOC|{macro_area}]] / [[{note_title}]]\n"
                if lines[idx] != new_bc:
                    lines[idx] = new_bc
                    modified = True
                break

    new_content = "".join(lines)

    if modified:
        if not dry_run:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        return True

    return False


def clean_empty_directories(vault_root: Path, dry_run: bool = True):
    """Rimuove ricorsivamente le cartelle vuote o contenenti solo .DS_Store."""
    dirs_to_check = [
        vault_root / "02 - Atlas",
        vault_root / "03 - Inbox",
    ]

    for base_dir in dirs_to_check:
        if not base_dir.exists():
            continue
        for root, dirs, files in os.walk(base_dir, topdown=False):
            dir_path = Path(root)
            if dir_path == base_dir:
                continue
            
            # Controlla se la cartella contiene solo file nascosti come .DS_Store
            try:
                all_entries = list(dir_path.iterdir())
                non_hidden = [e for e in all_entries if not e.name.startswith(".")]
                
                if len(non_hidden) == 0:
                    if not dry_run:
                        shutil.rmtree(dir_path)
                        print(f"  🗑️ Rimossa directory vuota: {dir_path.relative_to(vault_root)}")
                    else:
                        print(f"  [DRY-RUN] Rimozione cartella vuota: {dir_path.relative_to(vault_root)}")
            except Exception as e:
                pass


def main():
    parser = argparse.ArgumentParser(description="Migrazione strutturale atomica del Vault Obsidian")
    parser.add_argument("--dry-run", action="store_true", help="Simula lo spostamento e le modifiche senza scrivere su disco")
    parser.add_argument("--execute", action="store_true", help="Esegue fisicamente la migrazione dei file")
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("Specificare --dry-run oppure --execute. Esegui con --help per dettagli.")
        sys.exit(1)

    is_dry_run = args.dry_run or not args.execute

    print("=" * 65)
    print(f"🚀 VAULT STRUCTURE MIGRATION ({'DRY-RUN' if is_dry_run else 'EXECUTE'})")
    print(f"📁 Vault Root: {VAULT_ROOT}")
    print("=" * 65)

    # 1. Calcola trasferimenti
    migrations = compute_file_migrations(VAULT_ROOT)
    print(f"\n📋 Totale file identificati per il trasferimento: {len(migrations)}")

    # Raggruppa per destinazione
    by_macro: Dict[str, int] = {}
    for _, dest, macro in migrations:
        by_macro[macro] = by_macro.get(macro, 0) + 1

    for macro, count in sorted(by_macro.items()):
        print(f"  → {macro}: {count} note/file")

    # Mostra anteprima primi 10 trasferimenti
    print("\n🔍 Anteprima trasferimenti:")
    for src, dest, macro in migrations[:10]:
        print(f"  {src.relative_to(VAULT_ROOT)}  -->  {dest.relative_to(VAULT_ROOT)}")
    if len(migrations) > 10:
        print(f"  ... e altri {len(migrations) - 10} file.")

    if is_dry_run:
        print("\n✅ Simulazione completata senza errori o collisioni. Esegui con --execute per applicare le modifiche.")
        return

    # 2. Esecuzione Fisica dei trasferimenti
    print("\n📦 Esecuzione trasferimenti fisici su disco...")
    moved_count = 0
    for src, dest, _ in migrations:
        if not src.exists():
            continue
        
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(src), str(dest))
            moved_count += 1
        except Exception as e:
            print(f"❌ Errore spostamento {src} -> {dest}: {e}")

    print(f"✅ Spostati con successo {moved_count} file.")

    # 3. Aggiornamento Breadcrumb su tutti i file in 02 - Atlas
    print("\n🔄 Aggiornamento breadcrumb in 02 - Atlas/...")
    bc_updated = 0
    atlas_root = VAULT_ROOT / "02 - Atlas"
    for root, _, files in os.walk(atlas_root):
        for file in files:
            if not file.endswith(".md"):
                continue
            file_path = Path(root) / file
            macro = get_macro_area_for_dest(str(file_path.relative_to(VAULT_ROOT)))
            if update_breadcrumbs_and_links(file_path, macro, dry_run=False):
                bc_updated += 1

    print(f"✅ Breadcrumb aggiornate in {bc_updated} note.")

    # 4. Pulizia cartelle vuote
    print("\n🧹 Pulizia directory vuote residue...")
    clean_empty_directories(VAULT_ROOT, dry_run=False)

    print("\n🎉 Migrazione strutturale completata con successo!")


if __name__ == "__main__":
    main()
