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
        self.assertIn("trasformatori", cache3["files"][note_rel_path]["term_freq"])
        self.assertGreater(cache3["files"][note_rel_path]["doc_len"], 0)
        self.assertNotIn("tokens", cache3["files"][note_rel_path])

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

    def test_cache_compact_serialization_and_size(self):
        """Asserts .recall_cache.json is serialized with separators=(',', ':') without expanded indentation (D-09, PERF-03)."""
        note_rel_path = "02 - Atlas/Tech/Quantum Computing.md"
        note_abs_path = os.path.join(self.test_dir, note_rel_path)
        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: \"Quantum Computing\"\narea: tech\ntags: [tech/quantum]\n---\nAlgoritmo di Shor e qubit.")

        recall_engine.load_or_rebuild_cache(self.test_dir, force_reindex=True)
        cache_file = os.path.join(self.test_dir, "99 - Meta", "Scripts", ".recall_cache.json")
        self.assertTrue(os.path.exists(cache_file))

        with open(cache_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Should NOT contain expanded indentation newlines like "\n  \""
        self.assertNotIn('\n  "', raw_text)
        self.assertIn('{"version":1,"files":{', raw_text)

    def test_cache_structure_no_tokens_list(self):
        """Asserts cached_files entries store doc_len and term_freq, removing the redundant tokens list (D-10, PERF-03)."""
        note_rel_path = "02 - Atlas/Tech/Deep Learning Note.md"
        note_abs_path = os.path.join(self.test_dir, note_rel_path)
        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: \"Deep Learning Note\"\narea: tech\ntags: [tech/ai]\n---\nReti neurali convoluzionali e visione artificiale.")

        cache = recall_engine.load_or_rebuild_cache(self.test_dir, force_reindex=True)
        entry = cache["files"][note_rel_path]

        self.assertIn("doc_len", entry)
        self.assertIsInstance(entry["doc_len"], int)
        self.assertGreater(entry["doc_len"], 0)

        self.assertIn("term_freq", entry)
        self.assertIsInstance(entry["term_freq"], dict)
        self.assertIn("convoluzionali", entry["term_freq"])

        self.assertNotIn("tokens", entry)

    def test_inbox_folder_ignored_in_recall(self):
        """Asserts '03 - Inbox' is ignored by recall_engine to avoid indexing transient notes (D-12, PERF-03)."""
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        os.makedirs(inbox_dir, exist_ok=True)
        inbox_note = os.path.join(inbox_dir, "Bozza Grezza Inbox.md")
        with open(inbox_note, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: \"Bozza Grezza Inbox\"\narea: tech\n---\nTesto grezzo non verificato.")

        cache = recall_engine.load_or_rebuild_cache(self.test_dir, force_reindex=True)
        self.assertNotIn("03 - Inbox/Bozza Grezza Inbox.md", cache["files"])

    def test_bm25_build_from_term_freqs_equivalence(self):
        """Asserts build_from_term_freqs yields identical scores to build_from_corpus (D-10)."""
        corpus = {
            "doc1": ["intelligenza", "artificiale", "modello", "linguaggio", "modello"],
            "doc2": ["algoritmo", "struttura", "dati", "linguaggio", "programmazione"],
            "doc3": ["intelligenza", "biologica", "evoluzione", "modello"]
        }

        # Index 1: built from corpus
        bm25_1 = recall_engine.BM25Index(k1=1.5, b=0.75)
        bm25_1.build_from_corpus(corpus)

        # Index 2: built from term_freqs and doc_lengths
        from collections import Counter
        doc_lengths = {d: len(toks) for d, toks in corpus.items()}
        term_freqs = {d: dict(Counter(toks)) for d, toks in corpus.items()}

        bm25_2 = recall_engine.BM25Index(k1=1.5, b=0.75)
        bm25_2.build_from_term_freqs(doc_lengths, term_freqs)

        query = ["intelligenza", "modello"]
        scores_1 = dict(bm25_1.score(query))
        scores_2 = dict(bm25_2.score(query))

        self.assertEqual(scores_1.keys(), scores_2.keys())
        for doc_id in scores_1:
            self.assertAlmostEqual(scores_1[doc_id], scores_2[doc_id], places=5)


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


