<!-- .slide: class="title-slide" -->
<div class="hero">
  <div>
    <div class="kicker">Podman + Ollama</div>
    <h1>Containers for Local AI</h1>
    <p class="subtitle">A practical teaching deck: understand containers, images, registries, Podman commands, Ollama, Modelfile parameters, and REST API calls.</p>
    <p><span class="pill">containers</span><span class="pill green">images</span><span class="pill violet">Podman</span><span class="pill amber">Ollama</span><span class="pill red">REST API</span></p>
  </div>
  <div class="card">
    <div class="big-number">Goal</div>
    <p class="quote">By the end, you can run a local LLM as a service, tune it, and call it from code.</p>
    <p class="note">Keep this deck open while teaching. Press <strong>P</strong> for pen, <strong>L</strong> for laser, <strong>F</strong> for fullscreen.</p>
  </div>
</div>

---

<div>
  <div class="kicker">Big Picture</div>
  <h2>Why Containers Matter</h2>
  <div class="flow">
    <div class="step"><h3>Problem</h3><p>“It works on my machine” because OS, libraries, and versions differ.</p></div>
    <div class="step"><h3>Solution</h3><p>Package app + dependencies into a reusable image.</p></div>
    <div class="step"><h3>Run</h3><p>Create an isolated container from that image.</p></div>
    <div class="step"><h3>Ship</h3><p>Same image runs on laptop, server, or cloud.</p></div>
  </div>
  <div class="grid cols-3" style="margin-top:28px;">
    <div class="card mini"><h3>Container</h3><p>A running isolated process with its own filesystem, packages, and network view.</p></div>
    <div class="card mini"><h3>Image</h3><p>A read-only blueprint used to create containers again and again.</p></div>
    <div class="card mini"><h3>Registry</h3><p>Online storage for images, for example <code>docker.io</code> and <code>ghcr.io</code>.</p></div>
  </div>
</div>

---

<div>
  <div class="kicker">Mental Model</div>
  <h2>Image vs Container vs Volume</h2>
  <div class="grid cols-2" style="align-items:center; gap:30px;">
    <div class="card">
      <div class="flow" style="gap:10px;">
        <div class="step" style="min-height:110px;"><h3>Registry</h3><p>docker.io<br>ghcr.io</p></div>
        <div class="step" style="min-height:110px;"><h3>Image</h3><p>Blueprint<br>read-only layers</p></div>
        <div class="step" style="min-height:110px;"><h3>Container</h3><p>Running process<br>writable layer</p></div>
        <div class="step" style="min-height:110px;"><h3>Volume</h3><p>Persistent data<br>survives recreate</p></div>
      </div>
    </div>
    <div>
      <table class="table">
        <tbody>
          <tr><td>Image</td><td>Like a class / template</td></tr>
          <tr><td>Container</td><td>Like an object / running instance</td></tr>
          <tr><td>Volume</td><td>Data storage outside container lifecycle</td></tr>
          <tr><td>Port map</td><td>Host port → container port</td></tr>
        </tbody>
      </table>
      <p class="note">Important: deleting a container can remove its writable layer, but named volumes can keep model/data files.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Podman vs Docker</div>
  <h2>Same Container Idea, Different Engine Style</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div class="card">
      <h3>Docker mental model</h3>
      <div class="flow">
        <div class="step"><h3>CLI</h3><p>docker command</p></div>
        <div class="step"><h3>Daemon</h3><p>dockerd manages containers</p></div>
        <div class="step"><h3>Containers</h3><p>running apps</p></div>
      </div>
    </div>
    <div class="card">
      <h3>Podman mental model</h3>
      <div class="flow">
        <div class="step"><h3>CLI</h3><p>podman command</p></div>
        <div class="step"><h3>Daemonless</h3><p>no central always-running daemon</p></div>
        <div class="step"><h3>Containers</h3><p>rootless-friendly workflow</p></div>
      </div>
    </div>
  </div>
  <pre class="clean-code" style="margin-top:24px;"><code># Many basic commands look similar
