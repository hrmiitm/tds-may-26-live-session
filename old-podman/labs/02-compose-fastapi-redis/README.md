# Lab 02 — FastAPI + Redis with Compose

```bash
docker compose up --build
curl http://localhost:8000/count
```

Try repeatedly. The Redis counter increases.

Cleanup:

```bash
docker compose down
# delete saved Redis data too
docker compose down -v
```
