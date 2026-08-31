---
status: permanent
type: project
area: tech
related: []
source: original
title: "Pilota Airo - 03 Ambienti Dinamici e Domotica"
date: '2026-03-05'
updated: 2026-07-07T01:20
tags: []
summary: "In un'architettura di simulazione avanzata basata su Gazebo, un \"ambiente dinamico\" non si limita alla presenza di entità in movimento regolate dal motore fisico, ma si definisce propriamente come ..."
---
[[Home MOC|Home]] / [[Education & Learning]] / [[Pilota Airo - 03 Ambienti Dinamici e Domotica]]

[[Pilota AIRO]]
# Pilota AIRO - 03 Ambienti Dinamici e Domotica
## 1. Introduzione ai Sistemi Robotici Dinamici

In un'architettura di simulazione avanzata basata su Gazebo, un "ambiente dinamico" non si limita alla presenza di entità in movimento regolate dal motore fisico, ma si definisce propriamente come uno scenario in cui lo stato cinematico degli oggetti può essere alterato programmaticamente in tempo reale. Il passaggio da ambienti statici a scenari dinamici rappresenta un'evoluzione strategica: il robot SMARRtino smette di essere un'entità puramente passiva che si limita a evitare ostacoli (navigazione reattiva) per diventare un attore capace di interagire e modificare le infrastrutture intelligenti circostanti.

Dal punto di vista architettonico, la manipolazione indiretta — ovvero la modifica della posa di un oggetto tramite codice — richiede il coordinamento di chiamate asincrone verso il simulatore. Questa astrazione prepara lo studente alla gestione di ecosistemi domotici complessi, dove la logica del robot deve sincronizzarsi con lo stato fisico di attuatori ambientali come porte automatiche o sistemi di illuminazione.

**Obiettivi di apprendimento del modulo:**

- **Gestione Oggetti:** Manipolazione degli stati cinematici delle entità tramite il client Gazebo.
- **Controllo Porte:** Implementazione di wrapper semantici per l'automazione dei varchi.
- **Agenti di Ascolto:** Configurazione di thread asincroni per la reattività agli eventi di messaggistica.

La base di questa dinamicità risiede nella capacità del client Gazebo di interfacciarsi con il server per aggiornare le proprietà fisiche della scena in modo non bloccante.

## 2. Gestione degli Oggetti e delle Porte nel Simulatore Gazebo

L'interfaccia primaria per la modifica dell'ambiente è la classe `Gazebo`, che espone il metodo `move_object`. Questo metodo permette di aggiornare la posizione e l'orientamento di un'entità, garantendo la coerenza del mondo fisico simulato. Tuttavia, operare direttamente con coordinate grezze e stringhe di comando è inefficiente e soggetto a errori.

Per ovviare a ciò, abbiamo implementato la classe `Door`, che funge da **wrapper semantico** sopra `gz.move_object`. Questa astrazione trasforma un'interazione intrinsecamente _stateless_ (l'invio di coordinate X, Y, Z a Gazebo) in un'interazione _semantica_ focalizzata sullo stato dell'oggetto ("aperto" o "chiuso"). Incapsulando i dati geometrici all'interno dell'oggetto porta, separiamo la logica di controllo (il "cosa fare") dai dettagli implementativi della simulazione (il "come spostare i vertici").

```python
class Door():
    def __init__(self, gz, name, color, cx, cy, cth_rad, ox, oy, oth_rad):
        self.gz = gz
        self.name = name
        self.color = color
        self.closed_x = cx
        self.closed_y = cy
        self.closed_th_rad = cth_rad
        self.open_x = ox
        self.open_y = oy
        self.open_th_rad = oth_rad

    def open(self):
        # Il valore 0.5 rappresenta la coordinata Z fissa per la porta nel simulatore
        self.gz.move_object(self.name, "door_"+self.color, 
                           f"{self.open_x} {self.open_y} 0.5 0 0 {self.open_th_rad}")

    def close(self):
        self.gz.move_object(self.name, "door_"+self.color, 
                           f"{self.closed_x} {self.closed_y} 0.5 0 0 {self.closed_th_rad}")
```

