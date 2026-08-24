---
status: permanent
type: project
area: tech
related: []
source: original
title: "Animator2d"
date: '2025-03-06'
updated: 2026-05-22T18:29
tags: []
summary: "Un Viaggio nella Generazione di Animazioni Sprite con l’Intelligenza Artificiale"
---
[[Home MOC|Home]] / [[Projects MOC|Projects]] / [[Animator2D]]

Un Viaggio nella Generazione di Animazioni Sprite con l’Intelligenza Artificiale

#### Introduzione al Progetto
*Animator2D* è un progetto che ho intrapreso con l’idea di fondere la mia passione per i videogiochi indie e l’intelligenza artificiale. L’obiettivo era creare un sistema capace di generare animazioni sprite in stile pixel-art direttamente da descrizioni testuali—un prompt come “un cavaliere con armatura rossa che attacca con la spada, rivolto a destra” doveva trasformarsi in una sequenza animata pronta per un gioco, magari in formato GIF, sprite sheet o video. Volevo che fosse uno strumento utile per sviluppatori senza competenze grafiche, con sprite di altezza ideale di 35 pixel (range 25-50 pixel). Quello che è iniziato come un’idea semplice si è rivelato un percorso complesso, fatto di esperimenti, fallimenti e riflessioni. Questa nota racconta ogni passo del mio viaggio con *Animator2D*, un progetto che, a oggi, non funziona ancora come vorrei, ma che mi sta insegnando più di quanto immaginassi.

#### Il Punto di Partenza: Animator2D-v1.0.0-alpha (Sviluppo: 21 febbraio 2025 - Rilascio: 22 febbraio 2025)
Il mio viaggio è iniziato il 21 febbraio 2025, quando ho messo mano a *Animator2D-v1.0.0-alpha*. Ero pieno di entusiasmo: creare sprite animati con l’AI sembrava un sogno realizzabile. Ho scelto BERT come encoder testuale—mi sembrava un punto di partenza logico per processare descrizioni testuali—e ho costruito un generatore semplice con convoluzioni trasposte per produrre immagini a 64x64 pixel. Il giorno dopo, il 22 febbraio, ho rilasciato questa prima versione, completandola con un’interfaccia Gradio di base. Per testarla, generavo output simulati—cerchi gialli su sfondo blu—solo per vedere se il sistema rispondeva.

Ma i risultati reali erano deludenti. Invece di sprite animati, ottenevo un guazzabuglio di pixel senza forma. Mi sono reso conto che BERT, pur potente per il testo, non era abbastanza contestualizzato per generare immagini coerenti, e il generatore era troppo rudimentale per il compito. È stato un fallimento, ma mi ha aperto gli occhi: dovevo specializzare il modello e capire meglio cosa serviva per animare sprite. Questa versione non funzionava, ma mi ha dato il coraggio di andare avanti.

#### Semplificazione e Iterazioni: Animator2D-mini-v1.0.0-alpha (Sviluppo: 26 febbraio 2025 - Rilascio: 1 marzo 2025)
Dopo il primo tentativo, ho deciso di fare un passo indietro e semplificare. Il 26 febbraio 2025 ho iniziato a lavorare su *Animator2D-mini-v1.0.0-alpha*, una versione più leggera pensata per test rapidi. Ho sostituito BERT con CLIP, che prometteva una migliore connessione tra testo e immagini grazie al suo preaddestramento su coppie testo-immagine, e ho usato un generatore deconvoluzionale più snello. Ho scoperto il dataset `pawkanarek/spraix_1024` su Hugging Face—una raccolta di sprite con descrizioni, azioni e direzioni—e l’ho adottato come base per l’addestramento.

Ho sperimentato tre varianti, rilasciate il 1 marzo 2025:
- **10e**: Con 10 epoche, gli output a 64x64 pixel erano appena accennati—forme vaghe che non somigliavano a sprite.
- **100e**: Aumentando a 100 epoche, ho notato un miglioramento visibile: i pixel iniziavano a suggerire qualcosa, ma nulla di pratico.
- **250e**: Con 250 epoche, ho spinto il modello a una stabilità parziale, arrivando anche a 128x128 pixel in alcuni casi, ma senza coerenza.

