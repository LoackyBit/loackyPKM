---
name: brain-health
description: Vault health governance, 10-field YAML linting, Title Case normalization, smart forward/broken link audit, and static Health Dashboard generation.
---
# Skill: /brain-health (Vault Health & Governance)

Governance unificata, manutenzione qualitativa del grafo e conformità strutturale del Vault Obsidian.
Sostituisce e consolida le precedenti micro-skills `audit`, `meta` e `tidy`.

---

## 🎯 Obiettivi e Responsabilità

1. **Linting YAML Frontmatter Canonico a 10 Campi:**
   Garantisce la sequenza standard: `status` (o `stage` + `draft`) → `type` → `area` → `related` → `aliases` → `source` → `title` → `date` → `updated` → `tags` → `summary`.
2. **Audit Intelligente dei Link e Note Orfane:**
   - `[VALID-LINK]`: Target esistente nel grafo.
   - `[FORWARD-LINK]`: Link verso note concettuali pianificate (in Title Case) "da creare"; vengono preservate e mai cancellate.
   - `[BROKEN-LINK]`: Percorsi errati, URL malformati o errori di battitura.
   - `[ORPHAN-NOTE]`: Note in `02 - Atlas/` senza alcun backlink entrante e non censite in alcuna MOC di `01 - Map of Content/`.
3. **Normalizzazione Naming & Title Case:**
   Conversione e verifica di tutti i file in Title Case intelligente con spazi (nessun kebab-case, snake_case o emoji nei nomi file).
4. **Generazione Dashboard Statica:**
   Rigenerazione idempotente di `99 - Meta/Vault Health Dashboard.md` in puro Markdown statico (zero dipendenze Dataview).

---

## 🛠️ Modalità Operative & CLI

Il motore Python sottostante è `99 - Meta/Scripts/brain_health.py`.

### 1. Audit Interattivo Passo-Passo (Default)
Mostra la diagnostica e richiede conferma interattiva per ogni gruppo di correzioni:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --interactive
```

### 2. Ispezione Non Distruttiva (Dry-Run)
Scansiona il Vault e stampa il report completo senza modificare alcun file su disco:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --dry-run
```

### 3. Correzione Automatica Deterministica
Applica le correzioni sicure (formattazione YAML canonica, breadcrumb, rimozione hashtag isolati dal corpo) e aggiorna la dashboard:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --auto-fix
```

### 4. Aggiornamento Esclusivo della Dashboard
Ricalcola le metriche del grafo e aggiorna `99 - Meta/Vault Health Dashboard.md`:
```bash
python3 "99 - Meta/Scripts/brain_health.py" --dashboard-only
```

### 5. Controlli Mirati (Audit o Linting Singoli)
```bash
# Solo diagnostica link e orfani
python3 "99 - Meta/Scripts/brain_health.py" --audit-only

# Solo validazione frontmatter YAML
python3 "99 - Meta/Scripts/brain_health.py" --lint-only
```

---

## 📐 Schema Frontmatter Canonico (10 Campi)

| # | Chiave | Tipo / Valori Ammessi | Descrizione |
|---|---|---|---|
| 1 | `status` / `stage`+`draft` | `draft \| in-progress \| permanent \| reference` (Atlas) / `seed 🌱 \| growing 🌿 \| fine-tuned 🧠` + `boolean` (Blog) | Ciclo di vita della nota |
| 2 | `type` | `concept \| video \| article \| lecture \| book \| project \| moc \| journal` | Tipologia semantica |
| 3 | `area` | `tech \| education \| mentality \| finance \| projects \| meta \| calendar` | Dominio principale |
| 4 | `related` | `["[[Nota 1]]", "[[Nota 2]]"]` (Flow-style) | Wiki-links correlati quotati |
| 5 | `aliases` | `["Alias 1"]` (Flow-style, opzionale) | Alias per Obsidian |
| 6 | `source` | `URL` / `citazione` / `"original"` | Origine della risorsa |
| 7 | `title` | Stringa doppi apici | Titolo sincronizzato 1:1 con il nome file |
| 8 | `date` | `YYYY-MM-DD` | Data creazione |
| 9 | `updated` | `YYYY-MM-DDTHH:MM` | Data ultima modifica |
| 10 | `tags` | `[area/sotto-tag, ...]` (Flow-style) | Tassonomia gerarchica |
| 11 | `summary` | Stringa doppi apici | Sintesi concettuale esecutiva (120-180 caratteri, max 200) |

---

## 🔒 Regole di Preservazione e Sicurezza

- **Forward-Links:** Non eliminare o segnalare come errore fatale i link concettuali verso note future non ancora create.
- **Nessun Tag nel Corpo:** Gli hashtag isolati (`#tag`) nel corpo Markdown vengono estratti e consolidati in `tags: [...]` nel frontmatter.
- **Giunzione Markdown:** Esattamente una riga vuota tra la chiusura del frontmatter `---`, la riga Breadcrumb (`[[Home MOC|Home]] / ...`) e l'inizio del testo.
- **Zero Dataview:** Tutte le dashboard diagnostiche devono rimanere in puro Markdown statico per totale compatibilità con Quartz e mobile.
