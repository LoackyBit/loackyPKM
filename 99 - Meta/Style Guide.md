## Gerarchia evidenziatori (FONDAMENTALE)

- `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>parola</b></font></mark>` — parole chiave ASSOLUTE, concetti-cardine, tesi critiche fondamentali.
- `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>parola</b></font></mark>` — parole importanti COLLEGATE alle gialle (nomi propri, luoghi, concetti secondari), o di minor importanza rispetto alle gialle. Le parole viola sono di solito più frequenti rispetto alle gialle, perché le gialle racchiudono tante di quelle viola.
- **Budget di Parsimonia Estrema per l'AI (Anti-Cecità da Evidenziatore)**:
  - Per preservare la leggibilità in *Live Preview* ed evitare l'esplosione visiva di tag HTML lunghi al passaggio del cursore, l'AI deve applicare **al massimo 1 evidenziazione gialla (`#cc8800`) per sotto-sezione (il singolo concetto cardine)** e **massimo 2-3 evidenziazioni viola (`#9a54c1`) per sotto-sezione**.
  - Tutto il resto del testo deve rimanere pulito, impiegando il normale `**grassetto**` e `*corsivo*` Markdown per lasciare spazio all'evidenziazione manuale dello studente durante le sessioni di studio attivo.
  - Per comprendere la parsimonia e l'equilibrio cromatico, fare riferimento alla densità di [[Gabriele d'Annunzio]] e [[Giovanni Pascoli]].
