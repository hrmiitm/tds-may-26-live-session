# 02 — Images, containers, volumes, networks annotations

## 01-image-layers
Docker builds images in layers. Layers are cached. If `requirements.txt` has not changed, the dependency installation layer can be reused. This is why we copy requirements before copying the full app. If you copy the full app first, every code edit invalidates the dependency install layer.

## 02-build-tag-run
`-t my-fastapi:dev` gives a human-friendly name and tag. Without a tag, Docker stores the image with an ID only. `-p 8000:8000` maps host port to container port. First number is host, second is container. Students often reverse this.

## 03-ephemeral-fs
A container has a writable layer, but that layer belongs to that container. When the container is removed, that layer is removed. Databases, uploaded files, model cache, and logs should not rely only on the container layer.

## 04-volumes-bind-mounts
Named volume: runtime-managed persistent storage, usually best for database and model cache. Bind mount: maps a host folder into the container, best for development because code edits on host appear inside container. Warning: bind mounts can accidentally overwrite files inside the image path.

## 05-networking
Inside a Compose network, service names become DNS names. `redis` means the Redis service. `ollama` means the Ollama service. `localhost` inside a container means that same container, not your laptop and not another container.

## 06-port-publishing
Port publishing exposes a container service to the host. It is not needed for every internal service. For example, the API may need `8000:8000` so your browser can reach it, but Redis may not need a published port if only API uses it internally.

## 07-cleanup
Teach cleanup carefully. `docker system prune` feels useful but can delete important unused resources. `volume prune` is the dangerous one because it can delete database data. Make students run `docker system df` before cleanup.
