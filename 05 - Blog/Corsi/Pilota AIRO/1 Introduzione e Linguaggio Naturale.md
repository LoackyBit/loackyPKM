---
stage: fine-tuned 🧠
draft: false
type: article
area: education
related: []
source: original
title: "01 Introduzione e Linguaggio Naturale"
date: '2026-01-23'
updated: 2026-07-12T22:56
tags: []
summary: "Analisi Strategica: Il corso \"Laboratorio di Programmazione di Robot Sociali e Intelligenza Artificiale\" si pone come un ponte metodologico tra la programmazione deterministica tradizionale e la nu..."
---
[[Home MOC|Home]] / [[Blog]] / [[1 Introduzione e Linguaggio Naturale|01 Introduzione e Linguaggio Naturale]]

[[Pilota AIRO]]
# [[Pilota Airo - 01 Introduzione e Linguaggio Naturale]]
## 1. Introduzione al Corso e all'Ecosistema SMARRtino

**Analisi Strategica:** Il corso **"Laboratorio di Programmazione di Robot Sociali e Intelligenza Artificiale"** si pone come un ponte metodologico tra la programmazione deterministica tradizionale e la nuova era della Generative AI (GenAI). In un contesto tecnologico dove l'interazione uomo-macchina diventa sempre più semantica, questo percorso formativo abilita lo studente a governare sistemi complessi attraverso il linguaggio naturale. L'utilizzo strategico dei **Sapienza Remote Labs (SRL)** risponde alla necessità di democratizzare l'accesso alla robotica d'avanguardia: spostando l'hardware nel cloud, eliminiamo le barriere economiche e logistiche, permettendo una sperimentazione continua su sistemi reali e simulati indipendentemente dalla posizione geografica dell'utente.

### Obiettivi Didattici

Il corso è strutturato per fornire una padronanza pratica dei seguenti pilastri:

- **Robotica Sociale:** Progettazione di comportamenti e dinamiche di interazione naturale.
- **Machine Learning e GenAI:** Integrazione di Large Language Models (LLM) e Vision Language Models (VLM) nel loop di controllo robotico.
- **Architetture di Sistema:** Comprensione dei protocolli di comunicazione in tempo reale e del middleware robotico.

### Sapienza Remote Labs (SRL): L'Ambiente Abilitante

L'infrastruttura SRL rappresenta il framework operativo del corso. L'accesso avviene tramite una configurazione VPN che garantisce un tunnel sicuro verso il laboratorio, permettendo al PC dello studente di interagire direttamente con il simulatore basato su cloud. Questa architettura è fondamentale perché astrae la gestione dell'hardware fisico, permettendo allo studente di focalizzarsi interamente sulla logica di controllo e sull'integrazione dell'intelligenza artificiale.

### Hardware SMARRtino: Caratteristiche e Vincoli Tecnici

Il robot SMARRtino è un sistema educativo mobile ottimizzato per l'interazione sociale. Basandoci sulle specifiche tecniche, la sua configurazione include:

- **Cinematica:** Una base mobile dotata di due ruote motrici indipendenti e una _caster wheel_ posteriore per la stabilità. Il robot opera esclusivamente su una **superficie planare (2D)**.
- **Attuatori:**
    - **Braccia articolate:** Due braccia (destra e sinistra) con escursione verticale da 0° (posizione di riposo) a 180° (sopra la testa). **Nota bene:** Il sistema non è dotato di pinze o manipolatori; pertanto, non può eseguire compiti di manipolazione fisica di oggetti.
    - **Testa Pan-Tilt:** Sistema a due gradi di libertà per l'orientamento del campo visivo. I limiti operativi sono rigorosi: **Pan** (rotazione orizzontale) tra -90° (destra) e 90° (sinistra); **Tilt** (inclinazione verticale) tra -30° (giù) e 30° (su).
- **Sensori e Interazione:** Fotocamera integrata per l'acquisizione di immagini e interfaccia vocale per sintesi e riconoscimento del parlato.

