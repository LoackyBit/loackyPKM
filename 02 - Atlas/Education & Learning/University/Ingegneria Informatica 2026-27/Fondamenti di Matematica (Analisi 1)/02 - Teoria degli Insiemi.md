---
status: permanent
type: lecture
area: education
related: ["[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]", "[[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]"]
aliases: ["Lezione 2 Fondamenti di Matematica", "FdM Lezione 2", "Teoria degli Insiemi", "Assiomi della Teoria degli Insiemi", "Teoria Assiomatica degli Insiemi ZF"]
source: Lezione 2 FdM del 24/09/2026 - Prof. Saverio Salzo
title: "02 - Teoria degli Insiemi"
date: '2026-09-24'
updated: 2026-09-27T18:00
tags: [education/university, education/math, tech/logic]
summary: "Teoria assiomatica degli insiemi ZF: estensionalità, vuoto, inclusione, coppia, specificazione, unione, intersezione di famiglie, potenza, fondazione, Von Neumann, infinito e scelta."
course: "Fondamenti di Matematica Analisi 1"
sources: ["[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Fondamenti di Matematica Analisi 1 MOC]] / [[02 - Teoria degli Insiemi]]

# 02 - Teoria degli Insiemi

- **Docente:** Prof. [[Saverio Salzo]] / Canale A-L
- **Data Lezione:** 2026-09-24
- **Materiali Didattici Ufficiali:** \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=1|Dispensa Lezione 02 — Teoria degli Insiemi (Prof. Salzo)]]]
- **Riferimento MOC:** [[Fondamenti di Matematica (Analisi 1) MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Lezione Precedente:** [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]
- **Collegamento Interdisciplinare:** [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]] (dove la teoria degli insiemi fornisce la struttura algebrica per lo spazio campionario $\Omega$ e gli eventi aleatori)

La seconda lezione di Fondamenti di Matematica avvia la costruzione formale della <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>teoria assiomatica degli insiemi</b></font></mark>. L'obiettivo è definire gli enti e i procedimenti matematici partendo da nozioni primitive e postulati espliciti, eliminando ogni forma di ambiguità intuitiva e prevenendo le antinomie logiche scoperte all'inizio del Novecento.

La trattazione segue la formulazione della teoria assiomatica **ZF (Zermelo-Fraenkel)** in una versione accessibile e trasparente, nello spirito dell'opera di Paul Halmos, introducendo gli assiomi costruttivi dell'algebra insiemistica e completando il quadro con i complementi sulla fondazione, la costruzione dei numeri naturali di John von Neumann, l'assioma dell'infinito e l'assioma della scelta \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=1|Dispensa p. 1]]].

---

## Cenni Storici ed Epistemologici

La teoria degli insiemi fu concepita e sviluppata originariamente da Georg Cantor e Richard Dedekind intorno al 1870, per poi essere formalizzata nel linguaggio della logica da Gottlob Frege nei primi anni del Novecento. In seguito alla scoperta di celebri paradossi — primo fra tutti il **Paradosso di Russell** (1901) e l'antinomia di Burali-Forti — la teoria ingenua degli insiemi (*naive set theory*) dovette essere profondamente rifondata.

Il processo di assiomatizzazione rigorosa fu avviato da Ernst Zermelo nel 1908 e successivamente perfezionato da Abraham Fraenkel e Thoralf Skolem nel 1922. Il sistema risultante, noto come **teoria di Zermelo-Fraenkel (ZF)**, o **ZFC** con l'inclusione dell'Assioma della Scelta (*Choice*), costituisce il fondamento standard su cui poggia l'intera matematica contemporanea e l'analisi infinitesimale.

---

## Concetti Primitivi e Linguaggio dei Predicati

La teoria degli insiemi si occupa di oggetti formali denominati <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>insiemi</b></font></mark>. Il concetto di insieme è assunto come **primitivo**: non è riconducibile a definizioni più elementari, ma viene qualificato e governato esclusivamente dagli assiomi della teoria (in piena analogia con i concetti di punto, retta e piano nella geometria euclidea) \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=1|Dispensa p. 1]]].

Intuitivamente, gli insiemi rappresentano collezioni di oggetti. Nella teoria pura non vi sono enti non-insiemistici: **tutti gli oggetti del discorso matematico sono insiemi**. Quando si scrive $x \in A$, anche l'elemento $x$ è a sua volta un insieme.

Per articolare la teoria si adotta la [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione#Logica dei Predicati|logica dei predicati]]. Le lettere minuscole e maiuscole ($a, b, x, y, A, B, X, Y, \mathcal{F}, \mathcal{G}$) rappresentano variabili del linguaggio che denotano insiemi.

Tra gli insiemi sono stabilite due <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>relazioni primitive</b></font></mark>:
1. **Relazione di appartenenza ($\in$):** $x \in A$ asserisce che $x$ è un elemento di $A$ (o che $x$ appartiene ad $A$). È considerata un predicato atomico.
2. **Relazione di uguaglianza ($=$):** $x = y$ asserisce che due simboli identificano il medesimo oggetto matematico. È anch'essa assunta come predicato atomico.

A partire dai predicati atomici si costruiscono tutti i predicati complessi mediante i connettivi logici e i quantificatori:
$$\land, \quad \lor, \quad \neg, \quad \implies, \quad \impliedby, \quad \iff, \quad \forall, \quad \exists$$

### Proprietà Fondamentali dell'Uguaglianza

La relazione primitiva di uguaglianza gode delle tre proprietà caratteristiche di una relazione di equivalenza:
- **Riflessività:** $(\forall x) \, (x = x)$
- **Simmetria:** $(\forall x, y) \, (x = y \implies y = x)$
- **Transitività:** $(\forall x, y, z) \, (x = y \land y = z \implies x = z)$

### Abbreviazioni Notazionali Canoniche

Per snellire la scrittura formale si adottano le consuete abbreviazioni matematiche:
- $\neg(x \in A)$ si denota con $x \notin A$ (non appartenenza);
- $\neg(x = y)$ si denota con $x \ne y$ (disuguaglianza);
- $(\forall x) \, (x \in A \implies P(x))$ si abbrevia con $(\forall x \in A) \, P(x)$ (quantificazione universale ristretta);
- $(\exists x) \, (x \in A \land P(x))$ si abbrevia con $(\exists x \in A) \, P(x)$ (quantificazione esistenziale ristretta).

> [!tip]- Flashcard: Relazioni Primitive e Oggetti della Teoria
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Quali sono le relazioni primitive della teoria assiomatica degli insiemi e che natura hanno i suoi elementi?
> Back: Le relazioni primitive sono due predicati atomici non definiti: l'appartenenza ($\in$) e l'uguaglianza ($=$). Tutti gli oggetti della teoria sono insiemi: quando scriviamo $x \in A$, anche l'elemento $x$ è a sua volta, intrinsecamente, un insieme.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 1. Assioma di Estensionalità

L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma di estensionalità</b></font></mark> stabilisce il criterio d'identità tra insiemi, legando la relazione di uguaglianza alla relazione di appartenenza \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=2|Dispensa p. 2]]].

> [!danger] Assioma 1: Assioma di Estensionalità
> Siano $A$ e $B$ due insiemi. Allora:
> $$A = B \iff (\forall x) \, (x \in A \iff x \in B)$$

Questo assioma prescrive che due insiemi sono uguali se e solo se hanno gli stessi identici elementi. Gli insiemi sono caratterizzati esclusivamente dalla loro estensione (dagli elementi che vi appartengono), indipendentemente dall'ordine con cui sono enunciati o dalla presenza di ripetizioni.

> [!tip]- Flashcard: Assioma di Estensionalità
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Cloze
> Text: Dati due insiemi $A$ e $B$, l'assioma di estensionalità stabilisce che {{c1::$A = B \iff (\forall x) \, (x \in A \iff x \in B)$}}.
> Extra: Due insiemi sono identici se e solo se hanno gli stessi elementi; l'identità dipende unicamente dalla loro estensione.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 2. Assioma dell'Insieme Vuoto

Mentre l'assioma di estensionalità descrive la relazione tra insiemi, non garantisce l'esistenza di alcun oggetto nel discorso. L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma dell'insieme vuoto</b></font></mark> assicura l'esistenza del primo ente matematico concreto \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=2|Dispensa p. 2]]].