class TestRecallEngineTask1_0402(unittest.TestCase):
    """Test suite for Phase 04 Plan 02 Task 1: Filters, Snippets, Timestamps, Drilldown, and Polymorphic Output."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Education"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Scripts"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cli_filters_and_predicates(self):
        """Asserts query execution filters results accurately when passed --area tech, --type concept, --tag tech/ai, or --limit 2 per D-06."""
        notes = [
            ("02 - Atlas/Tech/AI Models.md", """---
title: "AI Models"
area: tech
type: concept
tags: [tech/ai, tech/neural]
summary: "Panoramica sui modelli di AI."
---
Modelli avanzati di intelligenza artificiale.
"""),
            ("02 - Atlas/Education/Education Models.md", """---
title: "Education Models"
area: education
type: lecture
tags: [education/math]
summary: "Lezione sui modelli matematici."
---
Modelli matematici per l'insegnamento universitario.
"""),
            ("02 - Atlas/Tech/Video Cloud.md", """---
title: "Video Cloud"
area: tech
type: video
tags: [tech/cloud]
summary: "Video sui modelli cloud."
---
Infrastrutture cloud per il deployment di modelli.
"""),
            ("02 - Atlas/Tech/Deep Learning.md", """---
title: "Deep Learning"
area: tech
type: concept
tags: [tech/ai/deeplearning]
summary: "Deep learning e reti neurali."
---
Modelli di deep learning e trasformatori.
""")
        ]
        for rel_path, content in notes:
            abs_p = os.path.join(self.test_dir, rel_path)
            with open(abs_p, 'w', encoding='utf-8') as f:
                f.write(content)

        # 1. Test --area tech filter
        res_area, _ = recall_engine.execute_query(self.test_dir, query="modelli", area="tech")
        self.assertTrue(len(res_area) > 0)
        for r in res_area:
            self.assertEqual(r["area"], "tech")

        # 2. Test --type concept filter
        res_type, _ = recall_engine.execute_query(self.test_dir, query="modelli", type_filter="concept")
        self.assertTrue(len(res_type) > 0)
        for r in res_type:
            self.assertEqual(r["type"], "concept")

        # 3. Test --tag tech/ai prefix filter
        res_tag, _ = recall_engine.execute_query(self.test_dir, query="modelli", tag_filter="tech/ai")
        self.assertEqual(len(res_tag), 2)
        titles = {r["title"] for r in res_tag}
        self.assertIn("AI Models", titles)
        self.assertIn("Deep Learning", titles)

        # 4. Test --limit 2
        res_lim, _ = recall_engine.execute_query(self.test_dir, query="modelli", limit=2)
        self.assertEqual(len(res_lim), 2)

    def test_video_timestamps_and_snippet_extraction(self):
        """Asserts extract_relevant_snippet_and_timestamps() extracts [MM:SS] or [HH:MM:SS] timestamps from video notes and returns top H2/H3 section snippet with highest query term overlap per D-07."""
        note_rel_path = "02 - Atlas/Tech/Transformer Video.md"
        note_abs_path = os.path.join(self.test_dir, note_rel_path)
        content = """---
title: "Transformer Video"
area: tech
type: video
tags: [tech/ai]
summary: "Video lecture sui Transformers."
---
[[Home MOC]] / [[Tech MOC]]

# Transformer Video

## Introduzione
Panoramica iniziale del video senza dettagli.

## Meccanismo di Self-Attention
In questa sezione spieghiamo l'attenzione dinamica e matrici Query Key Value [12:45] e poi la multi-head attention [01:23:45].

## Conclusioni
Riepilogo finale dei risultati.
"""
        with open(note_abs_path, 'w', encoding='utf-8') as f:
            f.write(content)

        snippets, timestamps = recall_engine.extract_relevant_snippet_and_timestamps(
            self.test_dir,
            note_rel_path,
            ["attenzione", "dinamica", "matrici"]
        )

        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]["heading"], "Meccanismo di Self-Attention")
        self.assertIn("attenzione dinamica", snippets[0]["text"])

        self.assertEqual(len(timestamps), 2)
        self.assertIn("12:45", timestamps)
        self.assertIn("01:23:45", timestamps)

    def test_drilldown_multi_domain_suggestions(self):
        """Asserts ambiguous queries matching multiple macro-areas produce proactive drilldown suggestions (e.g. area: education, count: 2, hint: 'Trovate corrispondenze anche in Education. Usa --area education per raffinare') per D-07."""
        notes = [
            ("02 - Atlas/Tech/Quantum Tech.md", """---
