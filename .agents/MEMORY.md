---
title: "MEMORY"
date: 2026-07-17
updated: 2026-08-25T00:10
tags: [meta, memory, index]
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[AI Second Brain System|AI System]] / [[MEMORY]]

# 🧠 Agent Memory — Ken Vault

> Ultima consolidazione: `2026-08-25 00:10`
> Struttura: 3 Macro-Skills consolidate (`brain-health`, `brain-ingest`, `brain-recall`)
> Questa memoria viene letta automaticamente all'avvio delle nuove sessioni per mantenere la continuità e allineare il contesto.

---

## 👤 Profilo Utente
*Dettagli completi in [[User Profile]].*
- **Utente:** Lorenzo, studente di Ingegneria Informatica.
- **Obiettivo:** Co-pilotare l'organizzazione automatica del Second Brain e lo studio accademico.

## 📋 Convenzioni Critiche (Non Regredire)
*Dettagli completi in [[Corrections Log]].*
- **[STRICT]** **Niente Dataview:** La dashboard e le visualizzazioni aggregate devono usare **puro Markdown statico**.
- **[STRICT]** **Blog Stages:** I tag di `stage` in `05 - Blog` (es. `seed 🌱`, `growing 🌿`) non devono essere normalizzati o alterati.
- **[STRICT]** **Naming Title Case:** Non usare mai trattini (kebab-case) o snake_case nei nomi dei file nel vault. Utilizzare sempre il **Title Case intelligente** con spazi, mantenendo articoli, congiunzioni e preposizioni in minuscolo (es. `Nome della Nota.md`).
- **[STRICT]** **3 Macro-Skills Unificate:** Le sole skills operative risiedono in `.agents/skills/brain-health/`, `.agents/skills/brain-ingest/`, e `.agents/skills/brain-recall/`.
- **[STRICT]** **No Convenzioni GitHub/Sviluppo:** In questo vault, ignorare totalmente le convenzioni globali di sviluppo software (es. naming dei branch 'type/scope/desc', conventional commits per note, kebab-case per file o cartelle). Seguire solo le regole del Vault.
- **[STRICT]** **Scrittura Obbligatoria su Disco:** Quando si elaborano note o proposte, l'agente deve **SEMPRE eseguire la scrittura effettiva sul file system usando lo strumento `write_to_file`**, e non limitarsi mai a mostrare il testo generato solo nella chat.
- **[STRICT]** **Zero Allucinazioni in Recall:** Se una query non ha corrispondenze nel Vault, dichiarare esplicitamente l'assenza senza inventare contenuti.
- **[STRICT]** **Evidenziazioni Senza Backtick:** Mai racchiudere tag HTML `<mark>` tra backtick markdown.

## ⚙️ Convenzioni del Vault
*Dettagli completi in [[Vault Conventions]].*
- Naming in **Title Case** senza emoji per compatibilità con l'hosting web Quartz.
- Organizzazione in 6 cartelle principali (struttura ACE modificata).
- Frontmatter YAML standard a 10 campi.
- Ingestione sempre in staging (`03 - Inbox/`) con revisione GTD in `Review Dashboard.md`.

## 🛠️ Stack Tecnologico
*Dettagli completi in [[Tech Stack]].*
- Obsidian + Quartz + Python Linting (`brain_health.py`, `brain_ingest.py`) + NotebookLM Retrieval (`brain-recall`).

## 📂 Progetti Attivi
*Dettagli completi in [[Active Projects]].*
- **AI Second Brain System:** Consolidamento 3 macro-flussi completato (Fase 3); predisposizione motore retrieval Fase 4.
- **Laurea Triennale Ing. Informatica:** Appunti e sintesi dei corsi accademici.
- **Blog Quartz:** Pubblicazione articoli tecnici.
- **PKM AI System Open Source:** Preparazione per la pubblicazione su GitHub del sistema per la community.

---
## Collegamenti
- [[Home MOC]]
- [[AI Second Brain System]]
- [[Vault Health Dashboard]]
