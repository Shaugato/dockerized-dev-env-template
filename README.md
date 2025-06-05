# Dockerized Dev Environment Template

> **TL;DR**  
> A minimal, ready-to-use Docker Compose template with a Flask web app, PostgreSQL, Adminer GUI, and Nginx reverse proxy. Includes a CI workflow to validate builds.

---

## 📖 What This Is

Setting up a local dev environment with multiple services can be error-prone and inconsistent. This template provides:

- A **Flask** web application (Python 3.9)  
- A **PostgreSQL** database (v13) with initial seed SQL  
- **Adminer** (lightweight DB GUI) for quick table browsing  
- An **Nginx** reverse proxy (routes `/` → Flask, `/adminer` → Adminer)  
- A single `docker-compose.yml` to orchestrate everything  
- A **GitHub Actions** workflow that builds and tests the Docker images  
- A clean `.env.example` for easy environment configuration  

---

## 🔧 Prerequisites

- [Docker 20.10+](https://docs.docker.com/get-docker/)  
- [Docker Compose 1.27+](https://docs.docker.com/compose/install/)  
- git (to clone this repo)  

---

## 🚀 Quick Start

1. **Clone this repo**  
   ```bash
   git clone https://github.com/yourusername/dockerized-dev-env-template.git
   cd dockerized-dev-env-template
````

2. **Copy `.env.example` to `.env`**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and customize `POSTGRES_PASSWORD` (and any other vars) as needed.

3. **Build & spin up containers**

   ```bash
   docker-compose up --build
   ```

   * **Flask app** → [http://localhost](http://localhost)
   * **Adminer GUI** → [http://localhost/adminer](http://localhost/adminer)
   * (Nginx listens on port 80)

4. **Verify**

   * Visit `http://localhost/health` → should return `{"status":"OK"}`
   * Visit `http://localhost/users` → should list seeded users (e.g., Alice, Bob)

   **Adminer**:

   * System: PostgreSQL
   * Server: db
   * Username/Password: from your `.env`
   * Database: `devdb`

---

## 🛠 How to Connect

* **Flask**

  * Default port: 5000 (exposed via Nginx → port 80).
  * DB connection reads from `DATABASE_URL` in `.env`.

* **PostgreSQL**

  * Host: `db` (Docker network)
  * Port: 5432
  * Credentials: look in `.env`

* **Adminer (DB GUI)**

  * URL: [http://localhost/adminer](http://localhost/adminer)
  * System: PostgreSQL
  * Server: `db`
  * Username/Password: from `.env`
  * Database: `devdb`

---

## 📦 How to Extend

Want to add Redis, MongoDB, or anything else? Just:

1. Add a new service block in `docker-compose.yml`.
2. Expose necessary ports and define environment variables.
3. Link the new service onto the `devnet` (shared network).
4. Adjust your application code (or add another container) to consume the new service.

For example, to add Redis:

```yaml
services:
  redis:
    image: redis:6-alpine
    container_name: dev-redis
    ports:
      - "6379:6379"
    networks:
      - devnet
```
