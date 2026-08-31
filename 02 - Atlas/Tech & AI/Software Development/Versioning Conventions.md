---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Versioning Conventions"
date: '2025-03-06'
updated: 2026-05-22T18:26
tags: []
summary: "In italiano, quando si parla di \"convenzioni nel scrivere versioni di un progetto\", ci si riferisce solitamente alle pratiche standardizzate per identificare e numerare le versioni di un documento,..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Versioning Conventions]]

In italiano, quando si parla di "convenzioni nel scrivere versioni di un progetto", ci si riferisce solitamente alle pratiche standardizzate per identificare e numerare le versioni di un documento, software o altro tipo di progetto. Queste convenzioni sono utili per mantenere ordine, tracciare i progressi e comunicare chiaramente le modifiche. Ecco alcune linee guida comuni:

### 1. **Sistema di numerazione delle versioni (Versioning)**
   - **Formato numerico**: Una delle convenzioni più diffuse è l'uso del sistema "Major.Minor.Patch" (es. 1.0.0):
     - **Major** (es. 1.x.x): Incrementa per cambiamenti significativi o radicali nel progetto (es. una nuova edizione o una revisione completa).
     - **Minor** (es. x.1.x): Incrementa per aggiornamenti minori o aggiunte di funzionalità senza stravolgere la struttura.
     - **Patch** (es. x.x.1): Incrementa per correzioni di bug o piccoli miglioramenti senza nuove funzionalità.
   - Esempio: Un software passa da 1.0.0 a 1.1.0 con l’aggiunta di una funzione, poi a 1.1.1 per una correzione.

   - **Versioni preliminari**: Per bozze o versioni non definitive, si possono usare suffissi come:
     - "Alpha" (es. 1.0.0-alpha): Versione iniziale, instabile, in fase di test interno.
     - "Beta" (es. 1.0.0-beta): Versione più stabile, ma ancora in fase di test pubblico.
     - "Draft" o "Bozza" (es. Draft 0.1): Per documenti o progetti non software.

### 2. **Convenzioni per i nomi dei file**
   - Includi sempre la versione nel nome del file per evitare confusione. Esempi:
     - `Progetto_v1.0.pdf`
     - `Manuale_2.1.3.docx`
     - `Software_1.0.0-beta.zip`
   - Usa un formato consistente: ad esempio, separa il nome del progetto dalla versione con un trattino basso (`_`) o un trattino (`-`).
   - Evita spazi o caratteri speciali per compatibilità con diversi sistemi.

### 3. **Datazione (opzionale)**
   - Puoi includere la data nel nome del file o nella documentazione per maggiore chiarezza, soprattutto per progetti che si evolvono nel tempo:
     - Formato consigliato: `YYYYMMDD` (es. `Progetto_v1.0_20250306.pdf`).
     - Questo aiuta a identificare rapidamente l’ultima versione in ordine cronologico.

### 4. **Note di versione (Changelog)**
   - Accompagna ogni versione con un documento o una sezione che descrive:
     - Cosa è cambiato rispetto alla versione precedente.
     - Data di rilascio.
     - Eventuali autori o contributori.
   - Esempio:
     ```
     Versione 1.1.0 (06/03/2025)
     - Aggiunta funzionalità X
     - Migliorata interfaccia Y
     - Corretto bug Z
     ```

### 5. **Contesto specifico**
   - **Documenti**: Per manuali o report, si usa spesso "Revisione" o "Rev" (es. Rev 1, Rev 2).
   - **Software**: Segue il sistema Major.Minor.Patch o il "Semantic Versioning" (semver.org).
   - **Progetti creativi**: A volte si usano nomi simbolici (es. "Versione Luna", "Versione Sole") combinati con numeri.

Se hai un contesto specifico in mente (es. software, documenti tecnici, design), fammi sapere e posso adattare la risposta! Vuoi un esempio pratico per un tipo di progetto particolare?

---
## Collegamenti
