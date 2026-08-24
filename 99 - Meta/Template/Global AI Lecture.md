---
status: permanent
type: lecture
area: education
related: []
aliases: []
source: original
title: "<% tp.file.title %>"
date: <% tp.file.creation_date("YYYY-MM-DD") %>
updated: <% tp.file.last_modified_date("YYYY-MM-DDTHH:mm") %>
tags: [education/lecture, tech/ai]
summary: "Appunti strutturati di lezione con integrazione di concetti AI."
---
[[Home MOC|Home]] / [[Template]] / [[Global AI Lecture]]

<%*
// ========== CONFIGURAZIONE ==========
const BASE_FOLDER = "03 - Inbox/Scuola";
const FILE_PREFIX = "AI SC ";
// ===================================

// 1. GESTIONE TITOLO
title = tp.file.title
if (title.startsWith('Untitled')) {
	title = await tp.system.prompt('Title: ');
	await tp.file.rename(FILE_PREFIX + title);
}

// 2. SELEZIONE MATERIA
const lectures = ["Italiano", "Matematica", "Fisica", "Informatica", "Inglese", "Storia", "Filosofia", "Arte"];
const lecture = await tp.system.suggester(lectures, lectures.map(l => l.toLowerCase()), false, "Select lecture:");
const lectureCapitalized = lecture.charAt(0).toUpperCase() + lecture.slice(1);

// 3. OTTIENI PARENT (usa BASE_FOLDER)
const lectureFolder = `${BASE_FOLDER}/${lectureCapitalized}`;
const allFiles = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith(lectureFolder))
    .map(f => f.basename);

const defaultMOC = lectureCapitalized + " MOC";
allFiles.unshift(defaultMOC);

// 4. SUGGESTER PER PARENT
const parentName = await tp.system.suggester(allFiles, allFiles, true, "Select parent note:");

tR += '---'
%>
Date: <%tp.date.now("YYYY-MM-DD")%> <%tp.date.now("HH")+":00"%>
Tags: 
- AI
- school
- <% lecture %>
Last modified: <% tp.file.last_modified_date() %>

---
Up: [[<%parentName%>]]
Related:

# <%* tR += title %>

<% tp.file.cursor(1) %>

<%* 
// 5. SPOSTA IL FILE (usa BASE_FOLDER e FILE_PREFIX)
await tp.file.move(`${BASE_FOLDER}/${lectureCapitalized}/${FILE_PREFIX}${title}`);

// 6. AGGIORNA IL PARENT
const parentFile = tp.file.find_tfile(parentName);
const currentFileName = FILE_PREFIX + title;

if (parentFile) {
    try {
        let parentContent = await app.vault.read(parentFile);
        
        if (parentContent.match(/Related(?:\s+to)?:/)) {
            parentContent = parentContent.replace(
                /(Related(?:\s+to)?:)\s*
((?:- .*
)*)/,
                `$1
- [[${currentFileName}]]
$2`
            );
        } else {
            parentContent += `
---
## Collegamenti to:
- [[${currentFileName}]]
`;
        }
        
        await app.vault.modify(parentFile, parentContent);
        new Notice(`✓ Link aggiunto a "${parentName}"`);
    } catch (error) {
        new Notice(`⚠ Errore: ${error.message}`);
    }
} else {
    new Notice(`⚠ Parent "${parentName}" non trovato. Link creato, modifica manualmente.`);
}
%>
