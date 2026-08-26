# AI Server agent entry

Source root: `apps/ai-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_MINIMAL_CHAT
COPIED_CORE_STATUS: UNWIRED
DATABASE_RUNTIME_USAGE: NONE
TEST_STATUS: NOT_FOUND
```

## Load theo task

| Task | Context |
|---|---|
| composition/copied infra | `architecture.md`, `core/copied-core.md` |
| chat module/API | `modules/chat.md`, `apis/chat.md` |
| Ollama behavior | `services/ollama.md` |
| DB | `database.md` |
| testing | `tests.md` |

## Critical rules

- Runtime-active means reachable from `app/main.py`; do not infer activation from file existence.
- Current main does not register copied middleware, exception handlers, DB, security or standard envelope.
- `query.py` and `validate.py` are empty placeholders; do not invent their future responsibilities beyond filenames.
- `pyproject.toml` only declares FastAPI/httpx/uvicorn. Copied core imports packages not in this dependency set.
- Current chat API response is `{response: <string>}`, not the shared Work/Study envelope.
