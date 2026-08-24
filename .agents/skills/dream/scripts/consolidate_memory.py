#!/usr/bin/env python3
# consolidate_memory.py - Script di consolidamento e indicizzazione per la skill /dream.
# Analizza i segnali estratti e genera/aggiorna i file topic e MEMORY.md.

import os
import sys
import json
import datetime
import subprocess

def run_signal_extraction(vault_root):
    """Lancia lo script dream_consolidate.py e ritorna i segnali estratti in formato dict."""
    script_path = os.path.join(vault_root, ".agents/skills/dream/scripts/dream_consolidate.py")
    if not os.path.exists(script_path):
        print(f"Errore: Script di estrazione segnali non trovato in {script_path}", file=sys.stderr)
        return None
        
    try:
        res = subprocess.run([sys.executable, script_path, "30"], cwd=vault_root, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Errore durante l'estrazione dei segnali: {e}", file=sys.stderr)
        return None

def write_topic_file(vault_root, filename, title, content_lines):
    """Scrive o aggiorna un file di memoria topic."""
    path = os.path.join(vault_root, ".agents/memory", filename)
    
    # Intestazione standard
    header = f"""---
title: "{title}"
date: {datetime.date.today().strftime("%Y-%m-%d")}
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY|Memory Index]]

# 🧠 Memory Topic: {title}

"""
    body = "\n".join(content_lines)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header + body + "\n")
        print(f"  -> Scritto topic di memoria: {filename}")
    except Exception as e:
        print(f"Errore nella scrittura del file {filename}: {e}", file=sys.stderr)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..'))
    
    print("Avvio della fase di consolidamento della memoria...")
    signals = run_signal_extraction(vault_root)
    
    if not signals:
        print("Impossibile procedere senza segnali.", file=sys.stderr)
        sys.exit(1)
        
    # Crea la directory memory se non esiste
    os.makedirs(os.path.join(vault_root, ".agents/memory"), exist_ok=True)
    
    # 1. COMPILA USER PROFILE
    user_profile = [
        "## Informazioni Generali",
        "- **Nome Utente:** Lorenzo",
        "- **Corso di Studi:** Laurea Triennale in Ingegneria Informatica",
        "- **Ruolo dell'Agente AI:** Co-pilota e \"giardiniere digitale\" per la gestione e riordino del Second Brain.",
        "",
        "## Obiettivi e Focus",
        "- Studio e consolidamento di appunti universitari.",
        "- Sviluppo di progetti personali (es. Quartz per la pubblicazione web).",
        "- Ottimizzazione e automazione dei flussi GTD."
    ]
    write_topic_file(vault_root, "user-profile.md", "User Profile", user_profile)
    
    # 2. COMPILA VAULT CONVENTIONS
    vault_conventions = [
        "## Naming Conventions",
        "- I file devono seguire la convenzione **Title Case** (es. `Nome Della Nota.md`).",
        "- Rimuovere emoji e caratteri speciali non standard dai nomi dei file per compatibilità Quartz.",
        "",
        "## Struttura delle Directory (ACE Modificato)",
        "- `Map of Content/`: Indici semantici generali (MOC).",
        "- `Atlas/`: Conoscenza consolidata (Corsi, Mentality, Finance, Tecnology, Prompt).",
        "- `Inbox/`: Punto di atterraggio per bozze e note da elaborare.",
        "- `04 - Calendar/`: Journaling e tracciamento temporale.",
        "- `Blog/`: Articoli pronti o in lavorazione per la pubblicazione web.",
        "- `Meta/`: Template e script di configurazione.",
        "",
        "## Convenzioni del Frontmatter YAML",
        "- Campi obbligatori Atlas/Scuola: `title`, `date`, `updated`, `tags`, `status`, `macro_area`.",
        "- Campi obbligatori Blog: `title`, `date`, `tags`, `stage`, `summary`, `draft`.",
        "- **Idempotenza:** Ripulire i backslash accumulati nei doppi apici (es. `\\\"` -> `\"`) prima di salvare lo YAML."
    ]
    write_topic_file(vault_root, "vault-conventions.md", "Vault Conventions", vault_conventions)
    
    # 3. COMPILA TECH STACK
    tech_stack = [
        "## Strumenti Principali",
        "- **Obsidian:** Gestione del grafo di note in Markdown.",
        "- **Vibe Coding / Cursor:** Sviluppo assistito da LLM.",
        "- **Quartz:** Framework per generare e ospitare il blog statico.",
        "- **Python / Bash:** Script di linter e automazione (`tidy_vault.py`, `lint_yaml.py`, `watch.sh`, `ingest.sh`).",
        "- **NotebookLM:** Generatore di appunti di studio universitari tramite server MCP."
    ]
    write_topic_file(vault_root, "tech-stack.md", "Tech Stack", tech_stack)
    
    # 4. COMPILA ACTIVE PROJECTS
    active_projects = [
        "## Progetti in Corso",
        "- **AI Second Brain System:** Consolidamento di MOC e automazione del riordino (Fase 0-3 completata).",
        "- **Laurea Triennale Ing. Informatica:** Appunti e sintesi dei corsi accademici.",
        "- **Blog Quartz:** Stesura e pubblicazione di articoli di divulgazione tecnica.",
        "- **Inbox Ingestion Automation:** Watcher di cartella (`watch.sh` + `ingest.sh` in background via `.zshrc`) per elaborare in automatico le note grezze."
    ]
    write_topic_file(vault_root, "active-projects.md", "Active Projects", active_projects)
    
    # 5. COMPILA CORRECTIONS LOG (Analisi dei segnali reali)
    corrections_list = []
    
    # Mappa le correzioni reali individuate nei transcript
    raw_corrections = signals.get('corrections', [])
    
    # Aggiungi preferenze note basandoci sul linter
    corrections_list.append("## Regole Critiche & Correzioni Rilevate")
    
    # Rilevamento manuale di pattern noti per garantire che non vadano persi
    corrections_list.append("- **[STRICT] No Dataview in Dashboard:** Non utilizzare blocchi ```dataview. La dashboard deve essere scritta in puro Markdown statico autogenerato per massima compatibilità.")
    corrections_list.append("- **[STRICT] Quartz Blog Stages:** Mantenere i livelli di `stage` personalizzati e non standard (es. `seed 🌱`, `growing 🌿`) nel frontmatter del Blog.")
    corrections_list.append("- **[STRICT] Note Generation Priority:** Le note universitarie di studio devono essere generate a partire da scheletri strutturati, espandendo i concetti in italiano con markup di evidenziazione colorata.")
    corrections_list.append("- **[STRICT] Naming Title Case:** Non usare mai trattini (kebab-case) nei nomi dei file nel vault. Utilizzare sempre il **Title Case intelligente** con spazi, mantenendo articoli, congiunzioni e preposizioni in minuscolo (es. Nome della Nota.md).")
    
    if raw_corrections:
        corrections_list.append("\n## Segnali ed Espressioni Rilevate nei Transcript")
        # Prendi le ultime 10 e formattale pulite
        unique_raw = list(set(raw_corrections))[:10]
        for rc in unique_raw:
            # Pulisci a capo e whitespace
            cleaned_rc = " ".join(rc.split())
            corrections_list.append(f"- *Rilevato:* \"{cleaned_rc[:180]}...\"")
            
    write_topic_file(vault_root, "corrections-log.md", "Corrections Log", corrections_list)
    
    # 6. GENERA MEMORY.md PRINCIPALE (INDEX)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    memory_content = f"""---
