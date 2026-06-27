# Podman/Docker + Local LLM — Reveal.js Notes

## Open the slides

```bash
cd podman_docker_local_llm_revealjs
python -m http.server 8000
# open http://localhost:8000
```

Press `D` or `P` to enable live drawing annotations. Use a pen tablet, mouse, or touch screen to draw directly on slides.

## Drawing annotation controls

This version does **not** use speaker notes or separate annotation markdown files. It has a built-in drawing canvas over the slides.

| Action | Shortcut / Button |
|---|---|
| Toggle drawing mode | `D` or `P` or ✏️ |
| Toggle eraser | `E` or ⌫ |
| Undo last stroke | `Ctrl+Z` or ↶ |
| Clear current slide | `C` or 🧹 |
| Change color / size | Toolbar color and size controls |

Drawings are stored per slide in your browser localStorage, so they can remain after refresh on the same browser.

## Files

```txt
index.html                              # Reveal.js presentation shell
slides.md                               # slide content
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
