---
status: permanent
type: lecture
area: education
related: ["[[Introduzione alla Programmazione MOC]]", "[[Ingegneria Informatica 2026 - 27 MOC]]", "[[University]]", "[[Metodo di Studio - PACRAR]]"]
aliases: ["Lezione 1 Introduzione alla Programmazione", "Programmazione Lezione 1", "Elaborazione delle Informazioni, Algoritmi e Introduzione a Python"]
source: Lezione 1 Introduzione alla Programmazione del 23/09/2026 - Canale 1 e 2
title: "01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python"
date: '2026-09-24'
updated: 2026-09-27T18:00
tags: [education/university, tech/programming, tech/python, tech/cs]
summary: "Sistemi di elaborazione, algoritmi e raffinamenti successivi, architettura di von Neumann, esecuzione bytecode e PVM in Python e uso critico degli LLM."
course: "Introduzione alla Programmazione"
sources: ["[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf]]", "[[Thinking Fast Slow and Artificial - How AI is Reshaping Human Reasoning.pdf]]"]
---
[[Home MOC|Home]] / [[University|University MOC]] / [[Introduzione alla Programmazione MOC]] / [[01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python]]

# 01 - Elaborazione delle Informazioni, Algoritmi e Introduzione a Python

- **Docente:** Prof. [[Giuseppe Santucci]]
- **Data Lezione:** 2026-09-23
- **Materiali Didattici:**
  - [[Introduzione alla Programmazione - Lezione 01 - Slide.pdf|Slide Ufficiali — Lezione 01]]
  - [[Thinking Fast Slow and Artificial - How AI is Reshaping Human Reasoning.pdf|Paper Scientifico Wharton — Shaw & Nave (2026)]]

## Quadro Concettuale e Obiettivi della Lezione

L'avvio dello studio dell'ingegneria informatica richiede una premessa epistemologica fondamentale: l'informatica non si identifica con lo studio del calcolatore elettronico in quanto macchina, esattamente come l'astronomia non coincide con lo studio dei telescopi né la biologia con quello dei microscopi. Essa costituisce la disciplina scientifica che analizza la rappresentazione, la manipolazione e l'<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>elaborazione automatica delle informazioni</b></font></mark> finalizzata alla risoluzione sistematica di problemi (*problem solving* computazionale).

Da un punto di vista storico, la disciplina affonda le proprie radici nella convergenza di due grandi ambiti:
1. **La matrice matematico-logica:** avviata tra gli anni Trenta e Quaranta da logici e matematici quali Alan Turing, Alonzo Church e Kurt Gödel, che hanno definito i fondamenti teorici della computabilità e delle macchine universali.
2. **La matrice ingegneristica:** sviluppata mediante le tecnologie circuitali ed elettroniche che hanno consentito la costruzione di dispositivi fisici capaci di compiere computazioni discrete ad altissima frequenza.

Il percorso formativo del corso unisce quindi due anime complementari: la programmazione applicata in linguaggio Python e i modelli teorici dell'architettura e della rappresentazione dei dati \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=7|Slide 7-10]]].

> [!summary] Percorso Concettuale della Lezione
> - [d] **Sistemi di Elaborazione:** Definizione di calcolatore, hardware, software e frequenza operativa
> - [d] **Algoritmo vs Programma:** Proprietà formali (non ambiguità, effettività, terminazione) e generalità dei dati
> - [d] **Raffinamenti Successivi:** Dalla specifica astratta allo pseudocodice e all'implementazione del MCD
> - [d] **Stratificazione Software:** Ruolo del Sistema Operativo come intermediario tra applicazioni e risorse hardware
> - [d] **Architettura di von Neumann:** CPU (ALU, CU, registri), memoria centrale RAM, BUS e dispositivi di I/O
> - [d] **Modelli di Traduzione:** Compilazione monolitica vs interpretazione riga per riga
> - [d] **Il Linguaggio Python:** Origini, multi-paradigma, tipizzazione forte dinamica, Garbage Collection, bytecode e PVM
> - [d] **Metodologia con LLM:** La Tri-System Theory, prevenzione della *Cognitive Surrender* e regole pratiche di apprendimento

