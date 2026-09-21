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

**Qui a écrit quoi :** la version Python est de moi. Le portage web (`extremites.html`,
`extremites.css`, `extremites.js`) a été écrit par une IA (Claude) à partir de mon code
Python, dont il reprend les règles et le déroulement.

## Lancer la version Python

```bash
python python-source/extremite.py
```

Tkinter est fourni avec Python. Le `.exe` livré n'est pas signé : Windows affiche
un avertissement SmartScreen au premier lancement.

---

Pierre Dunand-Chatellet — [tous mes projets](https://dunandchatellet.fr/projets.html)
