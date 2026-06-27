# Install on Ubuntu

```bash
sudo apt update
sudo apt install -y podman

podman --version
podman info
```

1) Tokenization (space)
- sudo
- apt
- update
2) Execute first token as executable
- sudo ---> search in PATH variable
3) Remaining tokens passed as arguments
4) sudo takes over excute --> with priviledge 



# Image Handling

`ghcr.io and docker.io` are container registries, which are secure online storage servers used to `host, share, and download` Docker container images.

```bash
# Pull image --> Remote to Local
podman pull docker.io/alpine/ollama:0.30.10

# List local images
podman images

# Remove image
podman rmi docker.io/alpine/ollama:0.30.10

# Force remove image
podman rmi -f IMAGE_ID

```

# Lifecycle of an Container (from Outside)

```bash
podman run docker.io/alpine/ollama:0.30.10 # run in foreground 
podman run -d docker.io/alpine/ollama:0.30.10 # run in background -- always -d detach used

podman ps       # process status: running containers
podman ps -a    # all process status: stopped/running containers

podman stop <container name or id> # To Stop Running Containers
podman start <container name or id>
podman restart <container name or id>
podman rm <container name or id> # To Remove Stopped Containers
```

# Inside Container (let's come inside Container)
```bash
podman run -d -p 11000:11434 --name myai docker.io/ollama/ollama

# Logs
podman logs myai # View logs
podman logs --tail 50 myai
podman logs -f myai # Follow logs live


# Enter container shell
podman exec -it myai sh # sh/bash/zsh/.........


podman exec myai ollama ls # Run one command inside container
podman inspect myai # Inspect full metadata
podman top myai # See processes inside container
```

# Modelfile

```
cat > Modelfile <<'EOF'
FROM gemma3:270m

PARAMETER temperature 0.2
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER num_predict 150
PARAMETER num_ctx 2048

SYSTEM """
You will answer in bullet points in brief.
"""
EOF
```

```bash
podman exec -it myai ollama create tds-gemma -f /Modelfile
```

### Parament meaning
-
-
- 