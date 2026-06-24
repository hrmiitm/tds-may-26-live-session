<div class="hero-center">
<div>
<div class="title-kicker">TDS • Local AI Serving</div>
<h1>Local LLM</h1>
<p class="big">Ollama for easy local models, vLLM for high-throughput serving, and APIs to connect your apps.</p>
<p><span class="tag">Ollama</span><span class="tag">vLLM</span><span class="tag">parameters</span><span class="tag">quantization</span><span class="tag">REST</span></p>
</div>
</div>

---

## Choose the right server

<div class="grid2">
<div class="card"><h3>Ollama</h3><p>Best for learning, quick local demos, model files, simple REST API.</p></div>
<div class="card"><h3>vLLM</h3><p>Best for GPU serving, batching, OpenAI-compatible endpoint, more throughput.</p></div>
</div>

<div class="callout">Do not start with infrastructure. Start with one model answering one request correctly.</div>

---

## Request flow

<div class="flow">
  <div class="node">User prompt</div><div class="arrow">→</div>
  <div class="node">FastAPI app</div><div class="arrow">→</div>
  <div class="node">Local LLM server</div><div class="arrow">→</div>
  <div class="node">Generated answer</div>
</div>

<p class="muted">The model server is just another HTTP service.</p>

---

## Ollama basics

```bash
ollama pull llama3.2:3b
ollama list
ollama run llama3.2:3b
ollama ps
```

<div class="grid3">
<div class="card"><h3>pull</h3><p>Download model.</p></div>
<div class="card"><h3>run</h3><p>Interactive chat.</p></div>
<div class="card"><h3>serve</h3><p>Expose local API.</p></div>
</div>

---

## Generation parameters

<div class="grid2">
<div class="card"><h3>temperature</h3><p>Higher = more creative; lower = more deterministic.</p></div>
<div class="card"><h3>top_p</h3><p>Limits next-token choices to likely options.</p></div>
<div class="card"><h3>num_ctx</h3><p>How much context the model can read.</p></div>
<div class="card"><h3>max tokens</h3><p>How long the answer can be.</p></div>
</div>

---

## Quantization: why smaller models run

<div class="flow">
  <div class="node">Full precision</div><div class="arrow">→</div>
  <div class="node">Less memory</div><div class="arrow">→</div>
  <div class="node">Lower precision</div><div class="arrow">→</div>
  <div class="node">Possible quality drop</div>
</div>

<div class="callout warn">Quantization is a trade-off: fit model on your machine, but test answer quality for your task.</div>

---

## Ollama Modelfile

```text
FROM llama3.2:3b

SYSTEM """
You are a concise teaching assistant for TDS students.
Explain with small examples.
"""

PARAMETER temperature 0.2
PARAMETER num_ctx 4096
```

```bash
ollama create tds-teacher -f Modelfile
ollama run tds-teacher
```

---

## Ollama REST API

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "Explain Docker volume in one example",
    "stream": false
  }'
```

```python
import httpx

async with httpx.AsyncClient(timeout=60) as client:
    r = await client.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False,
    })
```

---

## vLLM: OpenAI-compatible serving

```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8001
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8001/v1", api_key="local")
```

<div class="callout">vLLM becomes useful when many users send requests or GPU batching matters.</div>

---

## Performance knobs

<div class="grid3">
<div class="card"><h3>Model size</h3><p>Small model = faster; large model = more capable.</p></div>
<div class="card"><h3>Context length</h3><p>Longer context consumes memory.</p></div>
<div class="card"><h3>Batching</h3><p>Serve multiple requests more efficiently.</p></div>
</div>

<p class="muted">Measure latency, tokens/sec, memory, and answer quality.</p>

---

## FastAPI gateway for local LLM

```python
@app.post("/ask")
async def ask(req: AskRequest):
    async with httpx.AsyncClient(timeout=90) as client:
        res = await client.post(OLLAMA_URL, json={
            "model": req.model,
            "prompt": req.prompt,
            "stream": False,
            "options": {"temperature": req.temperature},
        })
    return {"answer": res.json()["response"]}
```

<div class="flow">
  <div class="node">Validate request</div><div class="arrow">→</div>
  <div class="node">Call model</div><div class="arrow">→</div>
  <div class="node">Log latency</div><div class="arrow">→</div>
  <div class="node">Return answer</div>
</div>

---

## Local LLM checklist

<ul class="checklist">
<li>Start with one small model and one endpoint.</li>
<li>Keep model name and temperature in config.</li>
<li>Add timeouts to all model calls.</li>
<li>Log prompt length, latency, model, and failures.</li>
<li>Test quantized models with real course questions.</li>
</ul>
