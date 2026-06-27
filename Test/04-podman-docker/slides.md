<div class="titlemark">TDS Infrastructure • Topic 4</div>

# Podman / Docker

Images, containers, volumes, networks, multi-container apps and Compose.

<span class="pill">Container</span><span class="pill">Image</span><span class="pill">Volume</span><span class="pill">Network</span><span class="pill">Compose</span>

---

## Container vs VM

<div class="split">
<div class="card"><h3>VM</h3><p class="small">Full guest OS, heavier isolation, slower startup.</p></div>
<div class="card"><h3>Container</h3><p class="small">Shares host kernel, packages app + dependencies, fast startup.</p></div>
</div>

---

## The container mental model

<div class="flow">
  <span class="box">Dockerfile</span><span class="arrow">→</span>
  <span class="box">Image</span><span class="arrow">→</span>
  <span class="box">Container</span><span class="arrow">→</span>
  <span class="box">Logs / Ports / Volumes</span>
</div>

---

## Image vs container

```text
Image      = read-only template
Container  = running instance of image
Volume     = persistent data outside container
Network    = private communication between containers
```

```bash
docker images
docker ps
docker ps -a
```

---

## First run

```bash
docker run --rm hello-world
podman run --rm hello-world
```

<p class="small">Podman commands are mostly Docker-compatible. In many cases, replace <code>docker</code> with <code>podman</code>.</p>

---

## Container lifecycle

```bash
docker run -d --name web nginx

docker logs web
docker exec -it web sh
docker stop web
docker rm web
```

---

## Port mapping

<div class="flow">
  <span class="box">Host port 8080</span><span class="arrow">→</span>
  <span class="box">Container port 80</span>
</div>

```bash
docker run --rm -p 8080:80 nginx
```

<p class="small">Open: <code>http://localhost:8080</code></p>

---

## Volumes: keep data

```bash
docker volume create pgdata

docker run -d --name db \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

> Containers are disposable. Data should live in volumes.

---

## Networks: containers talk by name

```bash
docker network create appnet

docker run -d --name redis --network appnet redis

docker run --rm --network appnet redis redis-cli -h redis ping
```

<p class="small">Inside same network, service name becomes hostname.</p>

---

## Dockerfile for FastAPI

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN pip install uv && uv sync --frozen || uv sync
COPY . .
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Build and run your app

```bash
docker build -t fastapi-demo .
docker run --rm -p 8000:8000 fastapi-demo
```

<div class="card">
<p class="small"><b>Build</b> creates image. <b>Run</b> starts container from image.</p>
</div>

---

## Multiple containers manually

```bash
docker network create demo

docker run -d --name redis --network demo redis

docker run -d --name api --network demo -p 8000:8000 \
  -e REDIS_URL=redis://redis:6379 \
  fastapi-demo
```

---

## Compose: one file, whole system

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7
```

```bash
docker compose up --build
```

---

## Compose adds defaults

<div class="three">
<div class="card"><b>Network</b><p class="small">Created automatically</p></div>
<div class="card"><b>DNS</b><p class="small">Service names resolve</p></div>
<div class="card"><b>Logs</b><p class="small">View all containers together</p></div>
</div>

---

## Clean up

```bash
docker compose down

docker stop web
docker rm web
docker rmi fastapi-demo
docker volume ls
```

<p class="small">Be careful: removing volumes can delete real data.</p>

---

## Practice

1. Containerize a FastAPI app.
2. Run Redis with the app using Compose.
3. Store app logs on a mounted volume.
4. Explain image, container, volume, network using one command each.

---

# Mental model

**Image is the recipe. Container is the running app. Volume stores data. Network connects services. Compose runs the system.**
