---
status: permanent
type: concept
area: tech
related: []
source: original
title: "01 Introduzione Probabilita - Azzardo della Matematica"
date: '2025-01-31'
updated: 2026-07-07T01:20
tags: []
summary: "Valore medio (media aritmetica): È la somma di tutti i valori divisa per il numero totale di elementi."
---
[[Home MOC|Home]] / [[Education & Learning]] / [[01 Introduzione Probabilita - Azzardo della Matematica]]

[[Azzardo della matematica]]
## **Statistica di base: media, varianza, moda e mediana**

- **Valore medio (media aritmetica)**: È la somma di tutti i valori divisa per il numero totale di elementi.
    
    $$ \bar{x} = \frac{\sum x_i}{n} $$
    
    Dove $x_i$ sono i valori e n è il numero di elementi.
    
- **Varianza ($\sigma^2$)**: Misura la dispersione dei dati rispetto alla media.
    
    $$ \sigma^2 = \frac{\sum (x_i - \bar{x})^2}{n} $$
    
- **Moda**: È il valore che compare più frequentemente in un insieme di dati.
    
- **Mediana**: È il valore centrale quando i dati sono ordinati in modo crescente. Se il numero di dati è pari, è la media dei due valori centrali.
    

---

## **Distribuzione gaussiana (Normale)**

- È una distribuzione di probabilità continua, simmetrica rispetto alla media.
    
- È descritta dalla funzione:
    
    $$ f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}} $$
    
    Dove $\mu$ è la media e $\sigma^2$ la varianza.
    
- Il **68-95-99.7 Rule** afferma che:
    
    - Il 68% dei dati si trova entro 1 deviazione standard dalla media.
    - Il 95% entro 2 deviazioni standard.
    - Il 99.7% entro 3 deviazioni standard.

---

## **Outlier (valori anomali)**

- **Outlier**: Valori che si discostano in modo significativo dalla media.
- Esempio: **GameStop stock** nel 2021, quando il prezzo delle azioni è aumentato rapidamente a causa di speculazioni e short squeeze.

---

## **Regressione e media mobile esponenziale**

- **Regressione**: Modello matematico per prevedere una variabile dipendente in base a una o più variabili indipendenti.
    
    - **Regressione lineare**:
    
    Dove $m$ è il coefficiente angolare e $b$ l’intercetta.
    
    ```
      $$
      y = mx + b
      $$
    ```
    
- **Media mobile esponenziale (EMA)**: Strumento usato in [[Finanza]] per analizzare i trend, dando più peso ai valori recenti rispetto a quelli passati.
    

---

## **Correlazione spuria**

- Si verifica quando due variabili sembrano correlate ma in realtà non hanno un nesso causale.
- Esempio: Aumento delle vendite di gelati e numero di attacchi di squali → entrambe correlate alla stagione estiva, ma senza relazione diretta.

---

## **Importanza della base statistica**

- **Se la base è errata, anche le correlazioni lo saranno.**
- **La statistica non è una scienza esatta**, ma uno strumento per analizzare dati con metodi probabilistici.
- **La precisione è fondamentale**: Errori nei dati iniziali possono portare a conclusioni errate.

---

## **Probabilità**

- **Probabilità semplice**: Evento singolo
    
    - Esempio: Qual è la probabilità di ottenere un 4 con un dado a 6 facce?
        
        $$ P(4) = \frac{1}{6} $$
        
- **Probabilità dipendente (composta)**: Due eventi dipendenti
    
    - Esempio: Qual è la probabilità di ottenere un 4 con un secondo dado, sapendo che il primo ha già dato 4?
        
        $$ P(4,4) = P(4) \times P(4) = \frac{1}{6} \times \frac{1}{6} = \frac{1}{36} $$
        
- **Probabilità di unione**: Probabilità che almeno uno dei due eventi si verifichi
    
    - Esempio: Qual è la probabilità di ottenere un 4 o un 5?
        
        $$ P(4 \cup 5) = P(4) + P(5) = \frac{1}{6} + \frac{1}{6} = \frac{1}{3} $$
        
- **Casi dipendenti e indipendenti**:
    
    - **Indipendenti**: Il risultato di un evento non influisce sul successivo (es. lanci di monete).
    - **Dipendenti**: Il primo evento influenza il secondo (es. estrazione di palline senza reinserimento).

---

## **Valore atteso**

- Media ponderata di tutte le possibili uscite di una variabile casuale.
    
- Esempio: Il valore atteso di un lancio di dado è:
    
    $$ E(X) = \sum x_i P(x_i) = 1 \times \frac{1}{6} + 2 \times \frac{1}{6} + \dots + 6 \times \frac{1}{6} = 3.5 $$
    

---

## **Schema Ponzi e Schema Piramidale**

- **Schema Ponzi**:
    - Sistema di investimento fraudolento dove i rendimenti per i vecchi investitori sono pagati con i soldi dei nuovi investitori.
    - Esempio: Bernie Madoff.
- **Schema Piramidale**:
    - Reclutamento di nuovi membri per finanziare quelli sopra nella gerarchia.
    - Collassa quando non ci sono più nuovi investitori.

---

## **Monty Hall Problem**

- Basato su un gioco televisivo:
    1. Scegli una porta su 3 (una ha il premio, le altre sono vuote).
    2. Il conduttore apre una porta vuota tra le due rimanenti.
    3. Ti chiede se vuoi cambiare scelta.
- **Strategia vincente**: Cambiare aumenta la probabilità di vittoria dal 33% al 66%.
- Spiegazione:
    - Se scegli la porta giusta inizialmente → non importa cambiare.
    - Se scegli una porta sbagliata (66% dei casi) → cambiare ti farà vincere.

---

- valore medio (media) e varianza, moda e mediana
- distribuzione gaussiana
- valori fuori dalla media si chiamano out lier ]?[ es. stock gamestop
- regressione e media mobile esponenziale
- correlazione spuria in probabilità
- se in statistica sbagli la base, la teoria, tutte le correlazioni sono sbagliate
- in statistica è importante essere precisi
- la statistica non è una scienza esatta
- probabilità semplice, composta, unione, dipendente pr. semplice: quante sono le probabilità che esce un 4 su un dado? pr. dipendente (o composta): quante sono le possibilità che esca 4 con un secondo dado? pr. unione
- casi dipendenti e indipendenti
- valore atteso
- schema ponzi
- schema piramidale
- monty hall problem

---
## Collegamenti