---

## Sistemi di Elaborazione delle Informazioni: Hardware e Software

Un <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>sistema di elaborazione delle informazioni</b></font></mark> è un insieme organizzato di risorse tecnologiche predisposto per raccogliere dati dall'ambiente esterno (ingresso o *input*), memorizzarli, elaborarli secondo sequenze ordinate di comandi e restituire informazioni elaborate (uscita o *output*).

La struttura di qualsiasi calcolatore poggia su una fondamentale dualità ontologica:

| Componente | Natura | Ruolo nel Sistema | Esempi Concreti |
| :--- | :--- | :--- | :--- |
| **Hardware (HW)** | Fisico / Tangibile | Dispositivi elettronici e meccanici che compiono materialmente le commutazioni binarie. | CPU, banchi di memoria RAM, circuiti integrati, schermi, bus di sistema. |
| **Software (SW)** | Logico / Intangibile | Programmi e dati codificati che governano il comportamento operativo dell'hardware. | Sistemi operativi, interpreti, compilatori, applicazioni e script utente. |

### Frequenza Operativa e Natura Atomica delle Istruzioni

Il calcolatore esegue internamente operazioni logico-aritmetiche primitive su sequenze binarie. La sua straordinaria capacità di calcolo non risiede nella complessità delle singole istruzioni, bensì nella **velocità estrema** con cui esse vengono completate. Una frequenza operativa di $3\text{ GHz}$ corrisponde a circa 3 miliardi di cicli operativi elementari al secondo. Qualsiasi applicativo complesso è il risultato della composizione gerarchica di miliardi di queste micro-operazioni atomiche.

\[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=28|Slide 28-29]]]

> [!tip]- Flashcard: Definizione di Informatica e Ruolo del Calcolatore
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Qual è la definizione fondativa dell'informatica come disciplina scientifica e come si colloca il calcolatore rispetto ad essa?
Back: L'informatica è lo studio sistematico della rappresentazione, manipolazione e risoluzione automatica dei problemi (*problem solving*) mediante procedimenti algoritmici. Il calcolatore non costituisce l'oggetto primario di studio, bensì lo strumento esecutivo automatico ad altissima velocità utilizzato per concretizzare tali processi computazionali.
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114755-->
END
%%

---

## Teoria dell'Algoritmo e Risoluzione dei Problemi

Nel ciclo di risoluzione di un problema mediante elaboratore, la riflessione logica precede obbligatoriamente la stesura del codice:
$$\text{Problema} \longrightarrow \text{Algoritmo} \longrightarrow \text{Programma}$$

### La Distinzione tra Algoritmo e Programma

- **<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Algoritmo</b></font></mark>:** Procedimento di calcolo astratto, costituito da una sequenza finita, ordinata e deterministica di passi, che prescrive le operazioni necessarie per trasformare un insieme valido di dati di ingresso nei corrispondenti dati di uscita.
- **<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Programma</b></font></mark>:** Realizzazione concreta e tangibile di un algoritmo, codificata mediante le regole sintattiche di un linguaggio di programmazione, direttamente o indirettamente eseguibile da un elaboratore.

![[Schema - Risoluzione di un Problema ed Elaborazione.png]]
*(Flusso di risoluzione di un problema: rif. \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=34|Slide 34]]])*

### Le Tre Proprietà Necessarie di un Algoritmo

Per essere considerato tale, un procedimento deve soddisfare congiuntamente tre proprietà formali \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=36|Slide 36]]]:

1. **Non Ambiguità (Determinatezza):** Ciascuna operazione deve essere definita in modo univoco, escludendo ogni margine di interpretazione soggettiva. Frasi come "mescolare a sufficienza" sono prive di valore algoritmico; l'operazione deve essere parametrizzata con precisione oggettiva.
2. **Eseguibilità (Effettività):** Ciascun singolo passo deve essere atomicamente realizzabile dall'esecutore meccanico con risorse e in tempi finiti.
3. **Terminazione (Finitudine):** La computazione deve obbligatoriamente concludersi dopo un numero finito di operazioni per qualsiasi insieme ammesso di dati in ingresso. Un procedimento che incorra in un ciclo infinito senza fine non è un algoritmo corretto.