> [!danger] Assioma 2: Assioma dell'Insieme Vuoto
> Esiste (ed è unico) l'insieme che non possiede elementi. Tale insieme si chiama **insieme vuoto** e si denota con $\emptyset$:
> $$(\forall x) \, (x \notin \emptyset)$$

> [!info] Osservazione: Derivabilità dell'Insieme Vuoto
> L'esistenza dell'insieme vuoto non richiederebbe necessariamente un assioma autonomo, potendosi dedurre dall'Assioma 4 di specificazione applicato a un predicato sempre falso: $\emptyset := \{x \in A \mid x \ne x\}$. Viene incluso esplicitamente per ragioni di chiarezza ed eleganza espositiva.

> [!tip]- Flashcard: Assioma dell'Insieme Vuoto ed Unicità
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Come si formula l'assioma dell'insieme vuoto e perché tale insieme è necessariamente unico?
> Back: Esiste un insieme privo di elementi: $(\forall x) \, (x \notin \emptyset)$. È unico in virtù dell'assioma di estensionalità: se esistessero due insiemi privi di elementi $\emptyset_1$ e $\emptyset_2$, la condizione $(\forall x)(x \in \emptyset_1 \iff x \in \emptyset_2)$ risulterebbe vera per vacuità ($F \iff F$), imponendo $\emptyset_1 = \emptyset_2$.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 3. Relazione di Inclusione e Sottoinsiemi

Accanto alle nozioni primitive, introduciamo per definizione la relazione di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>inclusione insiemistica</b></font></mark> \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=2|Dispensa p. 2]]].

> [!danger] Definizione 1.1: Sottoinsieme (Inclusione Insiemistica)
> Siano $A$ e $B$ due insiemi. Si scrive $B \subset A$ (oppure $B \subseteq A$) per denotare che:
> $$(\forall x) \, (x \in B \implies x \in A)$$
> e si dice che $B$ è un **sottoinsieme** di $A$ (o che $B$ è contenuto in $A$, o che $B$ è una parte di $A$).
> Se $B \subset A$ e $B \ne A$, allora $B$ si dice **sottoinsieme proprio** di $A$.

> [!example] Esempio 1.2: Inclusione dell'Insieme Vuoto e Riflessività
> Sia $A$ un insieme generico. Valgono sempre le inclusioni:
> $$\emptyset \subset A \quad \text{e} \quad A \subset A$$
> 
> **Dimostrazione Formale:**
> 1. Per verificare che $\emptyset \subset A$, applichiamo la Definizione 1.1: dobbiamo provare che $(\forall x) \, (x \in \emptyset \implies x \in A)$. Per l'Assioma 2, la premessa $x \in \emptyset$ è falsa per ogni elemento $x$. Per la semantica dell'implicazione materiale nella logica proposizionale, una proposizione condizionale con premessa falsa è identicamente vera (*ex falso quodlibet*). Ne consegue che l'implicazione è vera per qualunque $x$, dimostrando che $\emptyset \subset A$.
> 2. Per verificare che $A \subset A$, dobbiamo provare che $(\forall x) \, (x \in A \implies x \in A)$. Assegnando al predicato $x \in A$ il valore proposizionale $P$, l'espressione assume la forma $P \implies P$, che è una tautologia sempre vera per ogni $x$. Dunque ogni insieme è sottoinsieme di se stesso (proprietà riflessiva dell'inclusione).

> [!tip]- Flashcard: Inclusione Universale dell'Insieme Vuoto
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si dimostra formalmente che per ogni insieme $A$ vale $\emptyset \subset A$?
Back: Applicando la definizione di inclusione, dobbiamo verificare che $(\forall x) \, (x \in \emptyset \implies x \in A)$. Poiché per l'assioma dell'insieme vuoto la premessa $x \in \emptyset$ è sempre falsa per qualsiasi $x$, l'implicazione logica risulta identicamente vera per il principio di *ex falso quodlibet*. Dunque $\emptyset \subset A$ vale universalmente.
Tags: education/university education/math tech/logic
END
%%

> [!danger] Teorema: Principio della Doppia Inclusione
> Dati due insiemi $A$ e $B$:
> $$A = B \iff (A \subset B \land B \subset A)$$
> 
> **Dimostrazione:**
> - **$(\implies)$:** Se $A = B$, allora per l'Assioma 1 vale $(\forall x)(x \in A \iff x \in B)$. Scomponendo il bicondizionale nella congiunzione di due implicazioni, otteniamo $(\forall x)(x \in A \implies x \in B)$ (ossia $A \subset B$) e $(\forall x)(x \in B \implies x \in A)$ (ossia $B \subset A$).
> - **$(\impliedby)$:** Se valgono congiuntamente $A \subset B$ e $B \subset A$, allora per ogni $x$ sono vere contemporaneamente le implicazioni $x \in A \implies x \in B$ e $x \in B \implies x \in A$. Per la definizione del connettivo $\iff$, ciò equivale a $(\forall x)(x \in A \iff x \in B)$, che per l'Assioma 1 implica $A = B$.

