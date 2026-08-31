---
status: permanent
type: concept
area: tech
related: ["[[Tech & AI]]", "[[Custom Terminal]]", "[[Zsh Setup]]", "[[Dotfiles]]"]
source: original
title: "Terminal Setup"
date: '2026-07-13'
updated: 2026-07-13T13:52
tags: [tech/terminal, tech/zsh, tech/p10k, tech/iterm2, tech/setup]
summary: "Oggi ho aggiornato e personalizzato la configurazione del mio custom terminal per ottimizzare il flusso di lavoro e l'estetica dell'interfaccia."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Terminal Setup]]

# Terminal Setup

Oggi ho aggiornato e personalizzato la configurazione del mio **custom terminal** per ottimizzare il flusso di lavoro e l'estetica dell'interfaccia.

## Operazioni Eseguite

### 1. Installazione Font
* Ho installato su [[ITerm2|iTerm2]] i font consigliati da [[Powerlevel10k|p10k]], in particolare il font **MesloLGS NF** (Meslo Nerd Font patched per Powerlevel10k).
* Istruzioni di riferimento: [GitHub - romkatv/powerlevel10k](https://github.com/romkatv/powerlevel10k#meslo-nerd-font-patched-for-powerlevel10k).

### 2. Configurazione del Tema
* Ho installato e configurato il nuovo stile di [[Powerlevel10k|p10k]] eseguendo la configurazione guidata (`p10k configure`) per adattare gli elementi visivi (prompt, icone, colori).

### 3. Configurazione Zsh (`.zshrc`)
* Ho modificato il file di configurazione `~/.zshrc` per associare `ZSH_THEME="powerlevel10k/powerlevel10k"`.
* Ho abilitato e configurato i seguenti plugin per [[Zsh]]:
 - [git](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git): Abbreviazioni e utility per la gestione dei repository [[Git]].
 - [command-not-found](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/command-not-found): Suggerisce pacchetti da installare se un comando inserito non è presente nel sistema.
 - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions): Suggerimenti automatici basati sulla cronologia dei comandi.
 - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting): Evidenziazione sintattica dei comandi nel terminale in tempo reale.
 - [macos](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/macos): Utility e alias specifici per l'ambiente [[MacOS|macOS]].
