---
name: brain-recall
description: Retrieval and synthesis interface modeled after NotebookLM. Provides executive answers backed by exact [[Note]] citations and strict zero-hallucination guards.
---
# Skill: /brain-recall (NotebookLM Retrieval & Synthesis)

Interfaccia di consultazione conversazionale e recupero della conoscenza personale sul Second Brain, modellata sull'esperienza **NotebookLM**.
Fornisce sintesi esecutive dirette, radicate esclusivamente nelle note e fonti presenti nel Vault, con citazioni esatte `[[Nome Nota]]` e rigore anti-allucinazione.

---

## 🎯 Obiettivi e Contratto di Interfaccia

1. **Dual Invocation Paradigm:**
   - **CLI Slash Command:** Sintassi esplicita `/brain-recall <query>` con filtri opzionali (`--area`, `--type`).
   - **Linguaggio Naturale:** Interrogazione conversazionale ("Cosa ho annotato riguardo a RAG?", "Quali sono i concetti chiave su Calcolo Differenziale?").
2. **Standardized Response Schema (Schema di Risposta in 3 Sezioni):**
   - 🎯 **1. Sintesi Esecutiva:** Risposta concisa, densa e direttamente orientata al quesito dell'utente, strutturata con punti elenco logici o brevi paragrafi.
   - 📚 **2. Fonti & Citazioni:** Elenco accurato di wiki-link esatti `[[Nome Nota]]` da cui sono state tratte le informazioni (con timestamp cliccabili `[MM:SS]` se provenienti da note video).
   - 🔗 **3. Connessioni Correlate:** 1-2 suggerimenti proattivi di collegamenti semantici o note adiacenti presenti nel grafo per stimolare esplorazioni interdisciplinari.
3. **Guardia Anti-Allucinazione Assoluta (Zero-Hallucination Guard):**
   - Se il concetto richiesto non è presente tra le note indicizzate del Vault, l'assistente **NON deve inventare risposte** né attingere a conoscenze generiche senza esplicita dichiarazione.
   - Restituisce immediatamente il messaggio di controllo standard:
     > ⚠️ **Nessuna corrispondenza trovata nel Vault**: Il concetto *"query"* non è presente tra le note del Second Brain. Nessuna informazione esterna è stata integrata per preservare l'integrità della tua knowledge base.

---

## 🛠️ Modalità di Invocazione

### Invocazione via Slash Command
```bash
# Query generale libera
/brain-recall "Come funziona il meccanismo di Self-Attention nei Transformers?"

# Query filtrata per macro-area
/brain-recall "Teorema di Fermat" --area education

# Query filtrata per tipo di nota
/brain-recall "Architetture RAG" --type concept

# Query combinata
/brain-recall "Analisi Finanziaria 2025" --area finance --type article
```

### Invocazione Conversazionale Naturale
- *"Cosa so riguardo a Docker e containerizzazione nel mio Vault?"*
- *"Riassumi i punti principali delle note sul Dopamine Detox."*
- *"Quali progetti ho attivi nell'area Tech?"*

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
```

---

## 🔗 Integrazione di Sistema & Fase 4

Questa skill definisce il contratto formale per il motore di ricerca ibrido (BM25 + Dense Semantic Embeddings) che verrà implementato nella Fase 4 con `recall_engine.py`.
