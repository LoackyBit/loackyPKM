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
tags: [education/cornell, education/school]
summary: "Appunti in formato Cornell per lezioni universitarie e scolastiche."
---
[[Home MOC|Home]] / [[Template]] / [[Global Cornell]]

<%*
// ========== CONFIGURAZIONE ==========
const BASE_FOLDER = "03 - Inbox/Scuola";
const FILE_PREFIX = "SC ";
const LECTURES = ["Italiano", "Matematica", "Fisica", "Informatica", "Inglese", "Storia", "Filosofia", "Scienze"];
// ===================================

// 1. GESTIONE TITOLO
title = tp.file.title
if (title.startsWith('Untitled')) {
	title = await tp.system.prompt('Title: ');
	await tp.file.rename(FILE_PREFIX + title);
}

// 2. SELEZIONE MATERIA CON SUGGESTER
const lecture = await tp.system.suggester(LECTURES, LECTURES.map(l => l.toLowerCase()), false, "Select lecture:");
const lectureCapitalized = lecture.charAt(0).toUpperCase() + lecture.slice(1);

// 3. OTTIENI PARENT
const lectureFolder = `${BASE_FOLDER}/${lectureCapitalized}`;
const allFilesCornel = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith(lectureFolder))
    .map(f => f.basename);

const defaultMOCCornel = lectureCapitalized + " MOC";
allFilesCornel.unshift(defaultMOCCornel);

const parentNameCornel = await tp.system.suggester(allFilesCornel, allFilesCornel, true, "Select parent note:");

tR += '---'
%>
Date: <%tp.date.now("YYYY-MM-DD")%> <%tp.date.now("HH")+":00"%>
Tags:
- school
- cornell
- <% lecture %>
Last Modified: <% tp.file.last_modified_date() %>
cssclasses:
- cornell-left
- cornell-right
- cornell-bottom
---
Up: [[<%parentNameCornel%>]]
Related:
# <%* tR += title %>

> [!cue]
> 

## Notes

- notes goes here
- 

> [!summary]
> 

<%* 
// 4. SPOSTA IL FILE
try {
	await tp.file.move(`${BASE_FOLDER}/${lectureCapitalized}/${FILE_PREFIX}${title}`);
	new Notice(`✓ Cornell note "${title}" creata`);
} catch (error) {
	new Notice(`⚠ Errore: ${error.message}`);
}

// 5. AGGIORNA IL PARENT
const parentFileCornel = tp.file.find_tfile(parentNameCornel);
const currentFileNameCornel = FILE_PREFIX + title;

if (parentFileCornel) {
    try {
        let parentContentCornel = await app.vault.read(parentFileCornel);
        
        if (parentContentCornel.match(/Related(?:\s+to)?:/)) {
            parentContentCornel = parentContentCornel.replace(
                /(Related(?:\s+to)?:)\s*
((?:- .*
)*)/,
                `$1
- [[${currentFileNameCornel}]]
$2`
            );
        } else {
            parentContentCornel += `
---
## Collegamenti to:
- [[${currentFileNameCornel}]]
`;
        }
        
        await app.vault.modify(parentFileCornel, parentContentCornel);
        new Notice(`✓ Link aggiunto a "${parentNameCornel}"`);
    } catch (error) {
        new Notice(`⚠ Errore: ${error.message}`);
    }
} else {
    new Notice(`⚠ Parent "${parentNameCornel}" non trovato. Link creato, modifica manualmente.`);
}
%>