- **Stile Schematico e Telegrafico (Architettura a Scheletro Esecutivo)**:
  - Sostituire i muri di prosa accademica prolissa con **elenchi puntati o numerati telegrafici, densi e schematici** (ispirati a [[Gabriele d'Annunzio]]).
  - Limitare la prosa continua a massimo 3-4 righe di introduzione contestuale per sezione; sviluppare proprietà, analisi ed esempi tramite elenchi schematici con trattini (`—`) o sotto-bullet compatti.
- **Regola Critica HTML**: applica il codice html così com'è, sostituendo 'parola'. **Mai racchiudere i tag `<mark>` o `<font>` tra backtick markdown (`<mark...>` ❌).**
- **grassetto normale** senza html — enfasi generica su parole o frasi rilevanti.

## Anatomia delle Note e Tipografia

- **Titoli e Intestazioni (H1, H2, H3)**: DIVIETO ASSOLUTO DI EMOJI nei titoli. I titoli devono contenere solo testo pulito (es. `# Titolo Nota`, `## Sintesi Esecutiva`, `## Quadro Concettuale`). Mai inserire emoji decorative come `# 🎯`, `## 🔑`, `## 🏛️`.
- **Collegamenti Interni (Wiki-links)**: Incorporati organicamente nel flusso della prosa (es. `[[Target Note]]`, max 2 menzioni per nota target).
- **Divieto Sezione Collegamenti**: Non inserire mai una sezione finale separata come `## Collegamenti`, `## Note Correlate` o `## Vedi anche`. I collegamenti sono tessuti nel testo e sincronizzati nel frontmatter YAML (`related: [...]`).
- **Teoremi e Dimostrazioni (Pattern Dual-Layer & Progressive Disclosure)**:
  - Per teoremi, lemmi e proposizioni, separare l'intuizione concettuale dai passaggi algebrici:
    1. **Livello 1 (Visibile nel flusso o nel callout del teorema)**: enunciato formale sintetico, formula centrale `$$...$$` e **Idea chiave / Strategia della dimostrazione** in massimo 2-3 bullet sintetici che spiegano il *perché* logico funziona.
    2. **Livello 2 (Progressive Disclosure)**: tutti i passaggi algebrici estesi e i calcoli dettagliati sono racchiusi in un **callout collassato di default**:
       `> [!abstract]- Dimostrazione Formale Passo-Passo`
       (con tutte le righe interne prefissate da `> ` affinché rimanga realmente chiuso in Obsidian).
  - **Eliminazione dei 5 Sotto-Bullet Fissi**: non imporre la griglia rigida dei 5 punti (Ipotesi, Condizioni, Simboli con SI, Esempio) a ogni proposizione matematica elementare. Includere `Significato dei simboli (con unità SI)` e `Condizioni di validità` **solo** per formule fisiche, ingegneristiche o multivariate non auto-evidenti.
- **Diagrammi Mermaid**: Tutti i nodi con spazi o caratteri speciali devono avere etichette tra virgolette (es. `A["Nodo Principale (dettaglio)"]`). Mai inserire tag HTML all'interno dei nodi Mermaid. Diagrammi discrezionali, da riservare a flussi complessi.
- **Divieto Assoluto di Diagrammi Simbolici ASCII/Unicode**: Non inserire MAI blocchi di codice monospazio o testo contenenti schemi con caratteri box-drawing (`┌┐└┘`, `│`, `─`, `──►`). Questo tipo di grafica si de-sincronizza e risulta illeggibile su dispositivi mobile, iPad e temi con font a spaziatura proporzionale. Se esistono slide visive, transcludi direttamente i render PNG ad alta risoluzione (`![[Schema - ... .png]]`); altrimenti struttura le informazioni mediante tabelle Markdown standard reattive e callout semantici.
- **Fonti Didattiche e Citazioni Slide (`\[[[...#page=N|Slide N]]]`):** Citare e collegare come fonti attive e nel frontmatter unicamente materiali di studio ad alto valore accademico (slide PDF ufficiali d'aula, paper scientifici, libri di testo, articoli autorevoli). DIVIETO ASSOLUTO di citare o inserire le trascrizioni audio grezze nel corpo del testo o nel frontmatter. Per le slide PDF, utilizzare sempre la sintassi con escape della prima quadra `\[[[NomeFile.pdf#page=N|Slide N]]]`. Mantenere una densità equilibrata e strategica (a livello di macro-sezione o per chiarire passaggi sintetici/astratti ed evitare fraintendimenti), evitando la saturazione frase per frase.
- **Formule Matematiche (LaTeX)**: Usa la sintassi standard LaTeX inline (`$E = mc^2$`) o in blocco (`$$\int_a^b f(x)dx$$`).
- **Direttive Inline per l'IA (`%% AI: ... %%`) e Risoluzione Dubbi**: Per comunicare direttamente con l'IA rielaboratrice negli appunti grezzi, usa la sintassi ufficiale di commento `%% AI: <istruzione> %%` (inseribile rapidamente con il template snippet `[[AI Instruction]]`). In alternativa sono ammessi commenti HTML `<!-- AI: <istruzione> -->` o callout `> [!note]- AI: <istruzione>`. Se l'utente esprime un dubbio (es. `%% AI: non ho capito... %%`), l'IA risponde puntualmente all'interno di un callout dedicato `> [!question] Chiarimento sul tuo dubbio` posizionato nel punto esatto del testo, rimuovendo il commento originale. Le direttive operative vengono eseguite come prioritarie e pulite dalla nota finale. Mai usare parentesi quadre inverse `]...[`.

## Formattazione e Callouts

- Corsivo (_titolo_) per titoli di opere

- Callouts Generali e Tassonomia Scientifica/Universitaria:
	- Sintassi base:
	  ```markdown
	  > [!danger] Definizione / Teorema / Assioma: Titolo
	  > Corpo del callout con enunciato formale.
	  ```
	- **Tassonomia Rigorosa Note Scientifiche e Accademiche:**
	  - `> [!danger]` : **Assiomi, Teoremi, Definizioni e Corollari** formali.
	  - `> [!summary]` : **Proposizioni, Proprietà e Criteri** matematici.
	  - `> [!example]` : **Esempi, Casi di Studio e Controesempi**.
	  - `> [!info]` : **Osservazioni, Note a margine, Intuizioni geometriche/analitiche**.
	  - `> [!tip]- Flashcard: [Concetto]` : **Flashcard Anki** inline e contestuali (collassate di default).
	  - `> [!abstract]- Dimostrazione Formale Passo-Passo` : **Dimostrazioni estese** (Pattern Dual-Layer).
	  - `> [!question] Chiarimento sul tuo dubbio` : **Risoluzione dubbi utente** sollevati inline (`%% AI: ... %%`).
	  - `> [!warning]` : **Avvertenze critiche, errori concettuali frequenti e regole di distinzione**.
	  - `> [!quote]-` : **Citazioni d'autore e divagazioni didattiche del docente**.
	- Altri tipi Obsidian supportati: `note`, `todo`, `success`, `failure`, `bug`.

- Checkbox (Tri-State Review & Tasking):
	- | Syntax  | Description |
	  | --- | --- |
	  | `- [ ]` | To-do / Pending Ingestion |
	  | `- [/]` | Incomplete  |
	  | `- [x]` | Done / Approved Ingestion |
	  | `- [-]` | Canceled / Rejected Draft |
	  | `- [>]` | Forwarded   |
	  | `- [<]` | Scheduling  |
	  | `- [?]` | Question    |
	  | `- [!]` | Important   |
	  | `- [*]` | Star        |
	  | `- ["]` | Quote       |
	  | `- [l]` | Location    |
	  | `- [b]` | Bookmark    |
	  | `- [i]` | Information |
	  | `- [S]` | Savings     |
	  | `- [I]` | Idea        |
	  | `- [p]` | Pros        |
	  | `- [c]` | Cons        |
	  | `- [f]` | Fire        |
	  | `- [k]` | Key         |
	  | `- [w]` | Win         |
	  | `- [u]` | Up          |
	  | `- [d]` | Down        |
	  | `- [+]` | Add         |
	  | `- [B]` | Brainstorm  |
	  | `- [a]` | Alarm       |
	  | `- [n]` | Note        |
	  | `- [R]` | Review      |
	  | `- [t]` | Time        |
	  | `- [P]` | Phone       |
	  | `- [L]` | Love        |

- Tabelle: usa sempre il formato **Markdown standard** (no HTML) per garantire la corretta visualizzazione in Obsidian.
