#!/usr/bin/env python3
"""Modulo per l'interrogazione di NotebookLM (Alessandro de Concini) e caching metacognitivo.

Fornisce il wrapper subprocess per la CLI nlm, gestione timeout a 120s,
caching persistente su file e generazione di vincoli e sezioni per il Second Brain.
"""

import os
import sys
import json
import hashlib
import shutil
import subprocess
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

DEFAULT_NOTEBOOK_ID = "b7534dad-1515-44c1-bcc5-c77992b5e416"
DEFAULT_TIMEOUT = 120
MAX_SNIPPET_LENGTH = 1000


class NLMError(Exception):
    """Eccezione base per errori del modulo nlm_helper."""
    pass


class NLMAuthError(NLMError):
    """Sollevata quando la sessione Google/NLM è scaduta."""
    pass


class NLMTimeoutError(NLMError):
    """Sollevata quando la query supera il timeout prefissato."""
    pass


class NLMNetworkError(NLMError):
    """Sollevata su errori di connessione socket o DNS."""
    pass


def resolve_nlm_binary() -> str:
    """Risolve il percorso eseguibile del binario nlm nel sistema."""
    which_path = shutil.which("nlm")
    if which_path and os.path.isfile(which_path):
        return which_path

    home_dir = str(Path.home())
    candidate_paths = [
        os.path.join(home_dir, ".local", "bin", "nlm"),
        "/opt/homebrew/bin/nlm",
        "/usr/local/bin/nlm",
        "/usr/bin/nlm",
    ]
    for candidate in candidate_paths:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    raise NLMError(f"Binario nlm non trovato nel sistema (cercato in PATH e {candidate_paths})")


def build_nlm_query(title: str, course: Optional[str], snippet: str) -> str:
    """Costruisce il payload testuale di query per de Concini conforme a D-01."""
    clean_title = (title or "").strip()
    clean_snippet = (snippet or "").strip()
    if course and course.strip():
        prefix = f"Come schematizzare ed estrarre i principi primi di {clean_title} per la materia {course.strip()}?"
    else:
        prefix = f"Come schematizzare ed estrarre i principi primi di {clean_title}?"
    return f"{prefix} Ecco un estratto contestuale:\n\n{clean_snippet}"


def sanitize_json_output(raw_stdout: str) -> Dict[str, Any]:
    """Isola ed esegue il parse del JSON ignorando eventuali log rich o sequenze ANSI."""
    cleaned = raw_stdout.strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        snippet_json = cleaned[start_idx:end_idx + 1]
        try:
            data = json.loads(snippet_json)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    raise NLMError(f"Impossibile decodificare output JSON valido da nlm: {raw_stdout[:300]}")


def get_cache_dir(vault_root: Optional[str] = None) -> str:
    """Restituisce il percorso assoluto della directory di cache per NLM."""
    root = vault_root or os.getcwd()
    cache_dir = os.path.join(root, "99 - Meta", "Cache", "nlm")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def compute_cache_key(notebook_id: str, title: str, course: Optional[str], snippet: str) -> str:
    """Calcola la chiave hash SHA-256 su (notebook_id, corso, titolo, estratto)."""
    clean_course = (course or "").strip()
    payload = f"{notebook_id}::{clean_course}::{title.strip()}::{snippet.strip()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get_cached_response(vault_root: str, cache_key: str) -> Optional[Dict[str, Any]]:
    """Recupera la risposta memorizzata in cache se esistente e integra."""
    cache_file = os.path.join(get_cache_dir(vault_root), f"{cache_key}.json")
    if os.path.isfile(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            return None
    return None


def save_response_to_cache(vault_root: str, cache_key: str, data: Dict[str, Any]) -> None:
    """Salva la risposta di NotebookLM su file JSON nella directory di cache."""
    cache_file = os.path.join(get_cache_dir(vault_root), f"{cache_key}.json")
    try:
        temp_file = f"{cache_file}.tmp.{os.getpid()}"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(temp_file, cache_file)
    except Exception as e:
        sys.stderr.write(f"Avviso [nlm_helper]: Impossibile scrivere cache {cache_file}: {e}\n")


def clear_cache(vault_root: Optional[str] = None) -> int:
    """Elimina tutti i file JSON di cache in 99 - Meta/Cache/nlm/."""
    cache_dir = get_cache_dir(vault_root)
    count = 0
    if not os.path.exists(cache_dir):
        return 0
    for item in os.listdir(cache_dir):
        if item.endswith(".json"):
            file_path = os.path.join(cache_dir, item)
            try:
                os.remove(file_path)
                count += 1
            except Exception:
                pass
    return count


def format_metacognitive_constraints_prompt(directives_dict: Dict[str, Any]) -> str:
    """Genera il blocco di vincoli invisibili per il prompt di agy (Canale 1)."""
    answer = (directives_dict.get("answer") or "").strip()
    if not answer:
        return ""
    return f"""DIRETTIVE METACOGNITIVE SPECIALISTICHE (Alessandro de Concini):
{answer}

VINCOLI ATTIVI DI STRUTTURAZIONE:
1. Schematizzazione: Se le direttive suggeriscono modelli mentali o relazioni causa-effetto, inserisci obbligatoriamente un diagramma causale Mermaid con nodi quotati id["..."].
2. Densita e Principi Primi: Concentrati sui principi cardine individuati; elimina passaggi aneddotici o riempitivi.
3. Active Recall & Formule: Struttura definizioni e formule esplicitando ipotesi e condizioni di validita; rispetta il principio di atomicita concettuale per favorire la successiva creazione di flashcard."""


def format_metacognitive_markdown_section(directives_dict: Dict[str, Any]) -> str:
    """Genera la sezione pulita ## Direttive Metacognitive da appendere alla nota (Canale 2)."""
    answer = (directives_dict.get("answer") or "").strip()
    if not answer:
        return ""
    return f"""

## Direttive Metacognitive

**Linee Guida Alessandro de Concini (NotebookLM):**
{answer}
"""


def query_notebook(
    title: str,
    content: str,
    course: Optional[str] = None,
    notebook_id: str = DEFAULT_NOTEBOOK_ID,
    vault_root: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    use_cache: bool = True
) -> Dict[str, Any]:
    """Interroga il notebook di Alessandro de Concini con gestione cache e timeout."""
    snippet = (content or "")[:MAX_SNIPPET_LENGTH].strip()
    v_root = vault_root or os.getcwd()
    cache_key = compute_cache_key(notebook_id, title, course, snippet)

    if use_cache:
        cached = get_cached_response(v_root, cache_key)
        if cached is not None:
            return cached

    query_str = build_nlm_query(title, course, snippet)
    nlm_bin = resolve_nlm_binary()

    env = os.environ.copy()
    home_dir = str(Path.home())
    env['PATH'] = f"{home_dir}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:{env.get('PATH', '')}"

    cmd = [nlm_bin, "notebook", "query", notebook_id, query_str, "--json"]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            shell=False
        )
    except subprocess.TimeoutExpired as e:
        raise NLMTimeoutError(f"Timeout query NotebookLM ({timeout}s) superato per: {title}") from e
    except Exception as e:
        raise NLMError(f"Errore durante l'invocazione di nlm: {e}") from e

    out = proc.stdout.strip()
    err = proc.stderr.strip()

    combined_output = f"{out}\n{err}"
    if proc.returncode != 0 or "Authentication expired" in combined_output or "accounts.google.com" in combined_output:
        if "Authentication expired" in combined_output or "accounts.google.com" in combined_output or "Run 'nlm login'" in combined_output:
            raise NLMAuthError("Sessione di NotebookLM scaduta. Necessario 'nlm login'.")
        raise NLMError(f"Errore nlm (exit {proc.returncode}): {err or out}")

    data = sanitize_json_output(out)
    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "notebook_id": notebook_id,
        "title": title,
        "course": course,
        "query": query_str,
        "answer": data.get("answer", ""),
        "citations": data.get("citations", {}),
        "references": data.get("references", []),
        "sources_used": data.get("sources_used", [])
    }

    if use_cache:
        save_response_to_cache(v_root, cache_key, result)

    return result


