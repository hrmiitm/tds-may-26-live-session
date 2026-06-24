<div class="hero-center">
<div>
<div class="title-kicker">TDS • Web API Foundations</div>
<h1>Pydantic & FastAPI</h1>
<p class="big">Validate input → handle request → call other services → respond cleanly.</p>
<p><span class="tag">Pydantic</span><span class="tag">FastAPI</span><span class="tag">CORS</span><span class="tag">HTTPX</span><span class="tag">async</span></p>
</div>
</div>

---

## The mental model

<div class="flow">
  <div class="node">Browser / client</div><div class="arrow">→</div>
  <div class="node">FastAPI route</div><div class="arrow">→</div>
  <div class="node">Pydantic validation</div><div class="arrow">→</div>
  <div class="node">Your function</div><div class="arrow">→</div>
  <div class="node">JSON response</div>
</div>

<div class="callout">FastAPI is not “just Flask with decorators”. The powerful part is that <strong>types become runtime validation + documentation</strong>.</div>

---

## Pydantic: data validation first

```python
from pydantic import BaseModel, Field, HttpUrl

class JobRequest(BaseModel):
    target_url: HttpUrl
    retries: int = Field(default=3, ge=0, le=10)
    payload: dict = Field(default_factory=dict)
```

<div class="grid3">
<div class="card"><h3>Shape</h3><p>What fields are allowed?</p></div>
<div class="card"><h3>Type</h3><p>Should this be int, str, URL, list?</p></div>
<div class="card"><h3>Rule</h3><p>Range, length, default, optional?</p></div>
</div>

---

## Validation failure is a feature

```json
{
  "target_url": "not-a-url",
  "retries": 500
}
```

<div class="flow">
  <div class="node">Bad input</div><div class="arrow">→</div>
  <div class="node">Pydantic catches it</div><div class="arrow">→</div>
  <div class="node">FastAPI returns 422</div>
</div>

<p class="muted">Your route function does not even run until the request is valid.</p>

---

## FastAPI minimal app

```python
from fastapi import FastAPI

app = FastAPI(title="TDS Demo API")

@app.get("/")
def home():
    return {"message": "API is running"}
```

```bash
uv add fastapi uvicorn
uvicorn app:app --reload
# open http://127.0.0.1:8000/docs
```

---

## GET: path + query validation

```python
from typing import Annotated
from fastapi import Query

@app.get("/items/{item_id}")
def read_item(
    item_id: int,
    q: Annotated[str | None, Query(min_length=2)] = None,
):
    return {"item_id": item_id, "q": q}
```

<div class="callout">The URL is text, but FastAPI converts and validates it before your function receives it.</div>

---

## POST: validated Pydantic model

```python
class Student(BaseModel):
    name: str = Field(min_length=2)
    email: str
    marks: float = Field(ge=0, le=100)

@app.post("/students")
def create_student(student: Student):
    return {
        "saved": True,
        "student": student.model_dump()
    }
```

<p>Request body → Pydantic object → clean Python data.</p>

---

## CORS: browser safety gate

<div class="flow">
  <div class="node">Frontend<br><small>localhost:5173</small></div><div class="arrow">→</div>
  <div class="node">Browser asks:<br>allowed?</div><div class="arrow">→</div>
  <div class="node">API<br><small>localhost:8000</small></div>
</div>

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## HTTPX: API calling another API

```python
import httpx

@app.get("/github/{user}")
async def github_user(user: str):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"https://api.github.com/users/{user}")
        r.raise_for_status()
        return r.json()
```

<div class="callout">Use <code>httpx.AsyncClient</code> when your FastAPI route is <code>async def</code>.</div>

---

## Target URL → background task → send data

<div class="flow">
  <div class="node">POST job</div><div class="arrow">→</div>
  <div class="node">Validate URL</div><div class="arrow">→</div>
  <div class="node">Return 202 quickly</div><div class="arrow">→</div>
  <div class="node">Send later</div>
</div>

```python
from fastapi import BackgroundTasks

async def send_payload(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

@app.post("/jobs", status_code=202)
async def create_job(req: JobRequest, bg: BackgroundTasks):
    bg.add_task(send_payload, str(req.target_url), req.payload)
    return {"status": "accepted"}
```

---

## async / await: the simple rule

<div class="grid2">
<div class="card"><h3>Use async when waiting</h3><p>HTTP calls, DB calls, files, queues, network.</p></div>
<div class="card"><h3>Do not block the event loop</h3><p>Avoid slow CPU work and <code>time.sleep()</code> inside <code>async def</code>.</p></div>
</div>

```python
# good
await client.get(url)

# bad inside async route
# time.sleep(5)
```

---

## Practice flow

<div class="grid3">
<div class="card"><div class="number">1</div><p>Create <code>/validate</code> using Pydantic.</p></div>
<div class="card"><div class="number">2</div><p>Add CORS for a local frontend.</p></div>
<div class="card"><div class="number">3</div><p>Accept <code>target_url</code>, send data via <code>httpx</code> in background.</p></div>
</div>

<p class="muted">Use the pen: <span class="kbd">D</span> draw, <span class="kbd">E</span> erase, <span class="kbd">P</span> PDF.</p>
