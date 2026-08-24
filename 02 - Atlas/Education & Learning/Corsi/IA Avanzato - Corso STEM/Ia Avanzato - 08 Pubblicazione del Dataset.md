---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 08 Pubblicazione del Dataset"
date: '2025-05-07'
updated: 2026-07-07T01:20
tags: []
summary: "La pubblicazione di un dataset per sentiment analysis è un passaggio fondamentale per condividerlo con la comunità scientifica e gli sviluppatori, promuovendo la ricerca e l'innovazione. Pubblicare..."
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Ia Avanzato - 08 Pubblicazione del Dataset]]

[[IA Avanzato]]
La pubblicazione di un dataset per _sentiment analysis_ è un passaggio fondamentale per condividerlo con la comunità scientifica e gli sviluppatori, promuovendo la ricerca e l'innovazione. Pubblicare un dataset su piattaforme come Hugging Face garantisce accessibilità, riproducibilità e possibilità di collaborazione. Questa lezione si basa sulla **Lezione 07 - Creazione del Dataset** e si concentra sulla pubblicazione del dataset, utilizzando il codice tratto dal notebook [Sentiment Analysis.ipynb](https://colab.research.google.com/github/wbigger/2025-vian-sentiment-analysis/blob/main/Sentiment_Analysis.ipynb) e il dataset di esempio [Lod34/sentiment-analysis-test](https://huggingface.co/datasets/Lod34/sentiment-analysis-test).

### Perché pubblicare un dataset?

La pubblicazione di un dataset offre i seguenti vantaggi:

- **Accessibilità globale**: Rende il dataset disponibile a ricercatori, studenti e professionisti.
- **Riproducibilità**: Consente di validare i risultati e confrontare approcci diversi.
- **Collaborazione**: Favorisce feedback e contributi per migliorare il dataset.
- **Standardizzazione**: Promuove l’uso di formati compatibili con strumenti di machine learning.

Un dataset pubblicato deve includere una documentazione completa che ne descriva il contenuto, il processo di creazione e le applicazioni. In questa lezione, vedremo come preparare, autenticarsi, documentare e caricare un dataset su Hugging Face.

### Passaggi principali per la pubblicazione del dataset

Ecco i passaggi per pubblicare un dataset di _sentiment analysis_:

1. **Preparazione del dataset**:
    
    - Assicurati che il dataset sia stato pulito, strutturato e suddiviso in training e test set (come mostrato nella Lezione 07).
    - Usa la libreria `datasets` di Hugging Face per creare un oggetto `DatasetDict` compatibile.
    - Esempio: Il dataset `Lod34/sentiment-analysis-test` è organizzato con testi etichettati e suddiviso in training e test.
