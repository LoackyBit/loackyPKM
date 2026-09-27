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

import os, sys, re, datetime, hashlib, argparse, shutil, glob, time, subprocess, urllib.parse, logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path: sys.path.insert(0, SCRIPT_DIR)

import brain_health, youtube_helper, anki_helper

YT_URL_REGEX = re.compile(r'(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})')
WEB_URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
RE_APPROVAL_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+Approva\s+\[\[(?:Draft/)?(?P<name>[^\]]+)\]\](?:\s+\(fonte:\s+\[\[(?:Source/)?(?P<src>[^\]]+)\]\]\))?(?:\s+\(.*target:\s*(?P<target>.*?)\))?')
RE_ERROR_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+\[!\]\s+Riprova:\s+(?P<src>.*?)(?:\s+—\s+Motivo:\s*(?P<reason>.*))?$')
RE_PANIC_LINE = re.compile(r'^\s*-\s+\[(?P<status>[ xX\-])\]\s+.*(?:🛑|Interrompi|Panic\s+Button).*', re.IGNORECASE)
PANIC_BUTTON_LINE = "- [ ] 🛑 Interrompi elaborazioni attive (Panic Button)"
DEFAULT_AI_MODEL = os.environ.get("BRAIN_AI_MODEL", "gemini-3.8-flash-low")

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


class DashboardLock:
    """Mutex lock for 03 - Inbox/Review Dashboard.md with PID tracking, ISO timestamp, TTL auto-healing, and re-entrancy."""
    _process_locks: Dict[str, int] = {}

    def __init__(self, vault_root: str, timeout: float = 10.0, retry_interval: float = 0.2, ttl_seconds: int = 60, blocking: bool = True):
        vault_hash = hashlib.sha1(vault_root.encode('utf-8')).hexdigest()[:8]
        self.lock_file = f"/tmp/brain_dashboard_{vault_hash}.lock"
        self.vault_root = vault_root
        self.timeout = float(timeout)
        self.retry_interval = float(retry_interval)
        self.ttl_seconds = int(ttl_seconds)
        self.blocking = bool(blocking)
        self.acquired = False

    def _clean_stale_lock(self):
        if not os.path.exists(self.lock_file):
            return
        try:
            mtime = os.path.getmtime(self.lock_file)
            is_stale = (time.time() - mtime) > self.ttl_seconds
            if not is_stale:
                with open(self.lock_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                m = re.search(r'pid:\s*(\d+)', content)
                if m and not is_pid_alive(int(m.group(1))):
                    is_stale = True
            if is_stale:
                os.remove(self.lock_file)
        except Exception:
            pass

    def acquire(self, timeout: Optional[float] = None, retry_interval: Optional[float] = None, blocking: Optional[bool] = None) -> bool:
        t_out = self.timeout if timeout is None else float(timeout)
        r_int = self.retry_interval if retry_interval is None else float(retry_interval)
        blk = self.blocking if blocking is None else bool(blocking)

        # Re-entrancy within same process
        if self.lock_file in DashboardLock._process_locks and DashboardLock._process_locks[self.lock_file] > 0:
            DashboardLock._process_locks[self.lock_file] += 1
            self.acquired = True
            return True

        deadline = time.time() + t_out
        while True:
            try:
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"pid: {os.getpid()}\ntime: {datetime.datetime.now().isoformat()}\n".encode('utf-8'))
                os.close(fd)
                DashboardLock._process_locks[self.lock_file] = 1
                self.acquired = True
                return True
            except FileExistsError:
                self._clean_stale_lock()
                if not blk:
                    return False
                if time.time() >= deadline:
                    break
                time.sleep(min(r_int, max(0.01, deadline - time.time())))

        if blk:
            raise TimeoutError(f"Impossibile acquisire DashboardLock entro {t_out}s ({self.lock_file})")
        return False

    def release(self):
        if self.acquired:
            depth = DashboardLock._process_locks.get(self.lock_file, 1) - 1
            if depth <= 0:
                DashboardLock._process_locks.pop(self.lock_file, None)
                if os.path.exists(self.lock_file):
                    try:
                        os.remove(self.lock_file)
                    except Exception:
                        pass
            else:
                DashboardLock._process_locks[self.lock_file] = depth
            self.acquired = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


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
    """Classifies polymorphic input into youtube, web, pdf, file, or text."""
    s = source.strip()
    if YT_URL_REGEX.search(s): return "youtube"
    if WEB_URL_REGEX.match(s): return "web"
    if s.lower().endswith(".pdf") or (os.path.isfile(s) and s.lower().endswith(".pdf")):
        return "pdf"
    if os.path.isfile(s): return "file"
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
    """Checks if any keyword is present using regex word boundaries."""
    for kw in keywords:
        kw_clean = kw.lower().strip()
        if not kw_clean:
            continue
        if len(kw_clean) <= 3:
            if re.search(r'(?:\b|_)' + re.escape(kw_clean) + r'(?:\b|_)', text):
                return True
        else:
            if re.search(r'(?:\b|_)' + re.escape(kw_clean), text):
                return True
    return False


DIRECTORY_ROUTING_RULES: List[Tuple[str, List[str], List[str]]] = [
    # 1. Blog Studio
    (
        "05 - Blog",
        ["blog"],
        ["blog"],
    ),
    # 2. Finance Subdirectories
    # 2.1 Crypto
    (
        "02 - Atlas/Finance/Crypto",
        ["finance/crypto", "finance/blockchain", "tech/crypto", "tech/blockchain", "crypto", "blockchain", "bitcoin", "btc", "ethereum", "eth", "web3"],
        ["crypto", "criptovalut", "bitcoin", "btc", "ethereum", "eth", "blockchain", "web3", "defi", "nft", "token", "wallet", "smart contract", "altcoin", "binance"],
    ),
    # 2.2 Holdings & Tax
    (
        "02 - Atlas/Finance/Holdings & Tax",
        ["finance/tax", "finance/fisco", "finance/wealth", "finance/patrimonio", "finance/holdings", "tax", "fisco", "holdings"],
        ["fisco", "fiscale", "tasse", "irpef", "partita iva", "p.iva", "srl", "holding", "evasione", "elusione", "deduzion", "detrazion", "patrimonio", "quadro rw", "commercialista", "regime forfettario", "residenza fiscale"],
    ),
    # 2.3 Investments
    (
        "02 - Atlas/Finance/Investments",
        ["finance/investing", "finance/investments", "finance/stocks", "finance/etf", "finance/markets", "finance/trading", "investimenti", "etf", "trading"],
        ["investimenti", "investire", "borsa", "azioni", "etf", "fondi indicizzati", "obbligazioni", "compound interest", "interesse composto", "trading", "value investing", "s&p 500", "nasdaq", "rendimento", "portafoglio", "dividendi"],
    ),
    # 2.4 Economy & Macro
    (
        "02 - Atlas/Finance/Economy",
        ["finance/macro", "finance/economy", "finance/banks", "macroeconomia", "banche", "economia"],
        ["macroeconomia", "banche", "banca centrale", "bce", "federal reserve", "fed", "inflazione", "tassi di interesse", "debito pubblico", "pil", "recessione", "dazi", "geopolitica", "politica monetaria", "creazione del denaro"],
    ),
    # 2.5 General Finance Fallback
    (
        "02 - Atlas/Finance/Investments",
        ["finance"],
        ["finanza", "finance", "soldi", "money", "business"],
    ),
    # 3. Personal Growth & Health Subdirectories
    # 3.1 Gym & Health
    (
        "02 - Atlas/Personal Growth & Health/Gym & Health",
        ["health/fitness", "health/gym", "health/workout", "health/palestra", "mentality/fitness", "health/nutrition", "health/sleep", "health/biohacking", "health/health", "health", "palestra", "fitness", "gym", "workout", "salute", "nutrizione"],
        ["palestra", "workout", "allenamento", "ipertrofia", "bodybuilding", "calisthenics", "pesi", "squat", "panca piana", "stacco", "massa muscolare", "nutrizione", "dieta", "alimentazione", "salute", "sonno", "biohacking", "integratori", "fluoro", "dentifricio", "denti", "metabolismo", "calorie", "macronutrienti", "digiuno", "skincare"],
    ),
    # 3.2 Mentality & Mindset
    (
        "02 - Atlas/Personal Growth & Health/Mentality",
        ["mentality/habits", "mentality/productivity", "mentality/discipline", "mentality/focus", "mentality/produttivita", "mentality/philosophy", "mentality/mental-models", "mentality/stoicism", "mentality/growth", "mentality/psychology", "mentality/mindset", "mentality", "mindset", "produttivita", "abitudini", "focus", "filosofia", "stoicismo"],
        ["produttivita", "abitudini", "abitudine", "routine", "disciplina", "focus", "concentrazione", "time management", "gestione del tempo", "gtd", "second brain", "dopamina", "procrastinazione", "pomodoro", "back to focus", "distrazioni", "dipendenza neurocognitiva", "tempo di permanenza", "filosofia", "stoicismo", "modelli mentali", "modello mentale", "pensiero critico", "bias cognitivo", "decision making", "razionalita", "epistemologia", "socrate", "marco aurelio", "seneca", "fallacie", "mentalita", "mindset", "crescita personale", "resilienza", "autostima", "psicologia", "comunicazione", "public speaking", "relazioni", "persuasione", "parlare bene", "cancel culture"],
    ),
    # 3.3 General Personal Growth Fallback
    (
        "02 - Atlas/Personal Growth & Health/Mentality",
        ["mentality"],
        ["mentality", "crescita"],
    ),
    # 4. Education & Learning Subdirectories
    # 4.1 Learning
    (
        "02 - Atlas/Education & Learning/Learning",
        ["education/method", "education/learning", "education/study", "education/memory", "education/mnemonics", "education/school", "education/highschool", "apprendimento", "metodo-studio", "memoria", "scuola", "liceo"],
        ["metodo di studio", "apprendimento", "imparare", "feynman", "active recall", "spaced repetition", "ripetizione spaziata", "lettura veloce", "memorizzazione", "pacrar", "memoria", "mnemotecniche", "palazzo della memoria", "tecniche di memoria", "ricordare cio che leggi", "memorizzare", "leggere libri", "scuola", "liceo", "registro elettronico", "classeviva", "maturita", "professori", "interrogazione", "compiti", "bravo a scuola", "learning to learn"],
    ),
    # 4.2 University Sub-branches
    (
        "02 - Atlas/Education & Learning/University/Architettura & Sistemi",
        ["education/university/systems", "education/university/os"],
        ["architettura dei calcolatori", "sistemi operativi", "calcolatori elettronici", "assembly", "reti di calcolatori"],
    ),
    (
        "02 - Atlas/Education & Learning/University/Fondamenti di Informatica",
        ["education/university/cs", "education/university/programming", "education/university/fondamenti"],
        ["fondamenti di informatica", "programmazione c", "algoritmi e strutture dati"],
    ),
    (
        "02 - Atlas/Education & Learning/University/Matematica & Fisica",
        ["education/university/math", "education/university/physics", "education/math", "matematica", "fisica"],
        ["analisi matematica", "algebra lineare", "geometria", "fisica 1", "probabilita", "statistica", "calcolo numerico", "analisi 1", "analisi 2", "derivate", "integrali"],
    ),
    (
        "02 - Atlas/Education & Learning/University/Teoria dei Linguaggi",
        ["education/university/languages", "education/university/automata"],
        ["teoria dei linguaggi", "automi", "linguaggi formali", "compilatori", "grammatiche formali", "macchina di turing"],
    ),
    (
        "02 - Atlas/Education & Learning/University",
        ["education/university"],
        ["universita", "ingegneria informatica", "esame", "esami universitari", "cfu", "laurea", "sessione d'esami", "scegliere l'universita"],
    ),
    # 4.3 Courses
    (
        "02 - Atlas/Education & Learning/Courses",
        ["education/course", "education/courses", "education/cs50", "corso", "corsi"],
        ["corso stem", "corso ai", "cs50", "progetto enea", "progetto pilota airo", "corso python"],
    ),
    # 4.4 General Education Fallback
    (
        "02 - Atlas/Education & Learning/Learning",
        ["education"],
        ["education", "studio", "scuola", "universita"],
    ),
    # 5. Projects Subdirectories
    (
        "02 - Atlas/Projects/Active",
        ["projects/active", "project/active"],
        [],
    ),
    (
        "02 - Atlas/Projects/Archive",
        ["projects/archive", "project/archive"],
        [],
    ),
    (
        "02 - Atlas/Projects/Ideas & Sandbox",
        ["projects/ideas", "project/ideas", "projects/sandbox"],
        [],
    ),
    # 6. Tech & AI Subdirectories
    # 6.1 Agents & Automation
    (
        "02 - Atlas/Tech & AI/Agents & Automation",
        ["tech/agents", "tech/agent", "tech/automation", "tech/agenti", "agenti", "automazione"],
        ["agente ai", "agenti ai", "ai agent", "ai agents", "multi-agent", "crewai", "langchain", "autogen", "n8n", "automazione", "zapier", "workflow automat", "hermes agent"],
    ),
    # 6.2 Security
    (
        "02 - Atlas/Tech & AI/Security",
        ["tech/security", "tech/cybersecurity", "tech/hacking", "security", "cybersecurity", "hacking"],
        ["cybersecurity", "sicurezza informatica", "crittografia", "vulnerabilita", "malware", "exploit", "firewall", "pentesting", "penetration test", "oauth", "jwt", "xss", "csrf", "sql injection", "zero-day", "hacking", "ethical hacking", "reverse engineering", "buffer overflow", "ctf", "kali linux", "coinjoin"],
    ),
    # 6.3 Software Development
    (
        "02 - Atlas/Tech & AI/Software Development",
        ["tech/git", "tech/github", "tech/dev", "tech/software-engineering", "tech/semver", "tech/architecture", "tech/vibe-coding", "tech/vibecoding", "git", "github", "vibe-coding"],
        ["github", "git commit", "git push", "git rebase", "git branch", "pull request", "repository git", "gitflow", "vibe coding", "vibecoding", "sviluppo software", "software engineering", "semantic versioning", "semver", "versioning conventions", "design pattern", "clean code", "refactoring", "ci/cd", "continuous integration", "test unitari", "tdd", "agile", "scrum", "microservizi", "dependency hell", "major.minor.patch", "cursor", "submodule"],
    ),
    # 6.4 System & OS
    (
        "02 - Atlas/Tech & AI/System & OS",
        ["tech/os", "tech/linux", "tech/sysadmin", "tech/networks", "linux", "devops"],
        ["linux", "macos", "unix", "kernel", "terminale", "bash", "zsh", "file system", "tcp/ip", "dns", "server", "sysadmin", "ubuntu", "debian", "terminal setup", "situazione python"],
    ),
    # 6.5 Programming Generale & Coding con AI
    (
        "02 - Atlas/Tech & AI/Programming",
        ["tech/programming", "tech/code", "tech/python", "tech/js", "tech/ts", "tech/rust", "tech/golang", "tech/backend", "tech/frontend", "tech/database", "tech/sql", "tech/programming/ai", "programming", "coding"],
        ["python", "javascript", "typescript", "rust", "golang", "c++", "java", "database", "sql", "backend", "frontend", "api rest", "graphql", "docker", "kubernetes", "algoritmi", "strutture dati", "programmazione ai"],
    ),
    # 6.6 AI & Machine Learning
    (
        "02 - Atlas/Tech & AI/AI",
        ["tech/ai", "tech/llm", "tech/rag", "tech/ml", "tech/nlp", "tech/prompt", "ai", "llm", "prompt"],
        ["intelligenza artificiale", "ai", "llm", "large language model", "machine learning", "deep learning", "transformer", "neural network", "rag", "embeddings", "vision model", "nlp", "hugging face", "gpt", "claude", "gemini", "fine-tuning", "modelli linguistici", "notebooklm", "prompt engineering", "system prompt", "context window", "hardware ai"],
    ),
]


