---
status: permanent
type: lecture
area: education
related: ["[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[03 - Funzioni (Parte I)]]", "[[02 - Teoria degli Insiemi]]", "[[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]", "[[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]", "[[01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python]]"]
aliases: ["Lezione 4 Fondamenti di Matematica", "FdM Lezione 4", "Funzioni (Parte 2)", "Iniettività, Suriettività, Composizione e Invertibilità"]
source: Lezione 4 FdM del 26/09/2026 - Prof. Saverio Salzo
title: "04 - Funzioni Parte II"
date: '2026-09-26'
updated: 2026-09-30T14:29
tags: [education/university, education/math, tech/logic]
summary: "Funzioni iniettive, suriettive e biettive, composizione associativa non commutativa, teorema di invertibilità con unicità dell'inversa e problemi inversi."
course: "Fondamenti di Matematica (Analisi 1)"
sources: ["[[Lezione 4 FdM.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Fondamenti di Matematica (Analisi 1) MOC]] / [[04 - Funzioni (Parte II)]]

# 04 - Funzioni (Parte II)

- **Docente:** Prof. Saverio Salzo / Canale A-L
- **Data Lezione:** 2026-09-26
- **Materiali Didattici Ufficiali:** \[[[Lezione 4 FdM.pdf#page=1|Dispensa Lezione 04 — Funzioni (parte II) (Prof. Salzo)]]]
- **Riferimento MOC:** [[Fondamenti di Matematica (Analisi 1) MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Lezione Precedente:** [[03 - Funzioni (Parte I)]]
- **Collegamento Interdisciplinare:** [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]] (in cui le proprietà di iniettività e biettività sono il fondamento per le trasformazioni di variabili aleatorie e le partizioni campionarie), [[01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python]] (in cui le funzioni pure, la composizione di pipeline e l'invertibilità algoritmica strutturano il paradigma di calcolo funzionale)

> [!quote]- Divagazione del Docente: Esercitazioni e Tutoraggio Online
> Prima di entrare nel vivo della lezione, il docente ricorda gli appuntamenti didattici a supporto del corso: le esercitazioni pomeridiane in presenza tenute dalla dott.ssa Elisa Trisalti (aula 105) e l'avvio del tutoraggio online con funzione di ricevimento su Moodle curato dal tutor Vincenzo Tortora. Tali attività costituiscono parte integrante del percorso formativo di Analisi 1.

La quarta lezione di Fondamenti di Matematica porta a compimento la teoria generale delle corrispondenze introdotta in [[03 - Funzioni (Parte I)]]. Dopo aver definito una funzione in termini insiemistici rigorosi come <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>terna ordinata</b></font></mark> $f = (A, B, R_f)$, l'obiettivo è ora esplorare la struttura operativa e qualitativa delle trasformazioni: stabilire l'esatto criterio di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>uguaglianza tra funzioni</b></font></mark>, classificare le mappe mediante le proprietà fondamentali di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>iniettività</b></font></mark>, <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>suriettività</b></font></mark> e <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>biettività</b></font></mark>, formalizzare l'operazione algebrica di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>composizione</b></font></mark> e dimostrare il fondamentale <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Teorema di Invertibilità</b></font></mark> con la caratterizzazione dell'inversa e le sue implicazioni ingegneristiche sui <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>problemi inversi</b></font></mark> \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]].

---

## 1. Uguaglianza tra Funzioni e Notazione Operativa

Nella primissima lezione ([[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione|01]]) e nella trattazione della [[02 - Teoria degli Insiemi|teoria ZF]], l'uguaglianza è stata introdotta mediante l'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>assioma di estensionalità</b></font></mark>: due insiemi sono uguali se e solo se possiedono esattamente gli stessi elementi.

Poiché nella [[03 - Funzioni (Parte I)|prima parte]] abbiamo definito rigorosamente una funzione come un oggetto puramente insiemistico — nello specifico una <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>terna ordinata</b></font></mark> $f = (A, B, R_f)$ in cui $A$ è il dominio, $B$ il codominio e $R_f \subseteq A \times B$ è un <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>grafo funzionale</b></font></mark> soddisfacente il test della retta verticale — ha perfettamente senso chiedersi a quali condizioni due funzioni $f$ e $\tilde{f}$ coincidano \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]].

### Criterio di Coincidenza Insiemistica

Siano $f = (A, B, R_f)$ e $\tilde{f} = (\tilde{A}, \tilde{B}, R_{\tilde{f}})$ due funzioni. In virtù della proprietà caratteristica delle terne ordinate (estensione di quella delle coppie ordinate di Kuratowski), due terne sono uguali se e solo se coincidono ordinatamente tutte e tre le loro componenti:
1. Stesso <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>dominio</b></font></mark>: $A = \tilde{A}$;
2. Stesso <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>codominio</b></font></mark>: $B = \tilde{B}$;
3. Stessa <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>relazione funzionale</b></font></mark>: $R_f = R_{\tilde{f}}$.

Ricordiamo che per definizione di funzione, per ogni elemento del dominio esiste uno ed un solo elemento del codominio in relazione con esso:
$$\forall x \in A, \;\exists!\, y \in B \;\land\; \exists!\, \tilde{y} \in B \quad\text{tali che}\quad (x, y) \in R_f \;\land\; (x, \tilde{y}) \in R_{\tilde{f}}$$
Denotando tali unici valori rispettivamente con $y = f(x)$ e $\tilde{y} = \tilde{f}(x)$, l'uguaglianza dei grafi $R_f = R_{\tilde{f}}$ impone che le coppie ordinate appartengano simultaneamente a entrambe le relazioni. Ciò si traduce nella <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>condizione puntuale operativa</b></font></mark>:
$$(\forall x \in A)\; [f(x) = \tilde{f}(x)]$$

> [!summary] Criterio di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Uguaglianza tra Funzioni</b></font></mark>
> Due funzioni $f: A \to B$ e $\tilde{f}: \tilde{A} \to \tilde{B}$ sono **uguali** ($f = \tilde{f}$) se e solo se:
> 1. Condividono lo stesso dominio: $A = \tilde{A}$
> 2. Condividono lo stesso codominio: $B = \tilde{B}$
> 3. Assumono lo stesso valore in ogni punto: $\forall x \in A, \; f(x) = \tilde{f}(x)$

> [!tip]- Flashcard: Criterio di Uguaglianza tra Funzioni
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Quali sono le tre condizioni necessarie e sufficienti affinché due funzioni $f$ e $\tilde{f}$ siano uguali ($f = \tilde{f}$)?
Back: Siano $f = (A, B, R_f)$ e $\tilde{f} = (\tilde{A}, \tilde{B}, R_{\tilde{f}})$. Le funzioni coincidono se e solo se:
1. Hanno lo stesso dominio: $A = \tilde{A}$
2. Hanno lo stesso codominio: $B = \tilde{B}$
3. Assumono lo stesso valore per ogni punto del dominio:
$$(\forall x \in A)\; [f(x) = \tilde{f}(x)]$$
Tags: education/university education/math tech/logic
<!--ID: 1790873652740-->
END
%%

### Distinzione tra Funzione e Formula Analitica

Il docente sottolinea un errore concettuale frequentissimo: confondere una funzione con la <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>formula analitica</b></font></mark> che la descrive. Una formula non è una funzione se non ne vengono esplicitati il dominio e il codominio. Inoltre, il fatto che due funzioni assumano lo stesso valore in uno o più punti non è assolutamente sufficiente a garantirne l'uguaglianza.

- **Controesempio del Docente:**
  Consideriamo le funzioni $f, g: \mathbb{R} \to \mathbb{R}$ definite rispettivamente da:
  $$f(x) = e^{x^2}, \qquad g(y) = e^{2y}$$
  Se valutiamo le funzioni nel punto $x = 2$ e $y = 2$, otteniamo:
  $$f(2) = e^{2^2} = e^4, \qquad g(2) = e^{2 \cdot 2} = e^4 \implies f(2) = g(2)$$
  Nonostante $f(2) = g(2)$, le due funzioni **non sono uguali** ($f \neq g$). Infatti, per $x = 1$ si ha $f(1) = e^1 = e$, mentre $g(1) = e^2 \neq e$. L'uguaglianza tra funzioni esige il <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>quantificatore universale</b></font></mark> $(\forall x \in A)$, non il quantificatore esistenziale $(\exists x \in A)$.

- **Notazione Standard Operativa:**
  D'ora in avanti, per non appesantire la trattazione con la scrittura formale a terne insiemistiche $f = (A, B, R_f)$, adotteremo universalmente la notazione standard di uso comune in matematica e ingegneria:
  $$f: A \to B$$
  intendendo implicitamente che $A$ è il dominio, $B$ il codominio e la freccia sottintende la legge funzionale univoca.

> [!tip]- Flashcard: Funzione vs Formula Analitica
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Perché il fatto che due funzioni $f, g: \mathbb{R} \to \mathbb{R}$ coincidano in un punto (es. $f(2) = g(2)$) non implica che $f = g$?
Back: Perché l'uguaglianza tra funzioni richiede la validità del quantificatore universale sull'intero dominio:
$$(\forall x \in A)\; [f(x) = g(x)]$$
La coincidenza in uno o più punti isolati attesta unicamente un'intersezione tra i grafici, non l'identità tra gli enti funzionali.
Tags: education/university education/math tech/logic
<!--ID: 1790873652741-->
END
%%

---

## 2. Funzioni Iniettive, Suriettive e Biettive

Le proprietà di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>iniettività</b></font></mark>, <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>suriettività</b></font></mark> e <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>biettività</b></font></mark> descrivono il comportamento globale di una mappa $f: A \to B$ e sono strettamente connesse alla risolubilità dell'equazione fondamentale \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]]:
$$f(x) = y, \qquad y \in B$$
In ambito ingegneristico e scientifico, tale equazione modella un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>problema inverso</b></font></mark>: $y \in B$ rappresenta il dato misurato o l'obiettivo da raggiungere, mentre $x \in A$ è la causa incognita da individuare.

### Funzione Iniettiva (Ingettiva)

La nozione intuitiva di iniettività esprime il <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>principio di conservazione della distinzione</b></font></mark>: una funzione è iniettiva se non invia mai elementi distinti del dominio nello stesso valore del codominio \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]].