### Parametri di Inizializzazione della Porta (Signature `__init__`)

|   |   |   |
|---|---|---|
|Parametro|Descrizione Tecnica|Esempio|
|`gz`|Istanza del client Gazebo (comunicazione WebSocket)|`gz`|
|`name`|Identificativo univoco (ID) dell'entità nella scena|`"dw"`|
|`color`|Modello visivo associato (stringa colore)|`"white"`|
|`cx, cy, cth_rad`|Coordinate di chiusura: Posizione (x, y) e orientamento (theta in radianti)|`2.0, 0.0, 0`|
|`ox, oy, oth_rad`|Coordinate di apertura: Posizione (x, y) e orientamento (theta in radianti)|`2.5, 0.5, 1.57`|

Questa struttura permette di astrarre la complessità della posa fisica dietro metodi intuitivi, ma il successo dell'interazione dipende dalla precisione spaziale del robot.

## 3. Navigazione e Calcolo della Distanza dagli Ostacoli

In un ecosistema domotico, la navigazione di precisione è fondamentale. Il robot deve calcolare la propria posizione relativa rispetto agli ostacoli per eseguire manovre come l'avvicinamento a un varco senza compromettere la sicurezza o la visibilità sensoriale.

La funzione `robot.obstacle_distance()` interroga i sensori di prossimità per determinare lo spazio libero frontale. Nella logica `robot.forward(d - 0.7)`, l'offset di **0.7 metri** è un parametro critico:

1. **Margine di Sicurezza:** Impedisce la collisione fisica con la porta.
2. **Arco di Rotazione:** Garantisce che il robot sia fuori dal raggio di ingombro della porta mentre questa ruota per aprirsi.
3. **Campo Visivo:** Posiziona la fotocamera a una distanza ottimale per mantenere la porta (e gli oggetti retrostanti) all'interno del frame sensoriale.

### Integrazione Navigazione-Domotica (Esercizio 3.2)

```python
from robot_client import Robot
from gazebo_client import Gazebo, Door

robot = Robot()
gz = Gazebo()

# Astrazione dell'oggetto porta con coordinate di stato
door_white = Door(gz, "dw", "white", 2.0, 0.0, 0, 2.5, 0.5, 1.57)

# Percezione e navigazione di precisione
dist = robot.obstacle_distance()
if dist > 0.7:
    robot.forward(dist - 0.7) # Posizionamento nel raggio d'azione domotico

# Modifica dello stato dell'ambiente
door_white.open()
robot.forward(1.5) # Transito sicuro attraverso il varco
```

L'automazione cablata (hard-coded) mostrata sopra è efficiente, ma per scenari reali necessitiamo di un'interfaccia intelligente capace di interpretare il linguaggio naturale.

## 4. Architettura dell'Agente AI Domotico

L'agente AI agisce come un layer di traduzione tra l'utente (linguaggio naturale) e l'hardware (metodi Python). L'obiettivo non è la conversazione libera, ma la generazione di codice deterministico per il controllo ambientale.

Per questo task, utilizziamo il modello **GPT-5 Nano**. La scelta architettonica è guidata da un'analisi dei costi: con soli **0.05 per 1M di token di input** e ******0.40 per 1M di token di output**, il modello è ideale per micro-task di generazione codice dove la latenza e il costo devono rimanere minimi. Il `system_prompt` è configurato per forzare il modello a restituire esclusivamente stringhe eseguibili.

**System Prompt (automatic_door_system):** "Sei un sistema di domotica. Il tuo compito è ricevere comandi in linguaggio naturale e generare esclusivamente codice Python per il controllo degli oggetti. Esempio: se l'utente chiede di aprire la porta, rispondi con 'door_white.open()'."

### Flusso di Esecuzione dell'AI Agent

1. **Ricezione:** Un messaggio vocale o testuale viene intercettato dal sistema.
2. **Elaborazione LLM:** Il prompt viene processato da GPT-5 Nano per mappare l'intento su una funzione specifica.
3. **Generazione:** L'AI restituisce una stringa (es. `"door_white.open()"`).
4. **Esecuzione Asincrona:** La stringa viene passata alla funzione `exec()`, che agisce direttamente sugli oggetti definiti nello scope locale.