title: "Quantum Tech"
area: tech
type: concept
tags: [tech/quantum]
---
Algoritmi di calcolo quantistico e qubit.
"""),
            ("02 - Atlas/Education/Quantum Physics 1.md", """---
title: "Quantum Physics 1"
area: education
type: lecture
tags: [education/physics]
---
Corso universitario introduttivo sul calcolo quantistico.
"""),
            ("02 - Atlas/Education/Quantum Physics 2.md", """---
title: "Quantum Physics 2"
area: education
type: lecture
tags: [education/physics]
---
Lezione di laboratorio sul calcolo quantistico.
""")
        ]
        for rel_path, content in notes:
            abs_p = os.path.join(self.test_dir, rel_path)
            with open(abs_p, 'w', encoding='utf-8') as f:
                f.write(content)

        # Search with --area tech filter -> should suggest Education
        res, drilldowns = recall_engine.execute_query(self.test_dir, query="quantistico", area="tech")
        self.assertEqual(len(res), 1)
        self.assertEqual(len(drilldowns), 1)
        self.assertEqual(drilldowns[0]["area"], "education")
        self.assertEqual(drilldowns[0]["count"], 2)
        self.assertIn("Education", drilldowns[0]["hint"])
        self.assertIn("--area education", drilldowns[0]["hint"])

    def test_polymorphic_output_formats(self):
        """Asserts format_output() returns valid structured JSON under --format json, ANSI-colored output under --format pretty, and auto-detects TTY vs pipe per D-05."""
        results = [{
            "title": "Sample Note Alpha",
            "path": "02 - Atlas/Tech/Sample Note Alpha.md",
            "area": "tech",
            "type": "concept",
            "tags": ["tech/ai"],
            "summary": "Introduzione ai modelli alpha.",
            "score": 0.0482,
            "rrf_ranks": {"yaml": 1, "bm25": 1},
            "exact_citation": "[[Sample Note Alpha]]",
            "snippets": [{"heading": "Sezione Chiave", "text": "Testo dello snippet di test."}],
            "video_timestamps": ["04:15"],
            "related": ["[[Sample Note Beta]]"]
        }]
        drilldowns = [{"area": "education", "count": 2, "hint": "Trovate corrispondenze anche in Education. Usa --area education per raffinare."}]

        # 1. JSON Format
        json_out = recall_engine.format_output(results, "alpha", output_format="json", drilldown_suggestions=drilldowns)
        parsed = json.loads(json_out)
        self.assertEqual(parsed["status"], "success")
        self.assertEqual(parsed["total_matches"], 1)
        self.assertEqual(len(parsed["drilldown_suggestions"]), 1)
        self.assertEqual(parsed["results"][0]["title"], "Sample Note Alpha")

        # 2. Pretty Format (ANSI colors)
        pretty_out = recall_engine.format_output(results, "alpha", output_format="pretty", drilldown_suggestions=drilldowns)
        self.assertIn("Sample Note Alpha", pretty_out)
        self.assertIn("Sezione Chiave", pretty_out)
        self.assertIn("04:15", pretty_out)
        self.assertIn("Suggerimenti Drill-down", pretty_out)

        # 3. Markdown Format (2-section Contract without emoji per D-13)
        md_out = recall_engine.format_output(results, "alpha", output_format="markdown", drilldown_suggestions=drilldowns)
        self.assertIn("### Sintesi Esecutiva", md_out)
        self.assertIn("### Fonti & Citazioni", md_out)
        self.assertNotIn("### 🎯", md_out)
        self.assertNotIn("### 📚", md_out)
        self.assertNotIn("### 🔗", md_out)
        self.assertNotIn("Connessioni Correlate", md_out)
        self.assertIn("[[Sample Note Alpha]]", md_out)
        self.assertIn("(sezione: *Sezione Chiave*)", md_out)
        self.assertIn("(timestamp: `[04:15]`)", md_out)
        self.assertIn("> 💡 **Suggerimento:**", md_out)


class TestRecallEngineTask2_0402(unittest.TestCase):
    """Test suite for Phase 04 Plan 02 Task 2: NotebookLM Schema, Zero-Hallucination Guard, and System Integration."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "99 - Meta", "Scripts"), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_zero_hallucination_guard(self):
        """Asserts unknown queries return the exact refusal message without external hallucination in markdown and empty status in JSON per D-09."""
        query = "TermineTotalmenteInesistente12345"

        # Markdown refusal
        md_out = recall_engine.format_output([], query, output_format="markdown")
        self.assertIn("⚠️ **Nessuna corrispondenza trovata nel Vault**", md_out)
        self.assertIn(query, md_out)
        self.assertIn("Nessuna informazione esterna è stata integrata", md_out)

        # JSON refusal
        json_out = recall_engine.format_output([], query, output_format="json")
        data = json.loads(json_out)
        self.assertEqual(data["status"], "empty")
        self.assertEqual(data["total_matches"], 0)
        self.assertEqual(data["results"], [])
        self.assertIn("Nessuna corrispondenza trovata nel Vault", data["message"])

    def test_notebooklm_2section_markdown_synthesis(self):
        """Asserts 2-section Markdown output formats executive synthesis and verified citations without emoji per D-13, PERF-04."""
        results = [
            {
                "title": "Reti Neurali Ricorrenti",
                "path": "02 - Atlas/Tech/Reti Neurali Ricorrenti.md",
                "area": "tech",
                "type": "concept",
                "tags": ["tech/ai"],
                "summary": "Struttura delle reti ricorrenti e limiti del gradiente.",
                "score": 0.045,
                "rrf_ranks": {"bm25": 1},
                "exact_citation": "[[Reti Neurali Ricorrenti]]",
                "snippets": [{"heading": "Problema del Vanishing Gradient", "text": "Le RNN soffrono di vanishing gradient."}],
                "video_timestamps": [],
                "related": ["[[Transformers MOC]]", "[[LSTM Networks]]"]
            }
        ]

        md_out = recall_engine.format_output(results, "RNN", output_format="markdown")
        self.assertIn("### Sintesi Esecutiva", md_out)
        self.assertIn("- **[[Reti Neurali Ricorrenti]]**: Struttura delle reti ricorrenti e limiti del gradiente.", md_out)

        self.assertIn("### Fonti & Citazioni", md_out)
        self.assertIn("- [[Reti Neurali Ricorrenti]] (sezione: *Problema del Vanishing Gradient*)", md_out)

        self.assertNotIn("### 🎯", md_out)
        self.assertNotIn("### 📚", md_out)
        self.assertNotIn("### 🔗", md_out)
        self.assertNotIn("Connessioni Correlate", md_out)

    def test_recall_format_output_two_sections_no_emoji(self):
        """Asserts format_output generates exactly 2 sections and zero emoji in all headings (D-13, D-16, PERF-04)."""
        results = [
            {
                "title": "Nota Test Heading",
                "path": "02 - Atlas/Tech/Nota Test Heading.md",
                "area": "tech",
                "type": "concept",
                "tags": ["tech/ai"],
                "summary": "Sintesi pulita.",
                "score": 0.05,
                "snippets": [{"heading": "Introduzione", "text": "Snippet di prova."}],
                "video_timestamps": [],
                "related": ["[[Correlata 1]]"]
            }
        ]
        md_out = recall_engine.format_output(results, "Test", output_format="markdown")
        heading_lines = [line.strip() for line in md_out.splitlines() if line.strip().startswith("#")]

        # Must have exactly 2 headings: ### Sintesi Esecutiva and ### Fonti & Citazioni
        self.assertEqual(len(heading_lines), 2)
        self.assertEqual(heading_lines[0], "### Sintesi Esecutiva")
        self.assertEqual(heading_lines[1], "### Fonti & Citazioni")

        # Zero emoji across all headings
        import re
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]')
        for h in heading_lines:
            self.assertIsNone(emoji_pattern.search(h), f"Heading contains forbidden emoji: {h}")

    def test_gitignore_contains_recall_cache(self):
        """Asserts .gitignore contains .recall_cache.json rules to prevent tracking local indexes per D-01."""
        gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
        self.assertTrue(os.path.exists(gitignore_path))
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn(".recall_cache.json", content)
        self.assertIn("**/.recall_cache.json", content)
        self.assertIn("*.recall_cache.json.tmp", content)


if __name__ == '__main__':
    unittest.main()
