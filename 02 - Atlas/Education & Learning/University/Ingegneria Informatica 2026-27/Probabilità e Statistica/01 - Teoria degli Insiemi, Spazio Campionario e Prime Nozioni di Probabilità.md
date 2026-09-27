---
status: permanent
type: lecture
area: education
related: ["[[Probabilità e Statistica MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]", "[[02 - Teoria degli Insiemi]]"]
aliases: ["Lezione 1 Probabilità e Statistica", "PeS Lezione 1", "01 - Statistica e probabilità"]
source: Lezione 1 Probabilità e Statistica del 24/09/2026 - Prof.ssa Giovanna Nappo, Prof. Fabio Spizzichino
title: "01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità"
date: '2026-09-24'
updated: 2026-09-27T18:00
tags: [education/university, education/math, math/probability, math/statistics]
summary: "Notazione insiemistica, operazioni di Eulero-Venn e dimostrazione, introduzione a fenomeni aleatori, spazio campionario, eventi e cardinalità."
course: "Probabilità e Statistica"
sources: ["[[Dispense Statistica e Probabilità.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Probabilità e Statistica MOC]] / [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]

# 01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità

- **Docenti:** Prof.ssa Giovanna Nappo, Prof. Fabio Spizzichino
- **Data Lezione:** 2026-09-24
- **Materiale Didattico Ufficiale:** \[[[Dispense Statistica e Probabilità.pdf#page=8|Capitolo 1 — Fenomeni aleatori e nozioni insiemistiche]]]
- **Riferimento MOC:** [[Probabilità e Statistica MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Collegamenti Interdisciplinari:** [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]] (linguaggio formale dei predicati e connettivi), [[02 - Teoria degli Insiemi]] (costruzione assiomatica ZF di insiemi, unione, intersezione e insieme potenza)

La prima lezione di Elementi di Calcolo delle Probabilità e Statistica introduce i fondamenti algebrici e concettuali indispensabili per descrivere formalmente l'incertezza e la casualità. La teoria della probabilità adotta la teoria degli insiemi come linguaggio matematico di base: i possibili esiti di una prova empirica costituiscono gli elementi di un insieme universo (lo spazio campionario $\Omega$), mentre le asserzioni o scommesse probabilistiche (gli eventi) sono modellizzate da suoi sottoinsiemi.

---

## Notazione Insiemistica Fondamentale

### Come si Indica un Insieme e Proprietà Costitutive

Nel formalismo matematico, un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>insieme</b></font></mark> è una collezione non ordinata di elementi distinti. Per consuetudine viene denotato con una lettera latina maiuscola ($A, B, C, \dots$) e definito elencando i suoi elementi racchiusi tra parentesi graffe:

$$A := \{1, 2, 3, 4\}$$

Il simbolo **due punti uguale** ($:=$) rappresenta l'operatore di <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>definizione</b></font></mark>: si usa la prima volta che si introduce un oggetto matematico per attribuirgli formalmente un nome (ciò che sta a destra definisce ciò che sta a sinistra). Una volta battezzato l'oggetto, nelle occorrenze successive si usa la consueta uguaglianza ($=$).

> [!danger] Definizione: Insieme e Regole Auree Costitutive
> Un **insieme** è una collezione ben definita di oggetti distinti (detti elementi). Valgono due regole strutturali assolute:
> 1. **L'ordine non conta:** A differenza delle sequenze ordinate e delle coordinate cartesiane, la disposizione spaziale degli elementi non ha alcuna rilevanza:
>    $$\{4, 3, 1, 2\} = \{3, 4, 1, 2\} = \{1, 2, 3, 4\}$$
> 2. **Nessun doppione:** Ogni elemento appartiene all'insieme una sola volta. Ripetere la stessa etichetta non crea copie distinte dell'oggetto (es. $\{3, 3, 4\} = \{3, 4\}$).

> [!tip]- Flashcard: Definizione di Insieme
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Basic
> Front: Cos'è un insieme nella formulazione matematica e quali sono le sue due proprietà fondamentali rispetto agli elementi?
> Back: Un insieme è una collezione ben definita di oggetti distinti (detti elementi). Le sue due proprietà cardine sono: (1) l'ordine degli elementi non ha alcuna rilevanza (es. $\{1, 2\} = \{2, 1\}$); (2) non sono ammesse ripetizioni o doppioni (ogni elemento compare una sola volta, es. $\{1, 1, 2\} = \{1, 2\}$).
> Tags: University::Probabilita_e_Statistica::Insiemi::Definizione
> END
> %%

### Relazioni di Appartenenza e Non Appartenenza

La relazione tra un singolo elemento e un insieme si esprime mediante due simboli canonici (coerenti con i predicati atomici esaminati in [[02 - Teoria degli Insiemi]]):
- **Appartiene ($\in$):** $1 \in A$ afferma che l'elemento $1$ fa parte dell'insieme $A$.
- **Non appartiene ($\notin$):** $5 \notin A$ nega l'appartenenza di $5$ ad $A$. La sbarra diagonale sovrapposta indica esplicitamente la negazione logica della proposizione originaria.

### Insiemi Infiniti e Notazione Intensiva (per Proprietà)

Gli insiemi possono essere finiti o infiniti:
- Un insieme è **finito** quando i suoi elementi possono essere enumerati per intero.
- Un insieme è **infinito** quando il conteggio non ha termine (es. l'insieme dei numeri naturali $\mathbb{N} := \{1, 2, 3, \dots\}$).
- Spesso scrivere l'elenco esplicito è impraticabile; si ricorre alla **descrizione intensiva** che specifica la proprietà logica caratteristica (formalizzata tramite l'assioma di specificazione in [[02 - Teoria degli Insiemi]]):
  $$A := \{x \in \Omega \mid P(x)\}$$
  Ad esempio, per i numeri pari: $2\mathbb{N} := \{n \in \mathbb{N} \mid (\exists k \in \mathbb{N}) \, (n = 2k)\}$.

> [!tip]- Flashcard: Notazione Intensiva ed Estensiva
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Basic
> Front: Qual è la differenza sostanziale tra la rappresentazione estensiva e quella intensiva di un insieme?
> Back: La rappresentazione estensiva elenca esplicitamente tutti gli elementi tra parentesi graffe (es. $A = \{2, 4, 6, 8\}$). La rappresentazione intensiva (o per caratteristica) specifica la proprietà logica necessaria e sufficiente che gli elementi devono soddisfare per appartenere all'insieme: $A = \{x \in \Omega \mid P(x)\}$.
> Tags: University::Probabilita_e_Statistica::Insiemi::Rappresentazione
> END
> %%

---

## Operazioni tra Insiemi

Le operazioni insiemistiche associano o modificano collezioni di elementi all'interno di uno spazio ambiente $\Omega$ \[[[Dispense Statistica e Probabilità.pdf#page=9|Dispense p. 9]]].

> [!danger] Definizione: Operazioni Insiemistiche Fondamentali
> Siano $A$ e $B$ sottoinsiemi di uno spazio ambiente $\Omega$ ($A, B \subseteq \Omega$):
> 1. **Unione ($A \cup B$):** raccoglie gli elementi che appartengono ad $A$, oppure a $B$, o a entrambi (disgiunzione inclusiva $\lor$):
>    $$A \cup B := \{x \in \Omega \mid x \in A \lor x \in B\}$$
> 2. **Intersezione ($A \cap B$):** raccoglie esclusivamente gli elementi comuni condivisi simultaneamente sia da $A$ sia da $B$ (congiunzione logica $\land$):
>    $$A \cap B := \{x \in \Omega \mid x \in A \land x \in B\}$$
> 3. **Complementare ($A^\complement$ o $\complement_\Omega(A)$):** raccoglie tutti gli elementi dello spazio ambiente $\Omega$ che non appartengono ad $A$:
>    $$A^\complement := \{x \in \Omega \mid x \notin A\}$$
> 4. **Differenza Insiemistica ($A \setminus B$ o $A - B$):** individua gli elementi che stanno in $A$ e non appartengono a $B$:
>    $$A \setminus B := \{x \in \Omega \mid x \in A \land x \notin B\}$$

> [!tip]- Flashcard: Operazioni Insiemistiche Fondamentali
%%
TARGET DECK: University::Probabilità e Statistica
START
Cloze
Text: Dati $A, B \subseteq \Omega$, si definiscono:
- Unione: $A \cup B :=$ {{c1::$\{x \in \Omega \mid x \in A \lor x \in B\}$}}
- Intersezione: $A \cap B :=$ {{c2::$\{x \in \Omega \mid x \in A \land x \in B\}$}}
- Complementare: $A^\complement :=$ {{c3::$\{x \in \Omega \mid x \notin A\}$}}
- Differenza: $A \setminus B :=$ {{c4::$\{x \in \Omega \mid x \in A \land x \notin B\}$}}
Extra: Nel calcolo delle probabilità, l'unione corrisponde al verificarsi di almeno uno tra gli eventi, mentre l'intersezione al verificarsi congiunto di entrambi.
Tags: education/university education/math math/probability
END
%%

![[Schema - Diagramma di Eulero-Venn - Unione.png]]
*(Rappresentazione grafica dell'unione $A \cup B$)*

![[Schema - Diagramma di Eulero-Venn - Intersezione.png]]
*(Rappresentazione grafica dell'intersezione $A \cap B$)*

![[Schema - Diagramma di Eulero-Venn - Complementare.png]]
*(Rappresentazione grafica del complementare $A^\complement$ rispetto allo spazio ambiente $\Omega$)*

![[Schema - Diagramma di Eulero-Venn - Differenza.png]]
*(Rappresentazione grafica della differenza insiemistica $A \setminus B$)*

> [!danger] Teorema: Identità della Differenza Insiemistica
> Dati due insiemi $A, B \subseteq \Omega$, vale l'identità fondamentale:
> $$A \setminus B = A \cap B^\complement$$
> 
> **Dimostrazione Formale:**
> La verifica si conduce sviluppando la catena di equivalenze logiche per ogni elemento $x \in \Omega$:
> $$
> \begin{aligned}
> x \in (A \setminus B) &\iff x \in A \land x \notin B && \text{(definizione di differenza)} \\
> &\iff x \in A \land x \in B^\complement && \text{(poiché } x \notin B \iff x \in B^\complement\text{)} \\
> &\iff x \in (A \cap B^\complement) && \text{(definizione di intersezione)}
> \end{aligned}
> $$
> Poiché l'equivalenza vale universalmente $(\forall x \in \Omega)$, per l'assioma di estensionalità si ha $A \setminus B = A \cap B^\complement$. $\blacksquare$

> [!tip]- Flashcard: Dimostrazione Differenza Insiemistica
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Basic
> Front: Come si dimostra l'uguaglianza insiemistica $A \setminus B = A \cap B^\complement$?
> Back: Si dimostra mediante catena di equivalenze logiche elemento per elemento ($\forall x \in \Omega$):
> 1. $x \in A \setminus B \iff x \in A \land x \notin B$ (definizione di differenza).
> 2. Poiché $x \notin B \iff x \in B^\complement$ (definizione di complementare), l'espressione equivale a $x \in A \land x \in B^\complement$.
> 3. Per definizione di intersezione, $x \in A \land x \in B^\complement \iff x \in (A \cap B^\complement)$.
> Essendo le condizioni equivalenti per ogni $x$, si conclude che $A \setminus B = A \cap B^\complement$.
> Tags: University::Probabilita_e_Statistica::Insiemi::Dimostrazioni
> END
> %%

---

## Prime Nozioni di Probabilità

### 1. Fenomeno ed Esperimento Aleatorio

> [!danger] Definizione: Fenomeno ed Esperimento Aleatorio
> - Un **fenomeno aleatorio** è un processo reale caratterizzato da intrinseca incertezza, il cui esito specifico non è predicibile a priori con assoluta certezza deterministica (es. il lancio di una moneta o la durata di funzionamento di un calcolatore).
> - Un **esperimento aleatorio** è la singola realizzazione o prova empirica controllata di un fenomeno aleatorio (es. compiere materialmente un lancio e registrare se sia uscito Testa o Croce).

> [!tip]- Flashcard: Fenomeno vs Esperimento Aleatorio
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Basic
> Front: Qual è la distinzione concettuale tra fenomeno aleatorio ed esperimento aleatorio nel calcolo delle probabilità?
> Back: Il **fenomeno aleatorio** è la situazione empirica generale caratterizzata da incertezza sul risultato. L'**esperimento aleatorio** è la singola realizzazione o osservazione controllata del fenomeno volta a rilevarne l'esito specifico.
> Tags: University::Probabilita_e_Statistica::Probabilita::Fondamenti
> END
> %%

### 2. Spazio Campionario ($\Omega$) ed Eventi Elementari

> [!danger] Definizione: Spazio Campionario ed Evento Elementare
> Lo **spazio campionario** $\Omega$ è l'insieme di tutti i possibili esiti atomici e mutuamente esclusivi di un esperimento aleatorio.
> Ciascun singolo elemento $\omega \in \Omega$ prende il nome di **evento elementare**.

> [!tip]- Flashcard: Spazio Campionario ed Eventi Elementari
%%
TARGET DECK: University::Probabilità e Statistica
START
Basic
Front: Come sono definiti lo spazio campionario $\Omega$ e un evento elementare nella modellazione di un esperimento aleatorio?
Back: Lo **spazio campionario** $\Omega$ è l'insieme di tutti i possibili esiti atomici e mutuamente esclusivi dell'esperimento. Ciascun singolo esito atomico $\omega \in \Omega$ costituisce un **evento elementare**.
Tags: education/university education/math math/probability
END
%%

> [!example] Esempi Notabili di Spazio Campionario
> 1. **Lancio della Moneta:** $\Omega := \{T, C\}$
> 2. **Lancio del Dado a 6 Facce:** $\Omega := \{1, 2, 3, 4, 5, 6\}$
> 3. **Tempo di Vita di un Chip o Componente Elettronico:**
>    $$\Omega := \{t \in \mathbb{R} \mid t \ge 0\} = \mathbb{R}^+$$
> 4. **Due Lanci di Moneta (Prove Ripetute):**
>    $$\Omega := \{(T, T), (T, C), (C, T), (C, C)\}$$
>    Si utilizzano coppie ordinate tra parentesi tonde perché l'ordine temporale dei lanci è determinante: $(T, C) \ne (C, T)$.

### 3. Definizione Formale di Evento

> [!danger] Definizione: Evento Aleatorio
> Un **evento aleatorio** $E$ è un qualunque **sottoinsieme** dello spazio campionario $\Omega$:
> $$E \subseteq \Omega \iff E \in \mathcal{P}(\Omega)$$
> - **Evento Certo ($\Omega$):** l'intero spazio campionario; si verifica sempre.
> - **Evento Impossibile ($\emptyset$):** l'insieme vuoto privo di esiti; non si verifica mai.
> - **Eventi Incompatibili (Mutuamente Esclusivi):** due eventi $A$ e $B$ tali che:
>   $$A \cap B = \emptyset$$
>   I due eventi non possono verificarsi simultaneamente.
> - **Eventi Esaustivi:** due o più eventi la cui unione coincide con l'intero spazio campionario ($A \cup B = \Omega$).

> [!tip]- Flashcard: Tipologie di Eventi (Certo, Impossibile, Esaustivi)
%%
TARGET DECK: University::Probabilità e Statistica
START
Cloze
Text: All'interno di uno spazio campionario $\Omega$:
- L'{{c1::evento certo}} coincide con $\Omega$ e si verifica sempre.
- L'{{c2::evento impossibile}} coincide con $\emptyset$ e non si verifica mai.
- Due o più eventi si dicono {{c3::esaustivi}} se la loro unione copre l'intero spazio campionario: $A \cup B = \Omega$.
Extra: Due eventi $A$ e $B$ sono incompatibili (o disgiunti) se $A \cap B = \emptyset$.
Tags: education/university education/math math/probability
END
%%

![[Schema - Diagramma di Eulero-Venn - Spazio Campionario ed Eventi.png]]
*(Rappresentazione di eventi come sottoinsiemi dello spazio campionario $\Omega$)*

> [!tip]- Flashcard: Definizione di Evento e Incompatibilità
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Basic
> Front: Nel contesto di uno spazio campionario $\Omega$, come si definiscono formalmente un evento e la condizione di incompatibilità tra due eventi?
> Back: Un **evento** $E$ è un qualunque sottoinsieme dello spazio campionario, ossia $E \subseteq \Omega$ ($E \in \mathcal{P}(\Omega)$). Due eventi $A$ e $B$ si dicono **incompatibili** (o mutuamente esclusivi) se e solo se la loro intersezione coincide con l'insieme vuoto: $A \cap B = \emptyset$, il che implica che non possono verificarsi contemporaneamente.
> Tags: University::Probabilita_e_Statistica::Probabilita::Eventi
> END
> %%

---

## Cardinalità e Insieme delle Parti

### Definizione di Cardinalità

La <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>cardinalità</b></font></mark> di un insieme $A$ (denotata con $\#A$ o $|A|$) indica il numero di elementi distinti contenuti nell'insieme:
- $\#\emptyset = 0$
- Per un dado: $\#\Omega = 6$
- Per due lanci di moneta: $\#\Omega = 4$

> [!danger] Teorema: Numero Complessivo di Eventi ($2^n$)
> Sia $\Omega$ uno spazio campionario finito con cardinalità $\#\Omega = n$. Il numero complessivo di tutti i possibili eventi (sottoinsiemi) definibili su $\Omega$ coincide con la cardinalità dell'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>insieme delle parti</b></font></mark> $\mathcal{P}(\Omega)$ (introdotto nell'Assioma 6 in [[02 - Teoria degli Insiemi]]) ed è pari a:
> $$\#\mathcal{P}(\Omega) = 2^n$$
> 
> **Verifica per l'esperimento dei due lanci ($\#\Omega = 4$):**
> 1. Eventi con $0$ elementi (insieme vuoto $\emptyset$): $\binom{4}{0} = 1$
> 2. Eventi con $1$ elemento (singoletti atomici): $\binom{4}{1} = 4$
> 3. Eventi con $2$ elementi (coppie di esiti): $\binom{4}{2} = 6$
> 4. Eventi con $3$ elementi: $\binom{4}{3} = 4$
> 5. Eventi con $4$ elementi (l'evento certo $\Omega$): $\binom{4}{4} = 1$
> $$\text{Totale Eventi} = 1 + 4 + 6 + 4 + 1 = 16 = 2^4$$

> [!tip]- Flashcard: Cardinalità dell'Insieme delle Parti
> %%
> TARGET DECK: University::Probabilità e Statistica
> START
> Cloze
> Text: Dato uno spazio campionario finito $\Omega$ composto da $n$ eventi elementari ($\#\Omega = n$), il numero complessivo di eventi distinti (sottoinsiemi) definibili è pari a {{c1::$2^n$}}, corrispondente alla cardinalità dell'insieme delle parti {{c2::$\mathcal{P}(\Omega)$}}.
> Extra: Nel caso del lancio di due monete dove $\#\Omega = 4$, il numero totale di possibili eventi su cui scommettere è $2^4 = 16$.
> Tags: University::Probabilita_e_Statistica::Probabilita::Cardinalita
> END
> %%
