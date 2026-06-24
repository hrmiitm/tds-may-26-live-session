# 05 — Full-stack local LLM practice annotations

## 01-full-stack-pattern
A practical local AI app has at least two moving parts: app server and inference server. Add Redis for cache, vector DB for RAG, and database for user state. Compose is ideal for local development because every service can be started with one command.

## 02-compose-ollama
The Ollama volume stores downloaded models. Without the volume, model downloads may disappear when the container is removed. If running on GPU, Docker/Podman GPU setup needs extra host configuration; keep the first lab CPU-safe.

## 03-python-ollama
In Python, keep base URL in environment variables. Use `response.raise_for_status()` to catch HTTP errors. Use `timeout=120` because local inference can take time. In an API server, avoid blocking too many requests at once unless you control concurrency.

## 04-debugging
Debug systematically. Is the container running? Are logs clean? Is the process listening on the expected port? Can the API container curl the LLM service by service name? Is the model pulled? Is memory enough? This layered approach prevents random guessing.

## 05-common-mistakes
The biggest Compose networking mistake is `localhost`. Inside a container, localhost is the container itself. For container-to-container calls, use service names like `redis`, `db`, `ollama`, or `vllm`.

## 06-practice-questions
Use these questions as oral revision. The goal is not memorizing commands; the goal is being able to reason from first principles.
