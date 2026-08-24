---
title: "Note Folder"
date: 2026-01-31
updated: 2026-01-31T16:57
tags: []
status: permanent
macro_area: meta
---
[[Home MOC|Home]] / [[Template]] / [[Note Folder]]

<%*
// ========== CONFIGURAZIONE ==========
// ===================================

// 1. CHIEDI SEMPRE IL TITOLO
let title = await tp.system.prompt('Title: ');
if (!title) {
    new Notice("❌ Creazione annullata: nessun titolo inserito");
    return;
}
await tp.file.rename(title);

// 2. SELEZIONE PARENT (opzionale)
const currentFolder = tp.file.folder(true);
const allFiles = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith(currentFolder))
    .map(f => f.basename)
    .sort();

const defaultOption = "[ Nessun parent ]";
allFiles.unshift(defaultOption);

const parentName = await tp.system.suggester(allFiles, allFiles, true, "Select parent note (optional):");

tR += '---'
%>
Tags:
Created: <% tp.file.creation_date() %>
Last modified: <% tp.file.last_modified_date() %>

---
Up: 
Related:
- 
# <%* tR += title %>

<% tp.file.cursor(1) %>

<%*
// 3. AGGIORNA IL PARENT
if (parentName && parentName !== "[ Nessun parent ]") {
    const parentFile = tp.file.find_tfile(parentName);
    
    if (parentFile) {
        try {
            let parentContent = await app.vault.read(parentFile);
            
            if (parentContent.match(/Related(?:\s+to)?:/)) {
                parentContent = parentContent.replace(
                    /(Related(?:\s+to)?:)\s*\n((?:- .*\n)*)/,
                    `$1\n- [[${title}]]\n$2`
                );
            } else {
                parentContent += `\n---
## Collegamenti to:\n- [[${title}]]\n`;
            }
            
            await app.vault.modify(parentFile, parentContent);
            new Notice(`✓ Link aggiunto a "${parentName}"`);
        } catch (error) {
            new Notice(`⚠ Errore nell'aggiornamento parent: ${error.message}`);
        }
    } else {
        new Notice(`⚠ Parent "${parentName}" non trovato. Link creato, modifica manualmente.`);
    }
}

new Notice(`✓ Note "${title}" creata`);
%>
