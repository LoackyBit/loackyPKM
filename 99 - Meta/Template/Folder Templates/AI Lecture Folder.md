---
status: permanent
type: lecture
area: meta
related: []
source: original
title: "AI Lecture Folder"
date: '2026-01-31'
updated: 2026-01-31T16:19
tags: []
---
[[Home MOC|Home]] / [[Template]] / [[AI Lecture Folder]]

<%*
// ========== CONFIGURAZIONE ==========
const FILE_PREFIX = "AI SC ";
// ===================================

// 1. CHIEDI SEMPRE IL TITOLO (anche se non è Untitled)
title = await tp.system.prompt('Title: ');
if (!title) {
    new Notice("❌ Creazione annullata: nessun titolo inserito");
    return;
}
await tp.file.rename(FILE_PREFIX + title);

// 2. OTTIENI CARTELLA CORRENTE
const currentFolder = tp.file.folder(true);

// 3. OTTIENI TUTTI I FILE NELLA CARTELLA CORRENTE
const allFiles = app.vault.getMarkdownFiles()
    .filter(f => {
        const fileFolder = f.parent.path;
        return fileFolder === currentFolder;
    })
    .map(f => f.basename)
    .filter(name => name !== FILE_PREFIX + title);  // Escludi il file appena creato

// 4. AGGIUNGI MOC COME PRIMA OPZIONE
const folderName = currentFolder.split('/').pop();
const defaultMOC = folderName + " MOC";
allFiles.unshift(defaultMOC);

// 5. SUGGESTER PER PARENT
const parentName = await tp.system.suggester(allFiles, allFiles, true, "Select parent note:");

tR += '---'
%>
Date: <%tp.date.now("YYYY-MM-DD")%> <%tp.date.now("HH")+":00"%>
Tags: 
- AI
- school
- <% folderName.toLowerCase() %>
Last modified: <% tp.file.last_modified_date() %>

---
Up: [[<%parentName%>]]
Related:

# <%* tR += title %>

<% tp.file.cursor(1) %>

<%* 
// 6. AGGIORNA IL PARENT
const parentFile = tp.file.find_tfile(parentName);
const currentFileName = FILE_PREFIX + title;

if (parentFile) {
    try {
        let parentContent = await app.vault.read(parentFile);
        
        if (parentContent.match(/Related(?:\s+to)?:/)) {
            parentContent = parentContent.replace(
                /(Related(?:\s+to)?:)\s*\n((?:- .*\n)*)/,
                `$1\n- [[${currentFileName}]]\n$2`
            );
        } else {
            parentContent += `\n---
## Collegamenti to:\n- [[${currentFileName}]]\n`;
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
