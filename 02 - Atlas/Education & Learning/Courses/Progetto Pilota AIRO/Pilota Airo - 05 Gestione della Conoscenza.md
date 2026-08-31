---
status: permanent
type: project
area: tech
related: []
source: original
title: "Pilota Airo - 05 Gestione della Conoscenza"
date: '2026-03-05'
updated: 2026-07-07T01:20
tags: []
summary: "Nel dominio della robotica avanzata, il passaggio dalla reattività procedurale alla persistenza cognitiva segna la transizione tra un semplice automa e un agente intelligente. La gestione della con..."
---
[[Home MOC|Home]] / [[Education & Learning]] / [[Pilota Airo - 05 Gestione della Conoscenza]]

[[Pilota AIRO]]
# Pilota AIRO - 05 Gestione della Conoscenza

Nel dominio della robotica avanzata, il passaggio dalla reattività procedurale alla persistenza cognitiva segna la transizione tra un semplice automa e un agente intelligente. La gestione della conoscenza in SMARRtino non è una mera archiviazione di dati, ma l'implementazione di una **Long-Term Memory (LTM)** che permette al robot di trascendere i limiti della memoria di contesto (Short-Term Memory) tipica degli LLM standard. Questa capacità di mantenere una coerenza informativa tra diverse sessioni di lavoro trasforma il robot in un'entità capace di apprendimento esperienziale, in grado di agire non solo sulla base di comandi immediati, ma su un patrimonio di "fatti" accumulati nel tempo.

## 1. Le Primitive della Conoscenza: L'Interfaccia della Memoria

L'interazione con lo strato cognitivo di SMARRtino avviene attraverso la classe `AI` definita nel modulo `ai.py`. Questa interfaccia astrae la complessità del database vettoriale sottostante, offrendo allo sviluppatore quattro primitive fondamentali per la manipolazione della conoscenza:

- **`ai.clear_memory()`**: Esegue il reset completo dello stato cognitivo, eliminando tutti i documenti nella collezione e azzerando l'indice incrementale degli ID.
- **`ai.memorize(content)`**: Consente al robot di archiviare un'informazione testuale. Tecnicamente, la funzione utilizza un sistema di **ID incrementali** (`self.memoryid += 1`), essenziale per mantenere un ordine cronologico e logico delle esperienze acquisite.
- **`ai.print_memory()`**: Fornisce una visualizzazione trasparente dei fatti archiviati, permettendo all'operatore di verificare l'integrità del patrimonio informativo del robot.
- **`ai.remember(content, max_dist=1.0, n_results=3)`**: Rappresenta il cuore pulsante del sistema. Contrariamente a una semplice query di database, questa funzione implementa una pipeline di **Retrieval-Augmented Generation (RAG)**.

Il funzionamento di `ai.remember` è un processo cognitivo end-to-end: il sistema interroga il database vettoriale cercando i `n_results` più pertinenti. I risultati vengono filtrati attraverso il parametro `max_dist` (distanza semantica), dove il valore predefinito di **1.0** funge da baseline architettonica. Se vengono trovati fatti pertinenti, questi vengono iniettati in un prompt di sistema denominato `remember_system`, che istruisce l'LLM a rispondere basandosi esclusivamente su tali evidenze. In assenza di informazioni valide nello spazio latente, il sistema è istruito a dichiarare esplicitamente l'indisponibilità di dati, evitando fenomeni di allucinazione.

La calibrazione di `max_dist` è un'operazione critica di ingegneria del recupero: una distanza troppo elevata aumenta la _recall_ a rischio di includere rumore, mentre una distanza ridotta favorisce la _precision_, rischiando però di ignorare fatti correlati ma espressi con una sintassi differente.

## 2. Architettura Tecnica: Integrazione con ChromaDB

La persistenza della conoscenza è garantita dall'integrazione con **ChromaDB**, un database vettoriale locale configurato tramite un `PersistentClient` nella directory `./kb`. Questa scelta architettonica è strategica per un robot educativo: garantisce la sovranità locale dei dati e la persistenza dei ricordi anche dopo il riavvio del sistema hardware.

