---
title: "Cornell Folder"
date: 2026-01-31
updated: 2026-01-31T17:15
tags: []
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[Template]] / [[Cornell Folder]]

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
- cornell
- <% folderName.toLowerCase() %>
Last Modified: <% tp.file.last_modified_date() %>
cssclasses:
- cornell-left
- cornell-right
- cornell-bottom 

<%*
// 3. OTTIENI PARENT (da file nella cartella corrente)
const allFilesCornel = app.vault.getMarkdownFiles()
    .filter(f => f.parent.path === currentFolder)
    .map(f => f.basename);

const defaultMOCCornel = folderName + " MOC";
allFilesCornel.unshift(defaultMOCCornel);

const parentNameCornel = await tp.system.suggester(allFilesCornel, allFilesCornel, true, "Select parent note:");
%>
---
Up: [[<%parentNameCornel%>]]
Related:
<%* tR += '- ' %>

# <%* tR += title %>

> [!cue]
> 

## Notes

- notes goes here
- 

> [!summary]
> 

<%*
// 4. AGGIORNA IL PARENT
const parentFileCornel = tp.file.find_tfile(parentNameCornel);
const currentFileNameCornel = FILE_PREFIX + title;

if (parentFileCornel) {
    try {
        let parentContentCornel = await app.vault.read(parentFileCornel);
        
        if (parentContentCornel.match(/Related(?:\s+to)?:/)) {
            parentContentCornel = parentContentCornel.replace(
                /(Related(?:\s+to)?:)\s*\n((?:- .*\n)*)/,
                `$1\n- [[${currentFileNameCornel}]]\n$2`
            );
        } else {
            parentContentCornel += `\n---
## Collegamenti to:\n- [[${currentFileNameCornel}]]\n`;
        }
        
        await app.vault.modify(parentFileCornel, parentContentCornel);
        new Notice(`✓ Link aggiunto a "${parentNameCornel}"`);
    } catch (error) {
        new Notice(`⚠ Errore: ${error.message}`);
    }
} else {
    new Notice(`⚠ Parent "${parentNameCornel}" non trovato. Link creato, modifica manualmente.`);
}

new Notice(`✓ Cornell note "${title}" creata in ${folderName}`);
%>
