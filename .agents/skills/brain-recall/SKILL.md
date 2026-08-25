---
name: brain-recall
description: Retrieval and synthesis interface modeled after NotebookLM. Provides executive answers backed by exact [[Note]] citations, video timestamps, and strict zero-hallucination guards.
---
# Skill: /brain-recall (NotebookLM Retrieval & Synthesis)

Interfaccia di consultazione conversazionale e recupero della conoscenza personale sul Second Brain, modellata sull'esperienza **NotebookLM**.
Fornisce sintesi esecutive dirette, radicate esclusivamente nelle note e fonti presenti nel Vault, con citazioni esatte `[[Nome Nota]]`, sezioni contestuali, timestamp video `[MM:SS]` e rigore anti-allucinazione.

---

## 🎯 Obiettivi e Contratto di Interfaccia

1. **Dual Invocation Paradigm:**
   - **CLI Slash Command:** Sintassi esplicita `/brain-recall <query>` con filtri opzionali (`--area`, `--type`, `--tag`, `--limit`, `--similar-to`).
   - **Linguaggio Naturale:** Interrogazione conversazionale ("Cosa ho annotato riguardo a RAG?", "Quali sono i concetti chiave su Calcolo Differenziale?").
2. **Standardized Response Schema (Schema di Risposta in 3 Sezioni):**
   - 🎯 **1. Sintesi Esecutiva:** Risposta concisa, densa e direttamente orientata al quesito dell'utente, strutturata con punti elenco logici o brevi paragrafi.
   - 📚 **2. Fonti & Citazioni:** Elenco accurato di wiki-link esatti `[[Nome Nota]]` con indicazione della sezione H2/H3 rilevante `(sezione: *Heading*)` e timestamp `[MM:SS]` o `[HH:MM:SS]` per note video.
   - 🔗 **3. Connessioni Correlate:** 1-2 suggerimenti proattivi di collegamenti semantici o note adiacenti presenti nel grafo per stimolare esplorazioni interdisciplinari.
3. **Guardia Anti-Allucinazione Assoluta (Zero-Hallucination Guard):**
   - Se il concetto richiesto non è presente tra le note indicizzate del Vault, l'assistente **NON deve inventare risposte** né attingere a conoscenze generiche senza esplicita dichiarazione.
   - Restituisce immediatamente il messaggio di controllo standard:
     > ⚠️ **Nessuna corrispondenza trovata nel Vault**: Il concetto *"query"* non è presente tra le note del Second Brain. Nessuna informazione esterna è stata integrata per preservare l'integrità della tua knowledge base.

---

## 🛠️ Modalità Operative & CLI Backend

Il motore Python di retrieval ibrido a 3 vie (YAML + BM25 + Smart Connections Dense Vectors) è `99 - Meta/Scripts/recall_engine.py`.

### Comandi CLI Backend Supportati

```bash
# 1. Query generale libera (Output JSON per agenti AI)
python3 "99 - Meta/Scripts/recall_engine.py" "Come funziona il meccanismo di Self-Attention?" --format json

# 2. Query filtrata per macro-area
python3 "99 - Meta/Scripts/recall_engine.py" "Teorema di Fermat" --area education --format json

# 3. Query filtrata per tipologia di nota
python3 "99 - Meta/Scripts/recall_engine.py" "Architetture RAG" --type concept --format json

# 4. Query filtrata per prefisso tag gerarchico
python3 "99 - Meta/Scripts/recall_engine.py" "Neural Networks" --tag tech/ai --format json

# 5. Ricerca per similarità semantica vettoriale (384-d Dense Embeddings)
python3 "99 - Meta/Scripts/recall_engine.py" --similar-to "Architettura Transformers e Attention" --format json

# 6. Ricostruzione forzata della cache incrementale
python3 "99 - Meta/Scripts/recall_engine.py" --reindex
```

### Parametri e Filtri CLI

