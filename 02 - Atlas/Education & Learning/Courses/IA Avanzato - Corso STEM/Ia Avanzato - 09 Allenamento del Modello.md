---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 09 Allenamento del Modello"
date: '2025-05-07'
updated: 2026-07-07T01:20
tags: []
summary: "La sentiment analysis è una tecnica di elaborazione del linguaggio naturale (NLP) che permette di determinare l'atteggiamento emotivo espresso in un testo. Nel nostro caso, vogliamo classificare fr..."
---
[[Home MOC|Home]] / [[Education & Learning]] / [[Ia Avanzato - 09 Allenamento del Modello]]

[[IA Avanzato]]
### **1. Obiettivo della Sentiment Analysis**
La sentiment analysis è una tecnica di elaborazione del linguaggio naturale (NLP) che permette di determinare l'atteggiamento emotivo espresso in un testo. Nel nostro caso, vogliamo classificare frasi come "Personale docente" o "Interrogazioni a sorpresa" in una delle tre categorie: **positivo**, **neutrale** o **negativo**. Useremo un modello pre-addestrato e lo affineremo (fine-tuning) su un dataset specifico, quello caricato dal vostro username su Hugging Face.

---

### **2. Caricamento del Dataset**
La prima cosa da fare è caricare il dataset, che contiene testi e le relative etichette di sentimento. Nel codice, questo avviene con:

```python
from datasets import load_dataset
username = userdata.get('gh_username')
dataset = load_dataset(f"{username}/sentiment-analysis-test")
```

