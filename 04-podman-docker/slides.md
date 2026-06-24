<div class="hero-center">
<div>
<div class="title-kicker">TDS • Containers</div>
<h1>Podman / Docker</h1>
<p class="big">Package apps with their runtime, run them anywhere, and connect multiple services cleanly.</p>
<p><span class="tag">image</span><span class="tag">container</span><span class="tag">volume</span><span class="tag">network</span><span class="tag">compose</span></p>
</div>
</div>

---

## Container vs VM

<div class="grid2">
<div class="card"><h3>VM</h3><p>Full guest OS + kernel. Heavier isolation. Slower startup.</p></div>
<div class="card"><h3>Container</h3><p>Process isolation using host kernel. Fast startup. Great for apps.</p></div>
</div>

<div class="flow">
  <div class="node">Your app</div><div class="arrow">+</div>
  <div class="node">Dependencies</div><div class="arrow">+</div>
  <div class="node">Runtime</div><div class="arrow">→</div>
  <div class="node">Image</div>
</div>

---

## Four words to master

<div class="grid2">
<div class="card"><h3>Image</h3><p>Read-only template: code + dependencies + start command.</p></div>
<div class="card"><h3>Container</h3><p>Running instance of an image.</p></div>
<div class="card"><h3>Volume</h3><p>Persistent storage outside the container lifecycle.</p></div>
<div class="card"><h3>Network</h3><p>Private communication between containers.</p></div>
</div>

---

## Build and run

```bash
# Docker
docker build -t tds-api .
docker run --rm -p 8000:8000 tds-api

# Podman: mostly same command shape
podman build -t tds-api .
podman run --rm -p 8000:8000 tds-api
```

<div class="callout warn">Command names differ, but the mental model is the same: build image, run container.</div>

---

## Containerfile / Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

<p class="muted">Each line creates a reproducible layer.</p>

---

## Volumes: data that survives

```bash
# named volume for database files
podman volume create appdata
podman run -v appdata:/data my-app
```

<div class="flow">
  <div class="node">Container deleted</div><div class="arrow">×</div>
  <div class="node">App process gone</div><div class="arrow">✓</div>
  <div class="node">Volume data remains</div>
</div>

---

## Networks: containers talk by name

```bash
podman network create appnet
podman run --network appnet --name api tds-api
podman run --network appnet --name redis redis:7
```

```python
# inside api container
REDIS_URL = "redis://redis:6379"
```

<div class="callout">Inside the network, service name becomes DNS name.</div>

---

## Running multiple containers manually

<div class="flow">
  <div class="node">API</div><div class="arrow">→</div>
  <div class="node">Redis</div><div class="arrow">→</div>
  <div class="node">Postgres</div>
</div>

```bash
podman run -d --name redis redis:7
podman run -d --name db -e POSTGRES_PASSWORD=pass postgres:16
podman run -d --name api -p 8000:8000 tds-api
```

<p class="muted">Works, but becomes hard to repeat.</p>

---

## Compose: one file for the stack

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      REDIS_URL: redis://redis:6379
    depends_on: [redis]

  redis:
    image: redis:7
```

```bash
docker compose up --build
podman compose up --build
```

---

## Docker vs Podman

<div class="grid2">
<div class="card"><h3>Docker</h3><p>Common in tutorials and production. Uses Docker daemon.</p></div>
<div class="card"><h3>Podman</h3><p>Daemonless, rootless-friendly, popular in Linux/server environments.</p></div>
</div>

<div class="callout">For students: learn the container concepts first. Tool choice becomes easy later.</div>

---

## Debug commands

```bash
podman ps
podman logs api
podman exec -it api bash
podman inspect api
podman stop api
podman rm api
podman image ls
```

<div class="grid2">
<div class="card"><h3>Logs</h3><p>What did the process print?</p></div>
<div class="card"><h3>Exec</h3><p>Go inside and inspect environment/files.</p></div>
</div>

---

## Practice stack

<div class="grid3">
<div class="card"><div class="number">1</div><p>Containerize FastAPI.</p></div>
<div class="card"><div class="number">2</div><p>Add Redis as second service.</p></div>
<div class="card"><div class="number">3</div><p>Use volume for persistent data.</p></div>
</div>
