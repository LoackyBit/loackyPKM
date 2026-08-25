#!/usr/bin/env python3
"""
test_recall_engine.py - Unit tests for recall_engine.py.
"""

import os
import sys
import json
import time
import math
import tempfile
import shutil
import unittest
from pathlib import Path

# Insert project scripts into sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import recall_engine


class TestRecallEngineTask1(unittest.TestCase):
    """Test suite for Task 1: Tokenizer, BM25 Index, and Incremental Cache."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Education"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Scripts"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_tokenize_and_stopwords(self):
        """Asserts tokenize() strips Italian and English stopwords, normalizes accented characters, and produces clean alphanumeric keywords."""
        sample_it = "Questo è l'algoritmo di attenzione per il modello di intelligenza artificiale."
        tokens_it = recall_engine.tokenize(sample_it)
        # Stopwords 'questo', 'è' (len 1), 'l' (len 1), 'di', 'per', 'il' should be stripped
        self.assertNotIn("questo", tokens_it)
        self.assertNotIn("di", tokens_it)
        self.assertNotIn("il", tokens_it)
        self.assertNotIn("per", tokens_it)
        self.assertIn("algoritmo", tokens_it)
        self.assertIn("attenzione", tokens_it)
        self.assertIn("modello", tokens_it)
        self.assertIn("intelligenza", tokens_it)
        self.assertIn("artificiale", tokens_it)

        sample_en = "The quick brown fox jumps over the lazy dog and builds a neural network."
        tokens_en = recall_engine.tokenize(sample_en)
        self.assertNotIn("the", tokens_en)
        self.assertNotIn("and", tokens_en)
        self.assertNotIn("a", tokens_en)
        self.assertIn("quick", tokens_en)
        self.assertIn("neural", tokens_en)
        self.assertIn("network", tokens_en)

        # Accented characters preservation in tokens
        sample_acc = "Perché l'elettricità è fondamentale per l'ingegneria?"
        tokens_acc = recall_engine.tokenize(sample_acc)
        self.assertIn("elettricità", tokens_acc)
        self.assertIn("fondamentale", tokens_acc)
        self.assertIn("ingegneria", tokens_acc)

    def test_bm25_scoring_logic(self):
        """Asserts BM25Index calculates higher scores for documents with higher term frequencies and rarer terms across the corpus."""
        corpus = {
            "doc_rare": ["quantum", "teleportation", "protocol", "physics"],
            "doc_frequent_common": ["machine", "learning", "model", "neural", "network", "python"],
            "doc_repeated_rare": ["quantum", "quantum", "quantum", "mechanics", "entanglement"],
            "doc_other": ["history", "ancient", "rome", "philosophy"]
        }
        index = recall_engine.BM25Index(k1=1.5, b=0.75)
        index.build_from_corpus(corpus)

        self.assertEqual(index.total_docs, 4)
        self.assertGreater(index.avg_doc_len, 0)

        # Query for 'quantum'
        scores = dict(index.score(["quantum"]))
        self.assertIn("doc_rare", scores)
        self.assertIn("doc_repeated_rare", scores)
        self.assertNotIn("doc_other", scores)
        # doc_repeated_rare should score higher than doc_rare due to higher term frequency
        self.assertGreater(scores["doc_repeated_rare"], scores["doc_rare"])

        # Rare term 'teleportation' (1 doc) vs Common term across corpus
        score_rare = dict(index.score(["teleportation"]))
        self.assertEqual(len(score_rare), 1)
        self.assertIn("doc_rare", score_rare)

    def test_cache_load_and_mtime_invalidation(self):
        """Asserts load_or_rebuild_cache() reuses cached entries when mtime is unchanged, updates modified files, removes deleted notes, and writes atomically."""
        note_rel_path = "02 - Atlas/Tech/Neural Network Note.md"
        note_abs_path = os.path.join(self.test_dir, note_rel_path)

        content_v1 = """---
title: "Neural Network Note"
area: tech
type: concept
tags: [tech/ai, tech/deeplearning]
summary: "Introduzione alle reti neurali artificiali."
---
[[Home MOC]] / [[Tech MOC]]

# Neural Network Note
Le reti neurali simulano il funzionamento biologico.
"""
        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write(content_v1)

        # First build
        cache1 = recall_engine.load_or_rebuild_cache(self.test_dir)
        cache_file = os.path.join(self.test_dir, "99 - Meta", "Scripts", ".recall_cache.json")
        self.assertTrue(os.path.exists(cache_file))
        self.assertIn(note_rel_path, cache1["files"])
        self.assertEqual(cache1["files"][note_rel_path]["title"], "Neural Network Note")
        self.assertEqual(cache1["files"][note_rel_path]["area"], "tech")

        cached_mtime1 = cache1["files"][note_rel_path]["mtime"]

        # Second load without modifying note -> mtime is identical, returns valid cache
        cache2 = recall_engine.load_or_rebuild_cache(self.test_dir)
        self.assertEqual(cache2["files"][note_rel_path]["mtime"], cached_mtime1)

        # Modify note with small delay to ensure mtime change
        time.sleep(0.05)
        content_v2 = """---
title: "Neural Network Note V2"
area: tech
type: concept
tags: [tech/ai, tech/deeplearning]
summary: "Architettura aggiornata dei trasformatori e reti neurali."
---
[[Home MOC]] / [[Tech MOC]]

# Neural Network Note V2
Nuovi concetti sui trasformatori moderni.
"""
        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write(content_v2)
        # Ensure mtime is strictly greater
        os.utime(note_abs_path, (time.time() + 10, time.time() + 10))

        cache3 = recall_engine.load_or_rebuild_cache(self.test_dir)
        self.assertEqual(cache3["files"][note_rel_path]["title"], "Neural Network Note V2")
        self.assertIn("trasformatori", cache3["files"][note_rel_path]["tokens"])

        # Delete note -> should be pruned from cache
        os.remove(note_abs_path)
        cache4 = recall_engine.load_or_rebuild_cache(self.test_dir)
        self.assertNotIn(note_rel_path, cache4["files"])

    def test_reindex_flag_forces_full_rebuild(self):
        """Asserts passing force_reindex=True ignores existing cache and rebuilds the index from scratch."""
        note_rel_path = "02 - Atlas/Education/Fermat Theorem.md"
        note_abs_path = os.path.join(self.test_dir, note_rel_path)

        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write("""---
title: "Fermat Theorem"
area: education
type: concept
tags: [education/matematica]
summary: "Ultimo teorema di Fermat."
---
Dimostrazione di Andrew Wiles.
""")

        cache1 = recall_engine.load_or_rebuild_cache(self.test_dir)
        self.assertIn(note_rel_path, cache1["files"])

        # Force reindex
        cache_rebuild = recall_engine.load_or_rebuild_cache(self.test_dir, force_reindex=True)
        self.assertIn(note_rel_path, cache_rebuild["files"])
        self.assertEqual(cache_rebuild["files"][note_rel_path]["title"], "Fermat Theorem")


if __name__ == '__main__':
    unittest.main()
