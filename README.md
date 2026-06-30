# TechSecure - Secure Subsidiary Management

A containerized management (CRUD) application designed to provide centralized management of a company's subsidiaries. This project focuses on **infrastructure security** and **network segmentation**, as part of a professional deployment (AIS).

## ✨ Features

* **Subsidiary Management:** Create, read, update, and delete (CRUD) operations via a web interface.
* **Secure Architecture:** Strict network segmentation with database isolation.
* **Secrets Management:** Environment variables injected via `.env` (excluded from Git versioning).
* **Containerized Deployment:** Full infrastructure (Flask, MySQL, Adminer) orchestrated with Docker Compose.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** MySQL 8.0
* **Frontend:** HTML5, CSS (Responsive)
* **Infrastructure:** Docker, Docker Compose
* **Admin:** Adminer (DB Management)

## 🚀 Getting Started

### Prerequisites

You need [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Installation & Deployment

1. **Clone the project or navigate to the directory:**

   ```bash
   cd TechSecure
   ```

2. **Environment configuration:**

   Create a `.env` file at the root of the project and add the following variables. This file must never be committed:

   ```env
   DB_HOST=db_mysql
   DB_USER=techuser
   DB_PASSWORD=<YOUR_SECURE_PASSWORD>
   DB_NAME=techsecure_db
   MYSQL_ROOT_PASSWORD=<YOUR_ROOT_PASSWORD>
   FLASK_SECRET_KEY=<RANDOM_GENERATED_KEY>
   FLASK_APP=app.py
   FLASK_DEBUG=1
   ```

3. **Build and start the containers:**

   ```bash
   docker compose up -d --build
   ```

## 🌐 Accessing the Services

Once the containers are running, the services are accessible via the browser:

* **Web Application:** http://localhost:5000
* **Database Management (Adminer):** http://localhost:8082
  * System: MySQL
  * Server: db_mysql
  * Username: techuser
  * Password: The one set in `DB_PASSWORD` in the `.env` file

## 🛡️ Security with Docker Compose

The architecture is designed to minimize the attack surface as much as possible:

* **Network Isolation:** Use of two Docker networks. The `backend_net` network is declared with `internal: true`. The database is fully isolated, it cannot communicate with the internet nor be accessed directly from the host.
* **Least Privilege:** Only the `flask_app` and `adminer` containers are connected to `backend_net` and can interact with the database.
* **Limited Exposure:** Only ports `5000` (Application) and `8082` (Adminer) are mapped to the host. The database port `3306` is never exposed outside the Docker network.

## 📁 Project Structure

```
TechSecure/
├── app/               # Flask source code
│   ├── app.py         # Main application and routes
│   └── Dockerfile     # Build instructions for the Flask image
├── db/
│   └── init.sql       # SQL initialization script (database schema)
├── static/            # Assets (CSS, images)
├── templates/         # HTML templates (base, subsidiary view, forms)
├── .env               # Secrets configuration (excluded from Git)
├── .gitignore         # Files and folders to ignore (e.g. .env, __pycache__)
└── docker-compose.yml # Service and network orchestration
```