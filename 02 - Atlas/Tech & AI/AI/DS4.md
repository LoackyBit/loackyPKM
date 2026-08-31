---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Salvatore Sanfilippo Rivoluziona l'AI ed Io Sono Gasato Ds4 Spiegato"
date: '2026-07-19'
updated: 2026-08-23T22:08
tags: [tech/youtube, tech/ai, tech/darfstar, tech/quantizzazione, tech/inference]
summary: "Salvatore Sanfilippo, meglio noto come Antirez, è il creatore di Redis, il database in‑memory più diffuso al mondo. Oltre a gestire il progetto, Antirez è anche divulgatore scientifico e ha recente..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Ds4|Salvatore Sanfilippo Rivoluziona l'AI ed Io Sono Gasato Ds4 Spiegato]]

# Salvatore Sanfilippo rivoluziona l’AI — DS4 spiegato

## Introduzione

Salvatore Sanfilippo, meglio noto come **Antirez**, è il creatore di Redis, il database in‑memory più diffuso al mondo. Oltre a gestire il progetto, Antirez è anche divulgatore scientifico e ha recentemente lanciato **Darf Star**, un motore di inferenza progettato per far girare i modelli di frontiera direttamente sui PC personali.

## Cos’è Darf Star

Darf Star è un **inference engine** ottimizzato per la famiglia di modelli DeepSeek V4.
- **Quantizzazione dinamica**: riduce la precisione dei pesi solo dove è possibile, passando da 16 bit a 8 bit o 2 bit a seconda della rilevanza del layer.
- **Mixture‑of‑Experts (MoE)**: attiva solo i **13 miliardi** di parametri necessari per una generazione, lasciando inattivi gli altri ≈ 271 miliardi.
- **SSD‑Streaming**: combina RAM e SSD per memorizzare gli esperti “meno usati”, riducendo drasticamente i requisiti di memoria.

### Quantizzazione dinamica e intelligente

<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>Quantizzazione dinamica</b></font></mark> consente di conservare le prestazioni su layer critici (precisione 8 bit) e comprimere intensamente quelli meno attivi (precisione 2 bit).
Questo approccio riduce l’occupazione da **568 GB** a **81 GB**, rendendo il modello eseguibile su MacBook Pro con **128 GB** di RAM.

### Architettura MoE di DeepSeek

![[ff2iPMjPu1s_4_l_architettura_.jpg]]

Il modello è suddiviso in **43 layer**, ognuno con **256 esperti**.
Il **router** seleziona, per ogni token, gli esperti più pertinenti; solo questi vengono attivati, riducendo il carico computazionale.

### Quantizzazione empirica basata sui dati

<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>Dataset di 2,9 milioni di token</b></font></mark> è stato usato per individuare i layer più “informativi”.
Gli esperti più attivi rimangono a alta precisione, mentre quelli meno influenti vengono compressi ulteriormente.

### SSD‑Streaming

![[ff2iPMjPu1s_5_quantizzazione_.jpg]]

Se la RAM non basta, gli esperti “sporadici” vengono caricati **on‑the‑fly** dalla SSD.
Il sistema mantiene una **coda** di esperti in RAM e prevede un **prefetch** intelligente dalla SSD quando necessario.

## Gestione del contesto

Darf Star può gestire fino a **1 milione di token** di contesto, ma salva gli indici su disco, permettendo di riprendere conversazioni lunghe senza ricomputare l’intero contesto.

## Benchmark delle performance

| Hardware | Prefill (token/s) | Generazione (token/s) |
|---|---|---|
| MacBook Pro M3 Max 128 GB | 58 (Q2) | 26 |
| MacBook Pro M5 Max | 87 | 34 |
| MacStudio M3 Ultra | 468 | 35 |
| Nvidia GB10 | 343 | 13 |

Il risultato mostra che **un singolo MacBook Pro è più veloce di un server GB10** per questo modello.

## Inferenza distribuita

![[ff2iPMjPu1s_9_inferenza_distr.jpg]]

Collegando più macchine via **Thunderbolt 5**, è possibile distribuire i layer su più PC, ottenendo uno **speed‑up** significativo rispetto a una singola macchina.

## Conclusioni

Darf Star rappresenta una svolta nella democratizzazione dell’AI:
- **Quantizzazione dinamica** mantiene performance elevate riducendo il consumo di memoria.
- **SSD‑Streaming** elimina il “bottleneck” della RAM, consentendo l’esecuzione anche su PC con risorse limitate.
- **Inference distribuita** permette di scalare ulteriormente superando i limiti hardware di un singolo nodo.

Il progetto è open‑source, con una community attiva e **15 000 stelle su GitHub**. Supportarlo significa contribuire a rendere l’IA di frontiera accessibile a tutti.
