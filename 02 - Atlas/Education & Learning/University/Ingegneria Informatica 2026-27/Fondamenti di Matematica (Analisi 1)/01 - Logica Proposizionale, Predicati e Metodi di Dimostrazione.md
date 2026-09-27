---
status: permanent
type: lecture
area: education
related: ["[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[02 - Teoria degli Insiemi]]", "[[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]"]
aliases: ["Lezione 1 Fondamenti di Matematica", "FdM Lezione 1", "Logica Proposizionale, Predicati e Metodi di Dimostrazione"]
source: Lezione 1 FdM del 23/09/2026 - Prof. Saverio Salzo
title: "01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione"
date: '2026-09-23'
updated: 2026-09-27T18:00
tags: [education/university, education/math, tech/logic]
summary: "Fondamenti di logica e sillogismi, proposizioni e connettivi, tabelle di verità, leggi notevoli, predicati con quantificatori e dimostrazione per contronominale."
course: "Fondamenti di Matematica Analisi 1"
sources: ["[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Fondamenti di Matematica Analisi 1 MOC]] / [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]

# 01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione

- **Docente:** Prof. Saverio Salzo (Esercitatori: Dott. Giovanni Franzina, Prof.ssa Elisa Trasatti)
- **Contatti:** `saverio.salzo@uniroma1.it`, `giovanni.franzina@cnr.it`, `elisa.trasatti@uniroma1.it`
- **Data Lezione:** 2026-09-23
- **Materiale Didattico Ufficiale:** \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=1|Appunti Manoscritti Lezione 01]]]
- **Riferimento MOC:** [[Fondamenti di Matematica (Analisi 1) MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Lezione Successiva:** [[02 - Teoria degli Insiemi]]
- **Collegamento Interdisciplinare:** [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]

L'insegnamento di Analisi Matematica poggia su due concetti strutturali cardine: la proprietà di **completezza dei numeri reali** ($\mathbb{R}$) e il rigore del linguaggio formale. Da un punto di vista storico ed epistemologico, l'evoluzione della disciplina ha seguito un andamento a ritroso: il calcolo infinitesimale (derivate e integrali, formulati nel XVII secolo da Newton e Leibniz per risolvere problemi fisici e geometrici) ha preceduto di oltre due secoli la sua completa formalizzazione logica e assiomatica (sviluppata tra la fine dell'Ottocento e l'inizio del Novecento da Peano, Frege, Russell e Hilbert). La sistemazione assiomatica si è resa necessaria per eliminare i paradossi derivanti dall'intuito geometrico e costruire una teoria priva di fallacie deduttive.

Il <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>formalismo matematico</b></font></mark> non costituisce una complicazione fine a se stessa, ma lo strumento indispensabile per eliminare qualsiasi forma di <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>ambiguità</b></font></mark> insita nel linguaggio naturale, garantendo l'oggettività e la riproducibilità delle inferenze logiche \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=1|Appunti p. 1]]].

---

## Logica e Deduzione Formale

La logica costituisce lo studio delle regole formali del ragionamento valido, astraendo dal contenuto empirico delle affermazioni per analizzarne la pura struttura inferenziale.

### 1. Sillogismi e Validità Formale

Il modello classico del ragionamento deduttivo è rappresentato dal <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>sillogismo</b></font></mark>, in cui da due premesse assunte come vere discende necessariamente una conclusione. Il docente introduce la struttura attraverso l'argomento guida \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=1|Appunti p. 1]]]:

> *I Marziani vivono su Plutone.*
> *Socrate è un Marziano.*
> *Perciò, Socrate vive su Plutone.*

Analizzando la catena inferenziale nel formalismo relazionale:
- **Regola generale (implicazione condizionale):** *"Se $x$ è Marziano, allora $x$ vive su Plutone"*
- **Premessa (ipotesi):** *"Socrate è Marziano"* ($x = \text{Socrate}$)
- **Conclusione (tesi):** *"Socrate vive su Plutone"*

Anche se le affermazioni descrivono scenari privi di riscontro nella realtà fisica (i marziani non esistono e Plutone non è abitato), il ragionamento è formalmente **inappuntabile**: se le premesse fossero vere, la conclusione sarebbe ineluttabilmente vera. La matematica adotta il formalismo logico proprio per svincolare la correttezza del ragionamento dalle ambiguità e dalle interpretazioni soggettive del linguaggio ordinario.

> [!tip]- Flashcard: Struttura del Sillogismo e Validità Formale
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Basic
> Front: In cosa risiede la validità logica di un sillogismo (es. "Se $x$ è marziano, allora vive su Plutone") e perché la matematica adotta il formalismo?
> Back: La validità di un sillogismo risiede unicamente nella correttezza formale della struttura inferenziale: se la premessa (ipotesi) è vera, la conclusione (tesi) ne discende necessariamente, a prescindere dalla veridicità empirica dei termini. La matematica adotta il formalismo per eliminare ogni ambiguità del linguaggio naturale.
> Tags: education/university education/math tech/logic
> END
> %%

---

## Logica delle Proposizioni

### 1. Definizione di Proposizione

L'atomo elementare della logica proposizionale è la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>proposizione</b></font></mark> \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=1|Appunti p. 1]]].

> [!danger] Definizione: Proposizione
> Una **proposizione** è una frase dichiarativa del linguaggio naturale o formale alla quale è possibile attribuire, in modo univoco e oggettivo, uno e un solo valore di verità: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>vero ($V$)</b></font></mark> oppure <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>falso ($F$)</b></font></mark>, senza alcuna ambiguità interpretativa.

Nel formalismo matematico, le proposizioni semplici si denotano per convenzione con lettere latine maiuscole: $P, Q, R, S, \dots$.

> [!tip]- Flashcard: Definizione di Proposizione
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Basic
> Front: Qual è la definizione formale di proposizione nella logica matematica?
> Back: Una proposizione è una frase dichiarativa del linguaggio naturale o formale alla quale è possibile attribuire in modo univoco e oggettivo uno e un solo valore di verità: vero ($V$) oppure falso ($F$), senza alcuna ambiguità.
> Tags: education/university education/math tech/logic
> END
> %%

### 2. Differenze tra Proposizioni e Non-Proposizioni

Non ogni frase del linguaggio ordinario costituisce una proposizione:

> [!example] Esempi: Proposizioni vs Non-Proposizioni
> - **Proposizioni Valide (valori di verità ben definiti):**
>   - *"$4$ è un numero primo"* $\longrightarrow$ Proposizione valida (valore di verità: **F**).
>   - *"$\sqrt{2} \in \mathbb{R}$"* $\longrightarrow$ Proposizione valida (valore di verità: **V**).
>   - *"Tutti gli interi sono pari"* $\longrightarrow$ Proposizione valida (valore di verità: **F**).
> - **Non-Proposizioni (prive di valore di verità oggettivo):**
>   - *"Chiudi la porta!"* $\longrightarrow$ Frase imperativa / esortativa: non asserisce un fatto, dunque non ha senso chiedersi se sia vera o falsa.
>   - *"Napoli è lontana da Roma"* $\longrightarrow$ Affermazione soggettiva ed ambigua: priva di un parametro metrico quantitativo prefissato.

### 3. Composizione di Proposizioni e Operatori Logici

A partire da proposizioni atomiche, è possibile costruire espressioni più articolate mediante gli <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>operatori logici (connettivi logici)</b></font></mark> \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=1|Appunti p. 1]]].

