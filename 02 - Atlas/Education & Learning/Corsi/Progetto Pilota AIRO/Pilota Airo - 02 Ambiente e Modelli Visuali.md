---
status: permanent
type: project
area: tech
related: []
source: original
title: "Pilota Airo - 02 Ambiente e Modelli Visuali"
date: '2026-03-05'
updated: 2026-07-07T01:20
tags: []
summary: "Nel primo modulo abbiamo affrontato la cinematica di base e la navigazione reattiva. Tuttavia, per un robot sociale come SMARRtino, muoversi nello spazio è solo una precondizione: la vera sfida ris..."
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Pilota Airo - 02 Ambiente e Modelli Visuali]]

[[Pilota AIRO]]
# Pilota AIRO - 02 Ambiente e Modelli Visuali
## 1. Introduzione al Modulo 2: Contesto e Obiettivi

Nel primo modulo abbiamo affrontato la cinematica di base e la navigazione reattiva. Tuttavia, per un robot sociale come SMARRtino, muoversi nello spazio è solo una precondizione: la vera sfida risiede nella **comprensione semantica dell'ambiente**. Passare dalla semplice evitazione degli ostacoli alla capacità di identificare una "porta", un "utente" o un "oggetto specifico" è ciò che trasforma una macchina in un agente sociale capace di interazione significativa.

L'obiettivo di questo modulo è duplice. In primo luogo, impareremo a costruire e manipolare mondi 3D complessi all'interno del simulatore **Gazebo**, utilizzando un'interfaccia Python distribuita. In secondo luogo, integreremo i **Vision-Language Models (VLM)** per dotare il robot di una percezione visiva evoluta. Invece di limitarsi a interpretare nuvole di punti o distanze laser, il robot utilizzerà immagini e ragionamento testuale per "capire" il contesto in cui opera.

## 2. Costruzione e Gestione dell'Ambiente 3D (Gazebo)

L'interfaccia tra il nostro codice Python e il simulatore Gazebo si basa su un'architettura distribuita. La comunicazione avviene tramite il protocollo **WebSocket** (gestito dalla classe `WS` in `robot_client.py`), che permette di inviare comandi di manipolazione della scena in tempo reale.

### Architettura: Il Pattern Proxy e la Dynamic Method Invocation

Un aspetto tecnico fondamentale della classe `Gazebo` (definita in `gazebo.py`) è l'uso del metodo speciale `__getattr__`. Questo implementa una **Invocazione Dinamica di Metodi**: la classe agisce come un proxy. Quando chiamiamo un metodo che non è esplicitamente definito nel codice Python (es. `gz.add_object`), `__getattr__` cattura il nome della funzione e i suoi argomenti, li impacchetta in una stringa di comando (es. `"gz.add_object(...)"`) e li invia tramite WebSocket al server. Questo approccio permette una flessibilità estrema, consentendo di estendere le capacità del simulatore senza dover aggiornare costantemente le definizioni delle classi client.

### Configurazione del Client

Per iniziare la manipolazione dell'ambiente, inizializziamo il client Gazebo:

```python
from gazebo_client import Gazebo

# Inizializzazione del client per la gestione dell'ambiente 3D
gz = Gazebo()
```

### Comandi Operativi di Gazebo

Ecco i comandi principali per il controllo della scena simulata:

