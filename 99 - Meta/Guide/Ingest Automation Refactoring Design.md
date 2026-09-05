# 🛠️ Ingest Automation Refactoring Design

Questo documento definisce il design dell'architettura e dei flussi di lavoro per il rifacimento dell'automazione di ingestione del Second Brain. L'obiettivo principale è separare le responsabilità meccaniche (gestite via script deterministici Python) da quelle semantiche (gestite dall'agente LLM), ottimizzando le performance e garantendo feedback in tempo reale in Obsidian.

---

## 1. Riepilogo della Comprensione

* **Scopo**: Automatizzare l'elaborazione delle note grezze catturate nell'Inbox e gestire le approvazioni/rifiuti dell'utente in modo rapido e affidabile.
* **Componenti**:
  * Un watcher in background (`watch.sh`).
  * Un orchestratore deterministico in Python (`ingest_manager.py`).
  * Un helper ottimizzato per YouTube (`youtube_helper.py`).
  * L'agente AI (`agy`) delegato esclusivamente alla generazione del testo rielaborato.
* **Funzioni chiave**:
  * Aggiornamento dello stato dell'elaborazione in tempo reale su `Review Dashboard.md`.
  * Interruzione attiva (kill) dei sottoprocessi se il file originale viene eliminato dall'Inbox.
  * Spostamenti e cancellazioni deterministiche a prova di errori.

---

## 2. Assunzioni e Vincoli

* **Sistema Operativo**: macOS con `ffmpeg`, `yt-dlp` e l'agente `agy` nel PATH di sistema.
* **Ottimizzazione ffmpeg**: L'estrazione dei frame deve usare un seek rapido prima del caricamento dell'input (`-ss` prima di `-i`) per garantire l'esecuzione in meno di un secondo per frame.
* **Estendibilità**: Esclusa da questo ciclo di rifacimento. Si mantengono i template e le tipologie di note attuali.

---

## 3. Registro delle Decisioni (Decision Log)

| Decisione | Alternative Considerate | Perché è stata scelta questa opzione |
| :--- | :--- | :--- |
| **Orchestratore in Python** | Mantenere la logica in `ingest.sh` (Bash). | Python offre maggiore robustezza per la gestione di thread, sottoprocessi e manipolazione di file Markdown complessi, riducendo a zero il rischio di sovrascritture casuali. |
| **Kill Attivo dei Processi** | Controllo passivo sequenziale solo all'avvio. | Terminare attivamente i processi asincroni se il file originale scompare dal disco risparmia risorse CPU e previene sprechi di token API LLM. |
| **Stato in Obsidian Dashboard** | Notifiche macOS o log a terminale. | Mostrare il caricamento direttamente all'interno di `Review Dashboard.md` garantisce una visualizzazione integrata e nativa nell'interfaccia di Obsidian. |
| **Ottimizzazione ffmpeg** | Mantenere l'estrazione intelligente del "miglior frame". | La cattura immediata a frame singolo con seek posizionato all'inizio è incredibilmente più veloce e performante rispetto a elaborare 8 secondi di flusso ad alta definizione. |

---

## 4. Design Dettagliato della Soluzione

### 4.1. Architettura dei File
I file coinvolti nel sistema sono:
* `99 - Meta/Scripts/watch.sh`: Watcher ad attivazione rapida (ogni 5 secondi). Rileva i file pronti ed esegue `ingest_manager.py`.
* `99 - Meta/Scripts/ingest_manager.py` (Nuovo): Script orchestratore in Python.
* `99 - Meta/Scripts/youtube_helper.py`: Script di estrazione trascrizioni e frame, ottimizzato per le prestazioni.
* `03 - Inbox/Review Dashboard.md`: Dashboard di stato e approvazione per l'utente.

### 4.2. Flusso di Elaborazione Sequenziale e Kill Attivo
Per ogni nota rilevata con `ready: true`:
1. Viene inserita una riga in `Review Dashboard.md` sotto `## ⏳ In Elaborazione`:
   `- ⏳ [[Nome Nota]] (Elaborazione in corso...)`
2. L'orchestratore avvia un thread di elaborazione e un thread parallelo di monitoraggio.
3. Il thread di monitoraggio verifica ogni 500ms l'esistenza di `03 - Inbox/Nome Nota.md`. Se il file scompare:
   * Chiama `terminate()` e poi `kill()` sul sottoprocesso attivo.
   * Rimuove la riga dalla dashboard e pulisce eventuali residui temporanei.
4. Una volta completata la trascrizione e l'estrazione frame, l'orchestratore invoca `agy` limitatamente a questa nota:
   ```bash
   agy --model gemini-3.8-flash-low --dangerously-skip-permissions --print "Elabora solo la nota 'Nome Nota' usando i template specifici..."
   ```
5. A completamento avvenuto, l'orchestratore:
   * Rinominare il file originario in `raw-Nome Nota.md`.
   * Salva la proposta in `proposed-Nome Nota.md`.
   * Rimuove la nota da `## ⏳ In Elaborazione` e la sposta sotto `## 📋 Note in Attesa di Approvazione`.
