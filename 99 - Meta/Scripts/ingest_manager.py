#!/usr/bin/env python3
# ingest_manager.py - Orchestratore deterministico per l'ingestione del Second Brain.

import os
import sys
import re
import subprocess
import threading
import time
import datetime
import atexit

# Configurazione percorsi
VAULT_PATH = "/Users/lorenzo/Library/Mobile Documents/iCloud~md~obsidian/Documents/Ken vault"
INBOX_PATH = os.path.join(VAULT_PATH, "03 - Inbox")
DASHBOARD_FILE = os.path.join(INBOX_PATH, "Review Dashboard.md")
LOG_DIR = os.path.join(VAULT_PATH, "99 - Meta/logs")
LOG_FILE = os.path.join(LOG_DIR, "ingest.log")
LOCK_DIR = "/tmp/secondbrain_ingest.lock"

CONTENT_MEMORY_FILE = os.path.join(VAULT_PATH, "02 - Atlas/Prompt/Content Memory.md")
STYLE_GUIDE_FILE = os.path.join(VAULT_PATH, "99 - Meta/Style Guide.md")
TEMPLATE_DIR = os.path.join(VAULT_PATH, "99 - Meta/Template")

# Regex per analizzare le approvazioni/rifiuti nella Dashboard
RE_APPROVAL = re.compile(
    r'^\s*-\s+\[(?P<status>[ x-])\]\s+Approva\s+\[\[proposed-(?P<name>[^\]]+)\]\]\s+\(originale:\s+\[\[raw-(?P<raw>[^\]]+)\]\]\)'
)

# Mutex Lock per prevenire esecuzioni concorrenti
def acquire_lock():
    try:
        os.mkdir(LOCK_DIR)
        return True
    except FileExistsError:
        return False

def release_lock():
    try:
        os.rmdir(LOCK_DIR)
    except Exception:
        pass

# Registra il rilascio del lock all'uscita dello script
atexit.register(release_lock)

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"{timestamp} - {message}"
    print(formatted)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as lf:
            lf.write(formatted + "\n")
    except Exception as e:
        sys.stderr.write(f"Impossibile scrivere nel log: {e}\n")

class ProcessTerminator:
    """Monitora l'esistenza del file grezzo e termina attivamente i processi associati se viene eliminato."""
    def __init__(self, raw_file_path):
        self.raw_file_path = raw_file_path
        self.process = None
        self.stop_event = threading.Event()
        self.killed = False
        self.thread = None

    def start_monitoring(self, process):
        self.process = process
        self.stop_event.clear()
        self.killed = False
        self.thread = threading.Thread(target=self._monitor)
        self.thread.daemon = True
        self.thread.start()

    def stop_monitoring(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1.0)

    def _monitor(self):
        while not self.stop_event.is_set():
            if not os.path.exists(self.raw_file_path):
                log(f"Rilevata eliminazione del file '{self.raw_file_path}'. Terminazione processi attivi...")
                self.killed = True
                if self.process:
                    try:
                        self.process.terminate()
                        # Attendiamo brevemente che esca in modo pulito
                        for _ in range(10):
                            if self.process.poll() is not None:
                                break
                            time.sleep(0.1)
                        else:
                            self.process.kill()
                    except Exception as e:
                        log(f"Errore durante l'interruzione del processo: {e}")
                break
            time.sleep(0.5)

def read_dashboard():
    pending = []
    approvals = []
    rejections = []
    
    if not os.path.exists(DASHBOARD_FILE):
        return pending, approvals, rejections
        
    try:
        with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            match = RE_APPROVAL.match(line)
            if match:
                status = match.group('status')
                name = match.group('name')
                raw = match.group('raw')
                entry = {'name': name, 'raw': raw, 'line': line.strip()}
                if status == ' ':
                    pending.append(entry)
                elif status == 'x':
                    approvals.append(entry)
                elif status == '-':
                    rejections.append(entry)
    except Exception as e:
        log(f"Errore nella lettura della Dashboard: {e}")
        
    return pending, approvals, rejections

