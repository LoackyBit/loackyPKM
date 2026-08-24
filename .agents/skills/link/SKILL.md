---
name: link
description: Scansiona una nota target e converte le occorrenze testuali di concetti e titoli del Vault in wiki-links funzionanti [[Nome Nota]].
---
# Skill: /link (Auto-linking Contestuale)

Questa skill analizza una nota target e arricchisce il grafo del Vault trasformando le occorrenze di testo semplice in wiki-links standard di Obsidian (`[[Nome Nota]]`).

## Workflow Esecutivo

1. **Acquisizione Target:**
   - Ricevi il percorso del file markdown da scansionare e leggine il contenuto.
2. **Mappatura Titoli del Vault:**
   - Esegui lo script helper `scripts/get_vault_titles.sh` per ottenere l'elenco completo dei titoli di tutte le note presenti nel Vault (ricavati dai nomi dei file `.md` e dai frontmatter).
3. **Analisi Semantica e Testuale:**
   - Confronta il testo della nota target con la lista dei titoli del Vault.
   - Individua occorrenze esatte, plurali o sinonimi evidenti di concetti esistenti nel Vault.
   - **Regole di Esclusione:**
     - Non toccare link già esistenti in formato `[[...]]` o `[...](...)`.
     - Non toccare testo all'interno di blocchi di codice (```...```) o frontmatter YAML.
     - Non linkare parole generiche o troppo corte (es. "R", "AI", "Note") a meno che non si riferiscano in modo inequivocabile a una nota specifica (es. `[[esercizio + appunti R]]`).
     - Applica il principio di parsimonia: inserisci il wiki-link solo alla prima o seconda occorrenza di un concetto nel documento, per evitare sovraccarico visivo.
4. **Refactoring e Salvataggio:**
   - Sostituisci nel testo le occorrenze selezionate con la sintassi `[[Nome Nota]]` o `[[Nome Nota|testo visualizzato]]` (se il testo nella frase è flesso o al plurale).
   - Sovrascrivi il file target con il contenuto aggiornato utilizzando i tool di editing.
