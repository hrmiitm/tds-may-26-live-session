# Lab 03 — Ollama API and Modelfile

Install Ollama first, then:

```bash
ollama pull llama3.2
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install requests
python client.py
```

Create a custom wrapper model:

```bash
ollama create devops-tutor -f Modelfile
ollama run devops-tutor
```
