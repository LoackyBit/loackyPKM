#!/usr/bin/env python3
"""
recall_engine.py - Hybrid Retrieval & Conversational Search Engine for Second Brain.

Combines Ultra-Fast YAML Metadata Matching, Pure-Python Okapi BM25 Lexical Search,
and Smart Connections 384-d Dense Semantic Embeddings using Reciprocal Rank Fusion (RRF).
Outputs polymorphic responses (JSON, 3-section NotebookLM Markdown, and Colored Terminal).
"""

import os
import sys
import re
import json
import math
import struct
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, List, Set, Tuple, Optional, Any, Union

# Ensure script directory is available in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import ruamel.yaml

CONTROLLED_TYPES = {'concept', 'video', 'article', 'lecture', 'book', 'project', 'moc', 'journal'}
CONTROLLED_AREAS = {'tech', 'education', 'mentality', 'finance', 'projects', 'meta', 'calendar'}

IGNORE_FOLDERS = {
    '.git', '.obsidian', '.agents', '.gemini', '.trash', '.vscode',
    '.space', '.makemd', '.smart-env', '.antigravitycli', '.codacy',
    'node_modules', 'tests', '.planning', '99 - Meta', 'Template', '03 - Inbox'
}

STOPWORDS = {
    # Italian
    'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'di', 'del', 'dello',
    'della', 'dei', 'degli', 'delle', 'da', 'dal', 'dallo', 'dalla', 'dai', 'dagli',
    'dalle', 'in', 'nel', 'nello', 'nella', 'nei', 'negli', 'nelle', 'su', 'sul',
    'sullo', 'sulla', 'sui', 'sugli', 'sulle', 'con', 'per', 'tra', 'fra', 'e', 'ed',
    'o', 'od', 'ma', 'se', 'che', 'non', 'sono', 'come', 'anche', 'questo', 'questa',
    'questi', 'queste', 'quello', 'quella', 'quelli', 'quelle', 'cosa', 'chi', 'cui',
    'dove', 'quando', 'perché', 'perche', 'quale', 'quali', 'quanto', 'quanta',
    'quanti', 'quante', 'ci', 'vi', 'ne', 'si', 'mi', 'ti', 'li', 'lui', 'lei', 'loro',
    'noi', 'voi', 'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue',
    'suo', 'sua', 'suoi', 'sue', 'nostro', 'nostra', 'nostri', 'nostre',
    'vostro', 'vostra', 'vostri', 'vostre', 'ad', 'al', 'allo', 'alla', 'ai', 'agli', 'alle',
    # English
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with',
    'by', 'of', 'from', 'as', 'is', 'was', 'are', 'were', 'it', 'its', 'this',
    'that', 'these', 'those', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'can', 'could', 'should', 'would', 'will', 'what', 'which', 'who',
    'how', 'when', 'where', 'why', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'just'
}

CACHE_FILENAME = ".recall_cache.json"
VEC_DIM = 384
VEC_BYTES = VEC_DIM * 4  # 1536 bytes for 384 float32 values


def get_vault_root(start_path: Optional[str] = None) -> str:
    """Dynamically resolves the root path of the Second Brain vault."""
    if start_path:
        return os.path.abspath(start_path)
    return os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))


def tokenize(text: str) -> List[str]:
    """Tokenizes text into normalized alphanumeric keywords, stripping stopwords."""
    raw_tokens = re.findall(r'\b[a-zA-Z0-9_\-\u00C0-\u017F]+\b', text.lower())
    tokens = []
    for t in raw_tokens:
        clean_t = t.strip('_-')
        if clean_t and clean_t not in STOPWORDS and len(clean_t) > 1:
            tokens.append(clean_t)
    return tokens


