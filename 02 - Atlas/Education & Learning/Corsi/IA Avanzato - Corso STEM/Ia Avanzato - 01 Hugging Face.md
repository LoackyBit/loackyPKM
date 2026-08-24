---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 01 Hugging Face"
date: '2025-01-31'
updated: 2026-07-07T01:20
tags: []
summary: "La Home Page e Navigazione:"
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Ia Avanzato - 01 Hugging Face]]

[[IA Avanzato]]
# UI - Interfaccia utente

La Home Page e Navigazione:

- In alto trovi una barra di ricerca per trovare modelli, dataset e spazi
- Il menu principale include: Models, Datasets, Spaces, Docs e Solutions
- Puoi accedere/registrarti tramite il pulsante in alto a destra

La sezione Models:

- Catalogo di modelli di machine learning pre-addestrati
- Filtri per tipo di task o **modal**(traduzione, sintesi, classificazione, **NLP**, ecc.)
- Possibilità di cercare per linguaggio, licenza e framework
- Per ogni modello trovi:
    - Descrizione e parametri
    - Metriche di performance
    - Esempi di utilizzo
    - Widget per provare il modello direttamente nel browser
    - Codice di esempio per l'implementazione

La sezione Datasets:

- Raccolta di dataset per addestrare/testare modelli
- Organizzati per task e dominio
- Informazioni su formato, dimensione e licenza
- Possibilità di visualizzare e scaricare i dati
- Documentazione sull'utilizzo

Gli Spaces:

- App dimostrative create dalla community
- Interfacce web per provare i modelli
- Possibilità di creare i propri spazi
- Notebook interattivi e demo

Altri strumenti:

- AutoTrain: per addestrare modelli senza codice
- Inference API: per utilizzare i modelli via API
- Model Hub: per ospitare e versionare i propri modelli
- Datasets Hub: per condividere dataset

Funzionalità collaborative:

- Discussioni e issue tracker per ogni risorsa
- Sistema di valutazione e feedback
- Possibilità di contribuire e fare fork
- Documentazione collaborativa

Il Model Hub permette di:

- Caricare modelli addestrati
- Gestire diverse versioni
- Configurare pipeline di CI/CD
- Monitorare metriche e performance
- Condividere con la community

La documentazione include:

- Guide per iniziare
- Tutorial dettagliati
- Riferimenti API
- Best practice
- Esempi di codice

# Bert base model

### Cos'è BERT in breve?

BERT è un modello di machine learning che "capisce" il significato delle parole basandosi sul contesto attorno a esse (sia prima che dopo). È usato per compiti come traduzione, classificazione di testi e risposte a domande.

### Cosa vuol dire che si basa sulle maschere?

Durante l'addestramento, BERT "oscura" (maschera) alcune parole in una frase e impara a predirle usando il contesto delle altre parole. Ad esempio, nella frase:

> "Il [MASK] corre veloce",
> 
> BERT deve capire che il termine mancante potrebbe essere "cavallo" o "bambino" basandosi sul resto della frase.

### Cosa sono i parametri?

I parametri sono numeri che il modello impara durante l'addestramento, come pesi e bias nelle reti neurali. Questi determinano come il modello prende decisioni (ad esempio, come valuta una parola rispetto alle altre). Più parametri ha un modello, maggiore è la sua capacità di apprendere dettagli complessi, ma richiede più risorse computazionali.

### Confronto dei parametri:

- **TensorFlow Playground**: I modelli lì sono semplici, con 20-30 parametri in media (ad esempio, per una rete con pochi neuroni e strati).
- **BERT Base**: Ha **110 milioni di parametri**, una quantità enorme! Questo numero deriva dalla sua architettura con molti strati (12), neuroni per strato (768), e connessioni interne complesse.

# “Questa mattina”

La tastiera predittiva degli iPhone, basata sull'intelligenza artificiale di Apple, funziona in modo diverso rispetto ad alcune tastiere su dispositivi Android, come Gboard di Google. Vediamo le differenze chiave e perché si verifica il comportamento descritto.

### **Tastiera dell'iPhone e predizione delle parole**

Quando digiti "questa mattina" e premi ripetutamente il tasto al centro dei suggerimenti, la tastiera predittiva di iPhone tende a generare sempre la **stessa sequenza di parole**. Questo succede perché il sistema predittivo:

1. Si basa su modelli di linguaggio statici e deterministici che sono ottimizzati per la coerenza, e non usa un seme ("seed") casuale.
2. Impara dai tuoi schemi di scrittura e, in assenza di un contesto variabile, genera sempre la frase più probabile in base ai dati pre-addestrati o al tuo utilizzo passato.

