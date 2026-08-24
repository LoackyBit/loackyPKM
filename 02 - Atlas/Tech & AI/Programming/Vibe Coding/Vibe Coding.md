---
status: permanent
type: video
area: tech
related: []
source: "https://www.youtube.com/watch?v=v7UcVPO4y3c"
title: "Vibe Coding"
date: '2025-04-03'
updated: 2026-05-22T18:26
tags: [tech/video, tech/youtube]
summary: "Il vibe coding è un metodo di programmazione che utilizza strumenti basati su IA per scrivere codice in modo collaborativo e iterativo. L’idea è di lasciare che l’IA generi gran parte del codice, m..."
---
[[Home MOC|Home]] / [[Tech & AI MOC|Tech & AI]] / [[Vibe Coding]]

#video [[Vibe Coding]]
https://www.youtube.com/watch?v=v7UcVPO4y3c
---
### **Cos’è il Vibe Coding?**
Il *vibe coding* è un metodo di programmazione che utilizza strumenti basati su IA per scrivere codice in modo collaborativo e iterativo. L’idea è di lasciare che l’IA generi gran parte del codice, mentre l’utente fornisce indicazioni, definisce obiettivi e affina il risultato. Questo approccio è particolarmente utile per chi vuole creare progetti rapidamente o sperimentare senza dover padroneggiare ogni aspetto della programmazione tradizionale.

---

### **1. Strumenti per il Vibe Coding**
Il video presenta diverse opzioni di strumenti per il *vibe coding*, con un’enfasi particolare su Windsurf:

- **Windsurf**: Un editor di codice derivato da Visual Studio Code (VS Code), il più popolare al mondo. Windsurf è progettato per il *vibe coding* e offre funzionalità avanzate come:
  - Modalità chat, scrittura e legacy per interagire con l’IA.
  - Supporto per diversi modelli di IA (es. Claude 3.7, Claude 3.5, modelli Open AI).
  - Completamento con tab sensibile al contesto del codice, del terminale e della documentazione.
  - Anteprima nel browser integrata, che permette di visualizzare il progetto in tempo reale e fornire feedback specifici.
  - Integrazione di URL per documentazione esterna, migliorando la capacità dell’IA di scrivere codice personalizzato.
  Windsurf è il tool preferito dal narratore, che lo utilizza frequentemente per i suoi progetti.

- **Cursor**: Un’altra opzione simile a Windsurf, anch’essa basata su IA, ma non approfondita nel dettaglio.

- **Estensioni per VS Code**: Per chi preferisce restare su VS Code, c’è Klein, un’estensione che abilita funzionalità di *vibe coding*. Il narratore la menziona come valida, pur non avendola testata a fondo.

- **Replet**: Un editor di codice completamente online, ideale per sviluppare e distribuire applicazioni nel cloud con facilità.

- **Canvas nei modelli IA**: Strumenti come Claude, ChatGPT e Google offrono una funzione “canvas” che consente di scrivere ed eseguire codice (soprattutto HTML e JavaScript) direttamente nel browser. È un’opzione semplice per iniziare, ma limitata a progetti meno complessi.

Il narratore sottolinea che per progetti più articolati preferisce Windsurf o Cursor, definiti “agenti” più avanzati rispetto ai semplici canvas, poiché possono iterare sul codice in modo più sofisticato.

---

### **2. Scelta del Linguaggio e dello Stack**
Un aspetto cruciale del *vibe coding* è scegliere il linguaggio di programmazione e lo stack più adatto. Il narratore offre una regola semplice: **optare per i linguaggi più popolari**, perché l’IA è stata addestrata su una quantità maggiore di esempi, garantendo risultati migliori. I suggerimenti principali sono:

- **JavaScript**: Il linguaggio più popolare al mondo, ideale per il front-end (con HTML) e anche per il back-end tramite Node.js.
- **Python**: Considerato il linguaggio standard per l’IA, perfetto per il back-end.

Il narratore utilizza spesso uno stack composto da:
- **Front-end**: HTML e JavaScript.
- **Back-end**: Python (o JavaScript con Node.js).