### Principio di Generalità del Software

I programmi non vengono progettati per risolvere una singola circostanza isolata, bensì un'intera classe universale di problemi. In un'applicazione di calcolo di percorsi stradali, il software non modella unicamente il tragitto tra due vie note, ma riceve come **dati di ingresso** le coordinate generiche di partenza e destinazione, fornendo una risposta riutilizzabile in qualunque contesto.

### Tecnica dei Raffinamenti Successivi (Top-Down Refinement)

La formalizzazione di un algoritmo si sviluppa per gradi di dettaglio progressivi \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=37|Slide 37]]]:
1. **Specifica Informale:** Descrizione macroscopica in linguaggio naturale.
2. **Pseudocodice:** Formulazione strutturata che impiega blocchi logici standard (condizioni, iterazioni), libera dai rigidi vincoli di sintassi di uno specifico compilatore \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=38|Slide 38]]].
3. **Codifica Esecutiva:** Trasposizione fedele dello pseudocodice nel linguaggio di programmazione prescelto.

> [!example] Caso di Studio: Calcolo del Massimo Comun Divisore ($\mathrm{MCD}$) tra Interi Positivi $m, n$
> 
> **Fase 1: Formulazione Astratta**
> 1. Calcola l'insieme $A$ di tutti i divisori di $m$.
> 2. Calcola l'insieme $B$ di tutti i divisori di $n$.
> 3. Calcola l'insieme intersezione $C = A \cap B$ (divisori comuni).
> 4. Estrai il valore massimo appartenente a $C$.
> 
> **Fase 2: Raffinamento in Pseudocodice (Calcolo dell'insieme $A$)**
> ```text
> Inizializza A come insieme vuoto
> Per ciascun numero intero k compreso tra 1 ed m:
>     Se m è divisibile per k (m modulo k == 0):
>         Aggiungi k all'insieme A
> Restituisci A
> ```
> 
> **Fase 3: Codice Python Concreto \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=39|Slide 39-40]]]**
> ```python
> m = 1457
> n = 62
> 
> A = set()
> for i in range(1, m + 1):
>     if m % i == 0:
>         A.add(i)
> 
> B = set()
> for j in range(1, n + 1):
>     if n % j == 0:
>         B.add(j)
> 
> C = A.intersection(B)
> mcd = max(C)
> print("MCD:", mcd)
> ```

> [!tip]- Flashcard: Proprietà Fondative dell'Algoritmo
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Quali sono le tre proprietà formali necessarie affinché una sequenza di istruzioni sia definibile come algoritmo?
Back: 1. **Non ambiguità (determinatezza):** ogni passo deve avere un significato univoco e privo di discrezionalità soggettiva; 2. **Eseguibilità (effettività):** ogni operazione deve essere concretamente realizzabile dall'esecutore in un intervallo di tempo finito; 3. **Terminazione (finitudine):** la computazione deve necessariamente arrestarsi dopo un numero finito di passi per qualsiasi dato di ingresso valido.
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114756-->
END
%%

---

## Stratificazione Software e Ruolo del Sistema Operativo

Nei calcolatori moderni, i programmi applicativi sviluppati dagli utenti non interagiscono direttamente con l'hardware sottostante. L'architettura è strutturata a livelli di astrazione gerarchici:

![[Schema - Applicazioni e Sistema Operativo.png]]
*(Rapporto tra Applicazioni, Sistema Operativo e Hardware: rif. \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=41|Slide 41]]])*

Il <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>sistema operativo</b></font></mark> (OS) è il livello di software che gestisce direttamente l'hardware fisico, garantendo un utilizzo corretto, trasparente ed efficiente delle risorse di sistema.

### Il Principio del Disaccoppiamento dell'Astrazione

