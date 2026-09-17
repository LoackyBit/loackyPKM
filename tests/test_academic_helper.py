#!/usr/bin/env python3
"""Hermetic Unit Tests for academic_helper.py (Wave 0 Test Harness).

Tests text extraction, boilerplate cleaning, escaped page references,
source attachment archiving with collision versioning, image filtering,
color normalization, SHA-256 deduplication, and fail-fast exceptions
using synthetic in-memory PDFs (PDF-02, PDF-03, D-01..D-10).
"""

import os
import sys
import io
import shutil
import random
import tempfile
import unittest
import hashlib
from typing import List, Tuple, Optional
from pathlib import Path

# Adjust sys.path to import academic_helper
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "99 - Meta", "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import pypdf
from pypdf.generic import DecodedStreamObject, NameObject, DictionaryObject, NumberObject
from PIL import Image

import academic_helper


class TestAcademicHelper(unittest.TestCase):
    """Test suite for academic_helper.py."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.course_name = "Ricerca Operativa"
        self.attachments_dir = os.path.join(self.test_dir, "99 - Meta", "Attachments", self.course_name)
        self.clipboard_dir = os.path.join(self.test_dir, "99 - Meta", "Clipboard", self.course_name)
        os.makedirs(self.attachments_dir, exist_ok=True)
        os.makedirs(self.clipboard_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_synthetic_pdf(
        self,
        filename: str,
        pages_text: List[str],
        images: Optional[List[Optional[Tuple[Image.Image, str]]]] = None,
        password: Optional[str] = None
    ) -> str:
        """Helper to create a synthetic in-memory PDF with pypdf."""
        writer = pypdf.PdfWriter()
        font_dict = DictionaryObject({
            NameObject('/Type'): NameObject('/Font'),
            NameObject('/Subtype'): NameObject('/Type1'),
            NameObject('/BaseFont'): NameObject('/Helvetica')
        })

        img_refs = []
        if images:
            for item in images:
                if item is None:
                    img_refs.append(None)
                    continue
                img, cs = item
                img_buf = io.BytesIO()
                img.save(img_buf, format='JPEG')
                img_data = img_buf.getvalue()

                img_stream = DecodedStreamObject()
                img_stream.set_data(img_data)
                img_stream[NameObject('/Type')] = NameObject('/XObject')
                img_stream[NameObject('/Subtype')] = NameObject('/Image')
                img_stream[NameObject('/Width')] = NumberObject(img.width)
                img_stream[NameObject('/Height')] = NumberObject(img.height)
                img_stream[NameObject('/ColorSpace')] = NameObject('/' + cs)
                img_stream[NameObject('/BitsPerComponent')] = NumberObject(8)
                img_stream[NameObject('/Filter')] = NameObject('/DCTDecode')

                ref = writer._add_object(img_stream)
                img_refs.append(ref)

        for i, txt in enumerate(pages_text):
            page = writer.add_blank_page(width=612, height=792)
            stream_cmds = ['BT', '/F1 12 Tf', '50 750 Td']
            for line in txt.splitlines():
                esc = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
                stream_cmds.append(f'({esc}) Tj')
                stream_cmds.append('0 -15 Td')
            stream_cmds.append('ET')

            stream = DecodedStreamObject()
            stream.set_data('\n'.join(stream_cmds).encode('latin-1'))
            page[NameObject('/Contents')] = stream

            res_dict = DictionaryObject()
            res_font = DictionaryObject()
            res_font[NameObject('/F1')] = font_dict
            res_dict[NameObject('/Font')] = res_font

            if img_refs and i < len(img_refs) and img_refs[i] is not None:
                xobj_dict = DictionaryObject()
                xobj_dict[NameObject(f'/Im{i+1}')] = img_refs[i]
                res_dict[NameObject('/XObject')] = xobj_dict

            page[NameObject('/Resources')] = res_dict

        if password:
            writer.encrypt(password)

        pdf_path = os.path.join(self.test_dir, filename)
        with open(pdf_path, 'wb') as f:
            writer.write(f)

        return pdf_path

    def _create_high_entropy_image(self, size: Tuple[int, int] = (200, 200), mode: str = "RGB") -> Image.Image:
        """Generates an image with enough entropy so that compressed PNG bytes > 10KB."""
        im = Image.new(mode, size)
        rng = random.Random(42)
        if mode == "CMYK":
            pixels = [tuple(rng.randint(0, 255) for _ in range(4)) for _ in range(size[0] * size[1])]
        else:
            pixels = [tuple(rng.randint(0, 255) for _ in range(3)) for _ in range(size[0] * size[1])]
        im.putdata(pixels)
        return im

    # -------------------------------------------------------------------------
    # Task 16-01-01 Tests: Tracer Slice, Text Extraction, Boilerplate, Archive
    # -------------------------------------------------------------------------

    def test_extract_pdf_data_continuous_stream_and_escaped_page_references(self):
        """Asserte that text is structured as a continuous unified stream without '### Slide'
        and contains escaped page citations: \\[[[file.pdf#page=N|N]]] (D-01, PDF-02)."""
        pages = [
            "Introduzione alla Ricerca Operativa e Programmazione Lineare.\nFormulazione del problema canonico con vincoli di disuguaglianza.",
            "Definizione geometrica della regione ammissibile e poliedri convessi.\nTeorema fondamentale della programmazione lineare."
        ]
        pdf_path = self._create_synthetic_pdf("Lezione 01.pdf", pages)

        result = academic_helper.extract_pdf_data(
            pdf_path,
            course=self.course_name,
            vault_root=self.test_dir
        )

        self.assertEqual(result["title"], "Lezione 01")
        self.assertEqual(result["course"], self.course_name)
        self.assertEqual(result["page_count"], 2)

        raw_text = result["raw_text"]
        # Must not contain ### Slide N
        self.assertNotIn("### Slide", raw_text)
        self.assertNotIn("### slide", raw_text)

        # Must contain escaped page references
        self.assertIn("\\[[[Lezione 01.pdf#page=1|1]]]", raw_text)
        self.assertIn("\\[[[Lezione 01.pdf#page=2|2]]]", raw_text)

        # Must contain continuous content from both pages
        self.assertIn("Programmazione Lineare", raw_text)
        self.assertIn("poliedri convessi", raw_text)

    def test_clean_slide_boilerplate(self):
        """Asserte that recurring headers, footers, slide numbers, and academic years
        are epurated across slides while keeping core content (D-02)."""
        pages = [
            (1, "Prof. Mario Rossi\nCorso di Ricerca Operativa\nConcetti base di grafi e reti di flusso.\nSlide 1 / 4\nA.A. 2024/2025"),
            (2, "Prof. Mario Rossi\nCorso di Ricerca Operativa\nAlgoritmo di Ford e Fulkerson per flusso massimo.\nSlide 2 / 4\nA.A. 2024/2025"),
            (3, "Prof. Mario Rossi\nCorso di Ricerca Operativa\nTeorema del taglio minimo e dualita.\nSlide 3 / 4\nA.A. 2024/2025"),
            (4, "Prof. Mario Rossi\nCorso di Ricerca Operativa\nComplessita polinomiale dell'algoritmo di Edmonds-Karp.\nSlide 4 / 4\nA.A. 2024/2025"),
        ]

        cleaned = academic_helper.clean_slide_boilerplate(pages)

        # All pages should still exist
        self.assertEqual(len(cleaned), 4)

        for page_num, text in cleaned:
            # Recurring boilerplate must be removed
            self.assertNotIn("Prof. Mario Rossi", text)
            self.assertNotIn("Corso di Ricerca Operativa", text)
            self.assertNotIn("A.A. 2024/2025", text)
            self.assertNotIn(f"Slide {page_num} / 4", text)

        # Core content must be preserved
        self.assertIn("Concetti base di grafi", cleaned[0][1])
        self.assertIn("Algoritmo di Ford e Fulkerson", cleaned[1][1])
        self.assertIn("Teorema del taglio minimo", cleaned[2][1])
        self.assertIn("algoritmo di Edmonds-Karp", cleaned[3][1])

    def test_pdf_encrypted_error_raised(self):
        """Asserte that encrypted or password protected PDFs raise PdfEncryptedError (D-09)."""
        pages = ["Testo segreto protetto da crittografia simmetrica con password complessa."]
        pdf_path = self._create_synthetic_pdf("Protetto.pdf", pages, password="StrongPassword123")

        with self.assertRaises(academic_helper.PdfEncryptedError):
            academic_helper.extract_pdf_data(
                pdf_path,
                course=self.course_name,
                vault_root=self.test_dir
            )

    def test_pdf_text_unavailable_error_raised(self):
        """Asserte that PDFs with total characters < 50 raise PdfTextUnavailableError (D-09)."""
        pages = ["Testo breve"]  # 11 characters < 50
        pdf_path = self._create_synthetic_pdf("ScansioneVuota.pdf", pages)

        with self.assertRaises(academic_helper.PdfTextUnavailableError):
            academic_helper.extract_pdf_data(
                pdf_path,
                course=self.course_name,
                vault_root=self.test_dir
            )

    def test_archive_pdf_attachment_deduplication_and_versioning(self):
        """Asserte that archiving PDF reuses identical SHA files without duplicates,
        and applies (v2), (v3) versioning when content differs (D-08, D-10)."""
        pdf1_path = self._create_synthetic_pdf("Slide Deck.pdf", [
            "Contenuto prima versione della lezione di Programmazione Dinamica molto esteso e dettagliato."
        ])

        # 1. First archive: creates base "Slide Deck.pdf"
        final_name_1, perm_path_1 = academic_helper.archive_pdf_attachment(
            pdf1_path, self.attachments_dir, "Slide Deck"
        )
        self.assertEqual(final_name_1, "Slide Deck.pdf")
        self.assertTrue(os.path.exists(perm_path_1))

        # 2. Re-archive same file: returns same name without writing duplicate
        final_name_2, perm_path_2 = academic_helper.archive_pdf_attachment(
            pdf1_path, self.attachments_dir, "Slide Deck"
        )
        self.assertEqual(final_name_2, "Slide Deck.pdf")
        self.assertEqual(perm_path_1, perm_path_2)

        # 3. Archive updated/different content with same stem: creates (v2)
        pdf2_path = self._create_synthetic_pdf("Slide Deck Updated.pdf", [
            "Contenuto differente aggiornato dal professore per l'anno successivo con nuovi esercizi."
        ])
        final_name_3, perm_path_3 = academic_helper.archive_pdf_attachment(
            pdf2_path, self.attachments_dir, "Slide Deck"
        )
        self.assertEqual(final_name_3, "Slide Deck (v2).pdf")
        self.assertTrue(os.path.exists(perm_path_3))
        self.assertNotEqual(perm_path_1, perm_path_3)

        # 4. Re-archiving the v2 file: reuses (v2)
        final_name_4, perm_path_4 = academic_helper.archive_pdf_attachment(
            pdf2_path, self.attachments_dir, "Slide Deck"
        )
        self.assertEqual(final_name_4, "Slide Deck (v2).pdf")
        self.assertEqual(perm_path_3, perm_path_4)

        # 5. Archive yet another different file: creates (v3)
        pdf3_path = self._create_synthetic_pdf("Slide Deck Final.pdf", [
            "Terza versione delle slide con errata corrige e dimostrazioni complete del simplesso."
        ])
        final_name_5, perm_path_5 = academic_helper.archive_pdf_attachment(
            pdf3_path, self.attachments_dir, "Slide Deck"
        )
        self.assertEqual(final_name_5, "Slide Deck (v3).pdf")
        self.assertTrue(os.path.exists(perm_path_5))

    # -------------------------------------------------------------------------
    # Task 16-01-02 Tests: Image Extraction, Filtering, Pillow, SHA Deduplication
    # -------------------------------------------------------------------------

    def test_image_filtering_rejects_small_dimensions_and_low_bytes(self):
        """Asserte that images with dimension <= 150px or size <= 10KB are rejected (PDF-03)."""
        # Small image 100x100 (dimension filter rejects)
        small_im = Image.new("RGB", (100, 100), color="blue")
        # Large image 200x200 but flat uniform color (compression yields < 10KB, byte filter rejects)
        flat_im = Image.new("RGB", (200, 200), color="green")

        pages = [
            "Prima pagina con immagine piccola che deve essere scartata dal filtro dimensionale.",
            "Seconda pagina con immagine piatta uniforme che deve essere scartata dal filtro byte."
        ]
        pdf_path = self._create_synthetic_pdf(
            "FilterTest.pdf",
            pages,
            images=[(small_im, "DeviceRGB"), (flat_im, "DeviceRGB")]
        )

        result = academic_helper.extract_pdf_data(
            pdf_path,
            course=self.course_name,
            vault_root=self.test_dir
        )

        page_images = result["page_images"]
        # Both images must be rejected
        total_images = sum(len(imgs) for imgs in page_images.values())
        self.assertEqual(total_images, 0)
        self.assertEqual(len(os.listdir(self.clipboard_dir)), 0)

    def test_image_extraction_and_sha_deduplication(self):
        """Asserte that valid images (>150px, >10KB) are saved as Title Case PNGs,
        and identical images on multiple slides are deduplicated via SHA-256 (D-04, D-07, PDF-03)."""
        # High entropy image (>150px, >10KB)
        entropy_im = self._create_high_entropy_image((250, 250), mode="RGB")

        pages = [
            "Prima slide che introduce l'architettura del sistema di calcolo distribuito.",
            "Seconda slide che ripropone la medesima architettura con focus sul nodo centrale."
        ]
        # Inject the same image on both slide 1 and slide 2
        pdf_path = self._create_synthetic_pdf(
            "Architettura Calcolo.pdf",
            pages,
            images=[(entropy_im, "DeviceRGB"), (entropy_im, "DeviceRGB")]
        )

        result = academic_helper.extract_pdf_data(
            pdf_path,
            course=self.course_name,
            vault_root=self.test_dir
        )

        page_images = result["page_images"]
        self.assertIn(1, page_images)
        self.assertIn(2, page_images)
        self.assertEqual(len(page_images[1]), 1)
        self.assertEqual(len(page_images[2]), 1)

        img1_info = page_images[1][0]
        img2_info = page_images[2][0]

        # First image: newly saved
        self.assertFalse(img1_info["reused"])
        self.assertTrue(img1_info["filename"].startswith("Figura - Architettura Calcolo - p1 - 1"))
        self.assertTrue(img1_info["filename"].endswith(".png"))

        # Second image: deduplicated reuse!
        self.assertTrue(img2_info["reused"])
        self.assertEqual(img2_info["filename"], img1_info["filename"])
        self.assertEqual(img2_info["wikilink"], img1_info["wikilink"])
        self.assertEqual(img2_info["sha256"], img1_info["sha256"])

        # Exactly ONE image file written to disk in Clipboard/<Course>/
        saved_files = os.listdir(self.clipboard_dir)
        self.assertEqual(len(saved_files), 1)
        self.assertEqual(saved_files[0], img1_info["filename"])

    def test_cmyk_color_mode_normalization(self):
        """Asserte that CMYK images are safely converted to RGB and saved as valid PNGs (D-06)."""
        cmyk_im = self._create_high_entropy_image((220, 220), mode="CMYK")
        pages = ["Slide con immagine in spazio colore CMYK tipica di slide destinate alla stampa."]

        pdf_path = self._create_synthetic_pdf(
            "Stampa Slide.pdf",
            pages,
            images=[(cmyk_im, "DeviceCMYK")]
        )

        result = academic_helper.extract_pdf_data(
            pdf_path,
            course=self.course_name,
            vault_root=self.test_dir
        )

        page_images = result["page_images"]
        self.assertEqual(len(page_images[1]), 1)
        saved_name = page_images[1][0]["filename"]

        saved_path = os.path.join(self.clipboard_dir, saved_name)
        self.assertTrue(os.path.exists(saved_path))

        # Verify that the saved file is a valid RGB PNG readable by Pillow
        with Image.open(saved_path) as opened_im:
            self.assertEqual(opened_im.format, "PNG")
            self.assertEqual(opened_im.mode, "RGB")
            self.assertEqual(opened_im.size, (220, 220))

    def test_concurrency_and_idempotency(self):
        """Asserte that repeated extractions of the same PDF are idempotent and do not duplicate assets."""
        entropy_im = self._create_high_entropy_image((200, 200), mode="RGB")
        pages = ["Test di concorrenza e idempotenza per verificare che non vengano creati duplicati."]
        pdf_path = self._create_synthetic_pdf("Idempotenza.pdf", pages, images=[(entropy_im, "DeviceRGB")])

        # Run 1
        res1 = academic_helper.extract_pdf_data(pdf_path, course=self.course_name, vault_root=self.test_dir)
        # Run 2
        res2 = academic_helper.extract_pdf_data(pdf_path, course=self.course_name, vault_root=self.test_dir)

        # Output properties match exactly
        self.assertEqual(res1["pdf_filename"], res2["pdf_filename"])
        self.assertEqual(res1["raw_text"], res2["raw_text"])

        # No duplicate attachments
        att_files = [f for f in os.listdir(self.attachments_dir) if not f.startswith('.')]
        self.assertEqual(len(att_files), 1)

        # No duplicate clipboard images
        clip_files = [f for f in os.listdir(self.clipboard_dir) if not f.startswith('.')]
        self.assertEqual(len(clip_files), 1)


if __name__ == '__main__':
    unittest.main()
