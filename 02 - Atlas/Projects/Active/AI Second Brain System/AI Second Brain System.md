---
status: permanent
type: project
area: meta
related: []
source: original
title: "AI Second Brain System"
date: '2026-07-12'
updated: 2026-07-12T22:51
tags: [meta/meta, tech/obsidian, meta/agents, meta/system-design]
summary: "Questa nota descrive la struttura tecnica, le metodologie integrate e i comandi operativi che orchestrano il funzionamento automatico del Vault. Il sistema fonde le metodologie Second Brain (CODE),..."
---
[[Home MOC|Home]] / [[Projects]] / [[AI Second Brain System]]

## L'Architettura dell'AI Second Brain

Questa nota descrive la struttura tecnica, le metodologie integrate e i comandi operativi che orchestrano il funzionamento automatico del Vault. Il sistema fonde le metodologie **Second Brain (CODE)**, **ACE**, **LYT (MOC)** e **GTD** in un motore automatizzato tramite **Agentic Skills**.

---

## 1. Organizzazione del Vault (ACE Modificato)

Il Vault è strutturato su 6 directory principali:
1. `01 - Map of Content/` — Mappe di orientamento semantico (MOC) che collegano le note senza gerarchie rigide.
2. `02 - Atlas/` — La base di conoscenza consolidata divisa per macroaree (`Corsi`, `Mentality`, `Finance`, `Tecnology`, `Prompt`, `Education`).
3. `03 - Inbox/` — Punto d'ingresso per note grezze da elaborare (GTD Landing Zone).
4. `04 - Calendar/` — Registro storico giornaliero e journaling temporale.
5. `05 - Blog/` — Studio di scrittura ed esportazione degli articoli per il web statico (Quartz).
6. `99 - Meta/` — Logica di automazione, template di sistema e guide operative.

---

## 2. Il Motore delle Agent Skills (`.agents/skills/`)

Il comportamento dell'AI all'interno del Vault è esteso tramite lo standard aperto delle **Agentic Skills**. Ogni skill è una procedura memorizzata formata da istruzioni strutturate (`SKILL.md`) ed eventuali script eseguibili (`scripts/`):

### `/tidy` (Vault Knowledge Architect)
Standardizza l'integrità strutturale del Vault.
- **Naming Convention:** Rinomina i file in Title Case, rimuove emoji, accenti e caratteri speciali incompatibili con Quartz.
- **YAML Frontmatter:** Forza la compilazione dei metadati minimi a seconda del percorso della nota.
- **Navigazione:** Integra breadcrumbs in testa e collegamenti correlati in coda.

### `/process-inbox` (GTD Engine)
Orchestra lo svuotamento automatico di `03 - Inbox/`.
- Scansiona l'Inbox per note pendenti usando `inbox_scanner.sh`.
- Esegue l'analisi semantica per ricollocare la nota nella cartella e macroarea corretta (es. `Corsi`, `Mentality`, `Finance`).
- Passa lo status della nota da `draft` a `permanent` o `in-progress`.

### `/link` (Contextual Auto-linking)
Espande il grafo bi-direzionale del Vault.
- Mappa l'elenco completo dei titoli di tutte le note esistenti tramite `get_vault_titles.sh`.
- Analizza il corpo del testo della nota target e converte parole chiave o sinonimi di note esistenti in wiki-links `[[Nome Nota]]` seguendo il principio di parsimonia.

### `/dream` (Autonomic Discovery)
Stimola la serendipità e il pensiero laterale cross-disciplinare.
- Estrae 3 note casuali da `02 - Atlas` usando `discover.sh`.
- Chiede all'AI di trovare una connessione non ovvia e di proporre un'applicazione pratica di sintesi (es. collegare concetti di Algoritmi a routine di Crescita Personale).
- Genera un report di sintesi salvato in `03 - Inbox/`.

### `/nota` & `crea-nota` (NotebookLM Integration)
Genera note di studio complete a partire da registrazioni, slide e testi universitari.
- Interroga il database di NotebookLM tramite server MCP.
- Estrae con massima priorità le spiegazioni, gli esempi e le note del professore.
- Compila note estese in lingua italiana strutturate a paragrafi (almeno 18-20k caratteri) con sintassi di evidenziazione colorata dei concetti cardine.

---

## 3. Script di Automazione Attivi

Gli script eseguibili risiedono in `.agents/skills/<nome-skill>/scripts/` e in `99 - Meta/Scripts/`:
- **`tidy_vault.py`:** Lo standardizzatore Python generale del Vault. Eseguibile con `python3 tidy_vault.py --execute` per correggere nomi file, YAML e breadcrumbs.
- **`discover.sh`:** Raccoglie note casuali in Atlas.
- **`get_vault_titles.sh`:** Estrae tutti i titoli validi del Vault.
- **`inbox_scanner.sh`:** Monitora l'Inbox.
- **`lint_yaml.py`:** Effettua la validazione sintattica dello YAML frontmatter.

---
## Collegamenti
- [[Home]]
- [[Tech & AI]]
