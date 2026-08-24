---
status: permanent
type: project
area: tech
related: []
source: original
title: "ENEA - 02 Meshroom"
date: '2026-02-10'
updated: 2026-05-24T23:05
tags: []
summary: "M1 (montecchi): rudimenti di computer vision"
---
[[Home MOC|Home]] / [[Education & Learning MOC|Education & Learning]] / [[ENEA - 02 Meshroom]]

[[Progetto ENEA]]
# ENEA - 02 Meshroom

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

---

- organizzazione no-profit
- open source

- alicevision framework
- meshroom software

- 3d reconstruction
- camera tracking
- hdr panorama
- photometric stereo
- raw conversion

- pipeline di meshroom
	1. cameraInit
	2. featureExtraction → algoritmo SIFT
	3. imageMatching
	4. featureMatching
	5. structureForMotion

	6. prepareDenseScene
	7. depthMap
	8. depthMapFilter
	9. nodeTexturing → UV mapping

- argomenti extra
	- camera calibration
	- augment reconstruction
	- bounding box
	- meshdecimate & meshresampling
	- turntable
		- masking semplice
		- masking con colore

---
## Collegamenti
