# Projet_POO_PPMD : Le démineur en Orienté Objet

Ce dépot est le rendu du projet le programmation orienté objet de la filière PPMD 2025/2026. 

## Architecture du dépot

L'objectif du projet était de développer un jeu qui soit à la fois jouable depuis le terminal et depuis une interface graphique, c'est donc de cette manière qu'est organisé le dépot.

### analyse 
Ce dossier contient 4 diagrammes qui sont le résultat de mon analyse préalable, à savoir un diagramme des **cas d'utilisation**, un diagramme de **classe**, un diagramme **d'états transitions** et un diagramme de **sequence**.

### version_interface 
Ce dossier est la version du jeu avec interface graphique. Il contient: 
- un dossier **images_drapeaux** qui contient les images des drapeaux, utilisés pour marquer une case avec une potentielle bombe.
- un script python **classes.py** qui contient les différentes classes des éléments de mon jeu.
- un script python **demineur.py** qui gère l'affichage de l'interface avec PyQT en faisant appel à classes.py. **C'est ce script qu'il faut éxécuter si vous désirez jouer au jeu.**

### version_terminal 
De la même manière, ce dossier contient la version jouable depuis le terminal. Il contient : 
- un script un script python **classes.py** qui contient les différentes classes des éléments de mon jeu. Il est légèrement différent que le script classes.py de la version interface, notamment au niveau des drapeaux, qui s'affichent sur le terminal par le biais d'émojis. 
- un script python **demineur.py** qui gère l'affichage dans le terminal et le déroulement du jeu. **C'est ce script qu'il faut éxécuter si vous désirez jouer au jeu.**

### requirements.txt 
Ce fichier indique les modules python à installer pour pouvoir éxécuter les scripts, mais il y a de grandes chances que vous ayez déjà tout ce qu'il faut car ce sont des modules de base installés en même temsp que votre version de python. Pour information, le script a été développé avec la version 3.10.11 de python. 
La ligne a éxécuter pour installer les modules est la suivante: 

```bat
pip install requirements.txt
```
