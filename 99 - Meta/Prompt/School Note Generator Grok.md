---
status: permanent
type: concept
area: tech
related: []
source: original
title: "School Note Generator Grok"
date: '2025-10-23'
updated: 2026-05-24T21:56
tags: []
summary: "Sono uno studente di scuola superiore che deve creare appunti scolastici organizzati per un corso di letteratura italiana, da utilizzare nel mio vault scolastico su Obsidian. Il mio obiettivo è cap..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[School Note Generator Grok]]

```
Sono uno studente di scuola superiore che deve creare appunti scolastici organizzati per un corso di letteratura italiana, da utilizzare nel mio vault scolastico su Obsidian. Il mio obiettivo è **capire tutto perfettamente anche fra 6 mesi**, quindi gli appunti devono essere **chiari, completi, ben strutturati**, ma **non troppo sintetici né schematici in modo rigido**.

Il tuo compito è generare una nota scolastica **completa e ben organizzata** in formato markdown sull'argomento specificato: '[ARGOMENTO]', utilizzando i documenti allegati ('SC Pentecoste.md', 'SC Alessandro Manzoni.md', 'Cornell (Template).md', 'AI Lecture (Template).md') come base stilistica. I documenti allegati rappresentano il mio stile di scrittura e i template che uso nel vault Obsidian. Segui queste linee guida:

1. **Input e flessibilità**:
   - Usa i documenti allegati come riferimento per contenuto e stile.
   - Se l’argomento non è coperto o le informazioni sono scarse, **integra con spiegazioni chiare e complete** da fonti affidabili, aggiungendo contesto storico, letterario o culturale **in modo strutturato ma fluido**, senza contraddire il mio stile.
   - Se vengono fornite pagine di un libro o altri materiali, usali come fonte primaria.
   - Considera che alcune note (es. [[Sc Pentecoste]], [[SC Cinque Maggio]]) sono collegate a una principale (es. [[Sc Alessandro Manzoni]]), quindi **usa link interni con prefisso `SC`** per indicare note esistenti o da creare.

2. **Struttura della nota**:
   - **Titolo**: `# SC [Argomento]` (es. `# SC Pentecoste`)
   - **Contenuto**: Organizza in sezioni logiche con sottotitoli chiari (es. `## Contesto`, `## Struttura`, `## Stile`). **Usa uno stile schematico ma leggibile**:
     - **Paragrafi brevi** per le spiegazioni principali.
     - **Elenchi puntati o numerati** per punti chiari (es. struttura, temi).
     - **Tabelle** se utili per confronto o sintesi.
     - **Frasi complete**, **niente frasi spezzate**.
   - **Sezioni obbligatorie**:
     - **Introduzione**: contesto chiaro con link interni (es. `[[Sc Alessandro Manzoni]]`).
     - **Analisi**: struttura, temi, stile, simboli – spiegati in paragrafi o elenchi.
     - **Parole chiave**: in `[!done] Parole Chiave`.
     - **Sintesi**: in `[!summary]` con punti chiari.
     - **Domande**: in `[!question] Questions` (3-5 domande aperte).
   - **Collegamenti tematici**: spiega i legami con altre opere (es. `[[SC Odi Civili]]`) in modo chiaro e strutturato.

3. **Stile e formato**:
   - Scrivi in italiano, con linguaggio **formale ma accessibile**, adatto a uno studente di scuola superiore.
   - **Stile schematico ma non rigido**: usa **paragrafi**, **elenchi**, **tabelle**, **spaziature** per facilitare la lettura. **Niente muri di testo, niente frasi incomplete**.
   - Usa link interni con prefisso `SC` per ogni argomento principale o correlato.
   - Usa la sintassi markdown di Obsidian: blocchi `[!done]`, `[!summary]`, `[!question]`, elenchi, tabelle.

4. **Esportazione per Obsidian**:
   - Output: file markdown **pronto per copia-incolla**.
   - Usa struttura del template 'Cornell (Template).md' per argomenti generali, 'AI Lecture (Template).md' per AI.
   - **Non includere frontmatter, `Up`, `Related`**: li aggiungerò io.
   - Usa prefisso `SC` per **tutti i link interni** e il **nome file**: `Appunti_SC_[Argomento].md`.
   - Niente script Templater, solo markdown pulito.

5. **Integrazione e creatività**:
   - Se i documenti sono incompleti, **aggiungi spiegazioni chiare e strutturate**, non solo dati.
   - Non generare immagini/grafici se non richiesti.
   - Fonti esterne: cita in `[!cite]` alla fine.

6. **Output**:
   - File: `Appunti_SC_[Argomento].md`
   - **Solo il testo della nota**, niente spiegazioni esterne.
   - Se manca l’argomento, chiedimelo.

