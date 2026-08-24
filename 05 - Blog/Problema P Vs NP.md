---
stage: fine-tuned 🧠
draft: false
type: article
area: tech
related: []
source: original
title: "Problema P Vs NP"
date: '2026-03-09'
updated: 2026-07-12T21:35
tags: [tech/computer-science, tech/algoritmi, tech/complessità, education/matematica]
summary: "Il problema P vs NP è probabilmente il più grande quesito irrisolto dell'Informatica Teorica (e uno dei problemi del millennio da 1 milione di dollari del Clay Mathematics Institute)."
---
[[Home MOC|Home]] / [[Blog]] / [[Problema P Vs NP]]

Il problema **P vs NP** è probabilmente il più grande quesito irrisolto dell'[[Informatica Teorica]] (e uno dei problemi del millennio da 1 milione di dollari del Clay Mathematics Institute).

La domanda fondamentale è filosofica quanto matematica: **se è facile** _**verificare**_ **la soluzione di un problema, è altrettanto facile** _**trovarla**_ **partendo da zero?**
## Classi di Complessità: P e NP

Per comprendere il problema, bisogna dividere gli algoritmi in base a come scala il tempo di esecuzione al crescere dei dati di input (vedi [[Notazione Big-O]]).
### 1. Problemi di classe P (Polynomial Time)

Sono i problemi che un computer può **risolvere in modo efficiente** e ragionevole. Al crescere dell'input, il tempo necessario cresce in modo polinomiale (es. linearmente o quadraticamente).

- **Passaggio pratico**: Ordinare alfabeticamente una lista di nomi. Se la lista diventa 10 volte più grande, il computer fa circa 10-20 volte più lavoro. È un ritmo prevedibile e gestibile.
### 2. Problemi di classe NP (Nondeterministic Polynomial Time)

Sono problemi in cui **trovare** la soluzione può richiedere tempi incalcolabili (crescita esponenziale o fattoriale), ma **verificare** una soluzione già pronta è facilissimo (richiede tempo polinomiale).

> ⚠️ **Errore Comune**
> 
> Molti pensano che "NP" stia per "Non-Polinomiale". In realtà significa "Tempo Polinomiale Non Deterministico". Si riferisce al fatto che una "macchina non deterministica" (teorica, capace di tirare a indovinare sempre l'opzione giusta) potrebbe risolverli in tempo polinomiale.
## Esempi Intuitivi
### Il Sudoku

- **Trovare la soluzione**: Partire da una griglia quasi vuota richiede di testare un'infinità di combinazioni. Più grande è la griglia, più le combinazioni esplodono.
- **Verificare la soluzione**: Se ti do una griglia di Sudoku già compilata, ci metti pochi secondi a controllare che non ci siano numeri ripetuti in righe, colonne e quadrati.
- _Conclusione: È un problema NP._    
### Il Percorso più Corto (Commesso Viaggiatore / Shortest Path)

Hai un numero $N$ di città e devi trovare il percorso più breve che le visiti tutte una sola volta.

- **Trovare la soluzione (Brute Force)**: Devi calcolare ogni singola rotta possibile. Con sole 15 città, hai circa 87 miliardi di combinazioni. Il processore esplode.
- **Verificare la soluzione**: Se ti fornisco un percorso specifico e ti chiedo "questo percorso è lungo meno di 500 km?", basta sommare le distanze tra le tappe. Operazione banale.
### La Crittografia e i Numeri Primi

Alla base della [[Crittografia RSA]] c'è un concetto identico:

- **P (Facile)**: Moltiplicare due numeri primi (es. $7 \times 13 = 91$).
    
- **NP (Difficile)**: Scomporre in fattori primi un numero enorme. Se ti do `69420` (o un numero di 256 bit) e ti chiedo quali numeri primi lo compongono, devi andare per tentativi.
## I Problemi NP-Completi e l'implicazione di P = NP

Esiste un sottogruppo chiamato **NP-Completi**. Sono i "boss finali" della categoria NP (ne fa parte il Sudoku, il Commesso Viaggiatore, il protein folding, ecc.).

La loro particolarità? **Sono tutti matematicamente collegati.** Se trovi un algoritmo veloce (di classe P) per risolverne anche solo uno, li hai risolti automaticamente tutti.

**Cosa succederebbe se qualcuno dimostrasse che P = NP?**

Il mondo cambierebbe dall'oggi al domani:

- Tutta la **crittografia** mondiale (password, wallet crypto, comunicazioni bancarie) verrebbe violata istantaneamente.
- Scoprire **cure per il cancro** (simulando il ripiegamento delle proteine) diventerebbe semplice quanto riordinare un foglio Excel.
- L'ottimizzazione logistica sarebbe perfetta, eliminando immensi sprechi di risorse.

Finora, nessuno è riuscito a dimostrarlo (e quasi tutti gli esperti credono che $P \neq NP$, ovvero che esistono limiti computazionali intrinseci nel nostro universo).
---
## Collegamenti

- [[Teoria della Complessità Computazionale]]
- [[Notazione Big O]]
- [[Algoritmi di Ottimizzazione]]
- [[Crittografia RSA]]
