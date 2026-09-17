#!/usr/bin/env python3
"""Academic Helper Module — Low-level PDF slide ingestion, structured text extraction,
boilerplate cleaning, image filtering (>150px, >10KB), SHA-256 deduplication,
and permanent attachment archiving (PDF-01, PDF-02, PDF-03, D-01..D-10).
"""

import os
import sys
import re
import io
import shutil
import hashlib
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set

# External library imports with graceful fallback guards
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from PIL import Image
except ImportError:
    Image = None


# Custom Exception Hierarchy
class AcademicHelperError(Exception):
    """Base exception for academic helper errors."""
    pass


class PdfEncryptedError(AcademicHelperError):
    """Raised when a PDF file is encrypted or password-protected (D-09)."""
    pass


class PdfTextUnavailableError(AcademicHelperError):
    """Raised when a PDF yields insufficient text (<50 chars, raster scan) (D-09)."""
    pass


def get_vault_root(start_path: Optional[str] = None) -> str:
    """Dynamically resolves the root path of the Second Brain vault."""
    if start_path:
        return os.path.abspath(start_path)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Verify if candidate contains standard directories
    for check_dir in ("01 - Map of Content", "02 - Atlas", "99 - Meta"):
        if os.path.isdir(os.path.join(candidate, check_dir)):
            return candidate

    return candidate


