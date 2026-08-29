<%*
// 1. GESTIONE TITOLO
let title = tp.file.title;
if (title.startsWith('Untitled') || title === "") {
    title = await tp.system.prompt('Inserisci il Titolo della Nota: ');
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
