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
        os.makedirs(os.path.join(self.test_dir, "01 - Map of Content"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "02 - Atlas", "Education & Learning", "University"), exist_ok=True)
        
        # Minimal University.md
        self.uni_path = os.path.join(self.test_dir, "01 - Map of Content", "University.md")
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


if __name__ == "__main__":
    unittest.main()