> [!danger] Definizione 1.1a: Funzione Iniettiva
> Sia $f: A \to B$. La funzione $f$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>iniettiva</b></font></mark> (o ingettiva) se:
> $$(\forall x_1 \in A)(\forall x_2 \in A)\; [x_1 \neq x_2 \implies f(x_1) \neq f(x_2)]$$
> o, in <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>forma contronominale</b></font></mark> logicamente equivalente (usata nelle dimostrazioni algebriche):
> $$(\forall x_1 \in A)(\forall x_2 \in A)\; [f(x_1) = f(x_2) \implies x_1 = x_2]$$

In termini di equazioni e problemi inversi, l'iniettività equivale ad affermare che:
$$\forall y \in B, \quad \text{l’equazione } f(x) = y \text{ ammette al più una soluzione in } A$$
Geometricamente, nel piano cartesiano, ciò corrisponde al <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>test delle rette orizzontali</b></font></mark>: ogni retta orizzontale di equazione $y = c$ (con $c \in B$) interseca il grafico della funzione al massimo in un punto \[[[Lezione 4 FdM.pdf#page=2|Dispensa p. 2]]].

- **Esempi di non iniettività:**
  - La parabola $f: \mathbb{R} \to \mathbb{R}$ con $f(x) = x^2$: non è iniettiva perché $f(-2) = f(2) = 4$, pur essendo $-2 \neq 2$.
  - La funzione esponenziale quadratica $f(x) = e^{x^2}$: manda punti opposti nello stesso valore ($f(-x) = f(x)$).
  - Funzioni periodiche oscillanti: un segnale sinusoidale acquisito da un microfono $s(t) = \sin(\omega t)$ assume lo stesso valore infinite volte su $\mathbb{R}$, risultando marcatamente non iniettivo.

> [!tip]- Flashcard: Definizione di Funzione Iniettiva
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Sia $f: A \to B$. La funzione $f$ è iniettiva se e solo se {{c1::$(\forall x_1, x_2 \in A)\; [f(x_1) = f(x_2) \implies x_1 = x_2]$}}, il che equivale a dire che per ogni $y \in B$ l'equazione $f(x) = y$ ammette {{c2::al più una soluzione}}.
Extra: La formulazione contronominale diretta è $(\forall x_1, x_2 \in A)\; [x_1 \neq x_2 \implies f(x_1) \neq f(x_2)]$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652742-->
END
%%

### Funzione Suriettiva (Surgettiva)

La suriettività esprime la capacità della funzione di coprire interamente il codominio: ogni elemento dell'insieme di arrivo è raggiunto da almeno una freccia \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]].

> [!danger] Definizione 1.1b: Funzione Suriettiva
> Sia $f: A \to B$. La funzione $f$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>suriettiva</b></font></mark> (o surgettiva) se:
> $$(\forall y \in B)(\exists x \in A)\; [f(x) = y]$$
> o, in termini insiemistici equivalenti sull'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>immagine diretta</b></font></mark>:
> $$f(A) = B$$

In termini di problemi inversi, la suriettività è una pura <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>condizione di esistenza</b></font></mark>: per qualsiasi dato $y \in B$, l'equazione $f(x) = y$ è sempre risolvibile (ammette *almeno una* soluzione in $A$).

#### Il Ruolo Chiave della Scelta del Codominio

Come evidenziato dal docente a lezione, l'essere suriettiva non è una proprietà intrinseca della sola legge di assegnazione, ma dipende criticamente dalla <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>scelta del codominio</b></font></mark> $B$ \[[[Lezione 4 FdM.pdf#page=2|Dispensa p. 2]]]:
- Consideriamo la funzione esponenziale $x \mapsto e^x$:
  - Se considerata come $f: \mathbb{R} \to (0, +\infty)$, essa è **suriettiva**, poiché ogni numero reale strettamente positivo $y > 0$ si può esprimere come $e^x$, con $x = \ln y$.
  - Se invece la stessa espressione analitica viene considerata come $f: \mathbb{R} \to \mathbb{R}$, la funzione **non è suriettiva**: tutti i numeri negativi e lo zero ($y \le 0$) restano privi di controimmagine ("orfani di frecce").

- Esempio Discreto e <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Principio dei Cassetti</b></font></mark>:
  Se $A$ è un insieme finito di 2 elementi e $B$ un insieme di 3 elementi, non può esistere alcuna funzione suriettiva $f: A \to B$. Poiché da ciascuno dei 2 elementi di $A$ può partire una e una sola freccia (per definizione di funzione), al massimo 2 elementi di $B$ possono essere raggiunti, lasciando almeno un elemento di $B$ scoperto.

> [!tip]- Flashcard: Definizione di Funzione Suriettiva
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Sia $f: A \to B$. La funzione $f$ è suriettiva se e solo se {{c1::$(\forall y \in B)(\exists x \in A)\; [f(x) = y]$}}, il che equivale all'uguaglianza insiemistica {{c2::$f(A) = B$}}.
Extra: La suriettività garantisce che l'equazione $f(x) = y$ ammetta almeno una soluzione per ogni $y \in B$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652743-->
END
%%

### Esempi Comparativi di Comportamento Funzionale

Le proprietà di iniettività e suriettività sono reciprocamente indipendenti. La dispensa d'aula \[[[Lezione 4 FdM.pdf#page=2|Dispensa p. 2]], \[[[Lezione 4 FdM.pdf#page=3|Dispensa p. 3]]] illustra la casistica completa mediante esempi analitici notevoli:

| Funzione $f: A \to B$ | Dominio / Codominio | Iniettiva? | Suriettiva? | Risolubilità di $f(x) = y$ |
| :--- | :--- | :---: | :---: | :--- |
| $f(x) = x^2 + 1$ | $\mathbb{R} \to \mathbb{R}$ | **NO** | **NO** | Impossibile per $y < 1$; $1$ soluz. per $y=1$; $2$ soluz. per $y > 1$ ($x = \pm\sqrt{y-1}$). |
| $f(x) = \sqrt{x} + 1$ | $\mathbb{R}^+ \to \mathbb{R}$ | **SÌ** | **NO** | Impossibile per $y < 1$; $1$ unica soluz. per $y \ge 1$ ($x = (y-1)^2$). |
| $f(x) = x^3 - x$ | $\mathbb{R} \to \mathbb{R}$ | **NO** | **SÌ** | Sempre risolvibile; $1$ soluz. per $\vert y\vert > \frac{2}{3\sqrt{3}}$, $2$ soluz. per $\vert y\vert = \frac{2}{3\sqrt{3}}$, $3$ soluz. per $\vert y\vert < \frac{2}{3\sqrt{3}}$. |
| $f(x) = x^3 + 7$ | $\mathbb{R} \to \mathbb{R}$ | **SÌ** | **SÌ** | Sempre risolvibile con soluzione unica: $x = \sqrt[3]{y - 7}$. |

> [!example] Approfondimento Analitico: La Cubica $f(x) = x^3 - x$
> L'equazione $x^3 - x = y$ è un'equazione polinomiale di terzo grado.
> Studiando la derivata prima $f^\prime(x) = 3x^2 - 1$, si individuano i <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>punti stazionari</b></font></mark>:
> $$f^\prime(x) = 0 \iff x = \pm \frac{1}{\sqrt{3}}$$
> I valori corrispondenti di massimo e minimo locale sono:
> $$f\left(-\frac{1}{\sqrt{3}}\right) = \frac{2}{3\sqrt{3}}, \qquad f\left(\frac{1}{\sqrt{3}}\right) = -\frac{2}{3\sqrt{3}}$$
> - Per $\vert y\vert > \frac{2}{3\sqrt{3}}$, la retta orizzontale interseca il grafico in $1$ solo punto.
> - Per $y = \pm\frac{2}{3\sqrt{3}}$, la retta interseca il grafico in $2$ punti (uno di tangenza e uno di taglio).
> - Per $-\frac{2}{3\sqrt{3}} < y < \frac{2}{3\sqrt{3}}$, la retta interseca il grafico in $3$ punti distinti.
> 
> La funzione assume tutti i valori reali da $-\infty$ a $+\infty$ (è suriettiva), ma poiché a certe altezze esistono 3 controimmagini, non è iniettiva \[[[Lezione 4 FdM.pdf#page=3|Dispensa p. 3]]].

> [!tip]- Flashcard: Esempio di Funzione Suriettiva non Iniettiva
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Perché la funzione $f: \mathbb{R} \to \mathbb{R}$ definita da $f(x) = x^3 - x$ è suriettiva ma non iniettiva?
Back: 1. È **suriettiva** perché per ogni $y \in \mathbb{R}$ il polinomio di terzo grado $x^3 - x - y = 0$ ammette sempre almeno una radice reale.
2. **Non è iniettiva** perché possiede un massimo e un minimo locale; per i valori $y$ compresi nell'intervallo $\left(-\frac{2}{3\sqrt{3}}, \frac{2}{3\sqrt{3}}\right)$, le rette orizzontali intersecano il grafico in $3$ punti distinti (3 soluzioni distinte).
Tags: education/university education/math tech/logic
<!--ID: 1790873652744-->
END
%%

### Funzione Biettiva (Bigettiva o Corrispondenza Biunivoca)

Quando una funzione soddisfa contemporaneamente entrambe le condizioni, essa stabilisce un perfetto <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>accoppiamento uno-a-uno</b></font></mark> tra gli elementi del dominio e quelli del codominio \[[[Lezione 4 FdM.pdf#page=1|Dispensa p. 1]]].

> [!danger] Definizione 1.1c: Funzione Biettiva
> Sia $f: A \to B$. La funzione $f$ si dice <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>biettiva</b></font></mark> (o bigettiva, o corrispondenza biunivoca) se è sia iniettiva che suriettiva:
> $$(\forall y \in B)(\exists!\, x \in A)\; [f(x) = y]$$

La biettività assicura che per ogni dato $y \in B$ il problema inverso $f(x) = y$ sia <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>ben posto</b></font></mark> secondo Hadamard: la soluzione $x$ esiste sempre ed è rigorosamente unica.

> [!tip]- Flashcard: Definizione di Funzione Biettiva
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Una funzione $f: A \to B$ si dice biettiva se e solo se è contemporaneamente {{c1::iniettiva e suriettiva}}, ossia se {{c2::$(\forall y \in B)(\exists!\, x \in A)\; [f(x) = y]$}}.
Extra: La biettività garantisce esistenza e unicità della soluzione per l'equazione $f(x) = y$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652745-->
END
%%

### Proprietà Notevoli di Immagini e Controimmagini

In [[03 - Funzioni (Parte I)]] abbiamo dimostrato che per una funzione generica $f: A \to B$ valgono le inclusioni insiemistiche $X \subseteq f^{-1}(f(X))$ e $f(f^{-1}(Y)) \subseteq Y$.
Sotto le ipotesi di iniettività e suriettività, tali inclusioni collassano in esatte uguaglianze (Osservazione 1.4 \[[[Lezione 4 FdM.pdf#page=3|Dispensa p. 3]]]):

> [!summary] Proposizione: Uguaglianze di <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Immagini e Controimmagini</b></font></mark>
> Sia $f: A \to B$. Allora:
> 1. Se $f$ è **iniettiva**, per ogni sottoinsieme $X \subseteq A$ vale:
>    $$f^{-1}(f(X)) = X$$
> 2. Se $f$ è **suriettiva**, per ogni sottoinsieme $Y \subseteq B$ vale:
>    $$f(f^{-1}(Y)) = Y$$

> [!info] Dimostrazione Formale
> 1. Sappiamo già che $X \subseteq f^{-1}(f(X))$. Mostriamo l'inclusione inversa $f^{-1}(f(X)) \subseteq X$.
>    Sia $x \in f^{-1}(f(X))$. Per definizione di controimmagine, $f(x) \in f(X)$.
>    Per definizione di immagine diretta, ciò significa che esiste un elemento $\tilde{x} \in X$ tale che $f(x) = f(\tilde{x})$.
>    Poiché per ipotesi $f$ è iniettiva, $f(x) = f(\tilde{x}) \implies x = \tilde{x}$.
>    Dato che $\tilde{x} \in X$, ne consegue che $x \in X$. Dunque $f^{-1}(f(X)) = X$. $\blacksquare$
> 
> 2. Sappiamo già che $f(f^{-1}(Y)) \subseteq Y$. Mostriamo l'inclusione inversa $Y \subseteq f(f^{-1}(Y))$.
>    Sia $y \in Y$. Poiché per ipotesi $f$ è suriettiva, esiste almeno un $x \in A$ tale che $f(x) = y$.
>    Dato che $f(x) = y \in Y$, per definizione di controimmagine si ha $x \in f^{-1}(Y)$.
>    Applicando l'immagine diretta a tale elemento, $y = f(x) \in f(f^{-1}(Y))$.
>    Dunque $Y \subseteq f(f^{-1}(Y))$, da cui l'uguaglianza $f(f^{-1}(Y)) = Y$. $\blacksquare$

> [!tip]- Flashcard: Immagini e Controimmagini con Iniettività e Suriettività
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Sia $f: A \to B$.
1. Se $f$ è iniettiva e $X \subseteq A$, allora {{c1::$f^{-1}(f(X)) = X$}}.
2. Se $f$ è suriettiva e $Y \subseteq B$, allora {{c2::$f(f^{-1}(Y)) = Y$}}.
Extra: Per funzioni arbitrarie valgono solo le inclusioni $X \subseteq f^{-1}(f(X))$ e $f(f^{-1}(Y)) \subseteq Y$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652746-->
END
%%

---

## 3. Composizione di Funzioni

L'operazione fondamentale per combinare due trasformazioni in cascata è la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>composizione di funzioni</b></font></mark> \[[[Lezione 4 FdM.pdf#page=3|Dispensa p. 3]]].

### Definizione Formale e Diagramma di Venn

> [!danger] Definizione 1.5: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Funzione Composta</b></font></mark>
> Siano $f: A \to B$ e $g: B \to C$ due funzioni tali che il codominio di $f$ coincida con il dominio di $g$. Si definisce **funzione composta** di $f$ e $g$, indicata con $g \circ f: A \to C$ (letta "$g$ dopo $f$" o "$g$ composto $f$"):
> $$(\forall x \in A)\; [(g \circ f)(x) = g(f(x))]$$

Concettualmente, l'elemento $x \in A$ viene elaborato prima da $f$ producendo il valore intermedio $f(x) \in B$; tale valore viene quindi inserito ("plug-in") come argomento all'interno di $g$, restituendo il valore finale $g(f(x)) \in C$:
$$A \xrightarrow{\quad f \quad} B \xrightarrow{\quad g \quad} C$$

> [!info] Osservazione 1.9: Rilassamento del Dominio di Composizione
> La condizione stretta che il codominio di $f$ sia esattamente uguale al dominio di $g$ può essere rilassata \[[[Lezione 4 FdM.pdf#page=4|Dispensa p. 4]]]. Affinché $g(f(x))$ sia calcolabile per ogni $x \in A$, è sufficiente che l'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>immagine diretta</b></font></mark> di $f$ sia contenuta nel dominio di $g$:
> $$f(A) \subseteq \text{dom}(g)$$
> Ad esempio, se $f: \mathbb{R} \to \mathbb{R}$ con $f(x) = x^2 + 1$ e $g: [0, +\infty) \to \mathbb{R}$ con $g(t) = \sqrt{t}$, poiché $f(\mathbb{R}) = [1, +\infty) \subseteq [0, +\infty)$, la composizione $(g \circ f)(x) = \sqrt{x^2 + 1}$ è perfettamente ben definita su tutto $\mathbb{R}$.

> [!tip]- Flashcard: Definizione di Funzione Composta
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Dati $f: A \to B$ e $g: B \to C$, come viene definita la funzione composta $g \circ f$ e quale vincolo deve sussistere tra i loro insiemi?
Back: La funzione composta $g \circ f: A \to C$ è definita da:
$$(\forall x \in A)\; [(g \circ f)(x) = g(f(x))]$$
Affinché sia calcolabile, l'immagine di $f$ deve essere contenuta nel dominio di $g$ ($f(A) \subseteq \text{dom}(g)$).
Tags: education/university education/math tech/logic
<!--ID: 1790873652747-->
END
%%

### Proprietà Algebriche della Composizione

La composizione di funzioni definisce un'algebra su trasformazioni che condivide alcune proprietà dell'ordinaria moltiplicazione aritmetica, ma se ne discosta radicalmente per quanto riguarda la commutatività \[[[Lezione 4 FdM.pdf#page=4|Dispensa p. 4]]].

#### 1. Associatività

> [!summary] Proprietà: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Associatività della Composizione</b></font></mark>
> Siano $f: A \to B$, $g: B \to C$ e $h: C \to D$. Allora:
> $$h \circ (g \circ f) = (h \circ g) \circ f$$

*Dimostrazione:* Per ogni $x \in A$, per definizione di composizione applicata iterativamente:
$$(h \circ (g \circ f))(x) = h((g \circ f)(x)) = h(g(f(x)))$$
$(((h \circ g) \circ f)(x) = (h \circ g)(f(x)) = h(g(f(x)))$
Poiché le due funzioni hanno lo stesso dominio $A$, lo stesso codominio $D$ e assumono lo stesso valore in ogni $x$, esse coincidono. $\blacksquare$

#### 2. Elemento Neutro (Funzione Identità)

Ricordiamo che per ogni insieme $A$, la <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>funzione identità</b></font></mark> $i_A: A \to A$ è definita da $i_A(x) = x$ per ogni $x \in A$.
Data una funzione $f: A \to B$, la funzione identità funge da <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>elemento neutro</b></font></mark> a destra e a sinistra \[[[Lezione 4 FdM.pdf#page=4|Dispensa p. 4]]]:
$$f \circ i_A = f \qquad \land \qquad i_B \circ f = f$$
Infatti $(f \circ i_A)(x) = f(i_A(x)) = f(x)$ e $(i_B \circ f)(x) = i_B(f(x)) = f(x)$.

> [!quote]- Divagazione del Docente: La Notazione della Funzione Identità e Kenan Yıldız
> Il docente scherza sulla grafia della lettera $i$ utilizzata per la funzione identità ($i_A$ oppure $I_A$, con o senza puntino), collegandosi con ironia alle dispute sulla corretta pronuncia e trascrizione dei caratteri dell'alfabeto turco, come nel cognome del calciatore juventino Kenan Yıldız (in cui la "ı" senza puntino corrisponde a un fonema ben distinto dalla "i" con il puntino).

#### 3. Non Commutatività Generale

In generale, la composizione di funzioni <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>NON è commutativa</b></font></mark>:
$$g \circ f \neq f \circ g$$
Anche nei casi in cui entrambe le composizioni siano calcolabili (ossia quando $A = B = C$):
1. **Controesempio analitico:** Siano $f(x) = x^2$ e $g(x) = e^x$ su $\mathbb{R} \to \mathbb{R}$:
   $$(g \circ f)(x) = g(f(x)) = e^{x^2}$$
   $$(f \circ g)(x) = f(g(x)) = (e^x)^2 = e^{2x}$$
   Le due funzioni assumono lo stesso valore in $x = 2$ ($e^4$), ma per tutti gli altri $x \neq 2$ risultano distinte.
2. **Controesempio trigonometrico (Dispensa):** Siano $f(x) = \sin x$ e $g(x) = x^2$:
   $$(g \circ f)(x) = (\sin x)^2 = \sin^2 x, \qquad (f \circ g)(x) = \sin(x^2) \implies g \circ f \neq f \circ g$$

> [!example] Controesempio Geometrico: <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Isometrie del Quadrato</b></font></mark>
> Consideriamo un quadrato nel piano con i vertici numerati $\{1, 2, 3, 4\}$ disposti ordinatamente in senso antiorario:
> - $1$ a sud-est, $2$ a nord-est, $3$ a nord-ovest, $4$ a sud-ovest.
> 
> Definiamo due trasformazioni geometriche (isometrie del piano in sé):
> - $f$: <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>rotazione antioraria</b></font></mark> di $90^\circ$ attorno al centro del quadrato;
> - $g$: <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>riflessione a specchio</b></font></mark> rispetto all'asse di simmetria verticale.
> 
> Entrambe le mappe sono **biettive** (le isometrie conservano le distanze e non fanno collassare punti distinti \[[[Lezione 4 FdM.pdf#page=6|Dispensa p. 6]]]). Tuttavia:
> - **Applicando prima $f$ e poi $g$ ($g \circ f$):**
>   La rotazione $f$ porta i vertici nelle posizioni: $1 \to \text{nord-est}$, $2 \to \text{nord-ovest}$, $3 \to \text{sud-ovest}$, $4 \to \text{sud-est}$.
>   La successiva riflessione $g$ scambia la colonna destra con quella sinistra: la configurazione finale ha il vertice $1$ a nord-ovest e il vertice $2$ a nord-est.
> - **Applicando prima $g$ e poi $f$ ($f \circ g$):**
>   La riflessione $g$ scambia prima i vertici verticalmente: $1 \leftrightarrow 4$ e $2 \leftrightarrow 3$.
>   La successiva rotazione di $90^\circ$ produce una disposizione dei vertici completamente diversa dalla precedente.
> 
> Dunque $g \circ f \neq f \circ g$, dimostrando che persino nel gruppo delle trasformazioni biettive rigide la commutatività fallisce sistematicamente.

![[Schema - Composizione di Funzioni - Non Commutativita delle Isometrie.png]]

> [!tip]- Flashcard: Proprietà Algebriche della Composizione
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Quali proprietà algebriche possiede l'operazione di composizione di funzioni rispetto alla moltiplicazione numerica ordinaria?
Back: 1. **Associatività:** $h \circ (g \circ f) = (h \circ g) \circ f$ (sempre vera).
2. **Elemento neutro:** la funzione identità ($f \circ i_A = f$ e $i_B \circ f = f$).
3. **Non commutatività:** in generale $g \circ f \neq f \circ g$, anche quando le funzioni sono biettive e definite sullo stesso insieme.
Tags: education/university education/math tech/logic
<!--ID: 1790873652748-->
END
%%

---

## 4. Teorema di Invertibilità

Il culmine teorico della lezione è la caratterizzazione delle funzioni invertibili \[[[Lezione 4 FdM.pdf#page=4|Dispensa p. 4]]].

> [!danger] Teorema 1.10: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Teorema di Invertibilità</b></font></mark>
> $$f \text{ è biettiva} \iff \exists!\, g: B \to A \quad\text{tale che}\quad (g \circ f = i_A) \;\land\; (f \circ g = i_B)$$
> 
> - **Ipotesi:** $f: A \to B$ è una funzione assegnata tra gli insiemi $A$ e $B$.
> - **Condizioni di validità:** La corrispondenza $f$ deve essere simultaneamente iniettiva e suriettiva (biettiva) affinché l'inversa globale esista sull'intero codominio $B$.
> - **Significato dei simboli:**
>   - $f$: funzione diretta da $A$ in $B$
>   - $g = f^{-1}$: funzione inversa univoca da $B$ in $A$
>   - $i_A: A \to A$: funzione identità sul dominio $A$ ($i_A(x) = x$)
>   - $i_B: B \to B$: funzione identità sul codominio $B$ ($i_B(y) = y$)
>   - $\circ$: operatore binario di composizione funzionale
> - **Esempio operativo:** Sia $f: \mathbb{R} \to \mathbb{R}$ definita da $f(x) = x^3 + 7$. Risolvendo l'equazione $y = x^3 + 7 \iff x^3 = y - 7 \iff x = \sqrt[3]{y - 7}$, l'unica soluzione per ogni $y \in \mathbb{R}$ è $g(y) = \sqrt[3]{y - 7}$. Dunque la funzione inversa è $f^{-1}(y) = \sqrt[3]{y - 7}$.

Inoltre, la funzione $g$ che soddisfa tale condizione è <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>unica</b></font></mark>.
Tale funzione prende il nome di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>funzione inversa</b></font></mark> di $f$ e si denota con il simbolo:
$$f^{-1}: B \to A$$

Le <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>condizioni di cancellazione</b></font></mark> $g \circ f = i_A$ e $f \circ g = i_B$ si esplicitano punto per punto come:
$$\forall x \in A: \; g(f(x)) = x \qquad \land \qquad \forall y \in B: \; f(g(y)) = y$$

> [!tip]- Flashcard: Enunciato del Teorema di Invertibilità
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Sia $f: A \to B$. Il Teorema di Invertibilità stabilisce che $f$ è biettiva se e solo se esiste $g: B \to A$ tale che {{c1::$g \circ f = i_A$}} e {{c2::$f \circ g = i_B$}}. Inoltre, tale funzione $g$ è {{c3::unica}} ed è denotata con $f^{-1}$.
Extra: Punto per punto le condizioni equivalgono a $\forall x \in A, g(f(x)) = x$ e $\forall y \in B, f(g(y)) = y$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652749-->
END
%%

### Dimostrazione Completa del Teorema

La dimostrazione presentata dal docente si articola rigorosamente in tre fasi distinte \[[[Lezione 4 FdM.pdf#page=5|Dispensa p. 5]]]:
1. Implicazione diretta $(1) \implies (2)$
2. Implicazione inversa $(2) \implies (1)$
3. Unicità della funzione inversa $g$.
#### Dimostrazione $(1) \implies (2)$: Costruzione dell'Inversa

Assumiamo per ipotesi che $f: A \to B$ sia biettiva.
Per definizione di biettività, per ogni elemento $y \in B$ fissato arbitrariamente, l'equazione $f(x) = y$ ammette una ed una sola soluzione in $A$.
Definiamo allora una funzione $g: B \to A$ ponendo per ogni $y \in B$:
$$g(y) := \text{l’unica soluzione } x \in A \text{ di } f(x) = y$$
Dalla definizione stessa di $g$ discende immediatamente la catena di equivalenze:
$$(\forall x \in A)(\forall y \in B)\; [f(x) = y \iff x = g(y)]$$
Verifichiamo le due identità di composizione:
- **Verifica di $g \circ f = i_A$:**
  Dato un generico $x \in A$, poniamo $y = f(x)$. Poiché $x$ è per costruzione l'unica soluzione dell'equazione $f(?) = y$, applicando la funzione $g$ a tale $y$ otteniamo proprio $x$:
  $$g(f(x)) = g(y) = x = i_A(x)$$
  Dunque $g \circ f = i_A$.
- **Verifica di $f \circ g = i_B$:**
  Dato un generico $y \in B$, per definizione $g(y)$ è la soluzione dell'equazione $f(?) = y$. Sostituendo $g(y)$ all'interno di $f$:
  $$f(g(y)) = y = i_B(y)$$
  Dunque $f \circ g = i_B$. $\blacksquare$

> [!tip]- Flashcard: Dimostrazione (Biettiva implica Invertibile)
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Come si costruisce la funzione inversa $g: B \to A$ partendo dall'ipotesi che $f: A \to B$ sia biettiva?
Back: Essendo $f$ biettiva, per ogni $y \in B$ l'equazione $f(x) = y$ ammette un'unica soluzione $x \in A$.
Si definisce $g(y) := x$.
Ne segue direttamente che:
1. $g(f(x)) = x \implies g \circ f = i_A$
2. $f(g(y)) = y \implies f \circ g = i_B$
Tags: education/university education/math tech/logic
<!--ID: 1790873652750-->
END
%%

#### Dimostrazione $(2) \implies (1)$: Invertibile implica Biettiva

Assumiamo ora per ipotesi che esista una funzione $g: B \to A$ tale che $g \circ f = i_A$ e $f \circ g = i_B$. Dobbiamo dimostrare separatamente che $f$ è suriettiva e che $f$ è iniettiva:

1. **Suriettività di $f$:**
   Sia $y \in B$ un elemento arbitrario.
   Sfruttando la seconda ipotesi $f \circ g = i_B$, possiamo scrivere:
   $$y = i_B(y) = (f \circ g)(y) = f(g(y))$$
   Ponendo $x = g(y) \in A$, abbiamo trovato un elemento $x$ tale che $f(x) = y$.
   Poiché ciò vale per qualsiasi $y \in B$, ogni elemento del codominio possiede almeno una controimmagine, quindi $f$ è suriettiva.

2. **Iniettività di $f$:**
   Siano $x_1, x_2 \in A$ tali che $f(x_1) = f(x_2)$.
   Applichiamo la funzione $g$ a entrambi i membri dell'uguaglianza:
   $$g(f(x_1)) = g(f(x_2))$$
   Sfruttando la prima ipotesi $g \circ f = i_A$, si ha $g(f(x_1)) = x_1$ e $g(f(x_2)) = x_2$.
   Ne consegue immediatamente:
   $$x_1 = x_2$$
   Dunque $f$ è iniettiva.

Essendo $f$ contemporaneamente iniettiva e suriettiva, concludiamo che $f$ è biettiva. $\blacksquare$

> [!tip]- Flashcard: Dimostrazione (Invertibile implica Biettiva)
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Nella dimostrazione del Teorema di Invertibilità, come si prova che $f \circ g = i_B$ implica la suriettività e $g \circ f = i_A$ implica l'iniettività di $f$?
Back: 1. **Suriettività:** per ogni $y \in B$, $y = i_B(y) = f(g(y))$, quindi $x = g(y)$ è la soluzione dell'equazione $f(x) = y$.
2. **Iniettività:** se $f(x_1) = f(x_2)$, applicando $g$ si ha $g(f(x_1)) = g(f(x_2)) \implies x_1 = x_2$ poiché $g \circ f = i_A$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652751-->
END
%%

#### Dimostrazione dell'Unicità dell'Inversa

Supponiamo che esistano due funzioni $g, h: B \to A$ soddisfacenti entrambe le condizioni del teorema:
$$(g \circ f = i_A \;\land\; f \circ g = i_B) \qquad \text{e} \qquad (h \circ f = i_A \;\land\; f \circ h = i_B)$$
Valutiamo la funzione $h$:
$$h = h \circ i_B$$
Sostituendo l'identità $i_B = f \circ g$ (garantita dalle proprietà di $g$):
$$h = h \circ (f \circ g)$$
Applicando la proprietà associativa della composizione dimostrata nella sezione precedente:
$$h = (h \circ f) \circ g$$
Sostituendo ora la proprietà $h \circ f = i_A$ (garantita dalle proprietà di $h$):
$$h = i_A \circ g$$
Infine, poiché $i_A$ è l'elemento neutro a sinistra:
$$h = g$$
L'inversa, se esiste, è rigorosamente <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>unica</b></font></mark>. $\blacksquare$

> [!tip]- Flashcard: Unicità della Funzione Inversa
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Come si dimostra l'unicità della funzione inversa sfruttando l'associatività della composizione?
Back: Siano $g$ e $h$ due inverse di $f$. Allora:
$$h = h \circ i_B = h \circ (f \circ g) = (h \circ f) \circ g = i_A \circ g = g$$
Dunque $h = g$.
Tags: education/university education/math tech/logic
<!--ID: 1790873652752-->
END
%%

### Proprietà Geometriche e Strutturali dell'Inversa

1. <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Simmetria del Grafico</b></font></mark> rispetto alla bisettrice:
   Ricordando che il grafico di $f$ è $G_f = \{(x, y) \in A \times B \mid y = f(x)\}$, la relazione fondamentale dell'inversa $y = f(x) \iff x = f^{-1}(y)$ stabilisce che:
   $$(x, y) \in G_f \iff (y, x) \in G_{f^{-1}}$$
   Il grafico della funzione inversa $f^{-1}$ è esattamente il <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>simmetrico del grafico</b></font></mark> di $f$ rispetto alla bisettrice del primo e terzo quadrante ($y = x$) \[[[Lezione 4 FdM.pdf#page=5|Dispensa p. 5]]].

2. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Inversa della Composizione</b></font></mark>:
   Se due funzioni sono biettive, la loro composizione è biettiva e l'inversa <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>inverte l'ordine dei fattori</b></font></mark> \[[[Lezione 4 FdM.pdf#page=6|Dispensa p. 6]]]:

> [!danger] Teorema 1.15: <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Inversa della Composizione</b></font></mark>
> Siano $f: A \to B$ e $g: B \to C$ due funzioni biettive. Allora $g \circ f: A \to C$ è biettiva e la sua inversa è:
> $$(g \circ f)^{-1} = f^{-1} \circ g^{-1}$$

*Dimostrazione:*
Applichiamo l'associatività verificando che $(f^{-1} \circ g^{-1})$ sia l'inversa a destra e a sinistra di $(g \circ f)$:
$$(f^{-1} \circ g^{-1}) \circ (g \circ f) = f^{-1} \circ (g^{-1} \circ g) \circ f = f^{-1} \circ i_B \circ f = f^{-1} \circ f = i_A$$
$$(g \circ f) \circ (f^{-1} \circ g^{-1}) = g \circ (f \circ f^{-1}) \circ g^{-1} = g \circ i_B \circ g^{-1} = g \circ g^{-1} = i_C$$
Per l'unicità dell'inversa, $(g \circ f)^{-1} = f^{-1} \circ g^{-1}$. $\blacksquare$
*(Metafora intuitiva: l'azione di indossare prima le calze $f$ e poi le scarpe $g$ si inverte togliendo prima le scarpe $g^{-1}$ e poi le calze $f^{-1}$).*

> [!danger] Definizione 1.16: <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Invertibilità per Funzioni Iniettive</b></font></mark>
> Spesso in analisi una funzione $f: A \to B$ è iniettiva ma non suriettiva sul codominio $B$. Tuttavia, $f$ è banalmente biettiva se ristretta alla propria immagine $f(A) \subseteq B$.
> Si definisce allora la <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>funzione inversa ristretta</b></font></mark> \[[[Lezione 4 FdM.pdf#page=7|Dispensa p. 7]]]:
> $$f^{-1}: f(A) \to A, \qquad \forall y \in f(A): f^{-1}(y) = x \quad\text{con } f(x) = y$$
> soddisfacente $f^{-1} \circ f = i_A$ e $f \circ f^{-1} = i_{f(A)}$.

> [!tip]- Flashcard: Inversa della Composizione
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Cloze
Text: Siano $f: A \to B$ e $g: B \to C$ biettive. La funzione inversa della composizione $g \circ f$ è data da {{c1::$ (g \circ f)^{-1} = f^{-1} \circ g^{-1} $}}.
Extra: L'ordine dei fattori si inverte, analogamente a togliere prima le scarpe e poi le calze.
Tags: education/university education/math tech/logic
<!--ID: 1790873652753-->
END
%%

---

## 5. Applicazioni Ingegneristiche e Problemi Inversi

Il docente dedica una riflessione fondamentale ai <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>problemi inversi</b></font></mark> e al divario tra la purezza dell'astrazione matematica e la realtà del calcolo ingegneristico: **il fatto che una funzione inversa esista teoricamente non implica affatto che sia calcolabile in pratica** ("Questo teorema come ingegneri matematici lo dimostrate, ma nel mondo reale dei sistemi fisici e computazionali la situazione è drasticamente diversa").

### 1. Crittografia Asimmetrica e Algoritmo RSA

La sicurezza dei sistemi informatici moderni e della <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>crittografia asimmetrica</b></font></mark> si basa su funzioni matematiche cosiddette *one-way* (<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>funzioni unidirezionali a botola</b></font></mark> o *trapdoor*):
- Sia $f: \mathbb{P} \times \mathbb{P} \to \mathbb{N}$ la funzione che a una coppia di numeri primi molto grandi $(p, q)$ associa il loro prodotto:
  $$f(p, q) = p \cdot q = n$$
- Ristretta all'insieme dei semiprimi, la funzione $f$ è teoricamente biettiva (il <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Teorema Fondamentale dell'Aritmetica</b></font></mark> garantisce l'esistenza e l'unicità della scomposizione in fattori primi).
- Dunque l'inversa $f^{-1}: n \mapsto (p, q)$ **esiste teoricamente ed è unica**.
- Tuttavia, calcolare il prodotto in senso diretto $f(p, q)$ richiede frazioni di millisecondo mediante algoritmi polinomiali di moltiplicazione, mentre calcolare l'inversa $f^{-1}(n)$ (fattorizzazione di interi di migliaia di bit) richiede tempi esponenziali con gli algoritmi classici noti, risultando <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>computazionalmente intrattabile</b></font></mark>. L'asimmetria di complessità tra $f$ ed $f^{-1}$ fonda la robustezza della cifratura RSA.

### 2. Tomografia ad Impedenza Elettrica (EIT) e Geofisica

Nel mondo dell'ingegneria biomedica (con la <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>tomografia ad impedenza elettrica (EIT)</b></font></mark>) e della modellistica fisica differenziale:
- **Problema Diretto** (<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Equazioni di Maxwell</b></font></mark>): Data la conducibilità elettrica interna $\sigma$ dei tessuti cerebrali all'interno del cranio $\Omega$, le equazioni della fisica determinano in modo univoco il potenziale elettrico $u$ misurabile sul contorno $\Gamma$ (lo scalpo del paziente).
- **Problema Inverso (Diagnostica):** Il medico non può sezionare la testa del paziente vivo: posiziona elettrodi sullo scalpo, misura il potenziale $u$ sul bordo $\Gamma$ e desidera invertire la mappa per ricostruire la mappa di conducibilità interna $\sigma(x, y, z)$ e individuare emorragie o tumori.
- Analoghi problemi inversi governano la Magnetoencefalografia (MEG), la Risonanza Magnetica (RMN) e la geofisica (misura delle anomalie magnetiche ed elastiche da elicotteri o satelliti per localizzare faglie o prevedere sismi).
- In tutti questi problemi ingegneristici, l'operatore inverso spesso **non è continuo** o è <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>mal posto</b></font></mark> nel senso di Hadamard: piccolissime perturbazioni sul dato misurato $y$ producono divergenze catastrofiche sulla stima della causa $x$, richiedendo sofisticate tecniche di regolarizzazione numerica.

> [!tip]- Flashcard: Problemi Inversi e Crittografia
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Dal punto di vista ingegneristico e informatico, quale distinzione cruciale sussiste tra l'esistenza teorica dell'inversa e la sua applicabilità reale (es. algoritmo RSA)?
Back: Una funzione può essere biettiva ed esistere teoricamente un'inversa unica $f^{-1}$, ma il suo calcolo pratico può risultare **computazionalmente intrattabile** (es. fattorizzazione di grandi numeri primi in RSA) o **mal posto numericamente** (es. problemi inversi in tomografia e diagnostica biomedica).
Tags: education/university education/math tech/security
<!--ID: 1790873652754-->
END
%%

---

## 6. Attenzione alla Notazione e Ambiguità del Simbolo $f^{-1}$

In chiusura di lezione, il docente richiama l'attenzione su una pericolosa <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>sovrapposizione notazionale</b></font></mark> universale nella letteratura matematica: il simbolo $f^{-1}$ viene impiegato per denotare due concetti profondamente distinti \[[[Lezione 4 FdM.pdf#page=5|Dispensa p. 5]]]:

1. $f^{-1}$ come <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>funzione inversa</b></font></mark>:
   - È una funzione definita tra gli <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>elementi</b></font></mark> degli insiemi: $f^{-1}: B \to A$.
   - Ad ogni singolo elemento $y \in B$ associa l'unico elemento $x \in A$ tale che $f(x) = y$.
   - **Condizione di esistenza:** Esiste **esclusivamente** se la funzione $f$ è biettiva (o iniettiva se ristretta all'immagine).

2. $f^{-1}$ come <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>controimmagine</b></font></mark> (o preimmagine):
   - È un'operazione definita tra i <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>sottoinsiemi</b></font></mark> degli insiemi (tra gli <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>insiemi delle parti</b></font></mark>): $f^{-1}: \mathcal{P}(B) \to \mathcal{P}(A)$.
   - Ad ogni sottoinsieme $Y \subseteq B$ associa il sottoinsieme delle sue controimmagini:
     $$f^{-1}(Y) = \{x \in A \mid f(x) \in Y\}$$
   - **Condizione di esistenza:** È sempre definita per **qualsiasi funzione** $f$, a prescindere dal fatto che $f$ sia iniettiva, suriettiva o invertibile.

> [!warning] Regola di Distinzione
> Quando si incontra la scrittura $f^{-1}(\cdot)$, occorre osservare la natura dell'argomento:
> - Se l'argomento è un <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>sottoinsieme</b></font></mark> $Y \subseteq B$ (es. $f^{-1}([0, 1])$), si tratta della **controimmagine**.
> - Se l'argomento è un <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>singolo elemento</b></font></mark> $y \in B$ (es. $f^{-1}(5)$) e $f$ è invertibile, si tratta del valore della **funzione inversa**.

> [!tip]- Flashcard: Distinzione tra Funzione Inversa e Controimmagine
%%
TARGET DECK: University::Fondamenti di Matematica (Analisi 1)::04 - Funzioni (Parte II)
START
Basic
Front: Qual è la differenza fondamentale tra il simbolo $f^{-1}$ usato come funzione inversa e $f^{-1}$ usato come controimmagine?
Back: 1. **Funzione Inversa:** opera tra elementi ($f^{-1}: B \to A$) ed esiste **solo se** $f$ è biettiva.
2. **Controimmagine:** opera tra sottoinsiemi ($f^{-1}: \mathcal{P}(B) \to \mathcal{P}(A)$), definita da $f^{-1}(Y) = \{x \in A \mid f(x) \in Y\}$, ed esiste **sempre per qualsiasi funzione**, anche non iniettiva o non invertibile.
Tags: education/university education/math tech/logic
<!--ID: 1790873652755-->
END
%%
