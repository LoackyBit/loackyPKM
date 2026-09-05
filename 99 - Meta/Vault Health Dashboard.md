---
status: permanent
type: moc
area: meta
related: ["[[Home MOC]]", "[[Review Dashboard]]"]
source: original
title: "Vault Health Dashboard"
date: '2026-09-05'
updated: 2026-09-05T01:27
tags: [meta/dashboard, meta/health]
summary: "Pannello di controllo statico del Second Brain: monitoraggio dello stato di salute, note in staging, bozze del blog e diagnostica del grafo."
---
[[Home MOC|Home]] / [[Meta]] / [[Vault Health Dashboard]]

# Vault Health Dashboard

Pannello di controllo in **puro Markdown statico** per monitorare la salute del Vault, le note in staging e l'integrità del grafo semantico.

*Ultimo aggiornamento:* `2026-09-05 01:27`

---

## Metriche Generali del Vault
- **Note Totali:** 145
- **Note in Staging (Inbox):** 2
- **Bozze Blog:** 3
- **Note Orfane:** 4
- **Link Interrotti:** 8
- **Forward-Links Pianificati:** 2612
- **Collisioni Omonime (Note Duplicate):** 1

---

## Note in Staging (Inbox / Bozze)
| Nota | Creazione | Area | Stato |
|---|---|---|---|
| [[Clean Code Audit Report - 2026-09-03]] | 2026-09-03 | meta | `draft` |
| [[Review Dashboard]] | 2026-08-31 | meta | `draft` |


---

## Semi del Blog (Bozze Quartz)
| Articolo | Data | Stadio | Stato |
|---|---|---|---|
| [[Crono S]] | 2026-03-25 | raw 🗂️ | `Bozza` |
| [[BlogPost - 20260303it]] | 2026-03-03 | fine-tuned 🧠 | `Bozza` |
| [[BlogPost - 20250910it]] | 2025-09-10 | fine-tuned 🧠 | `Bozza` |


---

## Note Modificate di Recente
| Nota | Ultima Modifica | Area |
|---|---|---|
| [[Senza nome]] | 2026-09-03 22:40 | N/D |
| [[test]] | 2026-09-03 22:40 | N/D |
| [[Review Dashboard]] | 2026-09-03 22:31 | meta |
| [[Clean Code Audit Report - 2026-09-03]] | 2026-09-03 13:10 | meta |
| [[Workflow Perplexity NotebookLM]] | 2026-09-01 00:21 | tech |
| [[Unfuck Your Brain]] | 2026-09-01 00:21 | tech |
| [[TIL l'Inganno Dell'Applauso Quintiliano]] | 2026-09-01 00:21 | tech |
| [[Problema P Vs NP]] | 2026-09-01 00:21 | tech |
| [[Index]] | 2026-09-01 00:21 | tech |
| [[Crono S]] | 2026-09-01 00:21 | tech |


---

## Comandi di Governance
Per eseguire un audit interattivo o applicare correzioni automatiche:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --interactive
```
