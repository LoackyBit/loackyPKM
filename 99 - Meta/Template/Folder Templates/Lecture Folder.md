---
status: permanent
type: lecture
area: meta
related: []
source: original
title: "Lecture Folder"
date: '2026-01-31'
updated: 2026-01-31T17:08
tags: []
---
[[Home MOC|Home]] / [[Template]] / [[Lecture Folder]]

<%*
// ========== CONFIGURAZIONE ==========
const FILE_PREFIX = "SC ";
// ===================================

// 1. CHIEDI SEMPRE IL TITOLO
title = await tp.system.prompt('Title: ');
if (!title) {
    new Notice("❌ Creazione annullata: nessun titolo inserito");
    return;
}
await tp.file.rename(FILE_PREFIX + title);

// 2. OTTIENI CARTELLA CORRENTE (e.g., "Matematica")
const currentFolder = tp.file.folder(true);
const folderName = currentFolder.split('/').pop();

tR += '---'
%>
Date: <%tp.date.now("YYYY-MM-DD")%> <%tp.date.now("HH")+":00"%>
Tags: 
- school
- <% folderName.toLowerCase() %>
Last modified: <% tp.file.last_modified_date() %>

<%*
// 3. OTTIENI PARENT (da file nella cartella corrente)
const allFilesLec = app.vault.getMarkdownFiles()
    .filter(f => f.parent.path === currentFolder)
    .map(f => f.basename);

const defaultMOCLec = folderName + " MOC";
allFilesLec.unshift(defaultMOCLec);

const parentNameLec = await tp.system.suggester(allFilesLec, allFilesLec, true, "Select parent note:");
%>
---
Up: [[<%parentNameLec%>]]
Related:
<%* tR += '- ' %>

# <%* tR += title %>

<% tp.file.cursor(1) %>

<%*
// 4. AGGIORNA IL PARENT
const parentFileLec = tp.file.find_tfile(parentNameLec);
const currentFileNameLec = FILE_PREFIX + title;

if (parentFileLec) {
    try {
        let parentContentLec = await app.vault.read(parentFileLec);
        
        if (parentContentLec.match(/Related(?:\s+to)?:/)) {
            parentContentLec = parentContentLec.replace(
                /(Related(?:\s+to)?:)\s*\n((?:- .*\n)*)/,
                `$1\n- [[${currentFileNameLec}]]\n$2`
            );
        } else {
            parentContentLec += `\n---
## Collegamenti to:\n- [[${currentFileNameLec}]]\n`;
        }
        
        await app.vault.modify(parentFileLec, parentContentLec);
        new Notice(`✓ Link aggiunto a "${parentNameLec}"`);
    } catch (error) {
        new Notice(`⚠ Errore: ${error.message}`);
    }
} else {
    new Notice(`⚠ Parent "${parentNameLec}" non trovato. Link creato, modifica manualmente.`);
}

new Notice(`✓ Lecture "${title}" creata in ${folderName}`);
%>
