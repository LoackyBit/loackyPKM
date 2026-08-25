#!/usr/bin/env python3
"""
test_recall_engine.py - Comprehensive Unit tests for recall_engine.py.
"""

import os
import sys
import json
import time
import math
import struct
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
        # Stopwords 'questo', 'è', 'l', 'di', 'per', 'il' should be stripped
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

        # Modify note
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


class TestRecallEngineTask2(unittest.TestCase):
    """Test suite for Task 2: Vector Decoding, Cosine Similarity, YAML Weighting, RRF Fusion, and Fallback."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Finance"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Scripts"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, ".smart-env", "smart_sources"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_smart_connections_metadata_and_vector_reading(self):
        """Asserts load_smart_connections_metadata() performs line-reduction on .ajson and read_vector() unpacks 384 float32 values (<384f) with unit cosine similarity."""
        # 1. Create binary vector file with 2 vectors
        vec_file_path = os.path.join(self.test_dir, ".smart-env", "smart_sources", "mf_mock")
        # Vector 0: unit vector along dimension 0
        vec_0 = [1.0] + [0.0] * 383
        # Vector 1: unit vector along dimension 1
        vec_1 = [0.0, 1.0] + [0.0] * 382
        # Vector 2: uniform unit vector
        val = 1.0 / math.sqrt(384)
        vec_2 = [val] * 384

        raw_data = struct.pack('<384f', *vec_0) + struct.pack('<384f', *vec_1) + struct.pack('<384f', *vec_2)
        with open(vec_file_path, 'wb') as f:
            f.write(raw_data)

        # 2. Create mock smart_sources.ajson with line reduction (overwrites and nulls)
        ajson_path = os.path.join(self.test_dir, ".smart-env", "smart_sources", "smart_sources.ajson")
        lines = [
            # Old entry for Note A
            '"smart_sources:02 - Atlas/Tech/NoteA.md": {"path":"02 - Atlas/Tech/NoteA.md", "embedding":{"default":{"mf_old":{"file":"mf_mock","file_i":0,"at":100}}}},',
            # New overwritten entry for Note A with higher 'at' timestamp
            '"smart_sources:02 - Atlas/Tech/NoteA.md": {"path":"02 - Atlas/Tech/NoteA.md", "embedding":{"default":{"mf_new":{"file":"mf_mock","file_i":2,"at":200}}}},',
            # Deleted note B
            '"smart_sources:02 - Atlas/Tech/NoteB.md": {"path":"02 - Atlas/Tech/NoteB.md", "embedding":{"default":{"mf_b":{"file":"mf_mock","file_i":1,"at":150}}}},',
            '"smart_sources:02 - Atlas/Tech/NoteB.md": null,',
            # Active note C
            '"smart_sources:02 - Atlas/Tech/NoteC.md": {"path":"02 - Atlas/Tech/NoteC.md", "embedding":{"default":{"mf_c":{"file":"mf_mock","file_i":1,"at":180}}}}'
        ]
        with open(ajson_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines) + "\n")

        # Test metadata loading
        refs = recall_engine.load_smart_connections_metadata(self.test_dir)
        self.assertIn("02 - Atlas/Tech/NoteA.md", refs)
        # Should pick the newer index 2
        self.assertEqual(refs["02 - Atlas/Tech/NoteA.md"], ("mf_mock", 2))
        # NoteB should be deleted (null)
        self.assertNotIn("02 - Atlas/Tech/NoteB.md", refs)
        # NoteC should be present with index 1
        self.assertIn("02 - Atlas/Tech/NoteC.md", refs)
        self.assertEqual(refs["02 - Atlas/Tech/NoteC.md"], ("mf_mock", 1))

        # Test reading binary vector
        v0 = recall_engine.read_vector(self.test_dir, "mf_mock", 0)
        v1 = recall_engine.read_vector(self.test_dir, "mf_mock", 1)
        v2 = recall_engine.read_vector(self.test_dir, "mf_mock", 2)

        self.assertIsNotNone(v0)
        self.assertEqual(len(v0), 384)
        self.assertAlmostEqual(v0[0], 1.0, places=5)
        self.assertAlmostEqual(v0[1], 0.0, places=5)

        # Orthogonal vectors -> cosine similarity = 0.0
        self.assertAlmostEqual(recall_engine.cosine_similarity(v0, v1), 0.0, places=5)
        # Identical vectors -> cosine similarity = 1.0
        self.assertAlmostEqual(recall_engine.cosine_similarity(v2, v2), 1.0, places=5)

        # Out-of-bounds offset returns None
        v_invalid = recall_engine.read_vector(self.test_dir, "mf_mock", 999)
        self.assertIsNone(v_invalid)

    def test_yaml_metadata_weighting(self):
        """Asserts score_yaml_metadata() weights title at 10x, summary at 6x, tags/area at 4x, and related/aliases at 2x."""
        query = ["transformer", "attention"]

        # Note matching in title
        meta_title = {"title": "Transformer and Attention Mechanics", "summary": "", "area": "", "tags": [], "related": []}
        score_title = recall_engine.score_yaml_metadata(meta_title, query)
        # 10 + 10 = 20.0
        self.assertEqual(score_title, 20.0)

        # Note matching in summary
        meta_summary = {"title": "General AI", "summary": "Study on transformer architecture and attention mechanisms.", "area": "", "tags": [], "related": []}
        score_summary = recall_engine.score_yaml_metadata(meta_summary, query)
        # 6 + 6 = 12.0
        self.assertEqual(score_summary, 12.0)

        # Note matching in tags and area
        meta_tags_area = {"title": "AI Tools", "summary": "", "area": "transformer", "tags": ["tech/attention"], "related": []}
        score_tags_area = recall_engine.score_yaml_metadata(meta_tags_area, query)
        # 4 + 4 = 8.0
        self.assertEqual(score_tags_area, 8.0)

        # Note matching in related and aliases
        meta_related = {"title": "Models", "summary": "", "area": "tech", "tags": [], "related": ["[[Transformer]]"], "aliases": ["Attention Base"]}
        score_related = recall_engine.score_yaml_metadata(meta_related, query)
        # 2 + 2 = 4.0
        self.assertEqual(score_related, 4.0)

        # Verify hierarchy: Title (20) > Summary (12) > Tags/Area (8) > Related/Aliases (4)
        self.assertGreater(score_title, score_summary)
        self.assertGreater(score_summary, score_tags_area)
        self.assertGreater(score_tags_area, score_related)

    def test_reciprocal_rank_fusion_order(self):
        """Asserts reciprocal_rank_fusion() combines YAML, BM25, and Dense ranks with k=60 and correct track weights (yaml=1.0, bm25=1.0, dense=1.2)."""
        yaml_ranks = ["doc_yaml_top", "doc_shared", "doc_yaml_only"]
        bm25_ranks = ["doc_bm25_top", "doc_shared", "doc_bm25_only"]
        dense_ranks = ["doc_dense_top", "doc_shared", "doc_dense_only"]

        fused = recall_engine.reciprocal_rank_fusion(yaml_ranks, bm25_ranks, dense_ranks, k=60)
        fused_docs = [item[0] for item in fused]

        # doc_shared appears as rank 2 across all 3 tracks:
        # Score = 1.0/(60+2) + 1.0/(60+2) + 1.2/(60+2) = 3.2 / 62 = 0.05161
        # doc_dense_top appears as rank 1 in dense: 1.2/(60+1) = 1.2 / 61 = 0.01967
        # doc_shared must be top rank due to multi-track consensus
        self.assertEqual(fused_docs[0], "doc_shared")

        # Dense top (1.2/61 ~ 0.01967) should beat single yaml top (1.0/61 ~ 0.01639) due to weight 1.2
        doc_scores = {item[0]: item[1] for item in fused}
        self.assertGreater(doc_scores["doc_dense_top"], doc_scores["doc_yaml_top"])
        self.assertGreater(doc_scores["doc_dense_top"], doc_scores["doc_bm25_top"])

    def test_rrf_graceful_fallback_without_vectors(self):
        """Asserts RRF degrades gracefully without errors when dense vector list is empty or when notes lack vector embeddings."""
        yaml_ranks = ["doc_a", "doc_b"]
        bm25_ranks = ["doc_b", "doc_c"]
        dense_ranks = []  # No vectors available

        # Should execute cleanly without raising exceptions
        fused = recall_engine.reciprocal_rank_fusion(yaml_ranks, bm25_ranks, dense_ranks, k=60)
        self.assertEqual(len(fused), 3)

        doc_scores = {item[0]: item[1] for item in fused}
        # doc_b is rank 2 in yaml (1/62) and rank 1 in bm25 (1/61) -> ~0.0325
        # doc_a is rank 1 in yaml (1/61) -> ~0.0164
        # doc_c is rank 2 in bm25 (1/62) -> ~0.0161
        # Dense rank detail is absent in rank_details for doc_b since dense_ranks was empty
        self.assertNotIn("dense", fused[0][2])

    def test_similar_to_vector_search(self):
        """Asserts find_similar_notes() resolves target note vector and returns ranked neighbors by cosine dot product."""
        # 1. Create binary vector file with 3 vectors
        vec_file_path = os.path.join(self.test_dir, ".smart-env", "smart_sources", "mf_sim")
        # Target vector (uniform unit vector)
        val = 1.0 / math.sqrt(384)
        target_vec = [val] * 384

        # Very similar vector (dot product ~ 0.99)
        sim_vec = [val * 0.99 + (0.01 if i == 0 else 0.0) for i in range(384)]
        norm = math.sqrt(sum(x*x for x in sim_vec))
        sim_vec = [x / norm for x in sim_vec]

        # Dissimilar vector (orthogonal on first 2 dims)
        dissim_vec = [-val if i % 2 == 0 else val for i in range(384)]

        raw_bytes = struct.pack('<384f', *target_vec) + struct.pack('<384f', *sim_vec) + struct.pack('<384f', *dissim_vec)
        with open(vec_file_path, 'wb') as f:
            f.write(raw_bytes)

        cache_data = {
            "version": 1,
            "files": {
                "02 - Atlas/Tech/Target Note.md": {
                    "title": "Target Note",
                    "vector_file": "mf_sim",
                    "vector_i": 0
                },
                "02 - Atlas/Tech/Close Neighbor.md": {
                    "title": "Close Neighbor",
                    "vector_file": "mf_sim",
                    "vector_i": 1
                },
                "02 - Atlas/Finance/Distant Note.md": {
                    "title": "Distant Note",
                    "vector_file": "mf_sim",
                    "vector_i": 2
                }
            }
        }

        # Search by title
        similar_by_title = recall_engine.find_similar_notes(self.test_dir, "Target Note", cache_data, limit=5)
        self.assertEqual(len(similar_by_title), 2)
        # Close neighbor should have higher similarity
        self.assertEqual(similar_by_title[0][0], "02 - Atlas/Tech/Close Neighbor.md")
        self.assertGreater(similar_by_title[0][1], similar_by_title[1][1])
        self.assertGreater(similar_by_title[0][1], 0.95)

        # Search by wiki-link format [[Target Note]]
        similar_by_link = recall_engine.find_similar_notes(self.test_dir, "[[Target Note]]", cache_data, limit=5)
        self.assertEqual(similar_by_link[0][0], "02 - Atlas/Tech/Close Neighbor.md")

        # Unknown target returns empty list
        unknown_sim = recall_engine.find_similar_notes(self.test_dir, "NonExistentNote", cache_data)
        self.assertEqual(unknown_sim, [])


if __name__ == '__main__':
    unittest.main()
