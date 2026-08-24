---
stage: fine-tuned 🧠
draft: false
type: article
area: tech
related: []
source: original
title: "Bitcoin Protocollo"
date: '2026-03-09'
updated: 2026-07-12T21:45
tags: [finance/crypto, tech/blockchain, tech/crittografia, tech/proof-of-work, tech/sistemi-distribuiti, tech/sha-256]
summary: "Immaginiamo di voler creare la nostra moneta digitale da zero. Come faremmo a farla funzionare senza affidarci a una banca? Ecco quindi una spiegazione del Bitcoin Protocol|protocollo Bitcoin."
---
[[Home MOC|Home]] / [[Blog]] / [[Bitcoin Protocol|Bitcoin Protocollo]]

Immaginiamo di voler creare la nostra moneta digitale da zero. Come faremmo a farla funzionare senza affidarci a una banca? Ecco quindi una spiegazione del [[Bitcoin Protocol|protocollo Bitcoin]].

## 1. Il Libro Mastro (Ledger) Condiviso

Partiamo dalle basi. Invece di scambiarci banconote fisiche, io e i miei amici decidiamo di tenere un **registro** (un _ledger_). Ogni volta che qualcuno paga un altro, aggiungiamo una riga:

![[But how does bitcoin actually work_ 3-7 screenshot.png|1000x400]]

Alla fine del mese, guardiamo i saldi e chi è in negativo paga chi è in positivo.

**Ma c'è un problema enorme:** il registro è pubblico (o su un sito web condiviso). Cosa impedisce a Bob di aggiungere di nascosto la riga _"Alice paga a Bob 100$"_?

## 2. Il Problema dell'Autenticità: Firme Digitali

Abbiamo bisogno che solo Alice possa autorizzare un pagamento proveniente da lei. Nel mondo fisico usiamo le firme autografe. Nel mondo digitale usiamo la [[Crittografia Asimmetrica]].

Ogni persona genera due chiavi:

- **[[Chiave Privata]]**: Una password che tieni segreta. Serve a _creare_ la firma.
    
- **[[Chiave Pubblica]]**: Un indirizzo pubblico. Serve agli altri per _verificare_ che la firma sia autentica.
    

La magia matematica è che la firma digitale da 256 bit cambia a seconda del messaggio.

![[But how does bitcoin actually work_ 5-40 screenshot.png]]

Se Bob prova ad alterare il messaggio in _"Alice paga Bob 100$"_, la *firma* risulterà **invalida** se testata contro la chiave pubblica di Alice.

Ora siamo sicuri di _chi_ autorizza la transazione. **Tutto risolto? Non ancora.**

## 3. Il Problema della Fotocopia (Replay Attack)

Alice paga legittimamente Bob 20$ e genera una transazione perfetta con una firma valida.

Bob la riceve. Poi Bob si rende conto di una cosa: _il messaggio e la firma sono file digitali_. Cosa gli impedisce di fare "Copia-Incolla" di quella riga esatta e incollarla nel registro altre 10 volte?

```
4. Alice paga Bob 20$ (Firma123) ✅ Valida
5. Alice paga Bob 20$ (Firma123) ✅ Valida (Bob l'ha appena incollata di nuovo!)
```

Per risolvere questo, dobbiamo rendere ogni transazione unica.

Introduciamo un **ID Univoco** (un numero seriale) per ogni transazione.

```
[ID: 001] Alice paga Bob 20$ (Firma per l'ID 001)
```

Ora, se Bob copia e incolla la transazione 001, la rete la rifiuterà perché l'ID 001 è già stato speso. Se Bob prova a cambiare l'ID in 002, la firma di Alice si rompe (perché il contenuto del messaggio è cambiato).

## 4. Decentralizzare il Registro

Finora abbiamo un registro perfetto. Ma _dove_ risiede fisicamente questo file?

Se lo teniamo sul server di Charlie, Charlie ha il potere supremo. Può spegnere il server o censurare le transazioni di Alice.

**La soluzione:** Tutti ricevono una copia del registro. Quando Alice vuole pagare Bob, "grida" al mondo (fa _broadcasting_ alla rete P2P): _"Ehi tutti, registrate che Alice paga Bob 20$!"_. Tutti ascoltano e aggiornano il loro file.

![[But how does bitcoin actually work_ 11-30 screenshot.png]]

Ma qui sorge un altro grande problema.

## 5. Il Paradosso dell'Ordine Temporale (La Doppia Spesa)

Immagina che Alice abbia solo 20$ in totale.

Invia un messaggio a metà della rete: *"Alice paga Bob 20$"*.

Nello stesso istante millimetrico, invia un messaggio all'altra metà: _"Alice paga Charlie 20$"_.

Questo è il problema della [[Doppia Spesa]]. Poiché i segnali di rete impiegano tempo a viaggiare, alcuni nodi riceveranno prima il pagamento a Bob e considereranno nullo quello a Charlie (perché Alice ha finito i soldi). Altri nodi faranno l'esatto contrario.

Abbiamo perso il consenso. Chi decide quale transazione è arrivata _prima_?