title: "MEMORY"
date: {datetime.date.today().strftime("%Y-%m-%d")}
updated: {datetime.date.today().strftime("%Y-%m-%dT%H:%M")}
tags: [meta, memory, index]
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY]]

# 🧠 Agent Memory — Ken Vault

> Ultima consolidazione: `{today_str}`
> Sessioni analizzate: {signals.get('conversations_analyzed', 0)} | Segnali estratti: {signals.get('total_signals', 0)}
> Questa memoria viene letta automaticamente all'avvio delle nuove sessioni per mantenere la continuità e allineare il contesto.

---

## 👤 Profilo Utente
*Dettagli completi in [[User Profile]].*
- **Utente:** Lorenzo, studente di Ingegneria Informatica.
- **Obiettivo:** Co-pilotare l'organizzazione automatica del Second Brain e lo studio accademico.

## 📋 Convenzioni Critiche (Non Regredire)
*Dettagli completi in [[Corrections Log]].*
- **[STRICT]** **Niente Dataview:** La dashboard e le visualizzazioni aggregate devono usare **puro Markdown statico**.
- **[STRICT]** **Blog Stages:** I tag di `stage` in `Blog` (es. `seed 🌱`, `growing 🌿`) non devono essere normalizzati o alterati.
- **[STRICT]** **Naming Title Case:** Non usare mai trattini (kebab-case) nei nomi dei file nel vault. Utilizzare sempre il **Title Case intelligente** con spazi, mantenendo articoli, congiunzioni e preposizioni in minuscolo (es. Nome della Nota.md).
- **[STRICT]** **Directory Skills:** Le skills risiedono in `.agents/skills/<skill_name>/SKILL.md`.

## ⚙️ Convenzioni del Vault
*Dettagli completi in [[Vault Conventions]].*
- Naming in **Title Case** senza emoji per compatibilità con l'hosting web Quartz.
- Organizzazione in 6 cartelle principali (struttura ACE modificata).

## 🛠️ Stack Tecnologico
*Dettagli completi in [[Tech Stack]].*
- Obsidian + Quartz + Python Linting + NotebookLM MCP.

---
## Collegamenti
- [[Home MOC]]
- [[AI Second Brain System]]
- [[Vault Health Dashboard]]
"""
    
    memory_index_path = os.path.join(vault_root, ".agents/MEMORY.md")
    try:
        with open(memory_index_path, 'w', encoding='utf-8') as f:
            f.write(memory_content)
        print("Memory Index (MEMORY.md) generato con successo.")
    except Exception as e:
        print(f"Errore nella scrittura di MEMORY.md: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