def rewrite_dashboard(processing_notes, pending_approvals):
    try:
        content = f"""---
title: "Review Dashboard"
date: {datetime.date.today().strftime("%Y-%m-%d")}
tags: [meta, dashboard, review]
status: permanent
macro_area: meta
---

# 📥 Inbox Review Dashboard

Benvenuto nella **Dashboard di Revisione dell'Inbox**. Questo pannello ti permette di revisionare, perfezionare e approvare le note grezze catturate per integrarle armoniosamente nel tuo Second Brain.

## ⚙️ Istruzioni per la Revisione
* Per **APPROVARE** una proposta: Sostituisci `[ ]` con `[x]` o premi CLICK (sarà spostata nella cartella di destinazione definitiva del Vault con metadati aggiornati).
* Per **RIFIUTARE** una proposta: Sostituisci `[ ]` con `[-]` o premi CTRL+CLICK (la proposta e il file grezzo verranno eliminati definitivamente dall'Inbox).
"""
        
        if processing_notes:
            content += "\n## ⏳ In Elaborazione\n\n"
            for title, status in processing_notes.items():
                content += f"- ⏳ [[{title}]] ({status})\n"
                
        content += "\n## 📋 Note in Attesa di Approvazione\n\n"
        if pending_approvals:
            for app in pending_approvals:
                content += f"- [ ] Approva [[proposed-{app['name']}]] (originale: [[raw-{app['raw']}]])\n"
        else:
            content += "Tutte le note sono state elaborate con successo! Dashboard vuota.\n"
            
        with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        log(f"Errore nella scrittura della Dashboard: {e}")

