---
status: permanent
type: concept
area: tech
related: []
aliases: []
source: original
title: "<% tp.file.title %>"
date: <% tp.file.creation_date("YYYY-MM-DD") %>
updated: <% tp.file.last_modified_date("YYYY-MM-DDTHH:mm") %>
tags: [tech/ai]
summary: "Nota concettuale con focus su intelligenza artificiale e machine learning."
---
[[Home MOC|Home]] / [[Template]] / [[Global AI Note]]

<%*
// ========== CONFIGURAZIONE ==========
const BASE_FOLDER = "04 - Fleeting";
// ===================================

// 1. GESTIONE TITOLO
title = tp.file.title
if (title.startsWith('Untitled')) {
    title = await tp.system.prompt('Title: ');
    await tp.file.rename(title);
}

// 2. SELEZIONE PARENT (opzionale)
const allFiles = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith(BASE_FOLDER))
    .map(f => f.basename)
    .sort();

const defaultOption = "[ Nessun parent ]";
allFiles.unshift(defaultOption);

const parentName = await tp.system.suggester(allFiles, allFiles, true, "Select parent note (optional):");

tR += '---'
%>
Tags:
- AI
Created: <% tp.file.creation_date() %>
Last modified: <% tp.file.last_modified_date() %>
---
<%* if (parentName && parentName !== "[ Nessun parent ]") { %>
Up: [[<%parentName%>]]
Related:
<%* } else { %>Up:
Related:
<%* } %>

# <%* tR += title %>

<% tp.file.cursor(1) %>

<%*
// 3. SPOSTA IL FILE
try {
    await tp.file.move(`${BASE_FOLDER}/${title}`);
    new Notice(`✓ Note "${title}" creata`);
} catch (error) {
    new Notice(`⚠ Errore: ${error.message}`);
}

// 4. AGGIORNA IL PARENT
if (parentName && parentName !== "[ Nessun parent ]") {
    const parentFile = tp.file.find_tfile(parentName);
    if (parentFile) {
        try {
            let parentContent = await app.vault.read(parentFile);
            if (parentContent.match(/Related(?:\s+to)?:/)) {
                parentContent = parentContent.replace(
                    /(Related(?:\s+to)?:)\s*
((?:- .*
)*)/,
                    `$1
- [[${title}]]
$2`
                );
            } else {
                parentContent += `
---
## Collegamenti to:
- [[${title}]]
`;
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
%>