Senza il sistema operativo, ogni programmatore dovrebbe scrivere codice capace di pilotare i singoli registri dei controllori hardware, con conseguenze critiche:
- Un software scritto per un calcolatore con una certa dimensione di RAM o un particolare chip grafico non potrebbe funzionare su un modello differente.
- L'OS elimina questo vincolo: espone interfacce logiche uniformi (*system call*), traducendo le richieste delle applicazioni nelle istruzioni circuitali appropriate per i dispositivi montati sulla macchina specifica.

> [!tip]- Flashcard: Ruolo e Principio del Sistema Operativo
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Perché il Sistema Operativo funge da strato di disaccoppiamento tra applicazioni software e hardware fisico?
Back: Perché isola e astrae l'estrema eterogeneità dei dispositivi fisici. Senza il sistema operativo, ogni applicazione dovrebbe gestire direttamente i dettagli circuitali di ogni specifica CPU, memoria o controller, rendendo impossibile la portabilità del software. L'OS riceve comandi logici standardizzati e si occupa della loro corretta ed efficiente traduzione fisica sull'hardware specifico.
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114757-->
END
%%

---

## Architettura dei Calcolatori: Il Modello di von Neumann

La quasi totalità dei calcolatori elettronici per uso generale adotta l'architettura concettuale teorizzata da John von Neumann nel 1945 \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=10|Slide 10]]]. Il principio fondativo è il **programma memorizzato**: i dati numerici e le istruzioni esecutive del programma risiedono all'interno del medesimo supporto di memorizzazione (la memoria centrale) e condividono la medesima codifica binaria.

### Componenti Principali dell'Architettura

| Sottosistema | Componenti Interne | Funzione Principale nel Modello |
| :--- | :--- | :--- |
| **CPU (Processore)** | **Control Unit (CU)**<br>**ALU (Calcolo)**<br>**Registri Interni** | Coordina il ciclo macchina *Fetch-Decode-Execute*, compie le operazioni aritmetico-logiche booleane e conserva operandi immediati nei registri sub-nanosecondo. |
| **Memoria Centrale (RAM)** | Celle binarie indirizzabili | Memoria volatile ad accesso casuale ad alta velocità; ospita obbligatoriamente sia il codice del programma che i dati durante l'esecuzione attiva. |
| **Memorie Secondarie** | Dischi fissi, SSD | Supporti magnetici o a stato solido non volatili a capacità elevata per la persistenza a lungo termine dei file. |
| **Dispositivi di I/O** | Tastiera, mouse, display, schede di rete | Interfacce di ingresso per acquisire segnali esterni e di uscita per restituire dati all'utente. |
| **BUS di Sistema** | Bus Dati, Bus Indirizzi, Bus Controllo | Fascio di piste elettriche ad alta frequenza che connette tutte le unità per il transito simultaneo di segnali e comandi. |

### Ciclo Operativo di Esecuzione

All'avvio di un programma, il file eseguibile memorizzato sul disco secondario viene trasferito dal sistema operativo nella memoria RAM. Da questo momento, la CPU preleva e scandisce sequenzialmente le istruzioni:
1. **Fetch:** Prelievo dell'istruzione dalla locazione di memoria RAM puntata dal contatore di programma.
2. **Decode:** Decodifica del codice operativo da parte della Control Unit.
3. **Execute:** Esecuzione del comando mediante l'ALU o movimentazione dei registri, con eventuale scrittura dei risultati in memoria.

> [!tip]- Flashcard: Modello di von Neumann e Programma Memorizzato
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Qual è l'innovazione concettuale fondamentale introdotta dal modello della Macchina di von Neumann del 1945?
Back: L'introduzione del principio del programma memorizzato: le istruzioni del programma da eseguire e i dati numerici su cui operare risiedono all'interno del medesimo spazio d'indirizzamento della memoria centrale (RAM) e sono entrambi codificati in formato binario, superando i calcolatori a cablaggio fisso o a schede esterne.
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114758-->
END
%%

---

## Il Processo di Traduzione: Compilazione vs Interpretazione

