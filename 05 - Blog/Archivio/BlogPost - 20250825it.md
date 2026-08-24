---
stage: fine-tuned 🧠
draft: false
type: article
area: tech
related: []
source: "https://www.youtube.com/watch?v=gd7BXuUQ91w"
title: "Imparare Vim e Neovim: la Mia Configurazione per Programmazione Python"
date: '2025-08-25'
updated: 2026-07-19T02:09
tags: [tech/programmazione, tech/vim, tech/python, tech/terminale, tech/macos, tech/neovim]
summary: "Negli ultimi giorni ho deciso di immergermi nello studio di Vim, un editor di testo potente ma notoriamente ostico, per migliorare le mie competenze di programmazione. Sto seguendo il corso [CS50's..."
---
[[Home MOC|Home]] / [[Blog]] / [[BlogPost - 20250825it|Imparare Vim e Neovim: la Mia Configurazione per Programmazione Python]]

# Introduzione

Negli ultimi giorni ho deciso di immergermi nello studio di Vim, un editor di testo potente ma notoriamente ostico, per migliorare le mie competenze di programmazione. Sto seguendo il corso [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) di Harvard, che include una serie di *problem sets* – esercizi di coding che richiedono di sviluppare soluzioni a problemi specifici. Per rendere l’esperienza più formativa, ho scelto di scrivere questi programmi usando Vim, o meglio, Neovim, direttamente dal terminale. In questo post racconto come ho configurato il mio ambiente di lavoro, integrando Visual Studio Code, iTerm2 e cheat sheets per Vim e il terminale macOS, e come ho superato alcune sfide iniziali.

## Contesto

