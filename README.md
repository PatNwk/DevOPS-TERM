# TP Docker Compose - Stack Hybride

## Objectif

Ce projet repond au TP d'orchestration d'une stack hybride avec Docker Compose.

La stack contient 5 services :

- `db_mongo`
- `db_mysql`
- `admin_mongo`
- `admin_mysql`
- `api`

L'API expose :

- `GET /posts` depuis MongoDB
- `GET /users` depuis MySQL

## Fichiers utiles

- `docker-compose.yml`
- `api/app/main.py`
- `api/Dockerfile`
- `mongo/Dockerfile`
- `mongo/init.js`
- `sqlfiles/`
- `.env.example`

## Demarrage

Copier `.env.example` en `.env`, puis lancer :

```bash
docker compose up -d --build
```

Si tu veux rejouer toute l'initialisation des bases :

```bash
docker compose down -v --remove-orphans
docker compose up -d --build
```

## Ce que fait la stack

- MongoDB est initialise avec `5` posts
- MySQL est initialise avec `4` utilisateurs
- `mongo-express` permet de consulter MongoDB
- `Adminer` permet de consulter MySQL
- des healthchecks verifient les bases, les interfaces web et l'API

## Verification

Verifier les conteneurs :

```bash
docker compose ps
```

Etat attendu :

- `db_mongo` : `healthy`
- `db_mysql` : `healthy`
- `admin_mongo` : `healthy`
- `admin_mysql` : `healthy`
- `api` : `healthy`

Verifier l'API :

```bash
curl http://localhost:8000/posts
curl http://localhost:8000/users
```

Resultat attendu :

- `/posts` retourne `5` posts
- `/users` retourne `4` utilisateurs

## Acces

- API : `http://localhost:8000`
- Posts : `http://localhost:8000/posts`
- Users : `http://localhost:8000/users`
- Adminer : `http://localhost:8080`
- Mongo Express : `http://localhost:8081`

## Connexion Adminer

- Systeme : `MySQL`
- Serveur : `db_mysql`
- Utilisateur : `root`
- Mot de passe : valeur de `MYSQL_ROOT_PASSWORD` dans `.env`
- Base : `ynov_ci`

## Points importants pour le TP

- les bases ne sont pas exposees directement
- les donnees sont persistantes via volumes Docker
- les scripts d'initialisation ne se rejouent que sur des volumes vides
- les variables sensibles sont dans `.env`
- un `.env.example` est fourni pour le rendu
