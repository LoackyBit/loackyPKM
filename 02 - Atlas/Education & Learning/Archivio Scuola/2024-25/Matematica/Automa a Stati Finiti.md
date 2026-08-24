---
status: draft
type: concept
area: education
related: []
source: original
title: "Automa a Stati Finiti"
date: '2025-03-15'
updated: 2026-07-07T01:20
tags: [education/school, education/2024-25, education/matematica]
summary: "Un automa a stati finiti è un modello teorico usato in informatica per descrivere sistemi che possono trovarsi in un numero limitato di situazioni (chiamate \"stati\") e che cambiano da una situazion..."
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Automa a Stati Finiti]]

Un automa a stati finiti è un modello teorico usato in informatica per descrivere sistemi che possono trovarsi in un numero limitato di situazioni (chiamate "stati") e che cambiano da una situazione all'altra in base a delle regole precise. È come una macchina immaginaria che segue istruzioni per capire o elaborare qualcosa, ad esempio parole o sequenze.

Immagina un distributore automatico di bibite:
- Ha stati come "in attesa di soldi", "soldi inseriti", "bibita selezionata".
- Passa da uno stato all'altro quando inserisci una moneta o premi un pulsante.
- Alla fine, ti dà la bibita (o magari si blocca se qualcosa va storto).

Ecco, questo è un esempio pratico di un automa a stati finiti!

---

### Componenti principali
Un automa a stati finiti è fatto da 5 elementi fondamentali:

1. **Stati (Q)**: Un insieme finito di "situazioni" in cui la macchina può trovarsi. Ad esempio, "acceso", "spento", "in elaborazione". Uno di questi è lo **stato iniziale** (dove tutto comincia).
2. **Alfabeto (Σ)**: Un insieme di simboli che la macchina può leggere o ricevere come input. Ad esempio, "0" e "1" per un sistema binario, o "moneta" e "pulsante" per il distributore.
3. **Funzione di transizione (δ)**: Una regola che dice "se sei in questo stato e ricevi questo input, vai in quest'altro stato". È come una tabella di istruzioni.
4. **Stato iniziale (q₀)**: Il punto di partenza della macchina.
5. **Stati finali o di accettazione (F)**: Gli stati in cui la macchina "finisce" e dice "ho completato il compito" o "questa sequenza è valida".

---

### Come funziona?
La macchina:
1. Parte dallo **stato iniziale**.
2. Legge un simbolo dell'input (uno alla volta).
3. Usa la **funzione di transizione** per decidere in quale stato andare dopo aver letto il simbolo.
4. Continua così finché non finisce l'input.
5. Se alla fine si trova in uno degli **stati finali**, accetta l'input (cioè dice "sì, va bene"). Altrimenti, lo rifiuta.

---

### Un esempio semplice
Immaginiamo un automa che controlla se una sequenza di "0" e "1" finisce con "1". L'alfabeto è {0, 1}.

- **Stati**: Due stati possibili:
  - S0: "non ho ancora finito con 1" (stato iniziale).
  - S1: "l'ultimo simbolo è 1" (stato finale).
- **Transizioni**:
  - Se sono in S0 e leggo "0", resto in S0.
  - Se sono in S0 e leggo "1", vado in S1.
  - Se sono in S1 e leggo "0", torno in S0.
  - Se sono in S1 e leggo "1", resto in S1.
- **Stato iniziale**: S0.
- **Stato finale**: S1.

Proviamo con la sequenza "0101":
1. Parto da S0, leggo "0" → resto in S0.
2. S0, leggo "1" → vado in S1.
3. S1, leggo "0" → torno in S0.
4. S0, leggo "1" → vado in S1.
5. Finisco in S1 (stato finale) → la sequenza è accettata!

Ora con "0100":
1. S0 → "0" → S0.
2. S0 → "1" → S1.
3. S1 → "0" → S0.
4. S0 → "0" → S0.
5. Finisco in S0 (non finale) → sequenza rifiutata.

---

### Tipi di automi a stati finiti
Ci sono due versioni principali:
1. **Deterministici (DFA)**: Per ogni stato e ogni simbolo, c'è sempre un solo stato successivo possibile (come nell'esempio sopra).
2. **Non deterministici (NFA)**: Possono esserci più stati successivi possibili per lo stesso simbolo, o anche transizioni senza leggere simboli (chiamate "epsilon-transizioni"). Sono più flessibili ma più complessi.

Alla fine, però, DFA e NFA possono fare le stesse cose, anche se i DFA sono più "rigidi" e facili da implementare.

---

### A cosa servono?
Gli automi a stati finiti sono usati tantissimo:
- **Riconoscimento di pattern**: Per trovare parole o sequenze valide (es. controllare se un indirizzo email è scritto correttamente).
- **Compilatori**: Per analizzare il codice di un programma.
- **Sistemi reali**: Come il distributore automatico o i semafori.

---
## Collegamenti
