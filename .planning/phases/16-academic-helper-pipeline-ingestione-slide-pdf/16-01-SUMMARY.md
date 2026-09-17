---
phase: 16-academic-helper-pipeline-ingestione-slide-pdf
plan: "01"
subsystem: ingestion
tags: [pypdf, pillow, pdf, slides, academic, deduplication]
requires: []
provides:
  - academic-pdf-extractor
  - slide-boilerplate-cleaner
  - visual-asset-deduplicator
  - permanent-attachment-archiver
affects:
  - 99 - Meta/Scripts/academic_helper.py
  - tests/test_academic_helper.py
tech-stack:
  added: []
  patterns:
    - continuous-stream-escaped-citations
    - edge-slide-boilerplate-cleaning
    - sha256-image-deduplication
    - collision-attachment-versioning
key-files:
  created:
    - 99 - Meta/Scripts/academic_helper.py
    - tests/test_academic_helper.py
  modified: []
key-decisions:
  - "D-01: Formattazione testo PDF a flusso continuo unificato senza divisori '### Slide N' con rimandi inline sfuggiti: \\[[[nome.pdf#page=N|N]]]"
  - "D-02: Pulizia boilerplate automatica basata su frequenza (>=30%) delle righe ai bordi della diapositiva (prime/ultime 2 righe)"
  - "D-04 & PDF-03: Naming canonico Title Case per le immagini estratte: Figura - <NomeSlidePDF> - p<N> - <Index>.png"
  - "D-06 & D-07: Normalizzazione spazi colore con Pillow (RGB/RGBA) e deduplica stretta tramite digest SHA-256 dei byte PNG"
  - "D-08 & D-10: Archiviazione permanente in Attachments/<NomeCorso>/ con gestione collisioni e versionamento (v2) per mantenere stabili i link Obsidian"
  - "D-09: Fail-fast su PDF cifrati (PdfEncryptedError) e su scansioni raster con testo < 50 caratteri (PdfTextUnavailableError)"
requirements-completed:
  - PDF-02
  - PDF-03
duration: 3 min
completed: 2026-09-17T23:30:30+02:00
coverage:
  - deliverable: "academic_helper.py low-level PDF text extraction and continuous stream formatting with escaped page references"
    verification:
      kind: test
      ref: tests/test_academic_helper.py#TestAcademicHelper.test_extract_pdf_data_continuous_stream_and_escaped_page_references
      status: pass
    human_judgment: false
  - deliverable: "clean_slide_boilerplate algorithm stripping recurring edge lines, slide counters, and academic years"
    verification:
      kind: test
      ref: tests/test_academic_helper.py#TestAcademicHelper.test_clean_slide_boilerplate
      status: pass
    human_judgment: false
  - deliverable: "archive_pdf_attachment with SHA-256 deduplication and (v2) collision versioning"
    verification:
      kind: test
      ref: tests/test_academic_helper.py#TestAcademicHelper.test_archive_pdf_attachment_deduplication_and_versioning
      status: pass
    human_judgment: false
  - deliverable: "extract_and_deduplicate_images with >150px and >10KB filtering, Pillow normalization, and SHA-256 deduplication"
    verification:
      kind: test
      ref: tests/test_academic_helper.py#TestAcademicHelper.test_image_extraction_and_sha_deduplication
      status: pass
    human_judgment: false
  - deliverable: "Fail-fast detection of encrypted PDFs and insufficient text (<50 chars)"
    verification:
      kind: test
      ref: tests/test_academic_helper.py#TestAcademicHelper.test_pdf_encrypted_error_raised
      status: pass
    human_judgment: false
---

# Phase 16 Plan 01: Modulo academic_helper.py con estrattore PDF, filtraggio selettivo delle immagini e deduplica SHA-256 in Clipboard/<NomeCorso>/ Summary

Modulo specializzato `99 - Meta/Scripts/academic_helper.py` implementato con estrazione testo per slide, pulizia boilerplate euristica (D-02), sintassi con escape `\[[[nome.pdf#page=N|N]]]` (D-01), archiviazione permanente con versionamento `(v2)` in `99 - Meta/Attachments/<NomeCorso>/` (D-08, D-10), filtraggio immagini (>150px, >10KB), normalizzazione Pillow e deduplica crittografica SHA-256 (D-04, D-06, D-07, PDF-03).

## Key Accomplishments

1. **Tracer Slice & Text Extraction (PDF-02, D-01, D-02):**
   - Riconoscimento ed estrazione testo tramite `pypdf.PdfReader` con gestione della decifratura vuota (`decrypt("")`).
   - Rilevamento fail-fast di file protetti da password (`PdfEncryptedError`) e scansioni raster senza OCR con $<50$ caratteri (`PdfTextUnavailableError`).
   - Algoritmo `clean_slide_boilerplate` per eliminare intestazioni ricorrenti ($\ge 30\%$), contatori di pagina e anni accademici.
   - Formattazione a flusso continuo unificato con citazioni inline a tre parentesi quadre con escape: `\[[[nome.pdf#page=N|N]]]`.

2. **Archiviazione Permanente PDF & Gestione Collisioni (D-08, D-10):**
   - Funzione `archive_pdf_attachment` che copia il PDF in `99 - Meta/Attachments/<NomeCorso>/` (o `General/`).
   - Se il file esiste con medesimo hash SHA-256, viene riutilizzato senza duplicazione.
   - Se il contenuto differisce (aggiornamento slide), viene generato progressivamente il nome versionato `<Stem> (v2).pdf`, `(v3).pdf` preservando l'integrità dei riferimenti preesistenti.

3. **Filtro Qualitativo Immagini & Deduplica SHA-256 (PDF-03, D-04, D-06, D-07):**
   - Funzione `extract_and_deduplicate_images` che scarta elementi grafici con larghezza o altezza $\le 150\text{px}$ oppure peso compresso $\le 10\text{KB}$.
   - Normalizzazione spazi colore con Pillow (`CMYK` convertito in `RGB`, canali alfa preservati per `RGBA`/`LA`/`P` trasparente).
   - Calcolo hash SHA-256: immagini duplicate su più diapositive riutilizzano il primo file salvato con `reused: True` e medesimo wikilink `![[Figura - ...]]`.
   - Naming Title Case canonico: `Figura - <pdf_stem> - p<N> - <index>.png`.

4. **Wave 0 Test Harness Ermetica:**
   - Creata suite `tests/test_academic_helper.py` con generazione in-memory di PDF sintetici tramite `pypdf.PdfWriter` ed iniezione XObject.
   - 9 test unitari focalizzati, eseguiti al 100% con successo in 0.22s.
   - Suite globale del repository confermata verde (219 test passati).

## Deviations from Plan

None - plan executed exactly as written.

## Verification

Tutti i test unitari di Plan 16-01 e la regression suite globale sono stati eseguiti con esito positivo:
```bash
python3 -m unittest tests/test_academic_helper.py
# Ran 9 tests in 0.224s - OK
python3 -m unittest discover tests/
# Ran 219 tests in 14.172s - OK
```

## Self-Check: PASSED
