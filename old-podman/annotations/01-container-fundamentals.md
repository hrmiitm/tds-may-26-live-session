# 01 — Container fundamentals annotations

## 01-container-vs-vm
Start by removing fear: a container is not a tiny full computer. It is a normal process with isolation around filesystem, networking, users, and process tree. A VM brings its own guest OS kernel; a container shares the host kernel. This is why containers start fast and are lighter, but also why Linux containers need a Linux kernel underneath. On Windows/macOS, Docker Desktop often uses a lightweight Linux VM behind the scenes.

Teaching line: “VM virtualizes hardware; container virtualizes the application environment.”

## 02-core-model
Use the recipe analogy. Dockerfile is the recipe. Image is the cooked but frozen package. Container is a live plate served from that package. A single image can create many containers. Deleting a container does not delete the image. Updating code usually requires rebuilding the image unless you are using a bind mount in development.

## 03-why-containers
Connect this to student pain: package version conflicts, Python environment errors, different OS, missing system libraries. Containers solve “environment repeatability”. They do not automatically solve bad code, secret management, scaling, or security.

## 04-docker-vs-podman
Docker and Podman use similar CLI patterns, so students should learn the concepts, not memorize two separate worlds. Docker uses a daemon model. Podman is daemonless and has strong rootless support. In many labs, replace `docker` with `podman` and it works. Compose support can vary by installation, so always test with `podman compose version` or `podman-compose version`.

## 05-first-container
Important sequence: local image check → pull → create container → run main command → exit → remove if `--rm`. Explain why `hello-world` stops immediately: its only job is to print text and exit.

## 06-lifecycle
The main container process controls the lifecycle. If the main process exits, the container exits. A web server keeps running because the server process stays alive. A script container stops after the script finishes. `docker exec` enters a running container; it cannot enter a stopped one.
