---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 07 Creazione del Dataset"
date: '2025-04-16'
updated: 2026-07-07T01:20
tags: [tech/top]
summary: "La creazione di un dataset per sentiment analysis è un passaggio cruciale nello sviluppo di modelli di intelligenza artificiale avanzati. Un dataset ben strutturato, pulito e rappresentativo garant..."
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Ia Avanzato - 07 Creazione del Dataset]]

[[IA Avanzato]]
La creazione di un dataset per *sentiment analysis* è un passaggio cruciale nello sviluppo di modelli di intelligenza artificiale avanzati. Un dataset ben strutturato, pulito e rappresentativo garantisce che il modello possa apprendere correttamente i pattern associati ai sentimenti espressi nei testi (es. positivo, negativo, neutro). Questa lezione si concentra sulla raccolta, pulizia e pubblicazione di un dataset, utilizzando come esempio il dataset [Lod34/sentiment-analysis-test](https://huggingface.co/datasets/Lod34/sentiment-analysis-test) e il codice fornito nel [Google Colab](https://colab.research.google.com/github/wbigger/2025-vian-sentiment-analysis/blob/main/Sentiment_Analysis.ipynb#scrollTo=uEPGCdPp3rxD). La struttura della lezione segue quella della **Lezione 05 - Disinfestazione del Dataset**, adattandola al processo di creazione del dataset.

### Perché è necessaria la creazione di un dataset?
I dataset per *sentiment analysis* sono spesso derivati da fonti eterogenee come social media, recensioni online o forum, e richiedono un lavoro accurato per essere utilizzabili. Un dataset mal progettato può:
- Contenere dati rumorosi o irrilevanti (es. hashtag, URL, emoji non contestualizzate).
- Avere etichette incoerenti o errate, che confondono il modello.
- Essere sbilanciato, con una classe (es. positivo) sovrarappresentata rispetto alle altre.
- Mancare di una struttura standardizzata, rendendo difficile il suo utilizzo in pipeline di machine learning.

Creare un dataset pulito e ben organizzato è essenziale per ottenere risultati accurati e riproducibili. In questa lezione, vedremo come raccogliere dati, pulirli, strutturarli e pubblicarli su piattaforme come Hugging Face.

### Passaggi principali nella creazione del dataset
Ecco i passi chiave per creare un dataset di *sentiment analysis*:

1. **Raccolta dei dati grezzi**:
   - Identifica fonti affidabili, come dataset open-source, API di social media (es. Twitter/X), o piattaforme di recensioni.
   - Assicurati che ogni testo abbia un’etichetta di sentimento (es. positivo, negativo, neutro).
   - Esempio: Il dataset `Lod34/sentiment-analysis-test` contiene recensioni etichettate raccolte da fonti online.

2. **Pulizia del testo (disinfestazione)**:
   - Rimuovi elementi non rilevanti come URL, menzioni (@utente), hashtag e simboli inutili.
   - Normalizza il testo: converti in minuscolo, correggi errori ortografici, standardizza slang (es. "fantastiko" → "fantastico").
   - Gestisci le emoji: rimuovile o converti in testo descrittivo (es. "😊" → "sorriso").
   - Rimuovi stop words (es. "il", "di") che non contribuiscono al sentimento.
   - Esempio: "Fantastico prodotto! #top @negozio" → "fantastico prodotto".

3. **Validazione e bilanciamento**:
   - Controlla che le etichette siano corrette (es. un testo negativo non deve essere etichettato come positivo).
   - Identifica e rimuovi duplicati per evitare bias.
   - Bilancia le classi se necessario, ad esempio riducendo il numero di testi positivi se sono predominanti.

4. **Strutturazione del dataset**:
   - Organizza i dati in un formato standard (es. CSV o JSON) con colonne per testo e etichetta.
   - Dividi il dataset in training, validation e test set (es. 80% training, 10% validation, 10% test).
   - Usa la libreria `datasets` di Hugging Face per creare un oggetto compatibile con i framework di machine learning.

5. **Pubblicazione su Hugging Face**:
   - Carica il dataset su Hugging Face per condividerlo con la comunità.
   - Aggiungi una descrizione chiara, specificando il contesto, le fonti e il processo di creazione.

### Esempio pratico in codice
Il codice seguente, tratto dal [Google Colab di riferimento](https://colab.research.google.com/github/wbigger/2025-vian-sentiment-analysis/blob/main/Sentiment_Analysis.ipynb#scrollTo=uEPGCdPp3rxD) e adattato, mostra come creare un dataset per *sentiment analysis*. Lo script include la pulizia del testo, la strutturazione e il caricamento su Hugging Face.

```python
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datasets import Dataset, DatasetDict
from huggingface_hub import login

# Scarica risorse NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Carica il dataset grezzo (es. CSV con colonne 'text' e 'label')
data = {
    'text': [
        'Adoro questo prodotto! #fantastico',
        'Pessimo servizio, mai più!',
        'È nella media, nulla di speciale',
        'Super soddisfatto! 😊 #top'
    ],
    'label': ['positivo', 'negativo', 'neutro', 'positivo']
}
dataset = pd.DataFrame(data)

dataset = dataset.drop_duplicates(subset=['text'])

# Funzione di pulizia
def clean_text(text):
    # Rimuovi URL, menzioni e hashtag
    text = re.sub(r'http\S+|@\w+|#\w+', '', text)
    # Converti in minuscolo
    text = text.lower()
    # Rimuovi punteggiatura non essenziale
    text = re.sub(r'[^\w\s!]', '', text)
    # Tokenizzazione
    tokens = word_tokenize(text)
    # Rimuovi stop words
    stop_words = set(stopwords.words('italian'))
    tokens = [word for word in tokens if word not in stop_words]
    # Ricostruisci il testo
    return ' '.join(tokens)

# Applica la pulizia
dataset['clean_text'] = dataset['text'].apply(clean_text)

# Crea un dataset Hugging Face
hf_dataset = Dataset.from_pandas(dataset[['clean_text', 'label']])

# Dividi in train, validation, test
train_test = hf_dataset.train_test_split(test_size=0.2, seed=42)
test_valid = train_test['test'].train_test_split(test_size=0.5, seed=42)

dataset_dict = DatasetDict({
    'train': train_test['train'],
    'validation': test_valid['train'],
    'test': test_valid['test']
})

# Salva il dataset localmente
dataset_dict.save_to_disk("sentiment_dataset_processed")

# Autenticazione Hugging Face (esegui in Colab con il tuo token)
# login(token="YOUR_HF_TOKEN")

# Pubblica su Hugging Face (decommenta per caricare)
# dataset_dict.push_to_hub("tuo_username/sentiment-analysis-test")

print("Dataset creato e salvato!")
```

---
## Collegamenti
