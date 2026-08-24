---
title: "Tech Stack"
date: 2026-07-17
updated: 2026-08-25T00:10
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY|Memory Index]]

# 🧠 Memory Topic: Tech Stack

## Strumenti Principali
- **Obsidian:** Gestione del grafo di note in Markdown e knowledge base locale.
- **Quartz:** Framework SSG per generare e ospitare il digital garden statico da `05 - Blog/`.
- **Python / Bash:** Motori di governance e ingestione unificati in `99 - Meta/Scripts/`:
  - `brain_health.py`: Linter AST YAML a 10 campi, link auditor intelligente, orphan detector, generatore statico di `Vault Health Dashboard.md`.
  - `brain_ingest.py`: Router di ingestione polimorfico (YouTube, web, testi, file), autolinker contestuale, lock per-sorgente, staging e tri-state GTD processor.
  - `youtube_helper.py`: Wrapper `yt-dlp`, `youtube-transcript-api` e `ffmpeg` per frame visivi in `99 - Meta/Clipboard/`.
  - `watch.sh`: Daemon per il monitoraggio in background di `03 - Inbox/Review Dashboard.md`.
- **Antigravity CLI Agent Skills:** Le 3 macro-skills consolidate in `.agents/skills/` (`brain-health`, `brain-ingest`, `brain-recall`).
