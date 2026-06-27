# Lab 04 — vLLM server

This lab usually needs a suitable GPU and enough VRAM.

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-8B-Instruct --dtype auto --api-key local-token
```

Call the OpenAI-compatible endpoint:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer local-token" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"meta-llama/Llama-3.1-8B-Instruct",
    "messages":[{"role":"user","content":"Explain Podman in two lines."}]
  }'
```