podman run docker.io/library/alpine:latest echo "hello"
# docker run docker.io/library/alpine:latest echo "hello"</code></pre>
</div>

---

<div>
  <div class="kicker">Command Anatomy</div>
  <h2>How the Shell Reads a Command</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code>sudo apt install -y podman</code></pre>
      <div class="flow" style="margin-top:20px;">
        <div class="step"><h3>1. Split</h3><p>Shell splits by spaces.</p></div>
        <div class="step"><h3>2. Find</h3><p>First token is executable.</p></div>
        <div class="step"><h3>3. Pass</h3><p>Remaining tokens become arguments.</p></div>
        <div class="step"><h3>4. Run</h3><p><code>sudo</code> runs with privilege.</p></div>
      </div>
    </div>
    <div class="card">
      <table class="table">
        <tbody>
          <tr><td><code>sudo</code></td><td>Run next command with admin/root privilege</td></tr>
          <tr><td><code>apt</code></td><td>Ubuntu package manager</td></tr>
          <tr><td><code>install</code></td><td>Subcommand/action</td></tr>
          <tr><td><code>-y</code></td><td>Automatically answer yes</td></tr>
          <tr><td><code>podman</code></td><td>Package name to install</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Install</div>
  <h2>Install Podman on Ubuntu</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code>sudo apt update
sudo apt install -y podman

podman --version
podman info</code></pre>
    </div>
    <div class="card">
      <h3>Teaching meaning</h3>
      <div class="checklist" style="grid-template-columns:1fr;">
        <div class="check"><strong>update</strong> refreshes package list.</div>
        <div class="check"><strong>install</strong> downloads and installs Podman.</div>
        <div class="check"><strong>--version</strong> confirms command exists.</div>
        <div class="check"><strong>info</strong> shows storage, network, rootless details.</div>
      </div>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Image Handling</div>
  <h2>Pull, List, Remove Images</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># Pull image: remote registry → local machine
podman pull docker.io/library/alpine:latest

# List local images
podman images

# Remove image by name
podman rmi docker.io/library/alpine:latest

# Force remove by image id
podman rmi -f IMAGE_ID</code></pre>
    </div>
    <div class="card">
      <h3>Registry naming</h3>
      <table class="table">
        <tbody>
          <tr><td><code>docker.io</code></td><td>Registry/server</td></tr>
          <tr><td><code>library</code></td><td>Namespace/owner</td></tr>
          <tr><td><code>alpine</code></td><td>Image repository</td></tr>
          <tr><td><code>latest</code></td><td>Tag/version label</td></tr>
        </tbody>
      </table>
      <p class="note">For Ollama, use <code>docker.io/ollama/ollama</code>.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Container Lifecycle</div>
  <h2>Run, Check, Stop, Start, Remove</h2>
  <div class="flow">
    <div class="step"><h3>run</h3><p>Create + start container.</p></div>
    <div class="step"><h3>ps</h3><p>See running containers.</p></div>
    <div class="step"><h3>stop</h3><p>Stop process gracefully.</p></div>
    <div class="step"><h3>start</h3><p>Start existing container.</p></div>
    <div class="step"><h3>rm</h3><p>Delete stopped container.</p></div>
  </div>
  <pre class="clean-code" style="margin-top:26px;"><code>podman run docker.io/library/alpine:latest echo "hello"
podman run -d --name demo docker.io/library/alpine:latest sleep 3600

podman ps
podman ps -a
podman stop demo
podman start demo
podman restart demo
podman rm demo</code></pre>
</div>

---

