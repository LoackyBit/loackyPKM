#!/usr/bin/env python3
"""brain_ingest.py - Unified Second Brain Ingestion & GTD Staging Engine (<450 lines).

Features:
- Dedicated staging folders: 03 - Inbox/Draft/ and 03 - Inbox/Source/
- GTD Tri-State Review Dashboard ([x] Approve -> Atlas/Blog, [-] Reject -> Purge)
- Deterministic autolinking strictly against real existing notes (max 2 per target)
- SHA-256 mutex per-source locking with active PID & TTL auto-healing
- Optional YouTube frame extraction (--extract-frames)
- Preventative duplicate and missing transcript guards
"""

import os, sys, re, datetime, hashlib, argparse, shutil, glob, time, subprocess, urllib.parse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path: sys.path.insert(0, SCRIPT_DIR)

import brain_health, youtube_helper

YT_URL_REGEX = re.compile(r'(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})')
WEB_URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
RE_APPROVAL_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+Approva\s+\[\[(?:Draft/)?(?P<name>[^\]]+)\]\](?:\s+\(fonte:\s+\[\[(?:Source/)?(?P<src>[^\]]+)\]\]\))?(?:\s+\(.*target:\s*(?P<target>.*?)\))?')
RE_ERROR_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+\[!\]\s+Riprova:\s+(?P<src>.*?)(?:\s+—\s+Motivo:\s*(?P<reason>.*))?$')
RE_PANIC_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+.*(?:🛑|Interrompi|Panic\s+Button).*', re.IGNORECASE)
PANIC_BUTTON_LINE = "- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)"

def is_pid_alive(pid: int) -> bool:
    """Checks if a process with given PID is currently active."""
    if pid <= 0: return False
    try: os.kill(pid, 0); return True
    except (OSError, ProcessLookupError): return False

class NoteLock:
    """Mutex lock based on SHA-256 hash preventing concurrent runs with auto-healing."""
    def __init__(self, identifier: str, ttl_seconds: int = 600):
        slug = hashlib.sha256(identifier.encode('utf-8')).hexdigest()[:12]
        self.lock_file = f"/tmp/brain_ingest_{slug}.lock"
        self.ttl_seconds, self.acquired = ttl_seconds, False

    def _clean_stale_lock(self):
        if not os.path.exists(self.lock_file): return
        try:
            mtime = os.path.getmtime(self.lock_file)
            is_stale = (datetime.datetime.now().timestamp() - mtime) > self.ttl_seconds
            if not is_stale:
                with open(self.lock_file, 'r', encoding='utf-8') as f: content = f.read()
                m = re.search(r'pid:\s*(\d+)', content)
                if m and not is_pid_alive(int(m.group(1))): is_stale = True
            if is_stale: os.remove(self.lock_file)
        except Exception: pass

    def __enter__(self):
        self._clean_stale_lock()
        for _ in range(2):
            try:
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"pid: {os.getpid()}\ntime: {datetime.datetime.now().isoformat()}\n".encode('utf-8'))
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                self._clean_stale_lock()
        raise RuntimeError(f"Lock active for source ({self.lock_file}). Ingestion in progress.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired and os.path.exists(self.lock_file):
            try: os.remove(self.lock_file)
            except Exception: pass

def get_source_lock_file(source: str) -> str:
    """Returns the deterministic lock file path for a source identifier."""
    slug = hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]
    return f"/tmp/brain_ingest_{slug}.lock"