**Transizione:** L'efficacia di questo hardware non dipende solo dalla sua meccanica, ma dalla robustezza del "sistema nervoso" digitale che permette lo scambio di comandi e feedback: l'architettura WebSocket.

--------------------------------------------------------------------------------

## 2. Architettura di Comunicazione: WebSocket e Dynamic Method Invocation

**Analisi Strategica:** L'adozione di un sistema Client-Server basato su protocollo WebSocket è una scelta architetturale critica. A differenza dei protocolli request-response tradizionali, le WebSocket offrono un canale bidirezionale e persistente. Questo è vitale nella robotica per garantire una teleoperazione a bassa latenza e un feedback sensoriale immediato, trasformando il robot da entità isolata a nodo reattivo di una rete distribuita.

### Il Protocollo WebSocket (robot_client.py)

All'interno della classe `WS`, la gestione della comunicazione è affidata a un meccanismo di sincronizzazione basato su `threading.Event()`. Sebbene il protocollo sottostante sia asincrono, il metodo `send()` è progettato per essere **bloccante**. Questa scelta è fondamentale dal punto di vista didattico e operativo: impedisce allo script Python dello studente di inviare nuovi comandi prima che il robot abbia confermato l'esecuzione del precedente, evitando che la logica software "corra" più velocemente del movimento fisico o simulato della macchina.

### Il Pattern "Dynamic Method Invocation"

La classe `Robot` utilizza il metodo dunder `__getattr__` per implementare un'invocazione dinamica dei metodi.

- **Valutazione dell'Impatto:** Questo pattern non è una semplice comodità sintattica, ma una scelta di **disaccoppiamento strategico**. Permette di separare l'interfaccia client dalle API del server: se nuove funzionalità vengono aggiunte al firmware del robot remoto, il client può invocarle immediatamente senza alcuna modifica al codice locale della libreria `robot_client.py`.

### Snippet Tecnico: Implementazione di `__getattr__`

```python
def __getattr__(self, name):
    def wrapper(*args, **kwargs):
        # Utilizziamo repr(v) per garantire che i tipi di dato (es. stringhe virgolettate)
        # siano preservati correttamente nella stringa di comando finale.
        pos_args_str = ", ".join(map(repr, args))
        kw_args_str = ", ".join([f"{k}={repr(v)}" for k, v in kwargs.items()])
        
        # Costruzione della stringa che verrà eseguita dall'interprete remoto
        all_params = ", ".join(filter(None, [pos_args_str, kw_args_str]))
        full_call_str = f"robot.{name}({all_params})"
        
        r = None
        if self.ws_robot:
            r = self.ws_robot.send(full_call_str)
        return r
    return wrapper
```

**Nota tecnica:** L'uso di `repr()` è cruciale: assicura che una stringa passata come argomento rimanga una stringa (es. `"ciao"`) nella chiamata remota, garantendo la compatibilità con l'interprete Python che riceve il comando.

**Transizione:** Questa architettura di comunicazione trasparente fornisce la base perfetta per l'integrazione di moduli di intelligenza artificiale, capaci di generare autonomamente queste chiamate a partire da semplici istruzioni verbali.

--------------------------------------------------------------------------------

## 3. Integrazione AI e Prompt Engineering (Modulo 1)

**Analisi Strategica:** Il modulo `ai.py` funge da traduttore semantico tra l'intento umano e il codice macchina. L'impiego del modello `gpt-5-nano` risponde a una logica di efficienza ingegneristica: offre capacità di ragionamento logico superiori necessarie per la generazione di codice, mantenendo al contempo una latenza ridotta e costi operativi sostenibili per un ambiente di laboratorio.

### I Tre Pilastri del Sistema (System Prompts)

Il comportamento dell'AI è guidato da tre prompt di sistema definiti nel codice:

- **Chat Mode:** Ottimizzato per interazioni colloquiali brevi e naturali.
- **Code Mode:** Il modulo core per la programmazione. Richiede una precisione sintattica assoluta per mappare le richieste su funzioni come `robot.forward(m)` o `robot.tilt(deg)`.
- **Vision Mode:** Integra capacità multimodali permettendo al robot di interpretare visivamente l'ambiente. Questa modalità utilizza come input i dati acquisiti tramite la funzione `robot.get_image()`.

