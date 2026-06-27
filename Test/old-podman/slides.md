# Podman/Docker + Local LLM
## practical notes for containers, compose, Ollama, vLLM

<span class="pill">container fundamentals</span>
<span class="pill">multi-container apps</span>
<span class="pill">local inference</span>
<span class="pill">REST APIs</span>
<span class="pill">quantization</span>

<div class="footer-note">Annotations: annotations/00_all_annotations.md</div>

Note:
Use annotations/00_all_annotations.md as the detailed teaching script. This deck is command-first; annotations explain the mental models and common mistakes.

---

## How to use these notes

<div class="two">
<div class="card">
<h3>Slides</h3>
<p>Open <code>index.html</code> with a local server.</p>
<pre><code class="language-bash">cd podman_docker_local_llm_revealjs
python -m http.server 8000
# open http://localhost:8000</code></pre>
</div>
<div class="card">
<h3>Speaker view</h3>
<p>Press <code>S</code> in Reveal.js. Each section points to a separate annotation file.</p>
<p class="muted">Labs are inside <code>labs/</code>.</p>
</div>
</div>

Note:
Annotation: annotations/00_all_annotations.md#00-usage

---

# Part 1
## Podman / Docker fundamentals

<div class="footer-note">Annotation: annotations/01-container-fundamentals.md</div>

---

## Container vs VM

<div class="two">
<div class="card">
<h3>VM</h3>
<ul>
<li>Full guest OS</li>
<li>Heavier boot</li>
<li>Strong isolation boundary</li>
<li>Great for running different OS kernels</li>
</ul>
</div>
<div class="card">
<h3>Container</h3>
<ul>
<li>Process isolation</li>
<li>Shares host kernel</li>
<li>Fast startup</li>
<li>Great for packaging apps + dependencies</li>
</ul>
</div>
</div>

<pre class="mermaid">
flowchart LR
  VM[VM: app + libs + guest OS] --> Hypervisor --> HostOS[Host OS + kernel]
  C[Container: app + libs] --> Runtime[container runtime] --> HostOS
</pre>

Note:
Annotation: annotations/01-container-fundamentals.md#01-container-vs-vm

---

## The core mental model

> An image is a recipe. A container is a running copy of that recipe.

<pre class="mermaid">
flowchart LR
  Dockerfile[Dockerfile] --> Build[docker build]
  Build --> Image[Image layers]
  Image --> Run[docker run]
  Run --> Container[Running container]
  Container --> Logs[docker logs]
  Container --> Exec[docker exec]
</pre>

<span class="pill">Dockerfile</span> <span class="pill">image</span> <span class="pill">container</span> <span class="pill">registry</span> <span class="pill">runtime</span>

Note:
Annotation: annotations/01-container-fundamentals.md#02-core-model

---

## Why containers matter for developers

<div class="three">
<div class="card"><h3>Same environment</h3><p>Run app with exact Python, Node, CUDA, system libraries.</p></div>
<div class="card"><h3>Fast cleanup</h3><p>Delete container without breaking your laptop.</p></div>
<div class="card"><h3>Deployable artifact</h3><p>The image is the unit you can ship to a server.</p></div>
</div>

```bash
# the old problem
"it works on my machine"

# the container solution
"it works in this image"
```

Note:
Annotation: annotations/01-container-fundamentals.md#03-why-containers

---

## Docker and Podman: same idea, different engine

| Topic | Docker | Podman |
|---|---|---|
| CLI | `docker ...` | `podman ...` |
| Daemon | Docker daemon | daemonless design |
| Rootless | supported | first-class focus |
| Pods | not native concept | native pod concept |
| Compose | Docker Compose | `podman compose` / `podman-compose` depending setup |

```bash
# many simple commands map directly
docker run nginx
podman run nginx
```

Note:
Annotation: annotations/01-container-fundamentals.md#04-docker-vs-podman

---

## First container: hello world

```bash
# Docker
docker run --rm hello-world

# Podman
podman run --rm hello-world
```

What happened?

1. CLI searched local images.
2. Image was not present, so it pulled from registry.
3. Runtime created a container.
4. Process ran, printed output, exited.
5. `--rm` removed the stopped container.

Note:
Annotation: annotations/01-container-fundamentals.md#05-first-container

---

## Useful lifecycle commands

```bash
# list running containers
docker ps
podman ps

# list all containers, including stopped
docker ps -a
podman ps -a

# stop / remove
docker stop my-web
docker rm my-web

# inspect logs and enter shell
docker logs my-web
docker exec -it my-web sh
```

<span class="warn">Rule:</span> a container normally lives as long as its main process lives.

Note:
Annotation: annotations/01-container-fundamentals.md#06-lifecycle

---

# Part 2
## images, containers, volumes, networks

<div class="footer-note">Annotation: annotations/02-images-containers-volumes-networks.md</div>