| Parametro | Tipo | Valori Ammessi | Descrizione |
|---|---|---|---|
| `query` | Posizionale | String / Tokens | Termini di ricerca o quesito in linguaggio naturale |
| `--area` | Scelta controllata | `tech`, `education`, `mentality`, `finance`, `projects`, `meta`, `calendar` | Filtra per macro-area del Vault |
| `--type` | Scelta controllata | `concept`, `video`, `article`, `lecture`, `book`, `project`, `moc`, `journal` | Filtra per tipologia di nota |
| `--tag` | String | Prefisso tag (es. `tech/ai`) | Filtra note contenenti il tag o un sotto-tag |
| `--limit` | Intero | Default: `5` | Numero massimo di note restituite |
| `--format` | Scelta | `auto`, `json`, `markdown`, `pretty` | Formato di serializzazione output |
| `--similar-to` | String | Titolo nota o `[[Nome Nota]]` | Ricerca semantica vettoriale dei vicini più prossimi |
| `--reindex` | Flag | Boolean | Forza la ricostruzione completa della cache locale |
| `--vault-root` | Path | Percorso cartella | Radice personalizzata del Vault (default: root repository) |

---

## 🤖 Protocollo di Esecuzione per l'Agente AI

Quando l'utente richiede una consultazione tramite `/brain-recall` o con domanda in linguaggio naturale:

1. **Mapping Query & Parametri:** L'agente estrae termini di ricerca ed eventuali filtri (`--area`, `--type`, `--tag`, `--similar-to`).
2. **Invocazione Backend:** Esegue il comando CLI `python3 "99 - Meta/Scripts/recall_engine.py" <query> [opzioni] --format json`.
3. **Valutazione Risultati & Zero-Hallucination:**
   - Se `status == "empty"` (0 risultati): Restituisce **immediatamente ed esclusivamente** il messaggio di Zero-Hallucination Guard.
   - Se `status == "success"`: Sintetizza i risultati ricevuti rispettando rigorosamente lo **Schema in 3 Sezioni NotebookLM**.
4. **Suggerimenti di Drill-down Multi-Dominio:** Se `drilldown_suggestions` contiene aree adiacenti con corrispondenze rilevanti, include il box di suggerimento proattivo per facilitare l'esplorazione dell'utente.

---

## 📋 Standard di Risposta (Esempio Concreto)

```markdown
### 🎯 Sintesi Esecutiva
Il meccanismo di **Self-Attention** consente a ciascun token di una sequenza di interagire pesatamente con tutti gli altri token, calcolando punteggi di attenzione dinamici basati su tre matrici vettoriali: **Query (Q)**, **Key (K)** e **Value (V)**. Il prodotto scalare scalato viene normalizzato tramite softmax:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Nel contesto del Vault, le implementazioni evidenziano come la parallelizzazione dell'Attention elimini il collo di bottiglia sequenziale tipico delle RNN.

---

### 📚 Fonti & Citazioni
- [[Architettura Transformers e Attention]] (sezione: *Meccanismo di Scaled Dot-Product*)
- [[Deep Learning per Ingegneria]] (sezione: *Evoluzione delle Reti Sequenziali*)
- [[Attention Is All You Need Video]] (timestamp: `[12:45]`)

---

### 🔗 Connessioni Correlate
- [[Large Language Models MOC]]: Per la panoramica completa sui modelli generativi basati su transformer.
- [[Embedding Spaziali]]: Per comprendere come i vettori di input vengono mappati prima del livello di attenzione.

> 💡 **Suggerimento:** Trovate corrispondenze anche in Education (2). Usa `--area education` per raffinare.
```

---

## 🔒 Regole di Integrità e Robustezza

- **Click-Ready Wiki-Links:** Tutti i titoli citati devono essere formattati come `[[Nome Esatto Nota]]` corrispondenti a note reali del Vault.
- **Isolamento della Conoscenza:** Non utilizzare conoscenza generica di modelli esterni per completare dettagli non presenti nelle note richiamate.
- **Cache Local-Only:** Il file di cache `.recall_cache.json` non deve mai essere tracciato su Git ed è protetto in `.gitignore`.

