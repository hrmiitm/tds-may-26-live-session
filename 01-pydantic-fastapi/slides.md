<div class="titlemark">TDS Web Apps • Topic 1</div>

# Pydantic & FastAPI

Validation-first APIs, async routes, CORS, HTTPX and background calls.

<span class="pill">Pydantic</span><span class="pill">FastAPI</span><span class="pill">CORS</span><span class="pill">HTTPX</span><span class="pill">async/await</span>

---

## The one idea

<div class="flow">
  <span class="box">Client sends JSON</span><span class="arrow">→</span>
  <span class="box">Pydantic validates</span><span class="arrow">→</span>
  <span class="box">FastAPI runs logic</span><span class="arrow">→</span>
  <span class="box">Response model cleans output</span>
</div>

> In real APIs, bad input is normal. Validation is not decoration; it is your first security layer.

---

## Start small

```bash
uv init fastapi-demo
cd fastapi-demo
uv add fastapi uvicorn pydantic httpx
uv run uvicorn main:app --reload
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}
```

---

## Pydantic model = contract

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    age: int = Field(ge=13, le=120)
```

<div class="three">
<div class="card"><b>Types</b><p class="small">string, int, bool, list, nested objects</p></div>
<div class="card"><b>Rules</b><p class="small">min/max, regex pattern, enum choices</p></div>
<div class="card"><b>Errors</b><p class="small">automatic 422 response with details</p></div>
</div>

---

## GET: query validation

```python
from typing import Annotated
from fastapi import Query

@app.get("/search")
def search(
    q: Annotated[str, Query(min_length=2)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    return {"q": q, "limit": limit}
```

```text
/search?q=ai&limit=5     ✅
/search?q=a&limit=500    ❌ 422 validation error
```

---

## POST: body validation

```python
@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "created",
        "user": user.model_dump(),
    }
```

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "content-type: application/json" \
  -d '{"name":"Asha","email":"asha@example.com","age":21}'
```

---

## Response model: never leak extra fields

```python
class UserPublic(BaseModel):
    name: str
    email: EmailStr

@app.post("/users", response_model=UserPublic)
def create_user(user: UserCreate):
    db_row = {**user.model_dump(), "password_hash": "secret"}
    return db_row  # password_hash is removed from response
```

---

## CORS in one picture

<div class="flow">
  <span class="box">Browser page<br><b>localhost:5173</b></span><span class="arrow">→</span>
  <span class="box">API<br><b>localhost:8000</b></span>
</div>

<p class="small">Different origin = browser asks: “Is this frontend allowed to call this API?”</p>

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

## HTTPX: API calls from Python

```python
import httpx

@app.get("/joke")
def get_joke():
    r = httpx.get("https://official-joke-api.appspot.com/random_joke")
    r.raise_for_status()
    return r.json()
```

<p class="small">Use <code>httpx</code> when your FastAPI app must call another API.</p>

---

## Async route + AsyncClient

```python
import httpx

@app.get("/async-joke")
async def async_joke():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://official-joke-api.appspot.com/random_joke")
    r.raise_for_status()
    return r.json()
```

> <code>await</code> means: pause this request while network I/O is happening, let server handle other requests.

---

## Background process: accept target URL, send later

```python
from fastapi import BackgroundTasks, HttpUrl
from pydantic import BaseModel

class WebhookJob(BaseModel):
    target_url: HttpUrl
    payload: dict

async def send_webhook(url: str, payload: dict):
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(url, json=payload)

@app.post("/notify")
async def notify(job: WebhookJob, bg: BackgroundTasks):
    bg.add_task(send_webhook, str(job.target_url), job.payload)
    return {"status": "accepted"}
```

---

## When to use async?

<div class="split">
<div class="card">
<h3>Good async use</h3>
<p class="small">API calls, database calls, file/network I/O, waiting for external services.</p>
</div>
<div class="card">
<h3>Not magic</h3>
<p class="small">CPU-heavy work still blocks. Use workers/processes for large computation.</p>
</div>
</div>

---

## Mini project flow

<div class="flow">
  <span class="box">POST /notify</span><span class="arrow">→</span>
  <span class="box">Pydantic checks URL + payload</span><span class="arrow">→</span>
  <span class="box">Return accepted</span><span class="arrow">→</span>
  <span class="box">Background HTTPX call</span>
</div>

<p class="small">This is the base pattern for webhooks, task triggers, async callbacks and integrations.</p>

---

## Practice

1. Add a <code>status</code> field with only <code>pending</code>, <code>running</code>, <code>done</code>.
2. Add a response model that hides internal fields.
3. Add CORS for your frontend origin only.
4. Convert one blocking <code>httpx.get</code> route to async.

---

# Mental model

**FastAPI handles HTTP. Pydantic protects your boundaries. HTTPX talks to outside services. async helps during waiting.**
