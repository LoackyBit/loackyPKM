---
title: "Vault Conventions"
date: 2026-07-17
updated: 2026-08-25T00:10
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY|Memory Index]]

# 🧠 Memory Topic: Vault Conventions

## Naming Conventions
- I file devono seguire la convenzione **Title Case** con spazi (es. `Nome della Nota.md`).
- Rimuovere emoji e caratteri speciali non standard dai nomi dei file per compatibilità Quartz e Obsidian.
- Il campo `title` nel frontmatter YAML deve essere sincronizzato 1:1 con il nome del file.

## Struttura delle Directory (Topologia ACE a 6 Cartelle)
- `01 - Map of Content/`: Indici semantici generali e nodi di aggregazione (`type: moc`).
- `02 - Atlas/`: Conoscenza consolidata, corsi universitari, guide tecniche, saggi (`status: permanent`).
- `03 - Inbox/`: Punto di atterraggio per bozze e note da elaborare (`status: draft`) con `Review Dashboard.md`.
- `04 - Calendar/`: Journaling e tracciamento temporale quotidiano (`DailyNote - YYYYMMDD.md`).
- `05 - Blog/`: Articoli pronti o in lavorazione per la pubblicazione web con Quartz.
- `99 - Meta/`: Template, configurazioni, script di automazione e `Vault Health Dashboard.md`.

## Convenzioni del Frontmatter YAML (10 Campi Canonici)
- Sequenza canonica: `status` (o `stage`+`draft`) → `type` → `area` → `related` → `aliases` → `source` → `title` → `date` → `updated` → `tags` → `summary`.
- Array compatti in flow-style: `related: ["[[Nota 1]]"]`, `tags: [tech/ai, ...]`.
- Summary conciso a doppi apici (120-180 caratteri, max 200).

## Elaborazione Note & Staging GTD
- **Staging Protetto:** Ogni nota generata atterra in `03 - Inbox/` con `status: draft` ed è registrata in `03 - Inbox/Review Dashboard.md`.
- **Tri-State Lifecycle:** `[ ]` In attesa di revisione, `[x]` Approvata (promossa ad Atlas/Blog), `[-]` Rifiutata (eliminata).
- **Evidenziazioni HTML (Style Guide):** `<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>cardine</b></font></mark>` e `<mark style="background:rgba(181, 113, 255, 0.36)"><font color="#9a54c1"><b>secondario</b></font></mark>` senza backtick.
- **Supporti Visivi:** Inserire schemi Mermaid (con label quotate) o tabelle comparative Markdown per facilitare la comprensione.
