# Extrémités

Jeu de cartes : une rangée de cartes est posée, chaque joueur prend à son tour celle de
gauche ou celle de droite, et on compte les points à la fin. Simple à comprendre, moins
simple à jouer correctement.

En ligne : https://dunandchatellet.fr/extremites/extremites.html

## Deux versions du même jeu

| Version | Fichiers |
| --- | --- |
| Originale, en Python (Tkinter) | `python-source/extremite.py`, compilée en `extremites.exe` |
| Portage web, jouable sans rien installer | `extremites.html`, `extremites.css`, `extremites.js` |

Le portage reprend fidèlement les règles et le déroulement de la version Python.

## Lancer la version Python

```bash
python python-source/extremite.py
```

Tkinter est fourni avec Python. Le `.exe` livré n'est pas signé : Windows affiche
un avertissement SmartScreen au premier lancement.

---

Pierre Dunand-Chatellet — [tous mes projets](https://dunandchatellet.fr/projets.html)
