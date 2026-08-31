---
status: permanent
type: concept
area: tech
related: []
source: original
title: "Submodule"
date: '2025-03-03'
updated: 2026-05-22T18:26
tags: []
summary: "I submoduli su GitHub sono una funzionalità di Git che consente di includere un repository Git all'interno di un altro repository. Questo è utile per mantenere progetti separati all'interno di uno ..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[Submodule]]

I submoduli su GitHub sono una funzionalità di Git che consente di includere un repository Git all'interno di un altro repository. Questo è utile per mantenere progetti separati all'interno di uno principale, mantenendo la separazione tra le cronologie di commit. Ecco come gestirli:

## Cos'è un Submodule?

Un submodule è essenzialmente un repository Git che viene incorporato all'interno di un altro repository come una sottocartella. Mantiene il suo storico dei commit e può essere aggiornato indipendentemente dal repository principale[2](https://codegrind.it/documentazione/git/git-submodules)[3](https://www.atlassian.com/it/git/tutorials/git-submodule).

## Come Aggiungere un Submodule

1. **Aggiungi il Submodule**:
    
    `git submodule add https://github.com/utente/progetto-submodule.git percorso/submodule`
    
    Questo comando clona il repository specificato nella directory del submodule e aggiunge un file `.gitmodules` nella root del tuo repository[1](https://dagtech.it/blog/1013/git-submodules)[2](https://codegrind.it/documentazione/git/git-submodules).
    
2. **Committa le Modifiche**:
    
    `git add .gitmodules percorso/submodule git commit -m "Aggiunto submodule progetto-submodule"`
    

## Inizializzare e Aggiornare i Submoduli

1. **Inizializza i Submoduli**:
    
    `git submodule init`
    
2. **Aggiorna i Submoduli**:
    
    `git submodule update`
    
    Oppure, puoi combinare i due passaggi in uno:
    
    `git submodule update --init --recursive`
    

## Aggiornare un Submodule

1. **Naviga nella Directory del Submodule**:
    
    `cd percorso/submodule`
    
2. **Aggiorna il Submodule**:
    
    `git checkout main git pull origin main`
    
3. **Committa le Modifiche nel Repository Principale**:
    
    `cd ../.. git add percorso/submodule git commit -m "Aggiornato submodule progetto-submodule"`
    

I submoduli sono utili per includere librerie o componenti esterni senza integrare direttamente il codice sorgente nel tuo repository principale, mantenendo la modularità e l'indipendenza dei componenti[2](https://codegrind.it/documentazione/git/git-submodules)[4](https://klez.me/2019/04/11/git-submodules-una-feature-spettacolare-e-sottovalutata/).

---
## Collegamenti