def is_source_lock_active(source: str) -> bool:
    """Checks if a lock file for the given source exists with an active PID."""
    lf = get_source_lock_file(source)
    if not os.path.exists(lf): return False
    try:
        with open(lf, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
        m = re.search(r'pid:\s*(\d+)', content)
        if m and is_pid_alive(int(m.group(1))):
            return True
        try: os.remove(lf)
        except Exception: pass
        return False
    except Exception:
        return False


def detect_input_type(source: str) -> str:
    """Classifies polymorphic input into youtube, web, file, or text."""
    s = source.strip()
    if YT_URL_REGEX.search(s): return "youtube"
    if WEB_URL_REGEX.match(s): return "web"
    if os.path.exists(s) or (s.endswith('.md') and '\n' not in s): return "file"
    return "text"

def _has_tag(tags: List[str], target_tags: List[str]) -> bool:
    """Checks if any tag matches target tags (exact or hierarchical prefix)."""
    for t in tags:
        t_clean = t.lower().strip().lstrip('#')
        for target in target_tags:
            target_clean = target.lower().strip().lstrip('#')
            if t_clean == target_clean or t_clean.startswith(target_clean + '/'):
                return True
    return False


def _has_keyword(text: str, keywords: List[str]) -> bool:
    """Checks if any keyword is present using regex word boundaries for short tokens."""
    for kw in keywords:
        kw_clean = kw.lower().strip()
        if not kw_clean:
            continue
        if len(kw_clean) <= 3:
            if re.search(r'(?:\b|_)' + re.escape(kw_clean) + r'(?:\b|_)', text):
                return True
        else:
            if kw_clean in text:
                return True
    return False


def classify_target_directory(title: str, tags: List[str], content: str = "", vault_root: Optional[str] = None) -> str:
    """Heuristically and semantically determines destination subfolder in Atlas or Blog based on tags, title, and content."""
    tags_lower = [str(t).lower().strip().lstrip('#') for t in tags if t]
    c = (title + " " + " ".join(tags_lower) + " " + content[:2500]).lower()

    # 1. Blog Studio
    if _has_tag(tags_lower, ["blog"]) or _has_keyword(c, ["blog"]):
        return "05 - Blog"

    # 2. Finance Subdirectories
    # 2.1 Crypto
    if _has_tag(tags_lower, ["finance/crypto", "finance/blockchain", "tech/crypto", "tech/blockchain", "crypto", "blockchain", "bitcoin", "btc", "ethereum", "eth", "web3"]) or \
       _has_keyword(c, ["crypto", "criptovalut", "bitcoin", "btc", "ethereum", "eth", "blockchain", "web3", "defi", "nft", "token", "wallet", "smart contract", "altcoin", "binance"]):
        return "02 - Atlas/Finance/Crypto"

    # 2.2 Holdings & Tax
    if _has_tag(tags_lower, ["finance/tax", "finance/fisco", "finance/wealth", "finance/patrimonio", "finance/holdings", "tax", "fisco", "holdings"]) or \
       _has_keyword(c, ["fisco", "fiscale", "tasse", "irpef", "partita iva", "p.iva", "srl", "holding", "evasione", "elusione", "deduzion", "detrazion", "patrimonio", "quadro rw", "commercialista", "regime forfettario", "residenza fiscale"]):
        return "02 - Atlas/Finance/Holdings & Tax"

    # 2.3 Investments
    if _has_tag(tags_lower, ["finance/investing", "finance/investments", "finance/stocks", "finance/etf", "finance/markets", "finance/trading", "investimenti", "etf", "trading"]) or \
       _has_keyword(c, ["investimenti", "investire", "borsa", "azioni", "etf", "fondi indicizzati", "obbligazioni", "compound interest", "interesse composto", "trading", "value investing", "s&p 500", "nasdaq", "rendimento", "portafoglio", "dividendi"]):
        return "02 - Atlas/Finance/Investments"

    # 2.4 Economy & Macro
    if _has_tag(tags_lower, ["finance/macro", "finance/economy", "finance/banks", "macroeconomia", "banche", "economia"]) or \
       _has_keyword(c, ["macroeconomia", "banche", "banca centrale", "bce", "federal reserve", "fed", "inflazione", "tassi di interesse", "debito pubblico", "pil", "recessione", "dazi", "geopolitica", "politica monetaria", "creazione del denaro"]):
        return "02 - Atlas/Finance/Economy"

    # 2.5 General Finance Fallback
    if _has_tag(tags_lower, ["finance"]) or _has_keyword(c, ["finanza", "finance", "soldi", "money", "business"]):
        return "02 - Atlas/Finance/Investments"

    # 3. Personal Growth & Health Subdirectories
    # 3.1 Gym & Health
    if _has_tag(tags_lower, ["health/fitness", "health/gym", "health/workout", "health/palestra", "mentality/fitness", "health/nutrition", "health/sleep", "health/biohacking", "health/health", "health", "palestra", "fitness", "gym", "workout", "salute", "nutrizione"]) or \
       _has_keyword(c, ["palestra", "workout", "allenamento", "ipertrofia", "bodybuilding", "calisthenics", "pesi", "squat", "panca piana", "stacco", "massa muscolare", "nutrizione", "dieta", "alimentazione", "salute", "sonno", "biohacking", "integratori", "fluoro", "dentifricio", "denti", "metabolismo", "calorie", "macronutrienti", "digiuno", "skincare"]):
        return "02 - Atlas/Personal Growth & Health/Gym & Health"

    # 3.2 Mentality & Mindset
    if _has_tag(tags_lower, ["mentality/habits", "mentality/productivity", "mentality/discipline", "mentality/focus", "mentality/produttivita", "mentality/philosophy", "mentality/mental-models", "mentality/stoicism", "mentality/growth", "mentality/psychology", "mentality/mindset", "mentality", "mindset", "produttivita", "abitudini", "focus", "filosofia", "stoicismo"]) or \
       _has_keyword(c, ["produttivita", "abitudini", "abitudine", "routine", "disciplina", "focus", "concentrazione", "time management", "gestione del tempo", "gtd", "second brain", "dopamina", "procrastinazione", "pomodoro", "back to focus", "distrazioni", "dipendenza neurocognitiva", "tempo di permanenza", "filosofia", "stoicismo", "modelli mentali", "modello mentale", "pensiero critico", "bias cognitivo", "decision making", "razionalita", "epistemologia", "socrate", "marco aurelio", "seneca", "fallacie", "mentalita", "mindset", "crescita personale", "resilienza", "autostima", "psicologia", "comunicazione", "public speaking", "relazioni", "persuasione", "parlare bene", "cancel culture"]):
        return "02 - Atlas/Personal Growth & Health/Mentality"

    # 3.3 General Personal Growth Fallback
    if _has_tag(tags_lower, ["mentality"]) or _has_keyword(c, ["mentality", "crescita"]):
        return "02 - Atlas/Personal Growth & Health/Mentality"

    # 4. Education & Learning Subdirectories
    # 4.1 Learning (Metodo, Apprendimento, Lettura, Memory, School)
    if _has_tag(tags_lower, ["education/method", "education/learning", "education/study", "education/memory", "education/mnemonics", "education/school", "education/highschool", "apprendimento", "metodo-studio", "memoria", "scuola", "liceo"]) or \
       _has_keyword(c, ["metodo di studio", "apprendimento", "imparare", "feynman", "active recall", "spaced repetition", "ripetizione spaziata", "lettura veloce", "memorizzazione", "pacrar", "memoria", "mnemotecniche", "palazzo della memoria", "tecniche di memoria", "ricordare cio che leggi", "memorizzare", "leggere libri", "scuola", "liceo", "registro elettronico", "classeviva", "maturita", "professori", "interrogazione", "compiti", "bravo a scuola", "learning to learn"]):
        return "02 - Atlas/Education & Learning/Learning"

    # 4.2 University Sub-branches
    if _has_tag(tags_lower, ["education/university/systems", "education/university/os"]) or \
       _has_keyword(c, ["architettura dei calcolatori", "sistemi operativi", "calcolatori elettronici", "assembly", "reti di calcolatori"]):
        return "02 - Atlas/Education & Learning/University/Architettura & Sistemi"

    if _has_tag(tags_lower, ["education/university/cs", "education/university/programming", "education/university/fondamenti"]) or \
       _has_keyword(c, ["fondamenti di informatica", "programmazione c", "algoritmi e strutture dati"]):
        return "02 - Atlas/Education & Learning/University/Fondamenti di Informatica"

    if _has_tag(tags_lower, ["education/university/math", "education/university/physics", "education/math", "matematica", "fisica"]) or \
       _has_keyword(c, ["analisi matematica", "algebra lineare", "geometria", "fisica 1", "probabilita", "statistica", "calcolo numerico", "analisi 1", "analisi 2", "derivate", "integrali"]):
        return "02 - Atlas/Education & Learning/University/Matematica & Fisica"

    if _has_tag(tags_lower, ["education/university/languages", "education/university/automata"]) or \
       _has_keyword(c, ["teoria dei linguaggi", "automi", "linguaggi formali", "compilatori", "grammatiche formali", "macchina di turing"]):
        return "02 - Atlas/Education & Learning/University/Teoria dei Linguaggi"

    if _has_tag(tags_lower, ["education/university"]) or \
       _has_keyword(c, ["universita", "ingegneria informatica", "esame", "esami universitari", "cfu", "laurea", "sessione d'esami", "scegliere l'universita"]):
        return "02 - Atlas/Education & Learning/University"

    # 4.3 Courses
    if _has_tag(tags_lower, ["education/course", "education/courses", "education/cs50", "corso", "corsi"]) or \
       _has_keyword(c, ["corso stem", "corso ai", "cs50", "progetto enea", "progetto pilota airo", "corso python"]):
        return "02 - Atlas/Education & Learning/Courses"

    # 4.4 General Education Fallback
    if _has_tag(tags_lower, ["education"]) or _has_keyword(c, ["education", "studio", "scuola", "universita"]):
        return "02 - Atlas/Education & Learning/Learning"

    # 5. Projects Subdirectories
    if _has_tag(tags_lower, ["projects/active", "project/active"]):
        return "02 - Atlas/Projects/Active"
    if _has_tag(tags_lower, ["projects/archive", "project/archive"]):
        return "02 - Atlas/Projects/Archive"
    if _has_tag(tags_lower, ["projects/ideas", "project/ideas", "projects/sandbox"]):
        return "02 - Atlas/Projects/Ideas & Sandbox"

    # 6. Tech & AI Subdirectories
    # 6.1 Agents & Automation
    if _has_tag(tags_lower, ["tech/agents", "tech/agent", "tech/automation", "tech/agenti", "agenti", "automazione"]) or \
       _has_keyword(c, ["agente ai", "agenti ai", "ai agent", "ai agents", "multi-agent", "crewai", "langchain", "autogen", "n8n", "automazione", "zapier", "workflow automat", "hermes agent"]):
        return "02 - Atlas/Tech & AI/Agents & Automation"

    # 6.2 Security
    if _has_tag(tags_lower, ["tech/security", "tech/cybersecurity", "tech/hacking", "security", "cybersecurity", "hacking"]) or \
       _has_keyword(c, ["cybersecurity", "sicurezza informatica", "crittografia", "vulnerabilita", "malware", "exploit", "firewall", "pentesting", "penetration test", "oauth", "jwt", "xss", "csrf", "sql injection", "zero-day", "hacking", "ethical hacking", "reverse engineering", "buffer overflow", "ctf", "kali linux", "coinjoin"]):
        return "02 - Atlas/Tech & AI/Security"

    # 6.3 Software Development (GitHub, SemVer, Vibe Coding, Architecture, Clean Code)
    if _has_tag(tags_lower, ["tech/git", "tech/github", "tech/dev", "tech/software-engineering", "tech/semver", "tech/architecture", "tech/vibe-coding", "tech/vibecoding", "git", "github", "vibe-coding"]) or \
       _has_keyword(c, ["github", "git commit", "git push", "git rebase", "git branch", "pull request", "repository git", "gitflow", "vibe coding", "vibecoding", "sviluppo software", "software engineering", "semantic versioning", "semver", "versioning conventions", "design pattern", "clean code", "refactoring", "ci/cd", "continuous integration", "test unitari", "tdd", "agile", "scrum", "microservizi", "dependency hell", "major.minor.patch", "cursor", "submodule"]):
        return "02 - Atlas/Tech & AI/Software Development"

    # 6.4 System & OS
    if _has_tag(tags_lower, ["tech/os", "tech/linux", "tech/sysadmin", "tech/networks", "linux", "devops"]) or \
       _has_keyword(c, ["linux", "macos", "unix", "kernel", "terminale", "bash", "zsh", "file system", "tcp/ip", "dns", "server", "sysadmin", "ubuntu", "debian", "terminal setup", "situazione python"]):
        return "02 - Atlas/Tech & AI/System & OS"

    # 6.5 Programming Generale & Coding con AI
    if _has_tag(tags_lower, ["tech/programming", "tech/code", "tech/python", "tech/js", "tech/ts", "tech/rust", "tech/golang", "tech/backend", "tech/frontend", "tech/database", "tech/sql", "tech/programming/ai", "programming", "coding"]) or \
       _has_keyword(c, ["python", "javascript", "typescript", "rust", "golang", "c++", "java", "database", "sql", "backend", "frontend", "api rest", "graphql", "docker", "kubernetes", "algoritmi", "strutture dati", "programmazione ai"]):
        return "02 - Atlas/Tech & AI/Programming"

    # 6.6 AI & Machine Learning
    if _has_tag(tags_lower, ["tech/ai", "tech/llm", "tech/rag", "tech/ml", "tech/nlp", "tech/prompt", "ai", "llm", "prompt"]) or \
       _has_keyword(c, ["intelligenza artificiale", "ai", "llm", "large language model", "machine learning", "deep learning", "transformer", "neural network", "rag", "embeddings", "vision model", "nlp", "hugging face", "gpt", "claude", "gemini", "fine-tuning", "modelli linguistici", "notebooklm", "prompt engineering", "system prompt", "context window", "hardware ai"]):
        return "02 - Atlas/Tech & AI/AI"

    return "02 - Atlas/Tech & AI/AI"

    return "02 - Atlas/Tech & AI"

def check_duplicate_resource(vault_root: str, source_url: Optional[str], title: str) -> Optional[Tuple[str, str]]:
    """Checks 02 - Atlas notes frontmatter for existing source URL, video ID, or clean non-generic title."""
    clean_target = brain_health.clean_title_str(title).lower() if title else ""
    if clean_target.startswith("raw note") or clean_target in ("nuova nota", "untitled", "draft", "bozza", ""):
        clean_target = ""

    target_vid = youtube_helper.get_video_id(source_url) if source_url else None
    scan_path = os.path.join(vault_root, "02 - Atlas")
    if os.path.exists(scan_path):
        for root, _, files in os.walk(scan_path):
            for file in files:
                if not file.endswith('.md') or file.startswith('.'): continue
                fp = os.path.join(root, file)
                if clean_target and brain_health.clean_title_str(file[:-3]).lower() == clean_target:
                    return fp, "title"
                if source_url and source_url != "original" and not str(source_url).startswith("file://"):
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read(2500)
                        has_fm, fm_text, _, _ = brain_health.split_markdown_note(text)
                        if has_fm:
                            meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine())
                            note_src = str(meta.get('source') or '').strip()
                            note_vid = str(meta.get('video_url') or '').strip()
                            if source_url in (note_src, note_vid):
                                return fp, "source_url"
                            if target_vid:
                                src_vid = youtube_helper.get_video_id(note_src) if note_src else None
                                vid_vid = youtube_helper.get_video_id(note_vid) if note_vid else None
                                if (src_vid and src_vid == target_vid) or (vid_vid and vid_vid == target_vid):
                                    return fp, "source_url"
                    except Exception:
                        pass
    return None

