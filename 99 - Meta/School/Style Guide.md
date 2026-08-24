---
status: permanent
type: concept
area: meta
related: []
source: original
title: "Style Guide"
date: '2026-04-21'
updated: 2026-07-07T01:20
tags: []
summary: "<mark style=\"background:rgba(255, 193, 69, 0.32)\"<font color=\"#cc8800\"<bparola</b</font</mark — parole chiave ASSOLUTE, concetti-cardine, tesi critiche fondamentali"
---
[[Home MOC|Home]] / [[School]] / [[Style Guide]]

## Gerarchia evidenziatori (FONDAMENTALE)

- `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>parola</b></font></mark>` — parole chiave ASSOLUTE, concetti-cardine, tesi critiche fondamentali

- `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>parola</b></font></mark>` — parole importanti COLLEGATE alle gialle (nomi propri, luoghi, concetti secondari), o di minor importanza rispetto alle gialle. Le parole viola sono di solito più frequenti rispetto alle gialle, perché le gialle racchiudono tante di quelle viola

- Non abusare dei colori: le evidenziazioni gialle devono restare più rare e marcate, quelle viola più frequenti ma sempre mirate. Per capire ‘quanto’ colore usare, guarda la frequenza delle evidenziazioni presenti in [[Gabriele d'Annunzio]] e [[Giovanni Pascoli]] (le due note create da me, originali)

- applica il codice html così com'è, sostituendo 'parola'

- **grassetto normale** senza html — enfasi generica su parole o frasi rilevanti

## Formattazione

- Corsivo (_titolo_) per titoli di opere

- Citazioni per frasi celebri:
```
>[!quote] Autore
> testo
```
- Domande (solo se richieste):
``` 
>[!question] domanda
> risposta
```

- Tabelle: usa sempre il formato **Markdown standard** (no HTML) per garantire la corretta visualizzazione in Obsidian.

- Toggle: `#### Titolo` poi contenuto indentato con tab

- Separatori: `---` tra blocchi tematicamente distinti

- Elenchi numerati per fasi/periodi cronologici

- Elenchi puntati per caratteristiche/temi

- Link interni: incorporati inline nella prosa — mai in una sezione separata "Vedi anche". esempio: [[Giovanni Pascoli#^4ae267|Giovanni Pascoli - esempio collegamento blocco ‘fonosimbolismo’]]
## Tono e registro

- Sintetico ma discorsivo, NON accademico

- Spiega i "perché" dietro i fatti ("questo serve a...", "la chiave è...", "non è solo X ma anche Y...")

- Usa nessi causali tra biografia e opera

- Non si limita a elencare: contestualizza e interpreta

- Stile diretto: "Pascoli rifiuta...", "D'Annunzio vede nel teatro..."

## Frontmatter

```yaml
---
title: Nome Nota
date: YYYY-MM-DD        # data della lezione — da 99 - Meta/School/list.md
updated: YYYY-MM-DDTHH:MM
status: draft           # draft | stable | needs-update | stub
cadence: hot            # hot (7d) | tactical (30d) | iron-cold (60d) | frozen
type:                   # autore | movimento | opera | testo | evento | periodo | concetto | artista | argomento | entità | persona
sources:
---

- [[nota collegata]]
- [[altra nota collegata]]
```

---
## Collegamenti