> [!danger] Definizione: Operatori Logici (Connettivi)
> Siano $P$ e $Q$ proposizioni. Si definiscono le operazioni logiche fondamentali:
> 
> | Connettivo | Simbolo Formale | Nome Operazione | Lettura Verbale |
> | :--- | :---: | :--- | :--- |
> | **Negazione** | $\neg$ | Inversione logica | "non", "not" |
> | **Congiunzione** | $\land$ | Prodotto logico | "e", "and" |
> | **Disgiunzione** | $\lor$ | Somma logica inclusiva | "o", "or" (vel) |
> | **Implicazione** | $\implies$ | Condizionale | "se ... allora ...", "implica" |
> | **Equivalenza** | $\iff$ | Bicondizionale | "se e solo se", "equivale a" |
> 
> Le formule generate combinando connettivi:
> $$\neg P, \quad P \land Q, \quad P \lor Q, \quad P \implies Q, \quad P \iff Q$$
> sono a loro volta proposizioni, il cui valore di verità è determinato univocamente dai valori di verità delle singole componenti elementari.

### 4. Tabelle di Verità ed Esempi Applicativi

Le <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>tabelle di verità</b></font></mark> costituiscono lo strumento sistematico per enumerare tutti i possibili valori di verità assunti da una formula composta al variare delle combinazioni di verità delle variabili componenti.

#### Negazione ($\neg P$)
L'operatore monadico inverte il valore di verità della proposizione d'ingresso \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=2|Appunti p. 2]]]:

| $P$ | $\neg P$ |
| :---: | :---: |
| V | **F** |
| F | **V** |

