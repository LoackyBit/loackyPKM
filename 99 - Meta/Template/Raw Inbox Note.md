<%*
// ========== CONFIGURAZIONE ==========
const INBOX_FOLDER = "03 - Inbox";
// ===================================

// Helper per annullare la creazione della nota se l'utente preme ESC
const cancelCreation = async (reason = "Creazione nota annullata") => {
    new Notice(`${reason}`);
    try {
        const file = tp.file.find_tfile(tp.file.path(true));
        if (file && (tp.file.title.startsWith("Untitled") || tp.file.title === "")) {
            await app.vault.trash(file, false);
        }
    } catch (e) {
        // Fallback silenzioso
    }
};

// 1. GESTIONE TITOLO
let title = tp.file.title;
if (title.startsWith('Untitled') || title === "") {
    const promptedTitle = await tp.system.prompt('Inserisci il Titolo della Nota Grezza (ESC per annullare): ');
    if (promptedTitle === null) {
        await cancelCreation();
        return;
    }
    title = promptedTitle.trim();
    if (!title) {
        title = "Raw Note " + tp.date.now("YYYY-MM-DD HH-mm");
    }
}

// 2. SELEZIONE TIPO DI NOTA
const options = [
    "Trascrizione YouTube",
    "Log Attività / Nota Veloce",
    "Altro (Generico)"
];
const selectedType = await tp.system.suggester(options, options, true, "Seleziona il tipo di nota grezza (ESC per annullare):");
if (!selectedType) {
    await cancelCreation();
    return;
}

let tags = ["raw"];
let typePlaceholder = "";
let videoUrl = "";
let isReady = false;
let extractFrames = false;

if (selectedType === "Trascrizione YouTube") {
    tags = ["youtube", "transcript", "raw"];
    
    // Regex per verificare link YouTube validi (watch, shorts, embed, live, youtu.be)
    const ytRegex = /^(https?:\/\/)?((www|m)\.)?(youtube\.com\/(watch\?(?:.*&)?v=|embed\/|v\/|shorts\/|live\/)|youtu\.be\/)[a-zA-Z0-9_-]{11}/i;

    // Chiede l'URL del video con controllo di validità
    let isValid = false;
    while (!isValid) {
        const inputUrl = await tp.system.prompt("Inserisci l'URL del video YouTube (opzionale - Invio per saltare, ESC per annullare):");
        if (inputUrl === null) {
            // Annullato o ESC
            await cancelCreation();
            return;
        }
        const trimmedUrl = inputUrl.trim();
        if (trimmedUrl === "") {
            // URL opzionale lasciato vuoto (premuto Invio)
            videoUrl = "";
            isValid = true;
            break;
        }

        if (ytRegex.test(trimmedUrl)) {
            videoUrl = trimmedUrl;
            isValid = true;
        } else {
            new Notice("⚠ Link non valido! Inserisci un URL YouTube valido (es. https://youtu.be/... o https://youtube.com/watch?v=...) oppure premi Invio a vuoto.");
        }
    }
    
    // Se ha inserito un URL valido, chiede opzioni di estrazione
    if (videoUrl) {
        const frameOptions = ["No (Rilevamento automatico / Euristica)", "Sì (Forza estrazione screenshot 720p)"];
        const frameChoice = await tp.system.suggester(frameOptions, [false, true], true, "Vuoi forzare l'estrazione dei frame dal video? (ESC per annullare)");
        if (frameChoice === null) {
            await cancelCreation();
            return;
        }
        if (frameChoice === true) {
            extractFrames = true;
        }

        const readyOptions = ["Sì (Elabora subito)", "No (Modifica prima la nota)"];
        const readyChoice = await tp.system.suggester(readyOptions, [true, false], true, "Vuoi contrassegnare la nota come pronta per l'IA subito? (ESC per annullare)");
        if (readyChoice === null) {
            await cancelCreation();
            return;
        }
        if (readyChoice === true) {
            isReady = true;
        }
    }
    
    typePlaceholder = `- **Video URL**: ${videoUrl}
- **Canale**: [[Nome Canale]]

---
## Testo Grezzo della Trascrizione
<!-- Incolla qui sotto il testo grezzo della trascrizione audio del video da elaborare (opzionale se hai inserito video_url) -->

`;
} else if (selectedType === "Log Attività / Nota Veloce") {
    tags = ["log", "personal", "raw"];
    typePlaceholder = `- **Data Attività**: ${tp.date.now("YYYY-MM-DD")}
- **Tipo**: [es. Configurazione, Sviluppo, Studio, ecc.]

---
## Cosa ho fatto / Azioni eseguite
<!-- Descrivi qui in modo sintetico cosa hai fatto, i comandi usati, link utili, ecc. -->

`;
} else {
    tags = ["raw"];
    typePlaceholder = `---
## Appunti Grezzi / Idee
<!-- Scrivi o incolla qui sotto i tuoi appunti grezzi -->

`;
}

let videoUrlYaml = "";
if (selectedType === "Trascrizione YouTube") {
    videoUrlYaml = `\nvideo_url: "${videoUrl}"\nchannel: ""\nextract_frames: ${extractFrames}`;
}

// Costruisci il contenuto della nota
let fileContent = `---
ready: ${isReady}
title: "${title}"
date: ${tp.date.now("YYYY-MM-DD")}
tags: [${tags.join(", ")}]
area: ""${videoUrlYaml}
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[${title}]]

# ${title}

${typePlaceholder}
`;

// Scrive il contenuto generato nel file
tR += fileContent;

// 4. SPOSTA IL FILE IN INBOX
try {
    const currentFolder = tp.file.folder();
    if (currentFolder !== INBOX_FOLDER || tp.file.title !== title) {
        await tp.file.move(`${INBOX_FOLDER}/${title}`);
        new Notice(`✓ Nota Grezza "${title}" creata in Inbox`);
    } else {
        new Notice(`✓ Nota Grezza "${title}" inizializzata in Inbox`);
    }
} catch (error) {
    new Notice(`⚠ Errore nello spostamento: ${error.message}`);
}
-%>