### Tecniche Avanzate di Prompt Engineering

- **Few-Shot Learning:** Il sistema include esempi specifici nel `code_system` (es: _"to turn around, use 'robot.left(180)'"_). Questi esempi istruiscono il modello sul formato atteso, riducendo le ambiguità nella traduzione di comandi complessi.
- **Self-commenting Code:** Il prompt impone all'AI di aggiungere commenti a ogni riga di codice prodotta. Questa non è solo una pratica di buona documentazione, ma una forma di **Chain-of-Thought (CoT) implicita**: obbligando il modello a descrivere l'azione prima o durante la generazione del comando, si riducono drasticamente le allucinazioni logiche e gli errori di sintassi.

### Monitoraggio e Logica di Costo

La classe `AI` implementa un tracciamento rigoroso dei consumi. I costi stimati per il modello `gpt-5-nano` sono calcolati come segue:

- **Input:** $0.05 per 1 milione di token.
- **Output:** $0.40 per 1 milione di token (inclusi i reasoning token). Tutte le transazioni vengono archiviate nel file `ai.log` per consentire l'audit delle performance e dei costi.

**Transizione:** Una volta compresa la logica di traduzione dell'AI, è necessario configurare l'ambiente locale per rendere il sistema operativo e pronto all'esecuzione.

--------------------------------------------------------------------------------

## 4. Setup Operativo e Workflow di Implementazione

**Analisi Strategica:** La fase di setup è il momento in cui l'architettura software incontra l'ambiente di esecuzione. Una configurazione meticolosa è l'unico modo per garantire che la catena di comando — dall'input dell'utente alla risposta del robot — sia priva di colli di bottiglia o errori di dipendenza.

### Prerequisiti e Dipendenze

Il sistema richiede l'uso di Python 3.12 o superiore. I pacchetti necessari includono `openai`, `pytz`, `chromadb` e `ollama`. **Avvertenza Cruciale:** È tassativo installare esclusivamente il pacchetto `websocket-client`. L'installazione simultanea del pacchetto denominato semplicemente `websocket` genererà conflitti fatali nel modulo di comunicazione, impedendo la connessione al simulatore.

### Gestione della Sicurezza (API Keys)

Il modulo `ai.py` gestisce l'autenticazione OpenAI con una logica di fallback a due livelli:

1. **Variabile d'Ambiente:** Cerca inizialmente `OPENAI_API_KEY` nel sistema.
2. **File Locale:** Se la variabile non è definita, tenta di leggere la chiave dal file `key.txt` presente nella directory di lavoro.

### Esempio di Esecuzione Finale

Il seguente esempio mostra l'integrazione pratica tra i moduli `Robot` e `AI`:

```python
from ai import AI
from robot_client import Robot

# Inizializzazione dei moduli
robot = Robot()
ai = AI()

# Definizione dell'intento umano
prompt = "Vai avanti di mezzo metro, guarda a sinistra e alza il braccio destro"

# Generazione del codice (Traduzione semantica)
codice_python = ai.code(prompt)
print(f"Codice generato dall'AI:\n{codice_python}")

# Esecuzione (Safety Note: exec() è potente ma va usato solo su codice proveniente da prompt di sistema validati per evitare esecuzioni arbitrarie)
try:
    exec(codice_python)
except Exception as e:
    print(f"Errore durante l'esecuzione del comando robotico: {e}")
```

### Conclusione

La programmazione in linguaggio naturale rappresenta l'ultima frontiera dell'astrazione software. Attraverso l'ecosistema SMARRtino, la complessità dei protocolli WebSocket e della cinematica robotica viene nascosta dietro un'interfaccia intuitiva. Questo permette al programmatore di spostare il focus dalla "scrittura di righe di codice" alla "progettazione di comportamenti sociali", abilitando un'interazione robotica realmente intelligente e accessibile.

---
## Collegamenti
