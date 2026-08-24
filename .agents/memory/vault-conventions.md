---
title: "Vault Conventions"
date: 2026-07-17
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY|Memory Index]]

# 🧠 Memory Topic: Vault Conventions

## Naming Conventions
- I file devono seguire la convenzione **Title Case** (es. `Nome Della Nota.md`).
- Rimuovere emoji e caratteri speciali non standard dai nomi dei file per compatibilità Quartz.

## Struttura delle Directory (ACE Modificato)
- `01 - Map of Content/`: Indici semantici generali (MOC).
- `02 - Atlas/`: Conoscenza consolidata (Corsi, Mentality, Finance, Tecnology, Prompt).
- `03 - Inbox/`: Punto di atterraggio per bozze e note da elaborare.
- `04 - Calendar/`: Journaling e tracciamento temporale.
- `05 - Blog/`: Articoli pronti o in lavorazione per la pubblicazione web.
- `99 - Meta/`: Template e script di configurazione.

## Convenzioni del Frontmatter YAML
- Campi obbligatori Atlas/Scuola: `title`, `date`, `updated`, `tags`, `status`, `macro_area`.
- Campi obbligatori Blog: `title`, `date`, `tags`, `stage`, `summary`, `draft`.
- **Idempotenza:** Ripulire i backslash accumulati nei doppi apici (es. `\"` -> `"`) prima di salvare lo YAML.

## Elaborazione Note & Contenuti Raw
- **Utilizzo Template:** In fase di rielaborazione di contenuti raw e bozze in `03 - Inbox`, applicare in modo appropriato uno dei template disponibili in `99 - Meta/Template/` a seconda del tipo di contenuto.
- **Supporti Visivi:** Inserire immagini, schemi e grafi (es. diagrammi Mermaid) per facilitare la comprensione, evitando però di sovraccaricare le note inutilmente.
