import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import brain_ingest
import course_hub
import brain_health

class TestBrainIngestCourse(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Draft"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "03 - Inbox", "Source"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University"), exist_ok=True)
        os.environ["BRAIN_INGEST_NO_AI"] = "1"

        # Create minimal University.md
        uni_path = os.path.join(self.test_dir, "01 - Map of Content", "University.md")
        with open(uni_path, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: moc
area: education
related: []
title: "University MOC"
date: '2026-08-24'
tags: [education/university]
---
[[Home MOC|Home]] / [[University|University MOC]]

# Università

---

## Collegamenti
- [[Home]]
""")

    def tearDown(self):
        os.environ.pop("BRAIN_INGEST_NO_AI", None)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_ingest_source_with_course_flag_creates_hub_and_sets_academic_breadcrumb(self):
        """Asserts ingesting with --course auto-initializes Course Hub, routes to university folder, and sets academic breadcrumb per D-01, D-14."""
        sample_text = "# Lezione 01 - Limiti e Continuita\nDefinizione formale di limite e continuita secondo Cauchy-Weierstrass."
        draft_path = brain_ingest.ingest_source(
            sample_text,
            vault_root=self.test_dir,
            course="Analisi Matematica",
            use_ai=False
        )
        self.assertTrue(os.path.exists(draft_path))

        # Course hub MOC must have been auto-initialized
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", "Analisi Matematica MOC.md")
        self.assertTrue(os.path.exists(moc_path), f"MOC path {moc_path} should exist")

        # Atlas course folder must exist
        course_dir = os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University", "Analisi Matematica")
        self.assertTrue(os.path.isdir(course_dir))

        with open(draft_path, "r", encoding="utf-8") as f:
            draft_content = f.read()

        # Academic breadcrumb check per D-14
        self.assertIn(
            "[[Home MOC|Home]] / [[University|University MOC]] / [[Analisi Matematica MOC]] / [[Lezione 01 - Limiti e Continuita]]",
            draft_content
        )

        # Related field in YAML must NOT inject parent course MOC (preserving horizontal relations per D-14)
        has_fm, fm_text, _, _ = brain_health.split_markdown_note(draft_content)
        meta = brain_health.safe_load_frontmatter(fm_text, brain_health.build_yaml_engine())
        related = meta.get("related", [])
        self.assertNotIn("[[Analisi Matematica MOC]]", related)
        self.assertNotIn("[[Analisi Matematica]]", related)

    def test_promote_item_registers_lesson_in_pacrar_matrix(self):
        """Asserts promoting approved lesson note registers it in the Course Hub PACRAR table per PACRAR-03, D-15."""
        course_name = "Architettura dei Calcolatori"
        course_hub.init_course(course_name, vault_root=self.test_dir)

        lesson_title = "01 - Gerarchia di Memoria e Cache"
        dest_dir = f"02 - Atlas/Education & Learning/University/{course_name}"
        meta = {
            "title": lesson_title,
            "status": "draft",
            "type": "concept",
            "area": "education",
            "tags": ["education/university"],
            "course": course_name,
            "target_path": f"{dest_dir}/{lesson_title}.md"
        }

        # Stage note
        draft_path = brain_ingest.stage_note(
            self.test_dir,
            lesson_title,
            "# 01 - Gerarchia di Memoria e Cache\n\nPrincipio di localita spaziale e temporale.",
            metadata=meta,
            target_dir=dest_dir,
            source_content="Raw lecture notes",
            status="draft"
        )
        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{lesson_title}.md")

        # Promote item
        ok, err = brain_ingest._handle_promote_item(
            self.test_dir,
            draft_path,
            source_path,
            lesson_title,
            lesson_title,
            lesson_title
        )
        self.assertTrue(ok, f"Promotion failed: {err}")

        # Check that permanent note exists
        promoted_path = os.path.join(self.test_dir, dest_dir, f"{lesson_title}.md")
        self.assertTrue(os.path.exists(promoted_path))

        # Check that PACRAR table in course MOC contains the newly promoted lesson
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", f"{course_name} MOC.md")
        with open(moc_path, "r", encoding="utf-8") as f:
            moc_content = f.read()

        self.assertIn(f"[[{lesson_title}]]", moc_content)
        self.assertIn(f"| [[{lesson_title}]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |", moc_content)


if __name__ == "__main__":
    unittest.main()
