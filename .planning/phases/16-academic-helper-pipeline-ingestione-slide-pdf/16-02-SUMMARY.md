---
phase: 16-academic-helper-pipeline-ingestione-slide-pdf
plan: "02"
subsystem: ingestion
tags: [pdf, course-hub, pacrar, attachments, brain-ingest, brain-health]
requires:
  - 16-01
provides:
  - pdf-unified-ingestion-routing
  - pacrar-matrix-auto-registration
  - permanent-source-attachment-preservation
  - attachments-governance-audit
affects:
  - 99 - Meta/Scripts/brain_ingest.py
  - 99 - Meta/Scripts/brain_health.py
  - tests/test_brain_ingest_course.py
tech-stack:
  added: []
  patterns:
    - polymorphic-pdf-input-detection
    - permanent-attachment-preservation-on-gtd-promote
    - pacrar-matrix-auto-registration-hook
    - recursive-clipboard-asset-purge
    - attachments-versioning-and-duplicate-audit
key-files:
  created: []
  modified:
    - 99 - Meta/Scripts/brain_ingest.py
    - 99 - Meta/Scripts/brain_health.py
    - tests/test_brain_ingest_course.py
key-decisions:
  - "D-08 & D-13: Preservazione permanente dell'allegato originale in 99 - Meta/Attachments/<NomeCorso>/ durante la promozione GTD e registrazione automatica della lezione nella matrice PACRAR del Course Hub con stato iniziale [ ]"
  - "D-09: Gestione fail-fast su PDF cifrati e scansioni senza OCR con registrazione diagnostica in 03 - Inbox/Review Dashboard.md tramite record_ingest_error()"
  - "D-10: Audit automatico in brain_health.py per rilevare file slide versionati (v2) e duplicati SHA-256 in 99 - Meta/Attachments/"
  - "D-11: Routing universale per PDF con flag --course '<NomeCorso>' o fallback su 99 - Meta/Attachments/General/ con classificazione semantica Atlas"
  - "D-12, D-14 & D-17: Piena compatibilità dell'ingestione slide con le direttive metacognitive ADC (--nlm) e prompt di arricchimento AI per trattazione continua priva di divisori rigidi"
requirements-completed:
  - PDF-01
  - PDF-02
  - PDF-03
duration: 4 min
completed: 2026-09-17T23:33:30+02:00
coverage:
  - deliverable: "detect_input_type recognizing .pdf files and routing to academic_helper with --course or General fallback"
    verification:
      kind: test
      ref: tests/test_brain_ingest_course.py#TestBrainIngestCourse.test_ingest_pdf_with_course_flag_creates_attachment_and_draft
      status: pass
    human_judgment: false
  - deliverable: "Diagnostic error recording in Review Dashboard for encrypted or empty scan PDFs"
    verification:
      kind: test
      ref: tests/test_brain_ingest_course.py#TestBrainIngestCourse.test_ingest_pdf_encrypted_or_empty_records_review_dashboard_error
      status: pass
    human_judgment: false
  - deliverable: "Preservation of permanent attachments in 99 - Meta/Attachments/ and PACRAR matrix auto-registration on GTD promotion"
    verification:
      kind: test
      ref: tests/test_brain_ingest_course.py#TestBrainIngestCourse.test_promote_pdf_lesson_updates_pacrar_and_preserves_attachment
      status: pass
    human_judgment: false
  - deliverable: "Recursive purge of extracted clipboard figures on draft rejection"
    verification:
      kind: test
      ref: tests/test_brain_ingest_course.py#TestBrainIngestCourse.test_purge_pdf_lesson_removes_clipboard_images
      status: pass
    human_judgment: false
  - deliverable: "Audit of versioned (v2) and duplicate SHA-256 attachments in brain_health.py"
    verification:
      kind: test
      ref: tests/test_brain_ingest_course.py#TestBrainIngestCourse.test_audit_pdf_attachments_detects_versioned_and_duplicates
      status: pass
    human_judgment: false
---

# Phase 16 Plan 02: Integrazione in brain_ingest.py del flag --course, lifecycle a 3 fasi e staging con Review Dashboard Summary