---

## Image layers

<pre class="mermaid">
flowchart TB
  L4[app code layer] --> L3[dependencies layer]
  L3 --> L2[system packages layer]
  L2 --> L1[base image: python:3.12-slim]
</pre>

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

<span class="pill">Put slow-changing layers first</span>
<span class="pill">Put app code later</span>

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#01-image-layers

---

## Build, tag, run

```bash
# Build image from current folder
docker build -t my-fastapi:dev .

# Run as container
docker run --rm -p 8000:8000 my-fastapi:dev

# Same idea with Podman
podman build -t my-fastapi:dev .
podman run --rm -p 8000:8000 my-fastapi:dev
```

Port mapping:

```txt
host:container
8000:8000
```

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#02-build-tag-run

---

## Container filesystem is temporary

```bash
# run container and create file inside it
docker run --name tempbox -it alpine sh
/ # echo hello > /data.txt
/ # exit

# remove container: file disappears
docker rm tempbox
```

If data matters, use a volume or bind mount.

<span class="bad">Do not store database state only inside a disposable container layer.</span>

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#03-ephemeral-fs

---

## Volumes vs bind mounts

<div class="two">
<div class="card">
<h3>Named volume</h3>
<pre><code class="language-bash">docker volume create pgdata
docker run -v pgdata:/var/lib/postgresql/data postgres</code></pre>
<p>Best for database state managed by runtime.</p>
</div>
<div class="card">
<h3>Bind mount</h3>
<pre><code class="language-bash">docker run -v "$PWD":/app python:3.12</code></pre>
<p>Best for local development files.</p>
</div>
</div>

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#04-volumes-bind-mounts

---

## Network mental model

<pre class="mermaid">
flowchart LR
  Browser[Your browser] -- localhost:8000 --> HostPort[Host port]
  HostPort -- 8000 --> API[api container]
  API -- redis:6379 --> Redis[redis container]
  API -- ollama:11434 --> Ollama[ollama container]
</pre>

Inside the same Compose network, containers call each other by service name.

```txt
api calls redis:6379
api calls ollama:11434
browser calls localhost:8000
```

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#05-networking

---

## Port publishing is not container networking

```bash
# publish container port 80 to host port 8080
docker run --rm -p 8080:80 nginx

# browser on host
http://localhost:8080
```

Key distinction:

| Access path | Use |
|---|---|
| `localhost:8080` | host → container |
| `service-name:port` | container → container |

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#06-port-publishing

---

## Clean up safely

```bash
# remove stopped containers
docker container prune

# remove unused images
docker image prune

# remove unused volumes only when you know data is not needed
docker volume prune

# check disk usage
docker system df
```

<span class="warn">Volume prune can delete database data.</span>

Note:
Annotation: annotations/02-images-containers-volumes-networks.md#07-cleanup

---

# Part 3
## running multiple containers + Compose

<div class="footer-note">Annotation: annotations/03-multiple-containers-compose.md</div>

---

## Why multiple containers?

One container should usually run one main service.

<pre class="mermaid">
flowchart LR
  User --> Web[frontend]
  Web --> API[backend]
  API --> DB[(database)]
  API --> Cache[(Redis cache)]
  API --> LLM[Ollama / vLLM]
</pre>

Instead of manually starting 5 containers, declare the stack once.

Note:
Annotation: annotations/03-multiple-containers-compose.md#01-why-multiple

---

## Manual multi-container run

```bash
# 1. create network
docker network create demo-net

# 2. start redis
docker run -d --name redis --network demo-net redis:7-alpine

# 3. start app on same network
docker run -d --name api --network demo-net -p 8000:8000 my-api

# api can connect to redis://redis:6379
```

Works, but becomes painful for real projects.

Note:
Annotation: annotations/03-multiple-containers-compose.md#02-manual-network

---

## Compose file = stack blueprint

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

```bash
docker compose up --build
```

Note:
Annotation: annotations/03-multiple-containers-compose.md#03-compose-blueprint

---

## Compose commands you will use daily

```bash
# start in foreground
docker compose up --build

# start in background
docker compose up -d --build

# see containers
docker compose ps

# logs for all or one service
docker compose logs -f
docker compose logs -f api

# stop and remove stack containers/network
docker compose down

# also delete named volumes
docker compose down -v
```

Note:
Annotation: annotations/03-multiple-containers-compose.md#04-compose-commands

---

## `depends_on` is not health

```yaml
services:
  api:
    depends_on:
      - db
  db:
    image: postgres:16
```

`depends_on` starts `db` before `api`, but does not always mean DB is ready to accept connections.

Better pattern: retry connections in your app or add healthchecks.

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 5s
  timeout: 3s
  retries: 10
```

Note:
Annotation: annotations/03-multiple-containers-compose.md#05-depends-on

---

## Podman Compose options

Use whichever your machine supports:

```bash
# often works on modern Podman setups
podman compose up --build

