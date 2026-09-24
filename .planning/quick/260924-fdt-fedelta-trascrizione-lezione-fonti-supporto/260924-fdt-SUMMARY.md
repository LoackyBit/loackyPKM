---
id: 260924-fdt
slug: fedelta-trascrizione-lezione-fonti-supporto
title: "Fedeltà alla nota originale e alla trascrizione della lezione con dispense e slide come fonti di supporto in brain-ingest"
date: 2026-09-24
type: quick-summary
status: complete
---

# Quick Task 260924-fdt: Fedeltà alla nota originale e alla trascrizione della lezione con dispense e slide come fonti di supporto in brain-ingest

## Sintesi Esecutiva
Implementata la direttiva vincolante sulla **gerarchia delle fonti** in `brain-ingest`:
- **Fonte Primaria:** La nota originale dell'utente e la trascrizione audio della lezione costituiscono l'asse portante narrativo e il perimetro concettuale vincolante. La nota concettuale permanente generata NON deve mai discostarsi da quanto effettivamente spiegato, argomentato ed esposto dal docente a lezione o riportato negli appunti originali.
- **Fonti di Supporto:** Le dispense universitarie, le slide PDF e gli altri appunti ausiliari hanno uno scopo puramente ausiliario e di supporto. Servono per formalizzare le definizioni, recuperare l'esatta notazione matematica LaTeX per passaggi e formule menzionate a voce, aggiungere richiami precisi alle slide (`\[[[file.pdf#page=N|Slide N]]]`) ed estrarre tabelle o figure pertinenti, con **divieto assoluto di divagazioni o iper-estensioni enciclopediche** su capitoli o argomenti non affrontati a lezione.

## Modifiche Eseguite
1. **Aggiornamento logica di aggregazione in `99 - Meta/Scripts/brain_ingest.py` (`resolve_inbox_dependencies`)**:
   - Delimitazione esplicita della nota primaria con header:
     `=== NOTA ORIGINALE / CATTURA PRIMARIA DELL'UTENTE ===`
     `[Asse portante: non discostarsi troppo da questi appunti e dalla trascrizione]`
   - Etichettatura della trascrizione audio come `FONTE PRIMARIA: Trascrizione Audio Lezione` con vincolo di ricalcare fedelmente la spiegazione del docente.
   - Etichettatura di dispense/slide PDF come `FONTE DI SUPPORTO: Dispense / Slide PDF` con specifica del ruolo ausiliario formale/visivo senza discostarsi dalla lezione.
   - Etichettatura di note secondarie come `FONTE DI SUPPORTO: Appunti Ausiliari`.
2. **Aggiornamento Prompt di Rielaborazione AI (`enrich_draft_with_ai`)**:
   - Riformulata la Regola 1 come `1. GERARCHIA DELLE FONTI, FEDELTÀ ALLA LEZIONE E SEQUENZA LOGICO-TEMPORALE (TAX-01, D-06)`.
   - Introdotto divieto categorico di allargare la trattazione a capitoli, lemmi o interi argomenti presenti nelle dispense/slide ma non affrontati dal docente a lezione.
   - Rafforzata la Regola 6 specificando il ruolo di supporto e ancoraggio didattico delle slide PDF.
   - Rinumerata la sezione flashcard Anki opzionale a Regola 8.
3. **Aggiornamento Documentazione di Sistema e System Prompt**:
   - `GEMINI.md`: Aggiornata la specifica di `brain-ingest` e aggiunta la regola dedicata nella sezione 4 ("Regole e Convenzioni Operative").
   - `AGENTS.md`: Integrata la convenzione "Primary Lecture Source Fidelity & Supporting Materials" sotto gli standard visivi e Style Guide.
   - `.agents/skills/brain-ingest/SKILL.md`: Aggiunto il punto 10 ("Gerarchia delle Fonti & Fedeltà alla Lezione").
4. **Test Unitari di Verifica (`tests/test_brain_ingest.py`)**:
   - Aggiunto `test_resolve_inbox_dependencies_source_hierarchy_markers` per verificare la presenza e correttezza dei marcatori di gerarchia fonti.
   - Aggiunto `test_enrich_draft_with_ai_prompt_source_fidelity` per verificare la presenza dei vincoli vincolanti nel prompt generato per `agy`.
   - Eseguiti 93 test in `tests/test_brain_ingest.py` e 29 test in `tests/test_brain_health.py`: 100% OK senza warning.