Integrazione completata tra `brain_ingest.py`, `academic_helper.py`, `course_hub.py` e `brain_health.py` per l'ingestione unificata delle slide universitarie in PDF, con preservazione permanente degli allegati, auto-registrazione PACRAR, gestione errori diagnostici, purga ricorsiva delle figure su scarto e audit governance degli allegati (PDF-01, PDF-02, PDF-03).

## Key Accomplishments

1. **Routing Polimorfico & Gestione Parametri CLI (PDF-01, D-11):**
   - Riconoscimento automatico dei file `.pdf` in `detect_input_type(source)`.
   - Routing con `--course "<NomeCorso>"`: archiviazione permanente in `99 - Meta/Attachments/<NomeCorso>/`, inizializzazione automatica Course Hub con matrice PACRAR e destinazione `02 - Atlas/Education & Learning/University/<NomeCorso>`.
   - Fallback controllato per PDF senza corso: archiviazione in `99 - Meta/Attachments/General/` e classificazione semantica standard in Atlas.

2. **Ciclo di Vita Ingestion a 3 Macro-Fasi & Prompt AI Arricchito (PDF-02, D-01, D-03, D-05, D-12, D-14):**
   - *Fase 1/3:* Estrazione del flusso continuo unificato, pulizia boilerplate e salvataggio dell'estratto grezzo temporaneo in `03 - Inbox/Source/<Titolo>.md`.
   - *Fase 2/3:* Prompt AI aggiornato per elaborare il testo in flusso continuo privo di divisori rigidi `### Slide N` (D-01), preservare le citazioni inline con escape `\[[[nome.pdf#page=N|N]]]` (D-16), riallineare codice/tabelle (D-03) e incorporare figure (`![[Figura - ...]]`) a valle dei concetti chiave (D-05), con piena sinergia con il flag `--nlm` (D-14).
   - *Fase 3/3:* Calcolo breadcrumb accademico e staging bozza in `03 - Inbox/Draft/<Titolo>.md` con riga di approvazione interattiva in `03 - Inbox/Review Dashboard.md`.

3. **Gestione Errori & Fail-Fast Diagnostico (D-09):**
   - Intercettazione tempestiva di `PdfEncryptedError` e `PdfTextUnavailableError` in `ingest_source()`.
   - Registrazione diagnostica dell'errore nella sezione `## ⚠️ Errori di Acquisizione Recenti` di `Review Dashboard.md` tramite `record_ingest_error()`.
   - Pulizia dello stato in-progress senza generazione di note vuote o bozze corrotte.

4. **Promozione GTD & Preservazione Allegati (D-08, D-13):**
   - All'approvazione `[x]`, `_handle_promote_item` promuove la nota in Atlas e chiama automaticamente `course_hub.register_lesson()`, aggiungendo la lezione alla matrice PACRAR dell'hub di corso con stato iniziale `[ ]`.
   - Il file PDF permanente in `99 - Meta/Attachments/<NomeCorso>/` viene rigorosamente preservato (l'eliminazione è circoscritta all'estratto testuale temporaneo in `Source/`).
   - Al rifiuto `[-]`, `_handle_purge_item` effettua una scansione ricorsiva di `99 - Meta/Clipboard/` eliminando le figure collegate anche nelle sottocartelle di corso.

5. **Governance Allegati in `brain_health.py` (D-10):**
   - Implementata `audit_pdf_attachments(vault_root)` che scansiona ricorsivamente `Attachments/` per identificare file versionati `(v2)` e duplicati con medesimo digest SHA-256.
   - Esposizione della metrica statica nella sezione `## Metriche Generali del Vault` di `Vault Health Dashboard.md`.

6. **Integrazione Test Suite & Verifica End-to-End:**
   - Estesa la suite `tests/test_brain_ingest_course.py` con 8 test mirati di integrazione.
   - Suite globale del repository verificata al 100% verde (225 test passati con successo).

## Deviations from Plan

None - plan executed exactly as written.

## Verification

```bash
python3 -m unittest tests/test_brain_ingest_course.py
# Ran 8 tests in 0.166s - OK
python3 -m unittest tests/test_academic_helper.py
# Ran 9 tests in 0.237s - OK
python3 -m unittest discover tests/
# Ran 225 tests in 14.101s - OK
```

## Self-Check: PASSED
