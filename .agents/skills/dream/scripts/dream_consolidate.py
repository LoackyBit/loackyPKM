#!/usr/bin/env python3
# dream_consolidate.py - Estrae segnali chiave dai transcript delle conversazioni Antigravity CLI.
# Fase "Gather Signal" del ciclo Dreams: scansiona i JSONL e produce un report di raw signal
# che l'agente AI userà per consolidare MEMORY.md.

import os
import sys
import json
import glob
import datetime
import re

def find_transcript_files(brain_dir):
    """Trova tutti i file transcript.jsonl nelle conversazioni di Antigravity CLI."""
    pattern = os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript.jsonl")
    files = glob.glob(pattern)
    # Ordina per data di modifica (più recenti prima)
    files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    return files

def extract_signals_from_transcript(filepath, max_lines=500):
    """Estrae user inputs, correzioni, preferenze e decisioni chiave da un transcript JSONL."""
    signals = []
    conversation_id = filepath.split(os.sep)[-4]  # Risali al conversation ID
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return signals
    
    # Limita il numero di righe per efficienza
    lines = lines[:max_lines]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        entry_type = entry.get('type', '')
        source = entry.get('source', '')
        content = entry.get('content', '')
        
        if not content or not isinstance(content, str):
            continue
            
        # 1. Messaggi espliciti dell'utente (le sue richieste, correzioni, preferenze)
        if entry_type == 'USER_INPUT' or source == 'USER_EXPLICIT':
            # Filtra messaggi troppo corti o generici
            if len(content.strip()) > 15:
                signals.append({
                    'type': 'user_input',
                    'content': content.strip()[:500],  # Tronca a 500 caratteri
                    'conversation_id': conversation_id
                })
        
        # 2. Risposte dell'agente che contengono decisioni architetturali
        elif entry_type == 'PLANNER_RESPONSE' and source == 'MODEL':
            content_lower = content.lower()
            # Cerca pattern di decisione
            decision_markers = [
                'ho deciso', 'la scelta migliore', 'approccio consigliato',
                'convenzione', 'standard', 'regola', 'best practice',
                'non usare', 'usa sempre', 'evita', 'preferisci',
                'i decided', 'the best approach', 'convention', 'always use'
            ]
            for marker in decision_markers:
                if marker in content_lower:
                    # Estrai il paragrafo rilevante
                    for para in content.split('\n'):
                        para_lower = para.lower()
                        if marker in para_lower and len(para.strip()) > 20:
                            signals.append({
                                'type': 'decision',
                                'content': para.strip()[:400],
                                'conversation_id': conversation_id
                            })
                    break
    
    return signals

def extract_user_corrections(signals):
    """Filtra i segnali per trovare correzioni esplicite dell'utente."""
    corrections = []
    correction_markers = [
        'no,', 'non ', 'aspetta', 'sbagliato', 'correggi', 'cambia',
        'non puoi', 'non usare', 'usa il', 'usa la', 'preferisco',
        'non voglio', 'vorrei', 'meglio se', 'invece di', 'piuttosto',
        'wait', 'wrong', 'fix', 'change', "don't", 'stop',
        'procedi', 'esagerato', 'troppo'
    ]
    
    for signal in signals:
        if signal['type'] != 'user_input':
            continue
        content_lower = signal['content'].lower()
        for marker in correction_markers:
            if marker in content_lower:
                corrections.append(signal)
                break
    
    return corrections

def main():
    brain_dir = os.path.expanduser("~/.gemini/antigravity-cli/brain")
    
    if not os.path.exists(brain_dir):
        print(f"Directory brain non trovata: {brain_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Output arg: quante conversazioni analizzare (default 20)
    max_conversations = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    
    transcript_files = find_transcript_files(brain_dir)
    
    if not transcript_files:
        print("Nessun transcript trovato.", file=sys.stderr)
        sys.exit(0)
    
    # Limita al numero richiesto
    transcript_files = transcript_files[:max_conversations]
    
    all_signals = []
    for tf in transcript_files:
        signals = extract_signals_from_transcript(tf)
        all_signals.extend(signals)
    
    # Separa i tipi di segnale
    user_inputs = [s for s in all_signals if s['type'] == 'user_input']
    decisions = [s for s in all_signals if s['type'] == 'decision']
    corrections = extract_user_corrections(all_signals)
    
    # Scrivi il report di raw signal
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'conversations_analyzed': len(transcript_files),
        'total_signals': len(all_signals),
        'summary': {
            'user_inputs': len(user_inputs),
            'decisions': len(decisions),
            'corrections': len(corrections)
        },
        'corrections': [c['content'] for c in corrections],
        'decisions': [d['content'] for d in decisions[:50]],  # Max 50
        'recent_requests': [u['content'] for u in user_inputs[:30]]  # Max 30
    }
    
    # Output come JSON su stdout per l'agente
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