#### Congiunzione ($P \land Q$) e Disgiunzione ($P \lor Q$)
Per chiarire la semantica dei connettivi binari, il docente propone l'analogia genitoriale tra madre e figlio per concedere l'uscita da casa \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=2|Appunti p. 2]]]:
1. *Regola A:* *"Per uscire devi fare i piatti **e** portare fuori l'immondizia"* ($P \land Q$).
2. *Regola B:* *"Per uscire devi fare i piatti **o** portare fuori l'immondizia"* ($P \lor Q$).

| $P$ | $Q$ | $P \land Q$ | $P \lor Q$ |
| :---: | :---: | :---: | :---: |
| V | V | **V** | **V** |
| V | F | F | **V** |
| F | V | F | **V** |
| F | F | F | **F** |

- **Congiunzione ($P \land Q$):** è vera **esclusivamente** quando entrambe le proposizioni $P$ e $Q$ sono vere.
- **Disgiunzione ($P \lor Q$):** è falsa **esclusivamente** quando entrambe le proposizioni $P$ e $Q$ sono false; in matematica si adotta **rigorosamente solo la disgiunzione inclusiva** ($P \lor Q$ è vera anche quando sia $P$ sia $Q$ sono entrambe vere). Questo principio si ricollega direttamente alla definizione di unione tra insiemi in [[02 - Teoria degli Insiemi]] e [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]].

#### Implicazione Materiale ($P \implies Q$)
La proposizione condizionale $P \implies Q$ ("se $P$, allora $Q$") vincola l'ipotesi $P$ alla tesi $Q$ \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=3|Appunti p. 3]]]:

| $P$ | $Q$ | $P \implies Q$ |
| :---: | :---: | :---: |
| V | V | **V** |
| V | F | **F** |
| F | V | **V** |
| F | F | **V** |

L'implicazione materiale è falsa **esclusivamente quando l'ipotesi è vera e la tesi è falsa**. Da una premessa falsa segue qualsiasi affermazione mantenendo vera la proposizione condizionale, principio noto come <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>ex falso quodlibet</b></font></mark> (impiegato nella dimostrazione che $\emptyset \subset A$ in [[02 - Teoria degli Insiemi]]).

> [!tip]- Flashcard: Implicazione Materiale e Falsificabilità
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Cloze
> Text: L'implicazione materiale $P \implies Q$ è falsa {{c1::esclusivamente quando l'ipotesi $P$ è vera e la tesi $Q$ è falsa}}. In tutte le altre tre combinazioni di verità ($V \implies V$, $F \implies V$, $F \implies F$) l'implicazione è sempre {{c2::vera}}.
> Extra: Principio "ex falso quodlibet": da una premessa falsa segue qualsiasi conclusione mantenendo vera la proposizione condizionale.
> Tags: education/university education/math tech/logic
> END
> %%

##### Condizione Necessaria vs Condizione Sufficiente
Nell'implicazione $P \implies Q$:
- $P$ è <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>condizione sufficiente</b></font></mark> per $Q$: la verità di $P$ garantisce infallibilmente la verità di $Q$.
- $Q$ è <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>condizione necessaria</b></font></mark> per $P$: se non si realizza $Q$, è impossibile che si sia verificata $P$.

> [!example] Esempio: Condizione Necessaria in Analisi Matematica
> Nel teorema sulla convergenza delle serie numeriche:
> $$\sum_{n=0}^{+\infty} a_n \text{ converge} \implies a_n \to 0$$
> L'annullamento del termine generale ($a_n \to 0$) è condizione **necessaria** affinché la serie converga, ma non è sufficiente (ad esempio nella serie armonica $\sum \frac{1}{n}$, dove il termine generale tende a zero ma la serie diverge).

> [!tip]- Flashcard: Condizione Necessaria vs Sufficiente
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Cloze
> Text: Nella proposizione condizionale $A \implies B$, $A$ rappresenta una {{c1::condizione sufficiente}} per $B$, mentre $B$ rappresenta una {{c2::condizione necessaria}} per $A$.
> Extra: Se non si verifica la condizione necessaria ($B$ è falsa), l'ipotesi $A$ non può essersi verificata.
> Tags: education/university education/math tech/logic
> END
> %%

#### Equivalenza Logica ($P \iff Q$)
L'equivalenza (o bicondizionale, "se e solo se") stabilisce che due proposizioni possiedono sempre il medesimo valore di verità \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=3|Appunti p. 3]]]:

| $P$ | $Q$ | $P \iff Q$ |
| :---: | :---: | :---: |
| V | V | **V** |
| V | F | F |
| F | V | F |
| F | F | **V** |