- `gz.add_object(name, model, pose)`: Inserisce un'entità (es. `wall`, `person_standing`). La posa è una stringa: `"x y z roll pitch yaw"`.
- `gz.move_object(name, model, pose)`: Riposiziona dinamicamente un oggetto già esistente.
- `gz.move_robot(x, y, theta_deg)`: Teletrasporta il robot in una coordinata specifica con un orientamento in gradi.
- `gz.del_object(name)`: Rimuove un oggetto specifico.
- `gz.del_all_objects()`: Pulisce interamente la scena (reset dell'ambiente).
- `gz.list_objects()` e `gz.get_object_state(name)`: Funzioni di introspezione per monitorare lo stato degli oggetti.
- `gz.save_world(name)` e `gz.load_world(name)`: Gestiscono la persistenza delle configurazioni ambientali.

### Libreria Oggetti Geometrici

Il simulatore adotta una convenzione di denominazione semantica in cui il nome del modello riflette i suoi parametri dimensionali.

| Modello                   | Descrizione     | Parametri Dimensionali (m)           |
| ------------------------- | --------------- | ------------------------------------ |
| `sphere_orange_0.2`       | Sfera arancione | Raggio: 0.2                          |
| `cylinder_yellow_0.1_0.6` | Cilindro giallo | Raggio: 0.1, Altezza: 0.6            |
| `cylinder_blue_0.1_0.6`   | Cilindro blu    | Raggio: 0.1, Altezza: 0.6            |
| `box_green_0.1_1.0_0.8`   | Box verde       | Lunghezza: 0.1, Largh: 1.0, Alt: 0.8 |

### Esempio Pratico: Costruzione Scena (Esercizio 2.1)

Il seguente script popola l'ambiente con pareti, una porta e diversi ostacoli cromatici per testare la percezione del robot.

```python
from gazebo_client import Gazebo

gz = Gazebo()
gz.del_all_objects() # Reset preventivo

# Costruzione perimetro e varchi
gz.add_object("w1", "wall", "2.0 1 0 0 0 0")
gz.add_object("w2", "wall", "2.0 -1 0 0 0 0")
gz.add_object("d2", "door_white", "2.0 0 0.5 0 0 0")

# Popolamento con oggetti per test VLM
gz.add_object("b1", "sphere_orange_0.2", "3.5 0 0.5 0 0 0")
gz.add_object("c1", "cylinder_yellow_0.1_0.6", "4.5 0.75 0.5 0 0 0")
gz.add_object("c2", "cylinder_blue_0.1_0.6", "4.5 -0.75 0.5 0 0 0")
gz.add_object("x1", "box_green_0.1_1.0_0.8", "5.5 0 0.1 0 0 0")

gz.save_world("scena_vlm_test")
```

## 3. Modelli Linguistici Visivi (VLM) e Percezione Robotica

L'integrazione di **GPT-5 Nano** abilita una percezione di tipo "semantic-first". Utilizzando la funzione `robot.get_image()`, SMARRtino cattura un frame dalla camera virtuale, trasformando la sua visione da una misurazione geometrica a una descrizione concettuale.

### Implementazione Tecnica di `ai.vision`

La funzione `vision` nel modulo `ai.py` gestisce l'invio dell'immagine ai server OpenAI. L'immagine catturata viene codificata in **Base64** e trasmessa utilizzando uno schema Data URI specifico:

```python
# Struttura del payload inviato al modello (estratto da ai.py)
input=[
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": f"{prompt}"},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_b64}"}
        ]
    }
]
```

### Chain-of-Thought e Self-Commenting Code

Un segreto dell'efficacia di SMARRtino risiede nel `code_system` prompt: l'istruzione di **aggiungere commenti Python che spieghino ogni istruzione** non è solo per l'utente, ma serve come meccanismo di _Chain-of-Thought_ (Catena di Pensiero) per il modello. Obbligando l'AI a verbalizzare il ragionamento prima o durante la generazione del codice, si riducono drasticamente le allucinazioni e gli errori logici nei movimenti del robot.

### Analisi Sequenziale via `query`

La funzione `ai.query(description, query)` è strategicamente cruciale per l'efficienza. Invece di inviare nuovamente l'immagine (operazione costosa in termini di latenza e token), utilizziamo la descrizione testuale generata precedentemente come contesto. Questo permette al robot di rispondere a domande specifiche ("Di che colore è il pavimento?") basandosi sulla sua "memoria a breve termine" visiva.

### Esempio di Percezione (Esercizio 2.2)

```python
from ai import AI
from robot_client import Robot

robot = Robot()
ai = AI()

# Cattura e analisi semantica
img = robot.get_image()
descrizione = ai.vision(img, "Cosa vedi in questa immagine?")
print(f"Descrizione VLM: {descrizione}")

# Query specifica sulla descrizione ottenuta
colore = ai.query(descrizione, "Di che colore è il pavimento?")
oggetti = ai.query(descrizione, "Quanti oggetti colorati sono presenti?")
print(f"Risultati: Pavimento {colore}, Oggetti {oggetti}")
```

## 4. Gestione degli Oggetti Dinamici e Porte

In un ambiente sociale, molti elementi sono dinamici. La classe `Door` in `gazebo.py` astrae la complessità di `move_object` in azioni semantiche come `open()` e `close()`.

### Differenze di Unità di Misura: Radianti vs Gradi

Un dettaglio tecnico critico per lo sviluppatore è la gestione delle rotazioni:

- I comandi del robot (es. `robot.left(90)`) utilizzano i **gradi**.
- I parametri della classe `Door` (`cth_rad`, `oth_rad`) utilizzano i **radianti**.

**Esempio di inizializzazione corretta:**

```python
from gazebo_client import Door
# Porta bianca: chiusa a 0 rad, aperta a 1.57 rad (90 gradi)
door_white = Door(gz, "dw", "white", 2.0, 0.0, 0, 2.5, 0.5, 1.57)

door_white.open() # Sposta l'oggetto porta nello stato aperto
```

### Integrazione Robot-Ambiente

Il robot può interagire con la porta misurando la distanza con `robot.obstacle_distance()`. Una logica tipica prevede l'avvicinamento fino a 0.7 metri prima di invocare il comando `open()`, garantendo che il varco sia libero prima di procedere.

## 5. Note su Costi e Monitoraggio (Token Tracking)

L'utilizzo di modelli avanzati come GPT-5 Nano richiede una supervisione dei consumi. Il modello è ottimizzato per l'efficienza:

- **Input:** $0.05 / 1M token.
- **Output:** $0.40 / 1M token (nota: il costo di output **include i token di ragionamento** utilizzati dal modello per elaborare la risposta).

### Monitoraggio e Destructor

La classe `AI` gestisce il tracking dei token in background. Un dettaglio architetturale importante è che il riepilogo finale dei costi e dei token viene attivato dal metodo **destruttore** (`__del__`). Questo significa che vedrete il report dei costi nel terminale solo quando l'oggetto `ai` viene eliminato o alla chiusura dello script. Tutte le interazioni dettagliate sono inoltre persistite in `ai.log`.

---
## Collegamenti
