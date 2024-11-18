<p align="center">
  <img src="https://static.ankama.com/dofus/ng/modules/mmorpg/discover/illu-block3.png" />
</p>

# DofScraper3

**DofScraper3** est un projet Python dont l'objectif est de récupérer les liens des pages de l'encyclopédie et d'en extraire les images de tous les éléments. Les téléchargements sont faits selon l'arborescence de l'Encyclopédie et triés de manière pertinente grâce aux filtres.

## Fonctionnement

**DofScrapper** propose un menu, il fonctionne par étapes :

1. Scanner les pages de l'encyclopédie pour récupérer tous les liens selon les catégories et les filtres ;
2. Téléchargement des images grâce au remplissage au préalable d'un fichier JSON grâce aux scans ;

## Installation

1. Cloner ce dépôt ;
2. Créer un environnement virtuel _(non fourni)_ avec `python -m venv env` en étant dans le répertoire de **DofScrapper** ;
3. Activer le script dans `env/bin/activate` _(Sous Linux, il faut utliser `source env/bin/activate`, pour Windows, ouvrir Powershell et exécuter `./env/bin/Activate.ps1`)_ ;
4. Télécharger les dépendances une fois dans l'environnement virtuel avec `pip -r install requirements.txt` ;
5. Exécuter `python __init__.py`.

Le fichier JSON, résultant d'un scan de ma part est fourni. Il peut ne plus être à jour en fonction des changements dans l'encyclopédie.