> [!tip]- Flashcard: Principio della Doppia Inclusione
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si enuncia e dimostra il principio della doppia inclusione per l'uguaglianza tra insiemi?
Back: Dati due insiemi $A$ e $B$:
$$A = B \iff (A \subset B \land B \subset A)$$
Dimostrazione: per l'assioma di estensionalità $A = B \iff (\forall x)(x \in A \iff x \in B)$. Scomponendo il bicondizionale nella congiunzione di due implicazioni reciproche, si ottiene $(\forall x)(x \in A \implies x \in B)$ ($A \subset B$) e $(\forall x)(x \in B \implies x \in A)$ ($B \subset A$).
Tags: education/university education/math tech/logic
END
%%

---

## 4. Assioma della Coppia Non Ordinata e Genesi degli Insiemi

Per costruire nuovi insiemi a partire da enti già noti, si postula l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma della coppia non ordinata</b></font></mark> \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=3|Dispensa p. 3]]].

> [!danger] Assioma 3: Assioma della Coppia Non Ordinata
> Siano $x$ e $y$ insiemi. Esiste un (unico) insieme, indicato con $\{x, y\}$ e chiamato **coppia non ordinata** formata da $x$ e $y$, che possiede $x$ e $y$ come suoi unici elementi:
> $$(\forall z) \, (z \in \{x, y\} \iff z = x \lor z = y)$$
> Si pone inoltre:
> $$\{x\} := \{x, x\}$$
> detto **singoletto** (o insieme ridotto ad un solo elemento). Evidentemente vale:
> $$(\forall z) \, (z \in \{x\} \iff z = x)$$

> [!tip]- Flashcard: Assioma della Coppia Non Ordinata e Singoletto
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Cloze
Text: Dati due insiemi $x$ e $y$, l'assioma della coppia non ordinata assicura l'esistenza dell'insieme {{c1::$\{x, y\}$}} tale che {{c2::$z \in \{x, y\} \iff z = x \lor z = y$}}. Il singoletto è definito ponendo {{c3::$\{x\} := \{x, x\}$}}, per cui $z \in \{x\} \iff z = x$.
Extra: L'assioma della coppia permette la genesi di insiemi con elementi distinti a partire dal solo insieme vuoto.
Tags: education/university education/math tech/logic
END
%%

> [!example] Esempio 1.3: Costruzione di Insiemi dall'Insieme Vuoto
> All'inizio del sistema formale l'unico insieme esistente è l'insieme vuoto $\emptyset$. Applicando iterativamente l'assioma della coppia non ordinata possiamo costruire la successione di insiemi distinti:
> $$\emptyset, \quad \{\emptyset\}, \quad \{\emptyset, \{\emptyset\}\}, \quad \{\{\emptyset\}, \{\emptyset, \{\emptyset\}\}\}$$
> 
> È cruciale notare la distinzione ontologica:
> $$\emptyset \ne \{\emptyset\}$$
> L'insieme vuoto $\emptyset$ possiede $0$ elementi; il singoletto $\{\emptyset\}$ possiede $1$ elemento (il cui unico elemento è l'insieme vuoto stesso: $\emptyset \in \{\emptyset\}$).

> [!info] Osservazione 1.4: Metafore dei Diagrammi di Venn e delle Scatole
> Per visualizzare gli insiemi si impiegano due metafore intuitive:
> 1. **Diagrammi di Venn:** gli insiemi sono rappresentati come regioni del piano.
> 2. **Metafora delle Scatole (o dei Sacchi):** gli insiemi sono assimilabili a scatole che contengono altre scatole. In tale rappresentazione l'insieme vuoto $\emptyset$ è la scatola vuota, $\{\emptyset\}$ è una scatola che racchiude al suo interno la scatola vuota, e $\{\emptyset, \{\emptyset\}\}$ è una scatola contenente due scatole distinte.

![[Schema - Teoria degli Insiemi - Metafora delle Scatole.png]]
*(Rappresentazione secondo la metafora delle scatole: a sinistra l'insieme vuoto $\emptyset$, al centro il singoletto $\{\emptyset\}$, a destra l'insieme a due elementi $\{\emptyset, \{\emptyset\}\}$ — rif. \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=3|Dispensa p. 3]]])*

> [!tip]- Flashcard: Insieme Vuoto vs Singoletto del Vuoto
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Perché l'insieme vuoto $\emptyset$ e il singoletto $\{\emptyset\}$ sono ontologicamente distinti?
> Back: $\emptyset$ non possiede elementi (cardinalità $0$: $(\forall x) \, x \notin \emptyset$). L'insieme $\{\emptyset\}$ è invece un singoletto (cardinalità $1$) che ha come unico elemento l'insieme vuoto stesso ($\emptyset \in \{\emptyset\}$). Per l'assioma di estensionalità non hanno gli stessi elementi, quindi $\emptyset \ne \{\emptyset\}$.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 5. Assioma di Specificazione

L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma di specificazione</b></font></mark> (o di separazione) stabilisce che qualsiasi proprietà logica ben formulata ritaglia un sottoinsieme all'interno di un insieme universo preesistente \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=3|Dispensa p. 3]]].

> [!danger] Assioma 4: Assioma di Specificazione (o di Separazione)
> Sia $A$ un insieme e sia $P(x)$ un predicato in cui compare libera la variabile $x$ (ossia $x$ non è vincolata a monte da un quantificatore $(\forall x)$). Allora esiste un (unico) insieme, denotato con $\{x \in A \mid P(x)\}$, tale che:
> $$(\forall a) \, (a \in \{x \in A \mid P(x)\} \iff a \in A \land P(a))$$

Questo assioma permette di definire sottoinsiemi specificando una proprietà caratteristica $P(x)$. L'unicità dell'insieme $\{x \in A \mid P(x)\}$ è assicurata dall'assioma di estensionalità.

### Prevenzione del Paradosso di Russell

Il vincolo dell'Assioma 4 di specificare la proprietà su un **insieme $A$ già dato** è il meccanismo che preserva la teoria dalle contraddizioni:
- Se si ammettesse l'assioma di comprensione ingenua (poter formare l'insieme di tutti gli $x$ che soddisfano $P(x)$ senza vincolo a un universo $A$, ossia $\{x \mid P(x)\}$), ponendo $P(x) \equiv x \notin x$ si potrebbe formare l'insieme di Russell:
  $$R := \{x \mid x \notin x\}$$
- Valutando l'appartenenza di $R$ a se stesso, si otterrebbe l'antinomia insolubile:
  $$R \in R \iff R \notin R$$
- Con l'Assioma 4, invece, è possibile definire soltanto $R_A := \{x \in A \mid x \notin x\}$. Valutando $R_A$, si conclude semplicemente che $R_A \notin A$, dimostrando che **non può esistere l'insieme universale di tutti gli insiemi**.

> [!tip]- Flashcard: Assioma di Specificazione e Paradosso di Russell
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Come è formulato l'assioma di specificazione e quale fallacia logica previene?
> Back: Dato un insieme $A$ e un predicato $P(x)$, esiste l'insieme $\{x \in A \mid P(x)\}$ tale che: $(\forall a) \, (a \in \{x \in A \mid P(x)\} \iff a \in A \land P(a))$. Richiede di vincolare la proprietà a un insieme $A$ preesistente per prevenire insiemi autocontraddittori privi di universo, come quello del Paradosso di Russell ($R = \{x \mid x \notin x\}$).
> Tags: education/university education/math tech/logic
> END
> %%

