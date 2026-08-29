<%*
// 1. GESTIONE TITOLO
let title = tp.file.title;
if (title.startsWith('Untitled') || title === "") {
    title = await tp.system.prompt('Inserisci il Titolo del Post Blog: ');
    if (!title) {
        title = "Blog Post " + tp.date.now("YYYY-MM-DD HH-mm");
    }
}

// 2. COSTRUZIONE CONTENUTO CANONICO BLOG (Quartz)
let fileContent = `---
stage: seed 🌱
draft: true
type: article
area: tech
related: []
aliases: []
source: original
title: "${title}"
date: ${tp.date.now("YYYY-MM-DD")}
updated: ${tp.date.now("YYYY-MM-DDTHH:mm")}
tags: [tech/web]
summary: "Takeaway e sintesi dell'articolo per il Digital Garden Quartz."
---
[[Home MOC|Home]] / [[05 - Blog|Blog]] / [[${title}]]

# ${title}

## Concetto Principale
<mark style="background:rgba(255, 193, 69, 0.32)"><font color="#cc8800"><b>${title}</b></font></mark>: 

## Caso d'Uso ed Esempio Pratico

## Considerazioni e Limiti

`;

tR += fileContent;

// 3. SPOSTAMENTO IN BLOG
try {
    const targetFolder = "05 - Blog";
    if (tp.file.folder() !== targetFolder) {
        await tp.file.move(`${targetFolder}/${title}`);
        new Notice(`✓ Articolo Blog "${title}" creato in Blog`);
    }
} catch (error) {
    new Notice(`⚠ Spostamento: ${error.message}`);
}
-%>