# common external tool
podman-compose up --build

# Docker-compatible CLI style
podman ps
podman logs container_name
```

Podman is especially useful when you want rootless containers and daemonless operation.

Note:
Annotation: annotations/03-multiple-containers-compose.md#06-podman-compose

---

## Mini lab: FastAPI + Redis

Files included:

```txt
labs/02-compose-fastapi-redis/
├── app.py
├── Dockerfile
├── requirements.txt
└── compose.yaml
```

Run:

```bash
cd labs/02-compose-fastapi-redis
docker compose up --build
# or: podman compose up --build
```

Test:

```bash
curl http://localhost:8000/count
```

Note:
Annotation: annotations/03-multiple-containers-compose.md#07-mini-lab

---

# Part 4
## Local LLM: Ollama + vLLM

<div class="footer-note">Annotation: annotations/04-local-llm-ollama-vllm.md</div>

---

## Local LLM mental model

<pre class="mermaid">
flowchart LR
  App[Your app] --> API[Local inference server]
  API --> Runtime[Ollama or vLLM]
  Runtime --> Model[Model weights]
  Runtime --> GPU[GPU/CPU memory]
</pre>

You are not just “installing a chatbot”. You are running an inference server.

<span class="pill">model weights</span>
<span class="pill">context window</span>
<span class="pill">sampling parameters</span>
<span class="pill">GPU memory</span>

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#01-local-llm-model

---

## Ollama vs vLLM

| Tool | Best for | Style |
|---|---|---|
| Ollama | easy local use, laptop demos, quick REST API | simple model pull/run/create |
| vLLM | high-throughput serving, OpenAI-compatible API, GPU servers | production-style inference server |

```bash
# Ollama style
ollama run llama3.2

# vLLM style
vllm serve meta-llama/Llama-3.1-8B-Instruct --dtype auto
```

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#02-ollama-vs-vllm

---

## Running an Ollama model

```bash
# install from official website first, then:
ollama pull llama3.2
ollama run llama3.2

# list local models
ollama list

# show model details
ollama show llama3.2
```

Small models are better for weak laptops. Larger models need more RAM/VRAM.

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#03-running-ollama

---

## Important generation parameters

| Parameter | Meaning | Effect |
|---|---|---|
| `temperature` | randomness | lower = more deterministic |
| `top_p` | nucleus sampling | lower = safer/narrower choices |
| `num_ctx` | context length | larger = more memory |
| `num_predict` | max generated tokens | controls answer length |
| `stop` | stop strings | useful for templates |

```bash
ollama run llama3.2
/set parameter temperature 0.2
/set parameter num_ctx 4096
```

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#04-parameters

---

## Ollama REST API: generate

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Explain containers in 3 lines",
    "stream": false,
    "options": {
      "temperature": 0.2,
      "num_predict": 120
    }
  }'
```

Use REST API when connecting your app, bot, or RAG system to local models.

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#05-generate-api

---

## Ollama REST API: chat

```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "llama3.2",
    "stream": false,
    "messages": [
      {"role": "system", "content": "You are a concise tutor."},
      {"role": "user", "content": "What is Docker Compose?"}
    ]
  }'
```

`/api/chat` is better for multi-turn conversations.

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#06-chat-api

---

## Modelfile = custom local model wrapper

```Dockerfile
FROM llama3.2

SYSTEM """
You are a practical DevOps tutor.
Explain with commands first and short reasoning after.
"""

PARAMETER temperature 0.2
PARAMETER num_ctx 4096
PARAMETER num_predict 300
```

```bash
ollama create devops-tutor -f Modelfile
ollama run devops-tutor
```

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#07-modelfile

---

## What quantization does

> Quantization stores model weights with fewer bits.

<div class="three">
<div class="card"><h3>FP16</h3><p>higher quality, bigger memory</p></div>
<div class="card"><h3>8-bit</h3><p>good middle ground</p></div>
<div class="card"><h3>4-bit</h3><p>smaller, faster, more quality loss risk</p></div>
</div>

<pre class="mermaid">
flowchart LR
  Big[FP16 weights] --> Quant[quantization]
  Quant --> Small[smaller weights]
  Small --> LessMemory[less RAM/VRAM]
  Small --> Tradeoff[possible quality drop]
</pre>

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#08-quantization

---

## Choosing quantized models

Use this decision rule:

```txt
Not enough RAM/VRAM? choose smaller model or stronger quantization.
Bad answer quality? try larger model or weaker quantization.
Need speed? smaller/quantized often helps.
Need reasoning quality? model quality matters more than size alone.
```

Practical starting points:

| Machine | Start with |
|---|---|
| CPU-only / low RAM | 1B–3B quantized |
| 8 GB VRAM | 7B–8B quantized |
| 16+ GB VRAM | 8B–14B, maybe less aggressive quantization |

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#09-choosing-quantized

