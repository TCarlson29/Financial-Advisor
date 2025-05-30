# Financial‑Advisor

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Linux containers)
- Docker Compose (included with Docker Desktop)

---

## Quick Start with Docker

From the **project root** (where this README.md lives), run:

```bash
docker-compose up --build
```

- The **backend** (FastAPI + SQLAlchemy) will be available on port **8000**.
- The **frontend** (Vue) will be available on port **5173**.

Open your browser and navigate to:

> http://localhost:5173

---

## Stopping the App

To stop and remove containers, networks, and volumes:

```bash
docker-compose down
```

---

## Updating the App

After updating, run the docker-compose down and up --build, and navigate to exactly http://localhost:5173 so that the buttons can call on the API methods correctly in order

```bash
docker-compose down
docker-compose up --build
http://localhost:5173 
```
