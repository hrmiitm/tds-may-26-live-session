<div class="hero-center">
<div>
<div class="title-kicker">TDS • Ship the API</div>
<h1>Deployment</h1>
<p class="big">Small FastAPI app → Hugging Face Space → config → logs for future debugging.</p>
<p><span class="tag">Docker Space</span><span class="tag">env</span><span class="tag">secrets</span><span class="tag">logging</span></p>
</div>
</div>

---

## Deployment is a repeatable story

<div class="flow">
  <div class="node">Code</div><div class="arrow">→</div>
  <div class="node">Dependencies</div><div class="arrow">→</div>
  <div class="node">Config</div><div class="arrow">→</div>
  <div class="node">Runtime</div><div class="arrow">→</div>
  <div class="node">Logs</div>
</div>

<div class="callout">If it works only on your laptop, it is not deployed. Deployment means another machine can build and run it reliably.</div>

---

## Small app structure

```text
tds-api/
├─ app.py
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

```python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}
```

---

## Run locally first

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

<div class="grid2">
<div class="card"><h3>Local test</h3><p><code>/health</code> returns JSON.</p></div>
<div class="card"><h3>Deployment test</h3><p>Same route works on remote URL.</p></div>
</div>

---

## Hugging Face Space: Docker runtime

<div class="flow">
  <div class="node">Create Space</div><div class="arrow">→</div>
  <div class="node">Select Docker</div><div class="arrow">→</div>
  <div class="node">Push files</div><div class="arrow">→</div>
  <div class="node">Build logs</div><div class="arrow">→</div>
  <div class="node">Public URL</div>
</div>

<p class="muted">Hugging Face Spaces conventionally serves apps on port <code>7860</code>.</p>

---

## Dockerfile for FastAPI Space

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

```text
# requirements.txt
fastapi
uvicorn[standard]
```

---

## Config management

<div class="grid2">
<div class="card"><h3>Never hard-code</h3><p>API keys, database URLs, admin emails, model names.</p></div>
<div class="card"><h3>Use environment</h3><p>Different values for local, test, production.</p></div>
</div>

```python
import os

APP_ENV = os.getenv("APP_ENV", "local")
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "").split(",")
```

---

## Better config with settings object

```bash
pip install pydantic-settings
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    admin_emails: list[str] = []
    log_level: str = "INFO"

settings = Settings()
```

<p class="muted">One object keeps config readable and testable.</p>

---

## Logging: what happened, when, and why

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("tds-api")

@app.get("/health")
def health():
    logger.info("health_check")
    return {"ok": True}
```

<div class="callout">Use logs to answer: request came? config loaded? external API failed? exception trace?</div>

---

## Store/export logs for future debugging

<div class="grid3">
<div class="card"><h3>stdout</h3><p>Best for cloud platforms and containers.</p></div>
<div class="card"><h3>file</h3><p>Useful locally; rotate large logs.</p></div>
<div class="card"><h3>JSON</h3><p>Easy to search in log systems.</p></div>
</div>

```python
logger.info("job_created", extra={"job_id": job_id, "target": url})
logger.exception("job_failed")  # includes traceback
```

---

## Production checklist

<ul class="checklist">
<li><strong>/health</strong> endpoint works.</li>
<li><strong>Secrets</strong> are environment variables, not committed.</li>
<li><strong>Logs</strong> show startup and errors.</li>
<li><strong>CORS</strong> has real frontend origins, not unlimited production wildcard.</li>
<li><strong>Timeouts</strong> exist for all external HTTP calls.</li>
</ul>

---

## Debugging flow

<div class="flow">
  <div class="node">User says broken</div><div class="arrow">→</div>
  <div class="node">Check health</div><div class="arrow">→</div>
  <div class="node">Read logs</div><div class="arrow">→</div>
  <div class="node">Reproduce locally</div><div class="arrow">→</div>
  <div class="node">Patch + redeploy</div>
</div>

<p class="muted">A deployed app without logs is like debugging in the dark.</p>