I processori comprendono esclusivamente il <mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>linguaggio macchina</b></font></mark>, costituito da sequenze binarie codificate dipendenti dalla specifica architettura della CPU \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=42|Slide 42]]]. I linguaggi ad alto livello orientati alla leggibilità umana richiedono un processo di traduzione, articolato storicamente in due approcci:

### 1. Compilatore \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=44|Slide 44-45]]]
Il compilatore esamina il programma sorgente nella sua totalità e genera un file eseguibile binario autonomo, collegando il programma tradotto con le librerie esterne mediante la fase di *linking*.

![[Schema - Il Processo di Compilazione.png]]
*(Fasi del processo di compilazione: sorgente, traduttore, linker ed eseguibile: rif. \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=45|Slide 45]]])*

- **Vantaggi:** Massima velocità computazionale in fase di esecuzione.
- **Svantaggi:** Assenza di portabilità diretta (il binario prodotto è vincolato all'architettura hardware e al sistema operativo su cui è stato compilato).

### 2. Interprete
L'interprete legge il codice sorgente riga per riga, traducendo ed eseguendo ciascuna istruzione al volo durante il ciclo runtime.
- **Vantaggi:** Massima portabilità e flessibilità nello sviluppo interattivo.
- **Svantaggi:** Marcato rallentamento prestazionale dovuto alla continua decodifica delle istruzioni.

> [!tip]- Flashcard: Compilatore vs Interprete
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Qual è la differenza strutturale tra il modello di compilazione e quello di interpretazione di un linguaggio di programmazione?
Back: Il compilatore traduce l'intero codice sorgente in blocco in un file eseguibile binario autonomo in linguaggio macchina prima dell'esecuzione (massima velocità, ma binario vincolato a una specifica architettura HW/OS). L'interprete traduce ed esegue il codice istruzione per istruzione a runtime (portabilità elevata e flessibilità, ma con un significativo overhead prestazionale).
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114759-->
END
%%

---

## Il Linguaggio Python: Filosofia, Caratteristiche e Modello d'Esecuzione

### Genesi Storica e Filosofia di Progetto

Python è stato creato a cavallo tra gli anni Ottanta e Novanta dal programmatore olandese Guido van Rossum presso il CWI di Amsterdam \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=48|Slide 48]]]. Il nome è un tributo al celebre gruppo comico britannico dei *Monty Python* e alla trasmissione *Monty Python’s Flying Circus* \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=49|Slide 49]]].

Al medesimo immaginario è legata l'origine informatica del termine **spam**: il celebre sketch comico in cui ogni piatto servito nella taverna contiene immancabilmente carne in scatola "Spam" ha ispirato l'adozione del vocabolo per indicare messaggi non richiesti e ripetitivi.

Guido van Rossum è stato per quasi trent'anni il *Benevolent Dictator For Life* (BDFL) del linguaggio; dal 2018 la guida è affidata a uno Steering Council collegiale. Python è un software libero, gratuito e aperto \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=50|Slide 50]]].

### Caratteristiche del Linguaggio

1. **Linguaggio Multi-Paradigma:** Supporta in modo integrato programmazione imperativa, orientata agli oggetti e costrutti di tipo funzionale \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=51|Slide 51]]].
2. **Tipizzazione Forte e Dinamica (*Strong Dynamically Typed*):** Le variabili non richiedono dichiarazione esplicita del tipo (il tipo è proprietà del valore a runtime), ma l'interprete impedisce conversioni implicite incoerenti tra tipi non compatibili.
3. **Gestione Automatica della Memoria (<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Garbage Collection</b></font></mark>):** La liberazione della memoria per oggetti non più utilizzati è gestita in background dal sistema mediante conteggio dei riferimenti e spazzamento dei cicli \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=52|Slide 52]]].
4. **Batteries Included:** La libreria standard include una vastissima dotazione di moduli integrati per manipolazione dati, matematica, formati file e comunicazioni di rete.

### Il Modello Pseudo-Compilato: Bytecode e Python Virtual Machine (PVM)

Python adotta un'architettura di esecuzione ibrida a due stadi \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=53|Slide 53]]]:

