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
- **Formule Matematiche (LaTeX)**: Usa la sintassi standard LaTeX inline (`$E = mc^2$`) o in blocco (`$$\int_a^b f(x)dx$$`).

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
