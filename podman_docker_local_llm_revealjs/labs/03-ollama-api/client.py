import os
import requests

base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
model = os.getenv("OLLAMA_MODEL", "llama3.2")

payload = {
    "model": model,
    "prompt": "Explain Docker volumes in 5 beginner-friendly bullet points.",
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_predict": 250,
    },
}

response = requests.post(f"{base_url}/api/generate", json=payload, timeout=180)
response.raise_for_status()
print(response.json()["response"])