Nel tuo esempio:

- Scrivendo "questa mattina", la tastiera prevede automaticamente una sequenza che rappresenta un contesto comune nella lingua italiana: "sono andato in banca per il bonifico di un mutuo e mi sono accorto di".

Questo approccio è utile per **risultati prevedibili** e coerenti, ma limita la varietà creativa.

---

### **Tastiere su Android (es. Gboard)**

Le tastiere Android, come Gboard, funzionano in modo leggermente diverso:

1. Utilizzano **semi casuali (seed)** per introdurre variabilità nella generazione delle frasi.
2. Possono sfruttare modelli probabilistici avanzati per creare alternative leggermente diverse, anche partendo dalla stessa frase.

Ad esempio, con "questa mattina", la stessa operazione potrebbe portare a frasi differenti, come:

- "Questa mattina ho preso un caffè al bar."
- "Questa mattina sono andato a fare la spesa."
- "Questa mattina mi sono svegliato presto."

La variabilità viene introdotta intenzionalmente per rendere il modello più flessibile e adattabile a un'ampia gamma di contesti.

---

### **Perché questa differenza?**

- **Apple** punta sulla semplicità e sulla prevedibilità. La frase generata è sempre la stessa perché l'obiettivo è fornire un risultato "sicuro" basato su dati consolidati.
- **Google** (e altre tastiere Android) invece sfrutta tecniche di generazione più avanzate e variabili, che offrono maggiore creatività ma meno consistenza.

In breve, la tastiera dell'iPhone **non introduce casualità**, mentre le tastiere Android spesso lo fanno per offrire risultati più vari.

# Dataset

### **Che cos'è un dataset?**

Un **dataset** è una raccolta strutturata di dati, organizzata in modo da poter essere utilizzata per analisi, addestramento di modelli di machine learning o qualsiasi altro scopo specifico. Ogni elemento di un dataset rappresenta un'unità di dati, come una riga in un foglio Excel o un'immagine in una cartella.

Un dataset può contenere:

- **Dati tabulari**: Tabelle con righe e colonne (es., file CSV o database).
- **Dati testuali**: Documenti, articoli, conversazioni, ecc.
- **Immagini**: Foto o grafici.
- **Video o audio**: File multimediali per analisi avanzate.

---

### **Come si crea un dataset?**

Creare un dataset comporta diversi passaggi, che dipendono dal tipo di dati e dall'obiettivo. Ecco un processo generale:

### 1. **Definire lo scopo**

- Qual è il tuo obiettivo? Es. Addestrare un modello per classificare immagini o analizzare recensioni di prodotti.
- Quali tipi di dati servono? Es. Testo, immagini, numeri.

### 2. **Raccogliere i dati**

