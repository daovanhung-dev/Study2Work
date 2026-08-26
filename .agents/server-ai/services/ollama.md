# AI Ollama adapter

Source: `app/service/ai/ollama_service.py`.

## Configuration

- base URL: constructor -> `OLLAMA_BASE_URL` -> `http://127.0.0.1:11434`.
- default model: constructor -> `OLLAMA_MODEL` -> `qwen2.5-coder:1.5b`.
- timeout: constructor -> `OLLAMA_TIMEOUT` -> `180` seconds.
- singleton: `ai_service = OllamaService()` at import time.

## `generate(prompt, system=None, model=None, options=None)`
POST `/api/generate` with `{model,prompt,stream:false}` plus optional system/options. Returns normalized dict `{model, answer, done, raw}` where answer is Ollama `response` or empty string.

This is the **only Ollama method called by current API**.

## `chat(messages, ...)`
POST `/api/chat`; normalizes nested message into `{model, role, answer, done, raw}`. Present but no verified caller.

## `list_models()` / `health_check()`
GET `/api/tags`; present but no runtime endpoint/caller.

## `_request`
Creates a new `httpx.AsyncClient(timeout=self.timeout)` per request. No retry/backoff/circuit breaker.

Error mapping:
- `httpx.ConnectError` -> `AIConnectionError`;
- timeout -> `AITimeoutError`;
- non-2xx -> `AIResponseError` including upstream status/text;
- invalid/non-object JSON -> `AIResponseError`.

Current FastAPI composition has no global adapter-specific exception handler, so these exceptions are not translated to a custom safe envelope by current source.
