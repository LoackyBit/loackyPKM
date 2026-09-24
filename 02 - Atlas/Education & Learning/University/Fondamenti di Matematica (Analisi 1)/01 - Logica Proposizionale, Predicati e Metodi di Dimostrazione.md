---
status: permanent
type: lecture
area: education
related: ["[[Fondamenti di Matematica (Analisi 1) MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]"]
aliases: ["Lezione 1 Fondamenti di Matematica", "FdM Lezione 1", "Logica Proposizionale, Predicati e Metodi di Dimostrazione"]
source: Lezione 1 FdM del 23/09/2026 - Prof. Saverio Salzo
title: "01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione"
date: '2026-09-23'
updated: 2026-09-24T16:26
tags: [education/university, education/math, tech/logic]
summary: "Fondamenti di logica proposizionale e predicati: connettivi, tabelle di verità, leggi notevoli, quantificatori e dimostrazioni per contrapposizione e assurdo."
sources: ["[[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf]]", "[[Fondamenti di Matematica]]", "[[Fondamenti di Matematica (Analisi 1) 2026-27 - Trascrizione Audio]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Fondamenti di Matematica (Analisi 1) MOC]] / [[01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione]]

# 01 - Logica Proposizionale, Predicati e Metodi di Dimostrazione

- **Docente:** Prof. Saverio Salzo
- **Data Lezione:** 2026-09-23
- **Materiale Didattico Originale:** [[Fondamenti di Matematica - Lezione 01 - Appunti Manoscritti.pdf]]

## Quadro Concettuale e Obiettivi della Lezione

L'avvio dello studio dell'analisi matematica e dei <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>fondamenti della matematica</b></font></mark> richiede la costruzione preliminare di un apparato linguistico rigoroso, privo delle <mark style="background: rgba(181, 113, 255, 0.36); color: #9a54c1;"><b>ambiguità</b></mark> tipiche del linguaggio naturale. Da un punto di vista storico ed epistemologico, lo sviluppo della disciplina ha seguito un andamento apparentemente inverso: il calcolo infinitesimale (derivate e integrali, sviluppati nel XVII secolo da Newton e Leibniz) ha preceduto di oltre due secoli la sua completa formalizzazione logica e assiomatica (formalizzata tra fine Ottocento e inizio Novecento da figure quali Peano, Frege, Russell e Hilbert).

La necessità di formalizzazione nasce dall'esigenza di verificare la validità dei ragionamenti matematici mediante regole sintattiche definite, gettando le basi sia per la teoria degli insiemi e la proprietà di completezza dei numeri reali, sia per la logica matematica applicata all'informatica teorica.

> [!summary] Percorso Concettuale della Lezione
> - [d] **Linguaggio Naturale** $\to$ Necessità di eliminare ambiguità e soggettività
> - [d] **Formalizzazione Logica** $\to$ Sintassi, assiomi e valori oggettivi di verità ($V/F$)
> - [d] **Logica delle Proposizioni** $\to$ Connettivi $(\neg, \land, \lor, \implies, \iff)$ e tavole di verità
> - [d] **Tautologie & Regole d'Inferenza** $\to$ De Morgan, contronominale, dimostrazione per assurdo
> - [d] **Logica dei Predicati** $\to$ Proposizioni aperte e quantificatori $(\forall, \exists)$
> - [d] **Metodi di Dimostrazione** $\to$ Applicazione formale ai teoremi di Analisi Matematica

---

## Logica delle Proposizioni

### Proposizioni Semplici e Valori di Verità

L'atomo fondamentale del calcolo proposizionale è la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>proposizione</b></font></mark>. Una proposizione è una frase dichiarativa del linguaggio per la quale è possibile stabilire, in modo univoco e oggettivo, se sia vera ($V$) o falsa ($F$), escludendo interpretazioni soggettive o contestuali.

Nel formalismo, le proposizioni semplici si denotano con lettere maiuscole: $P, Q, R, S$.

- **Esempi di proposizioni:**
  - "$4$ è un numero primo" $\longrightarrow$ Proposizione valida (valore di verità: **F**).
  - "$\sqrt{2} \in \mathbb{R}$" $\longrightarrow$ Proposizione valida (valore di verità: **V**).
  - "Tutti gli interi sono pari" $\longrightarrow$ Proposizione valida (valore di verità: **F**).
- **Esempi di non proposizioni:**
  - "Chiudi la porta!" $\longrightarrow$ Frase imperativa: non ha senso attribuirle un valore di verità.
  - "Napoli è lontana da Roma" $\longrightarrow$ Giudizio soggettivo e ambiguo: la nozione di "lontananza" richiede una metrica non specificata.

> [!tip]- Flashcard: Definizione di Proposizione
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Basic
Front: Qual è la definizione formale di proposizione nella logica matematica?
Back: Una proposizione è una frase dichiarativa del linguaggio naturale o formale alla quale è possibile attribuire in modo univoco e oggettivo uno e un solo valore di verità: vero ($V$) oppure falso ($F$), senza alcuna ambiguità.
Tags: education/university education/math tech/logic
<!--ID: 1790260176596-->
END
%%

### Connettivi Logici

A partire da proposizioni atomiche, è possibile generare proposizioni composte impiegando gli <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>operatori logici (o connettivi logici)</b></font></mark>:

| Connettivo | Simbolo Formale | Nome Operazione | Lettura Verbale |
| :--- | :---: | :--- | :--- |
| Negazione | $\neg$ | Inversione logica | "non", "not" |
| Congiunzione | $\land$ | Prodotto logico | "e", "and" |
| Disgiunzione | $\lor$ | Somma logica (inclusiva) | "o", "or" |
| Implicazione | $\Rightarrow$ | Proposizione condizionale | "se ... allora ...", "implica" |
| Equivalenza | $\Leftrightarrow$ | Bicondizionale | "se e solo se", "equivale a" |

Se $P$ e $Q$ sono proposizioni, espressioni complesse quali $(P \Rightarrow Q) \lor (\neg R)$ e $[\neg(P \land Q)] \Rightarrow R$ sono a loro volta proposizioni il cui valore di verità è determinato univocamente dai valori delle componenti elementari.

### Tabelle di Verità e Semantica dei Connettivi

Le <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>tabelle di verità</b></font></mark> costituiscono lo strumento algebrico fondamentale per enumerare tutti i valori di verità assunti da una proposizione composta al variare delle combinazioni delle variabili di ingresso.

#### Negazione ($\neg P$)
L'operatore monadico inverte il valore di verità della proposizione:

| $P$ | $\neg P$ |
| :---: | :---: |
| V | F |
| F | V |

#### Congiunzione ($P \land Q$) e Disgiunzione Inclusiva ($P \lor Q$)
Per chiarire la semantica dei connettivi binari si consideri il vincolo imposto da un genitore a un figlio per poter uscire:
1. *Regola A:* "Lava i piatti **e** porta fuori l'immondizia" ($P \land Q$).
2. *Regola B:* "Lava i piatti **o** porta fuori l'immondizia" ($P \lor Q$).

Definendo $P =$ "il figlio lava i piatti" e $Q =$ "il figlio porta fuori l'immondizia", si ricavano le rispettive tavole:

| $P$ | $Q$ | $P \land Q$ | $P \lor Q$ |
| :---: | :---: | :---: | :---: |
| V | V | **V** | **V** |
| V | F | F | **V** |
| F | V | F | **V** |
| F | F | F | **F** |

- La congiunzione $P \land Q$ è vera **esclusivamente** se entrambi gli operandi sono veri; è falsa in ogni altro caso.
- La disgiunzione $P \lor Q$ è falsa **esclusivamente** se entrambi gli operandi sono falsi; è sufficiente che almeno una componente sia vera perché l'intera formula risulti vera.

> [!important] Convenzione Fondamentale sulla Disgiunzione
> Nel linguaggio naturale italiano la congiunzione "o" è spesso ambigua, potendo esprimere una scelta esclusiva (*aut-aut*, ad esempio "la luce è accesa o spenta"). La logica formale e la matematica adottano **esclusivamente la disgiunzione inclusiva** ($P \lor Q$ è vera anche se sia $P$ sia $Q$ sono simultaneamente vere). La disgiunzione esclusiva ($\text{XOR}$) viene esclusa dai connettivi primari per impedire ambiguità inferenziali.

---

## Implicazione ed Equivalenza Logica

### Implicazione Materiale ($P \Rightarrow Q$)

La proposizione condizionale $P \Rightarrow Q$ ("se $P$, allora $Q$") vincola logicamente la premessa (ipotesi) $P$ alla conclusione (tesi) $Q$.

Per comprenderne la tabella di verità, si consideri la promessa: *"Se oggi piove ($P$), allora resto a casa ($Q$)"*. In quale circostanza l'affermazione risulta palesemente tradita (falsa)?
- Se piove ($P$ vera) ma la persona esce di casa ($Q$ falsa), l'asserzione è smentita: l'implicazione è **falsa**.
- Se non piove ($P$ falsa), la promessa non vincola il comportamento: sia restare a casa sia uscire non violano l'enunciato di partenza.

Da ciò deriva la tavola di verità dell'implicazione materiale:

| $P$ | $Q$ | $P \Rightarrow Q$ |
| :---: | :---: | :---: |
| V | V | **V** |
| V | F | **F** |
| F | V | **V** |
| F | F | **V** |

L'implicazione è falsa **solo e soltanto quando l'ipotesi è vera e la tesi è falsa**. Da una premessa falsa segue logicamente qualsiasi conclusione: questo principio è noto come <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>ex falso quodlibet</b></font></mark> (da una premessa falsa segue qualunque asserzione mantenendo vera la proposizione condizionale).

> [!tip]- Flashcard: Implicazione Materiale e Falsificabilità
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Cloze
Text: L'implicazione materiale $P \implies Q$ è falsa {{c1::esclusivamente quando l'ipotesi $P$ è vera e la tesi $Q$ è falsa}}. In tutte le altre tre combinazioni di verità ($V \implies V$, $F \implies V$, $F \implies F$) l'implicazione è sempre {{c2::vera}}.
Extra: Principio "ex falso quodlibet": da una premessa falsa segue qualsiasi conclusione mantenendo vera la proposizione condizionale.
Tags: education/university education/math tech/logic
<!--ID: 1790260176601-->
END
%%

