# TechSecure - Gestion Sécurisée des Filiales

Une application de gestion (CRUD) conteneurisée, conçue pour assurer la gestion centralisée des filiales d'une entreprise. Ce projet met l'accent sur la **sécurisation de l'infrastructure** et la **segmentation réseau**, dans le cadre d'un déploiement professionnel (AIS).

## ✨ Features

* **Gestion des Filiales :** Création, lecture, mise à jour et suppression (CRUD) via une interface web.
* **Architecture Sécurisée :** Segmentation réseau stricte avec isolation de la base de données.
* **Gestion des Secrets :** Injection des variables d'environnement via `.env` (hors versionnage Git).
* **Déploiement Conteneurisé :** Infrastructure complète (Flask, MySQL, Adminer) orchestrée par Docker Compose.

## 🛠️ Tech Stack

* **Backend :** Python 3, Flask
* **Database :** MySQL 8.0
* **Frontend :** HTML5, CSS (Responsive)
* **Infrastructure :** Docker, Docker Compose
* **Admin :** Adminer (Gestion DB)

## 🚀 Getting Started

### Prérequis

Vous devez avoir [Docker](https://docs.docker.com/get-docker/) et [Docker Compose](https://docs.docker.com/compose/install/) installés sur votre machine.

### Installation & Déploiement

1. **Cloner le projet ou se rendre dans le répertoire :**

   ```bash
   cd TechSecure
   ```

2. **Configuration de l'environnement :**

   Créez un fichier `.env` à la racine du projet et ajoutez les variables suivantes, il ne faut d'ailleurs jamais commiter ce fichier :

   ```env
   DB_HOST=db_mysql
   DB_USER=techuser
   DB_PASSWORD=<VOTRE_MOT_DE_PASSE_SECURISE>
   DB_NAME=techsecure_db
   MYSQL_ROOT_PASSWORD=<VOTRE_MOT_DE_PASSE_ROOT>
   FLASK_SECRET_KEY=<CLE_ALEATOIRE_GENEREE>
   FLASK_APP=app.py
   FLASK_DEBUG=1
   ```

3. **Build et lancement des conteneurs :**

   ```bash
   docker compose up -d --build
   ```

## 🌐 Accès aux services

Une fois les conteneurs démarrés, les services sont accessibles via le navigateur :

* **Application Web :** http://localhost:5000
* **Gestion Base de Données (Adminer) :** http://localhost:8082
  * Système : MySQL
  * Serveur : db_mysql
  * Utilisateur : techuser
  * Mot de passe : Celui défini dans `DB_PASSWORD` dans le `.env`

## 🛡️ Sécurisation avec Docker Compose

L'architecture est pensée pour limiter au maximum la surface d'attaque :

* **Isolation Réseau :** Utilisation de deux réseaux Docker. Le réseau `backend_net` est déclaré avec `internal: true`. La base de données est totalement isolée, elle ne peut pas communiquer avec internet ni être accédée directement depuis l'hôte.
* **Moindre privilège :** Seuls les conteneurs `flask_app` et `adminer` sont connectés au `backend_net` et peuvent interagir avec la base de données.
* **Exposition limitée :** Seuls les ports `5000` pour l'Application et `8082` pour Adminer sont mappés sur l'hôte. Le port de la base de données `3306` n'est jamais exposé à l'extérieur du réseau Docker.

## 📁 Structure du Projet

```
TechSecure/
├── app/               # Code source Flask
│   ├── app.py         # Application principale et routes
│   └── Dockerfile     # Instructions de build pour l'image Flask
├── db/
│   └── init.sql       # Script d'initialisation SQL (schéma de base)
├── static/            # Assets (CSS, images)
├── templates/         # Templates HTML (base, vue filiales, formulaires)
├── .env               # Configuration des secrets (exclu de Git)
├── .gitignore         # Fichiers et dossiers à ignorer (ex: .env, __pycache__)
└── docker-compose.yml # Orchestration des services et des réseaux
```