## 6. La Soluzione: SHA-256 e Proof of Work

Senza un arbitro centrale (la banca) per decidere l'ordine temporale, dobbiamo usare la matematica computazionale.

Prendiamo l'elenco delle nuove transazioni e lo passiamo in un imbuto crittografico chiamato [[SHA-256]]. Questa funzione prende qualsiasi dato e sputa fuori una stringa alfanumerica a caso di lunghezza fissa (Hash).

![[But how does bitcoin actually work_ 14-9 screenshot.png]]

Per far sì che tutti si accordino sull'ordine delle transazioni, raggruppiamo i pagamenti in un **Blocco**.

Ma non possiamo semplicemente aggiungere il blocco al registro. Imponiamo una regola difficilissima: **il blocco è valido solo se il suo Hash inizia con un sacco di zeri** (es. `0000000000...`).

Dato che l'Hash è imprevedibile, come facciamo? Aggiungiamo un numero casuale al blocco, chiamato **Nonce**.

![[But how does bitcoin actually work_ 15-8 screenshot.png]]

I _miners_ della rete accendono i loro computer e iniziano a provare numeri (Forza Bruta):

- Nonce 1? Hash `f3a2...` (Sbagliato)
    
- Nonce 2? Hash `8b19...` (Sbagliato)
    
- ...dopo miliardi di tentativi...
    
- Nonce 5.483.291? Hash `0000004a...` (Giusto!)
    

**Perché far fare tutta questa fatica ai computer?**

Perché richiede tempo (circa 10 minuti). Questa [[Proof of Work]] (Prova di Lavoro) rallenta l'aggiunta di blocchi, dando alla rete il tempo di sincronizzarsi. Se Alice prova a fare una Doppia Spesa, la transazione che finisce nel blocco risolto per primo diventa la verità. 

## 7. La Catena di Blocchi (Blockchain) e la Fiducia

Ogni nuovo blocco deve contenere al suo interno l'Hash del blocco precedente. Questo li incatena indissolubilmente.

![[But how does bitcoin actually work_ 17-0 screenshot.png]]

Se Alice (un'attaccante) volesse tornare indietro nel tempo al Blocco #50 per cancellare un suo pagamento e rimettersi i soldi in tasca, cambierebbe i dati di quel blocco. Ma questo cambierebbe immediatamente l'Hash del Blocco #50!

Di conseguenza, il Blocco #51 (che conteneva il vecchio hash) si romperebbe. E così via.

Per frodare la rete, Alice dovrebbe ricalcolare la Proof of Work del Blocco 50, poi del 51, poi del 52... e farlo _più velocemente_ di quanto il resto del mondo stia calcolando i nuovi blocchi. Matematicamente e fisicamente impossibile.

![[But how does bitcoin actually work_ 21-15 screenshot.png]]

### La Regola Finale

Se la rete si divide temporaneamente (due miner risolvono un blocco contemporaneamente creando un bivio), quale strada si segue?

**Si segue sempre la catena valida più lunga.**

Perché la catena più lunga rappresenta quella su cui è stata spesa più energia e più lavoro computazionale. È l'orologio decentralizzato del mondo.

Ed è così che, partendo da un registro tra amici, abbiamo appena inventato Bitcoin.

## Passaggi Pratici ed Errori Comuni

### Errori Comuni da non fare

- **"Il Bitcoin crittografa le transazioni"**: Sbagliato! Le transazioni sono in chiaro e pubbliche per tutti. La crittografia (le firme digitali) serve solo a dimostrare l'_autorizzazione_ a spendere, non a nascondere i dati.
    
- **"I miner risolvono calcoli super complessi di matematica superiore"**: No. Come spiegato nel passaggio 6, è solo _forza bruta_. Immagina i miner come se cercassero di indovinare la password del Wi-Fi provando tutte le combinazioni possibili alla cieca.
    
- **Credere che l'identità sia legata al nome**: Sulla blockchain non esiste "Alice" o "Bob", esistono solo le [[Chiave Pubblica|Chiavi Pubbliche]]. Bitcoin è _pseudonimo_, non anonimo.
    

### Passaggi Pratici per approfondire

- **Comprendere da dove nascono i BTC**: Chi è che riceve il primo premio in denaro? Il protocollo definisce che il miner che trova la soluzione della Proof of Work ha il diritto di inserire una transazione speciale in cima al blocco (chiamata _Coinbase_) che crea nuovi Bitcoin dal nulla e li invia a se stesso. È così che l'offerta di moneta viene immessa nel sistema.
    
- **Le Transazioni (UTXO)**: Guarda i pagamenti non come un conto in banca che va su e giù, ma come banconote virtuali che si "fondono" o si "spezzano" ogni volta che le invii per generare il resto esatto.
    

---
## Collegamenti

- [[Crittografia Asimmetrica]]
- [[Doppia Spesa]]
- [[SHA-256]]
- [[Proof of Work]]
- [[Problema dei Generali Bizantini]]

# White Paper Ufficiale

![[bitcoin_it.pdf]]
