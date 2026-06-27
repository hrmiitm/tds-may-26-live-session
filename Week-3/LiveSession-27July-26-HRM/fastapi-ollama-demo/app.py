# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "fastapi>=0.138.1",
#     "pydantic>=2.13.4",
#     "requests>=2.34.2",
#     "uvicorn>=0.49.0",
# ]
# ///
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11000")
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:270m")


class AskRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "FastAPI + Ollama is running"}


@app.post("/ask")
def ask(req: AskRequest):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": req.prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