Ho passato giorni a regolare iperparametri—batch size tra 8 e 16, learning rate tra 1e-4 e 2e-4—osservando curve di perdita che scendevano senza tradursi in risultati utili. Mi sono accorto che il problema non era solo la durata dell’addestramento, ma la mancanza di una struttura capace di gestire il concetto di animazione. Tuttavia, questa fase mi ha insegnato a lavorare con PyTorch, a costruire DataLoader personalizzati e a gestire dataset reali. Anche se non funzionava, *mini-v1.0.0-alpha* mi ha dato una base tecnica più solida.

#### Una Riscrittura Ambiziosa: Animator2D-v2.0.0-alpha (Sviluppo: 2 marzo 2025 - Rilascio: 3 marzo 2025)
Il 2 marzo 2025, con un po’ più di esperienza, ho deciso di riscrivere tutto da capo con *Animator2D-v2.0.0-alpha*. Ho abbandonato CLIP per T5, un modello di generazione testuale che speravo potesse catturare meglio i dettagli dei prompt, e ho introdotto un *Frame Interpolator*—una rete per generare frame multipli in sequenza. Il generatore è diventato più complesso, con layer deconvoluzionali per un upscaling graduale, e ho migliorato l’interfaccia Gradio per renderla più interattiva. Il 3 marzo ho rilasciato questa versione, caricandola su Hugging Face Spaces per condividerla online.

Ero fiducioso, ma il risultato mi ha deluso. Invece di animazioni, ottenevo una “pallina gialla su sfondo blu”. Dopo ore di debug, ho scoperto che avevo caricato un file `.pth` errato su Hugging Face—un errore banale ma devastante. Anche correggendolo, però, il modello non funzionava: gli output erano incoerenti, e le animazioni non prendevano forma. Questa esperienza mi ha insegnato a controllare ogni passaggio del deployment, ma mi ha anche fatto dubitare dell’approccio: forse stavo cercando di fare troppo con un unico modello.

#### Un Fix e Nuove Speranze: Animator2D-v3.0.0-alpha (Sviluppo e Rilascio: 6 marzo 2025)
Il 6 marzo 2025, invece di ripartire da zero, ho deciso di correggere *v2.0.0-alpha* con *Animator2D-v3.0.0-alpha*. Ho riscritto parzialmente il codice, mantenendo T5 come encoder e il *Frame Interpolator*, ma ho potenziato il generatore con *Residual Blocks* per maggiore stabilità e *Self-Attention* per migliorare i dettagli spaziali. Ho ottimizzato l’addestramento con AdamW e uno scheduler Cosine Annealing, usando uno split 80/20 del dataset `pawkanarek/spraix_1024`. L’interfaccia Gradio è stata aggiornata con opzioni come il controllo FPS e l’output GIF, e ho risolto l’errore di importazione su Hugging Face Spaces (`Lod34/Animator2D`).

Il rilascio è avvenuto lo stesso giorno, e per un momento ho sperato: gli output mostravano pixel che sembravano quasi sprite. Ma la verità era che non funzionava ancora—le animazioni erano incoerenti, e i risultati non rispecchiavano i prompt. Questo fix ha migliorato alcuni aspetti tecnici, ma non ha risolto il problema di fondo: il modello non riusciva a generare sprite animati utilizzabili.

| ![[Pasted image 20250306171159.png]] | ![[Pasted image 20250306171647.png]] |
| ------------------------------------ | ------------------------------------ |

#### Riflessioni sui Fallimenti
A questo punto, dopo *v3.0.0-alpha*, mi sono fermato a pensare. Avevo fatto progressi: sapevo usare PyTorch, gestire dataset, deployare su Hugging Face, e avevo sperimentato architetture sempre più complesse. Ma il risultato pratico? Zero. Mi sono chiesto cosa stessi sbagliando. Il dataset era troppo limitato? L’approccio monolitico—un unico modello per testo e animazione—era irrealistico? O forse mi mancava una comprensione più profonda di come generare sequenze temporali coerenti? È stato un momento di frustrazione, ma anche un punto di svolta: dovevo cambiare strategia.

