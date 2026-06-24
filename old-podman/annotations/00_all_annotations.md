# Complete speaker annotations — Podman/Docker + Local LLM

Use this file as the full teaching script. The shorter section files contain the same ideas split by topic.

## 00-usage
Run a local server before opening the deck because Reveal.js loads `slides.md` through the browser. Direct file opening may be blocked by browser security.

```bash
cd podman_docker_local_llm_revealjs
python -m http.server 8000
# open http://localhost:8000
```

Press `S` for speaker view. Keep this annotations file open separately.

## 01-container-vs-vm
A VM virtualizes hardware and usually runs a full guest OS. A container isolates a process and its environment while sharing the host kernel. Containers are fast because they do not boot a whole OS for each app. But because they share the kernel, Linux containers need a Linux kernel somewhere. Docker Desktop on Windows/macOS solves this using a lightweight Linux VM underneath.

## 02-core-model
Dockerfile is the recipe. Image is the built artifact. Container is a running instance. Registry is where images are pushed and pulled. Runtime is what starts and isolates containers. This model explains almost every beginner confusion.

## 03-why-containers
Containers package app code with dependencies and system libraries. They reduce environment mismatch and make deployment reproducible. They are not magic security, scaling, or architecture solutions.

## 04-docker-vs-podman
Docker and Podman have similar CLI commands. Docker traditionally uses a daemon. Podman is daemonless and strong for rootless containers. Podman also has pods as a native concept. Compose support depends on installation: `podman compose` or `podman-compose`.

## 05-first-container
`run --rm hello-world` pulls if needed, creates a container, runs its command, prints output, exits, and removes the stopped container. `--rm` is best for temporary experiments.

## 06-lifecycle
A running container is tied to its main process. When the main process ends, the container stops. Use `logs` to inspect output and `exec` to enter a running container.

## 07-image-layers
Images are layered and cached. Put slow-changing steps first. Copy dependency files before application files. This makes rebuilds faster.

## 08-filesystem-and-volumes
The container writable layer is temporary. Use named volumes for persistent runtime data like DB state. Use bind mounts for live development files.

## 09-networking
A Compose project creates a network. Service names become DNS names. Host-to-container uses published ports. Container-to-container uses service names.

## 10-compose
Compose defines services, ports, volumes, networks, env variables, and healthchecks in YAML. It turns a set of manual commands into a repeatable stack.

## 11-depends-on
`depends_on` controls startup order. It does not guarantee that a service is ready. Add app retries and healthchecks.

## 12-local-llm
A local LLM application needs model weights, an inference runtime, and an API/app layer. Ollama is easier for local demos. vLLM is more serving-focused and supports OpenAI-compatible endpoints.

## 13-ollama-api
Use `/api/generate` for single prompts and `/api/chat` for role-based conversations. Set `stream: false` for easy demos. Use options such as `temperature`, `num_ctx`, and `num_predict` to control behavior.

## 14-modelfile
A Modelfile is reusable model configuration. It can set base model, system prompt, parameters, template, adapters, and license metadata. It is not fine-tuning.

## 15-quantization
Quantization stores weights with fewer bits, reducing memory and often improving speed. The tradeoff is possible quality loss. Use stronger quantization only when necessary for hardware constraints.

## 16-vllm
vLLM is useful when you want higher-throughput serving and OpenAI-compatible APIs. Most OpenAI SDK-style apps can target a vLLM server by changing base URL, model, and API key.

## 17-full-stack-pattern
A practical local AI stack might include FastAPI, Redis, Ollama/vLLM, and a database/vector DB. Compose makes this reproducible. Remember that inside the API container, `localhost` is the API container, not the Ollama container. Use `http://ollama:11434`.

## final-memory-map
Containers give repeatable app environments. Images create containers. Volumes persist data. Networks connect containers. Compose declares multi-service stacks. Local LLM tools run model weights as an inference service. Ollama is easy; vLLM is stronger for scalable serving. Quantization is the memory/speed/quality tradeoff.
