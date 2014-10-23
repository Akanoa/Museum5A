Museum5A
========


Projet réalisé dans le cadre du module REV - ENIB 2014

Programme principal
-------------------

* Pour lancer le projet avec le musée par defaut: ( localisé dans datas/generated/defaultMuseum/defaultMuseum.xml )
exemple ici : https://github.com/Akanoa/Museum5A/tree/master/datas/generated/defaultMuseum

```
python main.py
```

* Si vous souhaitez lancer un autre musée : 

```
python main.py -n "nomDuMusée"
```

Géneration de musée
-------------------

Les musées sont générés procéduralement en utilisant le script python generator.py
Il y a également un module de visualisation du musée utilisant pyglet.

* Pour lancer la génération d'un nouveau musée par defaut, lancer

```
python generator.py
```

* Vous pouvez choisir de generer un nouveau musée en utilisant 

```
python generator.py -n "nomDuMusée"
```

* Pour obtenir une visualisation utilisant pyglet et obtenir des fichiers bmp servant de map du niveau

```
python main.py -v Y -n "nomDuMusée"
```

Géneration de labyrinthe
------------------------

La génération du musée s'appuie sur un algorithme générant un labyrinthe.
Cet algorithme a été modifié pour les besoins du projet mais est disponible ici dans son état original :
http://thelinuxchronicles.blogspot.fr/2012/07/python-maze-generation-and-solution.html

Le fichier maze.py permet de générer un labyrinthe tandis que le fichier mazeView.py permet d'obtenir une visualisation du labyrinthe via pygame ( et la génération des fichiers de map servant à se reperer dans le musée ( implémentation à venir ))

Pour obtenir l'aide : 
```
python mazeView.py -h 
```

Pour generer un labyrinthe et obtenir sa visualisation sans passer par le generateur :
[rows, cols, sizeCell, sizeWall]

```
python mazeView.py 100 100 10 2
```

Pour plus d'infos sur les algorithmes de génération de labyrinthe
http://www.astrolog.org/labyrnth/algrithm.htm
