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
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/idealfitahiana/SAE_projet.git
   cd SAE_projet
    ```

2.  Lancer l'application via Docker Compose :
    ```bash
    docker-compose up --build -d
    ```
    *(Note : Utilisez `docker compose` sans tiret selon votre version de Docker).*

L'API sera accessible à l'adresse : `http://localhost:8000`

---

## 4. Documentation de l'API (Swagger)

Une documentation interactive complète (OpenAPI) est disponible à l'adresse suivante une fois le projet lancé :
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Exemples de routes disponibles :

#### **Gestion des auteurs**
- `GET /auteurs/` : Liste tous les auteurs et leurs livres.
- `POST /auteurs/` : Créer un auteur  
  **Exemple :** `{"nom": "Victor Hugo"}`
- `PUT /auteurs/{id}` : Modifier le nom d'un auteur.
- `DELETE /auteurs/{id}` : Supprimer un auteur (vérifie l'intégrité référentielle).

#### **Gestion des livres**
- `POST /livres/` : Créer un livre lié à un auteur et des genres  
  **Exemple :** `{"titre": "Notre-Dame de Paris", "auteur_id": 1, "genre_ids": [1, 2]}`
- `DELETE /livres/{id}` : Supprimer un livre.
---

## 5. Données de Test

Un fichier SQL contenant un jeu de données minimal est fourni à la racine du projet : `data_test.sql`.  
Il contient des insertions types pour peupler la base de données avec des auteurs (ex: J.K. Rowling), des genres et des livres liés.

La persistance des données est assurée par un volume Docker nommé `postgres_data`.

## 6. Image Docker Hub

L'image de l'API est construite et hébergée publiquement sur Docker Hub.

**Lien Docker Hub :** [https://hub.docker.com/repository/docker/idealfitahiana/sae-bibliotheque/general](https://hub.docker.com/repository/docker/idealfitahiana/sae-bibliotheque/general)

### Commandes Docker

**Télécharger l'image :**
```bash
docker pull idealfitahiana/sae-bibliotheque:v1
* **Commande pour lancer l'image seule (sans la BDD)** :
    ```bash
    docker run -p 8000:8000 idealfitahiana/sae-bibliotheque:v1
    ```
