### Ubicazione: [Edificio Marco Polo, Aula 105]

Istruttore: [Prof Saverio Salzo]

## 23/9/2026 (**Dalla logica proposizionale alla logica dei predicati: connettivi, quantificatori e metodi di dimostrazione)**

Data e Ora: 2026-09-23 08:47:58

## Riepilogo

Questa lezione introduce i concetti fondamentali della logica proposizionale. L'istruttore definisce cosa sia una proposizione e introduce i connettivi logici (negazione, congiunzione, disgiunzione, implicazione, equivalenza) che permettono di comporre proposizioni complesse. Vengono spiegate le tabelle di verità come strumento per determinare il valore di verità (vero o falso) delle proposizioni composte, partendo dai valori delle proposizioni semplici. Attraverso esempi pratici, come quello di una madre che dà istruzioni a un figlio, vengono illustrate in dettaglio le operazioni di negazione, congiunzione ("e") e disgiunzione ("o"). Infine, viene chiarita la distinzione tra la "o" inclusiva usata in matematica e la "o" esclusiva presente nel linguaggio comune, sottolineando come la logica formale adotti solo la versione inclusiva per evitare ambiguità.

## Punti chiave

### 1. Fondamenti della logica proposizionale

- **Oggetto di studio della logica**
- L'oggetto di studio della logica delle proposizioni sono le frasi (proposizioni) per cui è possibile determinare se sono vere o false.
- Le proposizioni semplici, in questo contesto, sono denotate con lettere maiuscole come P, Q, R.
- **Composizione di proposizioni e connettivi logici**
- Le proposizioni possono essere composte tra loro utilizzando operatori logici, detti anche connettivi logici.
- I principali connettivi logici sono:
    - **Negazione (non)**: Indicata con il simbolo `¬`. Inverte il valore di verità di una proposizione.
    - **Congiunzione (e)**: Indicata con `∧` (una V capovolta).
    - **Disgiunzione (o)**: Indicata con `∨` (una V).
    - **Implicazione (se... allora...)**: Indicata con `⇒` (una freccia con doppia barra).
    - **Equivalenza (se e solo se)**: Indicata con `⇔` (una doppia freccia).
- Se P e Q sono proposizioni, allora anche `¬P`, `P e Q`, `P o Q`, `P implica Q`, e `P equivale Q` sono proposizioni il cui valore di verità dipende da quello di P e Q.

### 2. Tabelle di verità e operatori logici

# **Tabelle di verità**

> Sono uno strumento utilizzato per stabilire i valori di verità delle proposizioni composte.

> Mostrano come il valore di verità di un'espressione logica dipenda dai valori di verità delle sue componenti.

- **Negazione (non P)**

<aside>  
💡

> La proposizione `¬P` è vera se P è falsa, ed è falsa se P è vera.

> Esempio: Se l'affermazione "Indosso una maglietta rossa" è falsa, la sua negazione "Non indosso una maglietta rossa" diventa vera.

</aside>

- **Congiunzione (P e Q)**

<aside>  
💡

> La proposizione `P e Q` è vera **solo** quando entrambe le proposizioni P e Q sono vere. In tutti gli altri casi, è falsa.

> Esempio: Una madre dice al figlio "per uscire devi fare i piatti **e** portare fuori l'immondizia". Il figlio potrà uscire solo se compie entrambe le azioni (P e Q sono entrambe vere).

</aside>

- **Disgiunzione (P o Q)**

<aside>  
💡

> La proposizione `P o Q` è falsa **solo** quando entrambe le proposizioni P e Q sono false. È vera in tutti gli altri casi, incluso quando sia P che Q sono vere.

> Esempio: Una madre dice al figlio "per uscire devi fare i piatti **o** portare fuori l'immondizia". Il figlio non potrà uscire solo se non fa nessuna delle due cose. Se ne fa una sola o entrambe, può uscire.

</aside>

### 3. Ambiguità della "o" nel linguaggio e precisione matematica

- **"O" inclusiva**

<aside>  
💡

- La disgiunzione `o` (simbolo `∨`) usata in logica matematica è di tipo "inclusivo".
    
