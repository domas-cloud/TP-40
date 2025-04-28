Engineering materials
====

This repository contains engineering materials of a self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2022.

## Content

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.
* `other` is for other files which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc. If there is nothing to add to this location, the directory can be removed.

## Introduction

Techniniai paaiškinimai apie kodą
Kodo struktūra:
...........
Ryšys su elektromechaniniais komponentais:
•	Arduino Mega 2560 naudojamas žemos pakopos realaus laiko operacijoms vykdyti, kaip jutiklių nuskaitymui (per I2C) ir duomenų siuntimui į Raspberry Pi.
•	Sensor Shield palengvina fizinius jutiklių sujungimus su Arduino Mega.
•	Motor Shield valdo nuolatinės srovės (DC) variklius pagal skaičiavimo modulio perduotas komandas.
•	Raspberry Pi 4 atlieka pagrindinį sprendimų priėmimo vaidmenį: gauna duomenis iš Arduino, apdoroja juos (apskaičiuoja padėtį sienos atžvilgiu) ir siunčia atitinkamas komandas atgal į Arduino.

Kodo kūrimo, kompiliavimo ir įkėlimo procesas:
•	Programavimo kalbos:
o	Arduino Mega: C kalba naudojant Arduino IDE 
o	Raspberry Pi 4: Python kalba, redaguojama ir vykdoma tiesiai per arba terminalą.

•	Kūrimo aplinka:
o	Arduino kodas rašomas, kompiliuojamas ir įkeliamas naudojant Arduino IDE.
o	Raspberry Pi Python skriptai tiesiogiai redaguojami ir paleidžiami be atskiro kompiliavimo proceso.

•	Įkėlimo procesas:
o	Arduino Mega: kodas kompiliuojamas ir per USB kabelį įkeliamas naudojant Arduino IDE.
o	Raspberry Pi 4: skriptai redaguojami tiesiogiai Raspberry Pi aplinkoje, vykdomi per Python interpretatorių.


## How to prepare the repo based on the template

_Remove this section before the first commit to the repository_

1. Clone this repo by using the `git clone` functionality.
2. Remove `.git` directory
3. [Initialize a new public repository on GitHub](https://github.com/new) by following instructions from "create a new repository on the command line" section (appeared after pressing "Create repository" button).
