<%*
// ========== CONFIGURAZIONE ==========
const INBOX_FOLDER = "03 - Inbox";
// ===================================

// 1. GESTIONE TITOLO
let title = tp.file.title;
if (title.startsWith('Untitled') || title === "") {
    title = await tp.system.prompt('Inserisci il Titolo della Nota Grezza: ');
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
const selectedType = await tp.system.suggester(options, options, true, "Seleziona il tipo di nota grezza:");

let tags = ["raw"];
let typePlaceholder = "";
let videoUrl = "";
let isReady = false;

if (selectedType === "Trascrizione YouTube") {
    tags = ["youtube", "transcript", "raw"];
    
    // Chiede l'URL del video
    videoUrl = await tp.system.prompt("Inserisci l'URL del video YouTube (opzionale):") || "";
    
    // Se ha inserito un URL, chiede se vuole elaborarlo subito
    if (videoUrl) {
        const readyOptions = ["Sì (Elabora subito)", "No (Modifica prima la nota)"];
        const readyChoice = await tp.system.suggester(readyOptions, [true, false], true, "Vuoi contrassegnare la nota come pronta per l'IA subito?");
        if (readyChoice === true) {
            isReady = true;
        }
    }
    
    typePlaceholder = `- **Data Trascrizione**: ${tp.date.now("YYYY-MM-DD")}

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
    videoUrlYaml = `\nvideo_url: "${videoUrl}"\nchannel: ""`;
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
