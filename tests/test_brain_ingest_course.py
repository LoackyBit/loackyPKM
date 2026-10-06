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

    def _create_test_pdf(self, filename: str, pages_text: list, password: str = None) -> str:
        """Creates a synthetic test PDF using pypdf."""
        import pypdf
        writer = pypdf.PdfWriter()
        font_dict = pypdf.generic.DictionaryObject({
            pypdf.generic.NameObject('/Type'): pypdf.generic.NameObject('/Font'),
            pypdf.generic.NameObject('/Subtype'): pypdf.generic.NameObject('/Type1'),
            pypdf.generic.NameObject('/BaseFont'): pypdf.generic.NameObject('/Helvetica')
        })
        for txt in pages_text:
            page = writer.add_blank_page(width=612, height=792)
            stream_cmds = ['BT', '/F1 12 Tf', '50 750 Td']
            for line in txt.splitlines():
                esc = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
                stream_cmds.append(f'({esc}) Tj')
                stream_cmds.append('0 -15 Td')
            stream_cmds.append('ET')

            stream = pypdf.generic.DecodedStreamObject()
            stream.set_data('\n'.join(stream_cmds).encode('latin-1'))
            page[pypdf.generic.NameObject('/Contents')] = stream

            res_dict = pypdf.generic.DictionaryObject()
            res_font = pypdf.generic.DictionaryObject()
            res_font[pypdf.generic.NameObject('/F1')] = font_dict
            res_dict[pypdf.generic.NameObject('/Font')] = res_font
            page[pypdf.generic.NameObject('/Resources')] = res_dict

        if password:
            writer.encrypt(password)

        pdf_path = os.path.join(self.test_dir, filename)
        with open(pdf_path, 'wb') as f:
            writer.write(f)
        return pdf_path

    def test_ingest_pdf_with_course_flag_creates_attachment_and_draft(self):
        """Asserts ingesting a PDF with --course archives to Attachments/<Course>/,
        creates draft with academic breadcrumb and stages source per PDF-01, PDF-02, D-08."""
        pdf_path = self._create_test_pdf(
            "Slide Ricerca Operativa.pdf",
            ["Introduzione alla Ricerca Operativa e al metodo del Simplesso con oltre 50 caratteri di testo utile per superare la soglia."]
        )

        draft_path = brain_ingest.ingest_source(
            pdf_path,
            vault_root=self.test_dir,
            course="Ricerca Operativa",
            use_ai=False
        )

        self.assertTrue(os.path.exists(draft_path))

        # Permanent attachment must be in 99 - Meta/Attachments/Ricerca Operativa/
        att_path = os.path.join(self.test_dir, "99 - Meta", "Attachments", "Ricerca Operativa", "Slide Ricerca Operativa.pdf")
        self.assertTrue(os.path.exists(att_path), f"Attachment should exist at {att_path}")

        # Staged source must be in 03 - Inbox/Source/
        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", "Slide Ricerca Operativa.md")
        self.assertTrue(os.path.exists(source_path))

        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Academic breadcrumb must link to Ricerca Operativa MOC
        self.assertIn("[[Ricerca Operativa MOC]]", content)
        self.assertIn("\\[[[Slide Ricerca Operativa.pdf#page=1|1]]]", content)

    def test_ingest_pdf_without_course_archives_in_general(self):
        """Asserts ingesting a PDF without --course archives to Attachments/General/ per D-11."""
        pdf_path = self._create_test_pdf(
            "Machine Learning Paper.pdf",
            ["Deep reinforcement learning algorithms and gradient-based policy optimization with over fifty characters."]
        )

        draft_path = brain_ingest.ingest_source(
            pdf_path,
            vault_root=self.test_dir,
            course=None,
            use_ai=False
        )

        self.assertTrue(os.path.exists(draft_path))

        # Permanent attachment must be in 99 - Meta/Attachments/General/
        att_path = os.path.join(self.test_dir, "99 - Meta", "Attachments", "General", "Machine Learning Paper.pdf")
        self.assertTrue(os.path.exists(att_path), f"General attachment should exist at {att_path}")

        with open(draft_path, "r", encoding="utf-8") as f:
            content = f.read()

        has_fm, fm_t, _, _ = brain_health.split_markdown_note(content)
        meta = brain_health.safe_load_frontmatter(fm_t, brain_health.build_yaml_engine())
        self.assertEqual(meta.get("area"), "tech")
        self.assertEqual(meta.get("type"), "concept")

    def test_ingest_pdf_encrypted_or_empty_records_review_dashboard_error(self):
        """Asserts encrypted or insufficient text PDFs record diagnostic error in Review Dashboard per D-09."""
        import academic_helper
        enc_pdf = self._create_test_pdf("Encrypted.pdf", ["Super secret text content"], password="pwd")

        with self.assertRaises(academic_helper.PdfEncryptedError):
            brain_ingest.ingest_source(
                enc_pdf,
                vault_root=self.test_dir,
                course="Sicurezza",
                use_ai=False
            )

        # Review Dashboard must have recorded the error
        dash_path = os.path.join(self.test_dir, "03 - Inbox", "Review Dashboard.md")
        self.assertTrue(os.path.exists(dash_path))
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_content = f.read()
        self.assertIn("PDF protetto da password", dash_content)

        # No draft must be created
        draft_files = os.listdir(os.path.join(self.test_dir, "03 - Inbox", "Draft"))
        self.assertEqual(len(draft_files), 0)

    def test_promote_pdf_lesson_updates_pacrar_and_preserves_attachment(self):
        """Asserts promotion registers lecture in Course Hub PACRAR matrix and PRESERVES permanent PDF per D-08, D-13."""
        course_name = "Calcolo Numerico"
        pdf_path = self._create_test_pdf(
            "Lezione 02 Metodo di Newton.pdf",
            ["Studio della convergenza quadratica del metodo di Newton per la risoluzione di equazioni non lineari."]
        )

        draft_path = brain_ingest.ingest_source(
            pdf_path,
            vault_root=self.test_dir,
            course=course_name,
            use_ai=False
        )
        lesson_title = "Lezione 02 Metodo di Newton"
        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{lesson_title}.md")
        perm_pdf_path = os.path.join(self.test_dir, "99 - Meta", "Attachments", course_name, "Lezione 02 Metodo di Newton.pdf")

        self.assertTrue(os.path.exists(perm_pdf_path), "Permanent PDF must exist before promotion")
        self.assertTrue(os.path.exists(source_path), "Source markdown must exist before promotion")

        # Promote item
        ok, err = brain_ingest._handle_promote_item(
            self.test_dir,
            draft_path,
            source_path,
            lesson_title,
            lesson_title,
            f"[[{lesson_title}.pdf]]"
        )
        self.assertTrue(ok, f"Promotion failed: {err}")

        # Permanent PDF must STILL exist (D-08)
        self.assertTrue(os.path.exists(perm_pdf_path), "Permanent PDF must NOT be removed during promotion!")

        # Temporary source markdown in Source/ must be removed
        self.assertFalse(os.path.exists(source_path), "Source markdown should be cleaned from 03 - Inbox/Source/")

        # PACRAR table in MOC must include the new lecture row
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", f"{course_name} MOC.md")
        with open(moc_path, "r", encoding="utf-8") as f:
            moc_content = f.read()

        self.assertIn(f"| [[{lesson_title}]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |", moc_content)

    def test_purge_pdf_lesson_removes_clipboard_images(self):
        """Asserts rejecting a draft [-] removes figures in Clipboard/<Course>/ per D-04, D-07."""
        course_name = "Sistemi Operativi"
        clip_course_dir = os.path.join(self.test_dir, "99 - Meta", "Clipboard", course_name)
        os.makedirs(clip_course_dir, exist_ok=True)

        img_filename = "Figura - Semafori e Mutex - p3 - 1.png"
        img_path = os.path.join(clip_course_dir, img_filename)
        with open(img_path, "wb") as f:
            f.write(b"fake image bytes")

        draft_content = f"""---
title: "Semafori e Mutex"
status: draft
type: lecture
area: education
course: "{course_name}"
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Sistemi Operativi MOC]] / [[Semafori e Mutex]]

# Semafori e Mutex

Illustrazione dei semafori di Dijkstra:
![[{img_filename}]]
"""
        draft_path = os.path.join(self.test_dir, "03 - Inbox", "Draft", "Semafori e Mutex.md")
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft_content)
        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", "Semafori e Mutex.md")
        with open(source_path, "w", encoding="utf-8") as f:
            f.write("Raw source")

        self.assertTrue(os.path.exists(img_path))

        # Purge item
        res = brain_ingest._handle_purge_item(self.test_dir, draft_path, source_path, "Semafori e Mutex")
        self.assertTrue(res)

        # Image in course clipboard directory must have been removed!
        self.assertFalse(os.path.exists(img_path), "Clipboard figure in course directory should be purged!")

    def test_audit_pdf_attachments_detects_versioned_and_duplicates(self):
        """Asserts audit_pdf_attachments detects versioned (v2) files and duplicate SHA-256 files per D-10."""
        att_course_dir = os.path.join(self.test_dir, "99 - Meta", "Attachments", "Fisica")
        att_gen_dir = os.path.join(self.test_dir, "99 - Meta", "Attachments", "General")
        os.makedirs(att_course_dir, exist_ok=True)
        os.makedirs(att_gen_dir, exist_ok=True)

        # Versioned file
        v2_path = os.path.join(att_course_dir, "Cinematica (v2).pdf")
        with open(v2_path, "wb") as f:
            f.write(b"content v2")

        # Duplicate files with same content in two folders
        dup_content = b"duplicate pdf binary content for sha test"
        f1_path = os.path.join(att_course_dir, "Meccanica.pdf")
        f2_path = os.path.join(att_gen_dir, "Meccanica Copy.pdf")
        with open(f1_path, "wb") as f:
            f.write(dup_content)
        with open(f2_path, "wb") as f:
            f.write(dup_content)

        stats = brain_health.audit_pdf_attachments(self.test_dir)

        self.assertEqual(stats["total_attachments"], 3)
        self.assertEqual(len(stats["versioned_files"]), 1)
        self.assertIn(os.path.relpath(v2_path, self.test_dir), stats["versioned_files"])
        self.assertEqual(len(stats["duplicate_hashes"]), 1)

    def test_promote_nested_university_degree_note_does_not_create_duplicate_folder(self):
        """Asserts promoting a note inside a nested degree folder (e.g. Ingegneria Informatica 2026-27/<Course>)
        correctly updates the course MOC and does NOT create a stray 'Ingegneria Informatica 2026 - 27' folder."""
        course_name = "Fondamenti di Matematica (Analisi 1)"
        nested_dir = os.path.join(
            self.test_dir,
            "02 - Atlas",
            "Education & Learning",
            "University",
            "Ingegneria Informatica 2026-27",
            course_name,
        )
        os.makedirs(nested_dir, exist_ok=True)
        course_hub.init_course(course_name, vault_root=self.test_dir)

        lesson_title = "06 - Valore Assoluto e Principio di Induzione"
        target_path = f"02 - Atlas/Education & Learning/University/Ingegneria Informatica 2026-27/{course_name}/{lesson_title}.md"

        meta = {
            "title": lesson_title,
            "status": "draft",
            "type": "concept",
            "area": "education",
            "tags": ["education/university"],
            "course": course_name,
            "target_path": target_path,
        }
        draft_content = brain_health.assemble_markdown_note(
            brain_health.format_canonical_frontmatter(meta),
            "[[Home MOC|Home]]",
            "Corpo della lezione sul valore assoluto."
        )

        draft_path = os.path.join(self.test_dir, "03 - Inbox", "Draft", f"{lesson_title}.md")
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(draft_content)

        source_path = os.path.join(self.test_dir, "03 - Inbox", "Source", f"{lesson_title}.md")
        with open(source_path, "w", encoding="utf-8") as f:
            f.write("Raw source")

        success, err = brain_ingest._handle_promote_item(
            self.test_dir,
            draft_path,
            source_path,
            lesson_title,
            lesson_title,
            lesson_title,
        )
        self.assertTrue(success, f"Promote failed: {err}")

        # Check lesson reached final destination
        final_dest = os.path.join(self.test_dir, target_path)
        self.assertTrue(os.path.exists(final_dest))

        # Check course MOC PACRAR table has registered the lesson
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", f"{course_name} MOC.md")
        self.assertTrue(os.path.exists(moc_path))
        with open(moc_path, "r", encoding="utf-8") as f:
            moc_text = f.read()
        self.assertIn(f"[[{lesson_title}]]", moc_text)

        # CRITICAL ASSERTION: Stray folder 'Ingegneria Informatica 2026 - 27' must NOT exist!
        stray_folder = os.path.join(
            self.test_dir,
            "02 - Atlas",
            "Education & Learning",
            "University",
            "Ingegneria Informatica 2026 - 27",
        )
        self.assertFalse(os.path.exists(stray_folder), "Stray 'Ingegneria Informatica 2026 - 27' directory should not be created!")


if __name__ == "__main__":
    unittest.main()