A differenza della ricerca testuale classica basata su parole chiave, SMARRtino opera attraverso la **vettorializzazione** (embeddings). Quando un fatto viene memorizzato o cercato, ChromaDB trasforma il linguaggio naturale in coordinate all'interno di uno spazio vettoriale ad alta dimensionalità. La ricerca avviene per **prossimità semantica**: il robot non cerca la corrispondenza esatta delle parole, ma la vicinanza dei concetti. Questo permette a SMARRtino di rispondere correttamente a una domanda su una "palla arancione" anche se l'informazione originale registrata parlava di un "oggetto sferico color pesca", implementando un vero **recupero associativo**.

## 2.1 Esempio di Memorizzazione: "oggi il cielo è sereno"

Per comprendere in modo concreto il flusso interno di `ai.memorize(content)`, analizziamo l'elaborazione del seguente fatto testuale:

```
"oggi il cielo è sereno"
		│
        ├──► [testo originale] ──► chroma.sqlite3
        │                           ├─ tabella: 
		│	 					    │  embedding_metadata
        │                           └─ tabella: 
		│					          embedding_fulltext_search
        │
        └──► [embedding model] ──► [0.023, -0.417, 0.891, ...]
                                    ├─ chroma.sqlite3 
									│  (tabella:embeddings)
                                    └─ <UUID>/data_level0.bin  
                                       (indice HNSW)
```

**Spiegazione passo-passo**:
- Il **testo originale** viene salvato direttamente nel file `chroma.sqlite3` all'interno delle tabelle `embedding_metadata` (per ID, timestamp, ecc.) e `embedding_fulltext_search` (per ricerche full-text veloci).
- Contemporaneamente, il modello di embedding (es. `all-MiniLM-L6-v2`) converte il testo in un vettore numerico ad alta dimensionalità.
- Il vettore viene inserito nella tabella `embeddings` del database SQLite.
- L'indice **HNSW** (Hierarchical Navigable Small World) viene aggiornato nel file binario `data_level0.bin` all'interno della cartella della collezione (identificata da un UUID). Questo indice permette ricerche ANN ultra-veloci durante le chiamate a `ai.remember()`.

Questo doppio binario (testo + vettore + indice) garantisce sia la persistenza che l'efficienza del recupero semantico.

## 3. Workflow Integrato: Dalla Percezione Visiva al Ricordo

Il culmine dell'integrazione cognitiva si manifesta nel flusso di lavoro che unisce mobilità, visione e memoria. Questo ciclo rappresenta il metodo con cui il robot costruisce autonomamente la propria esperienza del mondo:

1. **Esplorazione**: Il robot si posiziona nell'ambiente tramite comandi di navigazione.
2. **Acquisizione**: Viene catturato un frame visivo tramite `robot.get_image()`.
3. **Percezione e Descrizione**: L'immagine viene processata da `ai.vision(img, prompt)`. Qui, il prompt (es. "descrivi la scena") agisce come catalizzatore semantico, trasformando i pixel grezzi in una descrizione testuale strutturata dal VLM.
4. **Persistenza**: La descrizione testuale viene passata ad `ai.memorize()`, cristallizzando l'osservazione istantanea in un fatto permanente.

Consideriamo l'applicazione pratica osservata nel Modulo 5: durante il pattugliamento, SMARRtino può memorizzare sequenzialmente di aver visto una "palla rossa e una palla verde", poi un "cubo nero e un cubo verde" e infine un "cilindro blu e un cilindro rosso". Grazie alla pipeline RAG di `ai.remember`, il robot è in grado di rispondere a interrogazioni complesse come "quanti oggetti verdi hai visto?", sintetizzando informazioni distribuite in momenti diversi e posizioni spaziali differenti. Questo processo trasforma dati sensoriali volatili in una base di conoscenza interrogabile e persistente.

## 4. Conclusioni e Orizzonti Evolutivi

L'implementazione della gestione della conoscenza eleva SMARRtino da strumento programmato a **partner collaborativo**. La capacità di "ricordare" permette un'interazione uomo-robot naturale e contestuale, dove il robot apprende e si adatta all'ambiente operativo.

Dal punto di vista architettonico, questo modulo rappresenta la chiusura del cerchio dell'autonomia decisionale. Un robot che possiede una memoria a lungo termine non è più vincolato alla pura esecuzione di script, ma agisce come un agente autonomo capace di mantenere una coerenza narrativa e operativa. Questa integrazione tra percezione visiva, ragionamento probabilistico tramite LLM e persistenza vettoriale costituisce lo stato dell'arte nella robotica di servizio e definisce il futuro dell'intelligenza artificiale incarnata.

---
## Collegamenti
