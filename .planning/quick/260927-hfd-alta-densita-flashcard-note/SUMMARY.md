---
status: complete
quick_id: 260927-hfd
slug: alta-densita-flashcard-note
title: "Alta Densità Flashcard Anki su Note Universitarie e Integrazione Regole Second Brain"
date: '2026-09-27'
---

# Quick Task Summary: Alta Densità Flashcard Anki su Note Universitarie e Integrazione Regole Second Brain

## Sintesi delle Attività
È stata rimossa la limitazione restrittiva previgente (5-10 card per lezione) ed è stata stabilita la nuova regola permanente di **alta densità sistematica di flashcard Anki** per tutte le note create nel Vault. La nuova convenzione è stata integrata a livello di sistema in `.agents/MEMORY.md`, `GEMINI.md`, `AGENTS.md`, `.agents/skills/brain-ingest/SKILL.md` e nel prompt generator di `99 - Meta/Scripts/brain_ingest.py`.

In parallelo, sono state analizzate tutte le 4 note universitarie attive del primo anno di Ingegneria Informatica e la loro densità di flashcard è stata incrementata da 33 a 56 card (+23 flashcard atomiche), coprendo capillarmente teoremi, definizioni, assiomi, proprietà e dimostrazioni formali.

---

## Modifiche Normative & Integrazione Second Brain

1. **`.agents/MEMORY.md`:**
   - Aggiornata la Sezione 1 sancendo la regola permanente: **ALTA DENSITÀ SISTEMATICA (REGOLA PERMANENTE)**. Nessun limite restrittivo di 5-10 card: ogni concetto cardine evidenziato (`<mark>`), definizione formale, assioma, teorema (con enunciato o dimostrazione chiave), proprietà algebrica o legge logica deve avere la propria flashcard dedicata inline.
2. **`GEMINI.md`:**
   - Aggiornata la convenzione Anki (riga 111): le flashcard devono essere rigorosamente contestuali, inline e ad alta densità sistematica, eliminando la dicitura "(indicativamente 5-10 card per lezione)".
3. **`AGENTS.md`:**
   - Inserita la convenzione ufficiale sulle Flashcard Anki con prescrizione di alta densità sistematica e divieto assoluto di appendici finali a fondo pagina.
4. **`.agents/skills/brain-ingest/SKILL.md`:**
   - Rimosso il limite "5-10 per lezione" e aggiornata la specifica del prompt e del protocollo di generazione con l'alta densità sistematica.
5. **`99 - Meta/Scripts/brain_ingest.py`:**
   - Aggiornato il prompt di generazione AI (riga 855) imponendo la generazione ad alta densità sistematica per l'active recall Anki.

---

## Incremento Densità Note Universitarie (+23 Flashcard)

| Nota | Card Precedenti | Nuove Card | Totale | Principali Nuovi Argomenti Coperti |
| :--- | :---: | :---: | :---: | :--- |
| **`01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione`** | 7 | +8 | **15** | Congiunzione e disgiunzione inclusiva (vel vs aut), Equivalenza logica e doppia implicazione, Legge del terzo escluso (*tertium non datur*), Dimostrazione per assurdo, Definizione di predicato logico, Variabili libere vs legate, Ordine e dipendenza nei quantificatori multipli, Dimostrazione per contronominale della parità del quadrato. |
| **`02 - Teoria degli Insiemi`** | 13 | +8 | **21** | Principio della doppia inclusione, Assioma della coppia non ordinata e singoletto, Intersezione di una famiglia di insiemi, Perché l'unione richiede un assioma autonomo, Proprietà distributive insiemistiche, Dimostrazione formale di De Morgan per complementari, Definizione di insiemi per elencazione, Assioma di fondazione e divieto di auto-appartenenza ($x \notin x$). |
| **`01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità`** | 6 | +3 | **9** | Operazioni insiemistiche fondamentali in $\Omega$ (unione, intersezione, complementare, differenza), Spazio campionario ed eventi elementari, Tipologie di eventi (certo, impossibile, esaustivi). |
| **`01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python`** | 7 | +4 | **11** | Tecnica dei raffinamenti successivi (top-down), Componenti dell'architettura di von Neumann (CPU, RAM, BUS, I/O), Tipizzazione dinamica e forte in Python, Differenza tra SyntaxError ed eccezioni a runtime. |
| **TOTALE FLASHCARD UNIVERSITÀ** | **33** | **+23** | **56** | **Tutte le card conformi al 100% alle specifiche Anki e validate.** |

---

## Validazione & Test Suite
- `anki_helper.py --audit`: Scansionate 65 card totali nel vault, 0 errori sintattici, 0 collisioni di ID, integrità verificata.
- `python3 -m unittest discover tests`: Eseguiti tutti i 267 test unitari con esito positivo (`OK`).
