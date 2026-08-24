---
name: meta
description: Frontmatter Linter per verificare, correggere e standardizzare i metadati YAML secondo lo schema a 10 campi del Vault.
---
# Skill: /meta (Frontmatter Linter)

Questa skill garantisce che ogni nota rispetti rigorosamente la sequenza canonica a 10 campi dello standard Vault:
`status` (o `stage` + `draft`) → `type` → `area` → `related` → `aliases` → `source` → `title` → `date` → `updated` → `tags` → `summary`.

## Schema Canonico

| Posizione | Chiave | Tipo / Valori | Descrizione |
|---|---|---|---|
| 1 | `status` / `stage`+`draft` | `draft \| in-progress \| permanent \| reference` (o `seed 🌱 \| growing 🌿 \| fine-tuned 🧠` + `boolean`) | Stato del ciclo di vita della nota |
| 2 | `type` | `concept \| video \| article \| lecture \| book \| project \| moc \| journal` | Tipologia semantica della nota |
| 3 | `area` | `tech \| education \| mentality \| finance \| projects \| meta \| calendar` | Dominio di appartenenza |
| 4 | `related` | `["[[Nota 1]]", "[[Nota 2]]"]` (Flow-style) | Wikilinks correlati quotati |
| 5 | `aliases` | `["Alias 1"]` (Flow-style, opzionale) | Redirect interni per Obsidian |
| 6 | `source` | `URL` / `citazione` / `"original"` | Origine della nota |
| 7 | `title` | Stringa doppi apici | Titolo 1:1 in Title Case con il nome file |
| 8 | `date` | `YYYY-MM-DD` | Timestamp di creazione |
| 9 | `updated` | `YYYY-MM-DDTHH:MM` | Timestamp ultima modifica |
| 10 | `tags` | `[area/topic, ...]` (Flow-style) | Tassonomia gerarchica |
| 11 | `summary` | Stringa doppi apici | Sintesi esecutiva (120-180 caratteri, max 200) |

## Utilizzo CLI

```bash
# Preview non distruttiva (dry-run)
python3 .agents/skills/meta/scripts/lint_yaml.py --dry-run .

# Normalizzazione su disco (scrittura atomica)
python3 .agents/skills/meta/scripts/lint_yaml.py --execute .

# Linting con forzatura tipo o area
python3 .agents/skills/meta/scripts/lint_yaml.py --execute "02 - Atlas/Technology" --area tech --type concept

# Backfill batch dei summary con modello AI e checkpointing
python3 "99 - Meta/Scripts/backfill_summaries.py" --execute .
```

## Regole di Validazione
1. **Preservazione Markdown:** Giunzione esatta con singola riga vuota tra chiusura `---`, breadcrumb e corpo del testo.
2. **Nessun Tag nel Corpo:** Gli hashtag isolati nel corpo del testo vengono rimossi e consolidati in `tags: [...]`.
3. **Array Compatti:** `tags`, `related` e `aliases` devono sempre usare la sintassi flow-style su singola riga `[...]`.
