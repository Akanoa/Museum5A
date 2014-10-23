Museum5A
========


Projet réalisé dans le cadre du module REV - ENIB 2014

Contenu du projet & options de lancement

* Pour lancer le projet avec le musée par defaut: ( localisé dans datas/generated/defaultMuseum/defaultMuseum.xml )
exemple ici : https://github.com/Akanoa/Museum5A/tree/master/datas/generated/defaultMuseum

```
python main.py
```

* Si vous souhaitez lancer un autre musée : 

```
python main.py -n "nomDuMusée"
```

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
