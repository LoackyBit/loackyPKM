---
name: tidy
description: Standardizzatore e linter automatico del Vault. Pulisce la Naming Convention, valida e arricchisce lo YAML frontmatter, struttura la navigazione interna delle note e smista i file da Inbox.
---
# Skill: /tidy (Vault Knowledge Architect)

Questa skill definisce le regole deterministiche per garantire l'ordine entropico, la leggibilità semantica e l'integrità strutturale del Second Brain. Viene eseguita autonomamente per correggere, strutturare e ricollocare le note.

## 1. Naming Convention (Standardizzazione File)

Per garantire la massima leggibilità in Obsidian (file explorer e wiki-links) e prevenire errori nei server web statici (come Quartz):

*   **Formato:** **Title Case con spazi puliti** (es. `Evoluzione dell'Agente AI.md` o `Calcolo Differenziale.md`).
*   **Regole di pulizia (Sanitizzazione nomi file):**
    *   *Emoji:* Rimuovere qualsiasi emoji iniziale o interna (es. `📊 Analisi` -> `Analisi`).
    *   *Caratteri Speciali:* Rimuovere simboli speciali come `+`, `?`, `!`, parentesi tonde `()` o quadre `[]` (es. `Learning to Learn (ITA)` -> `Learning to Learn ITA`).
    *   *Accenti:* Convertire caratteri accentati in versioni non accentate o con apostrofo regolare a seconda dei casi (es. `Perche` invece di `Perché` o `Perche'`).
    *   *Apostrofi:* Convertire tutti gli apostrofi tipografici curvi (`’`) nel carattere apostrofo standard dritto (`'`).

---

## 2. Standard YAML Frontmatter

Ogni nota del Vault (ad eccezione delle note giornaliere in `04 - Calendar/`) deve iniziare con un frontmatter YAML standardizzato.

### A. Note in `Atlas` (Knowledge Base)
```yaml
---
title: "Titolo Nota Pulito"
date: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM
tags: [macro-area, sotto-tag]
status: permanent           # draft | in-progress | permanent | reference
macro_area: university      # university | school | mentality | finance | tech | meta
---
```
*   **Significato degli Stati (`status`):**
    *   `draft` / `in-progress`: Note incomplete o in fase di stesura/rielaborazione.
    *   `permanent`: Note concettuali attive, sintesi teoriche e appunti di studio generati su tuo scheletro. Rappresentano la conoscenza assimilata nel Second Brain.
    *   `reference`: Note contenenti materiale di consultazione passivo, cheat sheet, specifiche API, trascrizioni grezze o elenchi di risorse esterne.
*   **Macro-Aree Obbligatorie (`macro_area`):**
    *   `university`: Corsi, esami e appunti della Laurea Triennale in Ingegneria Informatica.
    *   `school`: Appunti e lezioni ereditati dalle scuole superiori.
    *   `mentality`: Crescita personale, psicologia, routine, autodisciplina e mindset.
    *   `finance`: Economia, investimenti, criptovalute, finanza personale.
    *   `tech`: Guide a tool AI, programmazione generica, prompt engineering, sistemi e CLI.
    *   `meta`: Note e guide di gestione del Vault o configurazioni degli agenti.

### B. Note in `Blog` (Quartz)
```yaml
---
title: "Titolo Articolo"
date: YYYY-MM-DD
tags:
  - tag1
  - tag2
stage: fine-tuned 🧠       # seed 🌱 (bozza iniziale) | growing 🌿 (strutturato) | fine-tuned 🧠 (pronto)
source:
  - "link-sorgente"
summary: "Breve descrizione della nota per scopi SEO e anteprima"
draft: false
---
```

---

## 3. Struttura e Layout della Nota (Navigazione)

Per non interrompere il flusso visivo del testo ma consentire una navigazione semantica efficace:

1.  **Header (Inizio Nota):**
    Immediatamente sotto lo YAML frontmatter, inserire un indicatore gerarchico di percorso (*Breadcrumbs*) ultra-compatto su una sola riga:
    `[[00 - Map of Content|Home]] / [[Materia o Area|Nome Area]] / [[Nota Padre (opzionale)|Nota Padre]]`
    *Esempio per Calcolo Differenziale:* `[[00 - Map of Content|Home]] / [[Matematica V]] / [[Calcolo Differenziale]]`
2.  **Footer (Fine Nota):**
    Separato da un divisore orizzontale `---`, aggiungere una sezione standardizzata per i link orizzontali/associativi non gerarchici:
    ```markdown
    ---
    ## Collegamenti
    - [[Nota Correlata 1]]
    - [[Nota Correlata 2]]
    ```

---

## 4. Logica di Smistamento (GTD Engine)

La skill riordina e smista i file da `Inbox/` alle cartelle definitive secondo queste regole:

*   **`04 - Calendar/`:** File denominati con il pattern di data `YYYY-MM-DD.md` o che contengono log di tracciamento temporale quotidiano.
*   **`Blog/`:** File con YAML contenente `draft: false` o che mostrano la struttura tipica di un articolo divulgativo completo per Quartz.
*   **`Atlas/Corsi/`:** Appunti universitari legati alla Laurea Triennale in Ingegneria Informatica o corsi scientifici (es. R, Python, Intelligenza Artificiale).
*   **`Atlas/Mentality/`:** Note e sintesi su crescita personale, psicologia, motivazione, riassunti video/libri (es. David Goggins, Dopamine Detox).
*   **`Atlas/Finance/`:** Guide, analisi o appunti su mercati, investimenti, criptovalute ed economia.
*   **`Atlas/Tecnology/` o `Prompt/`:** Guide, cheat sheet di programmazione, flussi di lavoro AI, prompt engineering.
*   **`Inbox/School/`:** Appunti storici delle scuole superiori in fase di catalogazione temporanea per anno accademico (es. `2025-26`).