---

## vLLM server: OpenAI-compatible local endpoint

```bash
pip install vllm

vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype auto \
  --api-key local-token
```

Call it like OpenAI API:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer local-token" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta-llama/Llama-3.1-8B-Instruct", "messages":[{"role":"user","content":"hi"}]}'
```

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#10-vllm-server

---

## Ollama API vs vLLM API

| Feature | Ollama | vLLM |
|---|---|---|
| Setup | easiest | more server/GPU oriented |
| API style | Ollama native endpoints | OpenAI-compatible endpoints |
| Custom wrapper | Modelfile | server flags / HF model config |
| Throughput | good for local use | optimized for serving many requests |

Choose Ollama for teaching and fast demos. Choose vLLM when you want a serious inference server.

Note:
Annotation: annotations/04-local-llm-ollama-vllm.md#11-api-comparison

---

# Part 5
## full-stack local LLM pattern

<div class="footer-note">Annotation: annotations/05-full-stack-practice.md</div>

---

## Pattern: app + database/cache + LLM

<pre class="mermaid">
flowchart LR
  User[User browser] --> API[FastAPI]
  API --> Cache[(Redis)]
  API --> LLM[Ollama / vLLM]
  API --> Logs[logs]
</pre>

Compose lets you run this whole local stack as one project.

```bash
docker compose up --build
```

Note:
Annotation: annotations/05-full-stack-practice.md#01-full-stack-pattern

---

## Compose with Ollama service

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama

  api:
    build: .
    environment:
      OLLAMA_BASE_URL: http://ollama:11434
    ports:
      - "8000:8000"
    depends_on:
      - ollama

volumes:
  ollama_models:
```

Note:
Annotation: annotations/05-full-stack-practice.md#02-compose-ollama

---

## Python call to Ollama

```python
import requests

base_url = "http://localhost:11434"

payload = {
    "model": "llama3.2",
    "prompt": "Explain Docker volumes briefly.",
    "stream": False,
    "options": {"temperature": 0.2}
}

response = requests.post(f"{base_url}/api/generate", json=payload, timeout=120)
response.raise_for_status()
print(response.json()["response"])
```

Note:
Annotation: annotations/05-full-stack-practice.md#03-python-ollama

---

## Debugging checklist

```bash
# container status
docker compose ps

# logs
docker compose logs -f api
docker compose logs -f ollama

# enter container
docker compose exec api sh

# test network inside api container
curl http://ollama:11434/api/tags

# inspect image/container/network
docker inspect container_name
```

Debug one layer at a time: process → port → network → environment → volume.

Note:
Annotation: annotations/05-full-stack-practice.md#04-debugging

---

## Common mistakes

<div class="two">
<div class="card">
<h3 class="bad">Wrong</h3>
<pre><code class="language-python"># inside api container
OLLAMA_BASE_URL = "http://localhost:11434"</code></pre>
<p><code>localhost</code> means the API container itself.</p>
</div>
<div class="card">
<h3 class="ok">Right</h3>
<pre><code class="language-python"># service name in Compose network
OLLAMA_BASE_URL = "http://ollama:11434"</code></pre>
<p>Use service name for container-to-container calls.</p>
</div>
</div>

Note:
Annotation: annotations/05-full-stack-practice.md#05-common-mistakes

---

## Practice questions

1. Explain image vs container with one command each.
2. Why does database data disappear after removing a container?
3. When should you use bind mount vs named volume?
4. Why does `localhost` fail between containers?
5. Convert a `docker run` command into Compose YAML.
6. What changes when you increase `temperature`?
7. Why does quantization reduce memory?
8. When would you choose vLLM instead of Ollama?

Note:
Annotation: annotations/05-full-stack-practice.md#06-practice-questions

---

## Final memory map

<pre class="mermaid">
flowchart TD
  C[Containers] --> I[Images]
  C --> V[Volumes]
  C --> N[Networks]
  C --> M[Multiple services]
  M --> Compose[Compose YAML]
  Compose --> Stack[App stack]
  Stack --> LLM[Local LLM]
  LLM --> Ollama[Ollama]
  LLM --> VLLM[vLLM]
  Ollama --> API[REST API]
  Ollama --> MF[Modelfile]
  VLLM --> OAI[OpenAI-compatible API]
  LLM --> Q[Quantization]
</pre>

Note:
Annotation: annotations/00_all_annotations.md#final-memory-map

---

## References to read next

- Docker Docs: Compose, volumes, networking
- Podman Docs: run, rootless, compose workflows
- Ollama Docs: API, Modelfile, importing/quantizing models
- vLLM Docs: online serving, OpenAI-compatible server

<div class="footer-note">See README.md for source links and lab commands.</div>