Evidenzia in grassetto le parole importanti, cioè quelle che rendono il testo più chiaro, coinvolgente e facilmente comprensibile. Non evidenziare le parole chiave nel senso tecnico del termine: il grassetto deve servire a guidare la lettura, non a marcare concetti personali o interpretativi.
```

```
Sono uno studente di scuola superiore che deve creare appunti scolastici organizzati per **qualsiasi materia**, da utilizzare nel mio vault scolastico su Obsidian. Il mio obiettivo è **capire tutto perfettamente anche fra 6 mesi**, quindi gli appunti devono essere **chiari, completi, ben strutturati**, ma **non troppo sintetici né schematici in modo rigido**.
Il tuo compito è generare una nota scolastica **completa e ben organizzata** in formato markdown sull'argomento specificato: '[ARGOMENTO]', utilizzando **SOLO i documenti allegati come ispirazione stilistica** ('SC Pentecoste.md', 'SC Alessandro Manzoni.md', 'Cornell (Template).md', 'AI Lecture (Template).md').
**IMPORTANTE**: *I contenuti su Manzoni sono solo esempi di stile (sezioni, blocchi, elenchi, link [[SC ...]]). **Non collegare mai l'argomento richiesto a Manzoni, alla letteratura italiana o ai suoi temi, a meno che l'argomento stesso non lo richieda esplicitamente.***
Segui queste linee guida:
1. **Input e flessibilità**:
   - Usa i documenti allegati **solo per lo stile**: struttura, blocchi, elenchi, tabelle, link `[[SC ...]]`, tono.
   - **Contenuti**: se l'argomento è coperto nei file allegati, estrai e riorganizza. Altrimenti, **ricostruisci da zero** con informazioni accurate da fonti affidabili (libri, web, manuali scolastici).
   - Se vengono fornite pagine di un libro o altri materiali, usali come fonte primaria.
   - **Link interni**: usa `[[SC Nome]]` **solo per argomenti che esistono o devono esistere nel vault** (es. [[SC Fotosintesi]], [[SC Seconda Guerra Mondiale]]). **Non creare mai link a Manzoni o opere letterarie se non pertinenti**.
2. **Struttura della nota**:
   - **Titolo**: `# SC [Argomento]` (es. `# SC Fotosintesi`)
   - **Contenuto**: Organizza in sezioni logiche con sottotitoli chiari (es. `## Contesto`, `## Processo`, `## Importanza`). **Stile schematico ma leggibile**:
     - **Paragrafi brevi** per spiegazioni.
     - **Elenchi puntati/numerati** per punti chiave.
     - **Tabelle** per confronti o sintesi.
     - **Frasi complete**, niente spezzate.
   - **Sezioni obbligatorie**:
     - **Introduzione**: contesto chiaro con link pertinenti.
     - **Analisi**: spiegata in modo strutturato.
     - **Parole chiave**: in `[!done] Parole Chiave`.
     - **Sintesi**: in `[!summary]` con punti chiari.
     - **Domande**: in `[!question] Questions` (3-5 domande aperte).
   - **Collegamenti tematici**: **solo se pertinenti** (es. in biologia: [[SC Respirazione cellulare]]).
3. **Stile e formato**:
   - Scrivi in italiano, linguaggio **formale ma accessibile**.
   - **Stile schematico ma fluido**: paragrafi, elenchi, tabelle, spaziature. **Niente muri di testo**.
   - Evidenzia in grassetto le parole importanti, cioè quelle che rendono il testo più chiaro, coinvolgente e facilmente comprensibile. Non evidenziare le parole chiave nel senso tecnico del termine: il grassetto deve servire a guidare la lettura, non a marcare concetti personali o interpretativi.
   - Usa link `[[SC ...]]` **solo per argomenti scolastici rilevanti**.
   - Usa blocchi `[!done]`, `[!summary]`, `[!question]`.
4. **Esportazione per Obsidian**:
   - Output: markdown **pronto per copia-incolla**.
   - Usa struttura del template **'Cornell (Template).md'** per argomenti generali, **'AI Lecture (Template).md'** per intelligenza artificiale.
   - **Non includere frontmatter, `Up`, `Related`**.
   - Usa prefisso `SC` per **tutti i link interni** e il **nome file**: `Appunti_SC_[Argomento].md`.
   - Solo markdown pulito.
5. **Integrazione e creatività**:
   - Se i documenti non coprono l'argomento, **crea da zero** con contenuto scolastico corretto.
   - Non generare immagini/grafici.
   - Fonti esterne: cita in `[!cite]`.
6. **Output**:
   - File: `Appunti_SC_[Argomento].md`
   - **Solo il testo della nota**, niente spiegazioni.
   - Se manca l’argomento, chiedimelo.
```

---
## Collegamenti
