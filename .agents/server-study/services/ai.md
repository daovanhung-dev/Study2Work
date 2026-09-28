# Study Ollama service

Source: `apps/study-server/app/service/ai/ollama_service.py`.

Status: implementation exists; **no verified Study runtime caller** at current snapshot because business modules were removed.

`OllamaService` is an async HTTP adapter using `httpx`.

- Base URL: arg -> `constants.OLLAMA_BASE_URL`.
- Model: arg -> `constants.OLLAMA_MODEL`.
- Timeout: arg -> `constants.OLLAMA_TIMEOUT`.
- Không đọc `.env` hoặc process environment; override chỉ qua constructor.
- `generate`: POST `/api/generate`, `stream=false`.
- `chat`: POST `/api/chat`, `stream=false`.
- `list_models`: GET `/api/tags`.
- `health_check`: wraps model listing.
- `_request`: creates an `httpx.AsyncClient` per call; no retry/backoff.

Error mapping:
- connection, timeout, non-2xx, non-object JSON, invalid JSON and other request
  failures -> a direct safe `error_response()` `JSONResponse` (HTTP 500 /
  `INTERNAL_SERVER_ERROR`) propagated by public adapter methods.

Do not add Study endpoint wiring to this service without a current module/requirement proving ownership.
