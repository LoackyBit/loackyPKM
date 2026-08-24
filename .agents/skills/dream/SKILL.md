---
name: dream
description: >
  Consolidamento autonomo della memoria dell'agente AI, ispirato a Claude Code Dreams.
  Analizza i transcript delle conversazioni passate di Antigravity CLI, estrae preferenze,
  correzioni e decisioni dell'utente, e aggiorna il file MEMORY.md persistente nel Vault.
  L'obiettivo è eliminare la necessità per l'utente di ripetere contesto ad ogni sessione.
---
# Skill: /dream (Memory Consolidation Engine)

## Scopo

Questa skill replica il comportamento di **Claude Code Dreams** per Antigravity CLI.
Il sistema opera come un ciclo di "sonno REM" per l'agente: analizza le sessioni passate,
estrae le conoscenze accumulate e le consolida in un file `MEMORY.md` persistente che
verrà letto automaticamente all'avvio di ogni nuova conversazione.

**Obiettivo finale:** L'utente non deve mai ripetere all'IA cose già dette.

---

## Architettura

### File di Memoria Persistente

```
<vault_root>/
├── .agents/
│   └── MEMORY.md          ← Indice principale della memoria (max 200 righe)
│   └── memory/
│       ├── user-profile.md     ← Chi è l'utente, background, obiettivi
│       ├── vault-conventions.md ← Regole, convenzioni, preferenze di struttura
│       ├── tech-stack.md        ← Stack tecnologico, tool e configurazioni
│       ├── active-projects.md   ← Progetti attivi e stato corrente
│       └── corrections-log.md   ← Storico delle correzioni (anti-regression)
```

### Fonte dei Dati

I transcript delle conversazioni Antigravity CLI sono in:
```
~/.gemini/antigravity-cli/brain/<conversation-id>/.system_generated/logs/transcript.jsonl
```

---

## Workflow Esecutivo — Ciclo a 4 Fasi

### Fase 1: ORIENT (Orientamento)
Leggi lo stato attuale della memoria:
1. Leggi `<vault_root>/.agents/MEMORY.md` (se esiste).
2. Leggi tutti i file in `<vault_root>/.agents/memory/*.md` (se la directory esiste).
3. Leggi `<vault_root>/GEMINI.md` per le regole di sistema del Vault.
4. Prendi nota dello stato corrente: quanti file di memoria esistono, quando è stata l'ultima consolidazione, quali aree sono coperte.

### Fase 2: GATHER SIGNAL (Raccolta Segnali)
Esegui lo script di estrazione dei segnali:
```bash
python3 scripts/dream_consolidate.py 20
```
Lo script analizza fino a 20 conversazioni recenti e produce un report JSON su stdout con:
- `corrections`: Correzioni esplicite dell'utente (es. "non usare dataview", "usa markdown puro").
- `decisions`: Decisioni architetturali e convenzioni emerse nelle sessioni.
- `recent_requests`: Le richieste recenti dell'utente per capire il contesto attivo.

### Fase 3: CONSOLIDATE (Consolidamento)
Analizza il report JSON e aggiorna i file di memoria:

**Regole di consolidamento:**
1. **Deduplicazione:** Se un'informazione è già presente in memoria, non aggiungerla di nuovo.
2. **Risoluzione Conflitti:** Se l'utente ha corretto un comportamento, aggiorna la voce esistente. La correzione più recente ha sempre priorità.
3. **Date Assolute:** Converti riferimenti relativi ("ieri", "la scorsa settimana") in date assolute.
4. **Verifica Referenze:** Non includere riferimenti a file che non esistono più nel Vault.
5. **Priorità ai Pattern:** Se l'utente ha corretto la stessa cosa 2+ volte, evidenziala come regola critica.

**Aggiornamento dei file topic:**
- `user-profile.md`: Nome, corso di studi, obiettivi, interessi.
- `vault-conventions.md`: Regole di naming, struttura cartelle, formato YAML, preferenze di output (es. "mai Dataview, solo Markdown puro").
- `tech-stack.md`: Obsidian, Python, Quartz, NotebookLM, plugin attivi, configurazioni.
- `active-projects.md`: Progetti in corso, stato, prossimi step.
- `corrections-log.md`: Log cronologico delle correzioni dell'utente con data.

### Fase 4: PRUNE & INDEX (Potatura e Indicizzazione)
Ricostruisci `MEMORY.md` come indice conciso:

**Formato di MEMORY.md:**
```markdown
# 🧠 Agent Memory — Ken Vault
> Ultima consolidazione: YYYY-MM-DD HH:MM
> Sessioni analizzate: N | Segnali estratti: N

## Profilo Utente
<!-- Sintesi da memory/user-profile.md -->

## Convenzioni del Vault
<!-- Sintesi da memory/vault-conventions.md -->

## Stack Tecnologico
<!-- Sintesi da memory/tech-stack.md -->

## Progetti Attivi
<!-- Sintesi da memory/active-projects.md -->

## ⚠️ Correzioni Critiche (Non Regredire)
<!-- Le top 10 correzioni più importanti da memory/corrections-log.md -->
```

**Vincoli:**
- `MEMORY.md` non deve superare le **200 righe**. Se lo supera, sintetizza ulteriormente.
- Ogni file topic in `memory/` non deve superare le **100 righe**.
- Usa bullet point concisi, non prosa.

---

## Trigger

### Manuale
L'utente invoca `/dream` o chiede "consolida la memoria" / "aggiorna il contesto".

### Automatico (consigliato)
Idealmente, questa skill va eseguita:
- Dopo ogni 5+ sessioni di lavoro.
- Quando l'utente nota che l'agente ha "dimenticato" qualcosa.
- Prima di iniziare un nuovo progetto complesso.

---

## Sicurezza

1. **Non distruttivo:** La memoria precedente non viene mai cancellata senza backup. Se MEMORY.md esiste già, leggilo PRIMA di sovrascriverlo.
2. **Trasparenza:** Al termine del consolidamento, mostra all'utente un riassunto delle modifiche apportate.
3. **Nessun dato sensibile:** Non memorizzare password, token, chiavi API o dati personali sensibili.
