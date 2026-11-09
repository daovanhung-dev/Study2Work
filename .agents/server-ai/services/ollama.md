# AI Ollama adapter

Source: `app/service/ai/ollama_service.py`.

## Configuration

- base URL: constructor -> `OLLAMA_BASE_URL` -> `http://127.0.0.1:11434`.
- default model: constructor -> `OLLAMA_MODEL` -> `qwen2.5-coder:1.5b`.
- timeout connect/read/write: constructor -> `OLLAMA_TIMEOUT` -> `180` seconds; pool wait 5 seconds.
- singleton: `ai_service = OllamaService()` at import time.

## `generate(prompt, system=None, model=None, options=None)`
POST `/api/generate` with `{model,prompt,stream:false}` plus optional system/options. Returns normalized dict `{model, answer, done, raw}`; `response` must be a string.

This is the **only Ollama method called by current API**.

## `chat(messages, ...)`
POST `/api/chat`; normalizes nested message into `{model, role, answer, done, raw}`. Present but no verified caller.

## `list_models()` / `health_check()`
GET `/api/tags`; present but no runtime endpoint/caller.

## `_request`
`start()` creates one `httpx.AsyncClient` with `max_connections=100`; `_request` requires it and reuses it; `close()` closes it. FastAPI lifespan owns the singleton's lifecycle. Direct callers must call `start()` before methods and `close()` in `finally`. Pool wait is 5 seconds. No retry/backoff/circuit breaker.

Error mapping:
- `httpx.PoolTimeout` -> `AIBusyError`;
- connect timeout/network errors -> `AIConnectionError`;
- read/write timeout -> `AITimeoutError`;
- non-2xx, protocol/decoding error, invalid JSON or invalid response field -> `AIResponseError`.

FastAPI maps these errors to safe 503/504/502 JSON via `app/main.py`. Logs omit prompt and upstream body.