Per aiutare nella scelta, cita **GitHut 2.0**, una risorsa che mostra i linguaggi più utilizzati (es. Python, Java, JavaScript, C++, TypeScript), e promette di linkarla nella descrizione.

---

### **3. Pianificazione del Progetto**
La pianificazione è una fase fondamentale. Il narratore consiglia di:
- Creare un **piano dettagliato** (Product Requirements Document - PRD) che specifichi cosa si vuole costruire, includendo casi limite e comportamenti attesi.
- Usare l’IA (ad esempio Grok) per generare questo piano. Fornisce un esempio: un’app SaaS per caricare link (articoli, video,论文), riassumerli con l’IA e cercare tra i contenuti salvati.
- Raffinare il piano iterativamente con l’IA, rispondendo a domande tecniche e trasformandolo in un file Markdown (`.md`).
- Creare una **lista di cose da fare** (to-do list) basata sul piano, anch’essa in Markdown, per guidare lo sviluppo passo-passo.

Sottolinea l’importanza di investire tempo in questa fase per evitare problemi futuri, come la gestione di casi limite non previsti.

---

### **4. Controllo di Versione con Git**
Il controllo di versione è essenziale per salvare il codice in diversi stati e rollback in caso di errori. Il narratore introduce:
- **Git**: Il software standard per il controllo di versione. Permette di salvare “commit” (punti di salvataggio) e reverting a versioni precedenti se l’IA rompe il codice.
- **GitHub**: Una piattaforma cloud per archiviare il codice in modo sicuro (come un “Google Docs per codice”), gratuita e facile da configurare con l’aiuto dell’IA.

Anche per chi non conosce Git, l’IA può gestire i comandi (es. `git init`, `git commit`), rendendo il processo accessibile.

---

### **5. Regole per l’IA**
Le “regole” sono istruzioni personalizzate che guidano l’IA nel rispettare lo stile e le preferenze dell’utente, simili a un prompt di sistema per un LLM. In Windsurf, si trovano nelle impostazioni sotto “Memories and Rules”:
- **Regole globali**: Valgono per tutti i progetti (es. “Avvia un nuovo server dopo ogni modifica”).
- **Regole di workspace**: Specifiche per un progetto.

Esempi di regole utili:
- “Cerca di modificare il codice esistente prima di scriverne di nuovo.”
- “Preferisci soluzioni semplici ed evita duplicazioni.”
- “Scrivi codice che consideri gli ambienti dev, test e prod.”

Il narratore cita anche il repository GitHub **Awesome Cursor Rules**, che offre regole predefinite per linguaggi e framework (es. React, Python con FastAPI), utili per adottare best practice.

---

### **6. Flusso di Lavoro del Vibe Coding**
Il flusso di lavoro consigliato è:
1. **Riferirsi al piano e alla to-do list**: L’IA legge questi documenti per sapere cosa fare.
2. **Sviluppare una feature alla volta**: Concentrarsi su un elemento per volta.
3. **Scrivere test**: Codice separato che verifica il funzionamento della feature.
4. **Eseguire i test**: Prima per la nuova feature, poi per l’intero progetto.
5. **Risolvere i test falliti**: Correggendo il codice o i test stessi.
6. **Commit del codice**: Salvare i progressi con Git e, se necessario, caricarli su GitHub.
7. **Ripetere**: Continuare iterativamente.

Se l’IA rovina il codice, si può rollback a un commit precedente con comandi come `git revert` o `git stash`, gestiti dall’IA.

---

### **7. Suggerimenti Aggiuntivi**
- **Modalità Chat vs Write**: In Windsurf, “write” genera codice, “chat” risponde a domande con il contesto del progetto.
- **Template per il front-end**: Per interfacce belle, usare template gratuiti (es. Bootstrap) e integrarli con l’IA.
- **3.js per giochi**: Una libreria JavaScript 3D popolare per creare giochi con l’IA.
- **Sicurezza**: Aggiungere regole per best practice (es. limitazione delle richieste API) e chiedere audit di sicurezza all’IA.
- **Manutenzione**: L’IA può refactoring il codice per renderlo più modulare.
- **MCP Server**: Funzionalità avanzata di Windsurf per aggiungere strumenti all’IA (es. Unity, Firecrawl per ricerche profonde).

---
## Collegamenti
