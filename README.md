# SAE - API de Gestion de Bibliothèque (DDAW)

Ce projet a été réalisé dans le cadre de la SAE "Développement & Déploiement d'une Application Web". Il s'agit d'une API RESTful conteneurisée permettant la gestion complète d'une bibliothèque (Auteurs, Livres, Genres, Biographies).

**Binôme :**
* **RANDRIANARISOA Ambinintsoa**
* **FANAMBIMIADANTSOA Khejia**

---

## 1. Contexte et Objectifs

L'objectif de cette application est de fournir un backend performant pour gérer des ressources bibliographiques. Elle met en œuvre le cycle de vie logiciel complet : développement modulaire, persistance des données via ORM, et déploiement via Docker.

**Technologies utilisées :**
* **Langage/Framework** : Python / FastAPI
* **Base de données** : PostgreSQL 13
* **ORM** : SQLAlchemy
* **Conteneurisation** : Docker & Docker Compose

---

## 2. Architecture et Modélisation

L'application respecte une architecture MVC (Modèle-Vue-Contrôleur) adaptée aux API. Les données sont persistées dans PostgreSQL avec les relations suivantes :

* **One-to-One** : Un **Auteur** possède une unique **Biographie**.
* **One-to-Many** : Un **Auteur** peut écrire plusieurs **Livres**.
* **Many-to-Many** : Un **Livre** peut appartenir à plusieurs **Genres**, et un Genre contient plusieurs Livres (via une table d'association `livre_genre`).

---

## 3. Installation et Lancement

### Prérequis
* Docker et Docker Compose installés sur la machine.
* Git.

### Démarrage rapide
1.  Cloner le dépôt :
    ```bash
    git clone [https://github.com/ton_pseudo_github/sae-bibliotheque.git](https://github.com/ton_pseudo_github/sae-bibliotheque.git)
    cd sae-bibliotheque
    ```

2.  Lancer l'application via Docker Compose :
    ```bash
    docker-compose up --build -d
    ```
    *(Note : Utilisez `docker compose` sans tiret selon votre version de Docker).*

L'API sera accessible à l'adresse : `http://localhost:8000`

---

## 4. Documentation et Exemples d'Utilisation

L'API dispose d'une documentation interactive Swagger UI accessible ici :
 **http://localhost:8000/docs**

### Exemples de routes principales :

**1. Créer un Auteur (POST)**
* Endpoint : `/auteurs/`
* Body :
    ```json
    {
      "nom": "Victor Hugo"
    }
    ```

**2. Créer un Genre (POST)**
* Endpoint : `/genres/`
* Body :
    ```json
    {
      "nom": "Drame"
    }
    ```

**3. Créer un Livre avec relations (POST)**
* Endpoint : `/livres/`
* Description : Crée un livre lié à l'auteur ID `1` et au genre ID `1`.
* Body :
    ```json
    {
      "titre": "Les Misérables",
      "auteur_id": 1,
      "genre_ids": [1]
    }
    ```

---

## 5. Données de Test

Un fichier SQL contenant un jeu de données minimal est fourni à la racine du projet : `data_test.sql`.
Il contient des insertions types pour peupler la base de données avec des auteurs (ex: J.K. Rowling), des genres et des livres liés.

La persistance des données est assurée par un volume Docker nommé `postgres_data`.

---

## 6. Image Docker Hub

L'image de l'API est construite et hébergée publiquement sur Docker Hub.

* **Lien Docker Hub** : [plus tard]
* **Commande pour pull l'image** :
    ```bash
    docker pull ton_pseudo/sae-bibliotheque:v1
    ```
* **Commande pour lancer l'image seule (sans la BDD)** :
    ```bash
    docker run -p 8000:8000 ton_pseudo/sae-bibliotheque:v1
    ```
