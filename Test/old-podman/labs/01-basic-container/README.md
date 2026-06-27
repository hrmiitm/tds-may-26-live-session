# Lab 01 — Basic container

```bash
docker build -t basic-fastapi .
docker run --rm -p 8000:8000 basic-fastapi
curl http://localhost:8000
```

Podman:

```bash
podman build -t basic-fastapi .
podman run --rm -p 8000:8000 basic-fastapi
```
