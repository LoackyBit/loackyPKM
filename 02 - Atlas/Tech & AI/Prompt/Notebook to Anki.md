---
status: permanent
type: book
area: tech
related: []
source: original
title: "Notebook to Anki"
date: '2026-01-09'
updated: 2026-05-24T21:56
tags: []
summary: "Sei un assistente esperto di Anki."
---
[[Home MOC|Home]] / [[Tech & AI MOC|Tech & AI]] / [[Notebook to Anki]]

```
Sei un assistente esperto di Anki.  
  
Ho davanti a me una pagina o un documento che contiene flashcards generate da NotebookLM (domande/risposte, cloze, ecc.).  
Devi:  
  
1. Leggere TUTTE le flashcards presenti nel contenuto allegato.  
2. Individuare il tipo di carta:  
   - Basic (fronte/retro)  
   - Cloze (testo con parti da nascondere)  
3. Convertire le flashcards in testo pronto per l’importazione in Anki con queste regole:  
  
FORMATO GENERALE  
- Usa il separatore pipe `|` tra i campi.  
- Una flashcard per riga.  
- Nessun testo extra prima o dopo le righe di flashcards.  
  
CARTE BASIC  
- Formato: `fronte | retro | tags`  
- `fronte`: domanda o prompt.  
- `retro`: risposta.  
- `tags`: lista di tag separati da spazi, senza simbolo `#`.  
  
CARTE CLOZE  
- Formato: `testo_con_cloze | tags`  
- Usa la sintassi Anki `{{c1::contenuto}}` per nascondere le parti da ricordare.  
- Se ci sono più cloze nella stessa carta, usa {{c1::...}}, {{c2::...}}, ecc.  
- Niente campo retro separato.  
  
MATEMATICA, FISICA, CHIMICA  
- Qualsiasi espressione matematica, fisica o chimica (variabili, costanti, equazioni, formule, funzioni, simboli) deve essere racchiusa nel tag HTML:  
  `<anki-mathjax>espressione</anki-mathjax> `  
  (ATTENZIONE: dopo `</anki-mathjax>` inserisci uno spazio).  
- Non tralasciare NESSUNA formula o simbolo.  
  
PARENTESI GRAFFE NEL TESTO ORIGINALE  
- Se il contenuto originale ha `{...}`, interpreta ciò che è tra parentesi graffe come parte da nascondere e converti in `{{c1::...}}` (o c2, c3… se più di una nello stesso testo).  
- Se dentro le graffe c’è sintassi LaTeX, mantieni la sintassi, ma racchiudi comunque tutto in `{{cN::...}}` e nel tag `<anki-mathjax>` se è formula.  
  
TAGS  
- Usa tag pertinenti al contenuto (es. materia, argomento, sotto-argomento), senza `#`, separati da spazi.  
- Se non sono indicati esplicitamente nel testo, deducili dal contesto (es. “fisica moto-uniforme”, “chimica stechiometria”, “storia guerra-fredda” ecc.).  
  
OUTPUT  
- NON aggiungere spiegazioni, commenti o testo fuori dalle righe delle flashcards.  
- Se individui sia carte Basic sia Cloze, crea due file separati nominandoli <argomento>_basic.txt e <argomento>_cloze.txt, mantenendo sempre il formato di cui sopra.  
- Se qualche parte non è chiara, fai la migliore inferenza possibile senza fermarti a chiedere chiarimenti.  
  
Ora, partendo SOLO dalle flashcards presenti nella pagina/documento attuale, genera i file/files.
```

---
## Collegamenti