Il mio obiettivo era duplice: imparare a usare Vim in modo efficace e fare pratica con i comandi del terminale macOS. I *problem sets* di CS50, come quello sulle [Vanity Plates](https://cs50.harvard.edu/python/psets/5/test_plates/), sono perfetti per esercitarsi, ma di solito li risolvevo usando un container Docker su Visual Studio Code (VS Code). Ho dovuto quindi decidere se usare Vim come estensione su VS Code o passare a Neovim direttamente dal terminale.

Dopo un po’ di esperimenti, ho optato per Neovim da terminale, perché mi permetteva di approfondire sia Vim che i comandi del terminale. Tuttavia, ho dovuto affrontare alcune configurazioni tecniche e trovare un modo per rendere il processo più efficiente, soprattutto per imparare i comandi di Vim e del terminale senza perdermi tra mille risorse.

## Configurazione di Visual Studio Code con Vim

Inizialmente, ho provato a integrare Vim su VS Code. Ho installato due estensioni:

- **[VSCode Neovim](https://marketplace.visualstudio.com/items?itemName=asvetliakov.vscode-neovim)**: Porta le funzionalità di Neovim direttamente in VS Code.
- **[Nvim UI+](https://marketplace.visualstudio.com/items?itemName=wrathcodes.nvim-ui-plus)**: Aggiunge un’interfaccia colorata che evidenzia la modalità di Vim (normale, inserimento, visiva, ecc.).

L’installazione di queste estensioni non è stata sufficiente. Ho dovuto modificare il file di configurazione di Neovim, `init.lua`, per integrare l’estensione Nvim UI+. Questo ha richiesto l’aggiunta di alcune righe specifiche, ma per evitare errori quando usavo Neovim fuori da VS Code, ho racchiuso il codice in un blocco condizionale `if`. Ecco un esempio di come ho configurato il file:

```lua
if vim.g.vscode then
    -- Configurazioni specifiche per VS Code
    
end
```

Questa configurazione ha funzionato, ma ho sentito che lavorare direttamente su VS Code mi stava tenendo lontano dall’esperienza “pura” del terminale, che volevo esplorare per imparare i comandi di sistema.

## Configurazione di iTerm2

Per usare Neovim dal terminale, ho deciso di passare a [iTerm2](https://iterm2.com/), un sostituto avanzato del terminale macOS standard. iTerm2 offre molte funzionalità, ma ho avuto un problema: non riuscivo a muovermi tra le parole usando la combinazione **Option + frecce direzionali**, una scorciatoia essenziale per la navigazione veloce.

Ho provato a cambiare l’impostazione dei tasti speciali da “Meta” a “Esc+” seguendo alcune guide, come quella su [iTerm2 Setup](https://sourabhbajaj.com/mac-setup/iTerm/), ma non ha risolto il problema. Alla fine, ho creato una scorciatoia personalizzata in iTerm2 per emulare il movimento tra le parole. Ecco i passaggi che ho seguito:

1. Apri iTerm2 > **Preferences** > **Profiles** > **Keys**.
2. Aggiungi una nuova scorciatoia:
   - **Keyboard Shortcut**: `Option + ←`
   - **Action**: `Send Escape Sequence`
   - **Esc+**: `b` (per spostarsi indietro di una parola).
3. Ripeti per `Option + →` con `Esc+ f` (per spostarsi avanti).

Questa soluzione ha reso la navigazione molto più fluida. Per approfondire, ho anche consultato la documentazione di iTerm2 su [CSI u](https://iterm2.com/documentation-csiu.html).

## Passaggio a Neovim da Terminale

Alla fine, ho deciso di abbandonare VS Code per usare Neovim direttamente da iTerm2. Questo mi ha permesso di concentrarmi sia su Vim che sui comandi del terminale. Tuttavia, mi sono accorto che non conoscevo molti comandi essenziali, come quelli per copiare file o navigare rapidamente. Inizialmente, ho cercato video su YouTube, come [“60 Linux Commands you NEED to know”](https://www.youtube.com/watch?v=gd7BXuUQ91w), ma ho trovato questo approccio poco efficiente per un accesso rapido alle informazioni.

## Cheat Sheets: La Svolta per l’Efficienza

Per velocizzare l’apprendimento, ho cercato dei *cheat sheets* per Vim e il terminale macOS. Dopo aver esplorato varie risorse, come [Vim Cheat Sheet](https://vim.rtorr.com/) e [Mac Terminal Commands Cheat Sheet](https://phoenixnap.com/kb/mac-terminal-commands), ho scaricato due PDF utili:

- [Vim Commands Cheat Sheet](https://phoenixnap.com/kb/wp-content/uploads/2021/11/vim-commands-cheat-sheet-by-pnap.pdf)
- [Mac Terminal Commands Cheat Sheet](https://phoenixnap.com/kb/wp-content/uploads/2023/05/mac-terminal-commands-cheat-sheet-pdf.pdf)

Ho stampato questi cheat sheets e li ho appesi sulla lavagna davanti alla mia scrivania, così da averli sempre a portata di mano. Questo mi ha permesso di consultare rapidamente comandi come `cp` per copiare file o `:w` per salvare in Vim, senza dover cercare online ogni volta.

## Sfide e Soluzioni

Ecco alcune delle sfide che ho affrontato e come le ho risolte:

- **Navigazione lenta in Vim**: Ho usato il tutor integrato di Vim (`:Tutor`) per imparare i comandi base e ho tenuto il cheat sheet a portata di mano per comandi più avanzati.
- **Comandi terminale sconosciuti**: Ho memorizzato comandi essenziali come `pwd` (stampa percorso corrente) e `cp file1 file2` (copia file) grazie al cheat sheet e a risorse come [Baeldung on Linux](https://www.baeldung.com/linux/files-quickly-duplicate-multiple).
- **Configurazione di iTerm2**: La creazione di scorciatoie personalizzate ha risolto il problema della navigazione con Option + frecce.

## Risultati

Ora sono pronto a programmare i *problem sets* di CS50 usando Neovim su iTerm2. L’ambiente è configurato, i cheat sheets sono sulla mia lavagna e sto iniziando a sentirmi più a mio agio con Vim e il terminale. Scrivere codice in questo modo è più impegnativo rispetto a usare un IDE come VS Code, ma mi sta aiutando a capire meglio il flusso di lavoro di un programmatore e a padroneggiare strumenti potenti.

## Conclusione

Imparare Vim e configurare un ambiente di lavoro basato su terminale non è stato semplice, ma è un investimento che sta già dando i suoi frutti. I cheat sheets e una configurazione personalizzata di iTerm2 hanno fatto la differenza, rendendo il processo più fluido. Se anche tu stai pensando di provare Vim o Neovim, ti consiglio di iniziare con il tutor integrato e di tenere a portata di mano un cheat sheet per non perderti. Hai mai provato a configurare il tuo terminale per la programmazione? Fammi sapere nei commenti come organizzi il tuo flusso di lavoro!

---

### Note Tecniche

- **Risorse utilizzate**:
  - [CS50 Python](https://cs50.harvard.edu/python/)
  - [iTerm2](https://iterm2.com/)
  - [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)
  - Cheat sheets: [Vim](https://phoenixnap.com/kb/vim-commands-cheat-sheet) e [Mac Terminal](https://phoenixnap.com/kb/mac-terminal-commands)

---
## Collegamenti
