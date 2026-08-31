---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Project Setup - Antigravity AI CLI Personal Agent"
date: '2026-07-06'
updated: 2026-07-07T01:03
tags: [tech/pkm, tech/obsidian, tech/ai-agent, tech/cli, tech/software-engineering, mentality/productivity, '!/bin/bash']
summary: "Il Vault è strutturato secondo una logica modulare e semantica per facilitare la navigazione sia dell'utente che dei sotto-agenti AI:"
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Antigravity AI CLI Personal Agent|Project Setup - Antigravity AI CLI Personal Agent]]

## 1. Architettura del Vault (ACE Rivisitata)

Il Vault è strutturato secondo una logica modulare e semantica per facilitare la navigazione sia dell'utente che dei sotto-agenti AI:

1. `01 - Map of Content/` (Map of Content): Indici semantici generali e dashboard tematiche.
2. `02 - Atlas/` (Efforts integrato): Conoscenza solida strutturata (Appunti della Laurea Triennale in Ingegneria Informatica, aree di crescita personale e progetti attivi).
3. `03 - Inbox/` (Punto di ingresso): Note rapide, ritagli web da Obsidian Clipper e bozze grezze da elaborare.
4. `04 - Calendar/` (Journaling): Note giornaliere formattate come `YYYY-MM-DD.md`.
5. `05 - Blog/` (Contenuti esterni): Bozze e post pronti per essere pubblicati sul sito web.
6. `99 - Meta/` (Logica di sistema): Template, configurazioni dei modelli e la directory delle automazioni. Le skill degli agenti risiedono in `.agents/skills/`.

---

## 2. Context Engineering & Regole di Sistema

Per garantire la coerenza semantica ed evitare token di contesto sprecati o modifiche distruttive dell'AI, viene posizionato un file `CLAUDE.md` (o `GEMINI.md`) nella root del Vault.

### Configurazione di `CLAUDE.md` / `GEMINI.md`
```markdown
# Antigravity CLI Rules

## Ruolo
Sei l'agente del Second Brain di uno studente di Ingegneria Informatica. Esperto in programmazione, crescita personale e blogging tecnico.

## Convenzioni di Scrittura
- Usa unicamente link interni nativi di Obsidian: `[[Nome Nota]]`.
- Ogni nuova nota creata in `02 - Atlas` o `05 - Blog` deve avere un frontmatter YAML valido (`title`, `date`, `tags`, `status: review`).
- Mantieni un tono tecnico e accademico per gli argomenti di Ingegneria, integrando snippet di codice puliti.

## Vincoli di Sicurezza
- **MAI** modificare o cancellare note esistenti senza una conferma interattiva dell'utente.
- Esegui o suggerisci comandi Git prima di elaborazioni in batch.
````

## 3. Registro delle Agent Skills (Comandi Personalizzati)

Ogni funzionalità avanzata viene implementata tramite lo standard delle **Agent Skills** (directory dedicate in `.agents/skills/` contenenti un file `SKILL.md` di istruzioni ed eventuali script Python/Bash di supporto).

### `/nota` (Già implementato)

- **Scopo:** Crea una nota standardizzata basata sull'argomento fornito in input, rispettando lo stile dell'utente.
    

### `/dream` (Sintesi e Connessioni Laterali)

- **Logica Bash:** `find "02 - Atlas/" -name "*.md" | shuf -n 3`
    
- **Istruzioni AI:** Analizza le 3 note estratte casualmente. Trova un'intersezione concettuale non ovvia. Genera un report creativo intitolato `Dream - [Argomento].md` salvandolo in `03 - Inbox`.
    

### `/link` (Interconnessione Semantica Automatica)

- **Logica Bash:** Utilizza `grep` / `ripgrep` sul Vault per mappare le corrispondenze testuali.
    
- **Istruzioni AI:** Scansiona il testo di una nota specifica; identifica parole chiave che corrispondono a titoli di note esistenti in _Atlas_ e sostituiscile con i wiki-links `[[Nome Nota]]`.
    

### `/meta` (Linting Frontmatter e Manutenzione Database)

- **Istruzioni AI:** Verifica i metadati delle note in una directory. Se lo YAML è assente o incompleto, deduci i tag dal testo, imposta la data odierna e assegna lo stato `review`.
    

### `/process-inbox` (Workflow GTD Autonomo)

- **Istruzioni AI:** Scansiona ciclicamente `03 - Inbox/`. Identifica la natura dei file e proponi all'utente lo spostamento deterministico tramite comandi `mv` verso _Atlas_, _Calendar_ o _Blog_.
    

## 4. Infrastruttura di Scripting e Automazioni Fondamentali

La gestione avanzata prevede l'interazione diretta con il sistema operativo per attivare i processi in background senza appesantire l'interfaccia grafica di Obsidian.

### Automazione 1: Inbox Watcher (`fswatch` su macOS/Linux)

Uno script daemon monitora la cartella di input e attiva la modalità headless dell'agente appena viene aggiunto un file da mobile o da web-clipper.

Bash

```
# Da salvare in 99 - Meta/scripts/watch_inbox.sh
fswatch -o "$HOME/Vault/03 - Inbox" | xargs -n1 -I{} claude -p "Esegui la skill process-inbox"
```

### Automazione 2: Version Control e Sicurezza (Git Hooks)

Prima di consentire all'agente l'esecuzione di comandi batch distruttivi su file markdown, il sistema si assicura della presenza di un commit pulito nel repository locale.

Bash

```
# Workflow consigliato nel prompt di sistema:
1. git status --porcelain
2. Se ci sono modifiche non salvate: git add . && git commit -m "Backup prima di operazione AI"
3. Esecuzione Skill (es. /link o /meta)
4. Ripristino in caso di allucinazione: git reset --hard HEAD
```

### Sviluppi Futuri (Integrazione MCP)

- Implementazione di un server **Obsidian Local REST API MCP** per consentire query ancora più veloci sui tag e i grafi di Obsidian.
    
- Connessione MCP con le API di pubblicazione del Blog (es. Git hook per Hugo/Astro o API REST WordPress) per automatizzare il comando `/publish [nome-nota].md`.

---
## Collegamenti
