<div class="titlemark">TDS AI Systems • Topic 5</div>

# Local LLM

Ollama, vLLM, model parameters, quantization, REST API and Modelfiles.

<span class="pill">Ollama</span><span class="pill">vLLM</span><span class="pill">Quantization</span><span class="pill">REST API</span><span class="pill">Modelfile</span>

---

## Why local LLM?

<div class="three">
<div class="card"><b>Privacy</b><p class="small">Data can stay on your machine/server.</p></div>
<div class="card"><b>Control</b><p class="small">Choose model, parameters, prompt format.</p></div>
<div class="card"><b>Cost</b><p class="small">Useful for repeated experiments and demos.</p></div>
</div>

---

## Ollama vs vLLM

<div class="split">
<div class="card"><h3>Ollama</h3><p class="small">Simple local model runner. Great for laptops, demos, REST API, Modelfiles.</p></div>
<div class="card"><h3>vLLM</h3><p class="small">High-throughput serving engine. Better for GPUs, batching, production-style serving.</p></div>
</div>

---

## Ollama basic commands

```bash
ollama pull llama3.2:3b
ollama run llama3.2:3b
ollama list
ollama rm llama3.2:3b
```

<p class="small">Choose smaller models first if RAM/VRAM is limited.</p>

---

## Run model with parameters

```bash
ollama run llama3.2:3b
```

Inside chat:

```text
/set parameter temperature 0.2
/set parameter num_ctx 4096
/set parameter top_p 0.9
```

---

## Key parameters

<div class="three">
<div class="card"><b>temperature</b><p class="small">Lower = focused. Higher = creative.</p></div>
<div class="card"><b>num_ctx</b><p class="small">Context window. More tokens need more memory.</p></div>
<div class="card"><b>top_p</b><p class="small">Controls sampling diversity.</p></div>
</div>

---

## Ollama REST API

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "Explain Docker in 3 lines",
    "stream": false
  }'
```

<p class="small">This lets your FastAPI app call a local model.</p>

---

## FastAPI → Ollama

```python
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ask(BaseModel):
    question: str

@app.post("/ask")
async def ask_llm(req: Ask):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:3b",
            "prompt": req.question,
            "stream": False,
        })
    return r.json()
```

---

## Quantization: the trade-off

<div class="flow">
  <span class="box">Original weights</span><span class="arrow">→</span>
  <span class="box">Compressed weights</span><span class="arrow">→</span>
  <span class="box">Less memory</span><span class="arrow">→</span>
  <span class="box">Maybe lower quality</span>
</div>

```text
Q4  = smaller, faster, lower memory
Q8  = larger, often better quality
FP16 = high quality, heavy memory
```

---

## Choosing a model

<div class="three">
<div class="card"><b>Laptop CPU</b><p class="small">1B–3B quantized</p></div>
<div class="card"><b>Consumer GPU</b><p class="small">7B–14B quantized</p></div>
<div class="card"><b>Server GPU</b><p class="small">vLLM + larger models</p></div>
</div>

---

## Ollama Modelfile

```text
FROM llama3.2:3b
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
SYSTEM "You are a concise teaching assistant for TDS students."
```

```bash
ollama create tds-teacher -f Modelfile
ollama run tds-teacher
```

---

## vLLM OpenAI-compatible server

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

<p class="small">Then call it like an OpenAI-style chat completions API.</p>

---

## Local LLM app architecture

<div class="flow">
  <span class="box">Browser</span><span class="arrow">→</span>
  <span class="box">FastAPI</span><span class="arrow">→</span>
  <span class="box">Ollama/vLLM</span><span class="arrow">→</span>
  <span class="box">Answer</span>
</div>

<p class="small">For RAG, insert retrieval before sending context to the model.</p>

---

## Debugging slow answers

- Model too large for hardware.
- Context window too high.
- CPU-only inference.
- Streaming disabled for long answers.
- Too many concurrent users.

---

## Practice

1. Pull one small model in Ollama.
2. Call it using REST API.
3. Create a custom Modelfile.
4. Wrap it with FastAPI <code>/ask</code> route.
5. Try temperature <code>0.1</code> vs <code>1.0</code>.

---

# Mental model

**Ollama is easiest for local demos. vLLM is for serious serving. Quantization buys memory savings. Parameters shape behavior.**