def autolink_content(vault_root: str, body_text: str, current_title: str) -> Tuple[str, List[str]]:
    """Links only real existing note titles (max 2 per target), safely preserving code blocks."""
    auditor = brain_health.VaultHealthAuditor(vault_root)
    all_titles = sorted(auditor.all_notes.keys(), key=lambda x: len(x), reverse=True)
    stopwords = {'home', 'daily', 'note', 'studio', 'guida', 'guide', 'indice', 'index',
                 'atlas', 'moc', 'blog', 'meta', 'tech', 'inbox', 'school', 'appunti', 'review'}
    code_blocks = []
    def mask_code(m):
        code_blocks.append(m.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    masked = re.sub(r'```[\s\S]*?```', mask_code, body_text)
    masked = re.sub(r'`[^`\n]+`', mask_code, masked)
    linked, inserted, cur_clean = masked, set(), current_title.lower().strip()

    for title in all_titles:
        t_low = title.lower().strip()
        if t_low == cur_clean or len(title) < 4 or t_low in stopwords: continue
        pat = re.compile(r'(?<!\[\[)(?<!/)(?<![\w#])(' + re.escape(title) + r')(?![\w])(?![^\[]*\]\])(?![^\(]*\))', re.IGNORECASE)
        if pat.search(linked):
            linked = pat.sub(f"[[{title}]]", linked, count=2)
            inserted.add(f"[[{title}]]")

    for idx, blk in enumerate(code_blocks): linked = linked.replace(f"__CODE_BLOCK_{idx}__", blk)
    return linked, sorted(list(inserted))

def sanitize_style_highlights(text: str) -> str:
    """Strips backticks from HTML <mark> and <font> tags."""
    return re.sub(r'`(<(?:mark|font)\b[^>]*>[\s\S]*?</(?:mark|font)>)`', r'\1', text)

def format_structured_note(title: str, raw_content: str, depth: str = "approfondimento", source_type: str = "text", source_url: str = "original") -> str:
    """Formats note body with clean headings (no emoji, no ## Collegamenti) and style guide highlights."""
    c_title = brain_health.clean_title_str(title)
    is_deep = depth in ("deep", "approfondimento")
    lead = raw_content.strip()[:250].replace('\n', ' ')
    lines = [
        f"# {c_title}\n",
        "## Sintesi Esecutiva\n",
        f'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>{c_title}</b></font></mark>: {lead}...\n'
    ]
    if is_deep:
        lines.extend([
            f"## Quadro Concettuale e Fondamenti\n\n{raw_content.strip()}\n",
            f"## Meccanica e Dettaglio Operativo\n\nAnalisi approfondita dei principi operativi di {c_title}.\n",
            "## Analisi Critica e Casi Applicativi\n\nValutazione di limiti, compromessi architetturali e contesti d'uso.\n"
        ])
    else:
        lines.extend([
            f"## Concetti Chiave e Takeaway\n\n- <mark style=\"background:rgba(181, 113, 255, 0.36)\"><font color=\"#9a54c1\"><b>Punto Chiave 1</b></font></mark>: {lead[:120]}\n",
            f"## Quadro Concettuale\n\n{raw_content.strip()}\n"
        ])
    return "\n".join(lines)

def enrich_draft_with_ai(vault_root: str, title: str, source_content: str, depth: str = "approfondimento",
                         source_type: str = "text", source_url: str = "original",
                         agy_path: str = "/Users/lorenzo/.local/bin/agy", timeout: int = 45) -> tuple[str, str]:
    """Generates enriched conceptual note body and executive summary via AI (agy CLI) with heuristic fallback.
    Returns (enriched_body, summary)."""
    c_title = brain_health.clean_title_str(title)
    is_deep = depth in ("deep", "approfondimento")

    if os.environ.get("BRAIN_INGEST_NO_AI") == "1":
        fallback_body = format_structured_note(c_title, source_content, depth=depth, source_type=source_type, source_url=source_url)
        fallback_summary = f"Trattazione concettuale ed evidenze operative per {c_title}."
        return fallback_body, fallback_summary

    depth_instruction = (
        "LIVELLO DI DETTAGLIO: APPROFONDIMENTO (DEFAULT)\n"
        "Fornisci una trattazione ricca, densa ed esaustiva di tutti i passaggi logici, modelli mentali e meccanismi di dettaglio. "
        "Non sintetizzare eccessivamente: sviluppa i concetti con ampiezza e precisione terminologica."
        if is_deep else
        "LIVELLO DI DETTAGLIO: SINTESI\n"
        "Fornisci una trattazione compatta (1-2 schermate) focalizzata sulla tesi centrale, definizioni essenziali e takeaway operativi."
    )

    prompt = f"""Sei il motore di elaborazione della conoscenza per un Second Brain PKM in Obsidian.
Il tuo compito è rielaborare il contenuto sorgente in una nota concettuale permanente di altissima qualità letteraria e tecnica per: "{c_title}".

CONTENUTO SORGENTE:
{source_content[:9000]}

{depth_instruction}

REGOLE CRITICHE DI CONTENUTO E STILE:
1. FILTRO ANTI-SLOP E ANTI-SPONSOR:
   - Elimina categoricamente sponsor commerciali (es. corsi online, piattaforme cloud, VPN, promozioni), saluti, formule di rito, aneddoti irrilevanti e frasi riempitive.
   - Distilla solo principi primi, definizioni rigorose, tesi argomentate, metodologie applicative e limiti critici.

2. ANATOMIA E SEZIONI DELLA NOTA:
   - Inizia sempre con il titolo H1 esatto della nota: # {c_title}
   - Struttura le sezioni H2 e H3 in modo completamente libero e flessibile, guidato dalla natura del contenuto (es. Sintesi Esecutiva, Fondamenti Teorici, Meccanica di Funzionamento, Analisi Critica, Applicazioni Pratiche).
   - DIVIETO ASSOLUTO DI EMOJI NEI TITOLI: I titoli H1, H2, H3 devono contenere SOLO testo pulito (es. '## Sintesi Esecutiva' e MAI '## 🎯 Sintesi Esecutiva').
   - NESSUNA SEZIONE COLLEGAMENTI SEPARATA: Non inserire mai sezioni come '## Collegamenti', '## Note Correlate' o '## Vedi anche'. I collegamenti semantici verranno gestiti altrove.

3. EVIDENZIAZIONI E ARRICCHIMENTO VISIVO:
   - Evidenzia i concetti cardine/parole chiave assolute in GIALLO: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>
   - Evidenzia i concetti secondari/nomi/luoghi in VIOLA: <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>
   - MAI racchiudere i tag <mark> o <font> tra backtick markdown (solo HTML inline grezzo).
   - Usa diagrammi Mermaid per processi/flussi logici complessi (tutti i nodi con apici: id["Etichetta"]).
   - Usa LaTeX per formule matematiche/tecniche ($...$ o $$...$$).

4. LINGUA E SINTESI FINALE:
   - Scrivi rigorosamente in italiano accademico, chiaro e professionale.
   - NON includere il frontmatter YAML (sarà generato dal sistema).
   - Alla fine assoluta della risposta, inserisci il marcatore esatto '---SUMMARY---' seguito da una singola frase densa di significato (120-180 caratteri, max 200) per il recupero sub-secondo.
"""

    agy_cmd = agy_path if os.path.exists(agy_path) else "agy"
    env = os.environ.copy()
    env['PATH'] = f"/Users/lorenzo/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env.get('PATH', '')}"
    env['PYTHONUNBUFFERED'] = '1'

    try:
        proc = subprocess.run(
            [agy_cmd, "--model", "gemini-3.7-flash-low", "--dangerously-skip-permissions", "--disable-slash-commands", f"--print={prompt}"],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        if proc.returncode == 0 and proc.stdout.strip():
            raw_out = proc.stdout.strip()
            summary = ""
            if "---SUMMARY---" in raw_out:
                parts = raw_out.split("---SUMMARY---", 1)
                body_part = parts[0].strip()
                summary = parts[1].strip().replace('\n', ' ').strip('"').strip("'")
            else:
                body_part = raw_out.strip()

            if not summary or len(summary) < 20:
                summary = f"Trattazione concettuale ed evidenze chiave per {c_title}."
            if len(summary) > 200:
                summary = summary[:197] + "..."

            cleaned_body = sanitize_style_highlights(body_part)
            # Ensure H1 header is clean without emoji
            cleaned_body = re.sub(r'^#\s+[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\s]*', f'# {c_title}\n\n', cleaned_body)
            if not cleaned_body.startswith("# "):
                cleaned_body = f"# {c_title}\n\n" + cleaned_body

            # Strip any hallucinated ## Collegamenti section
            cleaned_body = re.sub(r'\n+##\s+(?:🔗\s*)?(?:Collegamenti|Note Correlate|Vedi anche)[\s\S]*$', '', cleaned_body, flags=re.IGNORECASE)

            # Strip emojis from any H2/H3 headers
            cleaned_body = re.sub(r'^(#{2,6}\s+)[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\s]+', r'\1', cleaned_body, flags=re.MULTILINE)

            return cleaned_body.strip(), summary
    except Exception:
        pass

    fallback_body = format_structured_note(c_title, source_content, depth=depth, source_type=source_type, source_url=source_url)
    fallback_summary = f"Trattazione concettuale ed evidenze operative per {c_title}."
    return fallback_body, fallback_summary

def append_inbox_history(vault_root: str, action: str, note_title: str, target: str, source: str = ""):
    """Appends processed action to 99 - Meta/logs/inbox_history.md."""
    log_dir = os.path.join(vault_root, "99 - Meta", "logs")
    os.makedirs(log_dir, exist_ok=True)
    src_str = f" (source: {source})" if source else ""
    with open(os.path.join(log_dir, "inbox_history.md"), "a", encoding="utf-8") as f:
        f.write(f"- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | [{action}] | [[{note_title}]] -> {target}{src_str}\n")

def record_ingest_error(vault_root: str, source_or_url: str, reason: str):
    """Records ingestion error under ## ⚠️ Errori di Acquisizione in Review Dashboard."""
    update_review_dashboard(vault_root, add_error=(source_or_url, reason))


def trigger_panic_abort(vault_root: str) -> int:
    """Terminates all running ingestion processes, cleans locks, resets ready notes, and clears In Elaborazione."""
    aborted_pids = set()
    my_pid = os.getpid()

    # 1. Identify watcher PID if running to ensure it is NEVER killed
    watcher_pid = None
    pid_file = "/tmp/brain_watcher.pid"
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.isdigit():
                    watcher_pid = int(content)
        except Exception:
            pass

    # 2. Extract PIDs from all active lock files
    lock_files = glob.glob("/tmp/brain_ingest_*.lock")
    for lf in lock_files:
        try:
            with open(lf, "r", encoding="utf-8") as f:
                c = f.read()
            m = re.search(r'pid:\s*(\d+)', c)
            if m:
                target_pid = int(m.group(1))
                if target_pid > 0 and target_pid != my_pid and target_pid != watcher_pid:
                    aborted_pids.add(target_pid)
            os.remove(lf)
        except Exception:
            pass

    # 3. Discover any running brain_ingest.py or youtube_helper / yt-dlp / ffmpeg processes
    try:
        import subprocess
        ps_out = subprocess.run(["ps", "-eo", "pid,command"], capture_output=True, text=True, errors="ignore")
        for line in ps_out.stdout.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(None, 1)
            if len(parts) == 2 and parts[0].isdigit():
                p = int(parts[0])
                cmd = parts[1]
                if p in (my_pid, watcher_pid, 1, 0):
                    continue
                if ("brain_ingest.py" in cmd or "youtube_helper.py" in cmd or "yt-dlp" in cmd or "ffmpeg" in cmd) and "watch.sh" not in cmd and "--panic" not in cmd:
                    aborted_pids.add(p)
    except Exception:
        pass

    # 4. Terminate all discovered PIDs
    for p in aborted_pids:
        if is_pid_alive(p):
            try:
                os.kill(p, 15)  # SIGTERM
            except Exception:
                pass

    if aborted_pids:
        time.sleep(0.3)
        for p in aborted_pids:
            if is_pid_alive(p):
                try:
                    os.kill(p, 9)  # SIGKILL
                except Exception:
                    pass

    # 5. Clean up any remaining lock files
    for lf in glob.glob("/tmp/brain_ingest_*.lock"):
        try:
            os.remove(lf)
        except Exception:
            pass

    # 6. Reset ready: true to ready: false in 03 - Inbox/*.md
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    draft_dir = os.path.join(inbox_dir, "Draft")
    source_dir = os.path.join(inbox_dir, "Source")
    clip_dir = os.path.join(vault_root, "99 - Meta", "Clipboard")

    if os.path.exists(inbox_dir):
        for f in os.listdir(inbox_dir):
            if f.endswith(".md") and not f.startswith(".") and f not in ("Review Dashboard.md", "Draft", "Source"):
                fp = os.path.join(inbox_dir, f)
                if os.path.isfile(fp):
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as rf:
                            content = rf.read()
                        has_fm, fm_t, _, bdy = brain_health.split_markdown_note(content)
                        if has_fm and re.search(r'ready:\s*(true|"true"|\'true\'|1)', fm_t, re.IGNORECASE):
                            rfm = re.sub(r'ready:\s*(true|"true"|\'true\'|1)', 'ready: false', fm_t, flags=re.IGNORECASE)
                            with open(fp, "w", encoding="utf-8") as wf:
                                wf.write(f"---\n{rfm.strip()}\n---\n\n{bdy.strip()}\n")
                    except Exception:
                        pass

    # 7. Clean up aborted in-progress drafts in 03 - Inbox/Draft/
    if os.path.exists(draft_dir):
        for f in os.listdir(draft_dir):
            if f.endswith(".md") and not f.startswith("."):
                dfp = os.path.join(draft_dir, f)
                try:
                    with open(dfp, "r", encoding="utf-8", errors="ignore") as df:
                        content = df.read()
                    has_fm, fm_t, _, bdy = brain_health.split_markdown_note(content)
                    if has_fm:
                        meta = brain_health.safe_load_frontmatter(fm_t, brain_health.build_yaml_engine())
                        if str(meta.get('status', '')).lower() == 'in-progress':
                            sfp = os.path.join(source_dir, f)
                            src_val = meta.get('source', 'original')
                            if os.path.exists(sfp):
                                try:
                                    with open(sfp, "r", encoding="utf-8", errors="ignore") as sf:
                                        s_content = sf.read()
                                    if src_val == "original" or "ready:" in s_content:
                                        # Restore manual source note to Inbox root with ready: false
                                        rfm = re.sub(r'ready:\s*(true|"true"|\'true\'|1)', 'ready: false', s_content, flags=re.IGNORECASE)
                                        if "ready:" not in rfm:
                                            rfm = f"---\nready: false\n---\n\n{s_content}"
                                        with open(os.path.join(inbox_dir, f), "w", encoding="utf-8") as wf:
                                            wf.write(rfm)
                                    os.remove(sfp)
                                except Exception:
                                    pass
                            # Clean up clipboard frames
                            name_stem = f[:-3]
                            if os.path.exists(clip_dir):
                                for img in os.listdir(clip_dir):
                                    if img.startswith(name_stem[:10]) or name_stem.lower().replace(' ', '_')[:10] in img:
                                        try: os.remove(os.path.join(clip_dir, img))
                                        except Exception: pass
                            os.remove(dfp)
                except Exception:
                    pass

    # 8. Append history entry and refresh Review Dashboard
    append_inbox_history(vault_root, "PANIC_ABORT", "Tutti i processi", "STOPPED", "Review Dashboard")
    update_review_dashboard(vault_root, in_progress="CLEAR_ALL")
    return len(aborted_pids)



def mark_draft_ready(vault_root: str, title_or_path: str) -> bool:
    """Transitions a note in 03 - Inbox/Draft/ from status: in-progress to status: draft,
    moving it from In Elaborazione to Note in Attesa di Approvazione."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    draft_dir = os.path.join(inbox_dir, "Draft")
    clean_title = brain_health.clean_title_str(title_or_path)
    draft_path = os.path.join(draft_dir, f"{clean_title}.md")
    if not os.path.exists(draft_path):
        draft_path = os.path.join(draft_dir, f"{title_or_path}.md")
    if not os.path.exists(draft_path) and os.path.isabs(title_or_path) and os.path.exists(title_or_path):
        draft_path = title_or_path
        clean_title = brain_health.clean_title_str(os.path.basename(draft_path)[:-3])
    if not os.path.exists(draft_path):
        return False

    with open(draft_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    has_fm, fm_text, breadcrumb, body = brain_health.split_markdown_note(content)
    if not has_fm:
        meta = {'title': clean_title, 'status': 'draft', 'type': 'concept', 'area': 'tech'}
    else:
        meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine())
        meta['status'] = 'draft'
        meta['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    fm_str = brain_health.format_canonical_frontmatter(meta)
    bc = breadcrumb or f"[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{clean_title}]]"
    new_content = brain_health.assemble_markdown_note(fm_str, bc, sanitize_style_highlights(body))
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    update_review_dashboard(vault_root, finish_in_progress=clean_title)
    return True


def update_review_dashboard(vault_root: str, in_progress: Optional[str] = None,
                            phase: Optional[str] = None,
                            add_error: Optional[Tuple[str, str]] = None,
                            finish_in_progress: Optional[str] = None,
                            replace_in_progress: Optional[str] = None):
    """Synchronizes 03 - Inbox/Review Dashboard.md in static Markdown across 4 sections with progressive phase feedback."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    draft_dir, source_dir = os.path.join(inbox_dir, "Draft"), os.path.join(inbox_dir, "Source")
    dash_path = os.path.join(inbox_dir, "Review Dashboard.md")
    os.makedirs(inbox_dir, exist_ok=True)
    pend_lines, err_lines, prog_lines = [], [], []

    # 1. Parse existing dashboard if present
    if os.path.exists(dash_path):
        with open(dash_path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
        cur = None
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("## ⏳") or "in elaborazione" in s.lower() or "in rielaborazione" in s.lower(): cur = "p"
            elif s.startswith("## 📥") or "in attesa" in s.lower() or "attesa di approvazione" in s.lower(): cur = "w"
            elif s.startswith("## ⚠️") or "errori" in s.lower(): cur = "e"
            elif s.startswith("## 📜") or "storico" in s.lower() or s.startswith("## ⚙️") or "istruzioni" in s.lower(): cur = None
            elif cur == "p":
                if s.startswith("- ⏳"):
                    prog_lines.append(line)
            elif cur == "w" and s.startswith("- ["): pend_lines.append(line)
            elif cur == "e" and s.startswith("- ["): err_lines.append(line)

    # 2. Reconcile on-disk Draft/ files completely without truncating frontmatter
    draft_files: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(draft_dir):
        for f in sorted(os.listdir(draft_dir)):
            if f.endswith('.md') and not f.startswith('.'):
                t = f[:-3]
                clean_t = brain_health.clean_title_str(t)
                t_clean_low = clean_t.lower()
                fp = os.path.join(draft_dir, f)
                is_in_prog = False
                source_val, video_val = None, None
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as d_f:
                        d_content = d_f.read()
                    has_fm, d_fm, _, _ = brain_health.split_markdown_note(d_content)
                    if has_fm:
                        meta = brain_health.safe_load_frontmatter(d_fm, brain_health.build_yaml_engine())
                        status_val = str(meta.get('status', 'draft')).lower()
                        if status_val == 'in-progress':
                            is_in_prog = True
                        source_val = meta.get('source')
                        video_val = meta.get('video_url')
                except Exception:
                    pass
                draft_files[t_clean_low] = {
                    'title': clean_t,
                    'is_in_prog': is_in_prog,
                    'filename': f,
                    'source': source_val,
                    'video_url': video_val
                }

    # 3. Handle explicit runtime in_progress
    if in_progress:
        if in_progress == "CLEAR_ALL":
            prog_lines = []
        else:
            p_item = in_progress.strip()
            p_phase = phase or "Fase 1/3: Estrazione Sorgente..."
            clean_p = brain_health.clean_title_str(p_item)
            p_line = f"- ⏳ [[Draft/{clean_p}]] ({p_phase})" if not p_item.startswith("http") else f"- ⏳ {p_item} ({p_phase})"
            existing_idx = None
            for idx, pl in enumerate(prog_lines):
                if (replace_in_progress and (replace_in_progress.lower() in pl.lower() or brain_health.clean_title_str(replace_in_progress).lower() in pl.lower())) or \
                   f"[[Draft/{clean_p}]]" in pl or \
                   f"[[{clean_p}]]" in pl or \
                   (p_item.startswith("http") and p_item.lower() in pl.lower()) or \
                   (not p_item.startswith("http") and clean_p.lower() in pl.lower()):
                    existing_idx = idx
                    break
            if existing_idx is not None:
                prog_lines[existing_idx] = p_line
            else:
                prog_lines.append(p_line)

    # 4. Handle explicit finish_in_progress
    if finish_in_progress:
        f_clean_low = brain_health.clean_title_str(finish_in_progress).lower()
        keep_in_prog = False
        if f_clean_low in draft_files and draft_files[f_clean_low]['is_in_prog']:
            keep_in_prog = True
        if not keep_in_prog:
            new_prog = []
            for l in prog_lines:
                m_pr = re.search(r'\[\[(?:Draft/)?(?P<name>[^\]]+)\]\]', l)
                if m_pr:
                    name_clean = brain_health.clean_title_str(m_pr.group('name')).lower()
                    if name_clean == f_clean_low:
                        continue
                elif finish_in_progress.lower() in l.lower() or f_clean_low in l.lower():
                    continue
                new_prog.append(l)
            prog_lines = new_prog

    # 5. Handle add_error
    if add_error:
        entry = f"- [ ] [!] Riprova: {add_error[0]} — Motivo: {add_error[1]}"
        replaced = False
        for idx, err_l in enumerate(err_lines):
            m_err_existing = RE_ERROR_LINE.match(err_l)
            if m_err_existing and m_err_existing.group('src').strip() == str(add_error[0]).strip():
                err_lines[idx] = entry
                replaced = True
                break
        if not replaced and entry not in err_lines:
            err_lines.append(entry)

    # 6. Reconcile progress lines (## ⏳ In Elaborazione)
    active_in_prog_names = set()
    reconciled_prog_lines = []

    if in_progress and in_progress != "CLEAR_ALL":
        p_item = in_progress.strip()
        if not p_item.startswith("http"):
            active_in_prog_names.add(brain_health.clean_title_str(p_item).lower())

    seen_prog_names = set()
    for pl in prog_lines:
        m_pr = re.search(r'\[\[(?:Draft/)?(?P<name>[^\]]+)\]\]', pl)
        if m_pr:
            name_clean = brain_health.clean_title_str(m_pr.group('name'))
            name_low = name_clean.lower()
            if name_low in draft_files:
                d_info = draft_files[name_low]
                if d_info['is_in_prog'] or (in_progress and brain_health.clean_title_str(in_progress).lower() == name_low):
                    if name_low not in seen_prog_names:
                        reconciled_prog_lines.append(pl)
                        seen_prog_names.add(name_low)
                        active_in_prog_names.add(name_low)
            else:
                if (in_progress and brain_health.clean_title_str(in_progress).lower() == name_low) or is_source_lock_active(name_clean):
                    if name_low not in seen_prog_names:
                        reconciled_prog_lines.append(pl)
                        seen_prog_names.add(name_low)
                        active_in_prog_names.add(name_low)
        else:
            m_url = re.search(r'https?://[^\s\)]+', pl)
            url_str = m_url.group(0) if m_url else None
            if url_str:
                matching_draft = None
                for d_low, d_info in draft_files.items():
                    if d_info.get('source') == url_str or d_info.get('video_url') == url_str:
                        matching_draft = d_info
                        break
                if matching_draft:
                    if matching_draft['is_in_prog']:
                        active_in_prog_names.add(matching_draft['title'].lower())
                    continue
                if is_source_lock_active(url_str) or (in_progress and url_str in in_progress):
                    reconciled_prog_lines.append(pl)

    for name_low, d_info in draft_files.items():
        if d_info['is_in_prog']:
            active_in_prog_names.add(name_low)
            if name_low not in seen_prog_names:
                reconciled_prog_lines.append(f"- ⏳ [[Draft/{d_info['title']}]] (Fase 2/3: Rielaborazione Concettuale AI...)")
                seen_prog_names.add(name_low)

    prog_lines = reconciled_prog_lines

    # 7. Reconcile pend_lines (## 📥 Note in Attesa di Approvazione)
    existing_pend_map = {}
    for l in pend_lines:
        m = RE_APPROVAL_LINE.match(l)
        if m:
            n = brain_health.clean_title_str(m.group('name'))
            existing_pend_map[n.lower()] = l

    reconciled_pend_lines = []
    for name_low, d_info in draft_files.items():
        if d_info['is_in_prog'] or name_low in active_in_prog_names:
            continue
        src_exists = os.path.exists(os.path.join(source_dir, d_info['filename']))
        if name_low in existing_pend_map:
            reconciled_pend_lines.append(existing_pend_map[name_low])
        else:
            line_str = f"- [ ] Approva [[Draft/{d_info['title']}]] (fonte: [[Source/{d_info['title']}]])" if src_exists else f"- [ ] Approva [[Draft/{d_info['title']}]]"
            reconciled_pend_lines.append(line_str)

    pend_lines = reconciled_pend_lines

    hist_lines = []
    log_file = os.path.join(vault_root, "99 - Meta", "logs", "inbox_history.md")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            hist_lines = [l.strip() for l in f.readlines() if re.match(r'^-\s+\d{4}-\d{2}-\d{2}', l.strip())][-10:]

    now_iso, now_ts = datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    dash = ["---", "status: draft", "type: moc", "area: meta", 'related: ["[[Home MOC]]", "[[Vault Health Dashboard]]"]',
            'aliases: []', "source: original", 'title: "Review Dashboard"', f"date: '{now_iso}'", f"updated: {now_ts}",
            "tags: [meta/dashboard, meta/gtd]", 'summary: "Dashboard di revisione GTD per l\'approvazione o scarto delle note in Inbox."',
            "---", "[[Home MOC|Home]] / [[Atlas]] / [[Review Dashboard]]\n", "# 📥 Inbox Review Dashboard\n",
            "## ⚙️ Istruzioni per la Revisione",
            "* **APPROVARE** una proposta: Sostituisci `[ ]` con `[x]` (la nota passerà a `status: permanent` e verrà spostata nel target).",
            "* **RIFIUTARE** una proposta: Sostituisci `[ ]` con `[-]` (bozza, file sorgente e clipboard verranno eliminati).",
            "* **RIPROVARE UN ERRORE**: Sostituisci `[ ]` con `[x]` per ritentare l'ingestione (`[-]` per ignorare l'errore).",
            "* **PANIC BUTTON**: Sostituisci `[ ]` con `[x]` su `🛑 Interrompi...` per terminare tutte le rielaborazioni in corso senza bloccare il watcher.\n",
            "## ⏳ In Elaborazione",
            PANIC_BUTTON_LINE] + (prog_lines or ["*Nessun processo attivo.*"]) + [
            "\n## 📥 Note in Attesa di Approvazione"] + (pend_lines or ["*Nessuna nota in attesa di approvazione.*"]) + [
            "\n## ⚠️ Errori di Acquisizione & Azioni Richieste"] + (err_lines or ["*Nessun errore registrato.*"]) + [
            "\n## 📜 Storico Recente"] + (hist_lines or ["*Nessuna azione recente registrata.*"])

    with open(dash_path, "w", encoding="utf-8") as f: f.write("\n".join(dash) + "\n")



def format_note_header_block(title: str, metadata: Dict[str, Any]) -> str:
    """Generates canonical header metadata list for video and web notes right below # Title."""
    source = str(metadata.get('source') or metadata.get('video_url') or '').strip()
    channel = str(metadata.get('channel') or '').strip()
    date_val = str(metadata.get('date') or datetime.date.today().isoformat()).strip()
    note_type = str(metadata.get('type') or 'concept').strip()
    area_val = str(metadata.get('area') or 'tech').strip().lower()

    area_map = {
        'tech': ('Tech & AI MOC', 'Tech & AI'),
        'finance': ('Finance MOC', 'Finance'),
        'education': ('Education & Learning MOC', 'Education & Learning'),
        'mentality': ('Personal Growth & Health MOC', 'Personal Growth & Health'),
        'projects': ('Projects MOC', 'Projects'),
        'meta': ('Home MOC', 'Meta'),
    }
    moc_name, moc_label = area_map.get(area_val, ('Tech & AI MOC', 'Tech & AI'))

    lines = []
    if note_type == 'video' or (source and 'youtu' in source):
        lines.append(f"- **Video URL**: {source}")
        if channel:
            clean_c = channel.strip()
            if clean_c.startswith("[[") and clean_c.endswith("]]"):
                lines.append(f"- **Canale**: {clean_c}")
            else:
                lines.append(f"- **Canale**: [[{clean_c}]]")
    elif note_type == 'article' and source.startswith('http'):
        domain = urllib.parse.urlparse(source).netloc.replace('www.', '') or 'Web'
        lines.append(f"- **Fonte**: [{domain}]({source})")
        lines.append(f"- **Data Acquisizione**: {date_val}")
        lines.append(f"- **Area**: [[{moc_name}|{moc_label}]]")

    if lines:
        return "\n".join(lines) + "\n\n---\n"
    return ""

def stage_note(vault_root: str, title: str, body: str, metadata: Optional[Dict[str, Any]] = None,
               target_dir: str = "02 - Atlas", source_content: Optional[str] = None,
               status: Optional[str] = None) -> str:
    """Writes draft to 03 - Inbox/Draft/<Title>.md and source to 03 - Inbox/Source/<Title>.md."""
    clean_title = brain_health.clean_title_str(title)
    draft_dir, source_dir = os.path.join(vault_root, "03 - Inbox", "Draft"), os.path.join(vault_root, "03 - Inbox", "Source")
    os.makedirs(draft_dir, exist_ok=True); os.makedirs(source_dir, exist_ok=True)
    meta = dict(metadata) if metadata else {}
    meta['title'] = clean_title
    if status is not None:
        meta['status'] = status
    else:
        meta.setdefault('status', 'draft')

    if 'target_path' in meta and meta['target_path']:
        tp_dir = os.path.dirname(meta['target_path'])
        tp_stem = brain_health.clean_title_str(os.path.basename(meta['target_path'])[:-3])
        if tp_stem.lower().startswith("raw note") or tp_stem.lower() in ("untitled", "draft", "bozza", "nuova nota") or (not clean_title.lower().startswith("raw note") and clean_title != tp_stem):
            meta['target_path'] = os.path.join(tp_dir, f"{clean_title}.md") if tp_dir else f"{target_dir}/{clean_title}.md"
    else:
        meta['target_path'] = f"{target_dir}/{clean_title}.md"

    for k, v in [('date', datetime.date.today().isoformat()), ('type', 'concept'), ('area', 'tech'), ('source', 'original'), ('tags', [f"{meta.get('area', 'tech')}/raw"])]:
        meta.setdefault(k, v)

    # Clean redundant title lines from beginning of body if present
    body_clean = body.strip()
    body_clean = re.sub(r'^#\s+[^\n]+\n*', '', body_clean)
    body_clean = re.sub(r'^\s*' + re.escape(clean_title) + r'\s*\n*', '', body_clean, flags=re.IGNORECASE)
    body_clean = re.sub(r'^-\s+\*\*(?:Fonte|Video URL|Canale|Sorgente Video).*?\n+(?:-\s+\*\*.*?\n+)*---\n*', '', body_clean, flags=re.DOTALL)

    header_block = format_note_header_block(clean_title, meta)
    full_body = f"# {clean_title}\n\n"
    if header_block:
        full_body += header_block + "\n"
    full_body += body_clean.strip()

    fm_str = brain_health.format_canonical_frontmatter(meta)
    breadcrumb = f"[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[{clean_title}]]"
    note_content = brain_health.assemble_markdown_note(fm_str, breadcrumb, sanitize_style_highlights(full_body))

    draft_path = os.path.join(draft_dir, f"{clean_title}.md")
    with open(draft_path, "w", encoding="utf-8") as f: f.write(note_content)
    if source_content is not None:
        with open(os.path.join(source_dir, f"{clean_title}.md"), "w", encoding="utf-8") as f: f.write(source_content)

    if meta.get('status') == 'in-progress':
        update_review_dashboard(vault_root, in_progress=clean_title, phase="Fase 2/3: Rielaborazione Concettuale AI...")
    else:
        update_review_dashboard(vault_root, finish_in_progress=clean_title)
    return draft_path


def process_tri_state_approvals(vault_root: str) -> int:
    """Processes [x] (Promote), [-] (Purge), panic button, and error retry/dismiss lines in Review Dashboard.md."""
    dash_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    if not os.path.exists(dash_path): return 0
    with open(dash_path, "r", encoding="utf-8", errors="ignore") as f: lines = f.readlines()
    processed_count, updated_lines, pending_errors = 0, [], []
    panic_triggered = False

    for line in lines:
        m_panic = RE_PANIC_LINE.match(line)
        if m_panic:
            if m_panic.group('status') in ('x', 'X', '-'):
                panic_triggered = True
            continue

        m_err = RE_ERROR_LINE.match(line)
        if m_err:
            status = m_err.group('status')
            if status == ' ':
                updated_lines.append(line); continue
            src_target = m_err.group('src').strip()
            if status in ('x', 'X'):
                try:
                    raw_file = os.path.join(vault_root, "03 - Inbox", src_target)
                    if not os.path.exists(raw_file) and not src_target.endswith('.md'):
                        raw_file = os.path.join(vault_root, "03 - Inbox", f"{src_target}.md")
                    matching_raw_file = None
                    if os.path.exists(raw_file) and not os.path.isdir(raw_file):
                        matching_raw_file = raw_file
                    else:
                        inbox_dir = os.path.join(vault_root, "03 - Inbox")
                        if os.path.exists(inbox_dir):
                            for ib_f in os.listdir(inbox_dir):
                                if ib_f.endswith('.md') and not ib_f.startswith('.') and ib_f not in ("Review Dashboard.md", "Draft", "Source"):
                                    ib_fp = os.path.join(inbox_dir, ib_f)
                                    try:
                                        with open(ib_fp, 'r', encoding='utf-8', errors='ignore') as rf: rfc = rf.read()
                                        _, rfm_t, _, _ = brain_health.split_markdown_note(rfc)
                                        rmeta = brain_health.safe_load_frontmatter(rfm_t, brain_health.build_yaml_engine())
                                        if rmeta.get('video_url') == src_target or rmeta.get('source') == src_target:
                                            matching_raw_file = ib_fp
                                            break
                                    except Exception:
                                        pass

                    if matching_raw_file:
                        with open(matching_raw_file, 'r', encoding='utf-8', errors='ignore') as rf: rfc = rf.read()
                        _, rfm_t, _, rbdy = brain_health.split_markdown_note(rfc)
                        rfm_fixed = re.sub(r'ready:\s*false', 'ready: true', rfm_t, flags=re.IGNORECASE)
                        if 'ready:' not in rfm_fixed: rfm_fixed += "\nready: true"
                        with open(matching_raw_file, 'w', encoding='utf-8') as rf: rf.write(f"---\n{rfm_fixed.strip()}\n---\n\n{rbdy.strip()}\n")
                        process_inbox_raw_notes(vault_root)
                    else:
                        ingest_source(src_target, vault_root=vault_root, force=True)
                    append_inbox_history(vault_root, "RETRY_SUCCESS", src_target, "03 - Inbox/Draft")
                    processed_count += 1
                except Exception as e:
                    pending_errors.append((src_target, str(e)))
                    append_inbox_history(vault_root, "RETRY_FAILED", src_target, str(e))
            elif status == '-':
                raw_file = os.path.join(vault_root, "03 - Inbox", src_target)
                if not os.path.exists(raw_file) and not src_target.endswith('.md'):
                    raw_file = os.path.join(vault_root, "03 - Inbox", f"{src_target}.md")
                if os.path.exists(raw_file) and not os.path.isdir(raw_file):
                    try: os.remove(raw_file)
                    except Exception: pass
                else:
                    inbox_dir = os.path.join(vault_root, "03 - Inbox")
                    if os.path.exists(inbox_dir):
                        for ib_f in os.listdir(inbox_dir):
                            if ib_f.endswith('.md') and not ib_f.startswith('.') and ib_f not in ("Review Dashboard.md", "Draft", "Source"):
                                ib_fp = os.path.join(inbox_dir, ib_f)
                                try:
                                    with open(ib_fp, 'r', encoding='utf-8', errors='ignore') as rf: rfc = rf.read()
                                    _, rfm_t, _, _ = brain_health.split_markdown_note(rfc)
                                    rmeta = brain_health.safe_load_frontmatter(rfm_t, brain_health.build_yaml_engine())
                                    if rmeta.get('video_url') == src_target or rmeta.get('source') == src_target:
                                        os.remove(ib_fp)
                                except Exception:
                                    pass
                append_inbox_history(vault_root, "ERROR_DISMISSED", src_target, "DISMISSED")
                processed_count += 1
            continue

        m = RE_APPROVAL_LINE.match(line)
        if not m or m.group('status') == ' ':
            updated_lines.append(line); continue
        status, raw_name = m.group('status'), m.group('name')
        name = brain_health.clean_title_str(raw_name)
        draft_path = os.path.join(vault_root, "03 - Inbox", "Draft", f"{name}.md")
        if not os.path.exists(draft_path): draft_path = os.path.join(vault_root, "03 - Inbox", "Draft", f"{raw_name}.md")
        if not os.path.exists(draft_path): draft_path = os.path.join(vault_root, "03 - Inbox", f"{name}.md")
        if not os.path.exists(draft_path): draft_path = os.path.join(vault_root, "03 - Inbox", f"{raw_name}.md")
        source_path = os.path.join(vault_root, "03 - Inbox", "Source", f"{name}.md")
        if not os.path.exists(source_path): source_path = os.path.join(vault_root, "03 - Inbox", "Source", f"{raw_name}.md")

        if status in ('x', 'X'):
            if not os.path.exists(draft_path): continue
            with open(draft_path, "r", encoding="utf-8") as f: content = f.read()
            _, fm_text, _, body = brain_health.split_markdown_note(content)
            meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine())

            meta_title = brain_health.clean_title_str(str(meta.get('title') or ''))
            if name.lower().startswith("raw note") or name.lower() in ("untitled", "draft", "bozza", "nuova nota", ""):
                real_name = meta_title if (meta_title and not meta_title.lower().startswith("raw note") and meta_title.lower() not in ("untitled", "draft", "bozza", "nuova nota")) else name
            else:
                real_name = name

            target_rel = meta.get('target_path')
            if target_rel:
                target_dir_part = os.path.dirname(target_rel)
                old_file_stem = brain_health.clean_title_str(os.path.basename(target_rel)[:-3])
                if old_file_stem.lower().startswith("raw note") or old_file_stem.lower() in ("untitled", "draft", "bozza", "nuova nota") or (not real_name.lower().startswith("raw note") and real_name != old_file_stem):
                    target_file_part = f"{real_name}.md"
                else:
                    target_file_part = f"{old_file_stem}.md"
                target_rel = os.path.join(target_dir_part, target_file_part) if target_dir_part else target_file_part
            else:
                target_rel = classify_target_directory(real_name, meta.get('tags', []), body) + f"/{real_name}.md"

            dest_abs, vault_abs = os.path.abspath(os.path.join(vault_root, target_rel)), os.path.abspath(vault_root)

            if not dest_abs.startswith(vault_abs + os.sep) and dest_abs != vault_abs:
                pending_errors.append((real_name, f"Path traversal bloccato: {target_rel}"))
                updated_lines.append(line); continue
            src_val = meta.get('source', 'original')
            dup = check_duplicate_resource(vault_root, src_val, real_name)
            if dup and os.path.abspath(dup[0]) != dest_abs:
                pending_errors.append((real_name, f"Duplicato sorgente rilevato in {os.path.relpath(dup[0], vault_root)}"))
                updated_lines.append(line); continue
            if os.path.exists(dest_abs):
                with open(dest_abs, 'r', encoding='utf-8', errors='ignore') as f: dest_text = f.read(1500)
                if src_val != 'original' and src_val not in dest_text:
                    pending_errors.append((real_name, f"Conflitto nome file con sorgente diversa in {target_rel}"))
                    updated_lines.append(line); continue

            meta['status'] = 'permanent'
            meta['title'] = real_name
            meta['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
            if 'target_path' in meta: del meta['target_path']
            clean_body, _ = brain_health.strip_isolated_hashtag_lines(body)
            fm_str = brain_health.format_canonical_frontmatter(meta, is_blog=target_rel.startswith("05 - Blog"))
            final_note = brain_health.assemble_markdown_note(fm_str, brain_health.get_breadcrumbs(target_rel, real_name), sanitize_style_highlights(clean_body))

            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            with open(dest_abs, "w", encoding="utf-8") as f: f.write(final_note)
            if os.path.exists(draft_path): os.remove(draft_path)

            if os.path.exists(source_path):
                src_txt = ""
                with open(source_path, 'r', encoding='utf-8', errors='ignore') as sf:
                    src_txt = sf.read(500)
                if src_val == "original" or "ready:" in src_txt:
                    arc_dir = os.path.join(vault_root, "99 - Meta", "Archive")
                    os.makedirs(arc_dir, exist_ok=True)
                    shutil.move(source_path, os.path.join(arc_dir, f"{real_name}.md"))
                else: os.remove(source_path)

            append_inbox_history(vault_root, "APPROVED", real_name, target_rel, src_val)
            processed_count += 1

        elif status == '-':
            if os.path.exists(draft_path): os.remove(draft_path)
            if os.path.exists(source_path): os.remove(source_path)
            clip_dir = os.path.join(vault_root, "99 - Meta", "Clipboard")
            if os.path.exists(clip_dir):
                for img in os.listdir(clip_dir):
                    if img.startswith(name[:10]) or name.lower().replace(' ', '_')[:10] in img:
                        try: os.remove(os.path.join(clip_dir, img))
                        except Exception: pass
            append_inbox_history(vault_root, "REJECTED", name, "PURGED")
            processed_count += 1

    if panic_triggered:
        trigger_panic_abort(vault_root)
        processed_count += 1
    else:
        with open(dash_path, "w", encoding="utf-8") as f: f.writelines(updated_lines)
        update_review_dashboard(vault_root)
        for err_src, err_rsn in pending_errors: update_review_dashboard(vault_root, add_error=(err_src, err_rsn))
    return processed_count


def process_inbox_raw_notes(vault_root: str) -> List[str]:
    """Scans 03 - Inbox/ root for ready: true notes and stages their source into Source/, placing them under In Elaborazione."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    source_dir = os.path.join(inbox_dir, "Source")
    os.makedirs(source_dir, exist_ok=True)
    if not os.path.exists(inbox_dir): return []
    processed = []

    for file in sorted(os.listdir(inbox_dir)):
        if not file.endswith('.md') or file.startswith('.') or file in ("Review Dashboard.md", "Draft", "Source"): continue
        file_path = os.path.join(inbox_dir, file)
        if os.path.isdir(file_path): continue
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
            has_fm, fm_text, _, body = brain_health.split_markdown_note(content)
            meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine()) if has_fm else {}
            if str(meta.get('ready')).lower() != 'true': continue

            clean_title = brain_health.clean_title_str(meta.get('title') or file[:-3])
            if clean_title.lower().startswith("raw note") or clean_title.lower() in ("untitled", "draft", "bozza", "nuova nota", ""):
                m_h1 = re.search(r'^\s*#\s+([^\n]+)', body, re.MULTILINE)
                if m_h1:
                    cand_h1 = brain_health.clean_title_str(m_h1.group(1).strip())
                    if cand_h1 and not cand_h1.lower().startswith("raw note") and cand_h1.lower() not in ("untitled", "draft", "bozza", "nuova nota", "appunti grezzi", "idee"):
                        clean_title = cand_h1

            src_url = meta.get('video_url') or meta.get('source')
            check_title = "" if (src_url or clean_title.lower().startswith("raw note")) else clean_title

            dup = check_duplicate_resource(vault_root, src_url, check_title)
            if dup:
                raw_fm = re.sub(r'ready:\s*(true|"true"|\'true\')', 'ready: false', fm_text, flags=re.IGNORECASE)
                if 'ready:' not in raw_fm: raw_fm += "\nready: false"
                with open(file_path, 'w', encoding='utf-8') as f: f.write(f"---\n{raw_fm.strip()}\n---\n\n{body.strip()}\n")
                record_ingest_error(vault_root, src_url or clean_title, f"Duplicato rilevato: {os.path.relpath(dup[0], vault_root)}")
                continue

            if src_url and detect_input_type(src_url) in ("youtube", "web"):
                extract_frames_val = meta.get('extract_frames') or meta.get('frames')
                force_frames_bool = str(extract_frames_val).lower() == 'true' if extract_frames_val is not None else False
                depth_val = str(meta.get('depth') or "approfondimento")
                ingest_source(src_url, vault_root=vault_root, force=False, extract_frames=force_frames_bool, depth=depth_val)
                if os.path.exists(file_path): os.remove(file_path)
                processed.append(src_url)
                continue

            # -------------------------------------------------------------
            # FASE 1/3: Estrazione Sorgente
            # -------------------------------------------------------------
            update_review_dashboard(vault_root, in_progress=clean_title, phase="Fase 1/3: Estrazione Sorgente...")
            target_dir = classify_target_directory(clean_title, meta.get('tags', []), body)

            # -------------------------------------------------------------
            # FASE 2/3: Rielaborazione Concettuale AI
            # -------------------------------------------------------------
            update_review_dashboard(vault_root, in_progress=clean_title, phase="Fase 2/3: Rielaborazione Concettuale AI...")
            meta['title'] = clean_title
            meta['target_path'] = f"{target_dir}/{clean_title}.md"
            stage_note(vault_root, clean_title, body, meta, target_dir=target_dir, source_content=content, status='in-progress')
            if os.path.exists(file_path): os.remove(file_path)

            enriched_body, summary = enrich_draft_with_ai(vault_root, clean_title, content, depth="approfondimento", source_type="concept", source_url="original")

            if clean_title.lower().startswith("raw note") or clean_title.lower() in ("untitled", "draft", "bozza", "nuova nota", ""):
                m_ai_h1 = re.search(r'^\s*#\s+([^\n]+)', enriched_body, re.MULTILINE)
                if m_ai_h1:
                    cand_ai = brain_health.clean_title_str(m_ai_h1.group(1).strip())
                    if cand_ai and not cand_ai.lower().startswith("raw note") and cand_ai.lower() not in ("untitled", "draft", "bozza", "nuova nota", "appunti grezzi", "idee"):
                        old_in_prog = os.path.join(vault_root, "03 - Inbox", "Draft", f"{clean_title}.md")
                        old_source = os.path.join(vault_root, "03 - Inbox", "Source", f"{clean_title}.md")
                        clean_title = cand_ai
                        target_dir = classify_target_directory(clean_title, meta.get('tags', []), enriched_body)
                        if os.path.exists(old_in_prog) and clean_title != cand_ai:
                            try: os.remove(old_in_prog)
                            except Exception: pass
                        if os.path.exists(old_source) and clean_title != cand_ai:
                            try: os.remove(old_source)
                            except Exception: pass

            meta['title'] = clean_title
            meta['target_path'] = f"{target_dir}/{clean_title}.md"
            stage_note(vault_root, clean_title, enriched_body, meta, target_dir=target_dir, source_content=content, status='in-progress')

            # -------------------------------------------------------------
            # FASE 3/3: Autolinking & Staging
            # -------------------------------------------------------------
            linked_body, links = autolink_content(vault_root, enriched_body, clean_title)
            meta['summary'] = summary
            if links: meta['related'] = links
            stage_note(vault_root, clean_title, linked_body, meta, target_dir=target_dir, status='draft')
            processed.append(clean_title)

        except Exception as e:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
                _, fm_t, _, bdy = brain_health.split_markdown_note(c)
                rfm = re.sub(r'ready:\s*(true|"true"|\'true\')', 'ready: false', fm_t, flags=re.IGNORECASE)
                if 'ready:' not in rfm: rfm += "\nready: false"
                with open(file_path, 'w', encoding='utf-8') as f: f.write(f"---\n{rfm.strip()}\n---\n\n{bdy.strip()}\n")
            except Exception: pass
            err_target = src_url if (src_url and str(src_url).strip()) else file
            record_ingest_error(vault_root, err_target, str(e))
    return processed

def ingest_source(source: str, vault_root: Optional[str] = None, target_dir: Optional[str] = None,
                  depth: str = "approfondimento", extract_frames: bool = False, force: bool = False, use_ai: bool = True) -> str:
    """Unified entry point executing the lean 3-macro-phase lifecycle into 03 - Inbox/Draft/."""
    root = brain_health.get_vault_root(vault_root)
    result_path = None
    with NoteLock(source):
        in_type = detect_input_type(source)
        prov = Path(source).stem if in_type == "file" else (source if in_type in ("youtube", "web") else source.strip().splitlines()[0].lstrip('#').strip()[:40])

        # -------------------------------------------------------------
        # FASE 1/3: Estrazione Sorgente
        # -------------------------------------------------------------
        update_review_dashboard(root, in_progress=prov, phase="Fase 1/3: Estrazione Sorgente...")
        try:
            if in_type == "youtube":
                if not force:
                    dup = check_duplicate_resource(root, source, "")
                    if dup:
                        record_ingest_error(root, source, f"Duplicato rilevato: {os.path.relpath(dup[0], root)}")
                        raise ValueError(f"Duplicate YouTube resource: {source}")
                try:
                    data = youtube_helper.extract_youtube_data(source, force_frames=(True if extract_frames else None), vault_root=root)
                except youtube_helper.TranscriptUnavailableError as e:
                    record_ingest_error(root, source, f"Trascrizione non disponibile: {e}")
                    raise
                except Exception as e:
                    record_ingest_error(root, source, f"Errore estrazione YouTube: {e}")
                    raise
                title, channel = data['title'], data['channel']
                clean_title = brain_health.clean_title_str(title)
                raw_text = " ".join([t.get('text', '') for t in data['transcript']])
                dest_dir = target_dir or classify_target_directory(clean_title, ['tech/ai', 'video'], raw_text)
                meta = {'title': clean_title, 'type': 'video', 'area': 'tech', 'source': source, 'video_url': source, 'channel': channel, 'tags': ['tech/ai', 'video']}

            elif in_type == "file":
                with open(source, 'r', encoding='utf-8') as f: raw_text = f.read()
                title = Path(source).stem
                clean_title = brain_health.clean_title_str(title)
                dest_dir = target_dir or classify_target_directory(clean_title, ['raw'], raw_text)
                meta = {'title': clean_title, 'type': 'concept', 'area': 'tech', 'source': 'original', 'tags': ['raw']}

            else:
                lines = [l.strip() for l in source.strip().splitlines() if l.strip()]
                title = lines[0].lstrip('#').strip() if lines else "Nuova Nota"
                clean_title = brain_health.clean_title_str(title)
                raw_text = source
                dest_dir = target_dir or classify_target_directory(clean_title, ['tech'], source)
                meta = {'title': clean_title, 'type': 'article' if in_type == 'web' else 'concept', 'area': 'tech', 'source': source if in_type == 'web' else 'original'}

            # -------------------------------------------------------------
            # FASE 2/3: Rielaborazione Concettuale AI
            # -------------------------------------------------------------
            update_review_dashboard(root, in_progress=clean_title, phase="Fase 2/3: Rielaborazione Concettuale AI...", replace_in_progress=prov)
            dest_dir = target_dir or classify_target_directory(clean_title, meta.get('tags', []), raw_text)
            meta['title'] = clean_title
            meta['target_path'] = f"{dest_dir}/{clean_title}.md"
            stage_note(root, clean_title, raw_text, meta, target_dir=dest_dir, source_content=raw_text, status='in-progress')

            if use_ai:
                enriched_body, summary = enrich_draft_with_ai(root, clean_title, raw_text, depth=depth, source_type=in_type, source_url=source)
            else:
                enriched_body = format_structured_note(clean_title, raw_text, depth=depth, source_type=in_type, source_url=source)
                summary = f"Trattazione concettuale ed evidenze chiave per {clean_title}."

            if clean_title.lower().startswith("raw note") or clean_title.lower() in ("untitled", "draft", "bozza", "nuova nota"):
                m_ai_h1 = re.search(r'^\s*#\s+([^\n]+)', enriched_body, re.MULTILINE)
                if m_ai_h1:
                    cand_ai = brain_health.clean_title_str(m_ai_h1.group(1).strip())
                    if cand_ai and not cand_ai.lower().startswith("raw note") and cand_ai.lower() not in ("untitled", "draft", "bozza", "nuova nota", "appunti grezzi", "idee"):
                        old_in_prog = os.path.join(root, "03 - Inbox", "Draft", f"{clean_title}.md")
                        old_source = os.path.join(root, "03 - Inbox", "Source", f"{clean_title}.md")
                        clean_title = cand_ai
                        meta['title'] = clean_title
                        if os.path.exists(old_in_prog) and clean_title != cand_ai:
                            try: os.remove(old_in_prog)
                            except Exception: pass
                        if os.path.exists(old_source) and clean_title != cand_ai:
                            try: os.remove(old_source)
                            except Exception: pass

            dest_dir = target_dir or classify_target_directory(clean_title, meta.get('tags', []), enriched_body)
            meta['title'] = clean_title
            meta['target_path'] = f"{dest_dir}/{clean_title}.md"
            stage_note(root, clean_title, enriched_body, meta, target_dir=dest_dir, source_content=raw_text, status='in-progress')

            # -------------------------------------------------------------
            # FASE 3/3: Autolinking & Staging
            # -------------------------------------------------------------
            linked_body, links = autolink_content(root, enriched_body, clean_title)
            meta['summary'] = summary
            if links:
                meta['related'] = links
            result_path = stage_note(root, clean_title, linked_body, meta, target_dir=dest_dir, status='draft')

        except Exception:
            update_review_dashboard(root, in_progress="CLEAR_ALL")
            raise

    update_review_dashboard(root)
    return result_path or ""

def main():
    parser = argparse.ArgumentParser(description="Unified Second Brain Ingestion & GTD Staging Engine.")
    parser.add_argument('input', nargs='?', default=None, help="URL, file path, or raw text to ingest")
    parser.add_argument('--scan-inbox', action='store_true', help="Scan 03 - Inbox/ for notes with ready: true")
    parser.add_argument('--process-approvals', action='store_true', help="Process [x] and [-] lines in Review Dashboard.md")
    parser.add_argument('--ready', '--mark-ready', dest='mark_ready', default=None, help="Mark draft note as ready (status: draft) and update Review Dashboard")
    parser.add_argument('--refresh', action='store_true', help="Refresh and reconcile Review Dashboard.md")
    parser.add_argument('--no-ai', '--skip-ai', dest='no_ai', action='store_true', help="Skip autonomous AI Phase 2 enrichment (keeps in-progress or uses heuristic)")
    parser.add_argument('--depth', choices=['approfondimento', 'sintesi', 'deep', 'executive'], default='approfondimento')
    parser.add_argument('--extract-frames', action='store_true', help="Extract YouTube keyframes via ffmpeg")
    parser.add_argument('--force', action='store_true', help="Bypass duplicate resource check")
    parser.add_argument('--panic', action='store_true', help="Emergency stop: terminate all active ingestion/processing jobs")
    parser.add_argument('--in-progress', dest='set_in_progress', default=None, help="Set active item in progress on Review Dashboard")
    parser.add_argument('--phase', default=None, help="Phase description for in-progress item (e.g. 'Fase 1/3: ...')")
    parser.add_argument('--clear-in-progress', action='store_true', help="Clear in progress section on Review Dashboard")
    parser.add_argument('--target-dir', default=None, help="Custom target directory for promotion")
    parser.add_argument('--vault-root', default=None, help="Vault root directory")
    args = parser.parse_args()

    root = brain_health.get_vault_root(args.vault_root)
    if args.panic:
        count = trigger_panic_abort(root)
        print(f"Panic abort executed. Terminated {count} process(es). Watcher is active.")
    elif args.mark_ready:
        ok = mark_draft_ready(root, args.mark_ready)
        if ok:
            print(f"Marked draft ready: {args.mark_ready}")
        else:
            print(f"Error: Draft note '{args.mark_ready}' not found in 03 - Inbox/Draft/", file=sys.stderr)
            sys.exit(1)
    elif args.refresh:
        update_review_dashboard(root)
        print("Review Dashboard refreshed.")
    elif args.set_in_progress:
        update_review_dashboard(root, in_progress=args.set_in_progress, phase=args.phase)
        print(f"Set in progress: {args.set_in_progress} ({args.phase or 'Fase 1/3...'})")
    elif args.clear_in_progress:
        update_review_dashboard(root, in_progress="CLEAR_ALL")
        print("Cleared in progress.")
    elif args.process_approvals:
        print(f"Processed {process_tri_state_approvals(root)} approval/rejection items.")
    elif args.scan_inbox:
        items = process_inbox_raw_notes(root)
        print(f"Staged {len(items)} raw inbox notes: {items}")
    elif args.input:
        depth = "approfondimento" if args.depth in ("deep", "approfondimento") else "sintesi"
        path = ingest_source(args.input, vault_root=root, target_dir=args.target_dir, depth=depth, extract_frames=args.extract_frames, force=args.force, use_ai=not args.no_ai)
        print(f"Draft staged at: {path}")
    else:
        update_review_dashboard(root)
        print("Review Dashboard refreshed.")

if __name__ == '__main__':
    main()