class BM25Index:
    """Pure-Python Okapi BM25 Index with k1=1.5, b=0.75."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_lengths: Dict[str, int] = {}
        self.term_freqs: Dict[str, Dict[str, int]] = {}
        self.doc_freqs: Dict[str, int] = Counter()
        self.total_docs: int = 0
        self.avg_doc_len: float = 0.0

    def build_from_term_freqs(self, doc_lengths: Dict[str, int], term_freqs: Dict[str, Dict[str, int]]):
        """Builds inverted index and frequencies directly from document lengths and term frequencies (D-10)."""
        self.total_docs = len(doc_lengths)
        self.doc_lengths = dict(doc_lengths)
        self.term_freqs = dict(term_freqs)
        self.doc_freqs = Counter()
        for tf in self.term_freqs.values():
            for term in tf.keys():
                self.doc_freqs[term] += 1
        self.avg_doc_len = sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0.0

    def build_from_corpus(self, corpus: Dict[str, List[str]]):
        """Builds inverted index and term frequencies from tokenized document corpus."""
        doc_lengths = {doc_id: len(tokens) for doc_id, tokens in corpus.items()}
        term_freqs = {doc_id: dict(Counter(tokens)) for doc_id, tokens in corpus.items()}
        self.build_from_term_freqs(doc_lengths, term_freqs)

    def score(self, query_tokens: List[str]) -> List[Tuple[str, float]]:
        """Calculates Okapi BM25 scores for query tokens against all documents."""
        if not query_tokens or self.total_docs == 0:
            return []
        scores: List[Tuple[str, float]] = []
        for doc_id, tf in self.term_freqs.items():
            doc_len = self.doc_lengths.get(doc_id, 0)
            doc_score = 0.0
            for term in query_tokens:
                if term not in tf:
                    continue
                f = tf[term]
                n_q = self.doc_freqs.get(term, 0)
                # Robertson-Spärck Jones IDF with smoothing (+ 1.0 ensures non-negative idf)
                idf = math.log((self.total_docs - n_q + 0.5) / (n_q + 0.5) + 1.0)
                numerator = f * (self.k1 + 1.0)
                denominator = f + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                doc_score += idf * (numerator / denominator)
            if doc_score > 0.0:
                scores.append((doc_id, doc_score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


def split_markdown_note(content: str) -> Tuple[bool, str, Optional[str], str]:
    """Splits markdown into frontmatter text, breadcrumb line, and body."""
    lines = content.splitlines()
    has_frontmatter = False
    frontmatter_lines = []
    rest_lines = []

    if len(lines) > 0 and lines[0].strip() == '---':
        closing_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == '---':
                closing_idx = idx
                break
        if closing_idx != -1:
            has_frontmatter = True
            frontmatter_lines = lines[1:closing_idx]
            rest_lines = lines[closing_idx + 1:]
        else:
            rest_lines = lines
    else:
        rest_lines = lines

    breadcrumb = None
    body_start_idx = 0
    while body_start_idx < len(rest_lines) and not rest_lines[body_start_idx].strip():
        body_start_idx += 1

    if body_start_idx < len(rest_lines):
        candidate = rest_lines[body_start_idx].strip()
        if candidate.startswith('[[Home MOC') or (candidate.startswith('[[') and ' / ' in candidate):
            breadcrumb = candidate
            body_start_idx += 1

    body_lines = rest_lines[body_start_idx:]
    body_str = '\n'.join(body_lines).lstrip('\n')

    return has_frontmatter, '\n'.join(frontmatter_lines), breadcrumb, body_str


def safe_parse_frontmatter(fm_text: str) -> Dict[str, Any]:
    """Parses YAML frontmatter safely with fallback for unquoted wiki-links."""
    if not fm_text.strip():
        return {}
    yaml_engine = ruamel.yaml.YAML(typ='safe')
    try:
        data = yaml_engine.load(fm_text)
        if isinstance(data, dict):
            return dict(data)
    except Exception:
        pass

    # Regex fallback for key fields if ruamel fails on unquoted wiki-links
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip().strip('"\'')
            if k in ('tags', 'related', 'aliases'):
                items = re.findall(r'\[\[(.*?)\]\]', v) or [i.strip(' "\'[]') for i in v.split(',') if i.strip()]
                data[k] = items
            else:
                data[k] = v
    return data


def load_smart_connections_metadata(vault_root: str) -> Dict[str, Tuple[str, int]]:
    """
    Parses .smart-env/smart_sources/smart_sources.ajson using line-based reduction.
    Returns mapping {relative_path: (vector_file_name, vector_file_i)}.
    """
    ajson_path = os.path.join(vault_root, '.smart-env', 'smart_sources', 'smart_sources.ajson')
    if not os.path.exists(ajson_path):
        return {}

    sources: Dict[str, Any] = {}
    with open(ajson_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.endswith(','):
                line = line[:-1]
            idx = line.find(': ')
            if idx == -1:
                continue
            key = line[:idx].strip('\"')
            val = line[idx + 2:]
            if val == 'null':
                sources.pop(key, None)
            else:
                try:
                    sources[key] = json.loads(val)
                except Exception:
                    pass

    vector_refs: Dict[str, Tuple[str, int]] = {}
    for key, data in sources.items():
        if not isinstance(data, dict):
            continue
        path = data.get('path') or key.replace('smart_sources:', '')
        default_emb = data.get('embedding', {}).get('default', {})
        if isinstance(default_emb, dict) and default_emb:
            # Pick latest entry by timestamp 'at'
            latest = max(default_emb.values(), key=lambda x: x.get('at', 0) if isinstance(x, dict) else 0)
            if isinstance(latest, dict):
                v_file = latest.get('file')
                v_idx = latest.get('file_i')
                if v_file and v_idx is not None:
                    vector_refs[path] = (v_file, int(v_idx))

    return vector_refs


def read_vector(vault_root: str, vector_file: str, file_i: int) -> Optional[Tuple[float, ...]]:
    """Reads a 384-dimensional float32 unit vector directly from binary mf_* file."""
    bin_path = os.path.join(vault_root, '.smart-env', 'smart_sources', vector_file)
    if not os.path.exists(bin_path):
        return None
    offset = file_i * VEC_BYTES
    if offset + VEC_BYTES > os.path.getsize(bin_path):
        return None
    try:
        with open(bin_path, 'rb') as f:
            f.seek(offset)
            data = f.read(VEC_BYTES)
            if len(data) != VEC_BYTES:
                return None
            return struct.unpack('<384f', data)
    except Exception:
        return None


def cosine_similarity(vec_a: Tuple[float, ...], vec_b: Tuple[float, ...]) -> float:
    """Calculates dot product of two unit-normalized 384-d vectors."""
    return sum(a * b for a, b in zip(vec_a, vec_b))


def score_yaml_metadata(metadata: Dict[str, Any], query_tokens: List[str]) -> float:
    """
    Computes weighted YAML metadata score:
    - title: 10x
    - summary: 6x
    - tags & area: 4x
    - related & aliases: 2x
    """
    if not query_tokens:
        return 0.0

    title_text = str(metadata.get('title', '')).lower()
    summary_text = str(metadata.get('summary', '')).lower()
    area_text = str(metadata.get('area', '')).lower()
    tags = metadata.get('tags', [])
    tags_text = " ".join(str(t).lower() for t in tags if t) if isinstance(tags, list) else str(tags).lower()
    related = metadata.get('related', [])
    related_text = " ".join(str(r).lower() for r in related if r) if isinstance(related, list) else str(related).lower()
    aliases = metadata.get('aliases', [])
    aliases_text = " ".join(str(a).lower() for a in aliases if a) if isinstance(aliases, list) else str(aliases).lower()

    score = 0.0
    for tok in query_tokens:
        if tok in title_text:
            score += 10.0
        if tok in summary_text:
            score += 6.0
        if tok in area_text or tok in tags_text:
            score += 4.0
        if tok in related_text or tok in aliases_text:
            score += 2.0

    return score


def find_similar_notes(
    vault_root: str,
    target_note: str,
    cache_data: Dict[str, Any],
    limit: int = 5
) -> List[Tuple[str, float]]:
    """
    Finds semantically similar notes based on Smart Connections 384-d vector embeddings.
    """
    cleaned_target = target_note.strip('[]"\'').replace('.md', '').strip()
    files = cache_data.get('files', {})

    # Resolve target note key
    target_key = None
    target_entry = None

    for rel_path, entry in files.items():
        stem = Path(rel_path).stem
        title = entry.get('title', '')
        if (rel_path == target_note or
            rel_path == f"{cleaned_target}.md" or
            stem.lower() == cleaned_target.lower() or
            title.lower() == cleaned_target.lower()):
            target_key = rel_path
            target_entry = entry
            break

    if not target_entry:
        return []

    target_v_file = target_entry.get('vector_file')
    target_v_i = target_entry.get('vector_i')
    if not target_v_file or target_v_i is None:
        return []

    target_vec = read_vector(vault_root, target_v_file, target_v_i)
    if not target_vec:
        return []

    similarities: List[Tuple[str, float]] = []
    for rel_path, entry in files.items():
        if rel_path == target_key:
            continue
        v_file = entry.get('vector_file')
        v_i = entry.get('vector_i')
        if not v_file or v_i is None:
            continue
        vec = read_vector(vault_root, v_file, v_i)
        if vec:
            sim = cosine_similarity(target_vec, vec)
            similarities.append((rel_path, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:limit]


def reciprocal_rank_fusion(
    yaml_ranks: List[str],
    bm25_ranks: List[str],
    dense_ranks: List[str],
    k: int = 60,
    weights: Optional[Dict[str, float]] = None
) -> List[Tuple[str, float, Dict[str, int]]]:
    """
    Combines ranked lists from YAML, BM25, and Dense Semantic tracks using RRF:
    RRF(d) = sum_m [ w_m / (k + r_m(d)) ]
    Gracefully handles empty lists (e.g. dense_ranks=[]) without degradation.
    """
    if weights is None:
        weights = {'yaml': 1.0, 'bm25': 1.0, 'dense': 1.2}

    scores: Dict[str, float] = {}
    rank_details: Dict[str, Dict[str, int]] = {}

    tracks = [
        ('yaml', yaml_ranks, weights.get('yaml', 1.0)),
        ('bm25', bm25_ranks, weights.get('bm25', 1.0)),
        ('dense', dense_ranks, weights.get('dense', 1.2))
    ]

    for name, rank_list, w in tracks:
        for rank_idx, doc_id in enumerate(rank_list, start=1):
            if doc_id not in scores:
                scores[doc_id] = 0.0
                rank_details[doc_id] = {}
            scores[doc_id] += w / (k + rank_idx)
            rank_details[doc_id][name] = rank_idx

    fused = [(doc_id, score, rank_details[doc_id]) for doc_id, score in scores.items()]
    fused.sort(key=lambda x: x[1], reverse=True)
    return fused


def load_or_rebuild_cache(vault_root: str, force_reindex: bool = False) -> Dict[str, Any]:
    """
    Loads cache from .recall_cache.json with mtime invalidation.
    Reindexes modified or newly added files incrementally.
    """
    scripts_dir = os.path.join(vault_root, "99 - Meta", "Scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    cache_path = os.path.join(scripts_dir, CACHE_FILENAME)
    cache_data = {"version": 1, "files": {}}

    if os.path.exists(cache_path) and not force_reindex:
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if isinstance(loaded, dict) and loaded.get('version') == 1:
                    cache_data = loaded
        except Exception:
            cache_data = {"version": 1, "files": {}}

    cached_files = cache_data.get("files", {})
    updated = False
    for entry in cached_files.values():
        if "tokens" in entry:
            if "doc_len" not in entry:
                entry["doc_len"] = len(entry["tokens"])
            if "term_freq" not in entry:
                entry["term_freq"] = dict(Counter(entry["tokens"]))
            entry.pop("tokens", None)
            updated = True

    current_files = set()

    # Load Smart Connections vector references
    vector_refs = load_smart_connections_metadata(vault_root)

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')]
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, vault_root)
                current_files.add(rel_path)

                mtime = os.stat(abs_path).st_mtime
                cached_entry = cached_files.get(rel_path)

                v_info = vector_refs.get(rel_path)
                v_file = v_info[0] if v_info else None
                v_i = v_info[1] if v_info else None

                if (cached_entry and cached_entry.get('mtime') == mtime and not force_reindex):
                    # Check if vector reference updated
                    if cached_entry.get('vector_file') != v_file or cached_entry.get('vector_i') != v_i:
                        cached_entry['vector_file'] = v_file
                        cached_entry['vector_i'] = v_i
                        updated = True
                    continue

                # Read and parse file
                try:
                    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except Exception:
                    continue

                has_fm, fm_text, breadcrumb, body = split_markdown_note(content)
                meta = safe_parse_frontmatter(fm_text) if has_fm else {}

                tokens = tokenize(body)
                cached_files[rel_path] = {
                    "mtime": mtime,
                    "title": str(meta.get('title') or Path(rel_path).stem),
                    "area": str(meta.get('area') or ''),
                    "type": str(meta.get('type') or ''),
                    "tags": meta.get('tags') if isinstance(meta.get('tags'), list) else ([str(meta.get('tags'))] if meta.get('tags') else []),
                    "summary": str(meta.get('summary') or ''),
                    "related": meta.get('related') if isinstance(meta.get('related'), list) else ([str(meta.get('related'))] if meta.get('related') else []),
                    "aliases": meta.get('aliases') if isinstance(meta.get('aliases'), list) else ([str(meta.get('aliases'))] if meta.get('aliases') else []),
                    "doc_len": len(tokens),
                    "term_freq": dict(Counter(tokens)),
                    "vector_file": v_file,
                    "vector_i": v_i
                }
                updated = True

    # Remove deleted files
    deleted_keys = set(cached_files.keys()) - current_files
    if deleted_keys:
        for k in deleted_keys:
            del cached_files[k]
        updated = True

    cache_data["files"] = cached_files
    if updated or not os.path.exists(cache_path) or force_reindex:
        # Atomic write via temporary file with compact JSON serialization (D-09)
        tmp_path = cache_path + ".tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, separators=(',', ':'))
        os.replace(tmp_path, cache_path)

    return cache_data


ZERO_MATCH_MESSAGE = """⚠️ **Nessuna corrispondenza trovata nel Vault**: Il concetto "{query}" non è presente tra le note del Second Brain. Nessuna informazione esterna è stata integrata per preservare l'integrità della tua knowledge base."""