L'equivalenza corrisponde formalmente alla congiunzione di due implicazioni reciproche:
$$(P \iff Q) \equiv (P \implies Q) \land (Q \implies P)$$

---

## Leggi del Calcolo Proposizionale e Tautologie

Una formula proposizionale che risulta sempre vera per qualsiasi attribuzione di verità alle proposizioni atomiche componenti prende il nome di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>tautologia</b></font></mark> \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=4|Appunti p. 4]]].

> [!danger] Assioma / Principio Fondamentale: Legge del Terzo Escluso (Tertium Non Datur)
> Per qualunque proposizione $P$:
> $$P \lor (\neg P) \equiv V$$
> Una proposizione è o vera o falsa: non esiste una terza alternativa logica nel sistema classico bivalente.

> [!danger] Teorema: Leggi di De Morgan del Calcolo Proposizionale
> Siano $P$ e $Q$ due proposizioni. Valgono le equivalenze tautologiche:
> 1. $\neg(P \land Q) \iff (\neg P) \lor (\neg Q)$
> 2. $\neg(P \lor Q) \iff (\neg P) \land (\neg Q)$
> 
> La negazione logica rovescia il connettivo: la congiunzione ($\land$) diventa disgiunzione ($\lor$), e la disgiunzione diventa congiunzione.

> [!tip]- Flashcard: Leggi di De Morgan Proposizionali
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Cloze
> Text: Enunciare le due leggi di De Morgan per la logica proposizionale:
> 1. $\neg(P \land Q) \iff$ {{c1::$(\neg P) \lor (\neg Q)$}}
> 2. $\neg(P \lor Q) \iff$ {{c2::$(\neg P) \land (\neg Q)$}}
> Extra: La negazione inverte il connettivo logico: la congiunzione ($\land$) diventa disgiunzione ($\lor$) e viceversa.
> Tags: education/university education/math tech/logic
> END
> %%

> [!danger] Teorema: Legge della Contronominale (Contrapposizione Logica)
> Siano $P$ e $Q$ due proposizioni. Vale l'equivalenza:
> $$(P \implies Q) \iff (\neg Q \implies \neg P)$$
> Un'implicazione diretta è perfettamente equivalente alla sua implicazione contronominale, ottenuta scambiando ipotesi e tesi e negandole entrambe.

> [!tip]- Flashcard: Legge della Contronominale
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Basic
> Front: Come si formula la legge della contronominale e perché è utile nelle dimostrazioni matematiche?
> Back: $$(P \implies Q) \iff (\neg Q \implies \neg P)$$
> Permette di sostituire la dimostrazione diretta di un teorema con la dimostrazione equivalente della sua contronominale, che spesso risulta algebricamente molto più semplice e trasparente da trattare.
> Tags: education/university education/math tech/logic
> END
> %%

> [!summary] Metodo di Dimostrazione: Riduzione all'Assurdo (Reductio ad Absurdum)
> Siano $P$ l'ipotesi e $Q$ la tesi. La dimostrazione per assurdo si fonda sulla tautologia:
> $$(P \implies Q) \iff [(P \land \neg Q) \implies (R \land \neg R)]$$
> dove $R \land \neg R$ rappresenta una contraddizione ($F$). Se assumendo simultaneamente vera l'ipotesi $P$ e falsa la tesi ($\neg Q$) si deduce una contraddizione logica, allora l'assunzione $\neg Q$ è insostenibile e la tesi $Q$ deve essere necessariamente **vera**.

---

## Logica dei Predicati e Quantificatori

La logica delle proposizioni considera gli enunciati come blocchi indivisibili. Per esprimere proprietà matematiche dipendenti da variabili è necessario passare alla <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>logica dei predicati</b></font></mark> \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=5|Appunti p. 5]]].

> [!danger] Definizione: Predicato Logico (Proposizione Aperta)
> Un **predicato** (denotato con $P(x)$, $Q(x, y)$, ecc.) è un'espressione del linguaggio che contiene una o più variabili e che si trasforma in una proposizione (dotata di valore di verità vero o falso) non appena alle variabili viene sostituito un valore specifico del loro dominio di interpretazione.

> [!danger] Definizione: Quantificatori Logici
> Per trasformare una formula predicativa in un enunciato categorico valido sull'intero dominio si introducono i quantificatori:
> 1. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Quantificatore Universale ($\forall$)</b></font></mark>: si legge *"per ogni"*, *"qualunque sia"*:
>    $$(\forall x) \, P(x)$$
>    Afferma che la proprietà $P$ è vera per ogni elemento $x$ del dominio.
> 2. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Quantificatore Esistenziale ($\exists$)</b></font></mark>: si legge *"esiste"*, *"esiste almeno un"*:
>    $$(\exists x) \, P(x)$$
>    Afferma che nel dominio esiste almeno un elemento $x$ per il quale la proprietà $P$ è soddisfatta.

