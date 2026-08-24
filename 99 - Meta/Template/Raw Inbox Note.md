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
    "🎥 Trascrizione YouTube",
    "💻 Log Attività / Nota Veloce",
    "📝 Altro (Generico)"
];
const selectedType = await tp.system.suggester(options, options, true, "Seleziona il tipo di nota grezza:");

let tags = ["raw"];
let typePlaceholder = "";
let visualIcon = "📝";
let noteType = "concept";
let noteSource = "original";

if (selectedType === "🎥 Trascrizione YouTube") {
    tags = ["tech/video", "tech/transcript", "raw"];
    visualIcon = "🎥";
    noteType = "video";
    
    // Chiede l'URL del video
    let videoUrl = await tp.system.prompt("Inserisci l'URL del video YouTube (opzionale):") || "";
    if (videoUrl) {
        noteSource = videoUrl;
    }
    
    typePlaceholder = `- **Data Trascrizione**: ${tp.date.now("YYYY-MM-DD")}

---
## 📝 Testo Grezzo della Trascrizione
<!-- Incolla qui sotto il testo grezzo della trascrizione audio del video da elaborare -->

`;
} else if (selectedType === "💻 Log Attività / Nota Veloce") {
    tags = ["tech/log", "raw"];
    visualIcon = "💻";
    noteType = "project";
    typePlaceholder = `- **Data Attività**: ${tp.date.now("YYYY-MM-DD")}
- **Tipo**: [es. Configurazione, Sviluppo, Studio, ecc.]

---
## 🛠️ Cosa ho fatto / Azioni eseguite
<!-- Descrivi qui in modo sintetico cosa hai fatto, i comandi usati, link utili, ecc. -->

`;
} else {
    tags = ["raw"];
    visualIcon = "📝";
    noteType = "concept";
    typePlaceholder = `---
## 📝 Appunti Grezzi / Idee
<!-- Scrivi o incolla qui sotto i tuoi appunti grezzi -->

`;
}

// Costruisci il contenuto della nota con schema canonico
let fileContent = `---
status: draft
type: ${noteType}
area: tech
related: []
aliases: []
source: ${noteSource}
title: "${title}"
date: ${tp.date.now("YYYY-MM-DD")}
updated: ${tp.date.now("YYYY-MM-DDTHH:mm")}
tags: [${tags.join(", ")}]
summary: "Bozza grezza in attesa di elaborazione GTD."
---
[[Home MOC|Home]] / [[03 - Inbox|Inbox]] / [[${title}]]

# ${visualIcon} ${title}

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

---
## Collegamenti