---

## 6. Operazioni Insiemistiche: Intersezione, Differenza e Complementare

Appoggiandoci all'Assioma 4 di specificazione possiamo definire rigorosamente le prime fondamentali operazioni tra insiemi \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=4|Dispensa p. 4]]].

> [!danger] Definizione 1.5: Intersezione, Differenza e Complementare
> Siano $A$ e $B$ due insiemi.
> 1. Si pone:
>    $$A \cap B := \{x \in A \mid x \in B\}$$
>    e si chiama **intersezione di $A$ e $B$**. Evidentemente vale:
>    $$(\forall x) \, (x \in A \cap B \iff x \in A \land x \in B)$$
> 2. Si pone:
>    $$A \setminus B := \{x \in A \mid x \notin B\}$$
>    e si chiama **differenza tra $A$ e $B$** (o $A - B$). Evidentemente vale:
>    $$(\forall x) \, (x \in A \setminus B \iff x \in A \land x \notin B)$$
> 3. Se $B \subset A$, l'insieme $A \setminus B$ si denota anche con $\complement_A(B)$ e si chiama **complementare di $B$ rispetto ad $A$**:
>    $$\complement_A(B) := A \setminus B = \{x \in A \mid x \notin B\} \quad (\text{per } B \subset A)$$

![[Schema - Teoria degli Insiemi - Operazioni Insiemistiche.png]]
*(Rappresentazione delle operazioni fondamentali: a sinistra l'intersezione $A \cap B$, al centro la differenza $A \setminus B$, a destra il complementare $\complement_A(B)$ — rif. \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=4|Dispensa p. 4]]])*

> [!tip]- Flashcard: Intersezione, Differenza e Complementare
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Cloze
> Text: L'intersezione è definita da $A \cap B :=$ {{c1::$\{x \in A \mid x \in B\}$}} e corrisponde alla congiunzione logica. La differenza è definita da $A \setminus B :=$ {{c2::$\{x \in A \mid x \notin B\}$}}. Quando $B \subset A$, la differenza prende il nome di {{c3::complementare di $B$ rispetto ad $A$}} e si scrive $\complement_A(B)$.
> Extra: Entrambe le operazioni sono rigorosamente ricavate mediante l'Assioma 4 di specificazione applicato sull'universo $A$.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 7. Intersezione di una Famiglia di Insiemi

L'intersezione può essere generalizzata non soltanto a due insiemi, ma a una collezione arbitraria (finita o infinita) di insiemi \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=4|Dispensa p. 4]]].

> [!danger] Definizione 1.6: Intersezione di una Famiglia di Insiemi
> Sia $\mathcal{F}$ un insieme non vuoto (inteso come una collezione o famiglia di insiemi). Allora esiste almeno un elemento $B \in \mathcal{F}$, e mediante l'Assioma 4 di specificazione possiamo definire l'insieme:
> $$X := \{x \in B \mid (\forall A \in \mathcal{F}) \, (x \in A)\}$$
> Evidentemente vale:
> $$(\forall x) \, (x \in X \iff (\forall A \in \mathcal{F}) \, (x \in A))$$
> L'insieme $X$ non dipende dalla scelta iniziale dell'insieme $B \in \mathcal{F}$ e si chiama **intersezione degli insiemi di $\mathcal{F}$**, denotato con:
> $$\bigcap \mathcal{F} \quad \text{oppure} \quad \bigcap_{A \in \mathcal{F}} A$$

Intuitivamente, se la famiglia $\mathcal{F}$ contiene gli insiemi $A, B, C, D, \dots$, l'intersezione corrisponde alla parte comune a tutti:
$$\bigcap \mathcal{F} = A \cap B \cap C \cap D \cap \dots$$

> [!tip]- Flashcard: Intersezione di una Famiglia di Insiemi
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si definisce rigorosamente l'intersezione di una famiglia non vuota di insiemi $\mathcal{F}$ mediante l'Assioma di Specificazione?
Back: Scelto un elemento $B \in \mathcal{F}$, si definisce mediante l'Assioma 4:
$$\bigcap \mathcal{F} := \{x \in B \mid (\forall A \in \mathcal{F}) \, (x \in A)\}$$
Tale insieme non dipende dalla scelta iniziale di $B$ e soddisfa:
$$(\forall x) \, (x \in \bigcap \mathcal{F} \iff (\forall A \in \mathcal{F})(x \in A))$$
Tags: education/university education/math tech/logic
END
%%

---

## 8. Assioma dell'Unione e Unione di Insiemi

A differenza dell'intersezione, per unire due o più insiemi generici **non è possibile fare ricorso all'Assioma 4 di specificazione**, poiché non disponiamo a priori di un insieme universo già costituito che contenga entrambi gli insiemi. L'esistenza dell'unione deve essere quindi introdotta tramite un apposito postulato \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=4|Dispensa p. 4]]].

> [!tip]- Flashcard: Perché l'Unione Richiede un Assioma Autonomo
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Perché per definire l'unione di insiemi non è possibile usare l'Assioma di Specificazione e serve un assioma autonomo?
Back: L'Assioma di Specificazione consente di ritagliare sottoinsiemi solo a partire da un insieme universo $A$ già esistente nel sistema formale. Per due insiemi generici $A$ e $B$ non si dispone a priori di un insieme più grande che li contenga entrambi; l'esistenza di un insieme contenitore deve essere postulata espressamente tramite l'Assioma dell'Unione.
Tags: education/university education/math tech/logic
END
%%

> [!danger] Assioma 5: Assioma dell'Unione
> Sia $\mathcal{F}$ un insieme (pensato come una famiglia di insiemi). Esiste un insieme, che denotiamo con $\bigcup \mathcal{F}$ o con $\bigcup_{A \in \mathcal{F}} A$ e chiamiamo **unione degli insiemi di $\mathcal{F}$**, che ha per elementi tutti e soli gli elementi appartenenti ad almeno un insieme di $\mathcal{F}$:
> $$(\forall x) \, \left(x \in \bigcup \mathcal{F} \iff (\exists A \in \mathcal{F}) \, (x \in A)\right)$$

> [!example] Esempio 1.7: Metafora dei Sacchi di Grano
> Supponiamo che $\mathcal{F}$ sia un insieme di sacchi di grano. Ciascun sacco contiene chicchi di grano (elementi). Se immaginiamo di svuotare tutti i singoli sacchi in un sacco più grande, otterremo esattamente l'unione $\bigcup \mathcal{F}$.

