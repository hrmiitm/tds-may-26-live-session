# Podman/Docker + Local LLM — Reveal.js Notes

## Open the slides

```bash
cd podman_docker_local_llm_revealjs
python -m http.server 8000
# open http://localhost:8000
```

Press `S` for Reveal.js speaker view.

## Files

```txt
index.html                              # Reveal.js presentation shell
slides.md                               # slide content
annotations/00_all_annotations.md       # complete teaching notes
annotations/01-container-fundamentals.md
annotations/02-images-containers-volumes-networks.md
annotations/03-multiple-containers-compose.md
annotations/04-local-llm-ollama-vllm.md
annotations/05-full-stack-practice.md
labs/                                   # small runnable practice projects
```

## Lab order

1. `labs/01-basic-container` — build and run a FastAPI container.
2. `labs/02-compose-fastapi-redis` — run multiple containers with Compose.
3. `labs/03-ollama-api` — call Ollama REST API and create a Modelfile.
4. `labs/04-vllm-server` — serve a model through vLLM OpenAI-compatible API.

## Official references

- Docker Compose: https://docs.docker.com/compose/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- Podman run: https://docs.podman.io/en/latest/markdown/podman-run.1.html
- Podman command docs: https://docs.podman.io/en/stable/markdown/podman.1.html
- Podman Desktop Compose tutorial: https://podman-desktop.io/tutorial/getting-started-with-compose
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- Ollama Modelfile: https://docs.ollama.com/modelfile
- Ollama importing/quantization: https://docs.ollama.com/import
- vLLM online serving: https://docs.vllm.ai/en/stable/serving/online_serving/
- vLLM OpenAI-compatible server: https://docs.vllm.ai/en/v0.21.0/serving/openai_compatible_server/