#### Condizione Necessaria vs Condizione Sufficiente
Nella proposizione condizionale $P \Rightarrow Q$:
- $P$ è <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>condizione sufficiente</b></font></mark> per $Q$: la verifica di $P$ basta a garantire la verità di $Q$.
- $Q$ è <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>condizione necessaria</b></font></mark> per $P$: se non si realizza $Q$, non può in alcun modo essersi verificata $P$ (se $Q$ è falsa, $P$ deve essere falsa affinché l'implicazione regga).

*Applicazione in Analisi 1:*
Nel teorema sulla convergenza delle serie numeriche:
$$\sum_{n=0}^{+\infty} a_n \text{ converge} \implies \lim_{n \to +\infty} a_n = 0$$
L'annullamento del termine generale ($\lim a_n = 0$) è condizione **necessaria** per la convergenza della serie, ma non è sufficiente (ad esempio per la serie armonica $\sum \frac{1}{n}$, dove il termine generale tende a zero ma la serie diverge).

> [!tip]- Flashcard: Condizione Necessaria vs Sufficiente
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Cloze
Text: Nella proposizione condizionale $A \implies B$, $A$ rappresenta una {{c1::condizione sufficiente}} per $B$, mentre $B$ rappresenta una {{c2::condizione necessaria}} per $A$.
Extra: Se non si verifica la condizione necessaria ($B$ è falsa), l'ipotesi $A$ non può essersi verificata. Se la serie converge ($A$), necessariamente il termine generale tende a zero ($B$).
Tags: education/university education/math tech/logic
<!--ID: 1790260176604-->
END
%%

### Equivalenza Logica ($P \Leftrightarrow Q$)

La relazione di equivalenza logica (o bicondizionale, "se e solo se") stabilisce che due proposizioni possiedono sempre il medesimo valore di verità:

| $P$ | $Q$ | $P \Leftrightarrow Q$ |
| :---: | :---: | :---: |
| V | V | **V** |
| V | F | F |
| F | V | F |
| F | F | **V** |

L'equivalenza corrisponde alla doppia implicazione logica:
$$(P \Leftrightarrow Q) \equiv (P \Rightarrow Q) \land (Q \Rightarrow P)$$
Nelle dimostrazioni matematiche, dimostrare una condizione necessaria e sufficiente ($P \iff Q$) richiede tassativamente di articolare la dimostrazione in due fasi:
1. Dimostrare che $P \implies Q$ (sufficienza).
2. Dimostrare che $Q \implies P$ (necessità).

---

## Leggi del Calcolo Proposizionale e Tautologie

Una <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>tautologia</b></font></mark> è una formula proposizionale sempre vera per qualsiasi attribuzione di valori di verità alle proposizioni che la compongono. Le leggi fondamentali del calcolo proposizionale costituiscono la base strutturale delle dimostrazioni:

### 1. Legge del Terzo Escluso (Tertium Non Datur)
$$P \lor (\neg P) \equiv V$$
Una proposizione è o vera o falsa: non esiste una terza possibilità logica.

### 2. Leggi di De Morgan
Regolano la distribuzione della negazione attraverso congiunzione e disgiunzione:
1. $\neg(P \land Q) \Leftrightarrow (\neg P) \lor (\neg Q)$
2. $\neg(P \lor Q) \Leftrightarrow (\neg P) \land (\neg Q)$

*Esempio interpretativo:*
Posto $P =$ "Giovanni è romano" e $Q =$ "Giovanni è uno studente":
- Negare la congiunzione "Giovanni è uno studente romano": significa che "Giovanni non è studente **oppure** non è romano".
- Negare la disgiunzione "Giovanni è studente o romano": significa che "Giovanni non è studente **e** non è romano".

> [!tip]- Flashcard: Leggi di De Morgan
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Cloze
Text: Enunciare le due leggi di De Morgan per la negazione di congiunzione e disgiunzione:
1. $\neg(P \land Q) \iff$ {{c1::(\neg P) \lor (\neg Q)}}
2. $\neg(P \lor Q) \iff$ {{c2::(\neg P) \land (\neg Q)}}
Extra: La negazione inverte il connettivo logico: la congiunzione ($\land$) diventa disgiunzione ($\lor$) e viceversa.
Tags: education/university education/math tech/logic
<!--ID: 1790260176606-->
END
%%

### 3. Legge della Contronominale (Contrapposizione Logica)
$$(P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P)$$
Un'implicazione diretta è logicamente equivalente alla sua implicazione contronominale, ottenuta scambiando ipotesi e tesi e negandole entrambe. Se è arduo dedurre $Q$ partendo da $P$, è possibile e formalmente equivalente assumere $\neg Q$ e dedurne $\neg P$.

> [!tip]- Flashcard: Legge della Contronominale
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Basic
Front: Come si formula la legge della contronominale (contrapposizione logica) e perché è utile nelle dimostrazioni?
Back: $$(P \implies Q) \iff (\neg Q \implies \neg P)$$
È fondamentale perché permette di sostituire la dimostrazione diretta di un teorema con la dimostrazione equivalente della sua contronominale, che spesso risulta algebricamente molto più semplice e trasparente da trattare.
Tags: education/university education/math tech/logic
<!--ID: 1790260176607-->
END
%%

### 4. Schema di Dimostrazione per Assurdo
$$(P \Rightarrow Q) \Leftrightarrow [(P \land \neg Q) \Rightarrow (R \land \neg R)]$$
Poiché $R \land \neg R$ è una **contraddizione** (proposizione sempre falsa), se assumendo contemporaneamente l'ipotesi $P$ e la negazione della tesi $\neg Q$ si deduce una contraddizione logica, allora l'assunzione $\neg Q$ è insostenibile e la tesi $Q$ deve essere necessariamente vera.

---

## Logica dei Predicati del Primo Ordine

Il calcolo proposizionale analizza le proposizioni come blocchi indivisibili. Per esprimere affermazioni che coinvolgono proprietà matematiche, insiemi ed elementi variabili, è necessario estendere il linguaggio alla <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>logica dei predicati</b></font></mark>.

### Definizione di Predicato e Proposizioni Aperte

Un <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>predicato</b></font></mark> $P(x)$ è un'asserzione che contiene una o più variabili ($x, y, \dots$) appartenenti a un prefissato dominio. Il suo valore di verità non è assegnabile a priori, ma dipende dal valore attribuito alla variabile.

- In $x + 3 = 7$, l'espressione è vera se $x = 4$ e falsa per ogni $x \neq 4$.
- In "$x$ è un numero primo", la verità varia al variare di $x \in \mathbb{N}$.

Un predicato con variabili non quantificate costituisce una **proposizione aperta**.

### Quantificatori: Universale ed Esistenziale

Per trasformare una proposizione aperta in una **proposizione chiusa** (avente valore di verità assoluto nel dominio) si introducono i <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>quantificatori logici</b></font></mark>:

1. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Quantificatore Universale ($\forall$)</b></font></mark>: si legge "per ogni", "per qualunque".
   $$\forall x : P(x) \quad \text{oppure} \quad (\forall x)(P(x))$$
   Afferma che la proprietà $P(x)$ è soddisfatta da ogni elemento del dominio di riferimento.
2. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Quantificatore Esistenziale ($\exists$)</b></font></mark>: si legge "esiste almeno un", "esiste".
   $$\exists x : P(x) \quad \text{oppure} \quad (\exists x)(P(x))$$
   Afferma che nel dominio esiste almeno un elemento che soddisfa la proprietà $P(x)$.

### Campo d'Azione, Variabili Libere e Legate

- **Campo d'Azione:** La porzione di formula logica su cui il quantificatore esercita la propria portata semantica. In $(\forall x)(P(x) \Rightarrow Q(x))$, l'intera implicazione ricade sotto il raggio d'azione di $\forall x$.
- **Variabile Libera:** Una variabile presente in una formula non preceduta da un quantificatore che ne delimiti il raggio.
- **Variabile Legata:** Una variabile vincolata da un quantificatore.

*Esempi di legame:*
- In $x + 3 \le 7$, la variabile $x$ è **libera** (proposizione aperta).
- In $(\forall x)(x + 3 \le y)$, la variabile $x$ è **legata** al quantificatore universale, mentre la variabile $y$ è **libera**. L'intera espressione rimane aperta finché non viene quantificata o assegnata anche la variabile $y$.

---

## Leggi della Quantificazione e Formule Complesse

### Dualità e Negazione dei Quantificatori

Quando la negazione interagisce con i quantificatori, scambia la natura del quantificatore e sposta la negazione all'interno della proprietà:

1. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Negazione dell'Universale:</b></font></mark>
   $$\neg (\forall x : P(x)) \Longleftrightarrow \exists x : \neg P(x)$$
   Negare che una proprietà valga per tutti gli elementi equivale ad asserire che esiste almeno un elemento per cui la proprietà fallisce (controesempio).
2. <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Negazione dell'Esistenziale:</b></font></mark>
   $$\neg (\exists x : P(x)) \Longleftrightarrow \forall x : \neg P(x)$$
   Negare che esista almeno un elemento con tale proprietà equivale ad affermare che per tutti gli elementi la proprietà non sussiste.

*Esempio didattico:*
Sia $P(x) =$ "$x$ indossa una maglietta rossa" tra gli studenti di un'aula:
- $\forall x : P(x) =$ "Tutti gli studenti indossano una maglietta rossa".
- Negazione: $\neg(\forall x : P(x)) \equiv$ "C'è almeno uno studente che non indossa una maglietta rossa" $\equiv \exists x : \neg P(x)$.
- $\exists x : P(x) =$ "Esiste almeno uno studente con la maglietta rossa".
- Negazione: $\neg(\exists x : P(x)) \equiv$ "Nessuno studente indossa una maglietta rossa" $\equiv \forall x : \neg P(x)$.

> [!tip]- Flashcard: Negazione dei Quantificatori
%%
TARGET DECK: University::Fondamenti di Matematica Analisi 1
START
Cloze
Text: Sotto l'effetto della negazione logica, i quantificatori si trasformano secondo le regole di dualità:
- $\neg(\forall x : P(x)) \iff$ {{c1::\exists x : \neg P(x)}}
- $\neg(\exists x : P(x)) \iff$ {{c2::\forall x : \neg P(x)}}
Extra: Negare una proprietà universale equivale a trovare almeno un controesempio; negare una proprietà esistenziale equivale ad affermare che la negazione vale per tutti.
Tags: education/university education/math tech/logic
<!--ID: 1790260176608-->
END
%%

### Quantificatori Multipli e Dipendenze tra Variabili

Quando compaiono quantificatori diversi, **l'ordine di scrittura è vincolante e non commutabile**. Si consideri il predicato a due variabili:
$$P(x, y) = \text{"L'impiegato } x \text{ dell'azienda } A \text{ è in grado di svolgere la mansione } y \text{"}$$

Le diverse combinazioni quantificate esprimono scenari organizzativi radicalmente differenti:

1. $(\forall x)(\exists y) P(x, y)$: "Per ogni impiegato esiste almeno una mansione che sa svolgere" (ogni lavoratore è occupabile e non inutile).
2. $(\exists x)(\forall y) P(x, y)$: "Esiste un impiegato capace di svolgere ogni mansione aziendale" (esiste un profilo universale o tuttologo).
3. $(\forall y)(\exists x) P(x, y)$: "Per ogni mansione esiste almeno un impiegato in grado di svolgerla" (nessun compito aziendale rimane scoperto).
4. $(\exists y)(\forall x) P(x, y)$: "Esiste una mansione che qualunque impiegato è in grado di eseguire" (compito elementare condiviso).

#### Negazione a Cascata di Formule Annidate
Applicando le leggi di De Morgan ai quantificatori a cascata, ogni negazione inverte il quantificatore immediatamente adiacente e avanza:
$$\neg [(\forall y)(\exists x) P(x, y)] \Longleftrightarrow (\exists y) \neg [(\exists x) P(x, y)] \Longleftrightarrow (\exists y)(\forall x) \neg P(x, y)$$
L'asserzione "Non per ogni mansione c'è un lavoratore capace" equivale formalmente a "Esiste una mansione che nessun lavoratore è in grado di svolgere".

---

## Metodi di Dimostrazione: Esempio della Contronominale

Nelle dimostrazioni matematiche di teoremi strutturati come $\forall x : (P(x) \Rightarrow Q(x))$, la via diretta può risultare algebricamente impraticabile. La <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>dimostrazione per contrapposizione</b></font></mark> sfrutta l'equivalenza logica:
$$(\forall x)(P(x) \Rightarrow Q(x)) \Longleftrightarrow (\forall x)(\neg Q(x) \Rightarrow \neg P(x))$$

### Problema Esemplare
> Dimostrare che per ogni intero positivo $x \in \mathbb{N}^+$, se $x^2$ è pari allora $x$ è pari:
> $$(\forall x \in \mathbb{N}^+)\left(x^2 \text{ è pari} \implies x \text{ è pari}\right)$$

### Analisi delle Difficoltà della Prova Diretta
Nel tentativo di dimostrazione diretta si assume l'ipotesi: $x^2 = 2m$ con $m \in \mathbb{N}$. Da ciò discende $x = \sqrt{2m}$, espressione irrazionale che non fornisce informazioni immediate sulla parità di $x$ senza presupporre già teoremi sui fattori primi.

### Risoluzione Tramite Contronominale
1. **Identificazione delle componenti:**
   - Ipotesi $P(x): x^2 \text{ è pari}$
   - Tesi $Q(x): x \text{ è pari}$
2. **Formulazione della contronominale ($\neg Q(x) \Rightarrow \neg P(x)$):**
   - Negazione della tesi $\neg Q(x): x \text{ è dispari}$ (nell'insieme degli interi un numero non pari è dispari).
   - Negazione dell'ipotesi $\neg P(x): x^2 \text{ è dispari}$.
   - Proposizione da dimostrare:
     $$(\forall x \in \mathbb{N}^+)\left(x \text{ è dispari} \implies x^2 \text{ è dispari}\right)$$
3. **Sviluppo Algebrico:**
   - Se $x$ è dispari, per definizione esiste un numero naturale $n \in \mathbb{N}$ tale che:
     $$x = 2n + 1$$
   - Eleviamo $x$ al quadrato sviluppando il binomio:
     $$x^2 = (2n + 1)^2 = 4n^2 + 4n + 1$$
   - Raccogliamo il fattore $2$ dai primi due termini:
     $$x^2 = 2(2n^2 + 2n) + 1$$
   - Poiché $n \in \mathbb{N}$, la quantità $k = 2n^2 + 2n$ appartiene anch'essa a $\mathbb{N}$. Possiamo dunque riscrivere:
     $$x^2 = 2k + 1 \quad \text{con } k \in \mathbb{N}$$
4. **Conclusione:**
   La quantità $x^2$ soddisfa la forma canonica dei numeri dispari ($2k+1$). Risulta dunque dimostrata l'implicazione contronominale ($x \text{ dispari} \implies x^2 \text{ dispari}$). Per la legge di contrapposizione, è rigorosamente provata l'asserzione di partenza: se $x^2$ è pari, allora $x$ è pari.

---

## Direttive Metacognitive

Secondo il framework di apprendimento metodologico [[Metodo di Studio - PACRAR]] di Alessandro de Concini:
1. **Pianificazione & Acquisizione (P-A):** Nella prima settimana di lezione, la logica formale funge da alfabeto. Non limitarsi a memorizzare i simboli, ma esercitarsi nella traduzione bidirezionale tra espressioni verbali e formule simboliche.
2. **Comprensione Profonda (C):** Riconoscere la differenza cruciale tra *condizione necessaria* e *condizione sufficiente*. Nei teoremi di Analisi 1 (convergenza di successioni e serie, continuità, derivabilità), identificare sempre con precisione quale sia la direzione dell'implicazione per evitare errori concettuali sistematici (es. confondere la condizione necessaria $\lim a_n = 0$ con una sufficienza per la convergenza).
3. **Rielaborazione (R):** Sviluppare le dimostrazioni per contrapposizione e per assurdo esplicitando sempre la struttura logica: definire $P$, definire $Q$, enunciare $\neg Q \implies \neg P$, ed eseguire il passaggio algebrico.
4. **Applicazione & Revisione Attiva (A-R):** Utilizzare le flashcard Anki contestuali sopra strutturate a intervalli distanziati per rendere automatico il cambio dei quantificatori nelle negazioni, abilità indispensabile per comprendere la negazione della definizione di limite ($\varepsilon$-$\delta$) nelle lezioni successive.
