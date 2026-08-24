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
tags: [education/lecture, education/school]
summary: "Appunti e registrazione delle lezioni scolastiche e universitarie."
---
[[Home MOC|Home]] / [[Template]] / [[Global Lecture]]

<%*
// ========== CONFIGURAZIONE ==========
const BASE_FOLDER = "03 - Inbox/Scuola";
const FILE_PREFIX = "SC ";
const LECTURES = ["Italiano", "Matematica", "Fisica", "Informatica", "Inglese", "Storia", "Filosofia", "Latino", "Scienze", "Arte"];
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
const allFilesLec = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith(lectureFolder))
    .map(f => f.basename);

const defaultMOCLec = lectureCapitalized + " MOC";
allFilesLec.unshift(defaultMOCLec);

const parentNameLec = await tp.system.suggester(allFilesLec, allFilesLec, true, "Select parent note:");

tR += '---'
%>
Date: <%tp.date.now("YYYY-MM-DD")%> <%tp.date.now("HH")+":00"%>
Tags: 
- school
- <% lecture.toLowerCase() %>
Last modified: <% tp.file.last_modified_date() %>

---
Up: [[<%parentNameLec%>]]
Related:

# <%* tR += title %>

<% tp.file.cursor(1) %>

<%* 
// 4. SPOSTA IL FILE
try {
	await tp.file.move(`${BASE_FOLDER}/${lectureCapitalized}/${FILE_PREFIX}${title}`);
	new Notice(`✓ Lecture "${title}" creata`);
} catch (error) {
	new Notice(`⚠ Errore: ${error.message}`);
}

// 5. AGGIORNA IL PARENT
const parentFileLec = tp.file.find_tfile(parentNameLec);
const currentFileNameLec = FILE_PREFIX + title;

if (parentFileLec) {
    try {
        let parentContentLec = await app.vault.read(parentFileLec);
        
        if (parentContentLec.match(/Related(?:\s+to)?:/)) {
            parentContentLec = parentContentLec.replace(
                /(Related(?:\s+to)?:)\s*
((?:- .*
)*)/,
                `$1
- [[${currentFileNameLec}]]
$2`
            );
        } else {
            parentContentLec += `
---
## Collegamenti to:
- [[${currentFileNameLec}]]
`;
        }
        
        await app.vault.modify(parentFileLec, parentContentLec);
        new Notice(`✓ Link aggiunto a "${parentNameLec}"`);
    } catch (error) {
        new Notice(`⚠ Errore: ${error.message}`);
    }
} else {
    new Notice(`⚠ Parent "${parentNameLec}" non trovato. Link creato, modifica manualmente.`);
}
%>