> [!info] Osservazione: Variabili Libere e Legate
> In un'espressione matematica:
> - Una variabile si dice **legata (o vincolata)** se ricade all'interno del campo d'azione di un quantificatore $(\forall x)$ o $(\exists x)$.
> - Una variabile si dice **libera** se non è vincolata da alcun quantificatore. Nell'Assioma 4 di specificazione di [[02 - Teoria degli Insiemi]], il predicato $P(x)$ richiede espressamente che la variabile $x$ compaia libera.

---

## Leggi della Quantificazione

### 1. Dualità e Negazione dei Quantificatori

Quando la negazione interagisce con i quantificatori, scambia il tipo di quantificatore e si applica internamente al predicato \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=6|Appunti p. 6]]]:

> [!danger] Teorema: Negazione dei Quantificatori
> Per ogni proposizione aperta $P(x)$:
> $$\neg [(\forall x) \, P(x)] \iff (\exists x) \, \neg P(x)$$
> $$\neg [(\exists x) \, P(x)] \iff (\forall x) \, \neg P(x)$$
> - **Negare un'affermazione universale** equivale a trovare almeno un controesempio che non la soddisfa;
> - **Negare un'affermazione esistenziale** equivale ad affermare che la proprietà non sussiste per alcun elemento (vale la sua negazione per tutti).

> [!tip]- Flashcard: Negazione dei Quantificatori
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)
> START
> Cloze
> Text: Sotto l'azione della negazione logica, i quantificatori si trasformano secondo le regole di dualità:
> - $\neg [(\forall x) \, P(x)] \iff$ {{c1::$(\exists x) \, \neg P(x)$}}
> - $\neg [(\exists x) \, P(x)] \iff$ {{c2::$(\forall x) \, \neg P(x)$}}
> Extra: Negare una proprietà universale equivale a trovare almeno un controesempio; negare una proprietà esistenziale equivale ad affermare che la negazione vale per tutti.
> Tags: education/university education/math tech/logic
> END
> %%

### 2. Quantificatori Multipli e Dipendenze

Nelle formule con più quantificatori, l'ordine di scrittura definisce la dipendenza logica e **non è permutabile** \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=7|Appunti p. 7]]]. Ad esempio:
- $(\forall x) (\exists y) \, P(x, y)$: per ogni elemento $x$, esiste un $y$ (che può dipendere dalla scelta di $x$);
- $(\exists y) (\forall x) \, P(x, y)$: esiste un elemento universale $y$ che va bene simultaneamente per tutti gli $x$.

### 3. Applicazione: Dimostrazione per Contronominale

Il docente illustra l'efficacia della dimostrazione per contronominale su un classico teorema di aritmetica dei numeri interi \[[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf#page=8|Appunti p. 8]]]:

> [!danger] Teorema: Parità del Quadrato e Dimostrazione per Contronominale
> Sia $x \in \mathbb{N}^+$. Vale l'implicazione:
> $$(\forall x) \, (x^2 \text{ è pari} \implies x \text{ è pari})$$
> 
> **Dimostrazione per Contronominale:**
> L'implicazione diretta $(P \implies Q)$ equivale logicamente alla contronominale $(\neg Q \implies \neg P)$:
> $$(\forall x) \, (x \text{ è dispari} \implies x^2 \text{ è dispari})$$
> 
> 1. **Ipotesi contronominale:** assumiamo che $x$ sia un intero positivo dispari.
> 2. Per definizione algebrica di numero dispari, esiste un intero $n \in \mathbb{N}$ tale che:
>    $$x = 2n + 1$$
> 3. Calcoliamo il quadrato di $x$:
>    $$x^2 = (2n + 1)^2 = 4n^2 + 4n + 1 = 2(2n^2 + 2n) + 1$$
> 4. Ponendo $k = 2n^2 + 2n$, poiché $n \in \mathbb{N}$ anche $k \in \mathbb{N}$. Dunque:
>    $$x^2 = 2k + 1$$
> 5. **Conclusione:** la quantità $x^2$ ha la forma canonica di un numero dispari.
> 
> Essendo dimostrata l'implicazione contronominale, per la legge di contrapposizione logica resta rigorosamente provato il teorema di partenza: se $x^2$ è pari, allora $x$ è pari.