<div>
  <div class="kicker">Foreground vs Background</div>
  <h2>Detach Mode: Why <code>-d</code> Is Common</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div class="card">
      <h3>Foreground</h3>
      <pre class="clean-code"><code>podman run docker.io/library/alpine:latest ping google.com</code></pre>
      <p class="note">Terminal is attached to container output. Useful for quick tests.</p>
    </div>
    <div class="card">
      <h3>Background / detached</h3>
      <pre class="clean-code"><code>podman run -d --name demo docker.io/library/alpine:latest sleep 3600</code></pre>
      <p class="note">Container keeps running while your terminal is free. Useful for services.</p>
    </div>
  </div>
  <div class="card mini" style="margin-top:24px;"><p><strong>Rule:</strong> For servers like Ollama, FastAPI, PostgreSQL, Redis, use <code>-d</code> so the service stays running.</p></div>
</div>

---

<div>
  <div class="kicker">Ports</div>
  <h2>How Your Browser Reaches a Container</h2>
  <div class="grid cols-2" style="gap:30px; align-items:center;">
    <div class="card">
      <div class="flow">
        <div class="step"><h3>Host</h3><p><code>localhost:11000</code></p></div>
        <div class="step"><h3>Port Map</h3><p><code>-p 11000:11434</code></p></div>
        <div class="step"><h3>Container</h3><p>Ollama listens on <code>11434</code></p></div>
      </div>
    </div>
    <div>
      <pre class="clean-code"><code># Pattern
-p HOST_PORT:CONTAINER_PORT

# Ollama example
-p 11000:11434</code></pre>
      <p class="note">You call <code>localhost:11000</code> from your host. Podman forwards it to <code>11434</code> inside the container.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Run Ollama</div>
  <h2>Start Ollama as a Container Service</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code>podman run -d \
  --name myai \
  -p 11000:11434 \
  -v ollama-data:/root/.ollama \
  docker.io/ollama/ollama</code></pre>
      <pre class="clean-code" style="margin-top:14px;"><code>podman ps
curl http://localhost:11000/api/tags</code></pre>
    </div>
    <div class="card">
      <h3>Meaning of each part</h3>
      <table class="table">
        <tbody>
          <tr><td><code>-d</code></td><td>Run in background</td></tr>
          <tr><td><code>--name myai</code></td><td>Human-friendly container name</td></tr>
          <tr><td><code>-p</code></td><td>Expose service to host</td></tr>
          <tr><td><code>-v</code></td><td>Persist downloaded models</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Observe</div>
  <h2>Logs, Shell, Inspect, Processes</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># Logs
podman logs myai
podman logs --tail 50 myai
podman logs -f myai

# Enter container shell
podman exec -it myai sh</code></pre>
    </div>
    <div>
      <pre class="clean-code"><code># Run one command inside container
podman exec myai ollama ls

# Inspect metadata
podman inspect myai

# See processes inside container
podman top myai</code></pre>
      <div class="card mini" style="margin-top:14px;"><p><strong>Note:</strong> Many containers are minimal. If <code>vim</code>, <code>nano</code>, or <code>vi</code> are missing, create files on host and copy them in.</p></div>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Ollama Inside Container</div>
  <h2>Pull and Run <code>gemma3:270m</code></h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># Download model inside Ollama container
podman exec -it myai ollama pull gemma3:270m

# List models
podman exec myai ollama ls

# Quick prompt from inside container
podman exec -it myai ollama run gemma3:270m</code></pre>
    </div>
    <div class="card">
      <h3>What is happening?</h3>
      <div class="flow">
        <div class="step"><h3>Model files</h3><p>Stored in volume</p></div>
        <div class="step"><h3>Ollama server</h3><p>Loads model</p></div>
        <div class="step"><h3>Prompt</h3><p>Generates answer</p></div>
      </div>
      <p class="note" style="margin-top:18px;">Small models are best for teaching because downloads and responses are faster.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Modelfile</div>
  <h2>Make a Custom Teaching Model</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code>cat &gt; Modelfile &lt;&lt;'EOF'
FROM gemma3:270m

PARAMETER temperature 0.2
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER num_predict 150
PARAMETER num_ctx 2048