def classify_target_directory(title: str, tags: List[str], content: str = "", vault_root: Optional[str] = None) -> str:
    """Heuristically and semantically determines destination subfolder in Atlas or Blog based on declarative routing rules."""
    tags_lower = [str(t).lower().strip().lstrip('#') for t in tags if t]
    c = (title + " " + " ".join(tags_lower) + " " + content[:2500]).lower()

    for target_dir, rule_tags, rule_kws in DIRECTORY_ROUTING_RULES:
        if (rule_tags and _has_tag(tags_lower, rule_tags)) or (rule_kws and _has_keyword(c, rule_kws)):
            return target_dir

    # AI Assisted Classification Fallback (D-06)
    allowed_dirs = [
        "02 - Atlas/Finance/Crypto",
        "02 - Atlas/Finance/Holdings & Tax",
        "02 - Atlas/Finance/Investments",
        "02 - Atlas/Finance/Economy",
        "02 - Atlas/Personal Growth & Health/Gym & Health",
        "02 - Atlas/Personal Growth & Health/Mentality",
        "02 - Atlas/Education & Learning/Learning",
        "02 - Atlas/Education & Learning/University",
        "02 - Atlas/Education & Learning/Courses",
        "02 - Atlas/Projects/Active",
        "02 - Atlas/Projects/Archive",
        "02 - Atlas/Projects/Ideas & Sandbox",
        "02 - Atlas/Tech & AI/Agents & Automation",
        "02 - Atlas/Tech & AI/Security",
        "02 - Atlas/Tech & AI/Software Development",
        "02 - Atlas/Tech & AI/System & OS",
        "02 - Atlas/Tech & AI/Programming",
        "02 - Atlas/Tech & AI/AI",
        "05 - Blog",
    ]
    if os.environ.get("BRAIN_INGEST_NO_AI") == "1":
        return "02 - Atlas/Tech & AI/AI"

    home_bin = os.path.expanduser("~/.local/bin/agy")
    agy_cmd = shutil.which("agy") or (home_bin if (os.path.isfile(home_bin) and os.access(home_bin, os.X_OK)) else None)
    if not agy_cmd:
        return "02 - Atlas/Tech & AI/AI"

    dirs_list_str = "\n".join(f"- {d}" for d in allowed_dirs)
    prompt = f"""Classifica la seguente nota personale nella cartella di destinazione più appropriata.

TITOLO: {title}
CONTENUTO:
{content[:1000]}

CARTELLE AMMISSIBILI:
{dirs_list_str}

Rispondi UNICAMENTE con il percorso esatto di una delle cartelle sopra elencate, senza commenti, markdown o spiegazioni aggiuntive."""

    try:
        proc = subprocess.run(
            [agy_cmd, "--model", os.environ.get("BRAIN_AI_MODEL", DEFAULT_AI_MODEL), "--print", prompt],
            capture_output=True,
            text=True,
            timeout=10
        )
        if proc.returncode == 0:
            ans = proc.stdout.strip().strip('"').strip("'").strip('`')
            for d in allowed_dirs:
                if ans == d or ans.endswith(d):
                    return d
    except Exception:
        pass

    return "02 - Atlas/Tech & AI/AI"

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
    """Links only real existing note titles (max 2 per target), safely preserving code blocks, links, and URLs."""
    auditor = brain_health.VaultHealthAuditor(vault_root)
    all_titles = sorted(auditor.all_notes.keys(), key=lambda x: len(x), reverse=True)
    stopwords = {'home', 'daily', 'note', 'studio', 'guida', 'guide', 'indice', 'index',
                 'atlas', 'moc', 'blog', 'meta', 'tech', 'inbox', 'school', 'appunti', 'review'}
    protected_blocks = []
    def mask_block(m):
        protected_blocks.append(m.group(0))
        return f"__PROTECTED_BLOCK_{len(protected_blocks)-1}__"

    # 1. Mask fenced code blocks and inline code
    masked = re.sub(r'```[\s\S]*?```', mask_block, body_text)
    masked = re.sub(r'~~~[\s\S]*?~~~', mask_block, masked)
    masked = re.sub(r'`[^`\n]+`', mask_block, masked)

    # 2. Mask Anki flashcard callout blocks, Obsidian comments, and raw START...END blocks (ANKI-02, Pitfall 2)
    masked = re.sub(r'%%[\s\S]*?%%', mask_block, masked)
    masked = re.sub(r'^[ \t]*>[ \t]*\[![a-zA-Z0-9_-]+\]-?[ \t]*(?:Flashcard:[^\n]*)?\n(?:^[ \t]*>[ \t]*[^\n]*\n)*?^[ \t]*>[ \t]*END[ \t]*$', mask_block, masked, flags=re.MULTILINE)
    masked = re.sub(r'^[ \t]*(?:>[ \t]*)?START[ \t]*\n[\s\S]*?^[ \t]*(?:>[ \t]*)?END[ \t]*$', mask_block, masked, flags=re.MULTILINE)

    # 3. Mask Anki MathJax delimiters and standard display math
    masked = re.sub(r'\[\$\$\][\s\S]*?\[/\$\$\]', mask_block, masked)
    masked = re.sub(r'\[\$\][\s\S]*?\[/\$\]', mask_block, masked)
    masked = re.sub(r'\$\$[\s\S]*?\$\$', mask_block, masked)

    # 4. Mask existing wiki-links
    masked = re.sub(r'\[\[[^\]]+\]\]', mask_block, masked)

    # 5. Mask existing standard markdown links [text](url)
    masked = re.sub(r'\[[^\]]+\]\([^\)]+\)', mask_block, masked)

    # 6. Mask pure web URLs
    masked = re.sub(r'https?://[^\s\)]+', mask_block, masked)

    linked, inserted, cur_clean = masked, set(), current_title.lower().strip()

    for title in all_titles:
        t_low = title.lower().strip()
        if t_low == cur_clean or len(title) < 4 or t_low in stopwords:
            continue
        pat = re.compile(r'(?<![\w#])(' + re.escape(title) + r')(?![\w])', re.IGNORECASE)
        if pat.search(linked):
            linked = pat.sub(f"[[{title}]]", linked, count=2)
            inserted.add(f"[[{title}]]")

    for idx in range(len(protected_blocks) - 1, -1, -1):
        linked = linked.replace(f"__PROTECTED_BLOCK_{idx}__", protected_blocks[idx])
    return linked, sorted(list(inserted))

def sanitize_style_highlights(text: str) -> str:
    """Strips backticks from HTML <mark> and <font> tags."""
    return re.sub(r'`(<(?:mark|font)\b[^>]*>[\s\S]*?</(?:mark|font)>)`', r'\1', text)