## 5. Il Modulo messages.py e il Sistema di Dispatching

La comunicazione tra il robot e l'agente AI è gestita tramite un pattern **Publisher-Subscriber (Pub-Sub)** implementato in `messages.py`. Questa architettura è essenziale per disaccoppiare i componenti: il robot non deve sapere chi sta ascoltando il suo messaggio "say", e l'agente può elaborare i dati nel proprio thread.

Una sfida tecnica fondamentale è la sincronizzazione: il protocollo WebSocket è estremamente veloce (bassa latenza), mentre le chiamate agli LLM sono intrinsecamente lente (alta latenza). Per gestire questo dislivello, `MessageSubscriber` utilizza una `**queue.Queue**`. Il metodo `receive()` esegue una lettura bloccante sulla coda; questo permette di "tamponare" i messaggi in arrivo senza perdere dati e di sincronizzare il thread di ascolto con i tempi di risposta dell'intelligenza artificiale.

### Diagramma del Flusso dei Messaggi

1. `robot.say("apri porta")` → Comando inviato al server SRL.
2. **Server SRL** → Elabora il comando e lo ritrasmette a tutti i client come stato "say".
3. `Robot.handle_msg_cb` → Riceve lo stato "say" via WebSocket e lo rileva come evento.
4. `MessagePublisher.publish` → Inserisce il messaggio nel topic "speech".
5. `MessageSubscriber.receive` → Preleva il messaggio dalla coda (blocking `get()`).
6. `AIAgent.listener_thread` → Invia il contenuto all'LLM ed esegue la callback di risposta.

Questo sistema di dispatching centralizzato tramite `MessageDispatcher` permette il monitoraggio e la scalabilità: più agenti (es. un logger e un controllore AI) possono sottoscrivere lo stesso topic simultaneamente.

## 6. Implementazione Pratica: Esercizio 3.3

L'integrazione finale avviene tramite la funzione `exec(response)`. Dal punto di vista architettonico, `exec` offre una flessibilità estrema, permettendo all'AI di comporre sequenze di comandi non previste. Tuttavia, l'esecuzione dinamica di codice generato esternamente introduce rischi di sicurezza. In sistemi di produzione, questa pratica richiederebbe tecniche di **sandboxing** (limitazione dei moduli accessibili) e validazione dell'output. Nel nostro contesto educativo, la sicurezza è garantita dalla natura deterministica del prompt e dall'ambiente di simulazione isolato.

### Codice Integrato (Esercizio 3.3)

```python
from ai import AIAgent
from messages import getMessageDispatcher
from robot_client import Robot

# Inizializzazione delle interfacce hardware e messaggistica
robot = Robot()
md = getMessageDispatcher()

# Definizione del prompt di sistema per la specializzazione domotica
automatic_door_system = {
    'role': 'system',
    'content': "Sei un sistema di domotica. Genera codice Python come 'door_white.open()' basandoti sulle richieste."
}

def domotic_action(response):
    print(f"Esecuzione comando AI: {response}")
    # Esegue la stringa di codice nello scope dove gli oggetti door sono definiti
    exec(response)

# Inizializzazione Agente con GPT-5 Nano e registrazione listener
domotic_AI = AIAgent("domoticAI", automatic_door_system)
domotic_AI.add_listener(md, "speech", domotic_action)

# Azione: Il robot emette un messaggio che innesca la catena Pub-Sub
robot.say("apri la porta bianca")

# Cruciale: Impedisce la chiusura prematura dello script mentre l'LLM elabora
# Il metodo attende che la callback domotic_action venga completata
domotic_AI.waitfor_response()

# Cleanup delle risorse e dei listener
domotic_AI.del_listener()
```

Questa architettura trasforma SMARRtino in un orchestratore di sistemi cyber-fisici: non è più solo una macchina che si muove, ma un maggiordomo digitale capace di rimodellare l'ambiente fisico tramite la mediazione intelligente dell'AI.

---
## Collegamenti
