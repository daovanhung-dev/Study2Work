# Study Ollama service

Source: `apps/study-server/app/service/ai/ollama_service.py`.

Status: implementation exists; **no verified Study runtime caller** at current snapshot because business modules were removed.

`OllamaService` is an async HTTP adapter using `httpx`.

- Base URL: arg -> `OLLAMA_BASE_URL` -> `http://127.0.0.1:11434`.
- Model: arg -> `OLLAMA_MODEL` -> `qwen2.5-coder:1.5b`.
- Timeout: arg -> `OLLAMA_TIMEOUT` -> 180 seconds.
- `generate`: POST `/api/generate`, `stream=false`.
- `chat`: POST `/api/chat`, `stream=false`.
- `list_models`: GET `/api/tags`.
- `health_check`: wraps model listing.
- `_request`: creates an `httpx.AsyncClient` per call; no retry/backoff.

Error mapping:
- connect -> `AIConnectionError`;
- timeout -> `AITimeoutError`;
- non-2xx / non-object JSON / invalid JSON -> `AIResponseError`.

Do not add Study endpoint wiring to this service without a current module/requirement proving ownership.
