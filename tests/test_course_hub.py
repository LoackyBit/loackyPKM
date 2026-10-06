import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts"))

import course_hub
import brain_health

class TestCourseHub(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.moc_dir = os.path.join(self.test_dir, "01 - Map of Content")
        os.makedirs(self.moc_dir, exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University"), exist_ok=True)
        
        # Minimal University.md
        self.uni_path = os.path.join(self.moc_dir, "University.md")
        with open(self.uni_path, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: moc
area: education
related: []
aliases: []
source: original
title: "University MOC"
date: '2026-08-24'
updated: 2026-08-24T21:38
tags: [education/university, education/moc]
summary: "Indice e mappa concettuale per University MOC."
---
[[Home MOC|Home]] / [[University|University MOC]]

# Università & Percorso Accademico

Mappa concettuale relativa all'orientamento universitario.

---

## Collegamenti
- [[Home|Home]]
""")

        # Minimal Corsi.md (extracurricular) to assert it is strictly untouched per D-11
        self.corsi_path = os.path.join(self.test_dir, "01 - Map of Content", "Corsi.md")
        with open(self.corsi_path, "w", encoding="utf-8") as f:
            f.write("""---
status: permanent
type: moc
area: education
related: []
title: "Corsi MOC"
date: '2026-08-24'
tags: [education/corsi]
summary: "Indice per corsi extracurricolari."
---
[[Home MOC|Home]] / [[Corsi|Corsi MOC]]

# Corsi Extracurricolari

---

## Corsi Online
- [[CS50]]
""")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sanitize_course_name(self):
        """Asserts sanitize_course_name strips illegal path traversal / reserved characters (T-13-01)."""
        self.assertEqual(course_hub.sanitize_course_name("Analisi Matematica 1"), "Analisi Matematica 1")
        # Strips path traversal and illegal chars
        sanitized = course_hub.sanitize_course_name("../../Fisica: Generale*?")
        self.assertNotIn("..", sanitized)
        self.assertNotIn("/", sanitized)
        self.assertNotIn(":", sanitized)
        self.assertNotIn("*", sanitized)
        self.assertNotIn("?", sanitized)
        self.assertIn("Fisica", sanitized)
        
        # Empty string raises ValueError
        with self.assertRaises(ValueError):
            course_hub.sanitize_course_name("   ")
        with self.assertRaises(ValueError):
            course_hub.sanitize_course_name("../..//")

    def test_atomic_write_file(self):
        """Asserts atomic_write_file safely creates target file and overwrites atomically (T-13-02)."""
        target = os.path.join(self.test_dir, "atomic_test.txt")
        course_hub.atomic_write_file(target, "first content")
        self.assertTrue(os.path.exists(target))
        with open(target, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "first content")
            
        course_hub.atomic_write_file(target, "second content")
        with open(target, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "second content")

    def test_init_course_success(self):
        """Asserts init_course creates MOC and Atlas folder with canonical 10-field frontmatter per D-01, D-04, D-13."""
        ok = course_hub.init_course("Analisi Matematica", vault_root=self.test_dir)
        self.assertTrue(ok)
        
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", "Analisi Matematica MOC.md")
        self.assertTrue(os.path.exists(moc_path))
        
        atlas_dir = os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University", "Analisi Matematica")
        self.assertTrue(os.path.isdir(atlas_dir))
        
        with open(moc_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check canonical breadcrumb per D-13
        self.assertIn("[[Home MOC|Home]] / [[University|University MOC]] / [[Analisi Matematica MOC]]", content)
        
        # Check required sections without emoji
        self.assertIn("# Analisi Matematica — Course Hub & Matrice PACRAR", content)
        self.assertIn("## Informazioni Corso", content)
        self.assertIn("- **Docente:**", content)
        self.assertIn("- **CFU:**", content)
        self.assertIn("- **Materiali & Testi:**", content)
        self.assertIn("- **Cartella Vault:** `02 - Atlas/Education & Learning/University/Analisi Matematica/`", content)
        self.assertIn("## Matrice PACRAR", content)
        self.assertIn('<div class="pacrar-progress-widget" data-course="Analisi Matematica"></div>', content)
        self.assertIn("| Argomento | P | A | C | R | A | R |", content)
        self.assertIn("## Formulari & Risorse Chiave", content)

    def test_init_course_idempotence(self):
        """Asserts re-initializing an existing course warns and does not overwrite without --force per D-03."""
        course_hub.init_course("Fisica Generale", vault_root=self.test_dir)
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", "Fisica Generale MOC.md")
        
        # Modify MOC content to detect overwrite
        with open(moc_path, "a", encoding="utf-8") as f:
            f.write("\nCustom student notes here.")
            
        # Second call without force must return False and preserve file
        ok_second = course_hub.init_course("Fisica Generale", vault_root=self.test_dir, force=False)
        self.assertFalse(ok_second)
        with open(moc_path, "r", encoding="utf-8") as f:
            self.assertIn("Custom student notes here.", f.read())
            
        # Call with force must succeed and rewrite
        ok_force = course_hub.init_course("Fisica Generale", vault_root=self.test_dir, force=True)
        self.assertTrue(ok_force)
        with open(moc_path, "r", encoding="utf-8") as f:
            self.assertNotIn("Custom student notes here.", f.read())

    def test_register_in_university_moc_creates_section_and_link(self):
        """Asserts register_in_university_moc inserts ## Corsi Universitari and course link per D-12."""
        ok = course_hub.register_in_university_moc("Algoritmi e Strutture Dati", vault_root=self.test_dir)
        self.assertTrue(ok)
        
        with open(self.uni_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("## Corsi Universitari", content)
        self.assertIn("- [[Algoritmi e Strutture Dati MOC]]", content)

    def test_register_in_university_moc_idempotent(self):
        """Asserts repeated registrations do not duplicate links in University.md per D-12."""
        course_hub.register_in_university_moc("Basi di Dati", vault_root=self.test_dir)
        course_hub.register_in_university_moc("Basi di Dati", vault_root=self.test_dir)
        
        with open(self.uni_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertEqual(content.count("[[Basi di Dati MOC]]"), 1)

    def test_corsi_moc_strictly_untouched(self):
        """Asserts Corsi.md is strictly untouched when initializing university courses per D-11."""
        with open(self.corsi_path, "r", encoding="utf-8") as f:
            initial_corsi = f.read()
            
        course_hub.init_course("Sistemi Operativi", vault_root=self.test_dir)
        
        with open(self.corsi_path, "r", encoding="utf-8") as f:
            current_corsi = f.read()
            
        self.assertEqual(initial_corsi, current_corsi)

    def test_natural_sort_key(self):
        """Asserts natural_sort_key correctly orders numeric prefixes per D-10."""
        titles = ["10 - Grafi", "01 - Introduzione", "02 - Algoritmi", "2 - Ricorsione"]
        sorted_titles = sorted(titles, key=course_hub.natural_sort_key)
        self.assertEqual(sorted_titles, ["01 - Introduzione", "02 - Algoritmi", "2 - Ricorsione", "10 - Grafi"])

    def test_parse_and_format_pacrar_table(self):
        """Asserts parse_pacrar_table extracts rows and format_pacrar_table regenerates Markdown correctly (D-05, D-09)."""
        body_lines = [
            "# Header",
            "",
            "## Matrice PACRAR",
            "",
            "| Argomento | P | A | C | R | A | R |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
            "| [[01 - Limiti]] | [x] | [-] | [ ] | [ ] | [ ] | [ ] |",
            "| [[02 - Derivate]] | [x] | [x] | [x] | [-] | [ ] | [ ] |",
            "",
            "## Formulari",
        ]
        start_idx, end_idx, rows = course_hub.parse_pacrar_table(body_lines)
        self.assertEqual(start_idx, 4)
        self.assertEqual(end_idx, 8)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["key"], "01 - limiti")
        self.assertEqual(rows[0]["states"], ["[x]", "[-]", "[ ]", "[ ]", "[ ]", "[ ]"])
        self.assertEqual(rows[1]["key"], "02 - derivate")
        self.assertEqual(rows[1]["states"], ["[x]", "[x]", "[x]", "[-]", "[ ]", "[ ]"])

        formatted = course_hub.format_pacrar_table(rows)
        self.assertEqual(len(formatted), 4)  # 2 header lines + 2 data rows
        self.assertIn("| [[01 - Limiti]] | [x] | [-] | [ ] | [ ] | [ ] | [ ] |", formatted)

    def test_merge_lessons_preserves_existing_checkboxes_100_percent(self):
        """Asserts new lessons are appended while preserving 100% of existing checkbox states per D-08, D-09."""
        existing_rows = [
            {"key": "01 - cinematica", "argomento": "[[01 - Cinematica]]", "states": ["[x]", "[-]", "[x]", "[ ]", "[ ]", "[ ]"]}
        ]
        new_lessons = ["01 - Cinematica", "02 - Dinamica"]
        merged = course_hub.merge_lessons_into_rows(existing_rows, new_lessons)

        row_01 = next(r for r in merged if r["key"] == "01 - cinematica")
        self.assertEqual(row_01["states"], ["[x]", "[-]", "[x]", "[ ]", "[ ]", "[ ]"])

        row_02 = next(r for r in merged if r["key"] == "02 - dinamica")
        self.assertEqual(row_02["states"], ["[ ]", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"])

    def test_merge_lessons_preserves_manual_unwritten_rows(self):
        """Asserts manual syllabus rows created by user without disk files are 100% preserved (D-08)."""
        existing_rows = [
            {"key": "01 - intro", "argomento": "[[01 - Intro]]", "states": ["[x]", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]},
            {"key": "manual row", "argomento": "Prossima Lezione da Registrare", "states": ["[-]", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]},
        ]
        # Only 01 exists on disk
        new_lessons = ["01 - Intro"]
        merged = course_hub.merge_lessons_into_rows(existing_rows, new_lessons)

        keys = [r["key"] for r in merged]
        self.assertIn("01 - intro", keys)
        self.assertIn("manual row", keys)

    def test_pipe_character_escaped_in_table(self):
        """Asserts pipe characters in titles are properly escaped outside wikilinks (T-13-03)."""
        rows = [
            {"key": "lezione pipe", "argomento": "Lezione su Pipe | e Flussi", "states": ["[ ]"] * 6}
        ]
        formatted = course_hub.format_pacrar_table(rows)
        # Must have \| in argomento
        data_line = [l for l in formatted if "Lezione su Pipe" in l][0]
        self.assertIn("Pipe \\| e Flussi", data_line)

    def test_sync_course_hub_e2e(self):
        """End-to-end test verifying lesson discovery, checkbox preservation, and natural sort (PACRAR-02, PACRAR-03)."""
        course_name = "Fisica Sperimentale"
        course_hub.init_course(course_name, vault_root=self.test_dir)

        course_dir = os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University", course_name)
        # Create 2 initial lesson files
        f1 = os.path.join(course_dir, "01 - Misure ed Errori.md")
        f2 = os.path.join(course_dir, "02 - Statistica.md")
        with open(f1, "w", encoding="utf-8") as f: f.write("# Misure\n")
        with open(f2, "w", encoding="utf-8") as f: f.write("# Statistica\n")

        # Initial sync
        course_hub.sync_course_hub(course_name, vault_root=self.test_dir)
        moc_path = os.path.join(self.test_dir, "01 - Map of Content", f"{course_name} MOC.md")
        with open(moc_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("| [[01 - Misure ed Errori]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |", content)

        # Simulate user manually ticking checkboxes on disk
        modified_content = content.replace(
            "| [[01 - Misure ed Errori]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |",
            "| [[01 - Misure ed Errori]] | [x] | [-] | [x] | [ ] | [ ] | [ ] |"
        )
        with open(moc_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        # Add 3rd lesson file: 10 - Laboratorio (tests natural numeric sort 10 after 02)
        f10 = os.path.join(course_dir, "10 - Laboratorio.md")
        with open(f10, "w", encoding="utf-8") as f: f.write("# Lab\n")

        # Resync
        course_hub.sync_course_hub(course_name, vault_root=self.test_dir)

        with open(moc_path, "r", encoding="utf-8") as f:
            resynced = f.read()

        # 100% preservation check
        self.assertIn("| [[01 - Misure ed Errori]] | [x] | [-] | [x] | [ ] | [ ] | [ ] |", resynced)
        # New lesson added
        self.assertIn("| [[10 - Laboratorio]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |", resynced)
        # Check order in lines
        idx_01 = resynced.find("[[01 - Misure ed Errori]]")
        idx_02 = resynced.find("[[02 - Statistica]]")
        idx_10 = resynced.find("[[10 - Laboratorio]]")
        self.assertTrue(idx_01 < idx_02 < idx_10, "Expected natural order 01 < 02 < 10")

    def test_obsidian_assets_integrity(self):
        """Asserts Obsidian mini-plugin pacrar-tracker and pacrar.css snippet exist and are properly registered (PACRAR-02, D-06)."""
        import json

        # 1. Manifest
        manifest_path = os.path.join(PROJECT_ROOT, ".obsidian", "plugins", "pacrar-tracker", "manifest.json")
        self.assertTrue(os.path.exists(manifest_path), "manifest.json should exist")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest.get("id"), "pacrar-tracker")
        self.assertFalse(manifest.get("isDesktopOnly"))

        # 2. Main.js
        main_path = os.path.join(PROJECT_ROOT, ".obsidian", "plugins", "pacrar-tracker", "main.js")
        self.assertTrue(os.path.exists(main_path), "main.js should exist")
        with open(main_path, "r", encoding="utf-8") as f:
            main_code = f.read()
        self.assertIn("class PacrarTrackerPlugin", main_code)
        self.assertIn("CHECKBOX_CYCLE", main_code)
        self.assertIn("SCORES", main_code)
        self.assertIn("mountSvgRing", main_code)

        # 3. Snippet
        snippet_path = os.path.join(PROJECT_ROOT, ".obsidian", "snippets", "pacrar.css")
        self.assertTrue(os.path.exists(snippet_path), "pacrar.css should exist")
        with open(snippet_path, "r", encoding="utf-8") as f:
            css_code = f.read()
        self.assertIn(".pacrar-progress-widget", css_code)
        self.assertIn("td.pacrar-cell", css_code)

        # 4. Community plugins registration
        comm_path = os.path.join(PROJECT_ROOT, ".obsidian", "community-plugins.json")
        with open(comm_path, "r", encoding="utf-8") as f:
            comm_plugins = json.load(f)
        self.assertIn("pacrar-tracker", comm_plugins)

        # 5. Appearance snippets registration
        app_path = os.path.join(PROJECT_ROOT, ".obsidian", "appearance.json")
        with open(app_path, "r", encoding="utf-8") as f:
            appearance = json.load(f)
        self.assertIn("pacrar", appearance.get("enabledCssSnippets", []))

    def test_sync_master_moc_with_children(self):
        """Asserts master MOC synchronizes PACRAR tables from child course MOCs."""
        child_moc_content = (
            "---\nstatus: permanent\ntype: moc\narea: education\nrelated: [\"[[University]]\"]\ntitle: \"Analisi 1 MOC\"\n"
            "date: '2026-09-01'\nupdated: 2026-09-01T10:00\ntags: [education/university]\nsummary: \"Test\"\n---\n"
            "[[Home MOC|Home]] / [[University|University MOC]] / [[Analisi 1 MOC]]\n\n"
            "# Analisi 1 — Course Hub\n\n## Matrice PACRAR\n\n"
            "| Argomento | P | A | C | R | A | R | Sintesi |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n"
            "| [[01 - Limiti]] | [x] | [x] | [x] | [ ] | [ ] | [ ] | Definizione di limite |\n"
            "| [[02 - Derivate]] | [x] | [-] | [ ] | [ ] | [ ] | [ ] | Rapporto incrementale |\n"
        )
        child_path = os.path.join(self.moc_dir, "Analisi 1 MOC.md")
        with open(child_path, "w", encoding="utf-8") as f:
            f.write(child_moc_content)

        master_moc_content = (
            "---\nstatus: permanent\ntype: moc\narea: education\nrelated: [\"[[University]]\"]\ntitle: \"Master Hub MOC\"\n"
            "date: '2026-09-01'\nupdated: 2026-09-01T10:00\ntags: [education/university]\nsummary: \"Master\"\n---\n"
            "[[Home MOC|Home]] / [[University|University MOC]] / [[Master Hub MOC]]\n\n"
            "# Master Hub\n\n## Matrice Globale\n\n"
            "### 1. Analisi 1\n*Hub dedicato:* [[Analisi 1 MOC]]\n\n"
            "| Lezione / Argomento | P | A | C | R | A | R | Stato / Sintesi |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n"
            "| [[01 - Limiti]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Vecchia sintesi |\n"
        )
        master_path = os.path.join(self.moc_dir, "Master Hub MOC.md")
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(master_moc_content)

        res = course_hub.sync_master_moc_with_children(master_path, vault_root=self.test_dir)
        self.assertTrue(res)

        with open(master_path, "r", encoding="utf-8") as f:
            updated_master = f.read()

        # Row 1 must have updated checkboxes from child
        self.assertIn("| [[01 - Limiti]] | [x] | [x] | [x] | [ ] | [ ] | [ ] |", updated_master)
        # Row 2 must have been appended from child
        self.assertIn("| [[02 - Derivate]] | [x] | [-] | [ ] | [ ] | [ ] | [ ] |", updated_master)

    def test_sync_master_mocs_for_course_auto_cascades(self):
        """Asserts sync_master_mocs_for_course detects and cascades updates to master MOCs referencing the course."""
        child_moc_content = (
            "---\nstatus: permanent\ntype: moc\narea: education\nrelated: [\"[[University]]\"]\ntitle: \"Geometria MOC\"\n"
            "date: '2026-09-01'\nupdated: 2026-09-01T10:00\ntags: [education/university]\nsummary: \"Test\"\n---\n"
            "[[Home MOC|Home]] / [[University|University MOC]] / [[Geometria MOC]]\n\n"
            "# Geometria — Course Hub\n\n## Matrice PACRAR\n\n"
            "| Argomento | P | A | C | R | A | R | Sintesi |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n"
            "| [[01 - Vettori]] | [x] | [x] | [x] | [x] | [x] | [x] | Spazi vettoriali |\n"
        )
        child_path = os.path.join(self.moc_dir, "Geometria MOC.md")
        with open(child_path, "w", encoding="utf-8") as f:
            f.write(child_moc_content)

        master_moc_content = (
            "---\nstatus: permanent\ntype: moc\narea: education\nrelated: [\"[[University]]\"]\ntitle: \"Ingegneria MOC\"\n"
            "date: '2026-09-01'\nupdated: 2026-09-01T10:00\ntags: [education/university]\nsummary: \"Master\"\n---\n"
            "[[Home MOC|Home]] / [[University|University MOC]] / [[Ingegneria MOC]]\n\n"
            "# Ingegneria Hub\n\n## Matrice Globale\n\n"
            "### 1. Geometria\n*Hub dedicato:* [[Geometria MOC]]\n\n"
            "| Lezione / Argomento | P | A | C | R | A | R | Stato / Sintesi |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n"
            "| [[01 - Vettori]] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Spazi vettoriali |\n"
        )
        master_path = os.path.join(self.moc_dir, "Ingegneria MOC.md")
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(master_moc_content)

        count = course_hub.sync_master_mocs_for_course("Geometria", vault_root=self.test_dir)
        self.assertEqual(count, 1)

        with open(master_path, "r", encoding="utf-8") as f:
            updated = f.read()
        self.assertIn("| [[01 - Vettori]] | [x] | [x] | [x] | [x] | [x] | [x] |", updated)

    def test_resolve_course_dir_nested_degree_structure(self):
        """Asserts resolve_course_dir finds nested courses under degree folders and preserves parentheses."""
        nested_dir = os.path.join(
            self.test_dir,
            "02 - Atlas",
            "Education & Learning",
            "University",
            "Ingegneria Informatica 2026-27",
            "Fondamenti di Matematica (Analisi 1)",
        )
        os.makedirs(nested_dir, exist_ok=True)

        # Should resolve to the nested folder instead of creating a top-level University folder
        resolved = course_hub.resolve_course_dir("Fondamenti di Matematica (Analisi 1)", vault_root=self.test_dir)
        self.assertEqual(os.path.abspath(resolved), os.path.abspath(nested_dir))

    def test_sync_all_courses_nested_degree_structure(self):
        """Asserts sync_all_courses iterates over nested course subdirectories and ignores degree containers."""
        degree_dir = os.path.join(
            self.test_dir,
            "02 - Atlas",
            "Education & Learning",
            "University",
            "Ingegneria Informatica 2026-27",
        )
        course_a = os.path.join(degree_dir, "Introduzione alla Programmazione")
        course_b = os.path.join(degree_dir, "Probabilità e Statistica")
        os.makedirs(course_a, exist_ok=True)
        os.makedirs(course_b, exist_ok=True)

        with open(os.path.join(course_a, "01 - Lezione Python.md"), "w", encoding="utf-8") as f:
            f.write("# Lezione Python")
        with open(os.path.join(course_b, "01 - Lezione Prob.md"), "w", encoding="utf-8") as f:
            f.write("# Lezione Prob")

        synced = course_hub.sync_all_courses(vault_root=self.test_dir)
        self.assertEqual(synced, 2)

        # Ensure no stray folder with spaces was created
        stray_dir = os.path.join(
            self.test_dir,
            "02 - Atlas",
            "Education & Learning",
            "University",
            "Ingegneria Informatica 2026 - 27",
        )
        self.assertFalse(os.path.exists(stray_dir))


if __name__ == "__main__":
    unittest.main()