def strip_ai_directives(text: str) -> str:
    """Removes user-to-AI inline instructions/comments (%% AI: ... %%, <!-- AI: ... -->, and callouts)."""
    # 1. Strip Obsidian comments: %% AI: ... %% or %% IA: ... %%
    cleaned = re.sub(r'%%\s*(?:AI|IA):[\s\S]*?%%', '', text, flags=re.IGNORECASE)
    # 2. Strip HTML comments: <!-- AI: ... --> or <!-- IA: ... -->
    cleaned = re.sub(r'<!--\s*(?:AI|IA):[\s\S]*?-->', '', cleaned, flags=re.IGNORECASE)
    # 3. Strip collapsible/standard callouts dedicated to AI instructions: > [!note]- AI: ... or > [!todo]- AI: ...
    cleaned = re.sub(r'^[ \t]*>[ \t]*\[!(?:note|ai|todo|tip|info)\]-?[ \t]*(?:AI|IA):?[^\n]*\n(?:^[ \t]*>[ \t]*[^\n]*\n*)*', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    # 4. Clean up any leftover multiple blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned

def resolve_inbox_dependencies(
    content: str,
    note_path: Optional[str] = None,
    vault_root: Optional[str] = None,
    course: Optional[str] = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """Resolves transclusions and links to local inbox/external files (Option B: Deep Ingestion).

    Extracts text from PDFs (via academic_helper) and Markdown notes/transcripts, archives
    binary attachments (PDFs, images) to 99 - Meta/Attachments/<Course>/ in Title Case,
    stages secondary Markdown notes to 03 - Inbox/Source/, updates embedded links,
    and aggregates extracted content for comprehensive AI conceptual elaboration.
    """
    root = brain_health.get_vault_root(vault_root)
    clean_course = None
    if course:
        clean_course = brain_health.clean_title_str(str(course))
    else:
        has_fm, fm_t, _, _ = brain_health.split_markdown_note(content)
        if has_fm:
            meta_temp = brain_health.safe_load_frontmatter(fm_t, brain_health.build_yaml_engine())
            if meta_temp.get('course'):
                clean_course = brain_health.clean_title_str(str(meta_temp['course']))

    extracted_refs: List[Tuple[str, str, bool]] = []
    for m in re.finditer(r'!\[\[(.*?)\]\]', content):
        extracted_refs.append((m.group(0), m.group(1).strip(), True))
    for m in re.finditer(r'(?<!!)\[\[(.*?)\]\]', content):
        extracted_refs.append((m.group(0), m.group(1).strip(), False))
    for m in re.finditer(r'!\[(.*?)\]\((.*?)\)', content):
        extracted_refs.append((m.group(0), m.group(2).strip(), True))
    for m in re.finditer(r'(?<!!)\[(.*?)\]\((.*?)\)', content):
        extracted_refs.append((m.group(0), m.group(2).strip(), False))
    for m in re.finditer(r'@\[([^\n\]]+)\]', content):
        extracted_refs.append((m.group(0), m.group(1).strip(), False))
    for m in re.finditer(r'(?:^|\s)@([^\s\]\)\'"]+)', content):
        extracted_refs.append((m.group(0).strip(), m.group(1).strip(), False))

    inbox_dir = os.path.join(root, "03 - Inbox")
    source_dir = os.path.join(inbox_dir, "Source")
    os.makedirs(source_dir, exist_ok=True)

    if clean_course:
        attachments_dir = os.path.join(root, "99 - Meta", "Attachments", clean_course)
    else:
        attachments_dir = os.path.join(root, "99 - Meta", "Attachments")
    os.makedirs(attachments_dir, exist_ok=True)

    enriched_content = content
    aggregated_sections: List[str] = []
    sources_meta: List[Dict[str, Any]] = []
    processed_paths: Set[str] = set()

    for full_match, raw_target, is_transclusion in extracted_refs:
        clean_target = raw_target.strip().strip('"').strip("'").strip('`')
        if clean_target.startswith('file://'):
            clean_target = clean_target[7:]
        clean_target = clean_target.split('|')[0].strip()
        clean_target = clean_target.split('#')[0].strip()
        if not clean_target:
            continue

        cand_path = None
        if os.path.isabs(clean_target) and os.path.exists(clean_target):
            cand_path = clean_target
        elif note_path and os.path.exists(os.path.join(os.path.dirname(note_path), clean_target)):
            cand_path = os.path.join(os.path.dirname(note_path), clean_target)
        elif os.path.exists(os.path.join(root, clean_target)):
            cand_path = os.path.join(root, clean_target)
        elif os.path.exists(os.path.join(inbox_dir, clean_target)):
            cand_path = os.path.join(inbox_dir, clean_target)
        elif os.path.exists(os.path.join(source_dir, clean_target)):
            cand_path = os.path.join(source_dir, clean_target)
        elif not os.path.splitext(clean_target)[1]:
            for try_p in [
                os.path.join(inbox_dir, f"{clean_target}.md"),
                os.path.join(source_dir, f"{clean_target}.md"),
                os.path.join(os.path.dirname(note_path), f"{clean_target}.md") if note_path else None,
                os.path.join(root, f"{clean_target}.md")
            ]:
                if try_p and os.path.exists(try_p):
                    cand_path = try_p
                    break

        if not cand_path and os.path.exists(inbox_dir):
            target_base = os.path.basename(clean_target).lower()
            for f in os.listdir(inbox_dir):
                if f.lower() == target_base or f.lower() == f"{target_base}.md":
                    cand_path = os.path.join(inbox_dir, f)
                    break

        if not cand_path or not os.path.isfile(cand_path):
            continue

        cand_abs = os.path.abspath(cand_path)
        if note_path and cand_abs == os.path.abspath(note_path):
            continue
        if cand_abs in processed_paths:
            continue

        rel_from_root = os.path.relpath(cand_abs, root)
        is_inbox = rel_from_root.startswith("03 - Inbox") or rel_from_root.startswith("03 - Inbox/")
        is_external = not cand_abs.startswith(os.path.abspath(root) + os.sep)

        if not (is_inbox or is_external):
            continue

        processed_paths.add(cand_abs)
        ext = os.path.splitext(cand_abs)[1].lower()

        if ext == ".pdf":
            clean_stem = brain_health.clean_title_str(Path(cand_abs).stem)
            extracted_pdf_text = ""
            archived_pdf_name = f"{clean_stem}.pdf"
            archived_pdf_path = os.path.join(attachments_dir, archived_pdf_name)

            try:
                import academic_helper
                pdf_data = academic_helper.extract_pdf_data(cand_abs, course=clean_course, vault_root=root)
                extracted_pdf_text = pdf_data.get('raw_text', '')
                archived_pdf_name = pdf_data.get('pdf_filename') or archived_pdf_name
                archived_pdf_path = pdf_data.get('permanent_pdf_path') or archived_pdf_path
            except Exception:
                try:
                    import academic_helper
                    archived_pdf_name, archived_pdf_path = academic_helper.archive_pdf_attachment(cand_abs, attachments_dir, clean_stem)
                except Exception:
                    shutil.copy2(cand_abs, archived_pdf_path)
                extracted_pdf_text = f"<!-- PDF allegato: [[{archived_pdf_name}]] (Appunti manoscritti / scansione) -->"

            if is_inbox and os.path.exists(cand_abs) and os.path.abspath(cand_abs) != os.path.abspath(archived_pdf_path):
                try:
                    os.remove(cand_abs)
                except Exception:
                    pass

            new_ref = f"![[{archived_pdf_name}]]" if is_transclusion else f"[[{archived_pdf_name}]]"
            enriched_content = enriched_content.replace(full_match, new_ref)

            aggregated_sections.append(
                f"--- Inizio Contenuto da PDF: [[{archived_pdf_name}]] ---\n"
                f"[FONTE DI SUPPORTO: Dispense / Slide PDF — Materiale didattico ausiliario per formalismo matematico, formule LaTeX, schemi e citazioni di pagina: non discostarsi dalla lezione]\n"
                f"{extracted_pdf_text}\n"
                f"--- Fine Contenuto da PDF: [[{archived_pdf_name}]] ---"
            )
            sources_meta.append({
                'name': archived_pdf_name,
                'wikilink': f"[[{archived_pdf_name}]]",
                'path': archived_pdf_path,
                'type': 'pdf',
                'original_path': cand_abs
            })

        elif ext in ('.png', '.jpg', '.jpeg', '.webp'):
            raw_stem = Path(cand_abs).stem
            clean_stem = brain_health.clean_title_str(raw_stem)
            if raw_stem.lower().startswith("cleanshot") or "screenshot" in raw_stem.lower():
                if clean_course:
                    clean_stem = f"Figura - {clean_course} - {clean_stem}"
                else:
                    clean_stem = f"Figura - {clean_stem}"

            target_img_name = f"{clean_stem}{ext}"
            target_img_path = os.path.join(attachments_dir, target_img_name)

            v = 2
            while os.path.exists(target_img_path) and os.path.abspath(target_img_path) != cand_abs:
                try:
                    with open(cand_abs, 'rb') as sf, open(target_img_path, 'rb') as tf:
                        if hashlib.sha256(sf.read()).hexdigest() == hashlib.sha256(tf.read()).hexdigest():
                            break
                except Exception:
                    pass
                target_img_name = f"{clean_stem} (v{v}){ext}"
                target_img_path = os.path.join(attachments_dir, target_img_name)
                v += 1

            if is_inbox:
                shutil.move(cand_abs, target_img_path)
            else:
                shutil.copy2(cand_abs, target_img_path)

            new_ref = f"![[{target_img_name}]]"
            enriched_content = enriched_content.replace(full_match, new_ref)

            sources_meta.append({
                'name': target_img_name,
                'wikilink': f"[[{target_img_name}]]",
                'path': target_img_path,
                'type': 'image',
                'original_path': cand_abs
            })

        elif ext in ('.md', ''):
            try:
                with open(cand_abs, 'r', encoding='utf-8', errors='ignore') as mf:
                    sub_text = mf.read()
            except Exception:
                sub_text = ""

            txt_head = sub_text[:1500].lower()
            is_transcript = any(k in txt_head or k in clean_target.lower() for k in ('trascrizion', 'transcript', 'whisper', 'audio')) or bool(re.search(r'\[\d{2}:\d{2}', txt_head))
            kind = 'transcript' if is_transcript else 'note'

            file_name = os.path.basename(cand_abs)
            if not file_name.endswith('.md'):
                file_name += '.md'
            staged_path = os.path.join(source_dir, file_name)

            if is_inbox and os.path.abspath(cand_abs) != os.path.abspath(staged_path):
                if os.path.exists(staged_path):
                    try:
                        os.remove(staged_path)
                    except Exception:
                        pass
                shutil.move(cand_abs, staged_path)
            elif not is_inbox:
                shutil.copy2(cand_abs, staged_path)

            sub_stem = brain_health.clean_title_str(Path(cand_abs).stem)
            if is_transcript:
                aggregated_sections.append(
                    f"--- Inizio Contenuto da [[{sub_stem}]] ---\n"
                    f"[FONTE PRIMARIA: Trascrizione Audio Lezione — Asse narrativo portante e perimetro concettuale di quanto spiegato a lezione: ricalcare fedelmente]\n"
                    f"{sub_text.strip()}\n"
                    f"--- Fine Contenuto da [[{sub_stem}]] ---"
                )
            else:
                aggregated_sections.append(
                    f"--- Inizio Contenuto da [[{sub_stem}]] ---\n"
                    f"[FONTE DI SUPPORTO: Appunti Ausiliari — Materiale di supporto integrativo: utilizzare per chiarimenti senza allargare lo scope]\n"
                    f"{sub_text.strip()}\n"
                    f"--- Fine Contenuto da [[{sub_stem}]] ---"
                )

            sources_meta.append({
                'name': sub_stem,
                'wikilink': f"[[{sub_stem}]]",
                'path': staged_path,
                'type': 'note',
                'kind': kind,
                'original_path': cand_abs
            })

    if aggregated_sections:
        enriched_content = (
            f"=== NOTA ORIGINALE / CATTURA PRIMARIA DELL'UTENTE ===\n"
            f"[Asse portante: non discostarsi troppo da questi appunti e dalla trascrizione]\n"
            f"{enriched_content.strip()}\n"
            f"=== FINE NOTA ORIGINALE ===\n\n"
            + "\n\n".join(aggregated_sections) + "\n"
        )

    return enriched_content, sources_meta

def format_structured_note(title: str, raw_content: str, depth: str = "approfondimento", source_type: str = "text", source_url: str = "original") -> str:
    """Formats note body with clean headings (no emoji, no ## Collegamenti) and style guide highlights."""
    c_title = brain_health.clean_title_str(title)
    is_deep = depth in ("deep", "approfondimento")
    cleaned_source = strip_ai_directives(raw_content)
    lead = cleaned_source.strip()[:250].replace('\n', ' ')
    lines = [
        f"# {c_title}\n",
        "## Sintesi Esecutiva\n",
        f'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>{c_title}</b></font></mark>: {lead}...\n'
    ]
    if is_deep:
        lines.extend([
            f"## Quadro Concettuale e Fondamenti\n\n{cleaned_source.strip()}\n",
            f"## Meccanica e Dettaglio Operativo\n\nAnalisi approfondita dei <mark style=\"background:rgba(181, 113, 255, 0.36)\"><font color=\"#9a54c1\"><b>principi operativi</b></font></mark> di {c_title}.\n",
            "## Analisi Critica e Casi Applicativi\n\nValutazione di limiti, compromessi architetturali e contesti d'uso.\n"
        ])
    else:
        lines.extend([
            f"## Concetti Chiave e Takeaway\n\n- <mark style=\"background:rgba(181, 113, 255, 0.36)\"><font color=\"#9a54c1\"><b>Punto Chiave 1</b></font></mark>: {lead[:120]}\n",
            f"## Quadro Concettuale\n\n{cleaned_source.strip()}\n"
        ])
    return "\n".join(lines)

def enrich_draft_with_ai(vault_root: str, title: str, source_content: str, depth: str = "approfondimento",
                         source_type: str = "text", source_url: str = "original",
                         agy_path: Optional[str] = None, timeout: int = 90,
                         ai_model: Optional[str] = None,
                         metacognitive_constraints: Optional[str] = None,
                         enable_anki: bool = False,
                         course_name: Optional[str] = None) -> tuple[str, str]:
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

    meta_section = f"\n{metacognitive_constraints.strip()}\n" if metacognitive_constraints and metacognitive_constraints.strip() else ""

    anki_rules = ""
    if enable_anki:
        clean_deck = course_name.strip() if course_name else "Generale"
        anki_rules = f"""
8. GENERAZIONE FLASHCARD ANKI CONTESTUALI (CONFORMI A DOC ANKI & OBSIDIAN-TO-ANKI):
   - Genera flashcard contestuali atomiche collocate IMMEDIATAMENTE A VALLE di ciascun concetto cardine evidenziato in giallo (<mark>), definizione formale, assioma, proprietà o teorema STEM ad ALTA DENSITÀ SISTEMATICA (copertura capillare di ogni concetto chiave per l'active recall, senza alcun limite restrittivo di 5-10 card per lezione).
   - Struttura OBBLIGATORIA: La prima riga è il callout collassabile '> [!tip]- Flashcard: [Nome Concetto]', seguito IMMEDIATAMENTE A CAPO (SENZA '>') dall'intero blocco Anki racchiuso tra delimitatori di commento Obsidian '%%':
     > [!tip]- Flashcard: [Nome Concetto]
     %%
     TARGET DECK: University::{clean_deck}
     START
     [Basic|Cloze]
     [Front:|Text:] ...
     [Back:|Extra:] ...
     Tags: education/university tech/programming
     END
     %%
   - REGOLA CRITICA INDENTAZIONE: NON anteporre MAI il carattere '>' alle righe interne del blocco di commento Anki (%%, TARGET DECK, START, Basic/Cloze, Front/Text, Back/Extra, Tags, END, %%). Solo la primissima riga del callout ha '>'. Tutte le altre righe devono iniziare a colonna 0 senza '>'.
   - MODELLI E CAMPI SUPPORTATI (STANDARD UFFICIALE ANKI):
     * Modello 'Basic': campi 'Front:' (domanda di ragionamento o principio primo) e 'Back:' (risposta concettuale esaustiva).
     * Modello 'Cloze': campo 'Text:' contenente le cancellazioni {{{{c1::...}}}}, {{{{c2::...}}}} e campo opzionale 'Extra:' per note di contesto.
    - REGOLE TASSATIVE PER FORMULE MATEMATICHE E CLOZE (DOC UFFICIALE ANKI):
     a) Derivate in formule matematiche: USARE SEMPRE la notazione LaTeX standard con ^\\prime (es. $f^\\prime(\\xi)$, $f^{{\\prime\\prime}}(x)$, $s^\\prime(t)$). È SEVERAMENTE VIETATO usare l'apostrofo $f'(x)$, poiché il converter HTML del plugin lo codifica in entità HTML che generano errori di sintassi e tag orfani in Anki.
     b) Notazione Cloze: USARE SEMPRE il doppio due punti {{{{c1::risposta}}}}. Non usare MAI il singolo due punti {{{{c1:risposta}}}}.
     c) Delimitatori matematici in Cloze: SE il contenuto della cancellazione contiene comandi o simboli matematici LaTeX (es. \\forall, \\exists, \\lor, \\land, \\neg, \\complement, \\cup, \\cap), DEVE ESSERE RIGOROSAMENTE RACCHIUSO TRA DELIMITATORI $...$ ALL'INTERNO DELLA CLOZE (es. {{{{c1::$(\\neg P) \\lor (\\neg Q)$}}}} o {{{{c1::$\\exists x : \\neg P(x)$}}}}). Non lasciare MAI comandi LaTeX "nudi" senza '$' dentro {{{{c1::...}}}}, altrimenti il plugin non li converte in MathJax e Anki mostra il codice LaTeX testuale anziché la formula renderizzata.
     d) Testo ordinario in Cloze: usa {{{{c1::parola normale}}}} SENZA delimitatori matematici ($). Non racchiudere mai testo in prosa dentro $...$.
     e) Valori assoluti e pipe: usa \\vert anziché | nelle formule (es. $\\vert x\\vert$).
     f) Spaziatura graffe nidificate: all'interno delle formule TeX nelle cloze, evitare doppie graffe consecutive '}}}}' senza spazio (usare '{{ {{' o '\\left\\{{ ... \\right\\}}') per non confondere il parser delle cloze di Anki.
   - Figure didattiche consentite SOLO in Back/Extra con ![[Figura - ...png]]. Zero diagrammi Mermaid nelle card.
   - NON generare mai commenti <!--ID: -->: gli ID vengono assegnati esclusivamente dal plugin Anki al momento del sync.
"""

    # Dynamic content budgeting: avoid macOS ARG_MAX limits while preserving full document fidelity
    # Gemini context window is 1M+ tokens; macOS ARG_MAX limit is ~1MB (~1,000,000 bytes).
    # 700,000 characters safely accommodates full textbooks up to 300+ pages without cutting off early chapters.
    MAX_SOURCE_CHARS = 700_000
    if len(source_content) <= MAX_SOURCE_CHARS:
        trimmed_content = source_content
    else:
        half = (MAX_SOURCE_CHARS - 1000) // 2
        trimmed_content = (
            f"{source_content[:half]}\n\n"
            f"[... OMISSIONE INTERMEDIA: Documento esteso ({len(source_content)} caratteri). "
            f"Campionate sezioni iniziali e finali per preservare la completezza del corso ...]\n\n"
            f"{source_content[-half:]}"
        )

    prompt = f"""Sei il motore di elaborazione della conoscenza per un Second Brain PKM in Obsidian.
Il tuo compito è rielaborare il contenuto sorgente in una nota concettuale permanente di altissima qualità letteraria e tecnica per: "{c_title}".

CONTENUTO SORGENTE:
{trimmed_content}

{depth_instruction}
{meta_section}
REGOLE CRITICHE DI CONTENUTO E STILE (TASSONOMIA DIDATTICA ADC & STYLE GUIDE):
1. GERARCHIA DELLE FONTI, FEDELTÀ ALLA LEZIONE, SEQUENZA LOGICO-TEMPORALE E DIGRESSIONI DEL DOCENTE (TAX-01, D-06):
   - FEDELTÀ ASSOLUTA ALLA NOTA ORIGINALE E ALLA TRASCRIZIONE (FONTI PRIMARIE): La nota originale dell'utente e la trascrizione audio della lezione costituiscono la FONTE PRIMARIA, l'asse portante narrativo e il perimetro concettuale invalicabile. La nota finale NON DEVE MAI discostarsi troppo da quanto effettivamente spiegato, argomentato ed esposto dal docente a lezione o riportato negli appunti originali.
   - RUOLO RIGOROSAMENTE DI SUPPORTO DI DISPENSE, SLIDE E ALTRI APPUNTI (FONTI DI SUPPORTO): Le dispense del corso, le slide PDF e gli eventuali altri appunti hanno uno scopo puramente AUSILIARIO E DI SUPPORTO. Servono per formalizzare le definizioni, recuperare l'esatta notazione matematica LaTeX per formule menzionate o abbozzate a voce, chiarire passaggi algebrici o teoremi, aggiungere richiami precisi alle slide (\\[[[file.pdf#page=N|Slide N]]]) e arricchire con tabelle o figure pertinenti.
   - DIVIETO ASSOLUTO DI DIVAGAZIONI O IPER-ESTENSIONI ENCICLOPEDICHE: Non espandere mai la trattazione a capitoli, lemmi o interi argomenti presenti nelle dispense o nelle slide che NON siano stati affrontati o richiamati a lezione. I materiali di supporto non devono MAI stravolgere la sequenza della lezione né trasformare la nota in un compendio enciclopedico del libro di testo estraneo a quanto svolto dal docente.
   - SEQUENZA LOGICO-TEMPORALE DEL DOCENTE: Ricalca fedelmente la successione logico-temporale della spiegazione senza omettere passaggi concettuali. Nessun template monolitico o sezione generica fissa/vuota: l'articolazione delle sezioni H2 e H3 deve scaturire spontaneamente dall'ordine reale di esposizione dei contenuti.
   - DIVIETO ASSOLUTO DI EMOJI NEI TITOLI: I titoli H1, H2, H3 devono contenere SOLO testo pulito (es. '## Sintesi Esecutiva', '## Analisi Nodale' e MAI '## 🎯 Sintesi').
   - INCAPSULAMENTO DELLE DIGRESSIONI: Quando il docente introduce aneddoti, divagazioni storiche, commenti extra-curriculari o aneddoti personali, NON creare titoli H3/H4 spuri e non inquinare la tavola dei contenuti (TOC/Outline). Incapsula invece la divagazione in un callout collassabile dedicato:
     > [!quote]- Divagazione del Docente: [Breve Oggetto della Divagazione]
     > [Trascrizione o sintesi della divagazione]
   - NESSUNA SEZIONE COLLEGAMENTI SEPARATA: Non inserire mai sezioni come '## Collegamenti', '## Note Correlate' o '## Vedi anche'. I collegamenti semantici vengono assorbiti organicamente nel testo.

2. FORMULARIO STEM VINCOLATO E FORMALISMO MATEMATICO (TAX-02, D-04, D-05, D-08, D-09):
   - Adotta un approccio ibrido per formule e passaggi matematici:
     a) Formule di passaggio, passaggi algebrici e calcoli intermedi: utilizza blocchi display MathJax standard $$...$$ o inline $...$.
     b) Teoremi, leggi fisiche, principi e formule cardine della materia: racchiudili in un callout dedicato (> [!example] Teorema / Legge: [Nome] oppure > [!info] Principio / Definizione: [Nome]).
   - OGNI callout di teorema o formula cardine DEVE obbligatoriamente contenere questi 5 elementi strutturati:
     1. Espressione display LaTeX $$...$$ centrale
     2. - **Ipotesi:** (assunzioni necessarie e condizioni a monte)
     3. - **Condizioni di validità:** (limiti operativi, regimi fisici o vincoli di applicabilità)
     4. - **Significato dei simboli:** (elenco di ogni parametro con la relativa unità di misura SI, es. $[\\text{{V}}]$, $[\\Omega]$, $[\\text{{A}}]$, $[\\text{{m/s}}^2]$)
     5. - **Esempio operativo:** (caso applicativo pratico, calcolo d'esempio o note operative)
   - DIVIETO DI BACKTICK PER FORMULE: Non racchiudere MAI le formule LaTeX tra blocchi di codice markdown (```latex o ```). Usa solo la sintassi naturale MathJax ($...$ e $$...$$) per consentire il rendering nativo di Obsidian. Non effettuare conversioni premature per Anki (demandate a fasi successive).

3. EVIDENZIAZIONI CROMATICHE E ARRICCHIMENTO VISIVO (TAX-03, D-01, D-02, D-03):
   - EVIDENZIAZIONI OBBLIGATORIE SU OGNI NOTA:
     - Giallo (parole chiave assolute, principi primi, concetti cardine):
       <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>concetto cardine</b></font></mark>
     - Viola (concetti secondari, nomi propri, definizioni derivate):
       <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>concetto secondario</b></font></mark>
     - REGOLA CRITICA: Non racchiudere MAI i tag HTML <mark> o <font> tra backtick markdown (`<mark...>` ❌)!
   - PALETTE VISIVA COMPLETA: Impiega con priorità callout semantici e dinamici (> [!tip], > [!important], > [!warning], > [!note], > [!example], > [!summary]), checkbox avanzate da Style Guide (- [!], - [i], - [*], - [?], - [/], ecc.) e tabelle comparative in Markdown standard (zero tabelle HTML).
   - DIAGRAMMI MERMAID CONTESTUALI (NON OBBLIGATORI): Non inserire obbligatoriamente diagrammi Mermaid in ogni nota. Usali solo a discrezione in presenza di reali catene causali complesse, derivazioni logiche a stadi o flussi di processi che beneficiano concretamente di visualizzazione grafica. Altrimenti, prediligi callout dinamici, elenchi con checkbox personalizzate o tabelle.
   - REGOLE MERMAID RIGOROSE: Tutte le etichette dei nodi DEVONO essere rigorosamente racchiuse tra doppi apici (es. A["Testo del Nodo (con dettagli)"] --> B["Secondo Nodo"]). Non inserire MAI tag HTML all'interno dei nodi Mermaid.

4. FILTRO ANTI-SLOP E ANTI-SPONSOR:
   - Elimina categoricamente sponsor commerciali (es. corsi online, piattaforme cloud, VPN, promozioni), saluti, formule di rito, aneddoti irrilevanti e frasi riempitive.
   - Distilla solo principi primi, definizioni rigorose, tesi argomentate, metodologie applicative e limiti critici.

5. LINGUA E SINTESI FINALE:
   - Scrivi rigorosamente in italiano accademico, chiaro e professionale.
   - NON includere il frontmatter YAML (sarà generato dal sistema).
   - Inizia sempre con il titolo H1 esatto della nota: # {c_title}
   - Alla fine assoluta della risposta, inserisci il marcatore esatto '---SUMMARY---' seguito da una singola frase densa di significato (120-180 caratteri, max 200) per il recupero sub-secondo.

6. SLIDE ACCADEMICHE, DOCUMENTI PDF E ASSET VISIVI (PDF-02, PDF-03, D-01, D-03, D-05, D-16):
   - RUOLO DI SUPPORTO E ANCORAGGIO: Le slide PDF e le dispense sono materiali di supporto didattico per ancorare e chiarire i punti toccati a lezione, non per sostituire o stravolgere la narrazione del docente.
   - TRATTAZIONE CONTINUA E NARRATIVA: Elabora il contenuto come flusso continuo unificato, evitando categoricamente separatori rigidi '### Slide N' o '### Diapositiva N'.
   - CITAZIONI INLINE A PAGINE REALI: Preserva e posiziona accuratamente i richiami di pagina inline nella forma con escape \\[[[nome.pdf#page=N|N]]] o \\[[[nome.pdf#page=N|Slide N]]] a valle dei concetti e dei teoremi corrispondenti spiegati a lezione.
   - DIVIETO ASSOLUTO DI CITAZIONE DELLE TRASCRIZIONI AUDIO: Non citare o linkare MAI le trascrizioni audio grezze nel testo o nell'intestazione; servono unicamente come input di rielaborazione per l'AI. Cita solo materiali accademici di consultazione diretta (slide PDF ufficiali, paper scientifici, libri di testo, articoli).
   - DENSITÀ CALIBRATA DEI RICHIAMI: Posiziona i link alle slide a livello di macro-argomento o per chiarire passaggi sintetici/astratti ed evitare fraintendimenti, evitando la saturazione frase per frase.
   - DIVIETO ASSOLUTO DI DIAGRAMMI SIMBOLICI ASCII/UNICODE: Non generare MAI blocchi di codice monospazio o testo con box-drawing ('┌┐└┘', '│', '──►'), poiché non renderizzano in modo coerente tra mobile e desktop. Se sono presenti schemi grafici nelle slide, incorpora direttamente l'immagine della slide (![[Schema - ... .png]]) oppure struttura i dati con tabelle Markdown native standard e callout semantici.
   - REGOLA ANTI-ALLUCINAZIONE PAGINE: I richiami DEVONO riflettere le pagine REALI del corpo del documento in cui il singolo concetto o teorema viene effettivamente spiegato. NON associare mai le pagine dell'indice (TOC), prefazione o frontespizio (es. pag 1-3) ad argomenti e capitoli trattati nel testo principale (es. pag 8, 30, 108, 206).
   - RIALLINEAMENTO CODICE E TABELLE: Riorganizza pseudocodice, frammenti di codice e tabelle frammentate in blocchi Markdown sintatticamente evidenziati o tabelle comparative chiare.
   - EMBEDDING FIGURE DISCREZIONALE: Se nel testo o nel contesto sono presenti figure estratte (![[Figura - ...]] o ![[Schema - ...]]), incorporale solo se apportano reale valore concettuale (diagrammi, grafi, schemi a blocchi), posizionandole direttamente a valle del rispettivo concetto cardine. Ometti loghi ateneo o grafiche decorative.

7. DIRETTIVE OPERATIVE UTENTE E META-ISTRUZIONI INLINE (%% AI: ... %%):
   - Nel testo sorgente possono essere presenti istruzioni dirette dell'utente per te, racchiuse nella sintassi nativa di commento Obsidian '%% AI: <istruzione> %%' (o equivalenti commenti HTML '<!-- AI: <istruzione> -->' o callout '> [!note]- AI: ...').
   - Esegui queste direttive come COMANDI OPERATIVI PRIORITARI ASSOLUTI (es. richieste di ridimensionamento o posizionamento immagini, focus su argomenti specifici, inserimento di formule, schemi o tabelle mirate).
   - REGOLA TASSATIVA DI PULIZIA: Rimuovi ed elimina completamente qualsiasi commento o marcatore di direttiva ('%% AI: ... %%', '<!-- AI: ... -->', callout di istruzione) dal corpo finale della nota permanente. La nota finale deve contenere unicamente il testo rielaborato pulito, senza alcuna traccia dei comandi ricevuti.
{anki_rules}"""

    home_bin = str(Path.home() / ".local" / "bin" / "agy")
    if agy_path and os.path.exists(agy_path):
        agy_cmd = agy_path
    else:
        agy_cmd = shutil.which("agy") or (home_bin if os.path.exists(home_bin) else "agy")
    env = os.environ.copy()
    home_dir = str(Path.home())
    env['PATH'] = f"{home_dir}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{env.get('PATH', '')}"
    env['PYTHONUNBUFFERED'] = '1'

    try:
        model_to_use = ai_model or os.environ.get("BRAIN_AI_MODEL", DEFAULT_AI_MODEL)
        effective_timeout = max(timeout, min(300, 90 + int(len(trimmed_content) / 3000)))
        proc = subprocess.run(
            [agy_cmd, "--model", model_to_use, "--dangerously-skip-permissions", "--disable-slash-commands", f"--print={prompt}"],
            capture_output=True,
            text=True,
            timeout=effective_timeout,
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

            # Strip any leaked AI inline directives or comments
            cleaned_body = strip_ai_directives(cleaned_body)

            # Automatically sanitize and validate any generated Anki flashcards (Anki Official Doc & Plugin Compliance)
            if "TARGET DECK:" in cleaned_body or enable_anki:
                cleaned_body = anki_helper.sanitize_all_flashcards(cleaned_body)

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


def get_watcher_pid_file(vault_root: str) -> str:
    """Dynamically resolves watcher daemon PID file following precedence chain: $PID_FILE -> vault hash -> legacy."""
    env_pid = os.environ.get('PID_FILE')
    if env_pid and env_pid.strip():
        return env_pid.strip()

    shasum_hash = hashlib.sha1(vault_root.encode('utf-8')).hexdigest()[:8]
    md5_hash = hashlib.md5(vault_root.encode('utf-8')).hexdigest()[:8]
    full_md5 = hashlib.md5(vault_root.encode('utf-8')).hexdigest()

    candidates = [
        f"/tmp/brain_watcher_{shasum_hash}.pid",
        f"/tmp/brain_watcher_{md5_hash}.pid",
        f"/tmp/brain_watcher_{full_md5}.pid",
        "/tmp/brain_watcher.pid"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]


def trigger_panic_abort(vault_root: str, pid_file: Optional[str] = None) -> int:
    """Terminates all running ingestion processes, cleans locks, resets ready notes, and clears In Elaborazione."""
    aborted_pids = set()
    my_pid = os.getpid()

    # 1. Identify watcher PID if running to ensure it is NEVER killed (D-01, D-02, D-04)
    watcher_pid = None
    target_pid_file = pid_file or get_watcher_pid_file(vault_root)
    if target_pid_file and os.path.exists(target_pid_file):
        try:
            with open(target_pid_file, "r", encoding="utf-8") as f:
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
                if ("brain_ingest.py" in cmd or "youtube_helper.py" in cmd or "yt-dlp" in cmd or "ffmpeg" in cmd) and "watch.sh" not in cmd and "--panic" not in cmd and "test_brain_ingest" not in cmd and "unittest" not in cmd:
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

    # 7. Clean up all interrupted drafts and partial files in 03 - Inbox/Draft/ (D-03)
    if os.path.exists(draft_dir):
        for f in os.listdir(draft_dir):
            if f.endswith(".md") and not f.startswith("."):
                dfp = os.path.join(draft_dir, f)
                try:
                    meta = {}
                    if os.path.exists(dfp):
                        with open(dfp, "r", encoding="utf-8", errors="ignore") as df:
                            content = df.read()
                        has_fm, fm_t, _, bdy = brain_health.split_markdown_note(content)
                        if has_fm:
                            meta = brain_health.safe_load_frontmatter(fm_t, brain_health.build_yaml_engine()) or {}
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
                    if os.path.exists(dfp):
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


def _update_review_dashboard_unlocked(vault_root: str, in_progress: Optional[str] = None,
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
            n = brain_health.clean_title_str(m.group('name').split('|')[0].strip())
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


def update_review_dashboard(vault_root: str, in_progress: Optional[str] = None,
                            phase: Optional[str] = None,
                            add_error: Optional[Tuple[str, str]] = None,
                            finish_in_progress: Optional[str] = None,
                            replace_in_progress: Optional[str] = None):
    """Synchronizes 03 - Inbox/Review Dashboard.md in static Markdown across 4 sections under DashboardLock (D-07, D-08)."""
    try:
        with DashboardLock(vault_root, timeout=10.0, retry_interval=0.2):
            return _update_review_dashboard_unlocked(
                vault_root, in_progress=in_progress, phase=phase,
                add_error=add_error, finish_in_progress=finish_in_progress,
                replace_in_progress=replace_in_progress
            )
    except TimeoutError as e:
        logging.warning("Impossibile acquisire DashboardLock entro il timeout. Operazione saltata: %s", e)
        return



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
    if meta.get('course'):
        clean_course = brain_health.clean_title_str(str(meta['course']))
        breadcrumb = f"[[Home MOC|Home]] / [[University|University MOC]] / [[{clean_course} MOC]] / [[{clean_title}]]"
    else:
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


def _handle_panic_action(vault_root: str) -> bool:
    """Executes emergency abort by unchecking all dashboard boxes and moving active items to Panic folder."""
    trigger_panic_abort(vault_root)
    return True


def _handle_error_item(vault_root: str, src_target: str, status: str) -> Tuple[bool, Optional[str]]:
    """Handles retrying or dismissing an error line from Review Dashboard."""
    if status in ('x', 'X'):
        try:
            matching_raw_file = None
            candidate_paths = [
                os.path.join(vault_root, "03 - Inbox", src_target),
                os.path.join(vault_root, "03 - Inbox", f"{src_target}.md"),
                os.path.join(vault_root, "03 - Inbox", "Source", src_target),
                os.path.join(vault_root, "03 - Inbox", "Source", f"{src_target}.md"),
            ]
            for cp in candidate_paths:
                if os.path.isfile(cp):
                    matching_raw_file = cp
                    break

            if not matching_raw_file:
                for s_rel in ("03 - Inbox", os.path.join("03 - Inbox", "Source")):
                    s_dir = os.path.join(vault_root, s_rel)
                    if os.path.exists(s_dir):
                        for ib_f in os.listdir(s_dir):
                            if not ib_f.endswith('.md') or ib_f.startswith('.') or ib_f in ("Review Dashboard.md", "Draft", "Source"):
                                continue
                            ib_fp = os.path.join(s_dir, ib_f)
                            if not os.path.isfile(ib_fp):
                                continue
                            try:
                                with open(ib_fp, 'r', encoding='utf-8', errors='ignore') as rf:
                                    rfc = rf.read()
                                _, rfm_t, _, _ = brain_health.split_markdown_note(rfc)
                                rmeta = brain_health.safe_load_frontmatter(rfm_t, brain_health.build_yaml_engine())
                                if rmeta.get('video_url') == src_target or rmeta.get('source') == src_target:
                                    matching_raw_file = ib_fp
                                    break
                            except Exception:
                                pass
                        if matching_raw_file:
                            break

            if matching_raw_file:
                with open(matching_raw_file, 'r', encoding='utf-8', errors='ignore') as rf:
                    rfc = rf.read()
                _, rfm_t, _, rbdy = brain_health.split_markdown_note(rfc)
                rfm_fixed = re.sub(r'ready:\s*(false|"false"|\'false\'|0)', 'ready: true', rfm_t, flags=re.IGNORECASE)
                if 'ready:' not in rfm_fixed:
                    rfm_fixed += "\nready: true"
                with open(matching_raw_file, 'w', encoding='utf-8') as rf:
                    rf.write(f"---\n{rfm_fixed.strip()}\n---\n\n{rbdy.strip()}\n")
                process_inbox_raw_notes(vault_root)
            else:
                ingest_source(src_target, vault_root=vault_root, force=True)

            append_inbox_history(vault_root, "RETRY_SUCCESS", src_target, "03 - Inbox/Draft")
            return True, None
        except Exception as e:
            append_inbox_history(vault_root, "RETRY_FAILED", src_target, str(e))
            return False, str(e)

    elif status == '-':
        candidate_paths = [
            os.path.join(vault_root, "03 - Inbox", src_target),
            os.path.join(vault_root, "03 - Inbox", f"{src_target}.md"),
            os.path.join(vault_root, "03 - Inbox", "Source", src_target),
            os.path.join(vault_root, "03 - Inbox", "Source", f"{src_target}.md"),
        ]
        deleted = False
        for cp in candidate_paths:
            if os.path.isfile(cp):
                try:
                    os.remove(cp)
                    deleted = True
                except Exception:
                    pass
        if not deleted:
            for s_rel in ("03 - Inbox", os.path.join("03 - Inbox", "Source")):
                s_dir = os.path.join(vault_root, s_rel)
                if os.path.exists(s_dir):
                    for ib_f in os.listdir(s_dir):
                        if not ib_f.endswith('.md') or ib_f.startswith('.') or ib_f in ("Review Dashboard.md", "Draft", "Source"):
                            continue
                        ib_fp = os.path.join(s_dir, ib_f)
                        if not os.path.isfile(ib_fp):
                            continue
                        try:
                            with open(ib_fp, 'r', encoding='utf-8', errors='ignore') as rf:
                                rfc = rf.read()
                            _, rfm_t, _, _ = brain_health.split_markdown_note(rfc)
                            rmeta = brain_health.safe_load_frontmatter(rfm_t, brain_health.build_yaml_engine())
                            if rmeta.get('video_url') == src_target or rmeta.get('source') == src_target:
                                os.remove(ib_fp)
                                deleted = True
                                break
                        except Exception:
                            pass
                    if deleted:
                        break
        append_inbox_history(vault_root, "ERROR_DISMISSED", src_target, "DISMISSED")
        return True, None

    return False, None


def _handle_promote_item(vault_root: str, draft_path: str, source_path: str, name: str, raw_name: str, src_name: str) -> Tuple[bool, Optional[str]]:
    """Promotes an approved draft [x] to permanent Atlas/Blog storage."""
    if not os.path.exists(draft_path):
        return False, None
    with open(draft_path, "r", encoding="utf-8") as f:
        content = f.read()
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

    dest_abs = os.path.abspath(os.path.join(vault_root, target_rel))
    vault_abs = os.path.abspath(vault_root)

    if not dest_abs.startswith(vault_abs + os.sep) and dest_abs != vault_abs:
        return False, f"Path traversal bloccato: {target_rel}"
    src_val = meta.get('source', 'original')
    dup = check_duplicate_resource(vault_root, src_val, real_name)
    if dup and os.path.abspath(dup[0]) != dest_abs:
        return False, f"Duplicato sorgente rilevato in {os.path.relpath(dup[0], vault_root)}"
    if os.path.exists(dest_abs):
        with open(dest_abs, 'r', encoding='utf-8', errors='ignore') as f:
            dest_text = f.read(1500)
        if src_val != 'original' and src_val not in dest_text:
            return False, f"Conflitto nome file con sorgente diversa in {target_rel}"

    meta['status'] = 'permanent'
    meta['title'] = real_name
    meta['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    if 'target_path' in meta:
        del meta['target_path']
    clean_body, _ = brain_health.strip_isolated_hashtag_lines(body)
    fm_str = brain_health.format_canonical_frontmatter(meta, is_blog=target_rel.startswith("05 - Blog"))
    final_note = brain_health.assemble_markdown_note(fm_str, brain_health.get_breadcrumbs(target_rel, real_name), sanitize_style_highlights(clean_body))

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(final_note)
    if os.path.exists(draft_path):
        os.remove(draft_path)

    # University PACRAR matrix sync hook (D-15, PACRAR-03)
    if "02 - Atlas/Education & Learning/University/" in target_rel:
        parts = Path(target_rel).parts
        if len(parts) >= 5:
            course_name = parts[3]
            try:
                import course_hub
                course_hub.register_lesson(course_name, real_name, vault_root=vault_root)
            except Exception as e:
                logger.warning("Errore durante la registrazione PACRAR per '%s': %s", real_name, e)

    extra_sources = set()
    if os.path.exists(source_path):
        src_txt = ""
        with open(source_path, 'r', encoding='utf-8', errors='ignore') as sf:
            src_txt = sf.read()
        for m_lnk in re.finditer(r'\[\[(.*?)\]\]', src_txt):
            extra_sources.add(m_lnk.group(1).split('|')[0].strip())
        if src_val == "original" or "ready:" in src_txt[:500]:
            arc_dir = os.path.join(vault_root, "99 - Meta", "Archive")
            os.makedirs(arc_dir, exist_ok=True)
            shutil.move(source_path, os.path.join(arc_dir, f"{real_name}.md"))
        else:
            os.remove(source_path)

    # Multi-source dependencies cleanup on promote [x] (Option B)
    sources_list = meta.get('sources', [])
    if isinstance(sources_list, str):
        sources_list = [s.strip() for s in sources_list.split(',') if s.strip()]

    all_targets = set()
    for s_ref in sources_list:
        clean_s = str(s_ref).strip().strip('"').strip("'")
        m_link = re.search(r'\[\[(.*?)\]\]', clean_s)
        target_name = m_link.group(1).split('|')[0].strip() if m_link else clean_s
        if target_name:
            all_targets.add(target_name)
    all_targets.update(extra_sources)

    for target_name in all_targets:
        cand_srcs = [
            os.path.join(vault_root, "03 - Inbox", "Source", f"{target_name}.md"),
            os.path.join(vault_root, "03 - Inbox", "Source", target_name),
            os.path.join(vault_root, "03 - Inbox", f"{target_name}.md"),
            os.path.join(vault_root, "03 - Inbox", target_name),
        ]
        for c_src in cand_srcs:
            if os.path.exists(c_src) and os.path.isfile(c_src):
                if c_src.endswith('.md'):
                    try:
                        with open(c_src, 'r', encoding='utf-8', errors='ignore') as f:
                            txt_head = f.read(1500).lower()
                    except Exception:
                        txt_head = ""
                    is_transcript = any(k in txt_head or k in target_name.lower() for k in ('trascrizion', 'transcript', 'whisper', 'audio')) or bool(re.search(r'\[\d{2}:\d{2}', txt_head))
                    if is_transcript:
                        try:
                            os.remove(c_src)
                        except Exception:
                            pass
                    else:
                        arc_dir = os.path.join(vault_root, "99 - Meta", "Archive")
                        os.makedirs(arc_dir, exist_ok=True)
                        dest_arc = os.path.join(arc_dir, os.path.basename(c_src))
                        if os.path.exists(dest_arc):
                            dest_arc = os.path.join(arc_dir, f"{Path(c_src).stem} (Archived){Path(c_src).suffix}")
                        try:
                            shutil.move(c_src, dest_arc)
                        except Exception:
                            pass
                elif not c_src.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.webp')):
                    try:
                        os.remove(c_src)
                    except Exception:
                        pass
                break

    # Proactive cleanup of unlisted audio transcripts in 03 - Inbox/Source/ matching course or note
    course_val = meta.get('course')
    course_clean = brain_health.clean_title_str(str(course_val)).lower() if course_val else ""
    name_clean = real_name.lower()
    src_clean = src_name.lower() if src_name else ""
    source_inbox_dir = os.path.join(vault_root, "03 - Inbox", "Source")
    if os.path.exists(source_inbox_dir):
        for f_name in os.listdir(source_inbox_dir):
            if not f_name.endswith('.md') or f_name.startswith('.'):
                continue
            f_path = os.path.join(source_inbox_dir, f_name)
            if not os.path.isfile(f_path):
                continue
            try:
                with open(f_path, 'r', encoding='utf-8', errors='ignore') as sf:
                    head = sf.read(1500).lower()
            except Exception:
                head = ""
            is_tr = any(k in head or k in f_name.lower() for k in ('trascrizion', 'transcript', 'whisper', 'audio')) or bool(re.search(r'\[\d{2}:\d{2}', head))
            if is_tr:
                fn_low = f_name.lower()
                matches_course = bool(course_clean and (course_clean in fn_low or course_clean in head[:500]))
                matches_name = any(token in fn_low for token in name_clean.split() if len(token) > 4)
                matches_src = bool(src_clean and any(token in fn_low for token in src_clean.split() if len(token) > 4))
                if matches_course or matches_name or matches_src:
                    try:
                        os.remove(f_path)
                    except Exception:
                        pass

    append_inbox_history(vault_root, "APPROVED", real_name, target_rel, src_val)
    return True, None


def _handle_purge_item(vault_root: str, draft_path: str, source_path: str, name: str) -> bool:
    """Purges a rejected draft [-] and its associated clipboard assets."""
    note_content = ""
    if os.path.exists(draft_path):
        try:
            with open(draft_path, "r", encoding="utf-8", errors="ignore") as f:
                note_content = f.read()
        except Exception:
            pass
    elif os.path.exists(source_path):
        try:
            with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
                note_content = f.read()
        except Exception:
            pass

    meta = {}
    body = ""
    if note_content:
        has_fm, fm_t, _, bdy = brain_health.split_markdown_note(note_content)
        if has_fm:
            meta = brain_health.safe_load_frontmatter(fm_t, brain_health.build_yaml_engine())
        body = bdy

    vid_url = meta.get('video_url') or meta.get('source')
    video_id = youtube_helper.get_video_id(str(vid_url)) if vid_url else None

    clip_dir = os.path.join(vault_root, "99 - Meta", "Clipboard")
    if os.path.exists(clip_dir):
        # 1. Purge based on video_id
        if video_id:
            for img in os.listdir(clip_dir):
                if img.startswith(f"{video_id}_") and (img.endswith('.jpg') or img.endswith('.png')):
                    try:
                        os.remove(os.path.join(clip_dir, img))
                    except Exception:
                        pass

        # 2. Purge based on explicit markdown image embeddings (supports course subdirectories)
        img_refs = re.findall(r'!\[\[(.*?)\]\]', body) + re.findall(r'!\[.*?\]\((.*?)\)', body)
        for ref in img_refs:
            base_img = os.path.basename(ref.split('|')[0].strip())
            for root_dir, _, files in os.walk(clip_dir):
                if base_img in files:
                    try:
                        os.remove(os.path.join(root_dir, base_img))
                    except Exception:
                        pass

        # 3. Fallback: prefix-based purge
        prefix = name[:10]
        slug = name.lower().replace(' ', '_')[:10]
        for root_dir, _, files in os.walk(clip_dir):
            for img in files:
                if (img.startswith(prefix) or slug in img or img.startswith(f"Figura - {name}")) and (img.endswith('.jpg') or img.endswith('.png')):
                    try:
                        os.remove(os.path.join(root_dir, img))
                    except Exception:
                        pass

    # Physical removal of draft and source
    if os.path.exists(draft_path):
        try:
            os.remove(draft_path)
        except Exception:
            pass
    if os.path.exists(source_path):
        try:
            os.remove(source_path)
        except Exception:
            pass

    # Multi-source dependencies cleanup on purge [-] (Option B)
    sources_list = meta.get('sources', [])
    if isinstance(sources_list, str):
        sources_list = [s.strip() for s in sources_list.split(',') if s.strip()]

    all_targets = set()
    for s_ref in sources_list:
        clean_s = str(s_ref).strip().strip('"').strip("'")
        m_link = re.search(r'\[\[(.*?)\]\]', clean_s)
        target_name = m_link.group(1).split('|')[0].strip() if m_link else clean_s
        if target_name:
            all_targets.add(target_name)

    if note_content:
        for m_lnk in re.finditer(r'\[\[(.*?)\]\]', note_content):
            all_targets.add(m_lnk.group(1).split('|')[0].strip())

    for target_name in all_targets:
        cand_srcs = [
            os.path.join(vault_root, "03 - Inbox", "Source", f"{target_name}.md"),
            os.path.join(vault_root, "03 - Inbox", "Source", target_name),
            os.path.join(vault_root, "03 - Inbox", f"{target_name}.md"),
            os.path.join(vault_root, "03 - Inbox", target_name),
        ]
        for c_src in cand_srcs:
            if os.path.exists(c_src) and os.path.isfile(c_src):
                try:
                    os.remove(c_src)
                except Exception:
                    pass

        # Purge any newly archived attachments created for this note
        att_root = os.path.join(vault_root, "99 - Meta", "Attachments")
        if os.path.exists(att_root):
            for root_dir, _, files in os.walk(att_root):
                if target_name in files:
                    try:
                        os.remove(os.path.join(root_dir, target_name))
                    except Exception:
                        pass

    # Proactive purge of unlisted transcripts in 03 - Inbox/Source/
    course_val = meta.get('course')
    course_clean = brain_health.clean_title_str(str(course_val)).lower() if course_val else ""
    name_clean = name.lower()
    source_inbox_dir = os.path.join(vault_root, "03 - Inbox", "Source")
    if os.path.exists(source_inbox_dir):
        for f_name in os.listdir(source_inbox_dir):
            if not f_name.endswith('.md') or f_name.startswith('.'):
                continue
            f_path = os.path.join(source_inbox_dir, f_name)
            if not os.path.isfile(f_path):
                continue
            try:
                with open(f_path, 'r', encoding='utf-8', errors='ignore') as sf:
                    head = sf.read(1500).lower()
            except Exception:
                head = ""
            is_tr = any(k in head or k in f_name.lower() for k in ('trascrizion', 'transcript', 'whisper', 'audio')) or bool(re.search(r'\[\d{2}:\d{2}', head))
            if is_tr:
                fn_low = f_name.lower()
                matches_course = bool(course_clean and (course_clean in fn_low or course_clean in head[:500]))
                matches_name = any(token in fn_low for token in name_clean.split() if len(token) > 4)
                if matches_course or matches_name:
                    try:
                        os.remove(f_path)
                    except Exception:
                        pass

    append_inbox_history(vault_root, "REJECTED", name, "PURGED")
    return True


def _process_tri_state_approvals_unlocked(vault_root: str) -> int:
    """Processes [x] (Promote), [-] (Purge), panic button, and error retry/dismiss lines in Review Dashboard.md."""
    dash_path = os.path.join(vault_root, "03 - Inbox", "Review Dashboard.md")
    if not os.path.exists(dash_path):
        return 0
    with open(dash_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
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
                updated_lines.append(line)
                continue
            raw_target = m_err.group('src').strip()
            if raw_target.startswith('[[') and raw_target.endswith(']]'):
                raw_target = raw_target[2:-2]
            src_target = raw_target.split('|')[0].strip()
            if src_target.startswith("Draft/"):
                src_target = src_target[6:]
            if src_target.startswith("Source/"):
                src_target = src_target[7:]

            success, err_msg = _handle_error_item(vault_root, src_target, status)
            if success:
                processed_count += 1
            elif err_msg:
                pending_errors.append((src_target, err_msg))
            continue

        m = RE_APPROVAL_LINE.match(line)
        if not m or m.group('status') == ' ':
            updated_lines.append(line)
            continue
        status = m.group('status')
        raw_name = m.group('name').split('|')[0].strip()
        name = brain_health.clean_title_str(raw_name)
        raw_src = m.group('src').split('|')[0].strip() if m.group('src') else None
        src_name = brain_health.clean_title_str(raw_src) if raw_src else name

        draft_path = os.path.join(vault_root, "03 - Inbox", "Draft", f"{name}.md")
        if not os.path.exists(draft_path):
            draft_path = os.path.join(vault_root, "03 - Inbox", "Draft", f"{raw_name}.md")
        if not os.path.exists(draft_path):
            draft_path = os.path.join(vault_root, "03 - Inbox", f"{name}.md")
        if not os.path.exists(draft_path):
            draft_path = os.path.join(vault_root, "03 - Inbox", f"{raw_name}.md")
        source_path = os.path.join(vault_root, "03 - Inbox", "Source", f"{src_name}.md")
        if not os.path.exists(source_path):
            source_path = os.path.join(vault_root, "03 - Inbox", "Source", f"{name}.md")
        if not os.path.exists(source_path):
            source_path = os.path.join(vault_root, "03 - Inbox", "Source", f"{raw_name}.md")

        if status in ('x', 'X'):
            success, err_msg = _handle_promote_item(vault_root, draft_path, source_path, name, raw_name, src_name)
            if success:
                processed_count += 1
            elif err_msg:
                pending_errors.append((name, err_msg))
                updated_lines.append(line)
        elif status == '-':
            if _handle_purge_item(vault_root, draft_path, source_path, name):
                processed_count += 1

    if panic_triggered:
        _handle_panic_action(vault_root)
        processed_count += 1
    else:
        with open(dash_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        update_review_dashboard(vault_root)
        for err_src, err_rsn in pending_errors:
            update_review_dashboard(vault_root, add_error=(err_src, err_rsn))
    return processed_count


def process_tri_state_approvals(vault_root: str) -> int:
    """Processes [x] (Promote), [-] (Purge), panic button, and error retry/dismiss lines in Review Dashboard.md under DashboardLock (D-07)."""
    try:
        with DashboardLock(vault_root, timeout=10.0, retry_interval=0.2):
            return _process_tri_state_approvals_unlocked(vault_root)
    except TimeoutError as e:
        logging.warning("Impossibile acquisire DashboardLock per process_tri_state_approvals: %s", e)
        return 0


def process_inbox_raw_notes(vault_root: str) -> List[str]:
    """Scans 03 - Inbox/ root and 03 - Inbox/Source/ for ready: true notes and stages their source into Source/, placing them under In Elaborazione."""
    inbox_dir = os.path.join(vault_root, "03 - Inbox")
    source_dir = os.path.join(inbox_dir, "Source")
    os.makedirs(source_dir, exist_ok=True)
    if not os.path.exists(inbox_dir): return []
    processed = []

    candidates = []
    # 1. 03 - Inbox/ root
    for file in sorted(os.listdir(inbox_dir)):
        if not file.endswith('.md') or file.startswith('.') or file in ("Review Dashboard.md", "Draft", "Source"): continue
        file_path = os.path.join(inbox_dir, file)
        if os.path.isfile(file_path):
            candidates.append((file_path, False))

    # 2. 03 - Inbox/Source/ (for retried notes)
    if os.path.exists(source_dir):
        for file in sorted(os.listdir(source_dir)):
            if not file.endswith('.md') or file.startswith('.'): continue
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path):
                candidates.append((file_path, True))

    for file_path, is_in_source in candidates:
        if not os.path.exists(file_path): continue
        clean_title = ""
        src_url = None
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
            has_fm, fm_text, _, body = brain_health.split_markdown_note(content)
            meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine()) if has_fm else {}
            if str(meta.get('ready')).lower() != 'true': continue

            file_name = os.path.basename(file_path)
            clean_title = brain_health.clean_title_str(meta.get('title') or file_name[:-3])
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
                raw_fm = re.sub(r'ready:\s*(true|"true"|\'true\'|1)', 'ready: false', fm_text, flags=re.IGNORECASE)
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

            # D-01: Spostamento atomico preventivo delle note grezze in 03 - Inbox/Source/ prima di Fase 1/3 e Fase 2/3 AI
            if not is_in_source:
                target_source_path = os.path.join(source_dir, file_name)
                if os.path.exists(target_source_path) and os.path.abspath(file_path) != os.path.abspath(target_source_path):
                    try: os.remove(target_source_path)
                    except Exception: pass
                shutil.move(file_path, target_source_path)
                file_path = target_source_path
                is_in_source = True

            # -------------------------------------------------------------
            # FASE 1/3: Estrazione Sorgente
            # -------------------------------------------------------------
            update_review_dashboard(vault_root, in_progress=clean_title, phase="Fase 1/3: Estrazione Sorgente...")
            target_dir = classify_target_directory(clean_title, meta.get('tags', []), body)

            # Deep Ingestion (Option B): Resolve local inbox dependencies and attached files
            course_for_deps = meta.get('course')
            resolved_content, resolved_sources = resolve_inbox_dependencies(
                content=content,
                note_path=file_path,
                vault_root=vault_root,
                course=course_for_deps
            )
            content = resolved_content
            has_split, _, _, split_body = brain_health.split_markdown_note(resolved_content)
            body = split_body if has_split else resolved_content
            if resolved_sources:
                meta['sources'] = [s['wikilink'] for s in resolved_sources]

            # -------------------------------------------------------------
            # FASE 2/3: Rielaborazione Concettuale AI
            # -------------------------------------------------------------
            update_review_dashboard(vault_root, in_progress=clean_title, phase="Fase 2/3: Rielaborazione Concettuale AI...")
            meta['title'] = clean_title
            meta['target_path'] = f"{target_dir}/{clean_title}.md"
            stage_note(vault_root, clean_title, body, meta, target_dir=target_dir, source_content=content, status='in-progress')

            enriched_body, summary = enrich_draft_with_ai(vault_root, clean_title, content, depth="approfondimento", source_type="concept", source_url="original")

            if clean_title.lower().startswith("raw note") or clean_title.lower() in ("untitled", "draft", "bozza", "nuova nota", ""):
                m_ai_h1 = re.search(r'^\s*#\s+([^\n]+)', enriched_body, re.MULTILINE)
                if m_ai_h1:
                    cand_ai = brain_health.clean_title_str(m_ai_h1.group(1).strip())
                    if cand_ai and not cand_ai.lower().startswith("raw note") and cand_ai.lower() not in ("untitled", "draft", "bozza", "nuova nota", "appunti grezzi", "idee"):
                        old_title = clean_title
                        clean_title = cand_ai
                        old_in_prog = os.path.join(vault_root, "03 - Inbox", "Draft", f"{old_title}.md")
                        old_source = os.path.join(vault_root, "03 - Inbox", "Source", f"{old_title}.md")
                        new_source = os.path.join(vault_root, "03 - Inbox", "Source", f"{clean_title}.md")
                        if os.path.exists(old_in_prog):
                            try: os.remove(old_in_prog)
                            except Exception: pass
                        if os.path.exists(old_source) and old_title != clean_title:
                            if os.path.exists(new_source) and os.path.abspath(old_source) != os.path.abspath(new_source):
                                try: os.remove(new_source)
                                except Exception: pass
                            try: shutil.move(old_source, new_source)
                            except Exception: pass
                        file_path = new_source
                        target_dir = classify_target_directory(clean_title, meta.get('tags', []), enriched_body)

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
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
                    _, fm_t, _, bdy = brain_health.split_markdown_note(c)
                    rfm = re.sub(r'ready:\s*(true|"true"|\'true\'|1)', 'ready: false', fm_t, flags=re.IGNORECASE)
                    if 'ready:' not in rfm: rfm += "\nready: false"
                    with open(file_path, 'w', encoding='utf-8') as f: f.write(f"---\n{rfm.strip()}\n---\n\n{bdy.strip()}\n")
            except Exception: pass
            err_target = src_url if (src_url and str(src_url).strip()) else (clean_title if clean_title else os.path.basename(file_path)[:-3])
            record_ingest_error(vault_root, err_target, str(e))
    return processed

def ingest_source(source: str, vault_root: Optional[str] = None, target_dir: Optional[str] = None,
                  depth: str = "approfondimento", extract_frames: bool = False, force: bool = False,
                  use_ai: bool = True, course: Optional[str] = None, nlm: bool = False, anki: bool = False) -> str:
    """Unified entry point executing the lean 3-macro-phase lifecycle into 03 - Inbox/Draft/."""
    root = brain_health.get_vault_root(vault_root)
    result_path = None
    clean_course = None
    if course:
        import course_hub
        clean_course = course_hub.sanitize_course_name(course)
        course_hub.ensure_course_hub(clean_course, vault_root=root)
        dest_course_dir = f"02 - Atlas/Education & Learning/University/{clean_course}"
        target_dir = dest_course_dir

    with NoteLock(source):
        in_type = detect_input_type(source)
        prov = Path(source).stem if in_type in ("file", "pdf") else (source if in_type in ("youtube", "web") else source.strip().splitlines()[0].lstrip('#').strip()[:40])

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
                except youtube_helper.VideoMetadataError as e:
                    record_ingest_error(root, source, f"Errore metadati video: {e}")
                    raise
                except Exception as e:
                    record_ingest_error(root, source, f"Errore estrazione YouTube: {e}")
                    raise
                title, channel = data['title'], data['channel']
                clean_title = brain_health.clean_title_str(title)
                raw_text = " ".join([t.get('text', '') for t in data['transcript']])
                dest_dir = target_dir or classify_target_directory(clean_title, ['tech/ai', 'video'], raw_text)
                meta = {'title': clean_title, 'type': 'video', 'area': 'tech', 'source': source, 'video_url': source, 'channel': channel, 'tags': ['tech/ai', 'video']}

            elif in_type == "pdf":
                try:
                    import academic_helper
                    pdf_data = academic_helper.extract_pdf_data(
                        source,
                        course=clean_course,
                        vault_root=root
                    )
                except academic_helper.PdfEncryptedError as e:
                    record_ingest_error(root, source, f"PDF protetto da password: {e}")
                    update_review_dashboard(root, in_progress="CLEAR_ALL")
                    raise
                except academic_helper.PdfTextUnavailableError as e:
                    attachments_dir = os.path.join(root, "99 - Meta", "Attachments", clean_course if clean_course else "")
                    clean_stem = brain_health.clean_title_str(Path(source).stem)
                    pdf_filename, permanent_pdf_path = academic_helper.archive_pdf_attachment(source, attachments_dir, clean_stem)
                    raw_text = f"<!-- PDF allegato: [[{pdf_filename}]] (Appunti manoscritti / scansione priva di OCR) -->"
                    pdf_data = {
                        'title': clean_stem,
                        'pdf_filename': pdf_filename,
                        'permanent_pdf_path': permanent_pdf_path,
                        'raw_text': raw_text
                    }
                    if os.path.dirname(os.path.abspath(source)) == os.path.abspath(os.path.join(root, "03 - Inbox")):
                        try: os.remove(source)
                        except Exception: pass
                except Exception as e:
                    record_ingest_error(root, source, f"Errore estrazione PDF: {e}")
                    update_review_dashboard(root, in_progress="CLEAR_ALL")
                    raise

                title = pdf_data['title']
                clean_title = brain_health.clean_title_str(title)
                raw_text = pdf_data['raw_text']
                pdf_filename = pdf_data['pdf_filename']

                if clean_course:
                    dest_dir = target_dir
                    meta = {
                        'title': clean_title,
                        'type': 'lecture',
                        'area': 'education',
                        'source': f"[[{pdf_filename}]]",
                        'course': clean_course,
                        'tags': ['education/university', 'education/lecture']
                    }
                else:
                    dest_dir = target_dir or classify_target_directory(clean_title, ['tech'], raw_text)
                    meta = {
                        'title': clean_title,
                        'type': 'concept',
                        'area': 'tech',
                        'source': f"[[{pdf_filename}]]",
                        'tags': ['raw']
                    }

            elif in_type == "file":
                try:
                    with open(source, 'r', encoding='utf-8', errors='ignore') as f:
                        raw_text = f.read()
                    title = Path(source).stem
                    clean_title = brain_health.clean_title_str(title)
                    dest_dir = target_dir or classify_target_directory(clean_title, ['raw'], raw_text)
                    meta = {'title': clean_title, 'type': 'concept', 'area': 'tech', 'source': 'original', 'tags': ['raw']}
                except (FileNotFoundError, OSError):
                    lines = [l.strip() for l in source.strip().splitlines() if l.strip()]
                    title = lines[0].lstrip('#').strip() if lines else "Nuova Nota"
                    clean_title = brain_health.clean_title_str(title)
                    raw_text = source
                    dest_dir = target_dir or classify_target_directory(clean_title, ['tech'], source)
                    meta = {'title': clean_title, 'type': 'concept', 'area': 'tech', 'source': 'original'}

                # Deep Ingestion (Option B): Resolve local inbox dependencies and attached files
                resolved_text, resolved_sources = resolve_inbox_dependencies(
                    content=raw_text,
                    note_path=source if os.path.isfile(source) else None,
                    vault_root=root,
                    course=clean_course
                )
                raw_text = resolved_text
                if resolved_sources:
                    meta['sources'] = [s['wikilink'] for s in resolved_sources]

                # If source file is in 03 - Inbox/ root, stage it into 03 - Inbox/Source/
                if os.path.isfile(source):
                    src_dir_abs = os.path.abspath(os.path.dirname(source))
                    inbox_abs = os.path.abspath(os.path.join(root, "03 - Inbox"))
                    if src_dir_abs == inbox_abs:
                        target_source_path = os.path.join(inbox_abs, "Source", os.path.basename(source))
                        if os.path.exists(target_source_path) and os.path.abspath(source) != os.path.abspath(target_source_path):
                            try: os.remove(target_source_path)
                            except Exception: pass
                        try: shutil.move(source, target_source_path)
                        except Exception: pass

            else:
                lines = [l.strip() for l in source.strip().splitlines() if l.strip()]
                title = lines[0].lstrip('#').strip() if lines else "Nuova Nota"
                clean_title = brain_health.clean_title_str(title)
                raw_text = source
                dest_dir = target_dir or classify_target_directory(clean_title, ['tech'], source)
                meta = {'title': clean_title, 'type': 'article' if in_type == 'web' else 'concept', 'area': 'tech', 'source': source if in_type == 'web' else 'original'}

                if in_type != 'web':
                    resolved_text, resolved_sources = resolve_inbox_dependencies(
                        content=raw_text,
                        note_path=None,
                        vault_root=root,
                        course=clean_course
                    )
                    raw_text = resolved_text
                    if resolved_sources:
                        meta['sources'] = [s['wikilink'] for s in resolved_sources]

            if clean_course:
                dest_dir = target_dir
                meta['area'] = 'education'
                if 'tags' not in meta:
                    meta['tags'] = []
                if 'education/university' not in meta['tags']:
                    meta['tags'].append('education/university')
                meta['course'] = clean_course

            # -------------------------------------------------------------
            # FASE 2/3: Rielaborazione Concettuale AI
            # -------------------------------------------------------------
            update_review_dashboard(root, in_progress=clean_title, phase="Fase 2/3: Rielaborazione Concettuale AI...", replace_in_progress=prov)
            dest_dir = target_dir or classify_target_directory(clean_title, meta.get('tags', []), raw_text)
            meta['title'] = clean_title
            meta['target_path'] = f"{dest_dir}/{clean_title}.md"
            if clean_course:
                meta['course'] = clean_course
                meta['area'] = 'education'
            stage_note(root, clean_title, raw_text, meta, target_dir=dest_dir, source_content=raw_text, status='in-progress')

            # Check if target note already exists with Anki cards (D-14)
            original_target_content = ""
            existing_target_path = None
            if dest_dir:
                cand_target = os.path.join(root, dest_dir, f"{clean_title}.md") if not os.path.isabs(dest_dir) else os.path.join(dest_dir, f"{clean_title}.md")
                if os.path.exists(cand_target):
                    existing_target_path = cand_target
            if not existing_target_path:
                for root_dir, _, files in os.walk(os.path.join(root, "02 - Atlas")):
                    if f"{clean_title}.md" in files:
                        existing_target_path = os.path.join(root_dir, f"{clean_title}.md")
                        break

            if existing_target_path and os.path.exists(existing_target_path):
                try:
                    with open(existing_target_path, "r", encoding="utf-8", errors="ignore") as f:
                        original_target_content = f.read()
                except Exception:
                    original_target_content = ""

            metacognitive_prompt = None
            metacognitive_markdown = None
            if nlm and use_ai:
                import nlm_helper
                try:
                    directives = nlm_helper.query_notebook(clean_title, raw_text, course=clean_course, vault_root=root)
                    metacognitive_prompt = nlm_helper.format_metacognitive_constraints_prompt(directives)
                    metacognitive_markdown = nlm_helper.format_metacognitive_markdown_section(directives)
                except nlm_helper.NLMError as e:
                    err_msg = "ERRORE: Impossibile consultare NotebookLM. Esegui 'nlm login' o verifica la connessione."
                    sys.stderr.write(f"{err_msg}\n")
                    record_ingest_error(root, prov, err_msg)
                    update_review_dashboard(root, in_progress="CLEAR_ALL")
                    sys.exit(1)

            enable_anki = bool(
                anki or clean_course or
                (meta.get('area') == 'education') or
                ('education' in meta.get('tags', []))
            )

            if use_ai:
                enriched_body, summary = enrich_draft_with_ai(
                    root, clean_title, raw_text, depth=depth, source_type=in_type, source_url=source,
                    metacognitive_constraints=metacognitive_prompt,
                    enable_anki=enable_anki,
                    course_name=clean_course
                )
            else:
                enriched_body = format_structured_note(clean_title, raw_text, depth=depth, source_type=in_type, source_url=source)
                summary = f"Trattazione concettuale ed evidenze chiave per {clean_title}."

            # Post-enrichment ID realignment (D-14)
            if original_target_content:
                import anki_helper
                enriched_body = anki_helper.reinject_anki_cards(original_target_content, enriched_body)

            if metacognitive_markdown:
                if not re.search(r'^##\s+(?:Direttive Metacognitive)', enriched_body, re.MULTILINE | re.IGNORECASE):
                    enriched_body = f"{enriched_body.rstrip()}\n{metacognitive_markdown}"

            if clean_title.lower().startswith("raw note") or clean_title.lower() in ("untitled", "draft", "bozza", "nuova nota"):
                m_ai_h1 = re.search(r'^\s*#\s+([^\n]+)', enriched_body, re.MULTILINE)
                if m_ai_h1:
                    cand_ai = brain_health.clean_title_str(m_ai_h1.group(1).strip())
                    if cand_ai and not cand_ai.lower().startswith("raw note") and cand_ai.lower() not in ("untitled", "draft", "bozza", "nuova nota", "appunti grezzi", "idee"):
                        old_title = clean_title
                        clean_title = cand_ai
                        old_in_prog = os.path.join(root, "03 - Inbox", "Draft", f"{old_title}.md")
                        old_source = os.path.join(root, "03 - Inbox", "Source", f"{old_title}.md")
                        new_source = os.path.join(root, "03 - Inbox", "Source", f"{clean_title}.md")
                        meta['title'] = clean_title
                        if os.path.exists(old_in_prog):
                            try: os.remove(old_in_prog)
                            except Exception: pass
                        if os.path.exists(old_source) and old_title != clean_title:
                            if os.path.exists(new_source) and os.path.abspath(old_source) != os.path.abspath(new_source):
                                try: os.remove(new_source)
                                except Exception: pass
                            try: shutil.move(old_source, new_source)
                            except Exception: pass

            dest_dir = target_dir or classify_target_directory(clean_title, meta.get('tags', []), enriched_body)
            meta['title'] = clean_title
            meta['target_path'] = f"{dest_dir}/{clean_title}.md"
            if clean_course:
                meta['course'] = clean_course
                meta['area'] = 'education'
            stage_note(root, clean_title, enriched_body, meta, target_dir=dest_dir, source_content=raw_text, status='in-progress')

            # -------------------------------------------------------------
            # FASE 3/3: Autolinking & Staging
            # -------------------------------------------------------------
            linked_body, links = autolink_content(root, enriched_body, clean_title)
            meta['summary'] = summary
            if links:
                if clean_course:
                    links = [l for l in links if l not in (f"[[{clean_course} MOC]]", f"[[{clean_course}]]")]
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
    parser.add_argument('--course', default=None, help="Target university course name (auto-initializes Course Hub & PACRAR matrix)")
    parser.add_argument('--nlm', action='store_true', help="Consult NotebookLM (Alessandro de Concini) for metacognitive directives during AI conceptual enrichment (D-03)")
    parser.add_argument('--anki', action='store_true', help="Generate contextual Anki flashcards (Basic/Cloze) inside collapsible callouts (D-09)")
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
        path = ingest_source(args.input, vault_root=root, target_dir=args.target_dir, depth=depth, extract_frames=args.extract_frames, force=args.force, use_ai=not args.no_ai, course=args.course, nlm=args.nlm, anki=args.anki)
        print(f"Draft staged at: {path}")
    else:
        update_review_dashboard(root)
        print("Review Dashboard refreshed.")

if __name__ == '__main__':
    main()