> [!danger] Definizione 1.8: Unione di Due Insiemi
> Siano $A$ e $B$ due insiemi. Si definisce l'insieme **unione di $A$ e $B$** come l'unione della famiglia costituita dalla coppia non ordinata $\{A, B\}$ (costruita mediante l'Assioma 3):
> $$A \cup B := \bigcup \{A, B\}$$
> Evidentemente vale la caratterizzazione formale:
> $$(\forall x) \, (x \in A \cup B \iff (\exists X \in \{A, B\}) \, (x \in X) \iff x \in A \lor x \in B)$$

L'operazione di unione riflette esattamente la **disgiunzione logica inclusiva** ($\lor$).

![[Schema - Teoria degli Insiemi - Unione di Insiemi e Famiglie.png]]
*(Rappresentazione dell'unione: a sinistra l'unione binaria $A \cup B$; a destra l'unione della famiglia $\mathcal{F}$ che raccoglie tutti gli elementi degli insiemi costitutivi — rif. \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=5|Dispensa p. 5]]])*

> [!tip]- Flashcard: Assioma dell'Unione e Definizione di $A \cup B$
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Come viene formulato l'assioma dell'unione e come si definisce l'unione di due insiemi $A \cup B$?
> Back: L'assioma stabilisce che data una famiglia di insiemi $\mathcal{F}$, esiste l'insieme $\bigcup \mathcal{F}$ tale che $(\forall x) \, (x \in \bigcup \mathcal{F} \iff (\exists A \in \mathcal{F})(x \in A))$. L'unione di due insiemi è definita applicando tale assioma alla coppia non ordinata: $A \cup B := \bigcup \{A, B\}$, corrispondente alla disgiunzione logica $(\forall x)(x \in A \cup B \iff x \in A \lor x \in B)$.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 9. Proprietà dell'Algebra Insiemistica e Leggi di De Morgan

L'interazione tra le operazioni di unione, intersezione e differenza genera una struttura algebrica (algebra di Boole degli insiemi) governata dalla seguente proposizione fondamentale \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=5|Dispensa p. 5]]].

> [!summary] Proposizione 1.9: Proprietà dell'Unione e dell'Intersezione
> Siano $A, B$ e $C$ insiemi. Valgono le seguenti proprietà:
> 1. **Insieme Vuoto (Elemento Assorbente e Neutro):**
>    $$A \cap \emptyset = \emptyset \quad \text{e} \quad A \cup \emptyset = A$$
> 2. **Idempotenza:**
>    $$A \cap A = A \quad \text{e} \quad A \cup A = A$$
> 3. **Proprietà Commutativa:**
>    $$A \cap B = B \cap A \quad \text{e} \quad A \cup B = B \cup A$$
> 4. **Proprietà Associativa:**
>    $$(A \cap B) \cap C = A \cap (B \cap C) \quad \text{e} \quad (A \cup B) \cup C = A \cup (B \cup C)$$
> 5. **Proprietà Distributiva:**
>    $$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$$
>    $$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$$
> 6. **Leggi di De Morgan Insiemistiche (per la differenza):**
>    $$A \setminus (B \cap C) = (A \setminus B) \cup (A \setminus C)$$
>    $$A \setminus (B \cup C) = (A \setminus B) \cap (A \setminus C)$$
> 
> In particolare, se $B$ e $C$ sono sottoinsiemi di $A$ ($B, C \subset A$), le leggi di De Morgan si riformulano mediante la notazione di complementare:
> $$\complement_A(B \cap C) = \complement_A(B) \cup \complement_A(C)$$
> $$\complement_A(B \cup C) = \complement_A(B) \cap \complement_A(C)$$

> [!tip]- Flashcard: Proprietà Distributive Insiemistiche
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Cloze
Text: L'intersezione e l'unione godono di reciproca distributività:
1. $A \cap (B \cup C) =$ {{c1::$(A \cap B) \cup (A \cap C)$}}
2. $A \cup (B \cap C) =$ {{c2::$(A \cup B) \cap (A \cup C)$}}
Extra: A differenza dell'algebra numerica ordinaria (dove la somma non distribuisce sul prodotto), nell'algebra di Boole degli insiemi entrambe le operazioni distribuiscono l'una rispetto all'altra.
Tags: education/university education/math tech/logic
END
%%

### Dimostrazione Formale delle Leggi di De Morgan

Dimostriamo la prima legge per complementari: $\complement_A(B \cup C) = \complement_A(B) \cap \complement_A(C)$.
Sia $x \in A$ un elemento generico. Sviluppiamo la catena di equivalenze logiche applicando le definizioni e la corrispondente [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione#Leggi di De Morgan|legge di De Morgan proposizionale]]:

$$
\begin{aligned}
x \in \complement_A(B \cup C) &\iff x \in A \land x \notin (B \cup C) \\
&\iff x \in A \land \neg(x \in B \cup C) \\
&\iff x \in A \land \neg(x \in B \lor x \in C) \\
&\iff x \in A \land (\neg(x \in B) \land \neg(x \in C)) \quad \text{(De Morgan: } \neg(P \lor Q) \equiv \neg P \land \neg Q\text{)} \\
&\iff (x \in A \land x \notin B) \land (x \in A \land x \notin C) \quad \text{(idempotenza e associatività di } \land\text{)} \\
&\iff x \in \complement_A(B) \land x \in \complement_A(C) \\
&\iff x \in (\complement_A(B) \cap \complement_A(C))
\end{aligned}
$$

Poiché l'equivalenza vale per ogni $x$, per l'Assioma 1 di estensionalità i due insiemi coincidono. La seconda legge si dimostra specularmente impiegando l'altra dualità: $\neg(P \land Q) \equiv \neg P \lor \neg Q$.

> [!tip]- Flashcard: Leggi di De Morgan per Insiemi
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Cloze
Text: Siano $B, C \subset A$. Le leggi di De Morgan insiemistiche stabiliscono:
1. $\complement_A(B \cup C) =$ {{c1::$\complement_A(B) \cap \complement_A(C)$}}
2. $\complement_A(B \cap C) =$ {{c2::$\complement_A(B) \cup \complement_A(C)$}}
Extra: Il passaggio al complementare trasforma l'unione in intersezione e l'intersezione in unione, riflettendo esattamente la dualità logica tra congiunzione e disgiunzione.
Tags: education/university education/math tech/logic
END
%%

> [!tip]- Flashcard: Dimostrazione Formale della Legge di De Morgan per Complementari
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si dimostra formalmente che $\complement_A(B \cup C) = \complement_A(B) \cap \complement_A(C)$ per $B, C \subset A$?
Back: Mediante catena di equivalenze logiche per ogni $x \in A$:
$$x \in \complement_A(B \cup C) \iff x \in A \land \neg(x \in B \lor x \in C)$$
Applicando De Morgan proposizionale $\neg(P \lor Q) \equiv \neg P \land \neg Q$:
$$\iff x \in A \land (x \notin B \land x \notin C) \iff (x \in \complement_A(B)) \land (x \in \complement_A(C)) \iff x \in (\complement_A(B) \cap \complement_A(C))$$
Per l'assioma di estensionalità, i due insiemi coincidono.
Tags: education/university education/math tech/logic
END
%%

---

## 10. Insiemi per Elencazione ed Esempi Applicativi

Grazie alla combinazione dell'Assioma 3 (coppia non ordinata) e dell'Assioma 5 (unione), è possibile giustificare formalmente la notazione degli insiemi definiti per <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>elencazione</b></font></mark> \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=5|Dispensa p. 5]]].

