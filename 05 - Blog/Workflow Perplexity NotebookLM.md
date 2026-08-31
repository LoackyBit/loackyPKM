---
stage: raw 🗂️
draft: false
type: article
area: tech
related: []
source: original
title: "Workflow Perplexity Notebooklm"
date: '2026-04-03'
updated: 2026-07-12T21:35
tags: [meta/workflow, tech/notion, tech/notebooklm, tech/gemini, tech/perplexity, tech/produttività, tech/studio, tech/maturità]
summary: "Perplexity non supporta l'allegato diretto di interi notebook come fonte di contesto."
---
[[Home MOC|Home]] / [[Blog]] / [[Workflow Perplexity NotebookLM|Workflow Perplexity Notebooklm]]

## Il problema

[[Perplexity]] non supporta l'allegato diretto di interi notebook come fonte di contesto.
[[GEMINI]], invece, permette di caricare e leggere notebook completi in un'unica sessione.
La soluzione è usare i due strumenti in sequenza, sfruttando i punti di forza di ciascuno.

## Il flusso

Il workflow si articola in tre stadi:

0. **NotebookLM** — il notebook esiste già, con le fonti caricate (spesso già pronto).
1. **Gemini** — legge l'intero notebook e produce un *briefing operativo strutturato* con tutti gli argomenti che Perplexity dovrà affrontare nella pagina Notion.
2. **Perplexity** — riceve il briefing come contesto e crea la pagina Notion rispettando la guida di stile dello Spazio.

L'output di Gemini non deve essere un riassunto narrativo, ma una **scaletta editoriale gerarchica**: priorità assolute, parole-chiave cardine, parole-chiave collegate, struttura per sezioni, testi in programma con breve analisi.

## Prompt Gemini (estrattore)

```text
Devi leggere TUTTO il notebook allegato e trasformarlo in un briefing operativo per Perplexity.

OBIETTIVO
Non devi scrivere la pagina Notion finale.
Devi preparare una LISTA COMPLETA, ordinata e pulita di TUTTI gli argomenti che Perplexity dovrà affrontare.

REGOLE FONDAMENTALI
- Usa SOLO le informazioni contenute nel notebook.
- Non inventare nulla.
- Se un'informazione è dubbia, segnala [da verificare].
- Devi distinguere ciò che è centrale da ciò che è secondario.
- Devi segnalare collegamenti tra biografia, poetica e opere.
- Devi segnalare quali testi/opere richiedono una breve analisi.
- Se compaiono interpretazioni critiche o parole-concetto ricorrenti, mettile in evidenza.

FORMATO DI OUTPUT
TITOLO PAGINA: [nome autore o argomento]
TIPO PAGINA: [autore / opera / tema / movimento]
PRIORITÀ ASSOLUTE DA TRATTARE: ...
PAROLE-CHIAVE CARDINE: ...
PAROLE-CHIAVE COLLEGATE: ...
STRUTTURA CONSIGLIATA: Vita → Poetica → Opere principali → Testi in programma → Nodi critici

Poi per ciascuna sezione: elenco puntato di tutti i contenuti essenziali, con [da verificare] dove necessario.
L'output deve essere pensato per essere incollato direttamente in Perplexity come contesto di lavoro.
```

## Prompt Perplexity (scrittore)

```text
Ti inoltro un briefing estratto da un notebook tramite Gemini.

Crea UNA pagina Notion completa seguendo:
1. il briefing qui sotto;
2. la guida di stile di questo spazio;
3. la struttura tipica delle pagine di letteratura italiana.

Regole:
- Usa il briefing come fonte primaria.
- Non inventare informazioni mancanti.
- Mantieni i tag [da verificare].
- Tono sintetico ma discorsivo, con nessi causali.
- Prima elenca in chat la struttura che creerai, poi crea la pagina.

BRIEFING:
[INCOLLA QUI L'OUTPUT DI GEMINI]
```

## Variante a due prompt Gemini

Per risultati più puliti, si possono usare due prompt in sequenza in Gemini:

- **Prompt A** — "estrai tutto dal notebook"
- **Prompt B** — "ripulisci e comprimi per Perplexity" (elimina ripetizioni, unifica punti simili, mantieni tutti i contenuti essenziali senza scrivere in stile discorsivo)

Questa variante è utile quando il notebook è molto denso o le fonti sono ridondanti.

## Errori comuni

- Usare Gemini per scrivere direttamente la pagina Notion → il risultato non rispetta la guida di stile dello Spazio.
- Incollare in Perplexity un riassunto narrativo invece di un briefing strutturato → Perplexity perde la gerarchia delle informazioni.
- Dimenticare il tag `[da verificare]` nel briefing → Perplexity potrebbe "completare" le lacune inventando dati.

---
## Collegamenti

- [[Notion]]
- [[Guida di stile - letteratura italiana]]
- [[Esame di Stato 2026]]
- [[NotebookLM]]
- [[GEMINI]]
- [[Perplexity Spaces]]
