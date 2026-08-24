---
stage: learning 🧩
draft: false
type: article
area: tech
related: []
source: original
title: "Blog su Quartz"
date: '2026-03-02'
updated: 2026-07-12T21:34
tags: [tech/quartz, tech/migrazione, tech/obsidian, tech/github-actions, tech/digital-garden]
summary: "Oggi ho rifatto quasi tutto il setup del blog, passando da una logica Astro a una pipeline Quartz molto piu automatizzata e orientata a Obsidian."
---
[[Home MOC|Home]] / [[Blog]] / [[Blog su Quartz]]

## Cosa ho cambiato

Oggi ho rifatto quasi tutto il setup del blog, passando da una logica Astro a una pipeline Quartz molto piu automatizzata e orientata a Obsidian.  

Le modifiche principali che ho introdotto sono queste:

- ho aggiunto un workflow GitHub Actions dedicato al deploy su GitHub Pages (`.github/workflows/deploy.yml`), agganciato al branch `v4`
- ho integrato il fetch del tema remoto `ayu-light-mirage` in fase di build
- ho iterato piu volte su `quartz.config.ts` fino a stabilizzare `baseUrl` su `"/quartz"`
- ho costruito uno script Node per sincronizzare il vault Obsidian in `content/`
- ho aggiunto script npm per coprire casi d'uso diversi: sync una tantum, watch continuo, serve locale, push automatico
- ho riscritto il `README.md` come guida operativa del mio flusso reale
- ho fatto vari passaggi su `content` (directory, symlink, riallineamenti) per trovare la strategia piu robusta
- ho rimosso file temporanei di test come `content/sda.md`
## Timeline delle decisioni

La timeline non e stata lineare: ho fatto diversi tentativi prima di arrivare al setup attuale.

1. Ho introdotto deploy e contenuti iniziali su Quartz.
2. Ho corretto piu volte il `baseUrl` per allinearlo al comportamento di GitHub Pages.
3. Ho provato ad aggiungere/rimuovere/reinserire lo step di fetch tema nel workflow CI.
4. Ho sperimentato sia `content/` locale sia symlink verso il vault per valutare pro e contro.
5. Ho consolidato lo script `obsidian-sync.mjs` come punto unico di orchestrazione.
6. Ho attivato la modalita di auto-commit e auto-push dei soli contenuti.
7. Ho documentato tutto nel README con modalita operative chiare.
## CLI che ho creato

La parte piu importante del refactor e stata creare una piccola CLI operativa centrata su `scripts/obsidian-sync.mjs`.

Obiettivi della CLI:

- ridurre attrito tra scrittura in Obsidian e pubblicazione su Quartz
- avere una sola entrypoint per sync, watch, preview e deploy
- standardizzare i comandi per evitare errori manuali

Interfaccia del CLI `qsync`:

```text
Usage:
	qsync [command]

Commands:
	once               Run one sync and exit (default)
	watch              Watch Obsidian folder and sync on changes
	serve              Watch and start Quartz local server
	deploy             Watch, commit, and push synced content
	serve-deploy       Watch + server + auto commit/push
	install-agent      Install macOS LaunchAgent supervisor
	uninstall-agent    Uninstall macOS LaunchAgent supervisor
	-h, --help         Show this help message
```

Per usarlo in locale posso eseguirlo direttamente oppure tramite npm script.

Come funziona internamente:

- usa `rsync -a --delete` per avere mirror coerente tra vault e `content/`
- esclude cartelle/file non utili (`.obsidian`, `.trash`, `.DS_Store`, `.git`)
- usa `chokidar` per intercettare modifiche filesystem con debounce
- gestisce concorrenza (`isSyncRunning`, `pendingSync`) per evitare race condition
- in modalita `--push` fa `git add/commit/push` solo su `content/`
- in modalita `--serve` avvia `npx quartz build --serve`

Esempio di uso diretto dello script:

```bash

node ./scripts/obsidian-sync.mjs watch --serve --push

```
## Cose imparate

Durante la migrazione ho visto alcuni punti critici ricorrenti:

- `baseUrl` errato rompe facilmente asset e routing in Pages
- alternare directory e symlink su `content` crea diff rumorosi e storicita difficile da leggere
- auto-push senza controllo puo generare molti commit ravvicinati
- senza una versione Node fissata, il comportamento locale non e ripetibile
- ignorare `scripts/` nel `.gitignore` puo diventare un rischio se la repo deve essere replicabile
## Stato finale

Adesso il flusso e davvero "Obsidian-first":  

- scrivo nel vault Obsidian
- sincronizzo automaticamente su Quartz
- faccio preview locale quando serve
- pubblico con pipeline GitHub Actions senza passaggi manuali ripetitivi
---
## Collegamenti

- [[Quartz]]
- [[Obsidian Sync]]
- [[GitHub Actions Deploy]]
- [[Digital Garden Workflow]]
