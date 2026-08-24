---
stage: fine-tuned 🧠
draft: false
type: article
area: education
related: []
source: original
title: "04 Interazione Umana e Messaggi"
date: '2026-02-24'
updated: 2026-07-12T21:34
tags: []
summary: "Il passaggio dalla navigazione autonoma all'interazione sociale rappresenta un salto di paradigma nell'architettura di SMARRtino. Non operiamo più in un ambiente di soli ostacoli fisici, ma in un e..."
---
[[Home MOC|Home]] / [[Blog]] / [[4 Interazione Umana e Messaggi|04 Interazione Umana e Messaggi]]

[[Pilota AIRO]]
# Pilota AIRO - 04 Interazione Umana e Messaggi: Comunicazione e Collaborazione nel Sistema SMARRtino

## 1. Introduzione all'Interazione Sociale

Il passaggio dalla navigazione autonoma all'interazione sociale rappresenta un salto di paradigma nell'architettura di SMARRtino. Non operiamo più in un ambiente di soli ostacoli fisici, ma in un ecosistema collaborativo dove il robot deve agire come un agente sociale. Questo richiede la capacità di integrare entità umane simulate e di gestire flussi comunicativi che non interferiscano con i cicli di controllo motorio.

L'obiettivo del Modulo 4 è l'implementazione di un'infrastruttura di messaggistica asincrona che permetta al robot, all'ambiente e alle persone virtuali di scambiarsi informazioni in modo fluido. Trasformiamo così un semplice esecutore di traiettorie in un collaboratore intelligente, capace di interpretare il linguaggio naturale e coordinarsi con altri agenti. Il fondamento di questa evoluzione risiede nella creazione di una presenza antropomorfa all'interno del simulatore Gazebo.

## 2. Simulazione e Dialogo: La Persona nell'Ambiente Gazebo

Nella robotica sociale, la simulazione di esseri umani è fondamentale per validare le logiche di interazione uomo-macchina (HRI) in totale sicurezza. Questo approccio permette di testare scenari complessi senza rischi fisici per l'utente o danni hardware al robot durante la fase di debug degli agenti AI.

### Analisi Tecnica: Dynamic Proxying con Human Client

L'inserimento di una persona nel simulatore avviene tramite `human_client.py`. Utilizzando il comando `gz.add_object("mario", "person_standing", "1.5 -1.0 0 0 0 -2.2")`, instanziamo il modello "mario". La classe `Human` implementa un pattern di **Dynamic Proxying** estremamente efficiente. Attraverso il metodo dunder `__getattr__`, la classe intercetta ogni chiamata a metodi non definiti localmente e la incapsula in una stringa di comando inviata via WebSocket:

```python
# Estratto concettuale di human_client.py
def __getattr__(self, name):
    def wrapper(*args, **kwargs):
        # Invocazione dinamica: trasforma human.say("Ciao") in comando per il simulatore
        full_call_str = f"human.{name}({all_params})"
        return self.ws.send(full_call_str)
    return wrapper
```

Questa architettura permette al client di rimanere snello: qualsiasi nuova funzione aggiunta al simulatore remoto è immediatamente disponibile nel client Python senza necessità di aggiornare la libreria locale.

### Configurazione dell'Agente AI e Lifecycle Management

L'intelligenza dell'umano è gestita dalla classe `AIAgent`, configurata con un `system_prompt` che ne definisce l'identità, il comportamento e i vincoli operativi. È cruciale applicare una rigorosa gestione del ciclo di vita degli agenti: l'uso di `cleanAIagents()` e `del_listener()` è fondamentale per terminare i thread di ascolto ed evitare memory leak o l'accumulo di "ghost listeners" che potrebbero corrompere le simulazioni successive.

### Meccanismo di Ascolto e Flusso Dati

Mentre `robot.listen()` rappresenta l'interfaccia di alto livello per lo studente, il flusso dati sottostante è gestito dalla callback `handle_msg_cb` in `robot_client.py`. Quando il server invia un messaggio di tipo "say", il robot lo pubblica sul topic "speech" del `MessageDispatcher`, permettendo agli agenti in ascolto di reagire in modo asincrono.

### Esercizio 4.1: Ciclo di Dialogo Base

```python
from robot_client import Robot
from ai import AI, AIAgent, cleanAIagents
from human_client import Human
from messages import getMessageDispatcher

robot = Robot()
ai = AI()
human = Human()
md = getMessageDispatcher()

# Definizione identità dell'agente umano
human_system = { 
    'role': 'system', 
    'content': "Sei Mario, un assistente di laboratorio. Rispondi in modo conciso." 
}

def human_action(response):
    human.say(response)

# Inizializzazione agente con listener sul topic "speech"
human_AI = AIAgent("mario", human_system)
human_AI.add_listener(md, "speech", human_action)

# Avvio interazione
prompt_robot = ai.chat("Saluta Mario e chiedigli se può aiutarti.")
robot.say(prompt_robot)

# Attesa non bloccante della risposta dell'AI umana
if human_AI.waitfor_response(timeout=10):
    risposta = robot.listen()
    print(f"SMARRtino ha udito: {risposta}")

# Cleanup obbligatorio dei thread
human_AI.del_listener()
cleanAIagents()
```