> [!danger] Definizione 1.10: Insiemi per Elencazione
> Siano $a, b, c, d$ insiemi. Possiamo formare gli insiemi $\{a, b\}$ e $\{c\}$ e definire:
> $$\{a, b, c\} := \{a, b\} \cup \{c\}$$
> Successivamente definiamo:
> $$\{a, b, c, d\} := \{a, b, c\} \cup \{d\}$$
> Evidentemente vale:
> $$(\forall x) \, (x \in \{a, b, c, d\} \iff x = a \lor x = b \lor x = c \lor x = d)$$
> Iterando questo procedimento è possibile definire formalmente qualunque insieme finito mediante l'elencazione esplicita dei suoi elementi tra parentesi graffe.

> [!tip]- Flashcard: Definizione Formale di Insiemi per Elencazione
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si giustifica rigorosamente la notazione per elencazione $\{a, b, c\}$ mediante gli assiomi ZF?
Back: Si costruiscono prima la coppia $\{a, b\}$ e il singoletto $\{c\}$ (Assioma 3 della coppia) e si definisce:
$$\{a, b, c\} := \{a, b\} \cup \{c\}$$
mediante l'Assioma 5 dell'unione. Iterando il procedimento $(\{a_1, \dots, a_n\} \cup \{a_{n+1}\})$ si fonda rigorosamente qualsiasi insieme finito per elencazione.
Tags: education/university education/math tech/logic
END
%%

> [!example] Esempio 1.11: Calcolo di Operazioni su Insiemi Finiti
> Siano dati gli insiemi finiti:
> $$A = \{a, b, c, e, h\}, \quad B = \{c, d, e, f, g, h, i\}$$
> Calcolando le operazioni insiemistiche fondamentali:
> - **Intersezione (elementi comuni):**
>   $$A \cap B = \{c, e, h\}$$
> - **Differenza $A \setminus B$ (elementi di $A$ non in $B$):**
>   $$A \setminus B = \{a, b\}$$
> - **Differenza $B \setminus A$ (elementi di $B$ non in $A$):**
>   $$B \setminus A = \{d, f, g, i\}$$
> - **Unione (tutti gli elementi, senza duplicazioni):**
>   $$A \cup B = \{a, b, c, d, e, f, g, h, i\}$$

---

## 11. Assioma dell'Insieme Potenza (Insieme delle Parti)

L'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma dell'insieme potenza</b></font></mark> permette di collezionare la totalità dei possibili sottoinsiemi di un insieme dato in un nuovo ente matematico \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=6|Dispensa p. 6]]].

> [!danger] Assioma 6: Assioma dell'Insieme Potenza
> Sia $A$ un insieme. Esiste un insieme che ha per elementi tutti e soli i sottoinsiemi di $A$. Questo insieme si denota con $\mathcal{P}(A)$ (oppure con $2^A$) e si chiama **insieme potenza** di $A$ (o **insieme delle parti** di $A$):
> $$(\forall B) \, (B \in \mathcal{P}(A) \iff B \subset A)$$

> [!example] Esempio 1.12: Proprietà ed Esempi dell'Insieme Potenza
> - **Non vuotezza universale:** Sia $A$ un insieme. Poiché per l'Esempio 1.2 vale sempre $\emptyset \subset A$ e $A \subset A$, ne discende che:
>   $$\emptyset \in \mathcal{P}(A) \quad \text{e} \quad A \in \mathcal{P}(A)$$
>   Di conseguenza, l'insieme potenza **non è mai vuoto**, neppure per $A = \emptyset$.
> - **Coppia non ordinata:** Sia $A = \{x, y\}$. I suoi possibili sottoinsiemi sono:
>   $$\mathcal{P}(\{x, y\}) = \{\emptyset, \{x\}, \{y\}, \{x, y\}\}$$
> - **Iterazione a partire dall'Insieme Vuoto:**
>   1. Per $A = \emptyset$:
>      $$\mathcal{P}(\emptyset) = \{\emptyset\}$$
>      (possiede $1$ elemento: cardinalità $2^0 = 1$).
>   2. Applicando nuovamente l'insieme potenza:
>      $$\mathcal{P}(\mathcal{P}(\emptyset)) = \mathcal{P}(\{\emptyset\}) = \{\emptyset, \{\emptyset\}\}$$
>      (possiede $2$ elementi: cardinalità $2^1 = 2$).
>   3. Applicando una terza volta l'insieme potenza:
>      $$\mathcal{P}(\mathcal{P}(\mathcal{P}(\emptyset))) = \{\emptyset, \{\emptyset\}, \{\{\emptyset\}\}, \{\emptyset, \{\emptyset\}\}\}$$
>      (possiede $4$ elementi: cardinalità $2^2 = 4$).