- Questo significa che l'espressione `P o Q` è vera anche quando sia P che Q sono vere. L'esempio del figlio che può fare entrambe le cose (lavare i piatti e portare fuori l'immondizia) e comunque uscire, illustra questo concetto.  
    </aside>
    
- **"O" esclusiva**
    

<aside>  
💡

- Nel linguaggio comune (italiano), la "o" può avere anche un significato "esclusivo" o di alternativa, dove solo una delle due opzioni può essere vera, ma non entrambe contemporaneamente.
    
- Esempio: "La luce è accesa o è spenta". Non è possibile che la luce sia contemporaneamente accesa e spenta.  
    </aside>
    
- **Scelta della logica matematica**
    
- Per evitare ambiguità, la logica matematica adotta unicamente la "o" inclusiva. La "o" esclusiva non viene ammessa in questa formalizzazione per garantire che le affermazioni non siano soggette a interpretazioni multiple.
    

Data e ora: 2026-09-23 09:01:02

## Riepilogo

La lezione introduce i concetti di logica proposizionale, concentrandosi sull’implicazione materiale (“se P allora Q”) e sull’equivalenza logica (“P se e solo se Q”). Si spiega che un’implicazione è falsa solo quando la premessa è vera e la conseguenza è falsa; è vera in tutti gli altri casi, inclusa la situazione in cui la premessa è falsa. Si chiariscono le nozioni di “condizione necessaria” e “condizione sufficiente” nel contesto dell’implicazione. Infine, si presenta l’equivalenza come relazione in cui due proposizioni hanno sempre lo stesso valore di verità, mostrando che “P equivale a Q” significa “P implica Q e Q implica P”. La lezione si conclude con l’annuncio di una pausa di 10 minuti.

## Punti Chiave

### 1. Implicazione Logica (Proposizioni Condizionali)

<aside>  
💡

- **Definizione e Notazione**
    
    - “P implica Q” (P → Q) esprime la proposizione condizionale “se P, allora Q”.
- **Condizioni di Verità**
    
    - È falsa solo quando P è vera e Q è falsa.
    - Negli altri tre casi (P vera e Q vera; P falsa e Q vera; P falsa e Q falsa) è vera.
- **Principio "Ex Falso Quodlibet"**
    
    - Una premessa falsa può implicare qualsiasi conclusione (“ex falso quodlibet”), spiegando perché l’implicazione è sempre vera quando P è falsa, indipendentemente dal valore di verità di Q.
- **Esempio Pratico**
    
    - “Se oggi piove, non esco di casa” è falso solo se piove (P vera) e la persona esce comunque (Q falsa). Se non piove (P falsa), uscire o non uscire non contraddice l’affermazione.
- **Condizione Necessaria e Sufficiente**Q è una **condizione necessaria** per P (se P è vero, deve esserlo anche Q).
    
    $$  
    (P \implies Q)  
    $$
    
- P è una **condizione sufficiente** per Q (se P si verifica, ciò è sufficiente a garantire che Q si verifichi).  
    </aside>
    

### 2. Equivalenza Logica

<aside>  
💡

- **Definizione e Notazione**
    
    - “P equivale Q” (P ↔ Q) stabilisce che P e Q hanno sempre gli stessi valori di verità.
- **Tabella di Verità**
    
    - “P ↔ Q” è vera se e solo se P e Q sono entrambe vere oppure entrambe false.
    - È falsa se una proposizione è vera e l’altra è falsa.
- **Relazione con l’Implicazione**
    
    $$  
    (P \iff Q) \equiv (P \implies Q) \land (Q \implies P)  
    $$
    
    ossia la validità deve sussistere in entrambe le direzioni.
    
    - Nelle dimostrazioni matematiche si prova spesso l’implicazione in un verso e poi nell’altro per stabilire l’equivalenza.  
        </aside>

### 3. Esempi Matematici e Applicazioni

- **Teorema sulle Serie Convergenti**
    
    - Esempio: “Se una serie è convergente (P), allora la successione dei suoi termini tende a zero (Q)”.
    - Tendere a zero è una condizione necessaria per la convergenza della serie.
    
    ## 1. Riepilogo
    
    La lezione ha introdotto e sistematizzato le leggi fondamentali del calcolo proposizionale (legge del terzo escluso, leggi di De Morgan, contrapposizione) e il metodo di dimostrazione per assurdo. Successivamente ha esteso il linguaggio alla logica dei predicati introducendo i quantificatori universale ($\forall$) ed esistenziale ($\exists$), le nozioni di variabile libera/legata e le leggi di negazione dei quantificatori. È stata inoltre illustrata l’utilità della contrapposizione in una dimostrazione tipica sui numeri pari/dispari.
    
    ## 2. Definizioni e Teoremi
    
    - Definizione [Proposizione composta]: Una formula costruita a partire da proposizioni mediante connettivi logici ($\neg$, $\land$, $\lor$, $\Rightarrow$, $\Leftrightarrow$).
    
    <aside>  
    💡
    
    - _**Teorema [Legge del terzo escluso]**_: $p \lor \neg p$ è una tautologia.
    - _**Teorema [Leggi di De Morgan]**:_
        - $\neg(p \land q) \Leftrightarrow \neg p \lor \neg q$.
        - $\neg(p \lor q) \Leftrightarrow \neg p \land \neg q$.
    - _**Teorema [Contrapposizione]**_: $p \Rightarrow q \Leftrightarrow \neg q \Rightarrow \neg p$.
    - _**Definizione [Contraddizione**_]: Una formula della forma $r \land \neg r$ è sempre falsa.
    - _**Teorema [Schema del ragionamento per assurdo**_]: Per dimostrare $p \Rightarrow q$, si assume $p$ e $\neg q$ e si deduce una contraddizione ($r \land \neg r$); da ciò segue $q$.  
        </aside>
    
    > Definizione [Predicato]: Un’espressione con variabili (ad es. $P(x)$) il cui valore di verità dipende dall’assegnazione delle variabili e dal dominio.
    
    #### Definizione [Quantificatori]:
    
    - Universale: $\forall x\, P(x)$ (“per ogni $x$, $P(x)$”).
    - Esistenziale: $\exists x\, P(x)$ (“esiste $x$ tale che $P(x)$”).
    - Definizione [Variabile libera/legata]:
        - Libera: una variabile che occorre non preceduta dal quantificatore corrispondente entro il suo campo d’azione (es.: in $x+3\le 7$, $x$ è libera).
        - Legata: una variabile quantificata entro il campo di $\forall x$ o $\exists x$ (es.: in $\forall x\,(x+3\le 7)$, $x$ è legata).
    - Definizione [Proposizione aperta/chiusa]:
        - Aperta: contiene variabili libere, non ha valore di verità assoluto senza un’assegnazione.
        - Chiusa: tutte le variabili sono legate, ha valore di verità ben definito.
    - Teorema [Leggi di negazione dei quantificatori]:
        - $\neg\big(\forall x\, P(x)\big)\Leftrightarrow \exists x\, \neg P(x)$.
        - $\neg\big(\exists x\, P(x)\big)\Leftrightarrow \forall x\, \neg P(x)$.
    
    ## 3. Sviluppo della Classe
    
    - Calcolo proposizionale e tautologie:
        - Le “leggi” presentate sono tautologie: formule sempre vere per ogni assegnazione di verità a $p$, $q$, ecc.
        - Esempio e interpretazione:
            - Terzo escluso $p\lor \neg p$: i valori di verità sono binari; non esiste una terza possibilità.
        - Leggi di De Morgan: la negazione “entra” distribuendosi e scambiando $\land$ con $\lor$ e viceversa.
    - Metodo per assurdo:
        - Struttura tipica dei teoremi: $p \Rightarrow q$.
        - Procedura: assumere $p$ e $\neg q$; se si giunge a $r\land \neg r$, allora l’assunzione $\neg q$ è falsa e segue $q$.
    - Contrapposizione:
        - Equivalenza: $p\Rightarrow q$ è logicamente equivalente a $\neg q \Rightarrow \neg p$.
        - Uso strategico: spesso $\neg q \Rightarrow \neg p$ è più trasparente da dimostrare di $p\Rightarrow q$.
    - Dalla logica proposizionale alla logica dei predicati:
        - Motivazione: introdurre espressività con quantificatori $\forall$, $\exists$.
        - Predicati: esempi $x+3=7$, “$x$ è primo”, $x\le y$.
        - Dominio: occorre specificare l’insieme di riferimento (es. $\mathbb{N}$, $\mathbb{R}$).
        - Costruzione di formule: da atomi connettivi ($\neg$, $\land$, $\lor$, $\Rightarrow$, $\Leftrightarrow$) e quantificatori.
        - Campo di azione del quantificatore: porzione di formula su cui il quantificatore agisce.
    - Variabili libere e proposizioni:
        - $P(x)$ con $x$ libera è una proposizione aperta.
        - $\forall x\, P(x)$ e $\exists x\, P(x)$ sono proposizioni chiuse; si può attribuire vero/falso.
    - Leggi della quantificazione:
        - Notazioni: $\forall x: P(x)$ per $\forall x\,(P(x))$; $\exists x: P(x)$ per $\exists x\,(P(x))$.
        - Negazione dei quantificatori:
            - $\neg\forall \leftrightarrow \exists \neg$; $\neg\exists \leftrightarrow \forall \neg$.
        - Esempi intuitivi con proprietà come “indossare una maglietta rossa”.
        - Composizione di quantificatori multipli e negazione annidata:
            - Esempio: negare $\forall x\, \exists y\, P(x,y)$ produce $\exists x\, \forall y\, \neg P(x,y)$.
    
    ## 4. Esercizi Pratici Risolti
    
    Problema:  
    Dimostrare, per ogni intero $x$, l’implicazione $\big(x^2 \text{ è pari}\big)\Rightarrow \big(x \text{ è pari}\big)$.  
    Soluzione:
    
    - Si applica la contrapposizione:
        
        $$  
        \big(x^2 \text{ è pari}\big)\Rightarrow \big(x \text{ è pari}\big)\ \Leftrightarrow\ \big(x \text{ è dispari}\big)\Rightarrow \big(x^2 \text{ è dispari}\big).  
        $$
        
    - Sia $x$ dispari. Allora $x=2n+1$ per qualche $n\in\mathbb{N}$.
        
        $$  
        x^2=(2n+1)^2=4n^2+4n+1=2\big(2n^2+2n\big)+1.  
        $$
        
    - Poiché $2n^2+2n\in\mathbb{N}$, si ha $x^2=2k+1$ con $k=2n^2+2n\in\mathbb{N}$, dunque $x^2$ è dispari.  
        Risultato Finale: In base alla contrapposizione, si conclude che per ogni $x\in\mathbb{Z}$, se $x^2$ è pari allora $x$ è pari.
        
    
    ## 5. Note Importanti / Esami
    
    - Attenzione a spostare correttamente la negazione:
        - $\neg(p\land q)\equiv \neg p\lor \neg q$, non $\neg p\land \neg q$.
        - $\neg\forall x\,P(x)\equiv \exists x\,\neg P(x)$ e $\neg\exists x\,P(x)\equiv \forall x\,\neg P(x)$.
    - Nelle dimostrazioni per assurdo, identificare chiaramente la contraddizione della forma $r\land \neg r$.
    - La contrapposizione è un’equivalenza: si può dimostrare il verso più semplice.
    - Specificare sempre il dominio delle variabili nei predicati.

#### Trascrizione integrale lezione

00:00:00 Speaker 1  
No, quindi quest'altra non è una proposizione. Ok, bene. Quindi l'oggetto di studio della logica delle proposizioni sono frasi su cui posso dire siano vere e false.

00:00:17 Speaker 1  
Queste frasi poi le posso comporre

00:00:27 Speaker 1  
Quindi.

00:00:30 Speaker 1  
Composizione di proposizioni.

00:00:40 Speaker 1  
Ci sono quelli che si chiamano operatori logici o anche connettivi logici.

00:00:53 Speaker 1  
Allora chi sono? C'abbiamo la negazione.

00:00:58 Speaker 1  
Si indica con questo simbolo, ok, questa è la negazione.

00:01:08 Speaker 1  
Poi abbiamo la E, che si indica con una V capovolta, OK, con una A senza la barra orizzontale. Questa è una congiunzione. Si chiama come congiunzione.

00:01:23 Speaker 1  
Come in italiano, tra l'altro, la O.

00:01:30 Speaker 1  
La o si indica con invece una ve questa si chiama disgiunzione

00:01:42 Speaker 1  
Poi c'abbiamo l'implica, questo sarebbe.

00:02:00 Speaker 1  
Se puntini, allora puntini oppure anche implica. Si legge implica lo denotiamo con appunto doppia. Una freccia con una doppia barra orizzontale e questo sia poi l'implicazione.

00:02:24 Speaker 1  
OK. E infine abbiamo il se e solo se, o anche equivalenza, e questa è la doppia freccia. Quindi siamo così e questa si chiama appunto equivalenza. OK, questo scusate, questo si legge equivale. Quando lo trovate lo leggete: equivale, e questa è l'equivalenza.

00:02:54 Speaker 1  
OK. Quindi ci sono questi connettivi logici, che servono per connettere due proposizioni. Le proposizioni le denoteremo in questo contesto con delle lettere maiuscole, quindi tipo PQR.

00:03:22 Speaker 1  
Quindi le denoteremo con lettere maiuscole. Per cui, se Peq sono proposizioni.

00:03:32 Speaker 1  
Allora, se scrivo non P, oppure scrivo PEQ, oppure se scrivo POQ, oppure P implica Q, oppure P equivale Q, queste sono ancora proposizioni, OK? Cioè, possono essere vere o false e saranno vere o false a seconda dei valori di verità di queste funzioni, di queste proposizioni componenti.

00:04:04 Speaker 1  
Ok, facciamo adesso qualche esempio.

00:04:07 Speaker 2  
Così allora

00:04:13 Speaker 1  
Per stabilire questi valori si costruiscono anche queste, si chiamano tabelle di libertà.

00:04:24 Speaker 1  
Cominciamo dalla negazione, cioè non p.

00:04:29 Speaker 1  
Quando scrivo non p, questa è vera se p è falsa ed è falsa se p è vera. Si scrive una cosa di questo tipo, p. Ci metto il non p, una barra verticale p può assumere i valori vero falso. Ma se è vero non p diventa falso e se p è falsa non p diventa vera.

00:05:04 Speaker 1  
OK, quindi questo operatore logico non fa altro che invertire i valori di verità. Se io dico

00:05:17 Speaker 1  
Se dico per esempio.

00:05:20 Speaker 1  
Indosso una maglietta rossa. Voi mi guardate e dite: non è vera. Ma se faccio la negazione di questa affermazione, 'Non indosso una maglietta rossa', questa diventa vera, ok?

00:05:45 Speaker 1  
Vediamo la congiunzione e la distribuzione.

00:06:01 Speaker 1  
Quindi vediamo P o Q, P e Q e P o Q.

00:06:11 Speaker 1  
Una mamma potrebbe essere. Facciamo un altro esempio. Mamma dice al figlio

00:06:25 Speaker 1  
Allora per uscire devi due butti

00:06:33 Speaker 1  
Fare gli atti e portare fuori l'immondizia.

00:06:50 Speaker 1  
Oppure può dire fare i piatti, portare fuori l'immondizia.

00:07:06 Speaker 1  
OK, quindi la mamma sta ponendo una condizione al figlio. Allora P sarà il figlio.

00:07:16 Speaker 1  
Fa lava i piatti, invece il figlio porta fuori l'immondizia.

00:07:31 Speaker 1  
Porta fuori l'immondizia.

00:07:34 Speaker 1  
Ok, vedete, nel primo caso la mamma pone due condizioni: ha unito queste due proposizioni. Questa può essere vera o falsa, il figlio può o meglio farlo. Ok, nel primo caso guarda dice per uscire tu devi fare due cose e ci mette, quindi sono due condizioni che ci mette la Eok vuol dire fare l'uno e fare l'altro. Ok, quindi il figlio potrà uscire soltanto se entrambe queste due sono vere.

00:08:05 Speaker 1  
OK, entrambe devono essere vere in ogni altro caso. Il figlio non esce, OK? Se passano i piatti o portano soltanto fuori l'immondizia, il figlio purtroppo rimane a casa, OK? Quindi questa cosa la possiamo venire su una tabella di verità in cui ci mettiamo P, ci mettiamo Q, in cui ci mettiamo PEQ, in cui ci mettiamo POQ

00:08:34 Speaker 1  
No?

00:08:41 Speaker 2  
Blu ci metto di là.

00:08:51 Speaker 1  
Quindi dicevo T Q, poi qua ci mettiamo P e Q e qui ci mettiamo P o Q.

00:09:01 Speaker 1  
Quindi guardiamo la E. Qui abbiamo tutte le possibili situazioni che si possono verificare. Questa può essere vera, possono essere entrambe vere, oppure può essere vera l'una e falsa l'altra, oppure falsa la prima e vera la seconda, oppure entrambe false. OK, questa è la situazione che si può verificare, no? Sono tutte le scelte del figlio. OK, bene. Quindi il figlio potrà uscire nella condizione E.

00:09:34 Speaker 1  
Soltanto quando entrambe sono vere, questa diventa vera ed è un lasciapassare per il figlio. In tutti gli altri casi non è soddisfatta, è falsa, falsa.

00:09:51 Speaker 1  
Ok, ma se la mamma invece avesse detto: per uscire devi fare i gatti o portare fuori l'immondizia, quando riuscirebbe ad uscire? Tu in tutte le parti lui non fa niente. C'è un amo. Ok, tra i gatti o portare fuori l'immondizia. Facciamolo al contrario. Quando non viene soddisfatta, cioè quando non uscirebbe.

00:10:25 Speaker 1  
Quando non fa nessuna delle due, ok? Quindi questa diventa falsa quando nessuna delle due

00:10:34 Speaker 2  
Quando è falsa

00:10:41 Speaker 1  
Questa diventa falsa, ok? Quando tutte e due sono false, questa è falsa, ok? E nei casi particolari? È vero, nel senso che il figlio può fare i piatti soltanto, può fare soltanto quest'altra cosa, cioè portare fuori l'immondizia. Ma se è proprio il figlio, diciamo quello ideale, fa entrambe le cose, ok? E ovviamente la mamma non gli dice di non uscire, no? Quindi in tutti questi casi è vero.

00:11:13 Speaker 1  
È vero. Ok, attenzione, questa o, intesa in questo modo si chiama una o inclusiva. Ok, nell'italiano noi siamo stati d'accordo nell'interpretare questa o in modo inclusivo. Ok, questa è una frase in italiano, va bene, e l'abbiamo interpretato quella o in modo inclusivo. In italiano c'è un'altra forma della o che è una forma di alternativa. Ok, se io dico la luce è accesa o è spenta.

00:11:47 Speaker 1  
È sempre una o. Però questa volta io non mi posso immaginare che la luce è accesa e spenta contemporaneamente, o è accesa o è spenta. È una o di alternativa. Okay, questa o viene detta esclusiva. Okay. Quindi in italiano vedete la congiunzione o ha un'ambiguità. La posso usare sia in modo inclusivo che in modo esclusivo. In matematica questa cosa non va bene perché sennò mi incasinano tutti, le affermazioni che posso fare sulle questioni.

00:12:17 Speaker 1  
E quindi dico no, la esclusiva non l'ammetto. La mia è solo inclusiva.

00:12:22 Speaker 2  
Ok, bene.

seconda registrazione.

00:00:00 Speaker 1  
Li indica.

00:00:00 Speaker 2  
OK, questa è un'altra cosa che bisogna capire.

00:00:06 Speaker 2  
Allora, questo appunto si legge anche se PI. Qok. Abituatevi pian piano a leggerle. Queste cose si chiamano anche proposizioni condizionali.

00:00:33 Speaker 2  
Vediamo questa frase: se oggi piove

00:00:40 Speaker 1  
Non esco di casa.

00:00:48 Speaker 2  
Ok?

00:00:50 Speaker 2  
Se io dico questa affermazione: se oggi piove non esco di casa.

00:00:56 Speaker 2  
Quando mi sto rinnegando, ok? Qual è il mio comportamento affinché voi poi diciate: 'Guarda, hai detto ti sei rinnegato rispetto a quello che hai detto'. No, quale sarebbe? Se oggi piove, allora non esco di casa. Se esci lo stesso nonostante piova, cosa falsificherebbe quell'affermazione? Se quando piove, anzi, se esci di casa, se esci quando piove.

00:01:28 Speaker 2  
Esatto, quindi se sì, se oggi piove e uscissi di casa avrei detto una falsità, ok? Quindi questa affermazione si falsifica, diventa falsa quando si realizza la premessa e non si realizza la conseguenza. Oke negli altri casi?

00:01:52 Speaker 2  
Se invece...

00:01:55 Speaker 2  
Non piove affatto, è una bella giornata come oggi. Ci sarebbe una situazione in cui mi falsificherei.

00:02:04 Speaker 2  
Posso fare quello che voglio, posso uscire o non uscire? Non è che qualcuno, se è una bella giornata, mi direbbe no. Tu hai detto che se OK. Quindi questo ci dice che un'affermazione di questo tipo

00:02:16 Speaker 1  
Quindi PQ di nuovo questo è

00:02:22 Speaker 2  
Può essere vero, vero? Vero, falso.

00:02:30 Speaker 2  
Ok, poi abbiamo la nostra P implica Q.

00:02:34 Speaker 2  
Questa affermazione è falsa solo quando la premessa è vera e la conseguenza è falsa. Non si realizza. Quindi, premessa vera, conseguenza falsa. Qui è falsa, negli altri casi è sempre vera.

00:02:55 Speaker 2  
OK, quindi attenzione perché questa crea sempre un po' di confusione. Questo si dice perché succede questa situazione: se la premessa è falsa, una premessa falsa implica qualsiasi cosa. OK, quindi c'è questa situazione che può sembrare poco intuitiva.

00:03:16 Speaker 1  
Ma diciamo è così

00:03:22 Speaker 2  
OK? Per esempio, noi lo vedremo. Faccio questo esempio. Proveremo questo teorema: se una serie, adesso non sapete che cos'è, ma non è importante. Se una serie è convergente

00:03:39 Speaker 2  
La successione dei termini a con n tende a zero, OK. Vedete, questo ha una struttura che è proprio questa, no? Questo dice qualsiasi cosa. La serie adesso non sapete cosa cos'è, ma non è importante. OK, è un concetto. La serie è un'altra cosa da una successione. Oke, il concetto di convergenza di una serie è una cosa un po' diversa. OK, però questo dice se succede questo, che questa serie è convergente.

00:04:10 Speaker 2  
Questo sta a denotare qualcosa intuitivamente, tipo a con zero, più a con uno, più a con due, più a con tre, cioè è una somma infinita. OK, poi vedremo cosa vuol dire. Quindi se questa cosa converge, la successione dei termini deve tendere a zero. OK, allora in questo caso si dice che questa cosa è una condizione necessaria affinché si verifichi questa. OK, quindi si parla di condizione necessaria

00:04:40 Speaker 2  
Quindi la Q è una condizione necessaria affinché si verifichi P, perché ogni volta che si verifica P si verifica Q. OK, però posso anche dire un'altra cosa: se voglio che la successione a con n tenda a zero, è sufficiente che si verifichi questa condizione. OK, quindi se io voglio che si verifichi Q, è sufficiente che si verifichi questa pubblicazione qui nel nostro esempio.

00:05:10 Speaker 2  
Se oggi piove, se io voglio che tu esca di casa, è sufficiente che piova, OK? Quindi ci si esprime anche in questi termini. Quindi per realizzare questa conseguenza basta che succeda questo, OK? Però questa conseguenza si può realizzare anche se non si verifica questo, perché se non piove io sono comunque libero di uscire, Ok? Cioè potrebbe anche essere

00:05:38 Speaker 2  
Va bene?

00:05:38 Speaker 1  
Quindi questo è un vediamo

00:05:48 Speaker 2  
Faccio solo una breve introduzione. L'equivalenza, quindi, quando facciamo p equivale q, con questo intendiamo dire che p e q hanno gli stessi valori di verità. Ok, questo vuol dire che se io faccio la tabella di verità per p e q, quindi ho p e q.

00:06:23 Speaker 2  
P equivale q, questo è vero. Tutti i possibili sono sempre vero falso. E questa invece prende, questa è vera se e solo se entrambe sono vere oppure entrambe sono false. Quindi qui è vera e qui è vera, invece è falsa in queste situazioni se una è vera e l'altra è falsa. Allora è falsa. OK, perché quello sta a dire che quelle due proposizioni sono equivalenti.

00:06:58 Speaker 2  
OK, equivalenti anche, diciamo, da un punto di vista del significato, no? Stabilisce, guarda che quindi devono avere, si devono comportare allo stesso modo: se una è vera, l'altra è vera, se una è falsa, l'altra è falsa. Se invece hanno un comportamento diverso, una vera e l'altra falsa non sono equivalenti. Oke, questa equivale anche a scrivere, cioè l'equivalenza.

00:07:21 Speaker 2  
Questo, per esempio, lo si vede nelle dimostrazioni. Questa potrei scrivere equivale a dire che B implica qeq implica B.

00:07:37 Speaker 2  
Quando scrivo così vuol dire che questa affermazione qua equivale, la stessa cosa, ok? Che dire? Che B implica Q, ma anche che Q implica V, ok, cioè che vadano le due implicazioni nelle due direzioni. Va bene, allora ci fermiamo qui e facciamo 10 minuti di pausa. Va bene, inizio proprio tra 10 minuti, quindi guardate l'orologio perché sennò non ce la faccio.

terza registrazione

00:00:00  
Chiamo velocemente qui la prima po non p. Questa si chiama legge del terzo escluso. Due, la negazione di [pe.eu](http://pe.eu/) equivale a negazione di p. O negazione di q, la negazione invece di p è q.

00:00:37  
Questa equivale a negare p negare q. E poi abbiamo tre, queste si chiamano leggi di De Morgan. Poi abbiamo che invece p equivale q. Questo equivale a scusate p implica q equivale a non q implica non p. Questa si chiama legge della contronominale.

00:01:27  
implica q equivale a p e non q implica r e non r e questa è la dimostrazione della storia allora le commentiamo brevemente. Allora, questa prima si chiama legge del terzo escluso perché cosa sono queste leggi?

00:02:00  
Sono delle affermazioni, vedete che è una proposizione composta. Questa qua, vedete, è una proposizione. Ho preso due proposizioni, le sto facendo congiunzione, poi ci faccio la negazione, poi ce la metto in equivalenza con un'altra proposizione. Tutta quanta questa è una proposizione. Questa proposizione può essere in linea di principio vera o falsa a seconda dei valori di P eqok. Questi si chiamano leggi delle proposizioni del calcolo proposizionale, perché in realtà sono quelle che si chiamano delle tautologie, cioè sono sempre vere.

00:02:38  
Queste sono il valore di verità di queste affermazioni, sono sempre vere, qualsiasi siano i valori di P eq di verità che attribuisco a P eq. Allora vedete questa po non p, cosa succede? Che può essere p vera e allora qui c'è una o, questa è vera, ma allora può essere p falsa, ma se p è falsa questa è vera e allora questa è ancora vera. Questa semplicemente dice che i valori di verità sono due, cioè o è vera o è falsa e il terzo escluso ha.

00:03:12  
Si riferisce proprio a questa situazione, cioè nei valori di verità c'abbiamo due opzioni soltanto: o è vera o è falsa. Non c'è una terza possibilità. Queste si chiamano leggi di De Morgan. Allora vedete, questa dice negare una congiunzione quando la io dico che sono come per i piatti, no? Cioè per lavare i piatti è cos'era, portar fuori l'immondizia, no? Se c'è una condizione e quando. Se negare questa condizione, cioè dire non è verificata, quindi lavare i piatti e portare fuori l'immondizia, questa cosa non si verifica, perché c'è una negazione davanti.

00:03:56  
Cosa deve succedere per non verificarsi? Una delle due non deve essere vera, quindi o succede o non succede. Negare, vedete, la negazione passa a ciascuno dei termini, ma questa diventa una o. Così come negare una o se la condizione è di nuovo lavare i piatti o portare fuori l'immondizia.

00:04:30  
Il figlio non fa questa cosa, cioè? Cosa vuol dire quindi non fare questa cosa? Vuol dire non fare nessuna delle due cose, quindi vuol dire non lavare i piatti e neanche portare fuori l'immondizia. La negazione di nuovo entra qui dentro e questa diventa questa o, scusate, diventa una Eok. Queste si chiamano leggi di De Morgan.

00:05:07  
Va bene, un altro commento e adesso diciamo commenteremo queste due. Questa ultima stabilisce quello che si chiama dimostrazione per assurdo, perché normalmente è quello che succede con le dimostrazioni per assurdo, cioè. I teoremi, come vi dicevo, spesso hanno una forma del tipo P implica Q, dove P sono le ipotesi e Q è la tesi. Va bene?

00:05:38  
Allora la dimostrazione per assurdo procede in questo modo: assumo che P sia vera, per assurdo suppongo che la Q non sia vera. Se quindi cosa vedete qui c'è P e non Q. Quindi questo sta dicendo che sto facendo adesso un'altra cosa. Le mie assunzioni sono che assumo la P e assumo che la Q non sia vera. Vedete, c'è una P e non Q. Se da queste premesse arrivo ad una contraddizione.

00:06:17  
Questa Q non potrà, cioè questa Q allora ho sbagliato ad assumerla, non vera, deve essere per forza vera e quindi ho provato. Questa è una contraddizione, perché vedete, questa è una R, cioè un'altra proposizione, e c'è una congiunzione, la negazione di R. Questa è una cosa che è sempre falsa. Una contraddizione è quando io provo un'affermazione e simultaneamente provo la sua opposta, provo la sua negazione, quindi è vera sia l'una che la sua negazione.

00:06:52  
Questa non è possibile, questa è sempre falsa. Questa cosa è sempre falsa, si chiama una contraddizione. Quindi questo semplicemente mi stabilisce, diciamo in maniera formale, quello che normalmente si fa con il ragionamento per assurdo. Bene. Sulla legge della contro nominale, adesso ve la commento brevemente, ma poi vi faccio un altro esempio.

00:07:31  
Vedete che qui dice. Provare p implica q è la stessa cosa che provare non q implica non p. Questa è come dire: allora io sto assumendo p e voglio provare q. Allora questo è simile a un ragionamento per assurdo, perché questo dice: proviamo ad assumere che q non sia vera, quindi sto qua.

00:08:09  
Se questa cosa mi fa arrivare a non p, dato che avevo assunto che p fosse vera, questa cosa non può, diciamo, il non q non può verificarsi. Perché il non q mi implica non p, ma io stavo assumendo p, per cui q deve essere per forza vera. Questa cosa però adesso la vedremo con un altro esempio che vi chiarirà. Si tratta della stessa cosa, questa legge della contronominale si applica in tante situazioni.

00:08:42  
Bene, allora questa cosa sostanzialmente, vedete questa cosa che vi sto raccontando ora fa parte di un'area della matematica che si chiama logica matematica. In realtà questa ha delle affinità anche con l'informatica, tra l'altro. Perché io ne ho solo accennato un po'. Noi stiamo facendo una specie di una logica più o meno intuitiva, però già più o meno in un formalismo.

00:09:15  
Questa si può spingere molto avanti e rientra in quella cosa che si chiama logica formale. La logica formale è una cosa veramente astrusa, diciamo, devo essere, nel senso che è. Il linguaggio è ancora più pesante, cioè più meno intuitivo di quello che succede in matematica.

00:09:48  
Dovete sapere che nella ricerca di fare queste, questa, quando vi parlavo dei fondamenti della matematica, i fondamenti della matematica vanno quasi inevitabilmente a finire nella logica formale. Cioè studiare i linguaggi da un punto di vista formale. E questo è uno dei più semplici linguaggi, cioè il linguaggio del calcolo proposizionale, c'ha le sue leggi. Perché quello che si vuole fare, voi siete, diciamo, state studiando per forma informatica, in qualche modo cercare di formalizzare.

00:10:27  
Trovare delle regole di sintassi del linguaggio, chiare e automatizzare certe deduzioni, perché si presta poi ad essere implementato, per esempio, su un computer. Vi dicevo, c'è tra i logici più famosi Bernard Russell, nella ricerca di Favi, nel suo tentativo di.

00:11:01  
Dare conto dei fondamenti della matematica ha scritto un diciamo non so dei volumi in realtà credo che siano due sui credo che li abbia chiamati principi a matematica così ricordo benissimo però sono libri dove voi sfogliate le pagine e trovate solo cose scritte così non trovate la parola non trovate cioè è una cosa questo per dire la mente umana dove può arrivare.

00:11:31  
Però questo è l'esercizio estremo dell'astrazione. Noi non ci spingeremo, quello sarà solo per dirvi che in realtà questo è puro, poi è proprio un'altra. Adesso complichiamo un po' il linguaggio, perché questo linguaggio qui è molto elementare. Come c'è una domanda? Come vi dicevo, come avete visto anche all'inizio, per esempio nelle definizioni di vendite, c'erano anche i 'per ogni' 'esiste'.

00:12:05  
Allora adesso noi dobbiamo arricchire un pochettino questo tipo di linguaggio e dobbiamo includere questi simboli "per ogni" ed esiste. Questo dà luogo ad un linguaggio un pochino più espressivo, che si chiama logica dei predicati. Quella di prima era logica delle proposizioni, questa si chiama logica dei predicati. Questi linguaggi formali funzionano così: voi avete delle espressioni atomiche, si dice, quindi delle espressioni molto semplici, e poi a partire da queste espressioni semplici c'avete dei connettivi logici e le componete a formare nuove proposizioni.

00:12:52  
Ci sono delle leggi, quindi questo vi tira fuori tutta una possibile, diciamo, come dire? Delle espressioni che sono permesse dal linguaggio, si chiamano formule del formato nella logica dei predicati insieme, diciamo l'atomo, diciamo l'elemento di base non si chiama più proposizione, ma si chiama predicato. Bene, un predicato in maniera intuitiva è una proposizione.

00:13:31  
che contiene una o più variabili, che possono essere da notare x, y eccetera, e il cui valore di verità dipende dal valore assegnato alle variabili.

00:14:14  
Esempio, se io scrivo x più tre uguale 7, questo è il predicato, oppure X è un numero primo. Queste hanno la forma sostanzialmente di una frase affermativa. Contiene una variabile, contengono delle variabili Xxok, oppure posso scrivere anche non so X, che ne so, 7 minore o uguale di Yok.

00:14:53  
Allora queste frasi, queste diciamo affermazioni, espressioni, non gli posso attribuire direttamente un valore di verità. Quindi devo capire queste variabili su che dominio sono, cioè di cosa si sta parlando, sto parlando di nomi naturali, numeri reali? E poi saranno vere o false quando al posto della x ci metterò un elemento particolare del dominio della variabile. Va bene? Quindi i predicati saranno frasi di questo tipo, le denoteremo sempre con Pq, eccetera, e potrò sempre usare i collettivi logici che abbiamo visto finora, cioè potrò sempre usare comporre con usando la negazione, la congiunzione, la disgiunzione o l'implica e l'equivalenza.

00:15:46  
Posso sempre usare questi qui per ottenere altri predicati. Sui predicati invece possiamo fare altre operazioni, introducendo nuovi operatori, due nuovi operatori.

00:16:19  
Quindi, nella logica dei predicati si aggiungono due nuovi operatori che si chiamano quantificatori.

00:16:51  
quantificatori universale ed esistenziale. Quindi sono per ogni, questo si legge per ogni, e poi esiste, è una e girata speculare questa legge. Come si usano questi? Si usano in questo modo: se P è un predicato, allora per ogni XPE per ogni scusate, ed esiste XP, questo è ancora un predicato, sono predicati.

00:17:46  
Quindi vedete la cosa è questa, quindi io c'ho dei predicati, quindi questo semplicemente mi dice come posso generare nuovi predicati. Parto dai predicati elementari, voi lo vedrete per esempio quando domani vedrete la teoria degli insiemi, ci sono delle relazioni fondamentali, cioè i predicati base sono cose del tipo E: X appartiene ad A. Oppure x uguale y, queste sono formule di base, cioè di atomi.

00:18:19  
A partire da queste, vedete, contengono delle variabili, anche questa è una variabile. A partire da queste, io poi che faccio? Le compongo, quindi posso metterci una e, posso comporre con una e con una o con una negazione, posso metterci un peroni davanti e qui dentro ci metto una cosa del genere. Con questo tipo di operazioni questo mi dice. Cosa mi è permesso per generare nuove cose che chiamerò predicati? Si parte da dei predicati atomici e con l'uso di queste regole sintattiche, stiamo parlando di sintassi, generano nuove affermazioni che sono lecite del linguaggio.

00:18:58  
Quello che sto spiegando è come si generano delle frasi sintatticamente corrette del linguaggio di cui sto parlando. Bene, allora. Questo si chiama qualche volta il campo di azione del quantificatore universale tra ogni x.

00:19:34  
Anche questo viene chiamato campo di azione del quantificatore esistenziale.

00:20:13  
Allora vediamo subito una variabile x si dice libera una variabile x presente in un caricato. Si dice libera se non è immediatamente preceduta da per ogni o esiste.

00:20:49  
Quindi, per esempio, se io scrivo x 3 minore uguale a 7, questa x è libera. Se invece scrivo per ogni x x 3 minore o uguale a 7 è una variabile x che compare qui e qui. Diciamo questa x è preceduta dal Peroni, quindi questa x non è libera. La variabile x non è libera, diciamo più precisamente, se la x compare nel campo di azione di un Peroni x, la x non è libera.

00:21:29  
Vedete questa affermazione? Qual è la differenza tra questi due tipi di affermazioni? Questa viene chiamata anche una proposizione aperta perché la x è libera e quindi non posso stabilire un valore di verità. Questa invece viene chiamata una proposizione chiusa perché viene chiusa proprio dall'operatore di parola e questa ha senso dire se è vera o meno. Dire che per ogni xx 3 è minore o uguale a 7, questa cosa è falsa.

00:22:04  
Non è vero che ogni numero sommato a tre risulta essere più piccolo di 7. Va bene quindi questa cosa. Quando si usano gli operatori per gli operatori universali, queste affermazioni possono diventare chiuse, cioè si può a quel punto stabilire se sono veri o falsi. Se scrivo esiste x tale che x 3 è minore o uguale a 7, anche questa è vera.

00:22:34  
Sicuramente c'è un numero che sommato a tre è minore di 7. Va bene le proposizioni, diciamo un predicato.

00:23:08  
in cui x è libera. Quindi quando scrivo p tra parentesi x sto denotando un predicato in cui compare la variabile x e la variabile x è libera. Questo significa che questo è un modo per denotare delle proprietà che possono essere soddisfatte o meno a seconda del valore della x. Per esempio, PX vuol dire può significare X indossa una maglietta rossa, dove X, per esempio, è uno studente, un qualunque denota uno studente di una classe.

00:24:10  
Quindi x denota uno di voi e la proprietà di cui sto parlando è x indossa una maglietta rossa. Questa proprietà può essere soddisfatta o meno per ciascuno di voi. Allora, come ci sono le leggi che abbiamo visto dei predicati del campo delle proposizioni, esistono anche delle leggi per la quantificazione.

00:24:40  
Le leggi della quantificazione. Allora, le leggi della quantificazione sono queste. Vi dico solo una cosa.

00:25:15  
Quando scrivo per ogni xpx, questo si può scrivere anche, diciamo, è la stessa cosa per ogni x due punti pxe. Così quando scrivo esiste xpx tra parentesi, questa è la stessa cosa. Diciamo, si può scrivere anche. È solo un fatto notazionale, esiste X due punti X, allora questo si legge.

00:25:56  
Allora vedete qui, adesso avete notato che io scrivo sempre le cose tra parentesi. Poi adesso man mano, come dire, queste regole le rilassiamo un pochettino, perché altrimenti se ci teniamo le parentesi cominciano a complicarsi un po' tanto e non si legge bene. Quindi se, come dire, senza che le cose poi non creano ambiguità, cercheremo di eliminare le parentesi finché possibile.

00:26:27  
Quindi invece che scrivere per ogni x tra parentesi px, scriveremo per ogni x due punti px. Questo si legge per ogni x risulta px, per esempio si può leggere e questo vuol dire questo invece si legge esiste x tale che è px. Ok, quindi esiste un x che soddisfa questa proprietà, va bene? Questo invece vuol dire ogni x soddisfa questa proprietà, va bene? Allora le leggi della quantificazione sono queste: la negazione di per ogni xpx.

00:27:03  
equivale a esiste x due punti negazione di px e negazione di esiste x due punti px equivale a per ogni x due punti negazione di px. Allora facciamo il caso che px sia, cerchiamo di interpretare di nuovo, queste vanno intese come un'espressione, un predicato che è sempre vero, e quindi stabilisce l'equivalenza tra questa cosa che è a sinistra e questa cosa che è a destra.

00:27:46  
Laddove vedo una cosa a sinistra di questo tipo, la posso scrivere e trasformare in questa cosa a destra. Questo da un punto di vista sintattico. Vedete, la cosa che succede è che questa negazione passa dentro il P, vedete che qui diventa messa davanti al P, ma il peroni diventa un esiste. È la stessa cosa qui, la negazione passa dentro, diventa negazione di PE, questo esiste, diventa un peroni. Vediamo se questa cosa, questa cosa è una cosa, se volete, formale, no, però vediamo se ha senso.

00:28:22  
Prendiamo PX che è x denota dov'era x indossa una maglietta rossa. Quindi se io faccio l'affermazione per ogni x di x vuol dire tutti gli studenti, ciascuno studente, ogni studente indossa una maglietta rossa. Se adesso dico non è vero che ogni studente indossa la maglietta rossa, questa cosa vuol dire che c'è almeno uno studente che non indossa la maglietta rossa.

00:28:53  
Va bene? Quindi quando dico: non è vero che ogni studente tra di voi indossa la maglietta rossa, per provare questa cosa devo trovare almeno uno di voi che non indossa la maglietta rossa. È la stessa cosa. Così come dico, questa affermazione dice: esiste almeno uno studente che ha la maglietta rossa, almeno uno di voi c'ha la maglietta rossa, lui ce l'ha. Però se questa cosa non fosse vera, negare questa affermazione vorrebbe dire: ogni studente non ha la maglietta rossa.

00:29:31  
Non ne trovo nessuno di voi con la maglietta rossa, va bene? Quindi queste cose le applicheremo molte volte. Quindi negare un per ogni un'affermazione dove c'è un per ogni lo vedremo nella definizione del limite: se io il limite è per ogni epsilon maggiore di zero, esiste delta, eccetera. No, se io devo negare questa cosa, dico no, guarda, il limite non è uguale ad Lok, perché è la negazione di quella.

00:30:13  
Allora cosa vuol dire negare? Dico OK, questo per ogni deve diventare un esiste, questo esiste deve diventare un per ogni e poi dentro passa la negazione. Ok, questa cosa ovviamente si applica anche se io ho una cosa, dopo vi faccio, diciamo sugli appunti vi lascio un esempio carino, ma oggi non abbiamo il tempo. Se ho una cosa del tipo per ogni x esiste xpx, ok, una di xy, scusate, cioè ho un predicato dove c'ho due variabili, come erano epsilon e delta prima, e scrivo per ogni x esiste per ogni, scusate, per ogni x esiste y.

00:30:54  
Per ogni x esiste un y tale che Pxy è vera. Negare questa cosa vuol dire? Devo applicare queste leggi? Quindi questo vuol dire che per ogni diventa un esiste e la negazione passa dentro, ma adesso la devo far passare ancora dentro. Questo esiste e diventa un per ogni, alla fine questo diventa esiste x tale che per ogni y vale la negazione di Txy.

00:31:29  
Vi lascio l'esempio su questa cosa. Adesso invece terminiamo con questo esempio sulla contronominale. Vi dicevo che quindi sulla come usare questo lo incontreremo spesso, è la legge della conto nominale. Questa cosa dice, questa diciamo con i quantificatori, questa si esprime in questo modo.

00:32:20  
Se io ho per ogni x Px implica qx, questa è la stessa cosa che per ogni x la negazione di qx implica negazione di Px. Qui dentro ho applicato la contropositiva. Vedete, facciamo p implica q, è la stessa cosa che non q implica non p. Facciamo un esempio allora.

00:32:55  
Prendiamo px uguale x al quadrato è pari e prendiamo qx uguale x è pari. La prima affermazione diventa: per ogni x, x intendiamo numeri naturali, cioè numeri interi. X al quadrato è pari implica X è pari.

00:33:26  
Allora questo dice questa affermazione: se il quadrato di un numero è pari, il numero è pari. Io voglio capire se questa affermazione è vera sempre per ogni numero naturale intero positivo. Se il quadrato di un numero è pari, il numero deve essere per forza pari. Allora invece di fare questa cosa, io faccio la contro nomina e dico, invece di provare, perché questa cosa non mi è immediatamente chiara, non è trasparente questa, cioè non la vedo.

00:34:07  
Adesso io faccio la contro nominale e vedrete che la cosa si schiarisce. La contro nominale dice per ogni X. Devo negare, questa implica la negazione di questa, ma dire che x non è pari vuol dire x dispari. Ci sono o uno è l'altro, quindi x è dispari, implica x al quadrato è dispari. Invece di provare questa io provo quest'altra cosa.

00:34:40  
Tenete conto, questa cosa ha perfettamente senso, perché se io vi dico. Supponiamo che x al quadrato è pari. Voglio provare che x è pari. Aspetta, se x non fosse pari, suppongo per un minuto che x non fosse pari, ma se x non è pari sarebbe dispari. Ma se ho provato da un'altra parte che se x è dispari, il suo quadrato è dispari, allora questa cosa mi proverebbe questa affermazione.

00:35:14  
perché a quel punto x deve essere per forza pari, perché se fosse dispari il suo quadrato sarebbe dispari, contraddicendo quello che sto assumendo qua, che è il quadrato invece pari. Quindi si ragiona in questo modo. Bene, questa cosa è molto più evidente. Come sono fatti i numeri dispari? Che forma hanno? 2n più 1.

00:35:45  
x che forma dirà di n? 2? 2n più 1, ok? x deve avere sta forma, 2n più 1. Con n è un numero naturale. I numeri dispari sono fatti tutti così, ok? Facciamo il quadrato. Voglio provare questo: se x è dispari, il quadrato è dispari. Faccio il quadrato, x al quadrato diventa il quadrato di questo. Svolgo il quadrato, quindi diventa 4n al quadrato più il doppio prodotto 4n più.

00:36:17  
il quadrato di questo è uno e questo è della forma due per qualcosa più uno? Sì, è della forma due che moltiplica 2 n al quadrato più 2 n più 1. quindi questo qua è un altro numero naturale k e ho provato che questo x quadro ha la forma due volte un numero naturale, 1, quindi lui è un numero dispari, x al quadrato è dispari e quindi ho provato questo.

00:36:57  
Vedete l'utilità della contro nominale in molte situazioni, l'implicazione contro nominale è più trasparente dell'implicazione che ci siamo proposti di provare. Lo vedrete in varie situazioni. Bene, abbiamo concluso, quindi domani vi incontrerete con il nuovo docente e invece noi ci vedremo intorno a metà ottobre.

00:37:33  
Va bene, mi raccomando, seguite i miei consigli. Ma quindi domani io devo andare alla 1204? E' la 1204! Molto meglio. Per adesso la lezione tranquilla.

00:38:10  
Ma oddio, giusto capire questi concetti, però più che altro alla fine è il ragionamento umano.