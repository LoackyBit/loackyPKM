<%*
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
    const promptedTitle = await tp.system.prompt('Inserisci il Titolo della Nota (ESC per annullare): ');
    if (promptedTitle === null) {
        await cancelCreation();
        return;
    }
    title = promptedTitle.trim();
    if (!title) {
        title = "Nota " + tp.date.now("YYYY-MM-DD HH-mm");
    }
}

// 2. COSTRUZIONE CONTENUTO CANONICO VAULT
let fileContent = `---
status: permanent
type: concept
area: tech
related: []
aliases: []
source: original
title: "${title}"
date: ${tp.date.now("YYYY-MM-DD")}
updated: ${tp.date.now("YYYY-MM-DDTHH:mm")}
tags: [tech]
summary: "Sintesi concettuale esecutiva della nota per retrieval sub-secondo."
---
[[Home MOC|Home]] / [[02 - Atlas|Atlas]] / [[${title}]]

# ${title}

## Sintesi Esecutiva
<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>${title}</b></font></mark>: 

## Quadro Concettuale

`;

tR += fileContent;

// 3. SPOSTAMENTO IN ATLAS
try {
    const targetFolder = "02 - Atlas";
    if (tp.file.folder() !== targetFolder) {
        await tp.file.move(`${targetFolder}/${title}`);
        new Notice(`✓ Nota "${title}" creata in Atlas`);
    }
} catch (error) {
    new Notice(`⚠ Spostamento: ${error.message}`);
}
-%>