![[Schema - Teoria degli Insiemi - Insieme Potenza e Scatole Annidate.png]]
*(L'insieme $\mathcal{P}(\mathcal{P}(\mathcal{P}(\emptyset)))$ illustrato secondo la metafora delle scatole: contiene quattro elementi distinti, ciascuno dei quali è a sua volta una scatola contenente ulteriori scatole al suo interno — rif. \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=6|Dispensa p. 6]]])*

> [!tip]- Flashcard: Assioma dell'Insieme Potenza e Cardinalità
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Che cos'è l'insieme potenza $\mathcal{P}(A)$, perché non è mai vuoto e qual è la sua cardinalità per un insieme finito di $n$ elementi?
> Back: È l'insieme di tutti i sottoinsiemi di $A$: $(\forall B) \, (B \in \mathcal{P}(A) \iff B \subset A)$. Non è mai vuoto poiché contiene sempre almeno $\emptyset$ e $A$ stesso ($\emptyset, A \in \mathcal{P}(A)$). Per un insieme finito con $|A| = n$, la cardinalità dell'insieme potenza è $|\mathcal{P}(A)| = 2^n$. Per $A = \emptyset$, $\mathcal{P}(\emptyset) = \{\emptyset\}$ contiene $2^0 = 1$ elemento.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 12. Complementi: Costruzione dei Numeri Naturali di Von Neumann

La costruzione assiomatica consente di edificare l'intero edificio dei numeri a partire dal puro insieme vuoto, secondo il procedimento formulato da John von Neumann \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=6|Dispensa p. 6]]]. A tale scopo è necessario escludere insiemi patologici che appartengono a se stessi mediante l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma di fondazione</b></font></mark>.

> [!danger] Assioma 7: Assioma di Fondazione (o di Regolarità)
> Per ogni insieme non vuoto $A$, esiste un suo elemento $x \in A$ tale che $x$ e $A$ sono disgiunti:
> $$(\forall A \ne \emptyset) \, (\exists x \in A) \, (x \cap A = \emptyset)$$

### Conseguenze dell'Assioma di Fondazione

1. **Divieto di Auto-Appartenenza ($x \notin x$):**
   Questo assioma assicura formalmente che $(\forall x) \, (x \notin x)$.
   *Dimostrazione per assurdo:* se per assurdo esistesse un insieme $x$ tale che $x \in x$, potremmo considerare il singoletto $A = \{x\}$ (che ha come unico elemento $x$). Avremmo $x \in x$ e $x \in A$, da cui seguirebbe $x \in (x \cap A)$, e dunque $x \cap A \ne \emptyset$. Poiché $x$ è l'unico elemento di $A$, nessun elemento di $A$ sarebbe disgiunto da $A$, contraddicendo frontalmente l'Assioma 7! Pertanto nessun insieme può appartenere a se stesso.
2. **Proprietà di Distinzione del Successivo:**
   L'assioma assicura inoltre che per ogni insieme $x$ vale:
   $$x \ne x \cup \{x\}$$
   Infatti $x \in (x \cup \{x\})$, ma per quanto appena dimostrato $x \notin x$. Essendo i due insiemi distinti, la nozione di successivo è rigorosamente ben posta.

> [!tip]- Flashcard: Assioma di Fondazione e Divieto di Auto-Appartenenza
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
START
Basic
Front: Come si formula l'assioma di fondazione (o regolarità) e come dimostra che nessun insieme può appartenere a se stesso ($x \notin x$)?
Back: Enunciato: ogni insieme non vuoto $A$ possiede un elemento disgiunto da $A$: $(\forall A \ne \emptyset)(\exists x \in A)(x \cap A = \emptyset)$.
Dimostrazione $x \notin x$: se per assurdo $x \in x$, nel singoletto $A = \{x\}$ l'unico elemento $x$ soddisfa $x \in (x \cap A)$, dunque $x \cap A \ne \emptyset$, contraddicendo l'assioma. Ne segue che $(\forall x)(x \notin x)$.
Tags: education/university education/math tech/logic
END
%%

> [!danger] Definizione 2.1: Successivo di un Insieme
> Sia $x$ un insieme. Si chiama **successivo di $x$** l'insieme:
> $$x^+ := x \cup \{x\}$$
> Il successivo di $x$ contiene dunque tutti gli elementi di $x$ più l'insieme $x$ stesso.
> In virtù dell'Assioma 7, vale $x \subset x^+$ e $x \ne x^+$, cosicché $x$ è un sottoinsieme proprio di $x^+$ ed ha esattamente un elemento in più di $x$ (l'elemento $x$ stesso).

### La Costruzione dei Numeri Naturali di Von Neumann

Definendo lo zero come l'insieme vuoto e applicando iterativamente l'operatore di successivo, si generano tutti i numeri naturali:

$$
\begin{aligned}
0 &:= \emptyset \\
1 &:= 0^+ = 0 \cup \{0\} = \emptyset \cup \{\emptyset\} = \{\emptyset\} = \{0\} \\
2 &:= 1^+ = 1 \cup \{1\} = \{0\} \cup \{1\} = \{0, 1\} = \{\emptyset, \{\emptyset\}\} \\
3 &:= 2^+ = 2 \cup \{2\} = \{0, 1, 2\} = \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}\} \\
4 &:= 3^+ = 3 \cup \{3\} = \{0, 1, 2, 3\} = \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}, \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}\}\}
\end{aligned}
$$

In generale, ogni numero naturale $n$ risulta essere l'insieme di tutti i numeri naturali che lo precedono:
$$n = \{0, 1, 2, \dots, n-1\}$$
In questa costruzione vale la suggestiva catena di appartenenze:
$$0 \in 1 \in 2 \in 3 \in 4 \in \dots$$

> [!tip]- Flashcard: Successivo di un Insieme e Numeri di Von Neumann
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Come si definisce il successivo di un insieme $x$ e in cosa consiste la costruzione dei numeri naturali di Von Neumann?
> Back: Il successivo è $x^+ := x \cup \{x\}$. Per l'assioma di fondazione $x \notin x$, quindi $x \subset x^+$ con $x \ne x^+$ ($x^+$ ha esattamente un elemento in più). Von Neumann definisce i naturali ponendo $0 := \emptyset$, $1 := 0^+ = \{0\} = \{\emptyset\}$, $2 := 1^+ = \{0, 1\}$, $3 := 2^+ = \{0, 1, 2\}$, cosicché ogni numero naturale $n$ coincide con l'insieme di tutti i numeri naturali che lo precedono.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 13. Assioma dell'Infinito e Teorema dell'Esistenza di $\mathbb{N}$

L'operazione di successivo permette di generare potenzialmente ciascun numero naturale, ma non garantisce che esista un insieme in grado di contenerli tutti contemporaneamente. Per sancire l'esistenza di un insieme infinito si introduce l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma dell'infinito</b></font></mark> \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=7|Dispensa p. 7]]].

> [!danger] Assioma 8: Assioma dell'Infinito
> Esiste un insieme che contiene l'insieme vuoto $\emptyset$ e il successivo di ogni suo elemento. In formule, esiste un insieme $W$ tale che:
> $$\emptyset \in W \quad \land \quad (\forall x) \, (x \in W \implies x^+ \in W)$$
> Un insieme che soddisfa tale proprietà prende il nome di **insieme induttivo**.

Se $\mathcal{F}$ è una famiglia non vuota di insiemi induttivi, la loro intersezione $\bigcap_{A \in \mathcal{F}} A$ è ancora un insieme induttivo. Da questo principio discende il teorema fondativo dell'esistenza dei numeri naturali:

