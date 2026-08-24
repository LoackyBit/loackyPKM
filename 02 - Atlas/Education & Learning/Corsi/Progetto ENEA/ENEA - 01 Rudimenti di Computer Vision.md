---
status: permanent
type: project
area: tech
related: []
source: original
title: "ENEA - 01 Rudimenti di Computer Vision"
date: '2026-02-09'
updated: 2026-05-24T23:05
tags: []
summary: "M1 (montecchi): rudimenti di computer vision"
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[ENEA - 01 Rudimenti di Computer Vision]]

[[Progetto ENEA]]
# ENEA - 01 primo incontro

M1 (montecchi): rudimenti di computer vision
- camera model
- camera calibration
- tecniche ottiche per la caratterizzazione geometrica

M2 (Cara e ubertini): creazione immagine 3D
- software meshroom (2ds → 3d)
- scanner 3d*

M3 (ubertini): stampa 3d
- tecnologie di stampa 3d e preparazione dei file di stampa
- stampante 3d*

M1-E1: calibrazione della camera di un proprio dispositivo con il software CamCalib

M1-E2: determinazione coordinate di un punto reale mediante teodolite in doppia posizione

# Cap 1: La vista

- cristallino, elemento sensibile, fovea (acuità visiva)
- 2 occhi → profondità mediante convergenza

- radiazione elettromagnetica
	- onda elettromagnetica
		- polarizzata linearmente
		- nel vuoto viaggia a *c*
	- lunghezza d’onda
		- occhio umano → 400nm - 700nm
		- realtà → 0.01nm - 1km
	- ammasso aperto - telescopio Hubble
# Cap 2: 

# Cap 3: Costruzione dell’immagine

1. lente convergente & freccia
2. tracciare raggio passante per il centro della lente
3. tracciare raggio parallelo all’asse ottico
4. costruzione dell’immagine

# Cap 4: Immagine Digitale

- primi sensori digitali → CCD & CMOS → 3CCD usato alcune volte nei film
- scacchiera di pixel (collegamento alla matematica → matrici)
- convenzione 0,0 → pixel in alto a sinistra
- presenza del *firmware*
- formati *raster*

# Cap 5: Camera Model - il modello fisico



# Cap 6: Distorsione e Aberrazione dell’immagine

- aberrazioni
	- monocromatiche
		- sfocatura
		- sferica
		- coma
		- astigmatismo
		- **distorsione**
			- barrel
			- pincushion
		- curvatura spazio tempo
	- cromatiche
		- assiali
		- laterali

# Cap 7: Calibrazione Fotocamera

- stampare una scacchiera con passo noto
- spianarla su supporto piano rigido
- scattare una serie di fotografie con la **focale e l’apertura di lavoro (fisse)**
- utilizzare la funzione *calibrateCamera*

# Cap 8: Tecniche ottiche per la caratterizzazione geometrica

- triangolazione
	- teodolite
	- stazione totale
	- tecniche che vanno bene per pochi punti
- fotogrammetria
- dish solare → fotogrammetria + stazione totale
- laser scanner → stazione totale automatizzata
- scanner 3d sense → 
-

---
## Collegamenti
