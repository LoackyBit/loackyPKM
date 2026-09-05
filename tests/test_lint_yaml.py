import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_health as lint_yaml

class TestLintYaml(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fixtures_dir = os.path.join(PROJECT_ROOT, "tests", "fixtures")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_schema_canonical_order(self):
        """Asserts frontmatter keys follow exact sequence per D-16:
        status (or stage+draft) -> type -> area -> related -> aliases (if present) -> source -> title -> date -> updated -> tags -> summary
        """
        meta = {
            "status": "permanent",
            "type": "concept",
            "area": "tech",
            "related": ["[[Architetture LLM]]", "[[Prompt Engineering]]"],
            "aliases": ["RAG Guide"],
            "source": "original",
            "title": "Costruire Knowledge Base per AI con LLM Wiki",
            "date": "2026-02-01",
            "updated": "2026-02-01T20:32",
            "tags": ["tech/ai", "tech/rag"],
            "summary": "Guida pratica all'architettura di una knowledge base locale."
        }
        yaml_str = lint_yaml.format_canonical_frontmatter(meta, is_blog=False)
        lines = [line.split(":")[0].strip() for line in yaml_str.splitlines() if ":" in line]
        expected_order = ["status", "type", "area", "related", "aliases", "source", "title", "date", "updated", "tags", "summary"]
        self.assertEqual(lines, expected_order)

    def test_dual_mode_blog(self):
        """Asserts blog notes in 05 - Blog/ receive stage and draft: boolean while Atlas notes receive status per D-04."""
        meta = {
            "stage": "seed 🌱",
            "draft": True,
            "type": "article",
            "area": "tech",
            "related": [],
            "aliases": [],
            "source": "original",
            "title": "Guida Introduttiva a Quartz",
            "date": "2026-02-15",
            "updated": "2026-02-15T10:00",
            "tags": ["tech/web"],
            "summary": "Panoramica completa su come pubblicare un digital garden moderno con Quartz 4."
        }
        yaml_str = lint_yaml.format_canonical_frontmatter(meta, is_blog=True)
        self.assertIn("stage: seed 🌱", yaml_str)
        self.assertIn("draft: true", yaml_str)
        self.assertNotIn("status:", yaml_str)

        lines = [line.split(":")[0].strip() for line in yaml_str.splitlines() if ":" in line]
        expected_order = ["stage", "draft", "type", "area", "related", "aliases", "source", "title", "date", "updated", "tags", "summary"]
        self.assertEqual(lines, expected_order)

    def test_flow_style_arrays(self):
        """Asserts tags: [...], related: [...], and aliases: [...] are formatted as inline flow-style arrays per D-15."""
        meta = {
            "status": "permanent",
            "type": "concept",
            "area": "tech",
            "related": ["[[Nota A]]", "[[Nota B]]"],
            "aliases": ["Alias 1", "Alias 2"],
            "source": "original",
            "title": "Test Array Flow",
            "date": "2026-02-01",
            "tags": ["tech/ai", "tech/ml"]
        }
        yaml_str = lint_yaml.format_canonical_frontmatter(meta, is_blog=False)
        self.assertIn('related: ["[[Nota A]]", "[[Nota B]]"]', yaml_str)
        self.assertIn('aliases: ["Alias 1", "Alias 2"]', yaml_str)
        self.assertIn("tags: [tech/ai, tech/ml]", yaml_str)
        self.assertNotIn('- "[[Nota A]]"', yaml_str)
        self.assertNotIn("- tech/ai", yaml_str)

    def test_roundtrip_preservation(self):
        """Asserts Markdown body, headings, and breadcrumbs are preserved byte-for-byte with single empty line separation per D-17."""
        fixture_path = os.path.join(self.fixtures_dir, "sample_atlas_note.md")
        with open(fixture_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        has_fm, fm_text, breadcrumb, body = lint_yaml.split_markdown_note(original_content)
        self.assertTrue(has_fm)
        self.assertEqual(breadcrumb, "[[Home MOC|Home]] / [[Tech MOC]] / [[Costruire Knowledge Base per AI con LLM Wiki]]")
        self.assertIn("# Costruire Knowledge Base per AI con LLM Wiki", body)
        self.assertIn("## Sezione Dettaglio", body)
        self.assertIn("## Collegamenti", body)

        assembled = lint_yaml.assemble_markdown_note(fm_text, breadcrumb, body)
        self.assertEqual(original_content.strip(), assembled.strip())

    def test_tag_normalization_and_hashtag_stripping(self):
        """Asserts flat tags are mapped to hierarchical area/topic tags and isolated hashtag lines are stripped from body per D-07."""
        self.assertEqual(lint_yaml.normalize_tag("ai", "tech"), "tech/ai")
        self.assertEqual(lint_yaml.normalize_tag("#ai", "tech"), "tech/ai")
        self.assertEqual(lint_yaml.normalize_tag("cs50", "education"), "education/cs50")
        self.assertEqual(lint_yaml.normalize_tag("crypto", "finance"), "finance/crypto")
        self.assertEqual(lint_yaml.normalize_tag("tech/ai", "tech"), "tech/ai")

        body_with_hashtags = """# Intestazione Nota

#ai #tech #school

Questo e il corpo della nota.
# Non cancellare questo H1
## Neanche questo H2

#solotag

Altro testo.
"""
        cleaned_body, extracted_tags = lint_yaml.strip_isolated_hashtag_lines(body_with_hashtags)
        self.assertNotIn("#ai #tech #school", cleaned_body)
        self.assertNotIn("#solotag", cleaned_body)
        self.assertIn("# Intestazione Nota", cleaned_body)
        self.assertIn("# Non cancellare questo H1", cleaned_body)
        self.assertIn("## Neanche questo H2", cleaned_body)
        self.assertIn("ai", extracted_tags)
        self.assertIn("tech", extracted_tags)
        self.assertIn("school", extracted_tags)
        self.assertIn("solotag", extracted_tags)

    def test_legacy_key_migration(self):
        """Asserts macro_area is migrated to area and video fields (video_url, channel) are preserved for video type notes per D-07."""
        fixture_path = os.path.join(self.fixtures_dir, "sample_legacy_note.md")
        with open(fixture_path, "r", encoding="utf-8") as f:
            legacy_content = f.read()

        dest_file = os.path.join(self.test_dir, "sample_legacy_note.md")
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(legacy_content)

        changed, new_content = lint_yaml.lint_file(dest_file, vault_root=self.test_dir, execute=True)
        self.assertTrue(changed)

        self.assertIn("area: education", new_content)
        self.assertNotIn("macro_area:", new_content)
        self.assertIn('video_url: "https://youtube.com/watch?v=12345"', new_content)
        self.assertIn('channel: "AI Explained"', new_content)
        self.assertNotIn("last_modified:", new_content)
        self.assertIn('source: "https://youtube.com/watch?v=12345"', new_content)
        self.assertIn("type: video", new_content)
        self.assertIn("updated: 2025-10-12T15:30", new_content)

    def test_non_video_strips_video_metadata(self):
        """Asserts that non-video notes strip video_url and channel fields per D-07."""
        content = """---
status: permanent
type: concept
area: tech
title: "Nota Concettuale Senza Video"
date: '2026-02-01'
video_url: "https://youtube.com/watch?v=12345"
channel: "Tech Channel"
tags: [tech/ai]
---
# Nota Concettuale Senza Video
Corpo della nota.
"""
        dest_file = os.path.join(self.test_dir, "Nota Concettuale Senza Video.md")
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(content)

        changed, new_content = lint_yaml.lint_file(dest_file, vault_root=self.test_dir, execute=True)
        self.assertTrue(changed)
        self.assertNotIn("video_url:", new_content)
        self.assertNotIn("channel:", new_content)

    def test_dry_run_does_not_modify_disk(self):
        """Asserts that running lint_file with execute=False does not write to disk."""
        fixture_path = os.path.join(self.fixtures_dir, "sample_legacy_note.md")
        with open(fixture_path, "r", encoding="utf-8") as f:
            legacy_content = f.read()

        dest_file = os.path.join(self.test_dir, "sample_legacy_dry_run.md")
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(legacy_content)

        changed, _ = lint_yaml.lint_file(dest_file, vault_root=self.test_dir, execute=False)
        self.assertTrue(changed)

        with open(dest_file, "r", encoding="utf-8") as f:
            on_disk_content = f.read()
        self.assertEqual(on_disk_content, legacy_content)

    def test_controlled_type_and_area_inference(self):
        """Asserts infer_metadata respects controlled types and areas."""
        moc_meta = lint_yaml.infer_metadata("01 - Map of Content/Tech MOC.md", {}, "", "Tech MOC.md")
        self.assertEqual(moc_meta["type"], "moc")
        self.assertEqual(moc_meta["area"], "tech")

        cal_meta = lint_yaml.infer_metadata("04 - Calendar/DailyNote - 20260201.md", {}, "", "DailyNote - 20260201.md")
        self.assertEqual(cal_meta["type"], "journal")
        self.assertEqual(cal_meta["area"], "calendar")

    def test_clean_title_str_sanitizes_forbidden_characters(self):
        """Asserts clean_title_str removes or replaces /, :, \\ with hyphens and keeps valid Title Case."""
        raw_1 = "Palantir: Cosa Fa l'Azienda"
        self.assertEqual(lint_yaml.clean_title_str(raw_1), "Palantir - Cosa Fa l'Azienda")

        raw_2 = "Lezione 12/03/2026: Algoritmi & Strutture Dati"
        self.assertEqual(lint_yaml.clean_title_str(raw_2), "Lezione 12 - 03 - 2026 - Algoritmi & Strutture Dati")

        raw_3 = "C:\\Windows\\System32\\Note"
        self.assertEqual(lint_yaml.clean_title_str(raw_3), "C - Windows - System32 - Note")

    def test_format_canonical_frontmatter_type_specific_metadata(self):
        """Asserts format_canonical_frontmatter appends video_url and channel for type: video."""
        meta = {
            "status": "permanent",
            "type": "video",
            "area": "tech",
            "source": "https://youtube.com/watch?v=123",
            "video_url": "https://youtube.com/watch?v=123",
            "channel": "3Blue1Brown",
            "title": "Essenza del Calcolo",
            "date": "2026-02-01",
            "tags": ["tech/video"],
            "summary": "Sintesi visuale del calcolo infinitesimale."
        }
        yaml_str = lint_yaml.format_canonical_frontmatter(meta)
        self.assertIn('video_url: "https://youtube.com/watch?v=123"', yaml_str)
        self.assertIn('channel: "3Blue1Brown"', yaml_str)

    def test_lint_file_preserves_video_metadata_for_video_type(self):
        """Asserts lint_file(execute=True) preserves video_url and channel on disk for type: video notes (TEST-01)."""
        content = """---
status: permanent
type: video
area: tech
title: "Nota Video Test"
date: '2026-02-01'
video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
channel: "Rick Astley"
tags: [tech/video]
summary: "Trascrizione e sintesi video protetta."
---
[[Home MOC|Home]] / [[Tech MOC]] / [[Nota Video Test]]

# Nota Video Test
Corpo della nota video.
"""
        dest_file = os.path.join(self.test_dir, "Nota Video Test.md")
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(content)

        changed, new_content = lint_yaml.lint_file(dest_file, vault_root=self.test_dir, execute=True)
        self.assertIn('video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"', new_content)
        self.assertIn('channel: "Rick Astley"', new_content)
        self.assertIn("type: video", new_content)

        with open(dest_file, "r", encoding="utf-8") as f:
            on_disk = f.read()
        self.assertIn('video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"', on_disk)
        self.assertIn('channel: "Rick Astley"', on_disk)

    def test_lint_file_and_format_canonical_frontmatter_coherence(self):
        """Asserts frontmatter generated by format_canonical_frontmatter is fully coherent with lint_file (TEST-01)."""
        meta = {
            "status": "permanent",
            "type": "video",
            "area": "tech",
            "source": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "channel": "Rick Astley",
            "title": "Coherence Note",
            "date": "2026-02-01",
            "tags": ["tech/video"],
            "summary": "Sintesi coerente dei metadati video."
        }
        yaml_str = lint_yaml.format_canonical_frontmatter(meta)
        self.assertIn('video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"', yaml_str)
        self.assertIn('channel: "Rick Astley"', yaml_str)

        note_content = f"---\n{yaml_str}\n---\n[[Home MOC|Home]] / [[Coherence Note]]\n\n# Coherence Note\nCorpo nota."
        dest_file = os.path.join(self.test_dir, "Coherence Note.md")
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(note_content)

        changed, new_content = lint_yaml.lint_file(dest_file, vault_root=self.test_dir, execute=False)
        self.assertIn('video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"', new_content)
        self.assertIn('channel: "Rick Astley"', new_content)


if __name__ == "__main__":
    unittest.main()