- **Cosa succede qui?**
  - Usiamo la libreria `datasets` di Hugging Face per caricare un dataset personalizzato, che si trova su Hugging Face Hub sotto il vostro username.
  - Il dataset è già suddiviso in split, come `train` e `test`, e contiene due colonne principali: `text` (il testo da analizzare) e `sentiment` (l'etichetta, ad esempio "positive", "neutral", "negative").
  - **Nota**: Assicuratevi di aver impostato la variabile segreta `gh_username` in Google Colab con il vostro username di GitHub/Hugging Face.

- **Perché è importante?**
  Il dataset è il cuore del nostro modello. Senza dati di qualità, anche il migliore algoritmo fallirebbe. Qui, il dataset è specifico per il contesto scolastico (es. commenti sulla scuola VIAN), quindi il modello imparerà a riconoscere sentimenti in questo dominio.

---

### **3. Pre-elaborazione: Aggiunta delle Etichette Numeriche**
Il modello non capisce etichette testuali come "positive" o "negative"; dobbiamo convertirle in numeri. Questo avviene con:

```python
label2id = {"negative": 0, "neutral": 1, "positive": 2}

def add_label_column(examples):
    examples["label"] = label2id[examples["sentiment"]]
    return examples

dataset = dataset.map(add_label_column)
```

- **Cosa facciamo?**
  - Creiamo un dizionario `label2id` che mappa le etichette testuali a numeri: "negative" → 0, "neutral" → 1, "positive" → 2.
  - Usiamo la funzione `map` per aggiungere una nuova colonna `label` al dataset, dove ogni valore di `sentiment` viene convertito nel corrispondente numero.
  - La funzione `map` applica `add_label_column` a ogni esempio nel dataset in modo efficiente.

- **Perché?**
  I modelli di machine learning lavorano con valori numerici. Questa trasformazione è essenziale per il passo successivo, il fine-tuning.

- **Output atteso**:
  Se stampiamo `dataset`, vedremo che ora ogni esempio ha una colonna `label` con valori 0, 1 o 2, oltre a `text` e `sentiment`.

---

### **4. Tokenizzazione**
I modelli di NLP non lavorano direttamente con il testo grezzo; il testo deve essere convertito in una rappresentazione numerica chiamata **token**. Questo avviene con:

```python
from transformers import AutoTokenizer, DataCollatorWithPadding

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/xlm-roberta-base-tweet-sentiment-it")

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
```

- **Spiegazione passo per passo**:
  1. **Caricamento del tokenizer**:
     - Usiamo `AutoTokenizer` per caricare il tokenizer associato al modello pre-addestrato `xlm-roberta-base-tweet-sentiment-it`, ottimizzato per l'italiano e per testi brevi come tweet.
     - Il tokenizer suddivide il testo in token (parole o sottoparole) e li converte in ID numerici che il modello capisce.

  2. **Funzione di tokenizzazione**:
     - La funzione `tokenize_function` prende il testo da ogni esempio e lo tokenizza.
     - `truncation=True` assicura che i testi più lunghi di 128 token vengano tagliati (utile per mantenere la memoria sotto controllo).
     - `max_length=128` limita la lunghezza massima delle sequenze.

  3. **Applicazione al dataset**:
     - Con `dataset.map(tokenize_function, batched=True)`, applichiamo la tokenizzazione a tutto il dataset in batch (per maggiore efficienza).
     - Il risultato è un nuovo dataset (`tokenized_dataset`) con colonne aggiuntive come `input_ids` (gli ID dei token) e `attention_mask` (che indica quali token sono validi e quali sono padding).

  4. **Data Collator**:
     - `DataCollatorWithPadding` aggiunge padding ai batch di dati durante l'addestramento, assicurando che tutte le sequenze in un batch abbiano la stessa lunghezza. Questo è cruciale perché i modelli Transformer elaborano i dati in parallelo.

- **Perché è importante?**
  La tokenizzazione trasforma il testo in un formato che il modello può processare. Senza di essa, il modello non saprebbe come interpretare le parole. Inoltre, il `data_collator` ottimizza l'addestramento rendendo i batch uniformi.

- **Output atteso**:
  Stampando `tokenized_dataset`, vedremo nuove colonne (`input_ids`, `attention_mask`) che rappresentano il testo tokenizzato.

---

### **5. Fine-Tuning del Modello Pre-addestrato**
Ora che i dati sono pronti, passiamo al fine-tuning di un modello pre-addestrato. Il codice è:

```python
from transformers import AutoModelForSequenceClassification

checkpoint = "cardiffnlp/xlm-roberta-base-tweet-sentiment-it"
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=3)
```

- **Cosa succede?**
  - Carichiamo un modello pre-addestrato (`xlm-roberta-base-tweet-sentiment-it`) usando `AutoModelForSequenceClassification`, progettato per compiti di classificazione di sequenze come la sentiment analysis.
  - Specifichiamo `num_labels=3` per indicare che vogliamo classificare in tre categorie: negativo, neutrale, positivo.
  - Il modello è già stato addestrato su un vasto corpus di dati, inclusi testi in italiano, quindi il fine-tuning serve ad adattarlo al nostro dataset specifico per il contesto scolastico.
  - Se eseguiamo `print(model.config)` e osserviamo la sezione `label2id`, vedremo che le etichette corrispondono a quelle definite precedentemente nel nostro dizionario `label2id = {"negative": 0, "neutral": 1, "positive": 2}`. Questo conferma che il modello è configurato correttamente per mappare le nostre etichette numeriche alle categorie di sentimento.

- **Perché usiamo un modello pre-addestrato?**
  Addestrare un modello da zero richiede enormi quantità di dati e risorse computazionali. Con il fine-tuning, sfruttiamo le conoscenze generali del modello e le adattiamo al nostro compito con meno dati e tempo.

---

### **6. Configurazione dei Parametri di Addestramento**
Definiamo come il modello verrà addestrato:

```python
from transformers import TrainingArguments

training_args = TrainingArguments("sentiment-analysis-test")
```

- **Cosa sono i `TrainingArguments`?**
  - Questa classe definisce i parametri dell'addestramento, come il numero di epoche, la dimensione del batch, il learning rate, dove salvare il modello, ecc.
  - Nel codice, usiamo i valori predefiniti di `TrainingArguments`, ma in pratica potremmo personalizzarli, ad esempio:
    ```python
    training_args = TrainingArguments(
        output_dir="sentiment-analysis-test",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
    )
    ```
  - Qui, `"sentiment-analysis-test"` è la directory dove il modello verrà salvato.

- **Perché è importante?**
  I parametri influenzano la qualità e la velocità dell'addestramento. Ad esempio, un learning rate troppo alto può rendere l'addestramento instabile, mentre un numero di epoche troppo basso può portare a un modello sottoaddestrato.

---

### **7. Creazione del Trainer**
Ora colleghiamo tutto con il `Trainer`:

```python
from transformers import Trainer

trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator
)
```

- **Cosa fa il `Trainer`?**
  - Il `Trainer` è una classe di Hugging Face che semplifica l'addestramento. Collega il modello, i dati, i parametri di addestramento e il `data_collator`.
  - `train_dataset` e `eval_dataset` sono gli split del dataset tokenizzato per addestramento e valutazione.
  - `data_collator` gestisce il padding, come visto prima.

- **Perché usiamo il `Trainer`?**
  Potremmo scrivere un ciclo di addestramento manuale con PyTorch, ma il `Trainer` automatizza molte operazioni (es. gestione della GPU, logging, salvataggio dei checkpoint), rendendo il processo più semplice e robusto.

---

### **8. Addestramento del Modello**
Finalmente, avviamo l'addestramento:

```python
trainer.train()
```

- **Cosa succede?**
  - Il modello viene addestrato sul dataset di training (`train_dataset`).
  - Durante l'addestramento, il modello aggiorna i suoi pesi per minimizzare l'errore di classificazione (usando una funzione di perdita come la cross-entropy).
  - Se abbiamo specificato `evaluation_strategy="epoch"`, il modello verrà valutato sul dataset di test alla fine di ogni epoca.

- **Cosa aspettarsi?**
  - L'addestramento può richiedere da pochi minuti a ore, a seconda della dimensione del dataset e della GPU disponibile (il codice usa una T4 su Colab).
  - Vedremo un output che mostra la perdita (loss) che diminuisce e, se configurato, metriche di valutazione come l'accuratezza.

---

### **9. Salvataggio del Modello**
Dopo l'addestramento, salviamo il modello su Hugging Face Hub:

```python
trainer.push_to_hub()
```

- **Cosa fa?**
  - Carica il modello addestrato e il tokenizer su Hugging Face Hub, sotto il vostro username, nella repository chiamata `sentiment-analysis-test`.
  - Ora il modello è accessibile da chiunque (o solo da voi, se la repository è privata) e può essere usato per inferenza.

- **Perché?**
  Salvare il modello permette di riutilizzarlo senza doverlo riaddestrare. Inoltre, condividerlo su Hugging Face facilita la collaborazione e l'integrazione in applicazioni.

---

### **10. Valutazione del Modello**
Testiamo il modello, confrontandolo con quello originale:

```python
from transformers import pipeline

# Modello originale
sentiment_pipeline_orig = pipeline("sentiment-analysis", model="cardiffnlp/xlm-roberta-base-tweet-sentiment-it")
print(sentiment_pipeline_orig("Personale docente"))
print(sentiment_pipeline_orig("Interrogazioni a sorpresa"))

# Nostro modello
sentiment_pipeline = pipeline("sentiment-analysis", model=f"{username}/sentiment-analysis-test")
print(sentiment_pipeline("Personale docente"))
print(sentiment_pipeline("Interrogazioni a sorpresa"))
```

- **Cosa succede?**
  - Usiamo la classe `pipeline` per fare inferenza in modo semplice.
  - Testiamo due frasi: "Personale docente" e "Interrogazioni a sorpresa".
  - Confrontiamo i risultati del modello originale (`xlm-roberta-base-tweet-sentiment-it`) con il nostro modello fine-tuned.

- **Cosa aspettarsi?**
  - Il modello originale potrebbe dare risultati generici, perché non è stato addestrato sul nostro dataset specifico.
  - Il nostro modello dovrebbe essere più preciso nel contesto scolastico, ad esempio riconoscendo che "Interrogazioni a sorpresa" ha una connotazione negativa.

---

### **11. Interfaccia Gradio**
Infine, creiamo un'interfaccia interattiva con Gradio:

```python
import gradio as gr

sentiment_pipeline = pipeline("sentiment-analysis", model=f"{username}/sentiment-analysis-test")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    label = result[0]['label']
    score = result[0]['score']
    return f"Label: {label}, Score: {score}"

iface = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(label="Prompt", lines=2, placeholder="Scrivi qui qualcosa sulla tua scuola..."),
    outputs=gr.Textbox(label="Sentiment Analysis Result"),
    title="Sentiment Analysis for VIAN",
    description="Analizza i sentimenti riguardo alla tua scuola con un modello fine-tuned",
)

iface.launch()
```

- **Cosa fa?**
  - Creiamo una funzione `analyze_sentiment` che usa il nostro modello per analizzare il testo inserito e restituisce l'etichetta e il punteggio di confidenza.
  - Con `gr.Interface`, creiamo un'interfaccia web dove gli utenti possono inserire testo e vedere i risultati in tempo reale.
  - `iface.launch()` avvia l'interfaccia su Colab (o localmente, se state eseguendo il codice altrove).

- **Perché è utile?**
  - L'interfaccia rende il modello accessibile anche a chi non sa programmare.
  - È un ottimo modo per testare il modello in modo interattivo e mostrarlo a compagni o professori.

- **Output atteso**:
  Una pagina web con un campo di testo e un output che mostra il sentimento (es. "Label: negative, Score: 0.85").

---

### **12. Considerazioni Finali**
Abbiamo coperto l'intero processo di allenamento di un modello di sentiment analysis:
1. Caricamento e preparazione del dataset.
2. Tokenizzazione del testo.
3. Fine-tuning di un modello pre-addestrato.
4. Valutazione e confronto con il modello originale.
5. Creazione di un'interfaccia utente.

**Punti chiave da ricordare**:
- Il fine-tuning adatta un modello generale a un compito specifico, migliorando le prestazioni nel nostro dominio (es. scuola VIAN).
- La tokenizzazione e il `data_collator` sono essenziali per preparare i dati per il modello.
- Il `Trainer` di Hugging Face semplifica l'addestramento, ma capire i parametri (es. learning rate, epoche) è fondamentale per ottimizzare i risultati.
- L'interfaccia Gradio è un esempio di come i modelli di NLP possono essere integrati in applicazioni pratiche.

**Esercizio per casa**:
1. Provate a modificare i `TrainingArguments` (es. aumentare le epoche o cambiare il learning rate) e osservate come cambiano i risultati.
2. Aggiungete nuove frasi al dataset e riaddestrate il modello. Notate miglioramenti?
3. Esplorate altre metriche di valutazione (es. precision, recall) usando `trainer.evaluate()`.

Domande? Altrimenti, ci vediamo alla prossima lezione, dove parleremo di come ottimizzare ulteriormente i modelli!

---
## Collegamenti