SYSTEM """
You are a helpful TDS teaching assistant.
Answer in brief bullet points with simple examples.
"""
EOF</code></pre>
    </div>
    <div class="card">
      <h3>Modelfile blocks</h3>
      <table class="table">
        <tbody>
          <tr><td><code>FROM</code></td><td>Base model</td></tr>
          <tr><td><code>PARAMETER</code></td><td>Runtime behavior/tuning</td></tr>
          <tr><td><code>SYSTEM</code></td><td>Default instruction/personality</td></tr>
        </tbody>
      </table>
      <p class="note">Create the file on your host. Then copy it into the container.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">No vim/nano?</div>
  <h2>Copy Modelfile Into the Container</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># From host → container
podman cp Modelfile myai:/Modelfile

# Create custom model inside container
podman exec -it myai ollama create tds-gemma -f /Modelfile

# Test it
podman exec -it myai ollama run tds-gemma</code></pre>
    </div>
    <div class="card">
      <h3>Why this method is clean</h3>
      <div class="checklist" style="grid-template-columns:1fr;">
        <div class="check">No editor needed inside container.</div>
        <div class="check">You keep Modelfile versioned on host.</div>
        <div class="check">Easy to edit in VS Code.</div>
        <div class="check">Easy to recreate model after changes.</div>
      </div>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Parameter Meaning</div>
  <h2>How Parameters Change Answers</h2>
  <table class="table" style="font-size:16px;">
    <thead><tr><th>Parameter</th><th>Simple meaning</th><th>Teaching recommendation</th></tr></thead>
    <tbody>
      <tr><td><code>temperature</code></td><td>Creativity/randomness. Lower = more focused.</td><td><code>0.1–0.3</code> for factual teaching</td></tr>
      <tr><td><code>top_k</code></td><td>Choose from top K likely next tokens.</td><td><code>40</code> is a common balanced start</td></tr>
      <tr><td><code>top_p</code></td><td>Choose from smallest token set whose probability reaches p.</td><td><code>0.8–0.95</code> for controlled variety</td></tr>
      <tr><td><code>num_predict</code></td><td>Maximum tokens generated in answer.</td><td><code>100–300</code> for brief answers</td></tr>
      <tr><td><code>num_ctx</code></td><td>Context window: prompt + memory available to model.</td><td><code>2048</code> small; increase for long docs</td></tr>
    </tbody>
  </table>
  <p class="note">Practical rule: start with low temperature, small num_predict, then increase only when needed.</p>
</div>

---

<div>
  <div class="kicker">REST API</div>
  <h2>Call Ollama From Outside the Container</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># Check models
curl http://localhost:11000/api/tags

# Generate one non-streaming answer
curl -s http://localhost:11000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "tds-gemma",
    "prompt": "Explain containers in 3 bullets",
    "stream": false
  }'</code></pre>
    </div>
    <div class="card">
      <h3>API flow</h3>
      <div class="flow">
        <div class="step"><h3>Client</h3><p>curl / FastAPI / Python</p></div>
        <div class="step"><h3>Host port</h3><p>11000</p></div>
        <div class="step"><h3>Ollama</h3><p>11434 inside container</p></div>
        <div class="step"><h3>Model</h3><p>tds-gemma</p></div>
      </div>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Python Client</div>
  <h2>Minimal FastAPI / Python Connection</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code>import requests

OLLAMA_BASE_URL = "http://localhost:11000"

payload = {
    "model": "tds-gemma",
    "prompt": "Teach Podman ps in simple words",
    "stream": False,
}

r = requests.post(
    f"{OLLAMA_BASE_URL}/api/generate",
    json=payload,
    timeout=120,
)
print(r.json()["response"])</code></pre>
    </div>
    <div class="card">
      <h3>When FastAPI is also containerized</h3>
      <p style="font-size:18px!important;">Do not use <code>localhost</code> from one container to reach another container unless they share the same network/pod.</p>
      <pre class="clean-code" style="margin-top:14px;"><code># Same pod/network idea:
