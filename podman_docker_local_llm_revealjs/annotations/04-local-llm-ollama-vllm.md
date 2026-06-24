# 04 — Local LLM, Ollama, vLLM annotations

## 01-local-llm-model
A local LLM setup has three parts: model weights, inference runtime, and API/app layer. Students often think the model is the app. Actually the model is data; Ollama/vLLM load it and serve tokens through a process.

## 02-ollama-vs-vllm
Ollama is excellent for local development, teaching, quick demos, and simple REST API use. vLLM is stronger when serving many requests, exposing an OpenAI-compatible endpoint, or running on a GPU server. Do not teach one as universally better.

## 03-running-ollama
`ollama pull` downloads weights. `ollama run` starts an interactive chat and pulls if needed. `ollama list` shows downloaded models. `ollama show` helps inspect model metadata, template, and parameters.

## 04-parameters
Temperature changes randomness. Low temperature is better for deterministic tutoring and coding. Higher temperature is useful for brainstorming. `num_ctx` controls context length but also memory use. `num_predict` limits output length. Sampling cannot fix a weak model or missing context.

## 05-generate-api
`/api/generate` is single-prompt style. `stream: false` makes curl output easy to read. In production you may use streaming for better UX. Always set request timeout in Python clients because local LLM generation can be slow.

## 06-chat-api
`/api/chat` uses role-based messages and fits multi-turn chatbots. It is closer to chat model APIs. Keep system messages short and clear. Store conversation history carefully because long histories consume context.

## 07-modelfile
A Modelfile wraps a base model with default system prompt, parameters, templates, adapter, or license metadata. It does not magically fine-tune the model. It is more like a reusable configuration layer.

## 08-quantization
Quantization reduces memory by representing weights with fewer bits. It can speed up inference and allow larger models on smaller machines. Tradeoff: too much quantization can reduce quality, especially reasoning, math, and code precision.

## 09-choosing-quantized
Teach the resource-quality tradeoff. If model does not fit memory, it may be painfully slow or fail to load. A smaller model that fits well can feel better than a large model constantly swapping memory.

## 10-vllm-server
vLLM exposes an OpenAI-compatible API. This is powerful because existing OpenAI SDK code can often be pointed to the local server by changing base URL and API key. GPU drivers, CUDA version, model license/access, and memory are common setup blockers.

## 11-api-comparison
Ollama native endpoints are simple and excellent for labs. vLLM's OpenAI-compatible server is useful when you want app compatibility and higher-throughput serving.
