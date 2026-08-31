---
status: reference
type: concept
area: tech
related: []
source: original
title: "Conferenza AI 29 - 10 - 2025"
date: '2025-10-29'
updated: 2025-10-29T11:28
tags: [tech/tech, tech/ai, tech/conference]
summary: "figlio della Disanto"
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Conferenza AI 29-10-2025|Conferenza AI 29 - 10 - 2025]]

# Conferenza AI 29-10-2025

- figlio della Disanto
- google → primato alla tecnologia AI → dopo openAI
- chi ha inventato il chip è Federico Faggin
- 61% → statistica italiana che guarda porno
- fingerprint → stesso codice (ID JS) anche in incognito e vpn
- economia dell’attenzione (o **brevità**)
- 97% del fatturato di google generato solo dai **banner pubblicati** che pensi che nessuno clicca
- es. concessionaria → solo con 10k di dati si riesce a capire chi è perditempo e chi no
- cookies di terze parti **deprecati** → fingerprint
- la combinazione dei fonts è un identificatore del fingerprint
---
Ecco alcuni degli identificativi più strabilianti e persistenti utilizzati nella **fingerprint** di un dispositivo (soprattutto browser e mobile), che permettono un tracking avanzato anche senza cookie o con modalità privacy attive:

1. **Canvas Fingerprint**  
   Rendering nascosto di immagini/canvas HTML5 per estrarre differenze GPU/driver.  
   `canvas_fingerprint.js`

2. **WebGL Fingerprint**  
   Informazioni su renderer, vendor e estensioni della scheda grafica.  
   `webgl_fingerprint.js`

3. **AudioContext Fingerprint**  
   Oscillatori audio + offline rendering per captare variazioni hardware/audio stack.  
   `audiocontext_fingerprint.js`

4. **Font Probing (CSS + JS)**  
   Elenco preciso di font installati tramite misurazioni di testo o getComputedStyle.  
   `font_fingerprint.js`

5. **Hardware Concurrency + Device Memory**  
   `navigator.hardwareConcurrency` e `navigator.deviceMemory` (valori quantizzati ma unici).  
   `hardware_fingerprint.js`

6. **Screen Resolution + Color Depth + Pixel Ratio**  
   Combinazione di `screen.width/height`, `devicePixelRatio`, `colorDepth`.  
   `screen_fingerprint.js`

7. **Timezone + Language + Platform**  
   `Intl.DateTimeFormat().resolvedOptions().timeZone` + `navigator.languages`.  
   `locale_fingerprint.js`

8. **Battery API (deprecated ma ancora usato)**  
   Livello, carica, tempo rimanente (unico su mobile).  
   `battery_fingerprint.js`

9. **Sensor Fusion (Accelerometer, Gyro, etc.)**  
   Su mobile, rumore dei sensori tramite `DeviceMotionEvent`.  
   `sensor_fingerprint.js`

10. **TCP/IP Stack Fingerprint (via WebRTC/STUN)**  
    RTT, MTU e comportamento pacchetti (anche con IP leak).  
    `webrtc_fingerprint.js`

Questi identificativi, combinati con **entropia alta**, rendono la fingerprint **univoca al 99,99%** in molti casi, anche su dispositivi "anonimi".

----
- linguaggio
- ricerca
- 2013 prima ‘AI’ → **word to rec**

### Approccio LEAN (nei modelli matematici)
Immagina di costruire un modello come un prodotto minimo: **inizia semplice**, testa con dati reali, aggiungi solo ciò che serve. Evita complicazioni inutili per non sprecare tempo. È come "prova e impara" velocemente: modello base → verifica → migliora se necessario.

### TF-IDF
![[Pasted image 20251029121207.png]]
È un modo per dare **peso alle parole** in un testo:
- **TF** (Term Frequency): quante volte una parola appare in un documento (più appare, più è importante lì).
- **IDF** (Inverse Document Frequency): penalizza parole comuni in tutti i documenti (tipo "il" o "e", che non dicono niente di speciale).
- **TF-IDF** = TF × IDF: parole rare ma frequenti in un testo specifico diventano "importanti". Trasforma testi in numeri per computer.

### Similarità al Coseno
Misura **quanto due cose sono simili per direzione**, ignorando la grandezza. Come due frecce: se puntano nello stesso senso → similarità 1; perpendicolari → 0; opposte → -1.  
Usata per confrontare testi (es. due documenti con parole simili hanno coseno alto).

### Algoritmo di Clustering
Raggruppa dati **simili automaticamente** senza sapere in anticipo le categorie. Esempio: punti vicini formano un "gruppo".  
- **K-Means**: scegli quanti gruppi (k), metti centri, assegna punti vicini, ripeti fino a stabilizzare.
- Utile per scoprire pattern nascosti (es. clienti simili, documenti correlati).

In pratica: tokenizzi testo → TF-IDF → similarità coseno → clustering per raggruppare documenti simili.

`summary_nlp_concepts.py`
## Tokenizer 

