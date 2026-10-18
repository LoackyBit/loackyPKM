---
status: permanent
type: lecture
area: education
related: ["[[Probabilità e Statistica MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]", "[[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]", "[[02 - Teoria degli Insiemi]]", "[[03 - Funzioni (Parte I)]]"]
aliases: ["Lezione 2 Probabilità e Statistica", "PeS Lezione 2", "02 - Statistica e probabilità", "Insieme delle Parti e Assiomi di Kolmogorov", "Spazi Finiti di Probabilità"]
source: Lezione 2 Probabilità e Statistica del 25/09/2026 - Prof.ssa Giovanna Nappo, Prof. Fabio Spizzichino
title: "02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti"
date: '2026-09-25'
updated: 2026-10-01T18:41
tags: [education/university, education/math, math/probability, math/statistics]
summary: "Insieme delle parti e funzioni indicatrici, cardinalità 2^n e binomio di Newton, assiomi di Kolmogorov, proprietà e spazi finiti di probabilità."
course: "Probabilità e Statistica"
sources: ["[[Dispense Statistica e Probabilità.pdf]]", "[[Appunti Manoscritti - Lezione 02 Probabilità e Statistica.jpeg]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Probabilità e Statistica MOC]] / [[02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti]]

# 02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti

- **Docenti:** Prof.ssa Giovanna Nappo, Prof. Fabio Spizzichino
- **Data Lezione:** 2026-09-25
- **Materiale Didattico Ufficiale:** \[[[Dispense Statistica e Probabilità.pdf#page=17|Capitolo 2 — Spazi finiti di probabilità (pp. 17–24)]]]
- **Riferimento MOC:** [[Probabilità e Statistica MOC]], [[Ingegneria Informatica 2026 - 27 MOC]]
- **Lezione Precedente:** [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità]]
- **Collegamenti Interdisciplinari:** [[02 - Teoria degli Insiemi]] (assioma dell'insieme potenza ZF), [[03 - Funzioni (Parte I)]] (spazio funzionale $Y^X$, notazione esponenziale $2^A$ e funzioni binarie indicatrici)

La seconda lezione di Elementi di Calcolo delle Probabilità e Statistica approfondisce la struttura algebrica che consente di quantificare l'incertezza. Se nella [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità|prima lezione]] lo spazio campionario $\Omega$ e gli eventi sono stati introdotti a livello intuitivo, in questa lezione viene formalizzato l'oggetto matematico che raccoglie la totalità delle possibili asserzioni aleatorie: l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>insieme delle parti</b></font></mark> $2^\Omega$.

Attraverso la corrispondenza con le <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>funzioni indicatrici</b></font></mark> e il teorema del binomio di Newton, si dimostra che la cardinalità degli eventi cresce esponenzialmente con il numero di esiti elementari. Successivamente, la trattazione supera i limiti della probabilità classica introducendo l'approccio assiomatico di Kolmogorov: la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>misura di probabilità</b></font></mark> $\mathbb{P}$ viene definita come una funzione a valori reali regolata da tre assiomi fondanti, dai quali si deducono rigorosamente la probabilità dell'evento impossibile, l'additività finita e la probabilità del complementare. La lezione si conclude mostrando come, negli <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>spazi di probabilità finiti</b></font></mark> (o numerabili), la conoscenza della misura si riduca interamente all'assegnazione dei pesi sui singoli eventi elementari.

---

## 1. Insieme delle Parti e Funzione Indicatrice

### Definizione Insiemistica dell'Insieme delle Parti

Dato un insieme ambiente qualunque $A$, l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>insieme delle parti</b></font></mark> (noto anche come *insieme potenza* o *power set*, introdotto assiomaticamente in [[02 - Teoria degli Insiemi]]) è la famiglia costituita da tutti e soli i sottoinsiemi di $A$:

$$2^A \equiv \mathcal{P}(A) := \{B \mid B \subseteq A\}$$

> [!danger] Definizione: Insieme delle Parti
> Dato un insieme $A$, l'**insieme delle parti** di $A$ è la collezione di tutti i possibili sottoinsiemi di $A$:
> $$2^A := \{B \mid B \subseteq A\}$$
> 
> Tra i sottoinsiemi appartengono sempre a $2^A$ l'insieme vuoto $\emptyset$ (sottoinsieme improprio privo di elementi) e l'insieme ambiente stesso $A$:
> $$\emptyset \in 2^A, \quad A \in 2^A$$

> [!tip]- Flashcard: Definizione di Insieme delle Parti
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Dato un insieme generico $A$, come viene formalmente definito l'insieme delle parti e quali due sottoinsiemi vi appartengono sempre banalmente?
> Back: L'insieme delle parti di $A$ (denotato con $2^A$ o $\mathcal{P}(A)$) è la collezione di tutti i sottoinsiemi di $A$:
> $$2^A := \{B \mid B \subseteq A\}$$
> Vi appartengono sempre l'insieme vuoto $\emptyset$ e l'insieme ambiente stesso $A$, ossia $\emptyset \in 2^A$ e $A \in 2^A$.
> Tags: education/university education/math math/probability
> END
> %%

Il docente precisa che in ambito matematico si preferisce l'espressione "collezione di sottoinsiemi" anziché "insieme di insiemi" per evitare le antinomie della teoria ingenua degli insiemi (in particolare il paradosso di Russell) e rispettare la gerarchia assiomatica Zermelo-Fraenkel.

### La Funzione Indicatrice (Caratteristica)

Per comprendere il motivo profondo per cui l'insieme delle parti viene denotato con il simbolo esponenziale $2^A$, consideriamo un sottoinsieme arbitrario $B \subseteq A$. Esiste un modo canonico e univoco di descrivere l'appartenenza a $B$ attraverso una funzione a valori nell'insieme binario $\{0, 1\}$.

> [!danger] Definizione: Funzione Indicatrice (o Caratteristica)
> Sia $A$ un insieme e sia $B \subseteq A$. Si definisce <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>funzione indicatrice</b></font></mark> (o *funzione caratteristica*, denotata con $f_B$ o $\mathbf{1}_B$) l'applicazione $f_B: A \to \{0, 1\}$ definita puntualmente da:
> $$f_B(a) := \begin{cases} 1 & \text{se } a \in B \\ 0 & \text{se } a \notin B \end{cases}$$
> 
> - **Ipotesi:** $A$ insieme non vuoto, $B$ arbitrario sottoinsieme di $A$ ($B \in 2^A$).
> - **Condizioni di validità:** Il codominio è l'insieme discreto a due elementi $\{0, 1\}$.
> - **Significato dei simboli:**
>   - $a \in A$: generico elemento dell'insieme ambiente.
>   - $f_B(a) = 1$: l'elemento $a$ appartiene al sottoinsieme $B$.
>   - $f_B(a) = 0$: l'elemento $a$ non appartiene al sottoinsieme $B$ (appartiene al complementare $A \setminus B$).
> - **Esempio operativo:** Se $A = \{1, 2, 3\}$ e $B = \{2\}$, allora $f_B(1) = 0$, $f_B(2) = 1$, $f_B(3) = 0$.

> [!tip]- Flashcard: Funzione Indicatrice
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Cloze
> Text: Sia $B \subseteq A$. La **funzione indicatrice** $f_B: A \to \{0, 1\}$ associa a ciascun elemento $a \in A$ il valore {{c1::$1$}} se {{c2::$a \in B$}} e il valore {{c1::$0$}} se {{c2::$a \notin B$}}.
> Extra: La funzione indicatrice traduce la relazione insiemistica di appartenenza in una variabile logico-aritmetica binaria booleana.
> Tags: education/university education/math math/probability
> END
> %%

### Bigezione tra $\mathcal{P}(A)$ e lo Spazio delle Funzioni $\{0, 1\}^A$

La funzione indicatrice stabilisce un ponte concettuale perfetto tra sottoinsiemi e funzioni:

1. **Da sottoinsieme a funzione:** Ad ogni sottoinsieme $B \subseteq A$ corrisponde un'unica funzione indicatrice $f_B \in \{0, 1\}^A$.
2. **Da funzione a sottoinsieme:** Data una qualunque funzione binaria $g: A \to \{0, 1\}$, essa individua in modo univoco un sottoinsieme di $A$ prendendo la controimmagine dell'elemento $1$ (come formalizzato in [[03 - Funzioni (Parte I)]]):
   $$B_g := \{a \in A \mid g(a) = 1\} = g^{-1}(\{1\})$$

Poiché tale corrispondenza è biunivoca (<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>bigezione</b></font></mark>), i due insiemi sono isomorfi:

$$\mathcal{P}(A) \cong \{0, 1\}^A$$

In notazione insiemistica avanzata, l'insieme di tutte le funzioni con dominio $X$ e codominio $Y$ viene denotato con la scrittura esponenziale $Y^X$. Quando il codominio è l'insieme a due elementi $Y = \{0, 1\}$, la scrittura $\{0, 1\}^A$ viene naturalmente abbreviata con:

$$2^A$$

La notazione esponenziale $2^A$ non è quindi un mero artificio estetico, ma una diretta conseguenza della teoria delle corrispondenze funzionali.

> [!tip]- Flashcard: Bigezione tra Sottoinsiemi e Funzioni Binarie
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Perché in matematica l'insieme delle parti di un insieme $A$ viene denotato con la notazione esponenziale $2^A$?
> Back: Perché esiste una bigezione naturale tra la collezione dei sottoinsiemi di $A$ e l'insieme delle funzioni binarie $f: A \to \{0, 1\}$. Nella teoria degli insiemi lo spazio di tutte le funzioni da $A$ verso un insieme $Y$ si denota con $Y^A$; ponendo $Y = \{0, 1\}$ (insieme con $2$ elementi), lo spazio funzionale si denota con $\{0, 1\}^A \equiv 2^A$.
> Tags: education/university education/math math/probability
> END
> %%

---

## 2. Cardinalità degli Eventi e Binomio di Newton

### Teorema della Cardinalità dell'Insieme delle Parti

Dalla corrispondenza biunivoca con le funzioni binarie discende immediatamente il calcolo del numero totale di possibili sottoinsiemi definibili su un insieme finito.

> [!danger] Teorema: Cardinalità di $2^A$
> Sia $A$ un insieme finito avente cardinalità $\#A = n \in \mathbb{N}$. La cardinalità dell'insieme delle parti $2^A$ (ovvero il numero totale di suoi sottoinsiemi) è pari a:
> $$\#(2^A) = 2^{\#A} = 2^n$$
> 
> - **Ipotesi:** $A$ insieme finito con cardinalità $\#A = n$.
> - **Condizioni di validità:** Valido per ogni $n \ge 0$ (per $n = 0$, $A = \emptyset \implies \#(2^\emptyset) = 2^0 = 1$, corrispondente al solo $\{\emptyset\}$).
> - **Significato dei simboli:**
>   - $\#A$: numero di elementi distinti appartenenti ad $A$.
>   - $\#(2^A)$: numero complessivo di eventi (sottoinsiemi) generabili su $A$.
> - **Giustificazione combinatoria:** Costruire un sottoinsieme $B \subseteq A$ equivale a compiere $n$ decisioni binarie mutuamente indipendenti: per ciascuno degli $n$ elementi di $A$, decidere se includerlo ($1$) o escluderlo ($0$). Per il principio fondamentale del calcolo combinatorio, il numero totale di configurazioni possibili è:
>   $$\underbrace{2 \times 2 \times \dots \times 2}_{n \text{ volte}} = 2^n$$

> [!tip]- Flashcard: Teorema della Cardinalità di 2^A
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Cloze
> Text: Sia $A$ un insieme finito avente cardinalità $\#A = n$. La cardinalità dell'insieme delle parti è pari a {{c1::$\#(2^A) = 2^n$}}, corrispondente al numero complessivo di funzioni distinte appartenenti a {{c2::$\{0, 1\}^A$}}.
> Extra: Se lo spazio campionario $\Omega$ ha $n$ esiti elementari, il numero totale di eventi aleatori su cui si può scommettere è esattamente $2^n$.
> Tags: education/university education/math math/probability
> END
> %%

### Connessione con il Teorema del Binomio di Newton

Il docente evidenzia come la cardinalità complessiva $2^n$ possa essere ottenuta raggruppando i sottoinsiemi in classi disgiunte in base al numero di elementi $k$ che contengono ($k = 0, 1, 2, \dots, n$). Il numero di sottoinsiemi aventi esattamente $k$ elementi corrisponde al coefficiente binomiale $\binom{n}{k}$:

$$\#(2^A) = \sum_{k=0}^n \binom{n}{k}$$

In virtù del celebre <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>teorema del binomio di Newton</b></font></mark>:

$$(a + b)^n = \sum_{k=0}^n \binom{n}{k} a^{n-k} b^k$$

Ponendo la scelta elementare $a = 1$ e $b = 1$, si ottiene l'identità fondamentale:

$$(1 + 1)^n = \sum_{k=0}^n \binom{n}{k} 1^{n-k} 1^k \implies 2^n = \sum_{k=0}^n \binom{n}{k}$$

> [!tip]- Flashcard: Binomio di Newton e Sottoinsiemi
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Come si dimostra combinatoriamente l'uguaglianza $\sum_{k=0}^n \binom{n}{k} = 2^n$ mediante il binomio di Newton?
> Back: Applicando la formula del binomio di Newton $(a + b)^n = \sum_{k=0}^n \binom{n}{k} a^{n-k} b^k$ con $a = 1$ e $b = 1$:
> $$(1 + 1)^n = 2^n = \sum_{k=0}^n \binom{n}{k}$$
> Tale somma rappresenta il conteggio di tutti i possibili sottoinsiemi di un insieme di $n$ elementi, partizionati per cardinalità $k$ (da $k=0$ a $k=n$).
> Tags: education/university education/math math/probability
> END
> %%

### Esempio Operativo d'Aula: Lo Spazio dei Due Lanci di Moneta

Riprendendo l'esperimento dei due lanci di moneta introdotto nella [[01 - Teoria degli Insiemi, Spazio Campionario e Prime Nozioni di Probabilità|Lezione 1]]:

$$\Omega = \{(T, T), (T, C), (C, T), (C, C)\}$$

Ciascun evento elementare $\omega \in \Omega$ è un vettore a due componenti in cui l'ordine temporale dei lanci è discriminante: $(T, C) \ne (C, T)$.

La cardinalità dello spazio campionario è $\#\Omega = 4$. Il numero totale di eventi possibili è:

$$\#(2^\Omega) = 2^4 = 16$$

La scomposizione esplicita secondo le cardinalità $k$ illustrata dal docente è la seguente:

| Cardinalità $k$ | Coefficiente Binomiale | Numero Eventi | Eventi Corrispondenti |
| :---: | :---: | :---: | :--- |
| $k = 0$ | $\binom{4}{0}$ | $1$ | Insieme vuoto $\emptyset$ (evento impossibile) |
| $k = 1$ | $\binom{4}{1}$ | $4$ | Singoletti elementari: $\{(T, T)\}, \{(T, C)\}, \{(C, T)\}, \{(C, C)\}$ |
| $k = 2$ | $\binom{4}{2} = \frac{4 \times 3}{2}$ | $6$ | Coppie di esiti: es. $\{(T, T), (T, C)\}, \{(T, T), (C, C)\}, \dots$ |
| $k = 3$ | $\binom{4}{3} = \binom{4}{1}$ | $4$ | Terne di esiti, ottenute escludendo un singolo elemento: $\Omega \setminus \{\omega\}$ |
| $k = 4$ | $\binom{4}{4}$ | $1$ | Spazio campionario intero $\Omega$ (evento certo) |

$$\text{Totale Eventi} = 1 + 4 + 6 + 4 + 1 = 16 = 2^4$$

Il docente sottolinea la **simmetria complementare**: costruire un sottoinsieme con $3$ elementi su $4$ equivale esattamente a scegliere l'unico elemento da lasciare fuori ($\Omega \setminus \{(T, T)\}$, $\Omega \setminus \{(T, C)\}$, ecc.), da cui l'uguaglianza algebrica $\binom{4}{3} = \binom{4}{1} = 4$.

> [!tip]- Flashcard: Conteggio Eventi nei Due Lanci di Moneta
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Nell'esperimento del lancio di due monete ($\#\Omega = 4$), quanti eventi contengono esattamente 3 elementi e come si individuano rapidamente senza elencarli tutti?
> Back: Gli eventi con cardinalità $3$ sono $\binom{4}{3} = \binom{4}{1} = 4$. Si individuano sfruttando la simmetria complementare: scegliere $3$ elementi da includere equivale a scegliere l'unico evento elementare $\omega$ da escludere dallo spazio campionario, ossia considerando i complementari $\Omega \setminus \{\omega\}$.
> Tags: education/university education/math math/probability
> END
> %%

---

## 3. Spazio Campionario, Eventi e Incompatibilità

### Tipologie Fondamentali di Eventi

All'interno dell'algebra degli eventi generata da uno spazio campionario $\Omega$:
- **Evento Certo:** l'intero spazio campionario $\Omega$; si verifica sempre poiché il risultato dell'esperimento aleatorio appartiene necessariamente a $\Omega$.
- **Evento Impossibile:** l'insieme vuoto $\emptyset$; non si verifica mai poiché non contiene alcun esito elementare.

### Definizione Formale di Incompatibilità

> [!danger] Definizione: Eventi Incompatibili (Disgiunti)
> Due eventi $A, B \subseteq \Omega$ si dicono **incompatibili** (o *mutuamente esclusivi*, o *disgiunti*) se e solo se la loro intersezione coincide con l'insieme vuoto:
> $$A \cap B = \emptyset$$
> 
> - **Ipotesi:** $A, B \in 2^\Omega$.
> - **Condizioni di validità:** Non ammettono alcun esito elementare in comune ($\nexists \omega \in \Omega : \omega \in A \land \omega \in B$).
> - **Significato probabilistico:** I due eventi non possono verificarsi simultaneamente nel corso della medesima prova sperimentale.

> [!tip]- Flashcard: Definizione di Eventi Incompatibili
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Qual è la condizione insiemistica affinché due eventi $A$ e $B$ siano definiti incompatibili (o mutuamente esclusivi)?
> Back: Due eventi $A$ e $B$ sono incompatibili se e solo se la loro intersezione è vuota:
> $$A \cap B = \emptyset$$
> Ciò implica che il verificarsi di uno esclude categoricamente il verificarsi simultaneo dell'altro nella medesima prova sperimentale.
> Tags: education/university education/math math/probability
> END
> %%

![[Schema - Diagramma di Eulero-Venn - Spazio Campionario ed Eventi.png]]
*(Rappresentazione di eventi come sottoinsiemi dello spazio campionario $\Omega$)*

### L'Esempio Chiarificatore sulla Retta Reale

Per superare l'errore concettuale frequente secondo cui due insiemi incompatibili debbano essere fisicamente "separati da una distanza positiva", il docente presenta il seguente esempio analitico sulla retta reale $\mathbb{R}$:

- Sia $A = (-\infty, 0) = \{x \in \mathbb{R} \mid x < 0\}$ (semiretta negativa, $0$ escluso).
- Sia $B = [0, +\infty) = \{x \in \mathbb{R} \mid x \ge 0\}$ (semiretta non negativa, $0$ incluso).

Sebbene i due intervalli siano contigui e condividano il punto di frontiera $x = 0$, la loro intersezione è rigorosamente vuota:

$$A \cap B = \{x \in \mathbb{R} \mid x < 0 \land x \ge 0\} = \emptyset$$

Lo zero appartiene a $B$ ma non ad $A$; poiché per appartenere all'intersezione un elemento dovrebbe appartenere contemporaneamente a entrambi gli insiemi, nessun numero reale soddisfa tale condizione. Pertanto $A$ e $B$ sono incompatibili. Non serve una distanza metrica: è sufficiente la rigorosa disgiunzione insiemistica.

> [!tip]- Flashcard: Incompatibilità e Contiguità sulla Retta Reale
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Perché i due intervalli contigui $A = (-\infty, 0)$ e $B = [0, +\infty)$ sono formalmente incompatibili sebbene tocchino lo stesso punto soglia $x=0$?
> Back: Perché l'intersezione è rigorosamente vuota ($A \cap B = \emptyset$): l'elemento $0$ appartiene a $B$ ma non appartiene ad $A$. L'incompatibilità richiede unicamente che non vi siano elementi comuni condivisi, senza richiedere alcuna distanza metrica positiva tra gli insiemi.
> Tags: education/university education/math math/probability
> END
> %%

---

## 4. Definizione Assiomatica della Probabilità (Assiomi di Kolmogorov)

### Limiti della Definizione Classica e Necessità di una Teoria Assiomatica

La formulazione classica di Laplace definisce la probabilità come il rapporto tra il numero dei casi favorevoli e il numero dei casi possibili:

$$\mathbb{P}(E) = \frac{\#E}{\#\Omega}$$

Come rimarca il docente, tale impostazione presenta due limiti strutturali insormontabili \[[[Dispense Statistica e Probabilità.pdf#page=17|Dispense p. 17]]]:
1. **Presuppone a monte l'equiprobabilità:** Ha senso solo se tutti gli eventi elementari $\omega \in \Omega$ hanno la medesima probabilità di verificarsi (es. dado perfetto, moneta non truccata). Se la moneta o il dado sono sbilanciati o truccati, tale formula perde qualsiasi validità.
2. **Circolo vizioso:** Definire la probabilità presupponendo che gli eventi elementari siano "ugualmente possibili" (ossia equiprobabili) costituisce una tautologia logica.

Per costruire una teoria rigorosa valida per qualsiasi fenomeno aleatorio (finito, discreto o continuo), la matematica moderna adotta l'impostazione assiomatica introdotta da <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Andrej Nikolaevič Kolmogorov</b></font></mark> (1933).

### La Misura di Probabilità

La probabilità non è un semplice numero, ma una <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>misura di probabilità</b></font></mark> (funzione d'insieme) che assegna a ciascun evento $E$ dello spazio delle parti un valore numerico reale nell'intervallo chiuso $[0, 1]$:

$$\mathbb{P}: 2^\Omega \to [0, 1], \quad E \mapsto \mathbb{P}(E)$$

> [!danger] Definizione: Spazio di Probabilità e Assiomi di Kolmogorov
> Uno <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>spazio di probabilità</b></font></mark> è una struttura $(\Omega, 2^\Omega, \mathbb{P})$ dove $\Omega$ è lo spazio campionario, $2^\Omega$ è la famiglia degli eventi ammissibili, e $\mathbb{P}: 2^\Omega \to [0, 1]$ è una funzione che soddisfa i seguenti tre assiomi fondamentali \[[[Dispense Statistica e Probabilità.pdf#page=17|Dispense p. 17]]]:
> 
> 1. <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Assioma 1 (Non-negatività e Limitatezza)</b></font></mark>: Per ogni evento $E \subseteq \Omega$:
>    $$\mathbb{P}(E) \in [0, 1] \quad (\text{ovvero } 0 \le \mathbb{P}(E) \le 1)$$
> 2. <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Assioma 2 (Normalizzazione dell'Evento Certo)</b></font></mark>:
>    $$\mathbb{P}(\Omega) = 1$$
> 3. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Assioma 3 ($\sigma$-additività)</b></font></mark>: Per ogni successione di eventi $E_1, E_2, \dots, E_n, \dots \in 2^\Omega$ a due a due incompatibili ($E_i \cap E_j = \emptyset$ per ogni $i \ne j$):
>    $$\mathbb{P}\left(\bigcup_{j=1}^{+\infty} E_j\right) = \sum_{j=1}^{+\infty} \mathbb{P}(E_j)$$

> [!tip]- Flashcard: Assiomi di Kolmogorov
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Cloze
> Text: Dati uno spazio campionario $\Omega$ e la famiglia delle parti $2^\Omega$, una **misura di probabilità** $\mathbb{P}$ soddisfa i tre assiomi di Kolmogorov:
> 1. Non-negatività/Limitatezza: {{c1::$0 \le \mathbb{P}(E) \le 1, \; \forall E \in 2^\Omega$}}
> 2. Normalizzazione: {{c2::$\mathbb{P}(\Omega) = 1$}}
> 3. $\sigma$-additività: se $E_i \cap E_j = \emptyset$ per $i \ne j$, allora {{c3::$\mathbb{P}\left(\bigcup_{j=1}^{+\infty} E_j\right) = \sum_{j=1}^{+\infty} \mathbb{P}(E_j)$}}
> Extra: L'assioma 3 garantisce la compatibilità tra l'unione insiemistica numerabile e la serie numerica delle probabilità.
> Tags: education/university education/math math/probability
> END
> %%

Il docente spiega che l'Assioma 3 consente operativamente di "portare fuori" l'operatore di probabilità rispetto all'unione: la probabilità dell'unione di eventi non sovrapposti si trasforma nella somma aritmetica delle singole probabilità.

> [!tip]- Flashcard: Significato Concettuale dell'Assioma 3
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Cosa permette di compiere a livello operativo l'Assioma 3 ($\sigma$-additività) nel calcolo delle probabilità?
> Back: Permette di commutare l'operatore di probabilità con l'unione disgiunta numerabile: calcolare la probabilità che si verifichi almeno uno tra infiniti eventi disgiunti equivale a calcolare la serie numerica delle rispettive probabilità individuali:
> $$\mathbb{P}\left(\bigcup_{j=1}^{+\infty} E_j\right) = \sum_{j=1}^{+\infty} \mathbb{P}(E_j)$$
> Tags: education/university education/math math/probability
> END
> %%

---

## 5. Proprietà Fondamentali Dimostrate dagli Assiomi

A partire esclusivamente dai tre assiomi di Kolmogorov, si deducono in modo deduttivo tutte le leggi operative del calcolo delle probabilità \[[[Dispense Statistica e Probabilità.pdf#page=19|Dispense pp. 19–20]]].

### 5.1 Probabilità dell'Evento Impossibile $\mathbb{P}(\emptyset) = 0$

> [!summary] Proposizione 1: Probabilità dell'Insieme Vuoto
> L'<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>evento impossibile</b></font></mark> ha probabilità identicamente nulla:
> $$\mathbb{P}(\emptyset) = 0$$

> [!info] Dimostrazione Formale del Docente
> Per verificare che $\mathbb{P}(\emptyset) = 0$ disponendo esclusivamente dei tre assiomi, sfruttiamo l'arbitrarietà della successione di eventi disgiunti nell'Assioma 3.
> 
> Costruiamo la successione $\{E_j\}_{j=1}^{+\infty}$ ponendo:
> - $E_1 = \Omega$ (lo spazio campionario);
> - $E_j = \emptyset$ per ogni $j \ge 2$ ($E_2 = \emptyset, E_3 = \emptyset, \dots$).
> 
> **Verifica delle ipotesi di disgiunzione:**
> - $E_1 \cap E_j = \Omega \cap \emptyset = \emptyset$ per ogni $j \ge 2$;
> - $E_i \cap E_j = \emptyset \cap \emptyset = \emptyset$ per ogni $i, j \ge 2$ con $i \ne j$.
> Gli eventi sono a due a due incompatibili.
> 
> **Calcolo dell'unione numerabile:**
> $$\bigcup_{j=1}^{+\infty} E_j = \Omega \cup \emptyset \cup \emptyset \cup \dots = \Omega$$
> 
> **Applicazione dell'Assioma 3:**
> $$\mathbb{P}(\Omega) = \mathbb{P}\left(\bigcup_{j=1}^{+\infty} E_j\right) = \mathbb{P}(E_1) + \sum_{j=2}^{+\infty} \mathbb{P}(E_j) = \mathbb{P}(\Omega) + \sum_{j=2}^{+\infty} \mathbb{P}(\emptyset)$$
> 
> Per l'Assioma 2 sappiamo che $\mathbb{P}(\Omega) = 1$. Sostituendo nella relazione:
> $$1 = 1 + \sum_{j=2}^{+\infty} \mathbb{P}(\emptyset)$$
> 
> Sottraendo $1$ a entrambi i membri:
> $$\sum_{j=2}^{+\infty} \mathbb{P}(\emptyset) = 0$$
> 
> La serie a sinistra è una somma di infiniti termini identici $\mathbb{P}(\emptyset)$. Poiché per l'Assioma 1 ciascun termine è non negativo ($\mathbb{P}(\emptyset) \ge 0$), l'unico modo in cui una somma di quantità non negative possa essere identicamente nulla è che ogni singolo addendo sia nullo:
> $$\mathbb{P}(\emptyset) = 0 \quad \blacksquare$$

> [!tip]- Flashcard: Dimostrazione di P(vuoto) = 0
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Come si dimostra formalmente che $\mathbb{P}(\emptyset) = 0$ utilizzando esclusivamente gli assiomi di Kolmogorov?
> Back: Si sceglie la successione disgiunta $E_1 = \Omega$ e $E_j = \emptyset$ per $j \ge 2$. L'unione numerabile è $\bigcup_{j=1}^\infty E_j = \Omega$. Applicando l'Assioma 3:
> $$\mathbb{P}(\Omega) = \mathbb{P}(E_1) + \sum_{j=2}^\infty \mathbb{P}(E_j) = \mathbb{P}(\Omega) + \sum_{j=2}^\infty \mathbb{P}(\emptyset)$$
> Poiché $\mathbb{P}(\Omega) = 1$, si ottiene $1 = 1 + \sum_{j=2}^\infty \mathbb{P}(\emptyset) \implies \sum_{j=2}^\infty \mathbb{P}(\emptyset) = 0$. Essendo $\mathbb{P}(\emptyset) \ge 0$ per l'Assioma 1, l'unico termine possibile è $\mathbb{P}(\emptyset) = 0$.
> Tags: education/university education/math math/probability
> END
> %%

### 5.2 Additività Finita per Eventi Incompatibili

L'Assioma 3 postula l'additività su successioni infinite numerabili. In molte applicazioni reali si manipolano solo due o un numero finito $n$ di eventi.

> [!danger] Teorema: Additività Finita
> Siano $A, B \subseteq \Omega$ due eventi incompatibili ($A \cap B = \emptyset$). La proprietà di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>additività finita</b></font></mark> stabilisce che:
> $$\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B)$$
> 
> Più in generale, per una collezione finita di $n$ eventi $E_1, \dots, E_n \subseteq \Omega$ a due a due incompatibili ($E_i \cap E_j = \emptyset$ per $i \ne j$):
> $$\mathbb{P}\left(\bigcup_{i=1}^n E_i\right) = \sum_{i=1}^n \mathbb{P}(E_i)$$

![[Schema - Diagramma di Eulero-Venn - Unione.png]]
*(Rappresentazione grafica dell'unione di eventi)*

> [!info] Dimostrazione Formale per Due Eventi
> Siano $A, B \in 2^\Omega$ con $A \cap B = \emptyset$.
> Costruiamo una successione infinita definendo:
> - $E_1 = A$;
> - $E_2 = B$;
> - $E_j = \emptyset$ per ogni $j \ge 3$.
> 
> Poiché $A \cap B = \emptyset$ e l'intersezione con l'insieme vuoto è sempre vuota, gli eventi della successione sono a due a due disgiunti. L'unione numerabile è:
> $$\bigcup_{j=1}^{+\infty} E_j = A \cup B \cup \emptyset \cup \emptyset \cup \dots = A \cup B$$
> 
> Applicando l'Assioma 3:
> $$\mathbb{P}(A \cup B) = \mathbb{P}(E_1) + \mathbb{P}(E_2) + \sum_{j=3}^{+\infty} \mathbb{P}(E_j) = \mathbb{P}(A) + \mathbb{P}(B) + \sum_{j=3}^{+\infty} \mathbb{P}(\emptyset)$$
> 
> Avendo già dimostrato che $\mathbb{P}(\emptyset) = 0$, la coda infinita della serie si annulla completamente:
> $$\sum_{j=3}^{+\infty} \mathbb{P}(\emptyset) = 0$$
> Si ottiene quindi l'identità:
> $$\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B) \quad \blacksquare$$
> 
> *(La generalizzazione a $n$ eventi disgiunti si ottiene banalmente per induzione matematica su $n$ \[[[Dispense Statistica e Probabilità.pdf#page=19|Dispense p. 19]]].)*

> [!tip]- Flashcard: Dimostrazione Additività Finita
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Come si dimostra la proprietà di additività finita $\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B)$ per due eventi disgiunti partendo dalla $\sigma$-additività?
> Back: Si costruisce la successione ponendo $E_1 = A$, $E_2 = B$ e $E_j = \emptyset$ per ogni $j \ge 3$. L'unione infinita coincide con $A \cup B$. Per l'Assioma 3:
> $$\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B) + \sum_{j=3}^\infty \mathbb{P}(\emptyset)$$
> Poiché $\mathbb{P}(\emptyset) = 0$, la serie si annulla, lasciando esattamente $\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B)$.
> Tags: education/university education/math math/probability
> END
> %%

### 5.3 Probabilità dell'Evento Complementare

> [!danger] Teorema: Probabilità del Complementare
> Per ogni evento $A \subseteq \Omega$, la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>probabilità del complementare</b></font></mark> $A^\complement = \Omega \setminus A$ è data da:
> $$\mathbb{P}(A^\complement) = 1 - \mathbb{P}(A)$$

![[Schema - Diagramma di Eulero-Venn - Complementare.png]]
*(Rappresentazione grafica del complementare $A^\complement$ rispetto allo spazio $\Omega$)*

> [!info] Dimostrazione Formale
> Per definizione di insieme complementare, un elemento $x \in \Omega$ appartiene ad $A$ oppure non vi appartiene ($x \in A^\complement$). Di conseguenza:
> 1. $A \cup A^\complement = \Omega$ (gli eventi sono congiuntamente esaustivi);
> 2. $A \cap A^\complement = \emptyset$ (un elemento non può contemporaneamente appartenere e non appartenere ad $A$, per il principio di non contraddizione).
> 
> Poiché $A$ e $A^\complement$ sono incompatibili, possiamo applicare la proprietà di additività finita per due eventi:
> $$\mathbb{P}(A \cup A^\complement) = \mathbb{P}(A) + \mathbb{P}(A^\complement)$$
> 
> Poiché $A \cup A^\complement = \Omega$, per l'Assioma 2 si ha $\mathbb{P}(A \cup A^\complement) = \mathbb{P}(\Omega) = 1$:
> $$\mathbb{P}(A) + \mathbb{P}(A^\complement) = 1$$
> 
> Isolando $\mathbb{P}(A^\complement)$:
> $$\mathbb{P}(A^\complement) = 1 - \mathbb{P}(A) \quad \blacksquare$$

> [!tip]- Flashcard: Probabilità dell'Evento Complementare
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Cloze
> Text: Per qualunque evento $A \subseteq \Omega$, la probabilità del complementare è {{c1::$\mathbb{P}(A^\complement) = 1 - \mathbb{P}(A)$}}.
> Extra: Dimostrazione: $A$ e $A^\complement$ formano una partizione disgiunta dello spazio campionario ($A \cup A^\complement = \Omega$ e $A \cap A^\complement = \emptyset$); per l'additività finita $\mathbb{P}(A) + \mathbb{P}(A^\complement) = \mathbb{P}(\Omega) = 1$.
> Tags: education/university education/math math/probability
> END
> %%

---

## 6. Spazi di Probabilità Finiti e Distribuzione sugli Eventi Elementari

### Probabilità Equilibrata vs Truccata

Il docente illustra come gli assiomi consentano di trattare indifferentemente modelli simmetrici e asimmetrici:

1. **Moneta Equilibrata (Caso Classico):**
   - Spazio campionario $\Omega = \{T, C\}$.
   - Poiché i due esiti sono disgiunti ed esaustivi, per l'additività e la simmetria:
     $$\mathbb{P}(\{T\}) + \mathbb{P}(\{C\}) = 1 \implies \mathbb{P}(\{T\}) = \mathbb{P}(\{C\}) = \frac{1}{2}$$
2. **Moneta Truccata (Sbilanciata):**
   - Se per ragioni fisiche o costruttive la moneta favorisce l'uscita di Testa con probabilità $\mathbb{P}(\{T\}) = \frac{2}{3}$, la probabilità dell'esito Croce è rigidamente vincolata dalla formula del complementare:
     $$\mathbb{P}(\{C\}) = \mathbb{P}(\{T\}^\complement) = 1 - \mathbb{P}(\{T\}) = 1 - \frac{2}{3} = \frac{1}{3}$$
   - Non è possibile assegnare valori arbitrari slegati tra loro: la somma sulle parti disgiunte che coprono $\Omega$ deve restituire esattamente $1$.

> [!tip]- Flashcard: Moneta Truccata e Normalizzazione
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Se in un lancio di moneta la probabilità che esca Testa è assegnata pari a $\mathbb{P}(\{T\}) = \frac{2}{3}$, qual è la probabilità dell'esito Croce e quale principio assiomatico lo impone?
> Back: La probabilità è $\mathbb{P}(\{C\}) = \frac{1}{3}$. Lo impone l'Assioma 2 unitamente all'additività finita per eventi disgiunti ed esaustivi: $\{T\} \cup \{C\} = \Omega$ con $\{T\} \cap \{C\} = \emptyset$, da cui $\mathbb{P}(\{T\}) + \mathbb{P}(\{C\}) = \mathbb{P}(\Omega) = 1$.
> Tags: education/university education/math math/probability
> END
> %%

### Teorema Fondamentale di Riduzione agli Eventi Elementari

Uno dei messaggi centrali della lezione riguarda la semplificazione operativa consentita dagli spazi campionari discreti \[[[Dispense Statistica e Probabilità.pdf#page=19|Dispense p. 19]]].

In linea di principio, assegnare una probabilità richiederebbe di specificare una funzione $\mathbb{P}$ su ciascuno dei $2^n$ sottoinsiemi di $2^\Omega$. Tuttavia, se $\Omega$ è un insieme finito:

$$\Omega = \{\omega_1, \omega_2, \dots, \omega_N\}$$

ogni evento composto $E \subseteq \Omega$ può essere espresso in modo unico come l'unione disgiunta dei suoi eventi elementari atomici:

$$E = \bigcup_{\omega_i \in E} \{\omega_i\}$$

Applicando la proprietà di additività finita:

$$\mathbb{P}(E) = \sum_{\omega_i \in E} \mathbb{P}(\{\omega_i\})$$

> [!danger] Teorema: Riduzione della Misura di Probabilità agli Eventi Elementari
> Sia $(\Omega, 2^\Omega, \mathbb{P})$ uno spazio di probabilità finito con $\#\Omega = N$. Secondo il teorema di <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>riduzione agli eventi elementari</b></font></mark>, per determinare univocamente la probabilità di qualunque evento $E \in 2^\Omega$ è necessario e sufficiente assegnare la probabilità ai singoli eventi elementari:
> $$p(\omega_i) \equiv p_i := \mathbb{P}(\{\omega_i\}), \quad i = 1, \dots, N$$
> purché i pesi soddisfino le due condizioni di ammissibilità:
> 1. **Non-negatività:** $p(\omega_i) \ge 0 \quad (\forall i = 1, \dots, N)$
> 2. **Normalizzazione:** $\sum_{i=1}^N p(\omega_i) = 1$
> 
> La probabilità di un qualsiasi evento composto $E \subseteq \Omega$ è data semplicemente dalla somma:
> $$\mathbb{P}(E) = \sum_{\omega_i \in E} p(\omega_i)$$

> [!tip]- Flashcard: Teorema di Riduzione agli Eventi Elementari
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Basic
> Front: Perché negli spazi di probabilità finiti non è necessario definire la funzione $\mathbb{P}$ su tutti i $2^N$ sottoinsiemi di $2^\Omega$?
> Back: Perché ogni evento composto $E \subseteq \Omega$ è l'unione disgiunta dei suoi eventi elementari singoletti $E = \bigcup_{\omega \in E} \{\omega\}$. Per l'additività finita, basta conoscere i pesi assegnati ai singoli esiti atomici $p(\omega) := \mathbb{P}(\{\omega\})$, e calcolare la probabilità di $E$ sommando i pesi:
> $$\mathbb{P}(E) = \sum_{\omega \in E} p(\omega)$$
> Tags: education/university education/math math/probability
> END
> %%

### Esempio Pratico: Calcolo della Probabilità di un Evento Discreto

Consideriamo un esperimento con esiti discreti $\Omega = \{1, 2, 3, 4, 5, 6\}$ (un dado a 6 facce, eventualmente pesato). Conoscendo i pesi elementari $p(1), p(2), \dots, p(6)$:

Per calcolare la probabilità dell'evento $E = \{1, 2, 4\}$ (esce un numero appartenente a tale terna), non serve una nuova misura empirica complessa:

$$\mathbb{P}(E) = \mathbb{P}(\{1\} \cup \{2\} \cup \{4\}) = p(1) + p(2) + p(4)$$

Se il dado è equilibrato ($p(i) = \frac{1}{6}$ per ogni $i$):

$$\mathbb{P}(E) = \frac{1}{6} + \frac{1}{6} + \frac{1}{6} = \frac{3}{6} = \frac{1}{2}$$

Se il dado è truccato con pesi asimmetrici (es. $p(1) = 0.1, p(2) = 0.2, p(4) = 0.15$):

$$\mathbb{P}(E) = 0.1 + 0.2 + 0.15 = 0.45$$

### Estensione agli Spazi Numerabili ("come" $\mathbb{N}$)

Il docente conclude osservando che questa straordinaria semplificazione non si applica solo agli spazi finiti, ma rimane valida per qualsiasi <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>spazio campionario infinito numerabile</b></font></mark> (ossia che può essere messo in corrispondenza biunivoca con l'insieme dei numeri naturali $\mathbb{N}$):

$$\Omega = \{\omega_1, \omega_2, \dots, \omega_j, \dots\}$$

In tal caso, per l'Assioma 3 ($\sigma$-additività numerabile), la probabilità di un qualsiasi evento composto $E \subseteq \Omega$ è data dalla serie numerica convergente:

$$\mathbb{P}(E) = \sum_{\omega_j \in E} p(\omega_j), \quad \text{con } \sum_{j=1}^{+\infty} p(\omega_j) = 1$$

Negli spazi discreti (finiti o numerabili), la teoria della probabilità coincide dunque con la teoria delle distribuzioni di pesi elementari non negativi a somma unitaria.

> [!tip]- Flashcard: Estensione agli Spazi Numerabili
> %%
> TARGET DECK: University::Probabilità e Statistica::02 - Insieme delle Parti, Assiomi della Probabilità e Spazi Finiti
> START
> Cloze
> Text: Se uno spazio campionario $\Omega$ è infinito numerabile (in bigezione con $\mathbb{N}$), la probabilità di qualunque evento $E \subseteq \Omega$ è calcolata tramite la serie convergente {{c1::$\mathbb{P}(E) = \sum_{\omega \in E} p(\omega)$}}, garantita dall'{{c2::Assioma 3 ($\sigma$-additività)}}.
> Extra: La condizione di normalizzazione complessiva richiede che la serie su tutti gli esiti elementari converga a uno: $\sum_{j=1}^{+\infty} p(\omega_j) = 1$.
> Tags: education/university education/math math/probability
> END
> %%

---

## Sintesi dei Concetti Cardine

| Concetto | Notazione Matematica | Proprietà / Definizione | Significato Operativo |
| :--- | :--- | :--- | :--- |
| **Insieme delle Parti** | $2^\Omega \equiv \mathcal{P}(\Omega)$ | $\{B \mid B \subseteq \Omega\}$ | Famiglia di tutti gli eventi aleatori generabili |
| **Funzione Indicatrice** | $f_B: \Omega \to \{0, 1\}$ | $f_B(\omega) = 1$ se $\omega \in B$, altrimenti $0$ | Traduce l'appartenenza insiemistica in variabile booleana |
| **Cardinalità Eventi** | $\#(2^\Omega) = 2^n$ | $\sum_{k=0}^n \binom{n}{k} = 2^n$ (Newton) | Crescita esponenziale del numero di eventi rispetto a $\#\Omega = n$ |
| **Incompatibilità** | $A \cap B = \emptyset$ | Nessun esito elementare comune | Eventi che non possono verificarsi simultaneamente |
| **Assioma 1** | $\mathbb{P}(E) \in [0, 1]$ | $0 \le \mathbb{P}(E) \le 1, \; \forall E \subseteq \Omega$ | Non-negatività e limitatezza della misura |
| **Assioma 2** | $\mathbb{P}(\Omega) = 1$ | Evento certo ha probabilità unitaria | Condizione di normalizzazione dello spazio |
| **Assioma 3** | $\mathbb{P}(\bigcup_{j=1}^\infty E_j) = \sum_{j=1}^\infty \mathbb{P}(E_j)$ | Per eventi a due a due disgiunti | $\sigma$-additività numerabile |
| **Evento Impossibile** | $\mathbb{P}(\emptyset) = 0$ | Dedotto da A2 e A3 con $E_1 = \Omega, E_{j \ge 2} = \emptyset$ | L'insieme vuoto non ha peso probabilistico |
| **Additività Finita** | $\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B)$ | Se $A \cap B = \emptyset$ | Calcolo della probabilità di unioni finite disgiunte |
| **Complementare** | $\mathbb{P}(A^\complement) = 1 - \mathbb{P}(A)$ | Da $A \cup A^\complement = \Omega$ e $A \cap A^\complement = \emptyset$ | Probabilità del non verificarsi di un evento |
| **Riduzione Discreta** | $\mathbb{P}(E) = \sum_{\omega \in E} p(\omega)$ | Con $p(\omega) \ge 0, \; \sum_\Omega p(\omega) = 1$ | Riduzione del calcolo della misura ai soli eventi elementari |
