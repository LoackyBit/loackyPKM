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
    'node_modules', 'tests', '.planning'
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

    def build_from_corpus(self, corpus: Dict[str, List[str]]):
        """Builds inverted index and term frequencies from tokenized document corpus."""
        self.total_docs = len(corpus)
        self.doc_lengths.clear()
        self.term_freqs.clear()
        self.doc_freqs.clear()
        if self.total_docs == 0:
            self.avg_doc_len = 0.0
            return
        total_len = 0
        for doc_id, tokens in corpus.items():
            doc_len = len(tokens)
            self.doc_lengths[doc_id] = doc_len
            total_len += doc_len
            tf = Counter(tokens)
            self.term_freqs[doc_id] = dict(tf)
            for term in tf.keys():
                self.doc_freqs[term] += 1
        self.avg_doc_len = total_len / self.total_docs if self.total_docs > 0 else 0.0

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
                    "tokens": tokens,
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
        # Atomic write via temporary file
        tmp_path = cache_path + ".tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, cache_path)

    return cache_data