def main() -> None:
    """CLI Standalone per diagnostica, query di test e manutenzione cache."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Helper CLI per interrogare Google NotebookLM (Alessandro de Concini) e gestire la cache metacognitiva."
    )
    parser.add_argument("--check-auth", action="store_true", help="Verifica la disponibilita del binario nlm e la sessione Google attiva")
    parser.add_argument("--query", type=str, help="Esegue una query di test verso il notebook de Concini")
    parser.add_argument("--course", type=str, default=None, help="Materia o corso opzionale associato alla query")
    parser.add_argument("--snippet", type=str, default="Principi primi e schematizzazione per studio universitario.", help="Estratto contestuale per la query")
    parser.add_argument("--no-cache", action="store_true", help="Disabilita la cache su disco per la query corrente")
    parser.add_argument("--clear-cache", action="store_true", help="Svuota tutti i file memorizzati in 99 - Meta/Cache/nlm/")
    parser.add_argument("--vault-root", type=str, default=None, help="Percorso radice del vault Obsidian")

    args = parser.parse_args()

    v_root = args.vault_root or os.getcwd()

    if args.clear_cache:
        deleted = clear_cache(v_root)
        print(f"Cache svuotata con successo: {deleted} elementi rimossi da {get_cache_dir(v_root)}.")
        sys.exit(0)

    if args.check_auth:
        try:
            bin_path = resolve_nlm_binary()
            print(f"Binario nlm trovato: {bin_path}")
            proc = subprocess.run([bin_path, "--version"], capture_output=True, text=True, timeout=10)
            version_str = (proc.stdout or proc.stderr).strip()
            print(f"Versione CLI: {version_str}")
            print("Verifica autenticazione in corso...")
            probe_proc = subprocess.run(
                [bin_path, "notebook", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            probe_out = f"{probe_proc.stdout} {probe_proc.stderr}"
            if "Authentication expired" in probe_out or "accounts.google.com" in probe_out or probe_proc.returncode != 0:
                print("AVVISO: Autenticazione non valida o scaduta. Esegui 'nlm login'.")
                sys.exit(1)
            else:
                print("Autenticazione NotebookLM valida.")
                sys.exit(0)
        except Exception as e:
            print(f"ERRORE check-auth: {e}")
            sys.exit(1)

    if args.query:
        try:
            print(f"Esecuzione query per: '{args.query}' (Corso: {args.course})...")
            res = query_notebook(
                title=args.query,
                content=args.snippet,
                course=args.course,
                vault_root=v_root,
                use_cache=not args.no_cache
            )
            print("\n--- RISPOSTA NOTEBOOKLM ---")
            print(res.get("answer", ""))
            print("\n--- CITAZIONI ---")
            print(json.dumps(res.get("citations", {}), indent=2))
        except Exception as e:
            sys.stderr.write(f"ERRORE query: {e}\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
