# AI Server architecture

## Actual runtime path

```text
app/main.py
  -> FastAPI()
  -> GET /
  -> include app/api/v1.py:router
       -> POST /api/v1/chat_log_ai
          -> app/module/chat/chat.py re-export
          -> app/module/chat/view.py:chat_log_ai
          -> app/service/ai/ollama_service.py:ai_service.generate
          -> Ollama POST /api/generate
```

There is no verified runtime registration for:

- `app/core/middleware.py`;
- `app/core/exceptions.py`;
- `app/core/responses.py`;
- `app/core/security.py`;
- `app/core/database.py`;
- `app/core/trace.py`.

Those files are documented separately as `UNWIRED` copied core.

## Packaging discrepancy

`apps/ai-server/pyproject.toml` declares only FastAPI, httpx and uvicorn. Runtime chat path is compatible with that minimal set plus Pydantic through FastAPI. Copied core references SQLAlchemy/pydantic-settings/JWT/security dependencies not declared here; importing/wiring it requires an explicit dependency decision.
