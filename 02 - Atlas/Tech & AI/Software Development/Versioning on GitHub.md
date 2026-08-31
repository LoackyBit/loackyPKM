---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Versioning on Github"
date: '2025-04-03'
updated: 2026-05-22T18:26
tags: []
summary: "Il versioning è il modo in cui tieni traccia delle diverse versioni del tuo progetto, assegnando loro un identificativo (di solito un numero o un nome) per sapere cosa è cambiato e quando. Su GitHu..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Versioning on GitHub|Versioning on Github]]

Il versioning è il modo in cui tieni traccia delle diverse versioni del tuo progetto, assegnando loro un identificativo (di solito un numero o un nome) per sapere cosa è cambiato e quando. Su GitHub, questo si collega al sistema di controllo di versione Git, che registra ogni modifica al codice come un "commit". Il versioning ti aiuta a organizzare questi commit in modo che abbiano un senso, soprattutto quando condividi il tuo lavoro o collabori con altri.

### **Come si fa il versioning su GitHub?**
Su GitHub, il versioning si basa principalmente sui **tag** e sulle **release**, due strumenti che lavorano insieme a Git. Ecco come funziona passo per passo:

1. **Commit**: Ogni volta che salvi una modifica al tuo codice con `git commit`, crei un punto nella storia del progetto. Git assegna a ogni commit un ID unico, ma questi ID non sono facili da leggere per gli umani (es. `a1b2c3d4...`).

2. **Tag**: Per rendere le cose più chiare, puoi aggiungere un **tag** a un commit importante. Un tag è come un’etichetta leggibile, ad esempio `v1.0.0`. Lo crei con un comando come:
   - `git tag v1.0.0` (tag leggero).
   - O `git tag -a v1.0.0 -m "Prima versione stabile"` (tag annotato, con un messaggio).
   Poi spingi il tag su GitHub con `git push origin v1.0.0`.

3. **Semantic Versioning (SemVer)**: Molti usano un sistema standard per numerare i tag, chiamato Semantic Versioning. Funziona così:
   - **MAJOR.MINOR.PATCH** (es. `v1.2.3`).
   - **MAJOR**: cambi grossi e non compatibili (es. da `1.x.x` a `2.x.x`).
   - **MINOR**: nuove funzionalità compatibili (es. da `1.1.x` a `1.2.x`).
   - **PATCH**: correzioni o piccoli miglioramenti (es. da `1.2.2` a `1.2.3`).
   Questo dà un senso logico alle versioni e aiuta chi usa il tuo codice a capire cosa aspettarsi.

4. **Release**: Su GitHub, puoi trasformare un tag in una **release**. Vai nella sezione "Releases" del tuo repository, scegli un tag (es. `v1.0.0`), aggiungi un titolo, una descrizione (note di rilascio) e magari file aggiuntivi (es. un `.zip` del progetto). Poi pubblichi la release. Questo è utile per condividere versioni ufficiali con altri.

### **Esempio pratico**
Mettiamo che stai sviluppando un sito web:
- Finisci la prima versione funzionante e fai un commit: `git commit -m "Sito base completato"`.
- Aggiungi un tag: `git tag -a v1.0.0 -m "Versione iniziale"`.
- Spingi tutto su GitHub: `git push` e `git push origin v1.0.0`.
- Vai su GitHub, crei una release per `v1.0.0` e scrivi nelle note: "Prima versione con homepage e menu".
Ora chiunque può scaricare o vedere quella versione specifica.

Più tardi, aggiungi una nuova funzione (es. un form di contatto):
- Commit: `git commit -m "Aggiunto form di contatto"`.
- Tag: `git tag -a v1.1.0 -m "Aggiunta funzionalità form"`.
- Push e nuova release su GitHub.

### **Perché usare il versioning su GitHub?**
- **Tracciabilità**: Sai esattamente quale versione del codice corrisponde a un certo momento o funzionalità.
- **Collaborazione**: Chi lavora con te (o chi usa il tuo progetto) può scaricare una versione specifica o sapere cosa è cambiato.
- **Stabilità**: Puoi indicare quali versioni sono "stabili" (es. `v1.0.0`) rispetto a quelle in sviluppo (es. branch `dev`).
- **Ritorno indietro**: Se qualcosa va storto, puoi tornare a una versione precedente con `git checkout v1.0.0`.

### **Strumenti utili su GitHub**
- **Tags**: Li vedi nella sezione "Tags" del repository, accanto ai commit.
- **Releases**: Una pagina dedicata con tutte le versioni rilasciate, scaricabili e con note.
- **Branches**: Anche se non sono versioning in senso stretto, i branch come `main` o `release/v1.x` aiutano a separare il lavoro in corso dalle versioni stabili.

### **Trucco bonus**
Puoi automatizzare il versioning con strumenti come **GitHub Actions**. Ad esempio, configuri un flusso di lavoro che crea un tag e una release ogni volta che spingi un commit su un branch specifico. Oppure usi script per incrementare i numeri di versione automaticamente.

In breve, il versioning su GitHub ti dà controllo e chiarezza sul tuo progetto. Se vuoi un esempio più dettagliato o aiuto su un comando specifico, dimmelo pure!>)

---
## Collegamenti
