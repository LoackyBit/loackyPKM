## Gerarchia evidenziatori (FONDAMENTALE)

- `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>parola</b></font></mark>` — parole chiave ASSOLUTE, concetti-cardine, tesi critiche fondamentali

- `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>parola</b></font></mark>` — parole importanti COLLEGATE alle gialle (nomi propri, luoghi, concetti secondari), o di minor importanza rispetto alle gialle. Le parole viola sono di solito più frequenti rispetto alle gialle, perché le gialle racchiudono tante di quelle viola

- Non abusare dei colori: le evidenziazioni gialle devono restare più rare e marcate, quelle viola più frequenti ma sempre mirate. Per capire ‘quanto’ colore usare, guarda la frequenza delle evidenziazioni presenti in [[Gabriele d'Annunzio]] e [[Giovanni Pascoli]] (le due note create da me, originali)

- **Regola Critica HTML**: applica il codice html così com'è, sostituendo 'parola'. **Mai racchiudere i tag `<mark>` o `<font>` tra backtick markdown.**

- **grassetto normale** senza html — enfasi generica su parole o frasi rilevanti

## Anatomia delle Note e Tipografia

- **Titoli e Intestazioni (H1, H2, H3)**: DIVIETO ASSOLUTO DI EMOJI nei titoli. I titoli devono contenere solo testo pulito (es. `# Titolo Nota`, `## Sintesi Esecutiva`, `## Quadro Concettuale`). Mai inserire emoji decorative come `# 🎯`, `## 🔑`, `## 🏛️`.
- **Collegamenti Interni (Wiki-links)**: Incorporati organicamente nel flusso della prosa (es. `[[Target Note]]`, max 2 menzioni per nota target).
- **Divieto Sezione Collegamenti**: Non inserire mai una sezione finale separata come `## Collegamenti`, `## Note Correlate` o `## Vedi anche`. I collegamenti sono tessuti nel testo e sincronizzati nel frontmatter YAML (`related: [...]`).
- **Diagrammi Mermaid**: Tutti i nodi con spazi o caratteri speciali devono avere etichette tra virgolette (es. `A["Nodo Principale (dettaglio)"]`). Mai inserire tag HTML all'interno dei nodi Mermaid.
- **Divieto Assoluto di Diagrammi Simbolici ASCII/Unicode**: Non inserire MAI blocchi di codice monospazio o testo contenenti schemi con caratteri box-drawing (`┌┐└┘`, `│`, `─`, `──►`). Questo tipo di grafica si de-sincronizza e risulta illeggibile su dispositivi mobile, iPad e temi con font a spaziatura proporzionale. Se esistono slide visive, transcludi direttamente i render PNG ad alta risoluzione (`![[Schema - ... .png]]`); altrimenti struttura le informazioni mediante tabelle Markdown standard reattive e callout semantici.
- **Fonti Didattiche e Citazioni Slide (`\[[[...#page=N|Slide N]]]`):** Citare e collegare come fonti attive e nel frontmatter unicamente materiali di studio ad alto valore accademico (slide PDF ufficiali d'aula, paper scientifici, libri di testo, articoli autorevoli). DIVIETO ASSOLUTO di citare o inserire le trascrizioni audio grezze nel corpo del testo o nel frontmatter. Per le slide PDF, utilizzare sempre la sintassi con escape della prima quadra `\[[[NomeFile.pdf#page=N|Slide N]]]`. Mantenere una densità equilibrata e strategica (a livello di macro-sezione o per chiarire passaggi sintetici/astratti ed evitare fraintendimenti), evitando la saturazione frase per frase.
- **Formule Matematiche (LaTeX)**: Usa la sintassi standard LaTeX inline (`$E = mc^2$`) o in blocco (`$$\int_a^b f(x)dx$$`).
- **Direttive Inline per l'IA (`%% AI: ... %%`)**: Per comunicare direttamente con l'IA rielaboratrice negli appunti grezzi, usa la sintassi ufficiale di commento `%% AI: <istruzione> %%` (inseribile rapidamente con il template snippet `[[AI Instruction]]`). In alternativa sono ammessi commenti HTML `<!-- AI: <istruzione> -->` o callout `> [!note]- AI: <istruzione>`. L'IA esegue tali istruzioni come prioritarie e le rimuove categoricamente dal corpo finale della nota permanente. Mai usare parentesi quadre inverse `]...[` (che rompono il syntax highlighting dei link in Obsidian).

## Formattazione e Callouts

- Corsivo (_titolo_) per titoli di opere

- Callouts:
	- es:
	  ```
	  >[!quote] Autore
	  >citazione
	  ```
	- note  
	- abstract, summary, tldr  
	- info  
	- todo  
	- tip, hint, important  
	- success, check, done  
	- question, help, faq  
	- warning, caution, attention  
	- failure, fail, missing  
	- danger, error  
	- bug  
	- example  
	- quote, cite

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
