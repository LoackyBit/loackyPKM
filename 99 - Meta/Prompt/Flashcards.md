---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Flashcards"
date: '2025-09-10'
updated: 2026-05-24T21:56
tags: []
summary: "Ho allegato un documento con flashcards, genera file .txt distinti per ogni tipo di flashcard (es. Basic e Cloze). Ogni file deve contenere solo le carte di quel tipo, formattate per l'importazione..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Flashcards]]

```
Ho allegato un documento con flashcards, genera file .txt distinti per ogni tipo di flashcard (es. Basic e Cloze). Ogni file deve contenere solo le carte di quel tipo, formattate per l'importazione su Anki con i seguenti criteri:

- Usa il separatore pipe | tra i campi.
- Per le carte Basic: includi tre campi (fronte | retro | tags).
- Per le carte Cloze: includi due campi (testo con {{c1::}} | tags), senza campo retro.
- Converti TUTTE i riferimenti matematici o fisici (non tralasciare nessuna variabile, costante, equazione, funzione ecc.) in formato compatibile con Anki usando il tag html <anki-mathjax>, dopo il tag di chiusura </anki-mathjax> inserisci uno spazio ' '
- Usa tag pertinenti senza #, separati da spazi.
- Ogni file .txt deve essere un artefatto separato con un artifact_id unico, un titolo che indichi il tipo di flashcard (es. "Basic_flashcards.txt", "Cloze_flashcards.txt") e contentType "text/plain".
- Non includere spiegazioni o testo fuori dagli artefatti.
- Le parentesi graffe `{}` nelle flashcards originali possono indicare sia il contenuto da nascondere nelle carte cloze sia la sintassi LaTeX. Bisogna interpretare il contenuto tra parentesi graffe come quello da rendere nascosto con la sintassi `{{c1::contenuto}}` di Anki
```

```
Crea un set di flashcard formattate per l'importazione su Anki sull'argomento ''. Le flashcard devono essere in formato CSV, con domande e risposte separate da pipe (|). Concentrati su domande che aiutino a ricordare l'argomento per cultura personale, includendo il "perché" (es. motivi di eventi o scelte) e le "novità" (es. innovazioni o cambiamenti introdotti). Genera un numero sufficiente di flashcard per coprire adeguatamente l'argomento, con risposte concise e chiare, adatte a uno studio efficace.
```

---
## Collegamenti