2. **Autenticazione su Hugging Face**:
    
    - Crea un account su [Hugging Face](https://huggingface.co/) e genera un token di accesso (_Settings > Access Tokens_).
    - Usa la funzione `notebook_login()` o `login()` della libreria `huggingface_hub` per autenticarti.
3. **Documentazione del dataset**:
    
    - Prepara una descrizione dettagliata nel file `README.md` o nella scheda del dataset su Hugging Face.
    - Includi:
        - **Contesto**: Scopo del dataset (es. _sentiment analysis_ su testi in italiano).
        - **Fonti**: Origine dei dati (es. CSV da recensioni online).
        - **Processo**: Dettagli su raccolta, pulizia e suddivisione.
        - **Struttura**: Colonne (es. `text`, `label`), numero di esempi, suddivisione (train/test).
        - **Limitazioni**: Eventuali bias o lacune.
        - **Tag**: Parole chiave come "sentiment-analysis", "italian", "text-classification".
    - Usa un linguaggio chiaro e conciso per favorire la comprensione.
4. **Caricamento su Hugging Face**:
    
    - Crea un repository pubblico (o privato) su Hugging Face.
    - Usa il metodo `push_to_hub()` per caricare il `DatasetDict`.
    - Verifica che il dataset sia accessibile e scaricabile.
5. **Verifica e manutenzione**:
    
    - Controlla la visualizzazione del dataset sulla piattaforma Hugging Face.
    - Monitora feedback dalla comunità per eventuali aggiornamenti o correzioni.

### Esempio pratico in codice

Il codice seguente, tratto e adattato dal notebook [Sentiment Analysis.ipynb](https://colab.research.google.com/github/wbigger/2025-vian-sentiment-analysis/blob/main/Sentiment_Analysis.ipynb), mostra come pubblicare un dataset su Hugging Face. Il codice assume che il dataset sia già stato creato e salvato localmente (come mostrato nella sezione "Create dataset" del notebook).

```python
from datasets import load_dataset, DatasetDict
from huggingface_hub import notebook_login, HfApi

# Carica il dataset dai file CSV
v01_files = [
    "v01/m00 - m00-1.csv",
    "v01/m00 - m00-2.csv",
    "v01/m00 - m00-3.csv",
    "v01/m00 - m00-4.csv",
    "v01/m01 - m01-1.csv",
    "v01/m02 - m02-1.csv",
    "v01/m03 - m03-1.csv",
    "v01/m04 - m04-1.csv"
]
dataset = load_dataset("csv", data_files=v01_files)

# Dividi in training e test
dataset_clean = dataset["train"].train_test_split(train_size=0.8, seed=42)

# Salva localmente (opzionale)
dataset_clean.save_to_disk("v01/dataset_clean")

# Autenticazione Hugging Face
notebook_login()  # Esegui in Colab per inserire il token

# Crea un repository su Hugging Face
api = HfApi()
repo_id = "tuo_username/sentiment-analysis-test"
api.create_repo(repo_id=repo_id, repo_type="dataset", private=False)

# Pubblica il dataset
dataset_clean.push_to_hub(repo_id)

# Aggiungi una descrizione (README.md)
readme_content = """
# Sentiment Analysis Test Dataset

## Descrizione
Questo dataset è stato creato per l'analisi del sentimento in testi in lingua italiana, raccolti da fonti online come recensioni e social media. Contiene testi etichettati come positivi, negativi o neutri.

## Struttura
- **Colonne**: `text` (testo originale), `label` (positivo, negativo, neutro)
- **Suddivisione**:
  - Train: 80% dei dati
  - Test: 20% dei dati
- **Numero di esempi**: Varia in base ai file CSV caricati

## Processo di creazione
1. Raccolta di dati grezzi da file CSV.
2. Pulizia: rimozione di dati rumorosi (es. URL, hashtag) e normalizzazione del testo.
3. Suddivisione in training e test set con proporzione 80/20.

## Utilizzo
Adatto per addestrare e valutare modelli di *sentiment analysis* in italiano.

## Limitazioni
- Possibili bias legati alle fonti dei dati.
- Dimensioni del dataset dipendenti dai file CSV originali.

## Tag
- sentiment-analysis
- italian
- text-classification
"""

# Carica il README nel repository
api.upload_file(
    path_or_fileobj=readme_content.encode(),
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="dataset"
)

print(f"Dataset pubblicato con successo su https://huggingface.co/datasets/{repo_id}")
```

### Note finali

- **Token di accesso**: Non condividere il token Hugging Face nel codice. Usa `notebook_login()` in Colab per un’autenticazione sicura.
- **Aggiornamenti**: Per aggiornare il dataset, ricarica una nuova versione con `push_to_hub()` e modifica il `README.md` se necessario.
- **Buone pratiche**:
    - Usa nomi di repository descrittivi (es. `sentiment-analysis-italian-2025`).
    - Assicurati che la documentazione sia completa e includa tutte le informazioni rilevanti.
    - Verifica la compatibilità del dataset con pipeline di machine learning (es. controlla che i formati siano corretti).

Seguendo questi passaggi, il tuo dataset sarà accessibile alla comunità globale, contribuendo al progresso della ricerca in _sentiment analysis_!

---
## Collegamenti