1. **Pre-compilazione in <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Bytecode</b></font></mark>:**
   - I file di testo sorgente `.py` vengono analizzati dal controllore sintattico.
   - Se il codice rispetta le regole grammaticali, viene tradotto in un formato intermedio compatto e indipendente dall'hardware: il **bytecode**.
   - Il bytecode viene salvato in file `.pyc` (nella cartella `__pycache__`) per consentire il riutilizzo immediato nelle esecuzioni successive senza dover ripetere la verifica sintattica.
2. **Esecuzione tramite la <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Python Virtual Machine (PVM)</b></font></mark>:**
   - La PVM è un'applicazione reale che emula il funzionamento di una CPU virtuale.
   - Legge il bytecode istruzione per istruzione e lo interpreta traducendolo nelle chiamate appropriate per il sistema operativo sottostante.

![[Interpretazione di un Programma Python.png]]
*(Dettaglio del flusso di traduzione ed esecuzione: rif. \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=55|Slide 55]]])*

### Distinzione tra Errori Sintattici ed Errori a Runtime

Il modello a due stadi determina una netta distinzione tra le fasi di errore:
- **Errori di Sintassi (`SyntaxError`):** Rilevati a monte durante la fase di pre-compilazione; impediscono la generazione del bytecode e bloccano completamente l'avvio della PVM.
- **Eccezioni a Runtime (`RuntimeError`, `TypeError`, `ZeroDivisionError`):** Rilevate durante l'esecuzione del bytecode da parte della PVM a seguito di un'operazione non ammessa (es. divisione per zero o accesso a indice inesistente).

### Modalità di Esecuzione e Spyder IDE

L'interazione con l'interprete Python può avvenire attraverso due canali principali \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=58|Slide 58-60]]]:
- **Modalità Interattiva (Shell / REPL):** Esegue un comando alla volta restituendo subito l'output (ad es. `print(5*3)`). È ideale per verifiche atomiche e collaudi immediati, ma le istruzioni non vengono salvate.
- **Esecuzione di Script (File `.py`):** Il codice viene scritto e salvato in file testuali riutilizzabili e modificabili nel tempo (es. `hello.py`).

L'ambiente di sviluppo di riferimento per il corso è l'**IDE Spyder** (`https://www.spyder-ide.org/`) \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=14|Slide 14]]], che integra in un'unica schermata l'editor di testo per gli script, la console interattiva IPython e l'esploratore delle variabili per ispezionare lo stato della memoria.

> [!tip]- Flashcard: Modello a Due Stadi di Python (Bytecode e PVM)
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Come si articola il modello di esecuzione pseudo-compilato di Python attraverso bytecode e PVM?
Back: Il codice sorgente `.py` viene analizzato dal controllore sintattico e tradotto in un linguaggio intermedio astratto indipendente dall'hardware denominato **bytecode** (salvato opzionalmente in file `.pyc`). Successivamente, la **Python Virtual Machine (PVM)** interpreta ed esegue il bytecode istruzione per istruzione interfacciandosi con il sistema operativo della macchina reale.
Tags: education/university tech/programming tech/python
<!--ID: 1790280114760-->
END
%%

---

## Metodologia di Studio e Intelligenza Artificiale: Evitare la Cognitive Surrender

Un elemento metodologico cardine affrontato a lezione riguarda l'uso degli strumenti di intelligenza artificiale generativa (LLM, quali ChatGPT, Claude, Gemini, Copilot) durante lo studio della programmazione.

Gli LLM sono strumenti di lavoro ormai ubiqui con cui è essenziale imparare a confrontarsi; tuttavia, la programmazione è una competenza che si costruisce esclusivamente affrontando in prima persona la fatica della logica, della sintassi e del debugging.

### La Tri-System Theory e il Rischio di Resa Cognitiva (*Cognitive Surrender*)

