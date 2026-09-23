---
id: 260923-uv9
title: "Integrazione direttive inline AI %% AI: ... %%"
type: quick-task
status: complete
date: 2026-09-23
---

# Quick Task 260923-uv9: Integrazione direttive inline AI %% AI: ... %% - Summary

## Sintesi Risultati
Implementato il supporto organico e nativo per le direttive operative inline all'IA nel motore di ingestione, nella test suite e nella documentazione normativa del Vault:

1. **Parser & Sanitizzazione Regex (`99 - Meta/Scripts/brain_ingest.py`)**:
   - Implementata la funzione helper `strip_ai_directives(text)` per intercettare e rimuovere deterministamente:
     - Commenti nativi Obsidian: `%% AI: ... %%` (e `%% IA: ... %%`)
     - Commenti HTML standard: `<!-- AI: ... -->` (e `<!-- IA: ... -->`)
     - Callout dedicati a direttive: `> [!note]- AI: ...` o `> [!todo]- AI: ...`
   - Integrata la Regola 7 nel system prompt AI di `rewrite_note_with_ai`: istruisce il modello a eseguire tali direttive come comandi prioritari assoluti (ridimensionamento immagini, focus selettivo, schemi o formule) e a non includerle nel markdown finale.
   - Applicata sanitizzazione automatica dell'output in `rewrite_note_with_ai` e nella fallback `format_structured_note`.

2. **Test Suite (`tests/test_brain_ingest.py` e `tests/test_templates.py`)**:
   - Aggiunti test unitari `test_strip_ai_directives` e `test_format_structured_note_strips_ai_directives`.
   - Aggiornato `tests/test_templates.py` per distinguere i template di intera nota (`Nota Vault.md`, `Articolo Blog.md`, `Raw Inbox Note.md`) dai template snippet inline (`AI Instruction.md`), con test dedicato `test_ai_instruction_snippet`.
   - Esecuzione completa: 257 test passati con successo (0 errori, 0 fallimenti).

3. **Allineamento Normativo e Documentazione del Vault**:
   - **`99 - Meta/Style Guide.md`**: Aggiunta la specifica formale delle Direttive Inline per l'IA (`%% AI: ... %%`), con divieto di parentesi quadre inverse `]...[` (che rompono l'evidenziazione di CodeMirror).
   - **`GEMINI.md`**: Aggiornata la sezione 4 delle Regole e Convenzioni Operative per recepire la sintassi e il template snippet `AI Instruction.md`.
   - **`AGENTS.md`**: Sincronizzate le convenzioni markdown e visive.
   - **`.agents/skills/brain-ingest/SKILL.md`**: Aggiunto lo standard visivo punto 7 relativo alle direttive operative utente.
