---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 02 NLP"
date: '2025-01-31'
updated: 2026-07-07T01:20
tags: []
summary: "L'Elaborazione del Linguaggio Naturale (NLP) è un campo dell'intelligenza artificiale che permette alle macchine di comprendere, interpretare e generare il linguaggio umano."
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[Ia Avanzato - 02 NLP]]

[[IA Avanzato]]
## **1. Cos’è NLP?**

L'**Elaborazione del Linguaggio Naturale (NLP)** è un campo dell'intelligenza artificiale che permette alle macchine di comprendere, interpretare e generare il linguaggio umano.

Viene usato in applicazioni come chatbot, traduzione automatica, analisi del sentiment e riconoscimento vocale.

---

## **2. Reti Neurali**

Le **reti neurali artificiali** sono modelli matematici ispirati al funzionamento del cervello umano. Possono essere di vari tipi:

### **a. Reti Neurali Feed-Forward**

- Sono le più semplici: l'informazione si muove in un'unica direzione, dagli input all'output, senza loop.
- Utili per classificazione e regressione.

### **b. Reti Neurali Ricorrenti (RNN)**

- Hanno **connessioni ricorrenti**, cioè memorizzano informazioni da input precedenti.
- Utili per sequenze (testo, audio), ma hanno difficoltà con lunghe dipendenze nel tempo.
- Problema principale: **scomparsa del gradiente**, che limita l'apprendimento a lungo termine.

---

## **3. Convertire lettere/parole in numeri**

Per far capire il testo ai modelli, bisogna convertirlo in numeri.

### **a. Ogni lettera un numero**

- Es: 'A' = 1, 'B' = 2…
- Problema: non tiene conto del significato delle parole.

### **b. Ogni parola un numero**

- Es: "gatto" = 15, "cane" = 23…
- Problema: parole nuove (fuori dal vocabolario) non possono essere gestite.

### **c. Problema della Tokenizzazione**

- Alcune parole hanno più significati (es. "banca" può riferirsi a una sedia o a un istituto finanziario).
- Lingue come il cinese non separano le parole con spazi, rendendo difficile la segmentazione.
- Soluzione: usare tecniche come **Byte Pair Encoding (BPE)** o **WordPiece**, che dividono le parole in sottoparti più gestibili.

---

## **4. Cos’è un Transformer?**

Un **Transformer** è un'architettura di rete neurale per NLP che usa il **meccanismo di attenzione** per processare l’intera sequenza di testo in parallelo (a differenza delle RNN).

È alla base di modelli come **BERT, GPT e T5**.

---

## **5. Cosa può fare un Transformer?**

### **a. Completamento di frasi mascherate**

I transformer predicono parole mancanti basandosi sul contesto:

- **"Il [MASK] ha una grande coda vistosa."** → Risposta: **pavone** (perché il contesto suggerisce un animale con una coda vistosa).
- **"L’animale più veloce della savana è il [MASK]."** → Risposta: **ghepardo**.

Con una rete **feed-forward**, i risultati non sarebbero accurati perché manca la capacità di modellare il contesto.

Un altro esempio:

- **"Oggi è una bella [MASK]."** → Probabilmente **giornata**, perché si capisce che la parola termina in "a" grazie alla tokenizzazione.

### **b. Articolo "Attention is All You Need"**

L'articolo ha introdotto i **Transformer**, mostrando che mascherando parole si può imparare l'importanza delle altre nel contesto.

---

## **6. Encoder (+ matrice, + tensore)**

- L'**encoder** è la parte del Transformer che legge l’input e ne crea una rappresentazione numerica.
    - Usa il **meccanismo di attenzione** per pesare l'importanza delle parole nel contesto.
    - Produce **tensori** (array multidimensionali) che rappresentano le relazioni tra parole.

## **7. Decoder**

Il **decoder** prende la rappresentazione dell’encoder e genera un output (es. traduzione in un’altra lingua).

### **a. Funzionamento Separato**

- Un decoder può essere usato da solo, come nei modelli **GPT**, che generano testo.

### **b. Funzionamento Insieme all’Encoder (migliore)**

- Usato nei modelli **BERT** o **T5** per compiti più complessi come la traduzione automatica.
 
![[Pasted image 20250201222523.png]]

**Processo Self-Supervised**

- I modelli si addestrano mascherando parti del testo e cercando di ricostruirle.
- Non serve un dataset etichettato (da cui il termine **self-supervised learning**).

**GLUE Databases**

- Benchmark usati per valutare le prestazioni dei modelli NLP in vari compiti (analisi del sentiment, inferenza testuale, ecc.).

---

## **8. Transfer Learning**

- Tecnica in cui un modello già addestrato su un grande dataset viene **riutilizzato** per nuovi compiti, risparmiando tempo e dati.

Esempio:

- **BERT pre-addestrato su Wikipedia** → **Adattato per l’analisi delle recensioni su Amazon**.

---

## **9. Fine-Tuning**

- Processo in cui un modello pre-addestrato viene addestrato **ulteriormente** su un dataset specifico per ottimizzarlo per un compito preciso.

Esempio:

- Prendere **GPT-3** e adattarlo per **scrivere articoli di finanza** con dati specifici.

---

### **Conclusione**

I **Transformer** hanno rivoluzionato l’NLP grazie all’**attenzione**, permettendo risultati eccezionali rispetto alle RNN. **Transfer Learning e Fine-Tuning** rendono questi modelli flessibili e applicabili a numerosi scenari.

---

1. cos’è nlp
    
2. reti neurali
    
    - feed forward
    - recurrent … (no buoni risultati)
3. convertire lettere/parole in numeri
    
    1. ogni lettera un numero
    2. ogni parola un numero
    3. problema della tokenizzazione
4. cos’è un transformer
    
5. cosa può fare un transformer
    
    1. frase con maschera dove la maschera è il nome di un animale “il [mask] ha una grande coda vistosa.” alcune volte il transformer risponderà pavone.. “l’animale più veloce della savana è il [mask].” alcune volte il transformer risponderà il ghepardo… con reti feed-forward risultati eccezionali ”oggi è una bella [mask]”. con i token si può capire che la parola terminerà probabilmente con la “a” (quindi no ‘mattino’, si ‘giornata’)
    2. articolo: “attention is all you need” mascherando le parole si riesce ad avere l’attenzione sulle altre
6. encoder (+matrice, +tensore)
    
7. decoder
    
    1. funzionamento separato
    2. funzionamento insieme all’encoder, migliore

processo self-supervised

]glue databases[

![CleanShot 2025-01-29 at 15.21.53@2x.png](attachment:5ca7f919-cdc8-4228-b0cd-2494d899623f:CleanShot_2025-01-29_at_15.21.532x.png)

1. transfer learning
2. fine tuning

---
## Collegamenti