OLLAMA_BASE_URL=http://myai:11434</code></pre>
      <p class="note">From host: <code>localhost:11000</code>. From another container: use container DNS/name on same network.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Debugging</div>
  <h2>Common Problems and Fixes</h2>
  <table class="table" style="font-size:16px;">
    <thead><tr><th>Problem</th><th>Check</th><th>Fix</th></tr></thead>
    <tbody>
      <tr><td>Port not working</td><td><code>podman ps</code></td><td>Confirm <code>11000-&gt;11434</code> mapping exists</td></tr>
      <tr><td>Model missing</td><td><code>podman exec myai ollama ls</code></td><td>Run <code>ollama pull gemma3:270m</code></td></tr>
      <tr><td>Container exited</td><td><code>podman logs myai</code></td><td>Read error and recreate if needed</td></tr>
      <tr><td>Cannot edit file inside</td><td><code>which vim nano vi</code></td><td>Edit on host, then <code>podman cp</code></td></tr>
      <tr><td>Data lost after remove</td><td><code>podman volume ls</code></td><td>Use named volume <code>ollama-data</code></td></tr>
    </tbody>
  </table>
</div>

---

<div>
  <div class="kicker">Clean Up</div>
  <h2>Stop, Remove, and Reset Safely</h2>
  <div class="grid cols-2" style="gap:30px;">
    <div>
      <pre class="clean-code"><code># Stop container
podman stop myai

# Start again later
podman start myai

# Remove container only
podman rm myai

# Remove image
podman rmi docker.io/ollama/ollama

# Remove model volume only if you want full reset
podman volume rm ollama-data</code></pre>
    </div>
    <div class="card">
      <h3>Teach this warning</h3>
      <p class="quote" style="font-size:28px!important;">Container is disposable. Volume is memory.</p>
      <p style="font-size:18px!important; color:var(--muted);">Remove containers freely. Remove volumes carefully because they store downloaded models and persistent data.</p>
    </div>
  </div>
</div>

---

<div>
  <div class="kicker">Teaching Lab</div>
  <h2>One Practical Session Plan</h2>
  <div class="flow" style="flex-wrap:wrap; gap:10px;">
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>1. Install</h3><p>Install Podman and verify info.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>2. Run Alpine</h3><p>Show image vs container lifecycle.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>3. Run Ollama</h3><p>Expose port and persist volume.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>4. Pull model</h3><p>Use <code>gemma3:270m</code>.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>5. Modelfile</h3><p>Create <code>tds-gemma</code>.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>6. REST API</h3><p>Call from curl/Python.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>7. Debug</h3><p>Use logs, exec, inspect, top.</p></div>
    <div class="step" style="flex:1 1 22%; min-height:105px;"><h3>8. Clean</h3><p>Stop, start, remove safely.</p></div>
  </div>
</div>

---

<div>
  <div class="kicker">Final Summary</div>
  <h2>What Students Must Remember</h2>
  <div class="grid cols-2" style="gap:35px;">
    <div class="card">
      <p class="quote" style="font-size:30px!important;">Image is the blueprint. Container is the running app. Volume is the persistent memory.</p>
      <div style="margin-top:14px;">
        <span class="pill">podman pull</span>
        <span class="pill green">podman run -d</span>
        <span class="pill violet">podman ps</span>
        <span class="pill amber">podman logs</span>
        <span class="pill red">podman exec</span>
      </div>
    </div>
    <div class="card">
      <h3>Resources</h3>
      <table class="table" style="font-size:15px;">
        <tbody>
          <tr><td>Podman run docs</td><td><a href="https://docs.podman.io/en/latest/markdown/podman-run.1.html" target="_blank">docs.podman.io</a></td></tr>
          <tr><td>Podman ps docs</td><td><a href="https://docs.podman.io/en/stable/markdown/podman-ps.1.html" target="_blank">podman ps reference</a></td></tr>
          <tr><td>Ollama Modelfile</td><td><a href="https://docs.ollama.com/modelfile" target="_blank">docs.ollama.com/modelfile</a></td></tr>
          <tr><td>Ollama API</td><td><a href="https://ollama.readthedocs.io/en/api/" target="_blank">API reference</a></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