Nel tokenizer, **'tf'** e **'idf'** non sono concetti diretti (il tokenizer si occupa principalmente di dividere il testo in token, come parole o subword), ma compaiono nel contesto del **TF-IDF** (Term Frequency-Inverse Document Frequency), una tecnica usata in elaborazione del linguaggio naturale (NLP) per pesare l'importanza delle parole in un documento rispetto a una collezione.

Ecco la spiegazione concisa:

- **TF (Term Frequency)**: Frequenza del termine. Misura quante volte una parola appare in un singolo documento.  
  Formula base:  
  $$
  \text{TF}(t, d) = \frac{\text{numero di occorrenze di } t \text{ in } d}{\text{numero totale di termini in } d}
  $$

- **IDF (Inverse Document Frequency)**: Frequenza inversa del documento. Riduce il peso delle parole comuni (es. "il", "e") che appaiono in molti documenti.  
  Formula base:  
  $$
  \text{IDF}(t, D) = \log \left( \frac{\text{numero totale di documenti in } D}{\text{numero di documenti contenenti } t} \right)
  $$

Il **TF-IDF** è il prodotto:  
$$
\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)
$$

In pratica, dopo il tokenizing, si calcola TF-IDF per trasformare il testo in vettori numerici utili per modelli di machine learning (es. classificazione, ricerca).

Esempio in Python con scikit-learn:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documenti = [
    "Il cane corre nel parco",
    "Il gatto dorme sul tetto",
    "Il cane e il gatto giocano"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documenti)
print(vectorizer.get_feature_names_out())
print(X.toarray())
```

## Aproccio matematico LEAN

L'**approccio lean** nei modelli matematici si riferisce a una strategia di modellazione ispirata ai principi della **Lean Startup** o del **pensiero lean** (originato dal Toyota Production System), applicata al contesto scientifico e matematico. L'obiettivo è creare modelli **semplici, iterativi e validati empiricamente**, evitando complessità inutili ("overfitting" concettuale o computazionale) e focalizzandosi su ciò che genera valore reale (es. previsioni accurate con il minimo sforzo).

### Principi chiave:
- **Minimalismo**: Inizia con il modello più semplice possibile (MVP - Minimum Viable Model) che catturi l'essenza del fenomeno.
- **Iterazione rapida**: Costruisci, misura, impara (Build-Measure-Learn). Aggiungi complessità solo se i dati lo giustificano.
- **Eliminazione degli sprechi**: Rimuovi variabili, termini o assunzioni non essenziali (simile al "waste" nel lean manufacturing).
- **Validazione data-driven**: Usa metriche come AIC, BIC o cross-validation per decidere se complicare il modello.
- **Flessibilità**: Modelli "lean" sono facili da modificare, testare e scalare.

### Esempio pratico:
Supponi di modellare la crescita di una popolazione (equazione logistica):

- **Modello non lean**: Aggiungi subito termini per predazione, risorse limitate, stocasticità, ecc. → Complesso, parametri da stimare troppi.
- **Approccio lean**:
  1. Inizia con crescita esponenziale semplice:  
     $$
     \frac{dN}{dt} = rN
     $$
  2. Testa su dati: Se non fits, aggiungi capacità portante (K):  
     $$
     \frac{dN}{dt} = rN \left(1 - \frac{N}{K}\right)
     $$
  3. Solo se necessario, introduci rumore o altri fattori.

In machine learning, è simile al **principio di Occam** o al **regularization** (es. LASSO per selezionare feature).

### Vantaggi:
- Riduce overfitting.
- Migliora interpretabilità.
- Accelera sviluppo e deployment.

In sintesi, è "modella poco, ma modella bene" – priorizzando efficienza e risultati misurabili.


### Introduzione al CBOW
**CBOW** (Continuous Bag of Words) è un modello di **Word Embedding** usato negli algoritmi **Word2Vec** (sviluppati da Google). Prevede una **parola target** dal suo **contesto** (parole vicine), trattando il contesto come un "sacchetto" di parole (ignora l'ordine).

### Spiegazione semplice:
- **Input**: Parole contestuali (es. per finestra di 2: "il ___ mangia" → contesto: "il" e "mangia").
- **Output**: Parola centrale prevista (es. "cane").
- **Come funziona**:
  1. Ogni parola → vettore (embedding).
  2. Media dei vettori del contesto.
  3. Rete neurale semplice prevede la parola target.
- **Vantaggio**: Veloce, buono per dataset grandi; cattura relazioni semantiche (es. "re" - "uomo" + "donna" ≈ "regina").

Contrario: **Skip-Gram** (prevede contesto dalla parola centrale, meglio per parole rare).

Esempio Python (gensim):
```python
from gensim.models import Word2Vec

frasi = [["il", "cane", "corre"], ["il", "gatto", "dorme"]]
model = Word2Vec(frasi, vector_size=100, window=2, sg=0)  # sg=0 → CBOW
print(model.wv["cane"])
```

`cbow_word2vec.py`

---
## Collegamenti
- [[Evoluzione Dell'Agente AI]]