> [!danger] Teorema 2.2: Esistenza e Caratterizzazione di $\mathbb{N}$
> Esiste il più piccolo insieme induttivo, e tale insieme si denota con $\mathbb{N}$ (l'insieme dei numeri naturali).
> 
> **Dimostrazione Formale:**
> Sia $W$ un insieme induttivo garantito dall'Assioma 8. Consideriamo la famiglia di tutti i sottoinsiemi di $W$ che sono induttivi:
> $$\mathcal{F} := \{A \in \mathcal{P}(W) \mid A \text{ è un insieme induttivo}\}$$
> La famiglia $\mathcal{F}$ è non vuota dato che $W \in \mathcal{F}$. Possiamo dunque applicare l'Assioma 4 di specificazione per definire l'intersezione di questa famiglia:
> $$\mathbb{N} := \bigcap_{A \in \mathcal{F}} A$$
> Poiché l'intersezione di una famiglia di insiemi induttivi è induttiva, $\mathbb{N}$ è un insieme induttivo.
> Se ora $E$ è un qualunque altro insieme induttivo, l'intersezione $E \cap W$ appartiene ad $\mathcal{F}$ (è un sottoinsieme induttivo di $W$), e pertanto:
> $$\mathbb{N} \subset (E \cap W) \subset E$$
> Dunque $\mathbb{N}$ è contenuto in ogni insieme induttivo: è il più piccolo insieme induttivo.
> Ricordando la costruzione di Von Neumann, si ha $0, 1, 2, 3, 4, \dots \in \mathbb{N}$, e si dimostra che $\mathbb{N}$ racchiude tutti e soli i numeri naturali.

> [!tip]- Flashcard: Assioma dell'Infinito e Teorema di $\mathbb{N}$
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Come si formula l'assioma dell'infinito e come si dimostra l'esistenza del più piccolo insieme induttivo $\mathbb{N}$?
> Back: L'assioma garantisce l'esistenza di un insieme induttivo $W$: $(\emptyset \in W) \land (\forall x)(x \in W \implies x^+ \in W)$. L'insieme $\mathbb{N}$ dei numeri naturali si definisce come l'intersezione di tutti i sottoinsiemi induttivi di $W$: $\mathbb{N} := \bigcap \{A \in \mathcal{P}(W) \mid A \text{ induttivo}\}$. Se $E$ è un qualunque altro insieme induttivo, $E \cap W$ è induttivo, per cui $\mathbb{N} \subset E \cap W \subset E$, provando che $\mathbb{N}$ è il minimo insieme induttivo.
> Tags: education/university education/math tech/logic
> END
> %%

---

## 14. Assioma della Scelta (Axiom of Choice)

La costruzione del sistema assiomatico ZFC si conclude con l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>assioma della scelta</b></font></mark>, che postula la possibilità di operare simultaneamente scelte arbitrarie su una collezione infinita di insiemi \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf#page=8|Dispensa p. 8]]].

> [!danger] Assioma 9: Assioma della Scelta (Axiom of Choice)
> Per ogni famiglia $\mathcal{F}$ di insiemi non vuoti e a due a due disgiunti, cioè tale che:
> $$(\forall A, B \in \mathcal{F}) \, (A \ne B \implies A \cap B = \emptyset)$$
> esiste un insieme $X \subset \bigcup_{A \in \mathcal{F}} A$ tale che, per ogni insieme $A \in \mathcal{F}$, l'intersezione $A \cap X$ è ridotta ad un solo elemento:
> $$(\forall A \in \mathcal{F}) \, (\exists! x) \, (x \in A \cap X)$$

Mediante l'insieme $X$, la teoria assicura la possibilità di "scegliere" esattamente un rappresentante per ciascun insieme della famiglia, anche qualora la famiglia sia infinita e non esista una formula esplicita o un algoritmo computazionale per operare tale selezione. L'assioma della scelta è invocato costantemente nei teoremi cardine dell'Analisi Matematica (come il Teorema di Hahn-Banach, l'esistenza di basi per spazi vettoriali a dimensione infinita e il Teorema di Tychonoff).

> [!tip]- Flashcard: Assioma della Scelta
> %%
> TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::02 - Teoria degli Insiemi
> START
> Basic
> Front: Qual è l'enunciato formale dell'assioma della scelta (Axiom of Choice)?
> Back: Data una famiglia $\mathcal{F}$ di insiemi non vuoti e a due a due disgiunti ($A \ne B \implies A \cap B = \emptyset$), esiste un insieme $X \subset \bigcup_{A \in \mathcal{F}} A$ tale che per ogni $A \in \mathcal{F}$, l'intersezione $A \cap X$ è costituita da un unico elemento. L'insieme $X$ seleziona esattamente un elemento per ogni insieme della famiglia.
> Tags: education/university education/math tech/logic
> END
> %%

---

## Quadro Sinottico degli Assiomi della Teoria ZF(C)

A conclusione del percorso, riassumiamo la gerarchia canonica dei 9 assiomi esaminati:

| N. | Assioma | Espressione Formale Canonica | Significato Operativo |
| :---: | :--- | :--- | :--- |
| **1** | **Estensionalità** | $A = B \iff (\forall x)(x \in A \iff x \in B)$ | Due insiemi coincidono se e solo se hanno gli stessi elementi |
| **2** | **Insieme Vuoto** | $(\forall x)(x \notin \emptyset)$ | Esiste l'insieme privo di elementi |
| **3** | **Coppia Non Ordinata** | $(\forall z)(z \in \{x, y\} \iff z = x \lor z = y)$ | Dati due enti $x, y$, esiste l'insieme $\{x, y\}$ e il singoletto $\{x\}$ |
| **4** | **Specificazione** | $(\forall a)(a \in \{x \in A \mid P(x)\} \iff a \in A \land P(a))$ | Una proprietà ritaglia un sottoinsieme da un universo $A$ |
| **5** | **Unione** | $(\forall x)(x \in \bigcup \mathcal{F} \iff (\exists A \in \mathcal{F})(x \in A))$ | Esiste l'unione degli elementi di una famiglia di insiemi |
| **6** | **Insieme Potenza** | $(\forall B)(B \in \mathcal{P}(A) \iff B \subset A)$ | Esiste l'insieme di tutti i sottoinsiemi di $A$ (cardinalità $2^n$) |
| **7** | **Fondazione (Regolarità)** | $(\forall A \ne \emptyset)(\exists x \in A)(x \cap A = \emptyset)$ | Esclude catene infinite discendenti e auto-appartenenza ($x \notin x$) |
| **8** | **Infinito** | $(\emptyset \in W) \land (\forall x)(x \in W \implies x^+ \in W)$ | Garantisce l'esistenza di insiemi induttivi infiniti |
| **9** | **Scelta (Choice)** | $(\forall A \in \mathcal{F})(\exists! x)(x \in A \cap X)$ | Seleziona un elemento da ciascun insieme di una famiglia disgiunta |

---

## Riferimenti Bibliografici Ufficiali

- **[1]** J.W.R. Dedekind, *Scritti sui fondamenti della matematica*, Bibliopolis, Napoli, 1982.
- **[2]** P. R. Halmos, *Teoria elementare degli insiemi*, Feltrinelli, Milano, 1970.
- **[3]** Prof. Saverio Salzo, *Lezione 2: Teoria degli Insiemi* (Dispense ufficiali d'insegnamento), DIAG, Sapienza Università di Roma, 2025/2026 \[[[Fondamenti di Matematica - Lezione 02 - Teoria degli Insiemi.pdf|Dispensa PDF]]].
