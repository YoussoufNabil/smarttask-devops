# SmartTask - Projet DevOps

Application web simple de gestion de tâches conçue pour l'examen Microservices / Docker / Jenkins.

## Architecture
- Frontend : HTML/CSS/JavaScript servi par Nginx
- Backend : Python Flask + API REST
- Base de données : PostgreSQL
- Orchestration locale : Docker Compose
- CI/CD : Jenkins
- Registre : Docker Hub

## Fonctionnalités
- Ajouter une tâche
- Afficher les tâches
- Marquer une tâche comme terminée / réouverte
- Supprimer une tâche
- Endpoint de santé du backend : `/health`

## Prérequis
- Docker Engine / Docker Desktop
- Docker Compose v2
- Git
- Compte GitHub
- Compte Docker Hub
- Jenkins pour la partie CI/CD

## Lancement local
```bash
docker compose up -d --build
```
Puis ouvrir : http://localhost:8080

Arrêt :
```bash
docker compose down
```

Arrêt avec suppression du volume de données :
```bash
docker compose down -v
```

## Structure
```text
smarttask-devops/
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── nginx.conf
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── docker-compose.yml
├── Jenkinsfile
└── README.md
```
