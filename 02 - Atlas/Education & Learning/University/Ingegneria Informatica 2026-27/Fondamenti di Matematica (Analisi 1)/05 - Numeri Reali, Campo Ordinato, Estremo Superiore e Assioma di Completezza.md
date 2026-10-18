---
status: permanent
type: lecture
area: education
related: ["[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[04 - Funzioni (Parte II)]]", "[[03 - Funzioni (Parte I)]]", "[[02 - Teoria degli Insiemi]]", "[[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]", "[[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]", "[[02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti]]"]
aliases: ["Lezione 5 Fondamenti di Matematica", "FdM Lezione 5", "Numeri Reali e Assiomi di Campo", "Campo Totalmente Ordinato", "Estremo Superiore e Assioma di Completezza", "05 - I Numeri Reali"]
source: Lezione 5 FdM del 30/09/2026 - Prof. Saverio Salzo, Dott. Giovanni Franzina
title: "05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza"
date: '2026-09-30'
updated: 2026-10-06T07:59
tags: [education/university, education/math, tech/logic]
summary: "Assiomi di campo e ordinamento totale di R, conseguenze algebriche e dimostrazioni, insiemi limitati, maggioranti e minoranti, estremo superiore e inferiore, caratterizzazione epsilon e assioma di completezza."
course: "Fondamenti di Matematica (Analisi 1)"
sources: ["[[Lezione 5 FdM.pdf]]", "[[Epsilon 1.pdf]]", "[[Real Analysis.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Matematica & Fisica MOC]] / [[05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza]]

# 05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza

- **Docenti:** Prof. Saverio Salzo / Canale A-L, Dott. Giovanni Franzina
- **Data Lezione:** 2026-09-30
- **Materiali Didattici Ufficiali:** \[[[Lezione 5 FdM.pdf#page=1|Dispensa Lezione 05 — I numeri reali (Franzina & Salzo)]]]
- **Testi di Riferimento Didattico:** \[[[Epsilon 1.pdf|Acerbi, Buttazzo — Epsilon 1 (Cap. 1)]]], \[[[Real Analysis.pdf|Carothers — Real Analysis (Cap. 1)]]]
- **Riferimento MOC:** [[Fondamenti di Matematica (Analisi 1) MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Lezione Precedente:** [[04 - Funzioni (Parte II)]]
- **Collegamento Interdisciplinare:** [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]] e [[02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti]] (in cui la continuità di $\mathbb{R}$, la misura degli intervalli e l'assioma di completezza costituiscono il fondamento rigoroso per definire le variabili aleatorie continue, le funzioni di ripartizione e le $\sigma$-algebre di Borel)

La quinta lezione di Fondamenti di Matematica segna il passaggio fondativo dai linguaggi preparatori — la [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione|logica proposizionale]], la [[02 - Teoria degli Insiemi|teoria assiomatica degli insiemi ZF]] e la teoria delle [[03 - Funzioni (Parte I)|relazioni e corrispondenze funzionali]] completata in [[04 - Funzioni (Parte II)]] — alla costruzione del teatro operativo dell'Analisi Matematica: l'insieme dei <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>numeri reali</b></font></mark> $\mathbb{R}$.

Invece di costruire $\mathbb{R}$ a partire dai razionali $\mathbb{Q}$ mediante procedimenti insiemistici complessi (quali le sezioni di Dedekind o le classi di equivalenza di successioni di Cauchy), l'approccio moderno dell'Analisi Matematica consiste nell'introdurre $\mathbb{R}$ per **via assiomatica** \[[[Lezione 5 FdM.pdf#page=1|Dispensa p. 1]]]. L'insieme dei numeri reali viene postulato come una struttura caratterizzata in modo univoco da tre pilastri concettuali:
1. Una struttura algebrica di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>campo</b></font></mark> commutativo $(\mathbb{R}, +, \cdot)$;
2. Una struttura d'ordine di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>campo totalmente ordinato</b></font></mark> $(\mathbb{R}, \le)$ compatibile con le operazioni binarie;
3. Una proprietà topologico-geometrica di continuità espressa dall'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma di completezza</b></font></mark> (esistenza dell'estremo superiore e dell'elemento separatore), che colma tutti i "buchi" della retta razionale.

---

## 1. Struttura Algebrica: Assiomi di Campo di $(\mathbb{R}, +, \cdot)$

Sull'insieme $\mathbb{R}$ sono assegnate due <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>operazioni binarie interne</b></font></mark> (funzioni da $\mathbb{R} \times \mathbb{R}$ in $\mathbb{R}$):
- **Addizione:** $+ : \mathbb{R} \times \mathbb{R} \to \mathbb{R}$, con $(x, y) \mapsto x + y$
- **Moltiplicazione:** $\cdot : \mathbb{R} \times \mathbb{R} \to \mathbb{R}$, con $(x, y) \mapsto x \cdot y$

Tali operazioni soddisfano il seguente sistema di assiomi algebrici fondamentali \[[[Lezione 5 FdM.pdf#page=1|Dispensa p. 1]]].

> [!danger] Assioma 1.1: Assiomi di Campo per $(\mathbb{R}, +, \cdot)$
> L'insieme $\mathbb{R}$ dotato delle operazioni $+$ e $\cdot$ soddisfa le proprietà:
> - **Assiomi dell'Addizione $(\mathbb{R}, +)$:**
>   - **(A1) Proprietà Associativa:** $(\forall x, y, z \in \mathbb{R}) \; (x + y) + z = x + (y + z)$
>   - **(A2) Esistenza dell'Elemento Neutro (Zero):** $(\exists\, 0 \in \mathbb{R}) (\forall x \in \mathbb{R}) \; x + 0 = 0 + x = x$
>   - **(A3) Esistenza dell'Opposto (Inverso Additivo):** $(\forall x \in \mathbb{R}) (\exists\, -x \in \mathbb{R}) \; x + (-x) = (-x) + x = 0$
>   - **(A4) Proprietà Commutativa:** $(\forall x, y \in \mathbb{R}) \; x + y = y + x$
> - **Assiomi della Moltiplicazione $(\mathbb{R}^*, \cdot)$ (ove $\mathbb{R}^* = \mathbb{R} \setminus \{0\}$):**
>   - **(M1) Proprietà Associativa:** $(\forall x, y, z \in \mathbb{R}) \; (x \cdot y) \cdot z = x \cdot (y \cdot z)$
>   - **(M2) Esistenza dell'Elemento Neutro (Unità):** $(\exists\, 1 \in \mathbb{R} \setminus \{0\}) (\forall x \in \mathbb{R}) \; x \cdot 1 = 1 \cdot x = x$
>   - **(M3) Esistenza del Reciproco (Inverso Moltiplicativo):** $(\forall x \in \mathbb{R} \setminus \{0\}) (\exists\, x^{-1} \in \mathbb{R}) \; x \cdot x^{-1} = x^{-1} \cdot x = 1$
>   - **(M4) Proprietà Commutativa:** $(\forall x, y \in \mathbb{R}) \; x \cdot y = y \cdot x$
> - **Proprietà Distributiva (D):**
>   - $(\forall x, y, z \in \mathbb{R}) \; x \cdot (y + z) = x \cdot y + x \cdot z$

Gli assiomi (A1)–(A4) affermano che la struttura algebrica $(\mathbb{R}, +)$ costituisce un <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>gruppo abeliano</b></font></mark> (commutativo). Analogamente, gli assiomi (M1)–(M4) affermano che $(\mathbb{R} \setminus \{0\}, \cdot)$ è anch'esso un gruppo abeliano. L'assioma di distributività (D) raccorda le due operazioni, rendendo $(\mathbb{R}, +, \cdot)$ un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>campo</b></font></mark> (o corpo commutativo) \[[[Lezione 5 FdM.pdf#page=2|Dispensa p. 2]]].

> [!tip]- Flashcard: Definizione Assiomatica di Campo
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Quali sono le tre famiglie di assiomi che definiscono una struttura algebrica $(\mathbb{R}, +, \cdot)$ come campo?
Back: Una struttura $(\mathbb{R}, +, \cdot)$ è un campo se soddisfa:
1. Assiomi dell'addizione (A1-A4): $(\mathbb{R}, +)$ è un gruppo abeliano (associatività, neutro $0$, opposti $-x$, commutatività).
2. Assiomi della moltiplicazione (M1-M4): $(\mathbb{R} \setminus \{0\}, \cdot)$ è un gruppo abeliano (associatività, neutro $1 \neq 0$, reciproci $x^{-1}$, commutatività).
3. Proprietà distributiva (D): il prodotto è distributivo rispetto alla somma:
$$(\forall x, y, z \in \mathbb{R}) \; x \cdot (y + z) = x \cdot y + x \cdot z$$
Tags: education/university education/math tech/logic
END
%%
---

## 2. Conseguenze Immediate e Proprietà Algebriche Fondamentali

Dagli assiomi di campo scaturiscono proposizioni algebriche essenziali, comunemente considerate "regole ovvie del calcolo", ma che richiedono una rigorosa deduzione logica \[[[Lezione 5 FdM.pdf#page=2|Dispensa p. 2]]].

### Unicità degli Elementi Neutri e Inversi

> [!info] Osservazione 1.1: Unicità di Neutri, Opposti e Reciproci
> 1. **Unicità dell'Elemento Neutro Additivo e Moltiplicativo:**
>    - Lo zero è unico. Se $0^\prime \in \mathbb{R}$ soddisfa $(\forall x) \; x + 0^\prime = x$, allora per la neutralità di $0$ si ha $0^\prime = 0^\prime + 0$, e per la neutralità di $0^\prime$ si ha $0^\prime + 0 = 0$. Ne segue $0^\prime = 0$.
>    - In modo perfettamente speculare si dimostra che l'unità moltiplicativa $1$ è unica.
> 2. **Unicità dell'Opposto e del Reciproco:**
>    - Sia $x \in \mathbb{R}$. Se esistessero due opposti $x_1, x_2$ tali che $x + x_1 = 0$ e $x + x_2 = 0$, applicando gli assiomi si avrebbe:
>      $$x_1 \overset{\text{(A2)}}{=} x_1 + 0 \overset{\text{(A3)}}{=} x_1 + (x + x_2) \overset{\text{(A1)}}{=} (x_1 + x) + x_2 \overset{\text{(A4)}}{=} (x + x_1) + x_2 \overset{\text{(A3)}}{=} 0 + x_2 \overset{\text{(A2)}}{=} x_2$$
>      Dunque $x_1 = x_2$. L'opposto è unico e si denota con $-x$.
>    - Con analoga catena associativa nel gruppo moltiplicativo, si dimostra che per ogni $x \neq 0$ il reciproco è unico e si denota con $x^{-1}$.

> [!tip]- Flashcard: Unicità dell'Elemento Neutro
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Come si dimostra rigorosamente che l'elemento neutro additivo $0$ in un campo è unico?
Back: Siano $0$ e $0^\prime$ due elementi neutri per l'addizione.
Poiché $0$ è neutro per l'addizione:
$$0^\prime = 0^\prime + 0$$
Poiché anche $0^\prime$ è neutro per l'addizione:
$$0^\prime + 0 = 0$$
Confrontando le due identità si ottiene immediatamente $0^\prime = 0$. Con identico ragionamento si dimostra l'unicità dell'unità moltiplicativa $1$.
Tags: education/university education/math tech/logic
END
%%
### Non Esistenza dell'Inverso Moltiplicativo dello Zero

Una conseguenza strutturale dell'assioma (M2) ($1 \neq 0$) è l'impossibilità di definire l'inverso moltiplicativo di zero:

> [!info] Osservazione 1.3: Impossibilità dell'Inverso dello Zero
> Se per assurdo esistesse $0^{-1} \in \mathbb{R}$, per la definizione di reciproco (M3) dovrebbe valere $0 \cdot 0^{-1} = 1$. Tuttavia, poiché per qualsiasi elemento vale $x \cdot 0 = 0$, risulterebbe:
> $$1 = 0 \cdot 0^{-1} = 0 \implies 1 = 0$$
> Ciò contraddice esplicitamente l'assioma (M2) che impone $1 \neq 0$. Pertanto <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>zero non ammette inverso moltiplicativo</b></font></mark> e la divisione per zero è priva di senso algebrico.

> [!tip]- Flashcard: Non Esistenza dell'Inverso di Zero
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Perché in un campo non può esistere l'inverso moltiplicativo dello zero ($0^{-1}$)?
Back: Se per assurdo esistesse $0^{-1} \in \mathbb{R}$, allora per l'assioma dell'inverso si avrebbe $0 \cdot 0^{-1} = 1$.
D'altra parte, per la legge di annullamento si ha $0 \cdot x = 0$ per ogni $x$, da cui:
$$1 = 0 \cdot 0^{-1} = 0 \implies 1 = 0$$
Ciò contraddice l'assioma di campo (M2) che postula tassativamente $1 \neq 0$.
Tags: education/university education/math tech/logic
END
%%
### Operazioni Derivate: Sottrazione e Divisione

> [!danger] Definizione 1.4: Differenza e Quoziente tra Reali
> - L'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>operazione di differenza</b></font></mark> è definita sommando l'opposto:
>   $$(\forall x, y \in \mathbb{R}) \; x - y \overset{\text{def}}{=} x + (-y)$$
> - L'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>operazione di divisione</b></font></mark> è definita per $y \neq 0$ moltiplicando per il reciproco:
>   $$(\forall x \in \mathbb{R})(\forall y \in \mathbb{R} \setminus \{0\}) \; \frac{x}{y} \overset{\text{def}}{=} x \cdot y^{-1}$$
>   In particolare, per $x = 1$ si ha $\frac{1}{y} = 1 \cdot y^{-1} = y^{-1}$.

### Teorema delle Proprietà Algebriche e Dimostrazioni

> [!summary] Proposizione 1.2: Conseguenze Algebriche Fondamentali
> In $(\mathbb{R}, +, \cdot)$ valgono le seguenti proprietà \[[[Lezione 5 FdM.pdf#page=2|Dispensa p. 2]]]:
> 1. **Involuzione:** $(\forall x \in \mathbb{R}) \; -(-x) = x$, e per $x \neq 0$, $(x^{-1})^{-1} = x$.
> 2. **Legge di Cancellazione per la Somma:**
>    $$(\forall x, y, z \in \mathbb{R}) \; [x + z = y + z \implies x = y]$$
> 3. **Legge di Cancellazione per il Prodotto:**
>    $$(\forall x, y \in \mathbb{R})(\forall z \in \mathbb{R} \setminus \{0\}) \; [x \cdot z = y \cdot z \implies x = y]$$
> 4. **Legge di Annullamento del Prodotto:**
>    $$(\forall x, y \in \mathbb{R}) \; [x \cdot y = 0 \iff x = 0 \lor y = 0]$$
> 5. **Regola dei Segni per il Prodotto:**
>    $$(\forall x, y \in \mathbb{R}) \; [(-x)y = -(xy)] \;\land\; [(-x)(-y) = xy]$$
> 6. **Opposto del Reciproco:** $(\forall x \in \mathbb{R} \setminus \{0\}) \; -(x^{-1}) = (-x)^{-1}$.
> 7. **Reciproco del Prodotto:** $(\forall x, y \in \mathbb{R} \setminus \{0\}) \; (xy)^{-1} = x^{-1} y^{-1}$.

#### Dimostrazioni Formali

- **Dimostrazione 1 (Cancellazione Additiva):**
  Siano $x, y, z \in \mathbb{R}$ tali che $x + z = y + z$. Aggiungendo ad ambo i membri l'opposto di $z$:
  $$x = x + 0 = x + (z + (-z)) = (x + z) + (-z) = (y + z) + (-z) = y + (z + (-z)) = y + 0 = y$$
  Dunque $x = y$. $\blacksquare$

- **Dimostrazione 2 (Cancellazione Moltiplicativa):**
  Siano $x, y \in \mathbb{R}$ e sia $z \neq 0$. Se $xz = yz$, moltiplicando per il reciproco $z^{-1}$:
  $$x = x \cdot 1 = x(z \cdot z^{-1}) = (xz)z^{-1} = (yz)z^{-1} = y(z \cdot z^{-1}) = y \cdot 1 = y$$
  Dunque $x = y$. $\blacksquare$

- **Dimostrazione 3 (Legge di Annullamento del Prodotto):**
  - **Parte "$\Leftarrow$":** Supponiamo che uno dei due fattori sia $0$, per esempio $y = 0$. Allora:
    $$0 + x \cdot 0 = x \cdot 0 = x \cdot (0 + 0) = x \cdot 0 + x \cdot 0$$
    Aggiungendo l'opposto $-(x \cdot 0)$ ad entrambi i membri (o applicando la cancellazione additiva), si ottiene $x \cdot 0 = 0$.
  - **Parte "$\Rightarrow$":** Supponiamo che $x \cdot y = 0$. Se $x = 0$, la disgiunzione è verificata. Se $x \neq 0$, allora esiste l'inverso $x^{-1} \in \mathbb{R}$. Moltiplicando ambo i membri per $x^{-1}$:
    $$x^{-1} \cdot (xy) = x^{-1} \cdot 0 \implies (x^{-1} x) \cdot y = 0 \implies 1 \cdot y = 0 \implies y = 0$$
    Dunque o $x = 0$ oppure $y = 0$. $\blacksquare$

- **Dimostrazione 4 (Regola dei Segni):**
  Notiamo che $(-x)y + xy = (-x + x)y = 0 \cdot y = 0$. Poiché la somma di $(-x)y$ con $xy$ è zero, per l'unicità dell'opposto si deduce $(-x)y = -(xy)$.
  Applicando tale identità alla coppia $(x, -y)$:
  $$(-x)(-y) = -(x(-y)) = -((-y)x) = -(-(yx)) = yx = xy$$
  dove nell'ultimo passaggio si sfrutta l'involuzione dell'opposto $-(-a) = a$. $\blacksquare$

> [!tip]- Flashcard: Legge di Cancellazione e Annullamento del Prodotto
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: In un campo $(\mathbb{R}, +, \cdot)$:
1. La legge di cancellazione della somma afferma che {{c1::$x + z = y + z \implies x = y$}}.
2. La legge di annullamento del prodotto stabilisce che {{c2::$xy = 0 \iff x = 0 \lor y = 0$}}.
Extra: La cancellazione moltiplicativa $xz = yz \implies x = y$ esige rigorosamente l'ipotesi $z \neq 0$.
Tags: education/university education/math tech/logic
END
%%
> [!tip]- Flashcard: Dimostrazione di $x \cdot 0 = 0$
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Come si dimostra a partire dagli assiomi di campo che per ogni $x \in \mathbb{R}$ si ha $x \cdot 0 = 0$?
Back: Si sfrutta la neutralità dello zero e la proprietà distributiva:
$$x \cdot 0 = x \cdot (0 + 0) = x \cdot 0 + x \cdot 0$$
Aggiungendo a entrambi i membri l'opposto $-(x \cdot 0)$ e applicando l'associatività e l'elemento neutro:
$$x \cdot 0 + (-(x \cdot 0)) = (x \cdot 0 + x \cdot 0) + (-(x \cdot 0)) \implies 0 = x \cdot 0 + (x \cdot 0 + (-(x \cdot 0))) \implies 0 = x \cdot 0 + 0 = x \cdot 0$$
Ne segue $x \cdot 0 = 0$.
Tags: education/university education/math tech/logic
END
%%
---

## 3. Struttura d'Ordine: Campo Totalmente Ordinato $(\mathbb{R}, \le)$

Oltre alla struttura algebrica, $\mathbb{R}$ è dotato di una relazione d'ordine che ne permette il confronto quantitativo e la rappresentazione su una retta geometrica \[[[Lezione 5 FdM.pdf#page=3|Dispensa p. 3]]].

### Assiomi d'Ordine e Compatibilità

> [!danger] Assioma 2.1: Assiomi di Ordinamento Totale e Compatibilità
> Su $\mathbb{R}$ è definita una relazione binaria $\le$ (sottoinsieme di $\mathbb{R} \times \mathbb{R}$) che soddisfa:
> - **Assiomi d'Ordine:**
>   - **(O1) Proprietà Riflessiva:** $(\forall x \in \mathbb{R}) \; x \le x$
>   - **(O2) Proprietà Antisimmetrica:** $(\forall x, y \in \mathbb{R}) \; [x \le y \land y \le x \implies x = y]$
>   - **(O3) Proprietà Transitiva:** $(\forall x, y, z \in \mathbb{R}) \; [x \le y \land y \le z \implies x \le z]$
>   - **(O4) Ordine Totale (Tricotomia):** $(\forall x, y \in \mathbb{R}) \; [x \le y \lor y \le x]$
> - **Compatibilità con le Operazioni Binarie:**
>   - **(AO) Compatibilità con la Somma:** $(\forall x, y, z \in \mathbb{R}) \; [x \le y \implies x + z \le y + z]$
>   - **(MO) Compatibilità con il Prodotto (per non negativi):** $(\forall x, y, z \in \mathbb{R}) \; [x \le y \land z \ge 0 \implies x \cdot z \le y \cdot z]$

Gli assiomi (O1)–(O4) attestano che $(\mathbb{R}, \le)$ è un insieme <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>totalmente ordinato</b></font></mark> (ogni coppia di numeri reali è sempre confrontabile). Congiuntamente agli assiomi algebrici (A1)–(D) e alle condizioni di compatibilità (AO) e (MO), essi definiscono $\mathbb{R}$ come un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>campo totalmente ordinato</b></font></mark>.

> [!tip]- Flashcard: Assiomi di Ordinamento Totale
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: Una relazione d'ordine $\le$ su $\mathbb{R}$ è totale se soddisfa le proprietà {{c1::riflessiva}} ($x \le x$), {{c1::antisimmetrica}} ($x \le y \land y \le x \implies x = y$), {{c1::transitiva}} ($x \le y \land y \le z \implies x \le z$) e {{c2::di tricotomia / ordine totale}} ($(\forall x, y) \; x \le y \lor y \le x$).
Tags: education/university education/math tech/logic
END
%%
> [!tip]- Flashcard: Compatibilità dell'Ordinamento con le Operazioni
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Quali sono i due assiomi di compatibilità tra la relazione d'ordine $\le$ e le operazioni di campo $+$ e $\cdot$ in $\mathbb{R}$?
Back: 
1. **Compatibilità con la Somma (AO):**
$$(\forall x, y, z \in \mathbb{R}) \; [x \le y \implies x + z \le y + z]$$
2. **Compatibilità con il Prodotto (MO):**
$$(\forall x, y, z \in \mathbb{R}) \; [x \le y \land z \ge 0 \implies x \cdot z \le y \cdot z]$$
Tags: education/university education/math tech/logic
END
%%
### Ordine Stretto e Segno dei Numeri Reali

> [!danger] Definizione 2.2: Ordine Stretto e Insiemi di Positività
> - La <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>relazione d'ordine stretto</b></font></mark> ($<$) è definita da:
>   $$x < y \overset{\text{def}}{\iff} (x \le y) \land (x \neq y)$$
> - Definiamo gli insiemi numerici di riferimento:
>   - **Reali non negativi (positivi):** $\mathbb{R}_+ = \{x \in \mathbb{R} \mid x \ge 0\}$
>   - **Reali strettamente positivi:** $\mathbb{R}_+^* = \{x \in \mathbb{R} \mid x > 0\}$
>   - **Reali non positivi (negativi):** $\mathbb{R}_- = \{x \in \mathbb{R} \mid x \le 0\}$

### Teorema delle Proprietà dell'Ordinamento

> [!summary] Proposizione 2.2: Proprietà dell'Ordinamento Reale
> In $(\mathbb{R}, +, \cdot, \le)$ valgono le seguenti proprietà \[[[Lezione 5 FdM.pdf#page=4|Dispensa p. 4]]]:
> 1. **Inversione del Segno:** $(\forall x \in \mathbb{R}) \; [0 \le x \iff -x \le 0]$ e $[x \le 0 \iff 0 \le -x]$.
> 2. **Positività dei Quadrati:** $(\forall x \in \mathbb{R}) \; x^2 \ge 0$.
> 3. **Positività dell'Unità:** $1 > 0$.
> 4. **Monotonia Stretta del Prodotto:** $(\forall x, y, z \in \mathbb{R}) \; [z > 0 \land x < y \implies xz < yz]$.
> 5. **Monotonia dei Quadrati sui Positivi:** $(\forall x, y \in \mathbb{R}) \; [0 \le x < y \implies x^2 < y^2]$.
> 6. **Segno del Prodotto:**
>    - $x \ge 0 \land y \ge 0 \implies xy \ge 0$
>    - $x \ge 0 \land y \le 0 \implies xy \le 0$
> 7. **Conservazione della Positività del Reciproco:** $(\forall x \in \mathbb{R}^*) \; [x > 0 \implies x^{-1} > 0]$.
> 8. **Confronto con l'Unità:** Per ogni $x > 0$:
>    $$x < 1 \implies x^2 < x \qquad\text{e}\qquad x > 1 \implies x^2 > x$$
> 9. **Densità dell'Ordinamento:** $(\forall x, y \in \mathbb{R}) \; [x < y \implies (\exists\, z \in \mathbb{R}) \; x < z < y]$.

#### Dimostrazioni Salienti

- **Dimostrazione 1 (Inversione del Segno):**
  Dall'assioma (AO), sommando $-x$ ad ambo i membri di $0 \le x$, si ottiene $0 + (-x) \le x + (-x)$, ossia $-x \le 0$. Viceversa, se $-x \le 0$, sommando $x$ si ottiene $-x + x \le 0 + x$, ossia $0 \le x$.
- **Dimostrazione 2 (Positività dei Quadrati $x^2 \ge 0$):**
  Sia $x \in \mathbb{R}$. Per l'assioma di ordine totale (O4), si ha $x \ge 0$ oppure $x \le 0$.
  - Se $x \ge 0$, per (MO) ponendo $y = x$ e $z = x \ge 0$ si ha $0 \cdot x \le x \cdot x$, ossia $0 \le x^2$.
  - Se $x \le 0$, per la proprietà precedente si ha $-x \ge 0$. Per quanto appena provato $0 \le (-x)^2$. Ma per la regola dei segni $(-x)^2 = (-x)(-x) = x^2$, da cui segue $x^2 \ge 0$. $\blacksquare$
- **Dimostrazione 3 (Positività di $1 > 0$):**
  Per l'assioma (M2) $1 = 1^2$, dunque per la proprietà dei quadrati $1 \ge 0$. Poiché per assioma $1 \neq 0$, deve valere strettamente $1 > 0$. $\blacksquare$
- **Dimostrazione 4 (Densità dell'Ordinamento tramite Punto Medio):**
  Siano $x, y \in \mathbb{R}$ con $x < y$. Consideriamo il punto medio $z = \frac{x+y}{2} = 2^{-1}(x + y)$, ove $2 = 1 + 1 \ge 1 > 0$.
  Dall'assioma (AO):
  $$x < y \implies x + y < y + y = 2y \implies \frac{x+y}{2} < y \implies z < y$$
  $$x < y \implies x + x < x + y \implies 2x < x + y \implies x < \frac{x+y}{2} \implies x < z$$
  Combinando le due disuguaglianze si ottiene $x < z < y$. $\blacksquare$

> [!tip]- Flashcard: Dimostrazione di $x^2 \ge 0$ e $1 > 0$
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Come si dimostra che in ogni campo ordinato $x^2 \ge 0$ per ogni $x \in \mathbb{R}$ e che $1 > 0$?
Back: 
1. **$x^2 \ge 0$:** Per tricotomia, o $x \ge 0$ o $x \le 0$. Se $x \ge 0$, per compatibilità (MO) $x \cdot x \ge 0 \cdot x = 0 \implies x^2 \ge 0$. Se $x \le 0$, allora $-x \ge 0$, quindi per compatibilità $(-x)^2 \ge 0$; ma $(-x)^2 = (-x)(-x) = x^2$, quindi $x^2 \ge 0$.
2. **$1 > 0$:** Per l'assioma dell'elemento neutro $1 = 1^2 \ge 0$. Poiché per assioma (M2) $1 \neq 0$, ne consegue $1 > 0$.
Tags: education/university education/math tech/logic
END
%%
> [!tip]- Flashcard: Densità dell'Ordinamento di R
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Cosa afferma la proprietà di densità dell'ordinamento reale e come si dimostra l'esistenza di un elemento compreso tra due reali distinti?
Back: Afferma che tra due reali distinti $x < y$ esiste sempre un terzo reale $z \in \mathbb{R}$ intermedio:
$$(\forall x, y \in \mathbb{R}) \; [x < y \implies (\exists\, z \in \mathbb{R}) \; x < z < y]$$
Dimostrazione costruttiva: si pone $z$ pari al punto medio $z = \frac{x+y}{2}$.
Da $x < y$ sommando $x$ si ha $2x < x + y \implies x < z$; sommando $y$ si ha $x + y < 2y \implies z < y$. Dunque $x < z < y$.
Tags: education/university education/math tech/logic
END
%%
---

## 4. Topologia della Retta: Intervalli di $\mathbb{R}$

Gli insiemi convessi fondamentali della retta reale sono gli intervalli \[[[Lezione 5 FdM.pdf#page=5|Dispensa p. 5]]].

> [!danger] Definizione 3.1: Intervalli Limitati e Illimitati
> Assegnati $a, b \in \mathbb{R}$ con $a \le b$:
> - **Intervalli Limitati:**
>   - **Intervallo Chiuso:** $[a, b] = \{x \in \mathbb{R} \mid a \le x \le b\}$
>   - **Intervallo Semiaperto a Destra:** $[a, b[ = \{x \in \mathbb{R} \mid a \le x < b\}$
>   - **Intervallo Semiaperto a Sinistra:** $]a, b] = \{x \in \mathbb{R} \mid a < x \le b\}$
>   - **Intervallo Aperto:** $]a, b[ = \{x \in \mathbb{R} \mid a < x < b\}$
> - **Ampiezza (o Misura) dell'Intervallo:**
>   Se $I \subset \mathbb{R}$ è un intervallo di estremi $a$ e $b$, si definisce l'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>ampiezza</b></font></mark> come:
>   $$|I| = b - a$$
>   Inoltre, per ogni coppia di punti $x, y \in I$, vale la disuguaglianza metrica:
>   $$|x - y| \le |I|$$
> - **Intervalli Illimitati:**
>   - Illimitati superiormente: $[a, +\infty[ = \{x \in \mathbb{R} \mid a \le x\}$ e $]a, +\infty[ = \{x \in \mathbb{R} \mid a < x\}$
>   - Illimitati inferiormente: $]-\infty, a] = \{x \in \mathbb{R} \mid x \le a\}$ e $]-\infty, a[ = \{x \in \mathbb{R} \mid x < a\}$

> [!tip]- Flashcard: Definizione e Misura degli Intervalli di R
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Come viene definita l'ampiezza $\vert I\vert$ di un intervallo limitato di estremi $a \le b$ e quale proprietà metrica soddisfa per ogni coppia di suoi punti?
Back: L'ampiezza (o misura) di $I$ è:
$$\vert I\vert = b - a$$
Per ogni coppia di punti $x, y \in I$, la loro distanza soddisfa:
$$\vert x - y\vert \le \vert I\vert$$
Infatti se $a \le x \le y \le b$, allora $\vert x - y\vert = y - x \le b - a = \vert I\vert$.
Tags: education/university education/math tech/logic
END
%%
---

## 5. Insiemi Limitati, Maggioranti, Minoranti, Massimo e Minimo

L'ordinamento totale consente di formalizzare la limitatezza dei sottoinsiemi di $\mathbb{R}$ \[[[Lezione 5 FdM.pdf#page=6|Dispensa p. 6]]].

### Maggioranti e Minoranti

> [!danger] Definizione 4.1: Maggioranti, Minoranti e Insiemi Limitati
> Sia $A \subseteq \mathbb{R}$ un sottoinsieme non vuoto ($A \neq \emptyset$).
> - Un numero reale $M \in \mathbb{R}$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>maggiorante</b></font></mark> di $A$ se:
>   $$(\forall a \in A) \; a \le M$$
>   L'insieme di tutti i maggioranti di $A$ si denota con $U(A) = \{M \in \mathbb{R} \mid (\forall a \in A) \; a \le M\}$ (dall'inglese *Upper bounds*).
> - Un numero reale $m \in \mathbb{R}$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>minorante</b></font></mark> di $A$ se:
>   $$(\forall a \in A) \; m \le a$$
>   L'insieme di tutti i minoranti di $A$ si denota con $L(A) = \{m \in \mathbb{R} \mid (\forall a \in A) \; m \le a\}$ (dall'inglese *Lower bounds*).
> - **Classificazione di Limitatezza:**
>   - $A$ è <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>limitato superiormente</b></font></mark> se $U(A) \neq \emptyset$ (ammette almeno un maggiorante).
>   - $A$ è <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>limitato inferiormente</b></font></mark> se $L(A) \neq \emptyset$ (ammette almeno un minorante).
>   - $A$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>limitato</b></font></mark> se è simultaneamente limitato superiormente e inferiormente.

> [!info] Osservazione 4.4: Insiemi Illimitati
> Negando le definizioni mediante le regole dei predicati e dei quantificatori introdotte in [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]:
> - $A$ è **illimitato superiormente** se:
>   $$(\forall M \in \mathbb{R}) (\exists\, a \in A) \; a > M$$
> - $A$ è **illimitato inferiormente** se:
>   $$(\forall m \in \mathbb{R}) (\exists\, a \in A) \; a < m$$

> [!tip]- Flashcard: Maggioranti e Minoranti
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: Sia $A \subseteq \mathbb{R}, A \neq \emptyset$.
- $M \in \mathbb{R}$ è un maggiorante di $A$ se {{c1::$(\forall a \in A) \; a \le M$}}.
- $m \in \mathbb{R}$ è un minorante di $A$ se {{c1::$(\forall a \in A) \; m \le a$}}.
- $A$ è illimitato superiormente se {{c2::$(\forall M \in \mathbb{R})(\exists a \in A) \; a > M$}}.
Tags: education/university education/math tech/logic
END
%%
### Massimo e Minimo di un Insieme

> [!danger] Definizione 4.5: Massimo e Minimo
> Sia $A \subseteq \mathbb{R}$ non vuoto.
> - Se l'insieme dei maggioranti $U(A)$ ammette un elemento che appartiene ad $A$, tale elemento si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>massimo</b></font></mark> di $A$:
>   $$M = \max A \iff (M \in A) \land (M \in U(A)) \iff (M \in A) \land (\forall a \in A) \; a \le M$$
> - Se l'insieme dei minoranti $L(A)$ ammette un elemento che appartiene ad $A$, tale elemento si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>minimo</b></font></mark> di $A$:
>   $$m = \min A \iff (m \in A) \land (m \in L(A)) \iff (m \in A) \land (\forall a \in A) \; m \le a$$
> 
> **Unicità:** Se il massimo (rispettivamente il minimo) esiste, esso è **unico** per la proprietà antisimmetrica (O2).

> [!example] Esempio Fondamentale del Docente: Limitatezza vs Esistenza di Massimo
> Consideriamo l'intervallo semiaperto a destra $A = [0, 1[$:
> - $A$ ammette minimo: infatti $0 \in A$ e per ogni $x \in A$ si ha $0 \le x$. Quindi $\min [0, 1[ = 0$.
> - $A$ è limitato superiormente: qualunque numero $M \ge 1$ è un maggiorante per $A$ (ad esempio $1, 2, 5 \in U(A)$).
> - Tuttavia, $A$ **non ammette massimo**! Infatti, se per assurdo esistesse $M = \max A$, dovrebbe essere $M \in [0, 1[$, ossia $M < 1$. Ma per la densità dell'ordinamento reale, esisterebbe un punto intermedio $z = \frac{M + 1}{2}$ tale che $M < z < 1$. Poiché $z < 1$, si avrebbe $z \in A$; ma $M < z$ contraddice il fatto che $M$ sia un maggiorante di $A$.
> 
> Questo controesempio cruciale dimostra che **essere limitato non equivale ad avere massimo**. Il numero $1$ è "il migliore" tra tutti i maggioranti, pur non appartenendo all'insieme \[[[Lezione 5 FdM.pdf#page=6|Dispensa p. 6]]].

> [!tip]- Flashcard: Massimo e Minimo di un Insieme
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Quali condizioni definiscono il massimo $M = \max A$ di un insieme $A \subseteq \mathbb{R}$ e perché essere limitato superiormente non garantisce l'esistenza del massimo?
Back: $M = \max A$ se e solo se soddisfa due condizioni congiunte:
1. $M$ appartiene all'insieme: $M \in A$
2. $M$ è un maggiorante di $A$: $(\forall a \in A) \; a \le M$
Un insieme limitato superiormente non possiede necessariamente massimo: ad esempio $A = [0, 1[$ è limitato superiormente da $1$, ma $1 \notin A$, e nessun elemento interno può essere maggiorante a causa della densità reale.
Tags: education/university education/math tech/logic
END
%%
---

## 6. Estremo Superiore ed Estremo Inferiore

La constatazione che non tutti gli insiemi limitati ammettono massimo conduce alla nozione cardine di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>estremo superiore</b></font></mark> e <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>estremo inferiore</b></font></mark> \[[[Lezione 5 FdM.pdf#page=6|Dispensa p. 6]]].

> [!danger] Definizione 4.8 e 4.9: Estremo Superiore ed Inferiore
> - Sia $A \subset \mathbb{R}, A \neq \emptyset$, limitato superiormente. L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>estremo superiore</b></font></mark> di $A$, indicato con $\sup A$, è il **minimo dell'insieme dei maggioranti** $U(A)$:
>   $$\sup A \overset{\text{def}}{=} \min U(A) = \min \{M \in \mathbb{R} \mid (\forall a \in A) \; a \le M\}$$
> - Sia $B \subset \mathbb{R}, B \neq \emptyset$, limitato inferiormente. L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>estremo inferiore</b></font></mark> di $B$, indicato con $\inf B$, è il **massimo dell'insieme dei minoranti** $L(B)$:
>   $$\inf B \overset{\text{def}}{=} \max L(B) = \max \{m \in \mathbb{R} \mid (\forall b \in B) \; m \le b\}$$

> [!summary] Proposizione 4.10: Relazione tra Estremi e Massimo/Minimo
> - $\max A$ esiste se e solo se $\sup A$ esiste e appartiene ad $A$:
>   $$\max A \text{ esiste} \iff \sup A \in A \quad\implies\quad \max A = \sup A$$
> - $\min B$ esiste se e solo se $\inf B$ esiste e appartiene a $B$:
>   $$\min B \text{ esiste} \iff \inf B \in B \quad\implies\quad \min B = \inf B$$

Nell'esempio precedente dell'intervallo $A = [0, 1[$, l'insieme dei maggioranti è $U(A) = [1, +\infty[$. Poiché l'intervallo $[1, +\infty[$ ammette minimo pari a $1$, si ha:
$$\sup [0, 1[ = \min [1, +\infty[ = 1$$
Poiché $1 \notin [0, 1[$, il massimo non esiste, ma l'estremo superiore esiste ed è pari a $1$.

> [!tip]- Flashcard: Estremo Superiore e Inferiore
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: Dato un sottoinsieme non vuoto $A \subset \mathbb{R}$:
- L'estremo superiore è il {{c1::minimo dei maggioranti}}: $\sup A = \min U(A)$.
- L'estremo inferiore è il {{c1::massimo dei minoranti}}: $\inf A = \max L(A)$.
- Il massimo $\max A$ esiste se e solo se {{c2::$\sup A \in A$}}, e in tal caso coincide con $\sup A$.
Tags: education/university education/math tech/logic
END
%%
---

## 7. Assioma di Completezza di Dedekind

La definizione di estremo superiore richiede che l'insieme dei maggioranti $U(A)$ ammetta minimo. Tuttavia, in un generico campo ordinato come $\mathbb{Q}$, questo non è affatto garantito!

> [!info] Il Limite Strutturale dei Numeri Razionali $\mathbb{Q}$
> Consideriamo il sottoinsieme dei razionali:
> $$S = \{q \in \mathbb{Q} \mid q > 0 \;\land\; q^2 < 2\}$$
> L'insieme $S$ è non vuoto e limitato superiormente in $\mathbb{Q}$ (ad esempio da $2 \in \mathbb{Q}$). Tuttavia, non esiste alcun numero razionale il cui quadrato sia $2$ ($\sqrt{2} \notin \mathbb{Q}$).
> Ne consegue che l'insieme dei maggioranti razionali $U(S) \cap \mathbb{Q}$ non ammette minimo in $\mathbb{Q}$: il campo razionale presenta delle "fratture" o "buchi".

Per impedire la presenza di buchi e garantire la continuità della retta numerica, si introduce l'assioma fondativo dell'Analisi Matematica dovuto al matematico tedesco <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Richard Dedekind</b></font></mark> \[[[Lezione 5 FdM.pdf#page=7|Dispensa p. 7]]].

> [!danger] Assioma 4.12: Assioma di Completezza (o di Continuità di Dedekind)
> Ogni sottoinsieme non vuoto e limitato superiormente di $\mathbb{R}$ ammette estremo superiore in $\mathbb{R}$ secondo l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma di completezza di Dedekind</b></font></mark>:
> $$(\forall A \subset \mathbb{R}, A \neq \emptyset) \; [U(A) \neq \emptyset \implies \exists\, \sup A \in \mathbb{R}]$$

### Teorema di Esistenza dell'Estremo Inferiore

L'assioma di completezza postula l'esistenza del $\sup$ per insiemi superiormente limitati. Da esso si deduce rigorosamente l'esistenza dell'$\inf$ per insiemi inferiormente limitati \[[[Lezione 5 FdM.pdf#page=7|Dispensa p. 7]]].

> [!summary] Proposizione 4.13: Esistenza dell'Estremo Inferiore
> Ogni sottoinsieme non vuoto e limitato inferiormente di $\mathbb{R}$ ammette <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>estremo inferiore</b></font></mark> in $\mathbb{R}$.

#### Dimostrazione Formale del Docente
Sia $B \subset \mathbb{R}, B \neq \emptyset$, un insieme limitato inferiormente. Vogliamo dimostrare che l'insieme dei suoi minoranti $L(B)$ ammette massimo, ossia che esiste $\inf B = \max L(B)$.
1. Poiché $B$ è limitato inferiormente, l'insieme dei minoranti $L(B)$ non è vuoto ($L(B) \neq \emptyset$).
2. Per definizione di minorante, per ogni $m \in L(B)$ e per ogni $b \in B$ vale $m \le b$.
3. Fissato un arbitrario elemento $b_0 \in B$, esso è perciò un maggiorante per l'insieme $L(B)$. Dunque l'insieme $L(B)$ è non vuoto e **limitato superiormente**!
4. In virtù dell'**Assioma di Completezza 4.12**, $L(B)$ ammette estremo superiore. Poniamo:
   $$i \overset{\text{def}}{=} \sup L(B)$$
5. Poiché ogni $b \in B$ è un maggiorante per $L(B)$ e $i$ è il minimo dei maggioranti di $L(B)$, si deduce che $i \le b$ per ogni $b \in B$.
6. Tale disuguaglianza dimostra che $i$ è a sua volta un minorante per $B$, ossia $i \in L(B)$.
7. Essendo $i$ un maggiorante di $L(B)$ ed appartenendo ad $L(B)$, ne è il **massimo**:
   $$i = \max L(B) \overset{\text{def}}{=} \inf B$$
Pertanto $\inf B$ esiste in $\mathbb{R}$. $\blacksquare$

> [!tip]- Flashcard: Assioma di Completezza ed Esistenza dell'Inf
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Cosa enuncia l'Assioma di Completezza di $\mathbb{R}$ e come garantisce l'esistenza dell'estremo inferiore per insiemi limitati inferiormente?
Back: 
- **Assioma di Completezza:** Ogni sottoinsieme non vuoto e limitato superiormente di $\mathbb{R}$ ammette estremo superiore ($\sup A \in \mathbb{R}$).
- **Esistenza dell'inf:** Se $B \neq \emptyset$ è limitato inferiormente, l'insieme dei suoi minoranti $L(B)$ è non vuoto e limitato superiormente da ogni $b \in B$. Per l'assioma di completezza esiste $i = \sup L(B)$. Si dimostra che $i \in L(B)$, quindi $i = \max L(B) = \inf B$.
Tags: education/university education/math tech/logic
END
%%
---

## 8. Teorema di Caratterizzazione dell'Estremo Superiore e Inferiore

Operativamente, non si calcola l'estremo superiore determinando l'intero insieme dei maggioranti e cercandone il minimo. Si impiega invece il <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>teorema di caratterizzazione</b></font></mark> \[[[Lezione 5 FdM.pdf#page=7|Dispensa p. 7]]].

> [!danger] Proposizione 4.14: Teorema di Caratterizzazione dell'Estremo Superiore
> Sia $\emptyset \neq A \subset \mathbb{R}$ un insieme limitato superiormente e sia $s \in \mathbb{R}$.
> Allora $s = \sup A$ se e solo se sono verificate simultaneamente le due condizioni:
> 1. $s$ è un maggiorante di $A$:
>    $$(\forall a \in A) \; a \le s$$
> 2. Nessun numero strettamente minore di $s$ può essere un maggiorante di $A$:
>    $$(\forall t < s) (\exists\, a \in A) \; t < a$$

#### Dimostrazione Formale

- **Parte "$\implies$" (Soltanto se):**
  Supponiamo che $s = \sup A$. La condizione (1) è vera per definizione, essendo $\sup A \in U(A)$.
  Per provare la condizione (2), ragioniamo per assurdo: supponiamo che esista $t < s$ tale che $(\forall a \in A) \; a \le t$.
  Ciò significherebbe che $t$ è un maggiorante di $A$ ($t \in U(A)$). Ma poiché per ipotesi $s = \min U(A)$, deve valere $s \le t$, contraddicendo l'ipotesi $t < s$. Dunque la condizione (2) è verificata.
- **Parte "$\impliedby$" (Se):**
  Ragioniamo per contronominale (metodo studiato in [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]): supponiamo che $s \neq \sup A$ e mostriamo che la congiunzione logica è falsa.
  - Se $s$ non è un maggiorante di $A$, la condizione (1) è falsa.
  - Se $s$ è un maggiorante ma non è il minimo maggiorante, significa che esiste un maggiorante $t \in U(A)$ strettamente minore di $s$ ($t < s$). Ma per definizione di maggiorante, $(\forall a \in A) \; a \le t$, il che nega esattamente la condizione (2).
  In entrambi i casi la congiunzione è falsa. $\blacksquare$

### Formulazione Analitica $\varepsilon$-Forma

In Analisi Matematica, ponendo $t = s - \varepsilon$ (con $\varepsilon > 0$), la condizione di caratterizzazione assume la celebre <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>caratterizzazione con $\varepsilon$</b></font></mark> adoperata nelle dimostrazioni sui limiti e sulle successioni:

> [!danger] Caratterizzazione Operativa con $\varepsilon > 0$
> - **Estremo Superiore:**
>   $$s = \sup A \iff \begin{cases} 1) \; (\forall a \in A) \; a \le s & \text{($s$ è un maggiorante)} \\ 2) \; (\forall \varepsilon > 0)(\exists\, a \in A) \; s - \varepsilon < a & \text{(se si scende di $\varepsilon$, si "pesca" un punto di $A$)} \end{cases}$$
> - **Estremo Inferiore:**
>   $$i = \inf B \iff \begin{cases} 1) \; (\forall b \in B) \; i \le b & \text{($i$ è un minorante)} \\ 2) \; (\forall \varepsilon > 0)(\exists\, b \in B) \; b < i + \varepsilon & \text{(se si sale di $\varepsilon$, si "pesca" un punto di $B$)} \end{cases}$$

> [!info] Intuizione Geometrica dell'Intervallo $[s - \varepsilon, s]$
> Sulla retta reale, comunque si fissi un intorno sinistro di ampiezza $\varepsilon > 0$ dell'estremo superiore $s$, cadrà sempre all'interno dell'intervallo $(s - \varepsilon, s]$ almeno un elemento $a \in A$. Non vi è alcuno "spazio vuoto" tra gli elementi dell'insieme e il loro estremo superiore.

> [!tip]- Flashcard: Teorema di Caratterizzazione dell'Estremo Superiore
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: Dato $\emptyset \neq A \subset \mathbb{R}$ superiormente limitato, $s = \sup A$ se e solo se:
1. {{c1::$(\forall a \in A) \; a \le s$}} ($s$ è maggiorante)
2. {{c2::$(\forall \varepsilon > 0)(\exists a \in A) \; s - \varepsilon < a$}} (non esistono maggioranti minori di $s$)
Extra: La formulazione equivalente con parametro d'ordine è $(\forall t < s)(\exists a \in A) \; t < a$.
Tags: education/university education/math tech/logic
END
%%
> [!tip]- Flashcard: Teorema di Caratterizzazione dell'Estremo Inferiore
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Cloze
Text: Dato $\emptyset \neq B \subset \mathbb{R}$ inferiormente limitato, $i = \inf B$ se e solo se:
1. {{c1::$(\forall b \in B) \; i \le b$}} ($i$ è minorante)
2. {{c2::$(\forall \varepsilon > 0)(\exists b \in B) \; b < i + \varepsilon$}} (non esistono minoranti maggiori di $i$)
Extra: La formulazione con parametro d'ordine è $(\forall t > i)(\exists b \in B) \; b < t$.
Tags: education/university education/math tech/logic
END
%%
---

## 9. Teorema dell'Elemento Separatore (Separazione di Dedekind)

Il coronamento geometrico della completezza reale è rappresentato dalla proprietà delle classi contigue e dal <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>teorema dell'elemento separatore</b></font></mark> \[[[Lezione 5 FdM.pdf#page=8|Dispensa p. 8]]].

> [!danger] Teorema 4.16: Teorema dell'Elemento Separatore
> Siano $A, B \subset \mathbb{R}$ due insiemi non vuoti tali che ogni elemento di $A$ precede ogni elemento di $B$:
> $$(\forall a \in A)(\forall b \in B) \quad a \le b$$
> Allora:
> 1. L'estremo superiore di $A$ non supera l'estremo inferiore di $B$:
>    $$\sup A \le \inf B$$
> 2. L'intervallo $[\sup A, \inf B]$ non è vuoto e ogni numero reale $\lambda \in [\sup A, \inf B]$ è un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>elemento separatore</b></font></mark> per le classi $A$ e $B$:
>    $$(\forall a \in A)(\forall b \in B) \quad a \le \lambda \le b$$

### Significato Fondativo e Continuità della Retta

In geometria sintetica, la retta euclidea è priva di interruzioni. Il Teorema dell'Elemento Separatore garantisce che tra due classi di punti ordinati $A$ e $B$ esiste **sempre almeno un punto reale di separazione**. 
Se le due classi sono "contigue" (ossia la distanza tra esse può essere resa arbitrariamente piccola: $\inf B - \sup A = 0$), l'elemento separatore $\lambda$ è **unico**, realizzando il punto di cesura perfetta postulato da <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Richard Dedekind</b></font></mark>.

È precisamente questa proprietà che differenzia $\mathbb{R}$ da $\mathbb{Q}$: se consideriamo in $\mathbb{Q}$ le classi $A = \{q \in \mathbb{Q} \mid q \le 0 \lor q^2 < 2\}$ e $B = \{q \in \mathbb{Q} \mid q > 0 \land q^2 > 2\}$, esse soddisfano $a \le b$, ma in $\mathbb{Q}$ **non esiste alcun elemento separatore**, poiché $\sqrt{2}$ non è razionale! In $\mathbb{R}$, invece, $\lambda = \sqrt{2} \in \mathbb{R}$ separa perfettamente i due insiemi.

> [!tip]- Flashcard: Teorema dell'Elemento Separatore
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::05 - Numeri Reali, Campo Ordinato, Estremo Superiore e Assioma di Completezza
START
Basic
Front: Cosa stabilisce il Teorema dell'Elemento Separatore per due insiemi $A, B \subset \mathbb{R}$ non vuoti tali che $a \le b$ per ogni $a \in A, b \in B$?
Back: Stabilisce che:
1. $\sup A \le \inf B$
2. Esiste almeno un elemento separatore $\lambda \in \mathbb{R}$, e precisamente ogni $\lambda \in [\sup A, \inf B]$ soddisfa:
$$(\forall a \in A)(\forall b \in B) \quad a \le \lambda \le b$$
Tale teorema esprime la continuità della retta reale ed è equivalente all'assioma di completezza.
Tags: education/university education/math tech/logic
END
%%
---

## 10. Quadro Sinottico delle Proprietà Fondamentali

La tabella seguente riassume l'architettura gerarchica assiomatica di $\mathbb{R}$:

| Livello Strutturale | Oggetto Matematico | Assiomi Chiave | Proprietà Distintive Raggiunte |
| :--- | :--- | :--- | :--- |
| **1. Struttura Algebrica** | $(\mathbb{R}, +, \cdot)$ | A1–A4, M1–M4, D | Gruppo abeliano additivo e moltiplicativo, campo commutativo, cancellazione, annullamento del prodotto, unicità di opposti/inversi. |
| **2. Struttura d'Ordine** | $(\mathbb{R}, \le)$ | O1–O4, AO, MO | Insieme totalmente ordinato, campo totalmente ordinato, positività dei quadrati ($x^2 \ge 0$), $1 > 0$, densità dell'ordinamento. |
| **3. Struttura di Completezza** | $(\mathbb{R}, \text{Assioma Sup})$ | Assioma 4.12 | Esistenza di $\sup$ e $\inf$, assenza di lacune numeriche (rette continue), teorema dell'elemento separatore, convergenza di Cauchy. |
