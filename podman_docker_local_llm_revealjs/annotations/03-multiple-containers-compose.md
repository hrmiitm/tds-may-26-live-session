# 03 — Multiple containers and Compose annotations

## 01-why-multiple
A good container design separates services: app, database, cache, worker, LLM server. This keeps each container simple, replaceable, and debuggable. A beginner may try to put Python app + Redis + database inside one container; discourage that unless there is a very special reason.

## 02-manual-network
Manual networking is useful to understand what Compose automates. Create a network, start Redis on that network, start API on that network, and use `redis` as hostname. Compose automatically creates a project network and connects services to it.

## 03-compose-blueprint
Compose is not just “run many containers”. It is a repeatable stack definition: services, environment variables, ports, volumes, networks, healthchecks. The file becomes project documentation.

## 04-compose-commands
`up` creates and starts. `down` stops and removes Compose-created containers and networks. `down -v` also removes named volumes declared by the project. `logs -f` is the first debugging command.

## 05-depends-on
`depends_on` helps with order but is not a magic readiness guarantee. DB can start but still initialize. Robust apps retry DB/Redis connections. Healthchecks are useful, but application retries are still important.

## 06-podman-compose
Podman Compose can be provided by different implementations depending on OS and installation. Use `podman compose` when available. Use `podman-compose` if installed separately. Keep YAML mostly Compose-spec compatible to reduce surprises.

## 07-mini-lab
The included lab increments a Redis counter through FastAPI. It demonstrates a real reason for multiple containers: API process is stateless; Redis stores shared state. Ask students to run `docker compose down` and then `up` again. Counter persists if volume is kept; resets if volume is deleted.