- **Dati esistenti**: Cerca dataset pubblici, ad esempio su piattaforme come [Kaggle](https://www.kaggle.com/) o [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php).
- **Nuova raccolta**:
    - **Manuale**: Inserisci manualmente i dati (es. tramite fogli Excel).
    - **Automatica**: Scrivi script per scaricare dati da API o web scraping.
    - **Strumenti e app**: Usa piattaforme per sondaggi, software di gestione dati o sensori.

### 3. **Organizzare e strutturare i dati**

- I dati devono essere puliti e ben organizzati. Es.:
    - Tabelle: Colonne per attributi (es. "Nome", "Età") e righe per osservazioni.
    - Immagini: Nome file e cartelle per categorie.
- Formati comuni:
    - **CSV** o **Excel** per dati tabulari.
    - **JSON** o **XML** per dati gerarchici.
    - File **.jpg**, **.png**, **.wav**, ecc., per dati multimediali.

### 4. **Pulizia dei dati**

I dati grezzi spesso contengono errori, duplicati o valori mancanti. La pulizia dei dati è cruciale e comporta:

- Rimuovere duplicati.
- Correggere errori di ortografia o formattazione.
- Gestire valori mancanti (es. sostituendoli o eliminandoli).

### 5. **Annotare i dati**

Se stai creando un dataset per il machine learning, potresti dover aggiungere etichette (es. "Cane" o "Gatto" per immagini, "Positivo" o "Negativo" per sentimenti).

### 6. **Esportare o salvare il dataset**

Salva il dataset in un formato compatibile con i tuoi strumenti. Ad esempio:

- **CSV** o **Parquet** per analisi dati.
- **TFRecord** o **HDF5** per modelli di deep learning.

---

### **Esempio semplice di dataset**

Se vuoi creare un dataset per prevedere il prezzo delle case, puoi raccogliere dati come:

|ID|Superficie (m²)|Numero di stanze|Prezzo (€)|
|---|---|---|---|
|1|80|3|150,000|
|2|120|4|250,000|
|3|60|2|100,000|

Puoi creare questo dataset in un foglio Excel o un file CSV.

---

### **Strumenti utili per creare dataset**

- **Foglio di calcolo**: Excel, Google Sheets.
- **Programmazione**: Python (con librerie come `pandas`, `openpyxl`, `requests`).
- **Web scraping**: `BeautifulSoup`, `Scrapy`.
- **Dataset annotators**: Label Studio, Prodigy (per etichettatura manuale).

Un dataset ben fatto è il fondamento di qualsiasi progetto basato sui dati!

# Scraping

Lo **scraping** (cioè la raccolta automatica di dati da siti web) non è intrinsecamente immorale, ma può sollevare questioni **etiche** e **legali** a seconda di come viene effettuato e dello scopo per cui è utilizzato. La moralità dello scraping dipende dal contesto e dal rispetto delle norme e dei principi fondamentali. Vediamo i punti chiave:

---

### **Quando lo scraping può essere considerato accettabile?**

1. **Accesso a dati pubblici**: Se i dati sono già pubblici e accessibili a chiunque (ad esempio, liste di prodotti o articoli di notizie), lo scraping può essere moralmente accettabile, a patto di rispettare i termini di servizio del sito e il buon senso (es., non sovraccaricare i server).
2. **Ricerca o analisi non commerciali**: Se è usato per scopi di ricerca, educativi o di interesse pubblico (ad esempio, analisi di fenomeni sociali o studi scientifici), è generalmente considerato più giustificabile.
3. **Consenso implicito o esplicito**: Se il sito web dichiara chiaramente che i suoi dati possono essere raccolti o condivisi (ad esempio, tramite API ufficiali), allora lo scraping è lecito sia dal punto di vista legale che etico.

---

### **Quando lo scraping può essere considerato immorale?**

1. **Violazione della privacy**: Scraping di dati sensibili o personali senza il consenso degli utenti (ad esempio, informazioni di profili social) è sia immorale che illegale in molti paesi.
2. **Uso dannoso**:
    - Creare copie di un sito web per sottrarre traffico o guadagni.
    - Raccolta di dati per scopi di phishing, spam o frodi.
3. **Violazione dei termini di servizio**: Molti siti web specificano nei loro **Termini di utilizzo** che lo scraping è proibito. Ignorare queste regole può essere visto come una violazione della fiducia.
4. **Sovraccarico di server**: Effettuare scraping in modo aggressivo può danneggiare le infrastrutture di un sito web (es., rallentandolo o causandone il crash). Questo è immorale perché impatta negativamente sugli altri utenti.

---

### **Esempi concreti di dilemmi etici**

1. **Social media scraping**: Raccolta massiva di dati pubblici da piattaforme come Facebook o LinkedIn. Anche se i dati sono pubblici, il loro uso senza consenso (ad esempio, per creare profili o fare targeting) può essere considerato una violazione della privacy.
2. **Prezzi dei concorrenti**: Scraping di prezzi da siti e-commerce per battere la concorrenza. Se fatto senza autorizzazione, potrebbe essere percepito come una pratica sleale.
3. **Raccolta di informazioni personali**: Anche se i dati sono pubblicamente visibili (ad esempio, indirizzi e-mail su una pagina), il loro utilizzo per fini commerciali senza consenso può essere immorale.

---

### **Come fare scraping in modo etico**

1. **Rispettare i termini di servizio** del sito web.
2. **Utilizzare API ufficiali**, se disponibili, invece di raccogliere dati direttamente dalle pagine.
3. **Non raccogliere dati sensibili** o personali senza esplicito consenso.
4. **Limitare il carico sul server**: Ad esempio, usando una frequenza bassa e rispettando i file `robots.txt` (che indicano le aree del sito che è possibile o non possibile visitare automaticamente).
5. **Chiarire lo scopo**: Se stai raccogliendo dati per ricerca o analisi, considera di avvisare il proprietario del sito.

---

### **Conclusione**

Lo scraping non è intrinsecamente immorale, ma può diventarlo a seconda del **modo in cui viene fatto** e dello **scopo finale**. Per rimanere etici:

- Raccogli solo dati non sensibili.
- Rispetta le regole del sito.
- Assicurati che il tuo utilizzo non causi danni o violazioni della privacy.

---

# Tagging

Il **tagging delle immagini** è il processo di assegnare **etichette** o **parole chiave** (tag) a un'immagine per descrivere il suo contenuto. Questo aiuta i sistemi a comprendere e categorizzare le immagini, rendendole più facili da cercare, analizzare o utilizzare in applicazioni come l'addestramento di modelli di machine learning.

### **Come funziona il tagging?**

1. **Manuale**: Gli esseri umani osservano l'immagine e assegnano tag basati su ciò che vedono (es. "gatto", "cane", "natura").
2. **Automatico**: Sistemi di intelligenza artificiale, come le reti neurali convoluzionali (CNN), analizzano l'immagine per riconoscere oggetti, scene o attività e assegnano tag automaticamente.

### **Esempi di utilizzo**

- **Archiviazione**: Organizzare grandi raccolte di immagini in base al loro contenuto.
- **E-commerce**: Classificare prodotti in base alle immagini (es. "maglia", "scarpa").
- **Machine Learning**: Creare dataset etichettati per addestrare modelli di riconoscimento delle immagini.
- **Motori di ricerca**: Trovare immagini specifiche basandosi sui tag.

### **Strumenti comuni**

- Software di tagging manuale: Label Studio, CVAT.
- Modelli pre-addestrati: Microsoft Azure Computer Vision, Google Vision AI, Hugging Face.

Il tagging, sia manuale che automatico, è essenziale per creare dataset affidabili e per migliorare le capacità delle applicazioni basate su immagini.

# Descrizione delle immagini

![[Pasted image 20250201222709.png]]

Nei dataset di immagini su **Hugging Face**, le sezioni **"rejected"** e **"chosen"** si riferiscono tipicamente alla classificazione o selezione delle descrizioni associate alle immagini. Questo è particolarmente utile nei dataset che coinvolgono modelli di linguaggio o applicazioni di **visione-linguaggio**, come CLIP o modelli simili. Ecco una descrizione sintetica di entrambe:

---

### **Sezione "chosen"**

La sezione **"chosen"** contiene descrizioni delle immagini che sono state **selezionate** come quelle più pertinenti, accurate o utili per rappresentare il contenuto dell'immagine.

Queste descrizioni:

- Vengono considerate "corrette" o "ideali".
- Possono essere il risultato di un'annotazione manuale o di un filtro automatico basato su metriche di qualità.
- Sono usate per addestrare i modelli con dati puliti e rappresentativi.

**Esempio:** Un'immagine di un gatto potrebbe avere una descrizione in "chosen" come:

> "A child stands in the snow, dressed in a ski parka and holding two skis. The child is also wearing a beanie hat on their head. There are…"

---

### **Sezione "rejected"**

La sezione **"rejected"** contiene descrizioni che sono state **scartate** perché considerate:

- Inaccurate o ambigue.
- Rumorose o di bassa qualità (ad esempio, descrizioni generiche come "immagine" o "qualcosa di interessante").
- Generate automaticamente ma non ritenute adeguate rispetto all'immagine.

Queste descrizioni non vengono usate direttamente per l'addestramento, ma possono essere utili per analisi successive o per migliorare il filtraggio.

**Esempio:** Per la stessa immagine del gatto, una descrizione in "rejected" potrebbe essere:

> "A young boy (è un bambino) wearing a red jacket (non è un giacchetto) is skiing, holding two ski poles. He's near several Norwegian flags planted in the snow, and his…”

---

### **Perché queste sezioni sono importanti?**

1. **Qualità del dataset**: Separare le descrizioni accurate da quelle inutilizzabili migliora l'efficacia nell'addestramento dei modelli.
2. **Analisi e debug**: Permette ai ricercatori di capire quali descrizioni funzionano e quali no, ottimizzando i processi di annotazione o generazione automatica.
3. **Valutazione dei modelli**: Sezioni come queste possono essere usate per misurare quanto bene un modello discrimina tra descrizioni buone e cattive.

In sintesi, le sezioni **"chosen"** e **"rejected"** aiutano a mantenere la qualità e la coerenza dei dataset su Hugging Face!

# Spazi

La **sezione "Spaces"** su Hugging Face è una piattaforma che permette agli utenti di **creare, condividere ed eseguire applicazioni di machine learning e IA interattive**. Gli Spaces sono ambienti pronti per ospitare e condividere progetti, come demo di modelli di intelligenza artificiale, strumenti di visualizzazione, o applicazioni basate su machine learning.

---

### **Caratteristiche principali degli Spaces**

1. **Hosting di applicazioni IA** Gli Spaces permettono agli utenti di pubblicare applicazioni basate su:
    - **Modelli pre-addestrati** presenti nella piattaforma Hugging Face.
    - Algoritmi personalizzati sviluppati dagli utenti.
2. **Framework supportati** Hugging Face Spaces supporta tre principali framework:
    - **Gradio**: Semplice e intuitivo, ideale per creare interfacce utente con pochi passaggi.
    - **Streamlit**: Framework per dashboard interattive e applicazioni di data science.
    - **HTML + JavaScript**: Per personalizzazioni avanzate.
3. **Esecuzione immediata** Gli Spaces girano su un'infrastruttura gestita da Hugging Face, eliminando la necessità di configurare server. Basta caricare il codice, e l'applicazione è subito accessibile.
4. **Collaborazione e condivisione**
    - Gli Spaces possono essere **pubblici** (visibili a tutti) o **privati** (accessibili solo a utenti autorizzati).
    - Gli sviluppatori possono invitare altri utenti a collaborare.
5. **Risorse personalizzabili** Gli Spaces offrono opzioni di configurazione per CPU, GPU o TPU, a seconda delle esigenze computazionali del progetto.

---

### **Come creare uno Space**

1. **Vai alla sezione Spaces**: [Hugging Face Spaces](https://huggingface.co/spaces).
2. **Crea un nuovo Space**:
    - Clicca su "Create Space".
    - Assegna un nome al tuo Space.
    - Scegli un framework (Gradio, Streamlit, o HTML).
    - Configura la visibilità (pubblica o privata).
3. **Carica il tuo progetto**:
    - Inserisci il codice sorgente (es. file Python o HTML).
    - Aggiungi i file necessari (es. modelli o dati).
4. **Esegui lo Space**: Dopo il caricamento, l'app sarà subito disponibile all'URL generato.

---

### **Esempi di utilizzo**

1. **Dimostrazioni di modelli IA**:
    - Chatbot basati su modelli NLP come GPT o BERT.
    - Classificatori di immagini o audio.
2. **Strumenti interattivi**:
    - App per la generazione di immagini da testo.
    - Traduttori automatici in tempo reale.
3. **Data visualization**:
    - Dashboard per l'analisi di dati con Streamlit o visualizzazioni in tempo reale.

---

### **Vantaggi**

- **Facilità d'uso**: Non è necessario configurare server o infrastrutture.
- **Collaborazione globale**: Gli Spaces pubblici possono essere utilizzati da chiunque.
- **Scalabilità**: Le risorse vengono gestite automaticamente per supportare il carico dell'applicazione.

---

In sintesi, gli Spaces di Hugging Face sono uno strumento potente e accessibile per sviluppatori, ricercatori e appassionati di IA per condividere il proprio lavoro con il mondo in modo rapido e professionale!

# Storicità dei modelli di NLP

Ecco alcuni punti di riferimento nella (breve) storia dei modelli Transformer:

![[Pasted image 20250201223942.png]]

L' [**architettura Transformer**](https://arxiv.org/abs/1706.03762) è stata introdotta a giugno 2017. Il focus della ricerca originale era sulle attività di traduzione.

---

## **I trasformatori sono modelli linguistici**

Tutti i modelli Transformer sopra menzionati (GPT, BERT, BART, T5, ecc.) sono stati addestrati come _modelli linguistici_ . Ciò significa che sono stati addestrati su grandi quantità di testo grezzo in modo auto-supervisionato. L'apprendimento auto-supervisionato è un tipo di addestramento in cui l'obiettivo viene automaticamente calcolato dagli input del modello. Ciò significa che non è necessario che gli esseri umani etichettino i dati!

Questo tipo di modello sviluppa una comprensione statistica del linguaggio su cui è stato addestrato, ma non è molto utile per compiti pratici specifici. Per questo motivo, il modello pre-addestrato generale passa attraverso un processo chiamato _apprendimento per trasferimento_ . Durante questo processo, il modello viene messo a punto in modo supervisionato, ovvero utilizzando etichette annotate dall'uomo, su un dato compito.

Un esempio di compito è prevedere la parola successiva in una frase dopo aver letto le _n_ parole precedenti. Questo è chiamato _modellazione linguistica causale_ perché l'output dipende dagli input passati e presenti, ma non da quelli futuri.

---

A parte alcuni casi anomali (come DistilBERT), la strategia generale per ottenere prestazioni migliori consiste nell'aumentare le dimensioni dei modelli e la quantità di dati su cui vengono preaddestrati.

![[Pasted image 20250201224002.png]]

Sfortunatamente, addestrare un modello, specialmente uno di grandi dimensioni, richiede una grande quantità di dati. Ciò diventa molto costoso in termini di tempo e risorse di calcolo. Si traduce persino in impatto ambientale, come si può vedere nel grafico seguente.

---
## Collegamenti