def clean_double_frontmatter(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith("---\ntitle: \"Raw Inbox Note\"") or content.startswith("---\ntitle: 'Raw Inbox Note'"):
            parts = content.split('---\n')
            if len(parts) >= 4:
                # Ricostruisci il file a partire dal secondo frontmatter
                new_content = "---\n" + "---\n".join(parts[3:])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                log(f"Pulito doppio frontmatter in: {file_path}")
                return True
    except Exception as e:
        log(f"Errore pulizia doppio frontmatter: {e}")
    return False

def fix_highlight_backticks(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex per catturare e rimuovere i backticks che racchiudono i tag <mark>...</mark>
        pattern = r'`(<mark\s+style="[^"]*">.*?</mark>)`'
        
        fixed_content, count = re.subn(pattern, r'\1', content, flags=re.DOTALL)
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            log(f"Corrette {count} evidenziazioni HTML racchiuse tra backticks in: {file_path}")
            return True
    except Exception as e:
        log(f"Errore durante la correzione delle evidenziazioni tra backticks: {e}")
    return False



def is_ready_raw_file(file_path):
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            if re.search(r'^ready:\s*true', frontmatter, re.IGNORECASE | re.MULTILINE):
                return True
    except Exception:
        pass
    return False

def get_video_url_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^video_url:\s*"(.*?)"', content, re.MULTILINE)
        if not match:
            match = re.search(r'^video_url:\s*(.*?)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    except Exception:
        pass
    return None

def needs_youtube_helper(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "## 📝 Testo Grezzo della Trascrizione" in content:
            return True
        if not re.search(r'^##\s+', content, re.MULTILINE):
            return True
    except Exception:
        pass
    return False

def process_approval(entry):
    name = entry['name']
    raw = entry['raw']
    proposed_file = os.path.join(INBOX_PATH, f"proposed-{name}.md")
    raw_file = os.path.join(INBOX_PATH, f"raw-{raw}.md")
    
    if not os.path.exists(proposed_file):
        log(f"File proposto non trovato per l'approvazione: {proposed_file}")
        return False
        
    try:
        with open(proposed_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match_fm = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match_fm:
            log(f"Frontmatter YAML non trovato in: {proposed_file}")
            return False
            
        frontmatter = match_fm.group(1)
        target_path_match = re.search(r'^target_path:\s*"(.*?)"', frontmatter, re.MULTILINE)
        if not target_path_match:
            target_path_match = re.search(r'^target_path:\s*(.*?)$', frontmatter, re.MULTILINE)
            
        if not target_path_match:
            log(f"target_path non impostato nel frontmatter di {proposed_file}")
            return False
            
        target_rel = target_path_match.group(1).strip().strip('"').strip("'")
        dest_file = os.path.join(VAULT_PATH, target_rel)
        
        # Pulizia ed elaborazione del frontmatter
        updated_fm = frontmatter
        # Rimuove la riga target_path
        updated_fm = re.sub(r'^target_path:.*?(\r?\n|$)', '', updated_fm, flags=re.MULTILINE)
        # Aggiorna lo status
        if re.search(r'^status:\s*review', updated_fm, re.MULTILINE):
            updated_fm = re.sub(r'^status:\s*review', 'status: permanent', updated_fm, flags=re.MULTILINE)
        elif not re.search(r'^status:', updated_fm, re.MULTILINE):
            updated_fm += "\nstatus: permanent"
            
        # Ricostruisce il file
        updated_content = content[:match_fm.start(1)] + updated_fm + content[match_fm.end(1):]
        
        # Sposta e salva deterministicamente
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        # Elimina i file temporanei
        if os.path.exists(proposed_file):
            os.remove(proposed_file)
        if os.path.exists(raw_file):
            os.remove(raw_file)
            
        log(f"Nota approvata e archiviata con successo: {proposed_file} -> {dest_file}")
        return True
    except Exception as e:
        log(f"Errore durante l'approvazione di {proposed_file}: {e}")
        return False

def process_rejection(entry):
    name = entry['name']
    raw = entry['raw']
    proposed_file = os.path.join(INBOX_PATH, f"proposed-{name}.md")
    raw_file = os.path.join(INBOX_PATH, f"raw-{raw}.md")
    
    try:
        if os.path.exists(proposed_file):
            os.remove(proposed_file)
        if os.path.exists(raw_file):
            os.remove(raw_file)
        log(f"Nota rifiutata. Eliminati: proposed-{name}.md e raw-{raw}.md")
        return True
    except Exception as e:
        log(f"Errore durante il rifiuto dei file per {name}: {e}")
        return False

def run_command_with_monitor(cmd, raw_file_path, on_line_callback=None):
    terminator = ProcessTerminator(raw_file_path)
    try:
        env = os.environ.copy()
        env['PATH'] = f"/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env.get('PATH', '')}"
        env['PYTHONUNBUFFERED'] = '1'
        
        # Confluiamo stderr in stdout per evitare deadlock e leggere tutto in streaming
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env)
        terminator.start_monitoring(proc)
        
        stdout_lines = []
        # Legge l'output in tempo reale
        for line in proc.stdout:
            stdout_lines.append(line)
            if on_line_callback:
                on_line_callback(line)
                
        proc.wait()
        terminator.stop_monitoring()
        
        stdout = "".join(stdout_lines)
        
        if terminator.killed:
            return False, "Processo interrotto dall'utente"
            
        if proc.returncode != 0:
            return False, stdout or f"Codice d'uscita: {proc.returncode}"
            
        return True, stdout
    except Exception as e:
        terminator.stop_monitoring()
        return False, str(e)

def main():
    if not acquire_lock():
        sys.exit(0)
        
    try:
        # 1. Scansiona la dashboard per approvazioni o rifiuti (Fase 2)
        pending, approvals, rejections = read_dashboard()
        
        dashboard_changed = False
        
        if approvals or rejections:
            log(f"Rilevate decisioni utente: Approva ({len(approvals)}), Rifiuta ({len(rejections)})")
            
            for app in approvals:
                if process_approval(app):
                    dashboard_changed = True
            for rej in rejections:
                if process_rejection(rej):
                    dashboard_changed = True
                    
        # 2. Scansiona per nuovi file grezzi (Fase 1)
        raw_files = []
        for f in os.listdir(INBOX_PATH):
            if f.endswith(".md") and not f.startswith("proposed-") and not f.startswith("raw-") and not f.startswith("seen-") and f != "Review Dashboard.md":
                full_path = os.path.join(INBOX_PATH, f)
                clean_double_frontmatter(full_path)
                if is_ready_raw_file(full_path):
                    raw_files.append((f, full_path))
                    
        if not raw_files and not dashboard_changed and not approvals and not rejections:
            # Nulla da fare
            return
            
        # 3. Elabora i nuovi file grezzi uno ad uno
        processing_notes = {}
        
        # Carica Content Memory
        content_memory_prompt = ""
        if os.path.exists(CONTENT_MEMORY_FILE):
            try:
                with open(CONTENT_MEMORY_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                match = re.search(r'```.*?\n(.*?)```', content, re.DOTALL)
                if match:
                    content_memory_prompt = match.group(1).strip()
            except Exception as e:
                log(f"Impossibile leggere Content Memory: {e}")
                
        # Carica Style Guide
        style_guide_prompt = ""
        if os.path.exists(STYLE_GUIDE_FILE):
            try:
                with open(STYLE_GUIDE_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                parts = content.split('---')
                if len(parts) >= 3:
                    style_guide_prompt = parts[2].strip()
            except Exception as e:
                log(f"Impossibile leggere Style Guide: {e}")
                
        for filename, full_path in raw_files:
            note_title = os.path.splitext(filename)[0]
            log(f"Avvio elaborazione per la nota grezza: {note_title}")
            
            # Aggiunge alla dashboard nello stato iniziale
            processing_notes[note_title] = "Inizializzazione..."
            rewrite_dashboard(processing_notes, pending)
            
            # Rinomina subito in seen- per dare feedback visivo immediato all'utente
            seen_filename = f"seen-{filename}"
            seen_full_path = os.path.join(INBOX_PATH, seen_filename)
            try:
                os.rename(full_path, seen_full_path)
                log(f"Rinominato temporaneamente per elaborazione: {full_path} -> {seen_full_path}")
                full_path = seen_full_path
            except Exception as e:
                log(f"Impossibile rinominare in seen-: {e}")
            
            # Controlla se è un video YouTube
            video_url = get_video_url_from_file(full_path)
            success = True
            
            if video_url and needs_youtube_helper(full_path):
                processing_notes[note_title] = "Estrazione trascrizione e frame..."
                rewrite_dashboard(processing_notes, pending)
                
                # Chiama youtube_helper.py
                helper_script = os.path.join(VAULT_PATH, "99 - Meta/Scripts/youtube_helper.py")
                cmd_helper = ["python3", helper_script, video_url, full_path]
                
                log(f"Esecuzione youtube_helper.py per '{note_title}'...")
                ok, err = run_command_with_monitor(cmd_helper, full_path)
                if not ok:
                    log(f"youtube_helper fallito o interrotto: {err}")
                    success = False
                    
            if success and os.path.exists(full_path):
                # Rielaborazione AI con agy (Stato iniziale Fase 1/4)
                processing_notes[note_title] = "Rielaborazione AI (Fase 1/4: Lettura nota grezza & template...)"
                rewrite_dashboard(processing_notes, pending)
                
                proposed_file_path = os.path.join(INBOX_PATH, f"proposed-{filename}")
                
                # Costruisce il prompt specifico per agy
                agy_prompt = f"""
Sei l'agente di ingestione per l'AI Second Brain. Devi elaborare la nota grezza in '{full_path}' e creare la proposta di rielaborazione.

Istruzioni:
1. Leggi il contenuto della nota grezza '{full_path}'.
2. Determina il tipo di nota ed applica il template corretto presente in '{TEMPLATE_DIR}':
   - Se è una trascrizione video/YouTube, usa 'AI YouTube Transcript.md'.
     Segui queste istruzioni di scrittura e formattazione:
     "{content_memory_prompt}"
   - Se è un log di attività o una nota veloce di lavoro, usa 'AI Activity Log.md'.
   - Altrimenti, formattala in modo ottimale con YAML frontmatter standard (impostando 'status: review', 'title', 'date' YYYY-MM-DD, 'tags', 'macro_area').
3. Direttive fondamentali:
   - Preserva i collegamenti ad immagini ![[nome_immagine.jpg]] e posizionali in modo coerente.
   - Applicazione della skill 'mermaid-expert' per tutti i diagrammi Mermaid:
     Quando crei o inserisci diagrammi (usando blocchi ```mermaid) per processi o architetture complessi, applica sistematicamente le regole della skill 'mermaid-expert':
     * Scegli il tipo di diagramma più opportuno in base al contesto (flowchart, sequenceDiagram, erDiagram, stateDiagram-v2, gantt, etc.).
     * Sintassi sempre valida e pulita: racchiudi SEMPRE tra virgolette doppie le etichette dei nodi che contengono parentesi, due punti, trattini o spazi (es. `A["Nome Nodo (dettaglio)"]`).
     * NON inserire mai tag HTML (come <mark>, <font>, <b>, <i>) o sintassi markdown nei testi/etichette dei diagrammi.
     * Assicurati che l'intestazione del diagramma (es. `flowchart TD` o `graph TD`) sia posizionata subito all'inizio del blocco senza righe vuote.
     * Mantieni il diagramma leggibile e pulito senza overcrowding di nodi.
   - Scrivi in modo fluido, capitoli strutturati, approfondito in italiano. Evita formule schematiche predefinite dell'IA.
   - Applica le regole di stile, evidenziazione (HTML highlight giallo/viola) della Style Guide globale:
     "{style_guide_prompt}"
     CRITICAL: Inserisci i tag HTML per le evidenziazioni (<mark...>) come HTML puro inline direttamente nel testo. NON racchiudere MAI i tag tra backticks (ad esempio NON scrivere `<mark...>` o `` `<mark...>` ``). Deve essere HTML non formattato come codice in modo che Obsidian lo renderizzi visivamente.
4. Determina la destinazione finale ideale nel vault (es. '02 - Atlas/...', '05 - Blog/...') basandoti sulle cartelle esistenti e sul tipo di contenuto.
5. Salva la proposta finale in '{proposed_file_path}'. Aggiungi nel frontmatter YAML della proposta il campo `target_path` contenente il percorso relativo nel vault in cui spostare il file quando approvato (es. `target_path: "02 - Atlas/Tecnology/Programming/Nome Nota.md"`), con nome file in Title Case intelligente senza emoji.
"""
                cmd_agy = ["/Users/lorenzo/.local/bin/agy", "--dangerously-skip-permissions", "--print", agy_prompt]
                
                log(f"Chiamata agente agy per '{note_title}'...")
                
                def update_agy_status(line):
                    line_lower = line.lower()
                    status_text = None
                    if any(k in line_lower for k in ["write_file", "write_to_file", "writing", "proposed-", "replace_file_content", "multi_replace_file_content"]):
                        status_text = "Rielaborazione AI (Fase 4/4: Scrittura della nota proposta...)"
                    elif any(k in line_lower for k in ["grep_search", "list_dir", "read_resource", "search", "mcp", "atlas", "blog"]):
                        status_text = "Rielaborazione AI (Fase 2/4: Ricerca contesto nel Second Brain...)"
                    elif any(k in line_lower for k in ["view_file", "read_file", "reading", "template", "raw-", "seen-"]):
                        status_text = "Rielaborazione AI (Fase 1/4: Lettura nota grezza & template...)"
                    elif any(k in line_lower for k in ["thinking", "thought", "pensando", "analiz", "style", "mermaid", "frontmatter"]):
                        status_text = "Rielaborazione AI (Fase 3/4: Rielaborazione concettuale & Style Guide...)"
                    elif any(k in line_lower for k in ["complete", "finished", "finaliz"]):
                        status_text = "Rielaborazione AI (Finalizzazione proposta...)"
                    else:
                        current_status = processing_notes.get(note_title, "")
                        if len(line.strip()) > 0 and not current_status.startswith("Rielaborazione AI (Fase 3/4") and not current_status.startswith("Rielaborazione AI (Fase 4/4"):
                            status_text = "Rielaborazione AI (Fase 3/4: Rielaborazione concettuale & Style Guide...)"
                    
                    if status_text and processing_notes.get(note_title) != status_text:
                        processing_notes[note_title] = status_text
                        rewrite_dashboard(processing_notes, pending)
                
                ok, err = run_command_with_monitor(cmd_agy, full_path, on_line_callback=update_agy_status)
                if not ok:
                    log(f"Agente agy fallito o interrotto: {err}")
                    success = False
                else:
                    if os.path.exists(proposed_file_path):
                        fix_highlight_backticks(proposed_file_path)
                    
            # Conclusione elaborazione singola nota
            if success and os.path.exists(full_path):
                # Rinomina la nota grezza in raw-
                raw_file_path = os.path.join(INBOX_PATH, f"raw-{filename}")
                try:
                    os.rename(full_path, raw_file_path)
                    log(f"Rinominato file originale: {full_path} -> {raw_file_path}")
                except Exception as e:
                    log(f"Impossibile rinominare la nota grezza: {e}")
                    success = False
                    
            # Rimuove dallo stato di elaborazione ed eventualmente aggiunge alle approvazioni
            if note_title in processing_notes:
                del processing_notes[note_title]
                
            if success:
                pending.append({'name': note_title, 'raw': note_title})
                log(f"Elaborazione completata con successo per: {note_title}")
            else:
                # Se è stata interrotta per eliminazione file, pulisce i file parziali
                if not os.path.exists(full_path):
                    proposed_file = os.path.join(INBOX_PATH, f"proposed-{filename}")
                    if os.path.exists(proposed_file):
                        try:
                            os.remove(proposed_file)
                        except Exception:
                            pass
                    log(f"PULIZIA: rimosso file proposto parziale per '{note_title}' a causa della cancellazione della nota grezza.")
                else:
                    # Ripristina il nome originale se ha fallito per altri motivi ed esiste ancora il file 'seen-'
                    original_full_path = os.path.join(INBOX_PATH, filename)
                    try:
                        os.rename(full_path, original_full_path)
                        log(f"Ripristinato nome originale dopo fallimento: {full_path} -> {original_full_path}")
                    except Exception as e:
                        log(f"Impossibile ripristinare il nome originale dopo fallimento: {e}")
                    log(f"Elaborazione fallita per '{note_title}'. Verrà riprovata al prossimo ciclo watcher.")
                    
            # Aggiorna la dashboard dopo ogni file per feedback visivo immediato
            rewrite_dashboard(processing_notes, pending)
            
        # 4. Aggiorna la dashboard finale per sicurezza
        rewrite_dashboard(processing_notes, pending)
        
    finally:
        release_lock()

if __name__ == "__main__":
    main()