L'efficacia di questo dialogo dipende interamente dalla capacità del sistema di gestire i messaggi senza bloccare il loop di controllo principale.

## 3. Architettura dei Messaggi: Il Pattern MessageDispatcher

In robotica, l'uso di chiamate sincrone (bloccanti) per la comunicazione è una pratica critica: attendere la risposta di un LLM (che può richiedere diversi secondi) bloccherebbe l'intero processo, impedendo al robot di monitorare sensori o arrestare i motori in tempo reale.

### Il Pattern Topic-based Publish/Subscribe

Il `MessageDispatcher` risolve questo problema implementando un pattern **Pub/Sub asincrono**. Il sistema agisce come un hub centrale che utilizza `threading` e `queue.Queue` per disaccoppiare i componenti:

- **MessagePublisher:** Quando viene invocato `publish(message)`, il dispatcher itera attraverso un dizionario di code (`self.Q`). Se la chiave corrisponde al topic (es. "speech"), il messaggio viene inserito nella coda specifica.
- **MessageSubscriber:** Fornisce agli agenti un metodo `receive()` che interroga la propria coda in un thread dedicato, garantendo che l'elaborazione del linguaggio non interferisca con le altre funzioni del sistema.

### Vantaggi del Dispatching Asincrono

Questo approccio garantisce una **responsività deterministica**: il thread principale del robot rimane libero di gestire la navigazione, mentre uno o più thread `AIAgent` processano la logica conversazionale in background. La gestione della mutua esclusione tramite `threading.Lock` all'interno del dispatcher previene race conditions durante la registrazione dinamica di nuovi sottoscrittori.

## 4. Output Strutturato JSON e Controllo Condizionale

Per trasformare un intento comunicativo in un'azione fisica deterministica, dobbiamo superare la natura non deterministica degli LLM. La tecnica utilizzata consiste nel forzare il modello a produrre output in formato JSON strutturato, separando il linguaggio naturale dal codice operativo.

### Esercizio 4.2: Il Gatekeeper e il Ragionamento Condizionale

Nello scenario del "Codice Segreto", l'agente umano funge da gatekeeper. Deve decidere se eseguire un'azione (aprire la porta) basandosi su una condizione logica: la ricezione del segreto corretto da parte del robot.

### Ingegneria del Prompt e Funzione `analyze`

Il prompt di sistema istruisce l'LLM a rispondere esclusivamente con un oggetto JSON. La funzione `analyze` in `human_client.py` è l'anello di congiunzione tra linguaggio e azione:

```python
def analyze(response):
    try:
        jr = json.loads(response)
        return jr['text'], jr['code']
    except json.decoder.JSONDecodeError:
        print("Errore nel parsing dell'intento AI.")
        return None, None
```

### Esempio di Output Strutturato

Se il robot fornisce il codice corretto, l'AI genera:

```json
{ 
  "text": "Codice verificato. Apro la porta bianca per te.", 
  "code": "door_white.open()" 
}
```

Il comando `exec(code)` esegue quindi l'istruzione Python nell'ambiente virtuale. **Nota Tecnica:** Sebbene l'uso di `exec()` richieda cautela in sistemi di produzione, in questo contesto simulato rappresenta lo strumento ideale per tradurre istantaneamente un "intento cognitivo" dell'AI in una "trasformazione fisica" dello stato del mondo (apertura di un oggetto `Door`).

## 5. Sintesi delle Competenze Acquisite

Il completamento di questo modulo certifica la padronanza delle seguenti architetture software per la robotica:

- **Dynamic Proxying:** Utilizzo di `__getattr__` per l'interazione trasparente con componenti remoti in Gazebo.
- **Asincronia e Pub/Sub:** Implementazione di sistemi di messaggistica non bloccanti tramite `MessageDispatcher` per mitigare la latenza delle AI.
- **Lifecycle Engineering:** Gestione corretta dei thread e cleanup degli agenti per garantire la stabilità del sistema.
- **Controllo Deterministico via JSON:** Tecniche di prompt engineering per forzare gli LLM a generare codice eseguibile e gestire logiche condizionali complesse.

Queste basi sono essenziali per il modulo successivo, dove estenderemo le capacità di SMARRtino introducendo la gestione della memoria a lungo termine e la persistenza della conoscenza tramite database vettoriali.

---
## Collegamenti
