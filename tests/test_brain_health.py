import unittest
import os
import sys
import tempfile
import shutil
import unicodedata
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_health

class TestBrainHealth(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_canonical_frontmatter_order(self):
        """Asserts format_canonical_frontmatter serializes keys in exact sequence:
        status (or stage+draft), type, area, related, aliases, source, title, date, updated, tags, summary per D-04, D-10.
        """
        meta = {
            "status": "permanent",
            "type": "concept",
            "area": "tech",
            "related": ["[[Test Note]]", "[[Another Note]]"],
            "aliases": ["Alias 1"],
            "source": "original",
            "title": "Test Title",
            "date": "2026-08-25",
            "updated": "2026-08-25T12:00",
            "tags": ["tech/ai", "tech/python"],
            "summary": "Test executive summary text for health test."
        }
        yaml_str = brain_health.format_canonical_frontmatter(meta, is_blog=False)
        keys = [line.split(":")[0].strip() for line in yaml_str.splitlines() if ":" in line]
        expected_atlas = ["status", "type", "area", "related", "aliases", "source", "title", "date", "updated", "tags", "summary"]
        self.assertEqual(keys, expected_atlas)

        # Also test blog mode (stage + draft instead of status)
        blog_meta = dict(meta)
        blog_meta["stage"] = "seed 🌱"
        blog_meta["draft"] = True
        blog_yaml = brain_health.format_canonical_frontmatter(blog_meta, is_blog=True)
        blog_keys = [line.split(":")[0].strip() for line in blog_yaml.splitlines() if ":" in line]
        expected_blog = ["stage", "draft", "type", "area", "related", "aliases", "source", "title", "date", "updated", "tags", "summary"]
        self.assertEqual(blog_keys, expected_blog)

    def test_forward_link_classification(self):
        """Asserts VaultHealthAuditor.audit_file_links classifies uncreated Title Cased notes
        in outlines/lists as [FORWARD-LINK] and malformed/broken paths as [BROKEN-LINK] without false positives per D-02.
        """
        # Create a sample note in test vault
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)
        sample_file = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Existing Note.md")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("# Existing Note\nSome content.")

        auditor = brain_health.VaultHealthAuditor(self.test_dir)
        test_content = """---
title: "Test Caller"
---
Here is a valid link to [[Existing Note]].
Here is a planned forward link to [[Planned Concept Note]].
Here is another forward link to [[Architecture Design Pattern]].
Here is a malformed link to [[invalid/broken/path]].
Here is a malformed link to [[http://example.com/bad]].

```python
# Code block with pandas syntax should not be treated as broken links
df = dataset[['clean_text', 'label']]
```

Here is inline code: `code[['x', 'y']]`.
"""
        valid, forward, broken = auditor.audit_file_links("02 - Atlas/Tech/Test Caller.md", test_content)
        self.assertIn("Existing Note", valid)
        self.assertIn("Planned Concept Note", forward)
        self.assertIn("Architecture Design Pattern", forward)
        self.assertIn("invalid/broken/path", broken)
        self.assertIn("http://example.com/bad", broken)
        self.assertNotIn("Existing Note", forward)
        self.assertNotIn("Existing Note", broken)
        self.assertNotIn("'clean_text', 'label'", broken)
        self.assertNotIn("'x', 'y'", broken)

    def test_orphan_detection(self):
        """Asserts notes in 02 - Atlas/ with 0 incoming links and missing from 01 - Map of Content/ MOCs
        are flagged as orphans per D-02.
        """
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Tech"), exist_ok=True)

        # 1. Connected note referenced in MOC
        moc_file = os.path.join(self.test_dir, "01 - Map of Content", "Tech MOC.md")
        with open(moc_file, "w", encoding="utf-8") as f:
            f.write("# Tech MOC\n- [[Connected Note]]")

        connected_file = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Connected Note.md")
        with open(connected_file, "w", encoding="utf-8") as f:
            f.write("# Connected Note\nContent.")

        # 2. Orphan note not referenced anywhere
        orphan_file = os.path.join(self.test_dir, "02 - Atlas", "Tech", "Isolated Orphan Note.md")
        with open(orphan_file, "w", encoding="utf-8") as f:
            f.write("# Isolated Orphan Note\nLonely content.")

        auditor = brain_health.VaultHealthAuditor(self.test_dir)
        # Scan links for all files
        for clean_name, rel_path in auditor.all_notes.items():
            abs_p = os.path.join(self.test_dir, rel_path)
            with open(abs_p, "r", encoding="utf-8") as f:
                c = f.read()
            auditor.audit_file_links(rel_path, c)

        orphans = auditor.detect_orphans()
        orphan_rel = os.path.normpath("02 - Atlas/Tech/Isolated Orphan Note.md")
        orphans_norm = [os.path.normpath(o) for o in orphans]
        self.assertIn(orphan_rel, orphans_norm)
        self.assertNotIn(os.path.normpath("02 - Atlas/Tech/Connected Note.md"), orphans_norm)

    def test_title_case_and_breadcrumb_sync(self):
        """Asserts intelligent Title Case formatting preserves uppercase acronyms (AI, MOC, REST, CLI)
        and minor words (di, del, per, in) while updating breadcrumbs and filename per D-13.
        """
        title_raw = "guida pratica all'uso di rest api per ai e cli"
        cleaned_title = brain_health.clean_title_str(title_raw)
        self.assertIn("REST", cleaned_title)
        self.assertIn("API", cleaned_title)
        self.assertIn("AI", cleaned_title)
        self.assertIn("CLI", cleaned_title)
        self.assertIn("di", cleaned_title)
        self.assertIn("per", cleaned_title)
        self.assertIn("e", cleaned_title)

        filename_clean = brain_health.clean_filename("01 - introduzione all'ai e moc!.md")
        self.assertIn("AI", filename_clean)
        self.assertIn("MOC", filename_clean)
        self.assertNotIn("!", filename_clean)

        breadcrumb = brain_health.get_breadcrumbs("02 - Atlas/Tech/REST API Guide.md", "REST API Guide")
        self.assertEqual(breadcrumb, "[[Home MOC|Home]] / [[Tech]] / [[REST API Guide]]")

    def test_static_dashboard_rendering(self):
        """Asserts generate_health_dashboard outputs 100% pure static Markdown (metrics, staging notes table,
        blog seeds table, recent notes) without any dataview codeblocks to 99 - Meta/Vault Health Dashboard.md per D-03.
        """
        notes_data = [
            {
                "name": "Draft Note 1",
                "rel_path": "03 - Inbox/Draft Note 1.md",
                "mtime": 1700000000,
                "metadata": {"status": "draft", "date": "2026-08-25", "area": "tech"}
            },
            {
                "name": "Blog Post 1",
                "rel_path": "05 - Blog/Blog Post 1.md",
                "mtime": 1700000000,
                "metadata": {"stage": "seed 🌱", "draft": True, "date": "2026-08-25"}
            },
            {
                "name": "Permanent Note 1",
                "rel_path": "02 - Atlas/Tech/Permanent Note 1.md",
                "mtime": 1700000000,
                "metadata": {"status": "permanent", "date": "2026-08-20", "area": "tech"}
            }
        ]
        audit_stats = {
            "total_notes": 42,
            "orphan_count": 2,
            "broken_link_count": 1,
            "forward_link_count": 5
        }
        dashboard_md = brain_health.generate_health_dashboard(self.test_dir, notes_data, audit_stats)
        self.assertNotIn("```dataview", dashboard_md)
        self.assertNotIn("```dataviewjs", dashboard_md)
        self.assertIn("# Vault Health Dashboard", dashboard_md)
        self.assertIn("42", dashboard_md)
        self.assertIn("[[Draft Note 1]]", dashboard_md)
        self.assertIn("[[Blog Post 1]]", dashboard_md)
        self.assertIn("[[Permanent Note 1]]", dashboard_md)

        # Check writing to dashboard path
        out_path = brain_health.write_health_dashboard(self.test_dir, notes_data, audit_stats)
        self.assertTrue(os.path.exists(out_path))
        self.assertTrue(out_path.endswith("99 - Meta/Vault Health Dashboard.md"))

    def test_cli_flags_and_interactive_defaults(self):
        """Asserts --dry-run performs read-only checks, --auto-fix applies deterministic fixes,
        and default mode is interactive step-by-step confirmation per D-01.
        """
        parser = brain_health.build_arg_parser()
        args_default = parser.parse_args([])
        self.assertTrue(args_default.interactive)
        self.assertFalse(args_default.dry_run)
        self.assertFalse(args_default.auto_fix)

        args_dry = parser.parse_args(["--dry-run"])
        self.assertTrue(args_dry.dry_run)
        self.assertFalse(args_dry.auto_fix)

        args_fix = parser.parse_args(["--auto-fix"])
        self.assertTrue(args_fix.auto_fix)
        self.assertFalse(args_fix.dry_run)

        args_dash = parser.parse_args(["--dashboard-only"])
        self.assertTrue(args_dash.dashboard_only)

    def test_accented_characters_filename_title_symmetry(self):
        """Asserts symmetrical preservation of Italian accented vowels in Unicode NFC between clean_filename and clean_title_str per D-03."""
        test_samples = [
            ("identità del secondo brain", "Identità del Secondo Brain"),
            ("perché l'ingegneria informatica è essenziale", "Perché l'Ingegneria Informatica È Essenziale"),
            ("università e facoltà d'ingegneria", "Università e Facoltà d'Ingegneria"),
            ("città, virtù e verità", "Città, Virtù e Verità"),
        ]
        for raw, expected in test_samples:
            filename_res = brain_health.clean_filename(f"{raw}.md")
            title_res = brain_health.clean_title_str(raw)
            self.assertEqual(filename_res, expected)
            self.assertEqual(title_res, expected)
            self.assertEqual(filename_res, title_res)
            self.assertEqual(unicodedata.normalize('NFC', filename_res), filename_res)
            self.assertEqual(unicodedata.normalize('NFC', title_res), title_res)

    def test_sanitization_forbidden_characters_symmetry(self):
        """Asserts identical sanitization of forbidden characters (/, \\, :) between clean_filename and clean_title_str per D-04."""
        cases = [
            ("Lezione 12/03/2026: Algoritmi & Strutture Dati", "Lezione 12 - 03 - 2026 - Algoritmi & Strutture Dati"),
            ("C:\\Windows\\System32\\Note", "C - Windows - System32 - Note"),
        ]
        for raw, expected in cases:
            fn_res = brain_health.clean_filename(f"{raw}.md")
            title_res = brain_health.clean_title_str(raw)
            self.assertEqual(fn_res, expected)
            self.assertEqual(title_res, expected)
            self.assertEqual(fn_res, title_res)

    def test_infer_metadata_video_preservation(self):
        """Asserts infer_metadata preserves video_url and channel for notes with type: video per D-07."""
        meta = {
            "type": "video",
            "source": "https://youtube.com/watch?v=123",
            "video_url": "https://youtube.com/watch?v=123",
            "channel": "AI Explained"
        }
        res = brain_health.infer_metadata("02 - Atlas/Tech/Video Note.md", meta, "body", "Video Note.md")
        self.assertEqual(res["type"], "video")
        self.assertEqual(res["video_url"], "https://youtube.com/watch?v=123")
        self.assertEqual(res["channel"], "AI Explained")

    def test_video_source_bidirectional_sync(self):
        """Asserts bidirectional synchronization between source and video_url for YouTube links per D-08."""
        # 1. source has YouTube URL, video_url missing
        meta1 = {"type": "video", "source": "https://youtube.com/watch?v=123"}
        res1 = brain_health.infer_metadata("02 - Atlas/Tech/Video Note 1.md", meta1, "body", "Video Note 1.md")
        self.assertEqual(res1["video_url"], "https://youtube.com/watch?v=123")
        self.assertEqual(res1["source"], "https://youtube.com/watch?v=123")

        # 2. video_url has YouTube URL, source is 'original'
        meta2 = {"type": "video", "source": "original", "video_url": "https://youtu.be/abc"}
        res2 = brain_health.infer_metadata("02 - Atlas/Tech/Video Note 2.md", meta2, "body", "Video Note 2.md")
        self.assertEqual(res2["source"], "https://youtu.be/abc")
        self.assertEqual(res2["video_url"], "https://youtu.be/abc")

    def test_scan_vault_duplicate_collision_tracking(self):
        """Asserts VaultHealthAuditor.scan_vault prevents destructive overwrite of all_notes and tracks collisions in duplicate_notes per D-05, D-06."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech")
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        os.makedirs(atlas_dir, exist_ok=True)
        os.makedirs(inbox_dir, exist_ok=True)

        atlas_file = os.path.join(atlas_dir, "Concept Node.md")
        inbox_file = os.path.join(inbox_dir, "Concept Node.md")
        with open(atlas_file, "w", encoding="utf-8") as f:
            f.write("# Atlas Concept Node\nContent.")
        with open(inbox_file, "w", encoding="utf-8") as f:
            f.write("# Inbox Concept Node\nStaging draft.")

        auditor = brain_health.VaultHealthAuditor(self.test_dir)
        self.assertIn("Concept Node", auditor.all_notes)
        self.assertIn("Concept Node", auditor.duplicate_notes)
        self.assertEqual(len(auditor.duplicate_notes["Concept Node"]), 2)
        # 02 - Atlas is scanned first alphabetically before 03 - Inbox
        self.assertEqual(auditor.all_notes["Concept Node"], os.path.normpath("02 - Atlas/Tech/Concept Node.md"))

    def test_audit_stats_reports_duplicate_count(self):
        """Asserts run_governance_engine exposes duplicate_count and duplicate_notes in audit_stats per HLTH-04."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech")
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        os.makedirs(atlas_dir, exist_ok=True)
        os.makedirs(inbox_dir, exist_ok=True)

        with open(os.path.join(atlas_dir, "Duplicate Note.md"), "w", encoding="utf-8") as f:
            f.write("# Duplicate 1")
        with open(os.path.join(inbox_dir, "Duplicate Note.md"), "w", encoding="utf-8") as f:
            f.write("# Duplicate 2")

        stats = brain_health.run_governance_engine(self.test_dir, dry_run=True)
        self.assertEqual(stats["duplicate_count"], 1)
        self.assertIn("Duplicate Note", stats["duplicate_notes"])

    def test_lint_only_diagnostic_mode(self):
        """Asserts --lint-only runs a non-destructive read-only audit of YAML violations without modifying disk per D-01, HLTH-01."""
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Tech")
        os.makedirs(atlas_dir, exist_ok=True)
        note_path = os.path.join(atlas_dir, "Incomplete Note.md")
        original_content = """---
title: "Incomplete Note"
date: '2026-09-03'
---
# Incomplete Note
Body without status, type, area, tags.
"""
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(original_content)

        stats = brain_health.run_governance_engine(self.test_dir, lint_only=True)
        self.assertEqual(stats["total_notes"], 1)
        self.assertEqual(stats["misaligned_notes"], 1)
        self.assertEqual(stats["compliant_notes"], 0)
        self.assertEqual(len(stats["issues"]), 1)

        # Assert no modification to file on disk
        with open(note_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), original_content)

        # Assert no dashboard or report was created
        dashboard_path = os.path.join(self.test_dir, "99 - Meta", "Vault Health Dashboard.md")
        self.assertFalse(os.path.exists(dashboard_path))
        inbox_dir = os.path.join(self.test_dir, "03 - Inbox")
        self.assertFalse(os.path.exists(inbox_dir))

    def test_lint_only_rejects_auto_fix_conflict(self):
        """Asserts run_governance_engine rejects concurrent --lint-only and --auto-fix per D-02."""
        res = brain_health.run_governance_engine(self.test_dir, lint_only=True, auto_fix=True)
        self.assertEqual(res.get("error"), "lint_only_read_only_conflict")

    def test_diagnostic_report_and_dashboard_headings_no_emoji(self):
        """Asserts diagnostic report and dashboard have zero emoji in H1-H6 headings and no Collegamenti section (D-14, D-16, PERF-04)."""
        import re
        audit_stats = {
            "orphan_notes": ["02 - Atlas/Tech/Orphan Note.md"],
            "broken_links": {"02 - Atlas/Tech/Source Note.md": ["Broken Target"]},
            "forward_links": {"02 - Atlas/Tech/Source Note.md": ["Future Note"]},
            "lint_issues": [("02 - Atlas/Tech/Lint Note.md", ["Missing status"])],
            "title_case_renames": [],
            "total_notes": 10,
            "compliant_notes": 9,
            "misaligned_notes": 1,
            "recent_notes": []
        }

        # 1. Health Dashboard Markdown
        dashboard_md = brain_health.generate_health_dashboard(self.test_dir, [], audit_stats)
        self.assertNotIn("## Collegamenti", dashboard_md)

        dash_headings = [line.strip() for line in dashboard_md.splitlines() if line.strip().startswith("#")]
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]')
        for h in dash_headings:
            self.assertIsNone(emoji_pattern.search(h), f"Dashboard heading contains emoji: {h}")

        # 2. Audit Report Markdown
        report_path = brain_health.write_audit_report(
            self.test_dir,
            all_notes_count=10,
            orphan_notes=audit_stats["orphan_notes"],
            broken_links=audit_stats["broken_links"],
            forward_links=audit_stats["forward_links"],
            lint_issues=audit_stats["lint_issues"]
        )
        with open(report_path, "r", encoding="utf-8") as f:
            report_md = f.read()

        self.assertNotIn("## Collegamenti", report_md)
        report_headings = [line.strip() for line in report_md.splitlines() if line.strip().startswith("#")]
        for h in report_headings:
            self.assertIsNone(emoji_pattern.search(h), f"Audit report heading contains emoji: {h}")


if __name__ == "__main__":
    unittest.main()