def extract_relevant_snippet_and_timestamps(
    vault_root: str,
    rel_path: str,
    query_tokens: List[str]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Extracts top matching H2/H3 section snippets and [MM:SS] or [HH:MM:SS] video timestamps.
    """
    abs_path = os.path.join(vault_root, rel_path)
    if not os.path.exists(abs_path):
        return [], []

    try:
        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return [], []

    _, _, _, body = split_markdown_note(content)

    # Extract video timestamps like [12:34] or [01:23:45]
    timestamps = re.findall(r'\[([0-9]{1,2}:[0-9]{2}(?::[0-9]{2})?)\]', body)

    # Extract headings and paragraphs
    sections: List[Tuple[str, str]] = []
    current_heading = "Introduzione"
    current_lines: List[str] = []

    for line in body.splitlines():
        if line.startswith(('## ', '### ', '# ')):
            if current_lines:
                sec_content = "\n".join(current_lines).strip()
                if sec_content:
                    sections.append((current_heading, sec_content))
                current_lines = []
            current_heading = line.lstrip('#').strip()
        else:
            current_lines.append(line)
    if current_lines:
        sec_content = "\n".join(current_lines).strip()
        if sec_content:
            sections.append((current_heading, sec_content))

    snippets: List[Dict[str, Any]] = []
    scored_sections: List[Tuple[int, str, str]] = []

    for heading, text in sections:
        sec_tokens = tokenize(text)
        overlap = sum(1 for t in query_tokens if t in sec_tokens)
        scored_sections.append((overlap, heading, text))

    scored_sections.sort(key=lambda x: x[0], reverse=True)
    if scored_sections and scored_sections[0][0] > 0:
        top_overlap, top_heading, top_text = scored_sections[0]
        # Clean whitespace and truncate text snippet to first 300 characters
        snippet_text = " ".join(top_text.split())
        truncated = snippet_text[:300] + ("..." if len(snippet_text) > 300 else "")
        snippets.append({
            "heading": top_heading,
            "text": truncated
        })
    elif sections:
        first_heading, first_text = sections[0]
        snippet_text = " ".join(first_text.split())
        truncated = snippet_text[:300] + ("..." if len(snippet_text) > 300 else "")
        snippets.append({
            "heading": first_heading,
            "text": truncated
        })

    return snippets, timestamps[:3]


def execute_query(
    vault_root: str,
    query: str = "",
    area: Optional[str] = None,
    type_filter: Optional[str] = None,
    tag_filter: Optional[str] = None,
    limit: int = 5,
    similar_to: Optional[str] = None,
    force_reindex: bool = False
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes hybrid search or similarity retrieval with structured filtering and snippet extraction.
    Returns (results, drilldown_suggestions).
    """
    cache_data = load_or_rebuild_cache(vault_root, force_reindex=force_reindex)
    files = cache_data.get("files", {})

    if not files:
        return [], []

    query_tokens = tokenize(query) if query else []
    ranked_candidates: List[Tuple[str, float, Dict[str, int]]] = []

    if similar_to:
        sim_results = find_similar_notes(vault_root, similar_to, cache_data, limit=len(files))
        ranked_candidates = [(rel_path, score, {"dense": idx + 1}) for idx, (rel_path, score) in enumerate(sim_results)]
        if not query_tokens:
            query_tokens = tokenize(similar_to)
    else:
        if not query_tokens:
            return [], []

        # 1. YAML Metadata Ranking
        yaml_scores: List[Tuple[str, float]] = []
        for rel_path, entry in files.items():
            s = score_yaml_metadata(entry, query_tokens)
            if s > 0.0:
                yaml_scores.append((rel_path, s))
        yaml_scores.sort(key=lambda x: x[1], reverse=True)
        yaml_ranks = [rel_path for rel_path, _ in yaml_scores]

        # 2. BM25 Lexical Ranking (D-10)
        doc_lengths = {rel_path: entry.get("doc_len", 0) for rel_path, entry in files.items()}
        term_freqs = {rel_path: entry.get("term_freq", {}) for rel_path, entry in files.items()}
        bm25_index = BM25Index(k1=1.5, b=0.75)
        bm25_index.build_from_term_freqs(doc_lengths, term_freqs)
        bm25_scores = bm25_index.score(query_tokens)
        bm25_ranks = [rel_path for rel_path, _ in bm25_scores]

        # 3. Dense Semantic Track (if query matches a note title)
        dense_ranks: List[str] = []
        cleaned_query = query.strip('[]"\'').lower()
        matching_target = None
        for rel_path, entry in files.items():
            stem = Path(rel_path).stem.lower()
            title = entry.get("title", "").lower()
            if stem == cleaned_query or title == cleaned_query:
                matching_target = rel_path
                break
        if matching_target:
            sim_notes = find_similar_notes(vault_root, matching_target, cache_data, limit=len(files))
            dense_ranks = [rel_path for rel_path, _ in sim_notes]

        # RRF Fusion
        ranked_candidates = reciprocal_rank_fusion(yaml_ranks, bm25_ranks, dense_ranks, k=60)

    if not ranked_candidates:
        return [], []

    # Ambiguity and multi-domain drilldown suggestion generation
    matched_areas: Counter = Counter()
    for rel_path, score, _ in ranked_candidates:
        note_area = files.get(rel_path, {}).get("area", "")
        if note_area:
            matched_areas[note_area.lower()] += 1

    drilldown_suggestions: List[Dict[str, Any]] = []
    if area:
        for a, count in matched_areas.items():
            if a.lower() != area.lower() and count > 0:
                drilldown_suggestions.append({
                    "area": a,
                    "count": count,
                    "hint": f"Trovate corrispondenze anche in {a.capitalize()} ({count}). Usa --area {a} per raffinare."
                })
    elif len(matched_areas) > 1:
        sorted_areas = matched_areas.most_common()
        for a, count in sorted_areas[1:]:
            drilldown_suggestions.append({
                "area": a,
                "count": count,
                "hint": f"Trovate corrispondenze anche in {a.capitalize()} ({count}). Usa --area {a} per raffinare."
            })

    # Apply Structured Filters
    filtered_results: List[Dict[str, Any]] = []
    for rel_path, score, rank_details in ranked_candidates:
        entry = files.get(rel_path, {})
        if not entry:
            continue

        # Area filter
        if area and entry.get("area", "").lower() != area.lower():
            continue

        # Type filter
        if type_filter and entry.get("type", "").lower() != type_filter.lower():
            continue

        # Tag filter (exact or hierarchical prefix)
        if tag_filter:
            note_tags = [t.lower() for t in entry.get("tags", [])]
            tag_query = tag_filter.lower()
            tag_match = any(t == tag_query or t.startswith(tag_query + "/") for t in note_tags)
            if not tag_match:
                continue

        snippets, timestamps = extract_relevant_snippet_and_timestamps(vault_root, rel_path, query_tokens)

        filtered_results.append({
            "title": entry.get("title") or Path(rel_path).stem,
            "path": rel_path,
            "area": entry.get("area", ""),
            "type": entry.get("type", ""),
            "tags": entry.get("tags", []),
            "summary": entry.get("summary", ""),
            "score": round(score, 4),
            "rrf_ranks": rank_details,
            "exact_citation": f"[[{entry.get('title') or Path(rel_path).stem}]]",
            "snippets": snippets,
            "video_timestamps": timestamps,
            "related": entry.get("related", [])
        })

        if len(filtered_results) >= limit:
            break

    return filtered_results, drilldown_suggestions


def format_output(
    results: List[Dict[str, Any]],
    query_str: str,
    output_format: str = 'auto',
    drilldown_suggestions: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Formats search results as JSON, Markdown (3-section contract), or ANSI pretty."""
    if output_format == 'auto':
        output_format = 'pretty' if sys.stdout.isatty() else 'json'

    if not results:
        if output_format == 'json':
            return json.dumps({
                "status": "empty",
                "query": query_str,
                "total_matches": 0,
                "drilldown_suggestions": [],
                "results": [],
                "message": ZERO_MATCH_MESSAGE.format(query=query_str)
            }, ensure_ascii=False, indent=2)
        else:
            return ZERO_MATCH_MESSAGE.format(query=query_str)

    if output_format == 'json':
        payload = {
            "status": "success",
            "query": query_str,
            "total_matches": len(results),
            "drilldown_suggestions": drilldown_suggestions or [],
            "results": results
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    elif output_format == 'markdown':
        # Section 1: Executive Summary synthesis without emoji (D-13, PERF-04)
        summary_bullets = []
        for r in results:
            if r.get('summary'):
                summary_bullets.append(f"- **[[{r['title']}]]**: {r['summary']}")

        exec_text = "\n".join(summary_bullets) if summary_bullets else "- Sintesi dei concetti rilevanti estratti dal Vault."

        # Section 2: Sources & Citations without emoji (D-13, PERF-04)
        sources = []
        for r in results:
            cit = f"- [[{r['title']}]]"
            snippets = r.get('snippets', [])
            if snippets and snippets[0].get('heading'):
                cit += f" (sezione: *{snippets[0]['heading']}*)"
            timestamps = r.get('video_timestamps', [])
            if timestamps:
                cit += f" (timestamp: `[{timestamps[0]}]`)"
            sources.append(cit)
        sources_text = "\n".join(sources)

        # Organic integration of related semantic notes and drill-down hints (D-13, D-16)
        related_set: Set[str] = set()
        result_titles = {r['title'].lower() for r in results}
        for r in results:
            for rel in r.get('related', []):
                if rel:
                    clean_rel = rel.strip('[]').strip()
                    if clean_rel.lower() not in result_titles:
                        related_set.add(f"[[{clean_rel}]]")

        suggested = sorted(list(related_set))[:2]
        if suggested:
            sources_text += f"\n\n*Connessioni semantiche correlate:* {', '.join(suggested)}"

        if drilldown_suggestions:
            drill_hints = " ".join(d['hint'] for d in drilldown_suggestions)
            sources_text += f"\n\n> 💡 **Suggerimento:** {drill_hints}"

        return f"""### Sintesi Esecutiva\n{exec_text}\n\n---\n\n### Fonti & Citazioni\n{sources_text}"""

    else:
        # Pretty interactive terminal output
        lines = [f"\n🔍 Risultati Recall per: \033[1m{query_str}\033[0m\n"]
        for idx, r in enumerate(results, start=1):
            lines.append(f"\033[32m{idx}. [[{r['title']}]]\033[0m (Score: {r['score']:.4f}, Area: {r['area']}, Type: {r['type']})")
            if r.get('summary'):
                lines.append(f"   \033[90m{r['summary']}\033[0m")
            for snip in r.get('snippets', []):
                lines.append(f"   📌 \033[33m{snip['heading']}:\033[0m {snip['text']}")
            if r.get('video_timestamps'):
                lines.append(f"   ⏱️ \033[36mTimestamps:\033[0m {', '.join(r['video_timestamps'])}")
            lines.append("")
        if drilldown_suggestions:
            lines.append("\033[35m💡 Suggerimenti Drill-down:\033[0m")
            for d in drilldown_suggestions:
                lines.append(f"   - {d['hint']}")
            lines.append("")
        return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    """Builds CLI argument parser with structured filters and auto-formatting."""
    parser = argparse.ArgumentParser(
        description="recall_engine.py - Hybrid Retrieval & Conversational Search Engine."
    )
    parser.add_argument('query', nargs='*', help="Search query terms or natural language question.")
    parser.add_argument('--area', choices=sorted(CONTROLLED_AREAS), default=None, help="Filter by macro-area.")
    parser.add_argument('--type', choices=sorted(CONTROLLED_TYPES), default=None, help="Filter by note type.")
    parser.add_argument('--tag', type=str, default=None, help="Filter by hierarchical tag prefix (e.g. tech/ai).")
    parser.add_argument('--limit', type=int, default=5, help="Maximum number of results to return (default: 5).")
    parser.add_argument('--format', choices=['auto', 'json', 'markdown', 'pretty'], default='auto', help="Output format.")
    parser.add_argument('--similar-to', type=str, default=None, help="Note title to find semantic neighbors via 384-d vectors.")
    parser.add_argument('--reindex', action='store_true', help="Force full index rebuild.")
    parser.add_argument('--vault-root', type=str, default=None, help="Custom vault root directory.")
    return parser


def main(cli_args: Optional[List[str]] = None) -> int:
    """Main CLI entrypoint."""
    parser = build_arg_parser()
    args = parser.parse_args(cli_args)

    query_str = " ".join(args.query).strip() if args.query else ""
    if not query_str and not args.similar_to and not args.reindex:
        parser.print_help()
        return 1

    vault_root = get_vault_root(args.vault_root)
    if not os.path.isdir(vault_root):
        sys.stderr.write(f"Error: Vault root '{vault_root}' is not a valid directory.\n")
        return 1

    if args.reindex:
        load_or_rebuild_cache(vault_root, force_reindex=True)
        if not query_str and not args.similar_to:
            print("Index rebuild completed successfully.")
            return 0

    results, drilldowns = execute_query(
        vault_root=vault_root,
        query=query_str,
        area=args.area,
        type_filter=args.type,
        tag_filter=args.tag,
        limit=args.limit,
        similar_to=args.similar_to,
        force_reindex=False
    )

    display_query = args.similar_to if args.similar_to else query_str
    output = format_output(results, display_query, args.format, drilldowns)
    print(output)
    return 0


if __name__ == '__main__':
    sys.exit(main())