def clean_slide_boilerplate(pages_text: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Removes repetitive headers, footers, slide numbers, and academic years across slides (D-02).

    Identifies candidate boilerplate lines from the first 2 and last 2 non-empty lines
    of each slide that appear in >= 30% of slides (for documents with >= 3 slides).
    Also strips standalone slide numbers and academic year references at edges.
    """
    if len(pages_text) < 3:
        return pages_text

    # Count candidate lines occurring in edge positions (first 2 or last 2 non-empty lines)
    line_counts = Counter()
    for _, text in pages_text:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            continue
        edge_candidates = set(lines[:2] + lines[-2:])
        for cand in edge_candidates:
            norm = re.sub(r'\s+', ' ', cand).strip().lower()
            if len(norm) > 2:
                line_counts[norm] += 1

    # Frequency threshold: 30% of total slides, min 2
    threshold = max(2, int(len(pages_text) * 0.30))
    boilerplate_set: Set[str] = {norm for norm, count in line_counts.items() if count >= threshold}

    re_slide_counter = re.compile(r'^\s*(?:slide\s*)?\d+\s*(?:/\s*\d+)?\s*$', re.IGNORECASE)
    re_year = re.compile(r'a\.a\.\s*\d{4}[/-]\d{4}', re.IGNORECASE)

    cleaned_pages: List[Tuple[int, str]] = []
    for page_num, text in pages_text:
        raw_lines = text.splitlines()
        non_empty_indices = [i for i, l in enumerate(raw_lines) if l.strip()]
        if not non_empty_indices:
            cleaned_pages.append((page_num, ""))
            continue

        edge_indices = set(non_empty_indices[:2] + non_empty_indices[-2:])
        out_lines: List[str] = []

        for idx, line in enumerate(raw_lines):
            s_line = line.strip()
            if not s_line:
                continue

            norm = re.sub(r'\s+', ' ', s_line).strip().lower()
            is_edge = idx in edge_indices

            if is_edge:
                if norm in boilerplate_set:
                    continue
                if re_slide_counter.match(s_line):
                    continue
                if re_year.search(s_line) and len(s_line) < 40:
                    continue

            out_lines.append(s_line)

        cleaned_pages.append((page_num, "\n".join(out_lines)))

    return cleaned_pages


def archive_pdf_attachment(
    source_pdf_path: str,
    attachments_dir: str,
    clean_stem: str
) -> Tuple[str, str]:
    """Permanently archives PDF to Attachments directory with SHA-256 deduplication
    and versioning (v2), (v3) on naming collision with different content (D-08, D-10).

    Returns:
        Tuple of (final_filename, permanent_filepath)
    """
    os.makedirs(attachments_dir, exist_ok=True)

    with open(source_pdf_path, "rb") as sf:
        src_bytes = sf.read()
    src_sha = hashlib.sha256(src_bytes).hexdigest()

    base_name = f"{clean_stem}.pdf"
    target_path = os.path.join(attachments_dir, base_name)

    # If source is already the target path, return as is
    if os.path.abspath(source_pdf_path) == os.path.abspath(target_path):
        return base_name, target_path

    if not os.path.exists(target_path):
        shutil.copy2(source_pdf_path, target_path)
        return base_name, target_path

    # Check collision on base_name
    with open(target_path, "rb") as tf:
        if hashlib.sha256(tf.read()).hexdigest() == src_sha:
            return base_name, target_path

    # Different content collision: incremental versioning (v2), (v3)...
    v = 2
    while True:
        v_name = f"{clean_stem} (v{v}).pdf"
        v_path = os.path.join(attachments_dir, v_name)

        if os.path.abspath(source_pdf_path) == os.path.abspath(v_path):
            return v_name, v_path

        if not os.path.exists(v_path):
            shutil.copy2(source_pdf_path, v_path)
            return v_name, v_path

        with open(v_path, "rb") as vf:
            if hashlib.sha256(vf.read()).hexdigest() == src_sha:
                return v_name, v_path

        v += 1


def extract_and_deduplicate_images(
    reader: Any,
    pdf_stem: str,
    course_clipboard_dir: str,
    min_dim: int = 150,
    min_bytes: int = 10240
) -> Dict[int, List[Dict[str, Any]]]:
    """Extracts images from PDF pages, applies dimension and byte size filtering (>150px, >10KB),
    normalizes colorspace via Pillow (RGB/RGBA), deduplicates via SHA-256, and saves PNGs
    to course_clipboard_dir with Title Case naming (D-04, D-06, D-07).

    Returns:
        Dict mapping page_num (1-indexed) to list of image metadata dicts:
        {
            'filename': 'Figura - ... - pN - M.png',
            'wikilink': '![[Figura - ... - pN - M.png]]',
            'sha256': '...',
            'reused': bool,
            'page': int
        }
    """
    if Image is None:
        return {}

    os.makedirs(course_clipboard_dir, exist_ok=True)

    # Build existing SHA-256 hash map from course clipboard directory
    sha_to_filename: Dict[str, str] = {}
    if os.path.isdir(course_clipboard_dir):
        for entry in os.listdir(course_clipboard_dir):
            if entry.lower().endswith(('.png', '.jpg', '.jpeg')) and not entry.startswith('.'):
                fpath = os.path.join(course_clipboard_dir, entry)
                try:
                    with open(fpath, "rb") as ef:
                        existing_sha = hashlib.sha256(ef.read()).hexdigest()
                        sha_to_filename[existing_sha] = entry
                except Exception:
                    continue

    page_images_map: Dict[int, List[Dict[str, Any]]] = {}

    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        page_images_map[page_num] = []
        img_counter = 1

        try:
            images = getattr(page, 'images', [])
        except Exception:
            continue

        for img_obj in images:
            try:
                pil_img = img_obj.image
            except Exception:
                continue

            if pil_img is None:
                continue

            w, h = pil_img.size
            # Dimensional filter: both width and height must exceed min_dim (150px)
            if w <= min_dim or h <= min_dim:
                continue

            # Color mode normalization via Pillow
            buf = io.BytesIO()
            try:
                if pil_img.mode == "CMYK":
                    # Convert CMYK to RGB
                    rgb_img = pil_img.convert("RGB")
                    rgb_img.save(buf, format="PNG", optimize=True)
                elif pil_img.mode in ("RGBA", "LA") or (pil_img.mode == "P" and "transparency" in pil_img.info):
                    # Preserve alpha channel
                    pil_img.save(buf, format="PNG", optimize=True)
                elif pil_img.mode == "P":
                    # Indexed palette without transparency -> RGB
                    rgb_img = pil_img.convert("RGB")
                    rgb_img.save(buf, format="PNG", optimize=True)
                elif pil_img.mode in ("RGB", "L"):
                    pil_img.save(buf, format="PNG", optimize=True)
                else:
                    rgb_img = pil_img.convert("RGB")
                    rgb_img.save(buf, format="PNG", optimize=True)
            except Exception:
                # Fallback conversion to RGB on any unexpected mode error
                try:
                    buf = io.BytesIO()
                    rgb_img = pil_img.convert("RGB")
                    rgb_img.save(buf, format="PNG", optimize=True)
                except Exception:
                    continue

            img_bytes = buf.getvalue()

            # Byte size filter: must exceed min_bytes (10240 bytes / 10KB)
            if len(img_bytes) <= min_bytes:
                continue

            # Cryptographic SHA-256 hash calculation for strict deduplication
            img_sha = hashlib.sha256(img_bytes).hexdigest()

            if img_sha in sha_to_filename:
                # Deduplication hit: reuse existing file reference without disk duplication
                existing_name = sha_to_filename[img_sha]
                page_images_map[page_num].append({
                    "filename": existing_name,
                    "wikilink": f"![[{existing_name}]]",
                    "sha256": img_sha,
                    "reused": True,
                    "page": page_num
                })
            else:
                # Unique asset: Title Case canonical naming per D-04
                target_filename = f"Figura - {pdf_stem} - p{page_num} - {img_counter}.png"
                target_path = os.path.join(course_clipboard_dir, target_filename)

                # Avoid overwriting unexpected existing file of same name
                if os.path.exists(target_path):
                    with open(target_path, "rb") as ef:
                        if hashlib.sha256(ef.read()).hexdigest() == img_sha:
                            sha_to_filename[img_sha] = target_filename
                            page_images_map[page_num].append({
                                "filename": target_filename,
                                "wikilink": f"![[{target_filename}]]",
                                "sha256": img_sha,
                                "reused": True,
                                "page": page_num
                            })
                            img_counter += 1
                            continue
                    target_filename = f"Figura - {pdf_stem} - p{page_num} - {img_counter}_{img_sha[:8]}.png"
                    target_path = os.path.join(course_clipboard_dir, target_filename)

                with open(target_path, "wb") as out_f:
                    out_f.write(img_bytes)

                sha_to_filename[img_sha] = target_filename
                page_images_map[page_num].append({
                    "filename": target_filename,
                    "wikilink": f"![[{target_filename}]]",
                    "sha256": img_sha,
                    "reused": False,
                    "page": page_num
                })
                img_counter += 1

    return page_images_map


def extract_pdf_data(
    pdf_path: str,
    course: Optional[str] = None,
    vault_root: Optional[str] = None,
    min_dim: int = 150,
    min_bytes: int = 10240
) -> Dict[str, Any]:
    """Main extraction engine for PDF slides (PDF-02, PDF-03, D-01..D-10).

    Extracts text per slide, removes boilerplate, verifies character threshold,
    formats continuous stream with escaped page references:
        \\[[[file.pdf#page=N|N]]]
    filters and deduplicates images into Clipboard/<Course>/, and permanently archives
    the source PDF into Attachments/<Course>/ with collision versioning.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
        PdfEncryptedError: If PDF is encrypted/password protected.
        PdfTextUnavailableError: If total extracted text < 50 characters (raster scan).
        AcademicHelperError: On pypdf import or read errors.
    """
    if pypdf is None:
        raise AcademicHelperError("Libreria pypdf non installata nel runtime Python.")

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File PDF non trovato: {pdf_path}")

    root = get_vault_root(vault_root)

    try:
        reader = pypdf.PdfReader(pdf_path)
    except Exception as e:
        raise AcademicHelperError(f"Impossibile aprire il file PDF: {e}")

    # Decryption check: attempt empty password (standard permissions)
    if reader.is_encrypted:
        try:
            reader.decrypt("")
            if reader.is_encrypted:
                raise PdfEncryptedError("Il file PDF è cifrato o protetto da password.")
        except PdfEncryptedError:
            raise
        except Exception:
            raise PdfEncryptedError("Il file PDF è cifrato o protetto da password.")

    # Extract raw text from all pages
    raw_pages: List[Tuple[int, str]] = []
    total_chars = 0
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        raw_pages.append((page_num, txt))
        total_chars += len(txt.strip())

    # Fail-fast check for raster scans or empty layers (D-09)
    if total_chars < 50:
        raise PdfTextUnavailableError(
            f"Testo estratto insufficiente ({total_chars} caratteri < 50). "
            "Il PDF potrebbe essere una scansione rasterizzata priva di OCR."
        )

    # Clean slide boilerplate across pages (D-02)
    cleaned_pages = clean_slide_boilerplate(raw_pages)

    # Resolve course and target attachment / clipboard directories
    subfolder = course.strip() if course and course.strip() else "General"
    # Basic sanitize for folder creation to prevent directory traversal
    subfolder_clean = re.sub(r'[\\/:*?"<>|]', '', subfolder).strip()
    if not subfolder_clean:
        subfolder_clean = "General"

    attachments_dir = os.path.join(root, "99 - Meta", "Attachments", subfolder_clean)
    clipboard_dir = os.path.join(root, "99 - Meta", "Clipboard", subfolder_clean)

    # Clean stem for file naming
    raw_stem = Path(pdf_path).stem
    # Sanitize stem removing illegal filesystem chars and normalizing spaces
    clean_stem = re.sub(r'[:*?"<>|/\\]', '', raw_stem).strip()
    if not clean_stem:
        clean_stem = "Slide PDF"

    # Permanently archive the source PDF (D-08, D-10)
    final_pdf_filename, permanent_pdf_path = archive_pdf_attachment(
        pdf_path, attachments_dir, clean_stem
    )

    # Extract, filter (>150px, >10KB), and deduplicate images (D-04, D-06, D-07)
    page_images = extract_and_deduplicate_images(
        reader, clean_stem, clipboard_dir, min_dim=min_dim, min_bytes=min_bytes
    )

    # Format unified continuous text with escaped page references:
    # \[[[nome.pdf#page=N|N]]] (D-01)
    formatted_sections: List[str] = []
    for page_num, text in cleaned_pages:
        s_text = text.strip()
        if not s_text:
            continue
        page_ref = f"\\[[[{final_pdf_filename}#page={page_num}|{page_num}]]]"
        formatted_sections.append(f"{s_text} {page_ref}")

    continuous_text = "\n\n".join(formatted_sections)

    return {
        'title': clean_stem,
        'course': course,
        'pdf_filename': final_pdf_filename,
        'permanent_pdf_path': permanent_pdf_path,
        'page_count': len(reader.pages),
        'raw_text': continuous_text,
        'page_images': page_images,
        'total_chars': total_chars
    }
