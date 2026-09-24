---
id: 260924-orz
slug: non-salvare-in-memory-md-ma-integra-nel-
title: "Integrazione regole didattiche e visuali nel sistema Second Brain (senza MEMORY.md)"
date: 2026-09-24
type: quick-summary
status: complete
---

# Quick Task Summary: Integrazione Regole nel Sistema Second Brain

In risposta alla direttiva dell'utente (*"non salvare in MEMORY.md ma integra nel sistema di Second Brain"*), le convenzioni e le regole critiche relative alla gestione delle lezioni universitarie e alla qualità visiva delle note sono state rimosse da `.agents/MEMORY.md` e integrate permanentemente all'interno dell'architettura e della documentazione di sistema del Second Brain.

## Interventi Effettuati

### 1. Pulizia di `.agents/MEMORY.md`
- Rimossa la Sezione 5 precedentemente aggiunta ("Gestione Fonti Accademiche, Citazioni Slide e Diagrammi Visuali").
- Mantenuti inalterati il profilo utente e i vincoli metodologici storici (PACRAR, Anki inline, Zero emoji, ecc.).

### 2. Integrazione nel Sistema Second Brain
- **`GEMINI.md`:**
  - **Sezione 3 (`brain-ingest`):** integrata la direttiva su citazioni esclusive a materiali accademici di valore (slide, paper, testi) con divieto assoluto di citare trascrizioni audio grezze; densità calibrata dei richiami `\[[[...#page=N|Slide N]]]`; divieto assoluto di diagrammi simbolici ASCII/Unicode complessi in favore di transclusioni PNG ad alta risoluzione o tabelle native.
  - **Sezione 4 (`Regole e Convenzioni Operative`):** codificate le regole vincolanti per l'assistente di sistema su fonti didattiche e divieto di box-drawing monospazio.
- **`AGENTS.md`:**
  - Aggiornate le convenzioni operative e la sezione Style Guide con le regole di citazione slide e divieto ASCII box art.
- **`.agents/skills/brain-ingest/SKILL.md`:**
  - Aggiunti i punti 8 e 9 alla sezione 4 ("Standard Visivi & Style Guide del Vault"), specificando dettagliatamente la sintassi `\[[[NomeFile.pdf#page=N|Slide N]]]`, il divieto di citazione trascrizioni, e l'approccio alle grafiche e schemi visuali.
- **`99 - Meta/Style Guide.md`:**
  - Integrata in *Anatomia delle Note e Tipografia* la regola sulle citazioni a slide/fonti accademiche e il divieto assoluto di grafiche con caratteri box-drawing (`┌┐└┘`, `│`, `──►`), con indicazione di usare render PNG ad alta risoluzione (`![[Schema - ... .png]]`) o tabelle Markdown standard reattive.
- **`99 - Meta/Scripts/brain_ingest.py`:**
  - Aggiornata la Regola 6 del prompt master di rielaborazione concettuale per istruire l'AI a non citare mai le trascrizioni audio, calibrare la densità dei richiami alle slide d'aula ed evitare schemi ASCII/Unicode box-drawing a favore di transclusioni di figure o tabelle standard.

## Verifica
- Compilazione Python di `99 - Meta/Scripts/brain_ingest.py` superata senza errori.
- Test suite automatizzata (`python3 -m unittest discover tests`): eseguiti tutti i 261 test con esito positivo (`OK`).