Nello studio scientifico dei ricercatori Steven D. Shaw e Gideon Nave (*The Wharton School, University of Pennsylvania*), intitolato *Thinking—Fast, Slow, and Artificial: How AI is Reshaping Human Reasoning and the Rise of Cognitive Surrender* \[[[Thinking Fast Slow and Artificial - How AI is Reshaping Human Reasoning.pdf|Paper di Riferimento]]], il classico modello a due sistemi cognitivi di Daniel Kahneman viene esteso per comprendere l'interazione uomo-macchina:

| Sistema Cognitivo | Natura | Modalità di Funzionamento | Ruolo nell'Apprendimento |
| :--- | :--- | :--- | :--- |
| **Sistema 1** | Biologico | Rapido, intuitivo, associativo, automatico a basso costo energetico. | Genera euristiche immediate ma non strutturate. |
| **Sistema 2** | Biologico | Lento, deliberativo, analitico, riflessivo e ad alto dispendio cognitivo. | Responsabile dell'astrazione logica, della formalizzazione algoritmica e del controllo critico. |
| **Sistema 3** | Artificiale | Inferenza statistica su larga scala (LLM, assistenti generativi). | Strumento esterno di supporto cognitivo; se usato passivamente, induce resa e atrofia del Sistema 2. |

Il rischio primario evidenziato dai ricercatori è la cosiddetta <mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Cognitive Surrender</b></font></mark> (resa cognitiva). Quando uno studente delega la scrittura o la risoluzione di un esercizio a un LLM:
1. Il Sistema 3 fornisce una soluzione pronta e apparentemente valida.
2. Il **Sistema 2 viene bypassato e disattivato**: lo studente evita lo sforzo cognitivo della scomposizione top-down e della ricerca dell'errore.
3. Si instaura una falsa sensazione di comprensione (*fluency illusion*): leggere una soluzione funzionante fa credere di aver compreso il procedimento, ma non allena le connessioni logiche necessarie per impostare autonomamente il codice durante l'esame.

### I Tre Usi Virtuosi degli LLM nello Studio della Programmazione

Nello studio universitario, l'LLM deve agire come un tutor socratico finalizzato all'apprendimento attivo, non come un esecutore passivo \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=19|Slide 19-22]]]:

1. **Farsi spiegare il codice:** Chiedere chiarimenti riga per riga su frammenti ostici delle dispense, analizzando la motivazione per cui un costrutto o un ciclo si comporta in modo inatteso.
2. **Generare varianti di un problema:** Risolto autonomamente un esercizio, chiedere all'LLM di proporre una variante con vincoli o strutture dati modificate, affrontandola da soli prima di verificare eventuali riscontri.
3. **Farsi generare esercizi su misura:** Usare il modello come generatore illimitato di problemi a difficoltà incrementale su costrutti specifici (liste, cicli, funzioni), da risolvere rigorosamente a libro chiuso.

### La Regola di Autonomia Cognitiva

> [!important] Criterio di Validazione PACRAR
> **Se dopo aver consultato l'LLM non sei in grado di riscrivere una soluzione simile da solo, a libro chiuso, allora non lo stai usando bene \[[[Introduzione alla Programmazione - Lezione 01 - Slide.pdf#page=25|Slide 25]]].**
> - Prima ci provo da solo, poi chiedo aiuto.
> - Chiedo spiegazioni causali, non soluzioni pronte.
> - Uso l'LLM per esercitarmi di più, non di meno.

> [!tip]- Flashcard: Cognitive Surrender e Tri-System Theory
%%
TARGET DECK: University::Introduzione alla Programmazione
START
Basic
Front: Cosa si intende per "Cognitive Surrender" (resa cognitiva) nell'apprendimento della programmazione secondo la Tri-System Theory di Shaw e Nave?
Back: È il fenomeno per cui lo studente, delegando passivamente la generazione della soluzione algoritmica a un LLM (Sistema 3), disattiva lo sforzo deliberativo e analitico del proprio Sistema 2 biologico. La lettura della soluzione pronta crea una falsa illusione di padronanza (*fluency illusion*), inibendo l'acquisizione delle reali capacità di scomposizione algoritmica e debugging autonomo.
Tags: education/university tech/programming tech/cs
<!--ID: 1790280114761-->
END
%%
