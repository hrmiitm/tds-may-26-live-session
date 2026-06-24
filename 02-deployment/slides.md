<div class="titlemark">TDS Web Apps • Topic 2</div>

# Deployment

Build a small FastAPI app, deploy it, manage config, and keep logs for debugging.

<span class="pill">Hugging Face Spaces</span><span class="pill">Config</span><span class="pill">Secrets</span><span class="pill">Logging</span>

---

## What deployment really means

<div class="flow">
  <span class="box">Code works locally</span><span class="arrow">→</span>
  <span class="box">Runs on remote machine</span><span class="arrow">→</span>
  <span class="box">Config comes from environment</span><span class="arrow">→</span>
  <span class="box">Logs explain failures</span>
</div>

---

## Minimal app structure

```text
app/
  main.py
  settings.py
  logging_config.py
pyproject.toml
README.md
```

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="TDS Deploy Demo")

@app.get("/health")
def health():
    return {"ok": True}
```

---

## Local run

```bash
uv add fastapi uvicorn pydantic-settings
uv run uvicorn app.main:app --host 0.0.0.0 --port 7860
```

<p class="small"><b>7860</b> is commonly used by Hugging Face Spaces web apps.</p>

---

## Config management

```python
# app/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TDS Deploy Demo"
    debug: bool = False
    allowed_origin: str = "http://localhost:5173"
    api_key: str | None = None

settings = Settings()
```

```bash
DEBUG=true API_KEY=dev-secret uv run uvicorn app.main:app --reload
```

---

## Config rule

<div class="three">
<div class="card"><b>Code</b><p class="small">Business logic, routes, models</p></div>
<div class="card"><b>Config</b><p class="small">Port, origin, database URL, model name</p></div>
<div class="card"><b>Secrets</b><p class="small">API keys, OAuth secrets, tokens</p></div>
</div>

> Never hard-code secrets inside GitHub code.

---

## Logging: future debugging

```python
# app/logging_config.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("tds-app")
```

---

## Use logs inside routes

```python
from app.logging_config import logger

@app.get("/items/{item_id}")
def get_item(item_id: int):
    logger.info("fetch_item item_id=%s", item_id)
    return {"item_id": item_id}
```

<p class="small">Good logs answer: what happened, when, for which input, and where.</p>

---

## Store logs locally during development

```python
import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,
    backupCount=3,
)
logging.getLogger().addHandler(file_handler)
```

<p class="small">In hosted platforms, stdout logs are usually collected by the platform.</p>

---

## Deploy on Hugging Face Space

```text
Create Space → SDK: Docker or Gradio Static? For FastAPI choose Docker.
```

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync --frozen || uv sync
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Health checks

```python
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "debug": settings.debug,
    }
```

<div class="flow">
  <span class="box">Browser</span><span class="arrow">→</span>
  <span class="box">/health</span><span class="arrow">→</span>
  <span class="box">Is app alive?</span>
</div>

---

## Deployment checklist

- App starts with one command.
- Port is correct.
- Secrets come from environment variables.
- CORS is configured for real frontend.
- Logs go to stdout.
- <code>/health</code> works.

---

## Common mistakes

<div class="split">
<div class="card"><h3>Works locally only</h3><p class="small">Using relative files, missing dependencies, wrong port.</p></div>
<div class="card"><h3>No debugging trail</h3><p class="small">No logs, no request IDs, swallowing exceptions.</p></div>
</div>

---

## Practice

1. Create <code>/health</code>, <code>/config</code>, <code>/echo</code> routes.
2. Read <code>APP_NAME</code> from env.
3. Log every request input.
4. Deploy and check logs after one failed request.

---

# Mental model

**Deployment is not “upload code”. It is repeatable startup + external config + observable behavior.**