#### Una Nuova Visione: Animator2D-v1.0.0 (Sviluppo iniziato: 6 marzo 2025)
Dopo il rilascio di *v3.0.0-alpha* il 6 marzo 2025, ho deciso di ripartire da zero con *Animator2D-v1.0.0*—un nome che segna un ritorno alle origini, ma con una visione diversa. Ispirato da software come Da Vinci Resolve, ho immaginato un processo in tre fasi:

1. **Creation**: L’utente crea o importa uno sprite base. Sto valutando se usare un modello preesistente (es. Stable Diffusion per pixel-art) per generarlo come immagine singola, o se分解 lo sprite in componenti (testa, braccia, gambe) per semplificare l’animazione. La prima opzione è più user-friendly, ma la seconda potrebbe essere più efficace—una scelta che devo ancora esplorare.

2. **Animation**: L’utente definisce i parametri—azione (es. “cammina”), direzione (es. “destra”), numero di frame—usando `pawkanarek/spraix_1024` come base. Potrei cercare dataset con più dettagli, come pose o keyframes, per arricchire questa fase. Separare l’animazione dalla creazione mi sembra un modo per ridurre la complessità.

3. **Generation**: L’output finale viene generato, con la possibilità di scegliere tra GIF, sprite sheet o video. Potrei aggiungere un’anteprima per migliorare l’esperienza.

Questa versione è ancora nella fase di ideazione—non ho codice funzionante—ma mi dà speranza: dividendo il problema, posso affrontarlo un pezzo alla volta.

#### Dettagli Tecnici del Percorso
- **Dataset**: `pawkanarek/spraix_1024`, preprocessato con ridimensionamento, normalizzazione e conversione RGB. È stato un punto di partenza, ma forse non basta per animazioni.
- **Architetture**: Ho usato BERT (*v1.0.0-alpha*), CLIP (*mini-v1.0.0-alpha*), e T5 (*v2.0.0-alpha* e *v3.0.0-alpha*), con generatori deconvoluzionali sempre più complessi—fino a *Residual Blocks* e *Self-Attention* in *v3.0.0-alpha*.
- **Addestramento**: Batch size 8-16, learning rate 1e-4/2e-4, fino a 250 epoche in *mini*. Ho usato MSE Loss, ma sto pensando a alternative.
- **Interfaccia**: Da un Gradio base in *v1.0.0-alpha* a una versione avanzata in *v3.0.0-alpha* su Hugging Face Spaces.
- **Tecnologie**: PyTorch, Transformers, Gradio, Diffusers, PIL, NumPy. GPU (CUDA) quando possibile, altrimenti CPU.

#### Sfide Affrontate
- **Output incoerenti**: Gli sprite non seguono i prompt, e le animazioni sono un caos.
- **Dataset limitato**: `pawkanarek/spraix_1024` manca della varietà necessaria.
- **Errori di deployment**: La “pallina gialla” di *v2.0.0-alpha* mi ha insegnato a verificare i file.
- **Complessità**: Un modello unico era troppo ambizioso, portandomi al design modulare.

#### Prossimi Passi
- Sviluppare *Animator2D-v1.0.0* con le tre fasi.
- Testare modelli preesistenti per la *Creation*.
- Cercare dataset migliori o crearne uno mio.
- Esplorare pipeline di diffusione per risultati più stabili.
- Migliorare la coerenza delle animazioni.

#### Riflessioni Personali
*Animator2D* è stato un viaggio intenso. La delusione della “pallina gialla” e gli output incoerenti mi hanno fatto dubitare, ma ogni passo mi ha fatto crescere. Ho imparato a programmare reti neurali, debuggare problemi complessi e non arrendermi. Anche se non funziona ancora, questo progetto è una testimonianza della mia perseveranza. Il codice è su GitHub, e *v3.0.0-alpha* è su Hugging Face—non perfetto, ma un punto di partenza. Continuerò, perché so che la soluzione è là fuori.

---
## Collegamenti
