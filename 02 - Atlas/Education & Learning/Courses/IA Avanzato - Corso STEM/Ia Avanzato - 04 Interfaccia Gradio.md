---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Ia Avanzato - 04 Interfaccia Gradio"
date: '2025-02-12'
updated: 2026-07-07T01:20
tags: []
summary: "Gradio è una libreria Python che permette di creare facilmente interfacce web per modelli di machine learning, funzioni e algoritmi. È particolarmente utile per creare demo e prototipi rapidamente."
---
[[Home MOC|Home]] / [[Education & Learning]] / [[Ia Avanzato - 04 Interfaccia Gradio]]

[[IA Avanzato]]
### Cos’è Gradio?

Gradio è una libreria Python che permette di creare facilmente interfacce web per modelli di machine learning, funzioni e algoritmi. È particolarmente utile per creare demo e prototipi rapidamente.

### Prima demo

Analizziamo il codice:

```python
import gradio as gr

```

Questa riga importa la libreria Gradio e la rinomina come 'gr' per comodità.

```python
def greet(name, intensity):
 return "Hello, " + name + "!" * int(intensity)

```

Questa è la funzione che verrà esposta nell'interfaccia web:

- Prende due parametri: `name` (il nome) e `intensity` (un numero)
- Restituisce una stringa che concatena "Hello, " con il nome fornito
- Moltiplica il punto esclamativo "!" per il numero specificato in `intensity`

```python
demo = gr.Interface(
 fn=greet,
 inputs=["text", "slider"],
 outputs=["text"],
)

```

Qui creiamo l'interfaccia Gradio:

- `fn=greet`: specifica quale funzione utilizzare
- `inputs=["text", "slider"]`: definisce due input:
 - un campo di testo per il nome
 - uno slider per l'intensità
- `outputs=["text"]`: specifica che l'output sarà testo

```python
demo.launch()

```

Questa riga avvia il server web che mostrerà l'interfaccia.

Quando esegui questo codice, si aprirà una pagina web con:

1. Un campo di testo dove inserire il nome
2. Uno slider per selezionare l'intensità
3. Un'area dove verrà mostrato il risultato

Per esempio, se inserisci:

- Nome: "Mario"
- Intensità: 3

Otterrai come output: "Hello, Mario!!!"

Gradio è molto utile perché:

- Rende interattive le tue funzioni Python
- Non richiede conoscenze di sviluppo web
- Supporta molti tipi di input/output (immagini, audio, video, ecc.)
- È facile da integrare con altri framework come PyTorch o TensorFlow

---

## **Prima Demo: Saluto Personalizzato**
Vediamo il codice:  

```python
import gradio as gr
```
Questa riga importa la libreria **Gradio**, abbreviandola come `gr` per comodità.  

```python
def greet(name, intensity):
 return "Ciao, " + name + "!" * int(intensity)
```
Questa è la funzione che verrà esposta nell'interfaccia web:  
- **Prende due parametri**:
 - `name` (stringa) → Il nome della persona  
 - `intensity` (numero) → Il numero di punti esclamativi da aggiungere  
- **Restituisce** una stringa che concatena `"Ciao, "` con il nome e un numero variabile di `!`  

```python
demo = gr.Interface(
 fn=greet,
 inputs=["text", "slider"],
 outputs=["text"],
)
```
Qui creiamo l’interfaccia Gradio:  
- `fn=greet` → Specifica la funzione da usare  
- `inputs=["text", "slider"]` → Definisce gli input:
 - Un **campo di testo** per il nome  
 - Uno **slider** per l’intensità  
- `outputs=["text"]` → L’output sarà una stringa di testo  

```python
demo.launch()
```
Avvia il server web e apre l’interfaccia nel browser.  

Se inserisci:  
- **Nome**: "Luca"  
- **Intensità**: 3  

Otterrai: **"Ciao, Luca!!!"**  

---

## **Seconda Demo: Scambio di Nomi**
Il codice è molto simile al precedente, con una piccola differenza:  

```python
def greet2(name1, name2):
 return "Sono " + name1 + ", ciao " + name2 + "!"
```
- Questa funzione accetta **due nomi** e genera un saluto personalizzato.  

```python
demo = gr.Interface(
 fn=greet2,
 inputs=["text", "text"],
 outputs=["text"],
)
```
- Gli input sono **due campi di testo** invece di uno solo e uno slider.  

```python
demo.launch()
```
Avvia l’interfaccia.  

Se inserisci:  
- **Nome1**: "Marco"  
- **Nome2**: "Giulia"  

Otterrai: **"Sono Marco, ciao Giulia!"**  

---

## **Terza Demo: Somma e Prodotto**
Questa demo introduce un’interfaccia con **tre numeri** in input e due valori di output.  

```python
def somma(num1, num2, num3):
 sum_result = num1 + num2 + num3
 product_result = num1 * num2 * num3
 return sum_result, product_result
```
- **Accetta tre numeri** e calcola sia la **somma** che il **prodotto**.  

```python
demo = gr.Interface(
 title="La calcolatrice di Lorenzo!",
 fn=somma,
 inputs=["number", "number", "number"],
 outputs=[gr.Number(label="La somma è: "),
 gr.Number(label="Il prodotto è: ")],
)
```
- Aggiunge un **titolo** all’interfaccia.  
- Gli input sono **tre numeri**.  
- Gli output sono due numeri, con **etichette personalizzate**.  

```python
demo.launch(share=True)
```
- `share=True` → Genera un link pubblico per accedere all’interfaccia da qualsiasi dispositivo.  

Se inserisci:  
- **Numeri**: 2, 3, 4  

Otterrai:  
- **Somma**: 9  
- **Prodotto**: 24  

---

### **Conclusione**
Gradio è uno strumento potente per creare interfacce web interattive in pochi minuti. I suoi vantaggi principali:  
Semplice da usare  
Non richiede conoscenze di sviluppo web  
Supporta vari tipi di input/output  
Perfetto per testare funzioni Python rapidamente

---
## Collegamenti
