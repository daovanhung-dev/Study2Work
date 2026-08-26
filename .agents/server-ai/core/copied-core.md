# AI copied core

Global status: `UNWIRED` from current composition root.

## What exists

`app/core/` contains config, database, exceptions, middleware, responses, security and trace implementations resembling infrastructure from Study.

Examples:
- `database.py`: sync SQLAlchemy PostgreSQL engine/session/query helpers; identical helper blob to the tracked Study DB helper.
- `responses.py`: standard `success_response`, `error_response`, `ApiError`, compatibility payload helpers and `ApiResponse`.
- other core files provide security/trace/middleware-style infrastructure.

## Why it is not runtime context

`app/main.py` only imports FastAPI + `app.api.v1.router`; no core module is registered or called on the chat path.

`pyproject.toml` does not declare the full dependency set needed by copied core. Therefore:

```text
FILE_EXISTS != RUNTIME_ACTIVE
```

## Editing rule

A task that asks to standardize AI response/auth/DB may choose to wire or replace this core, but that is an architecture/dependency change and requires an approved plan. Until then, describe current behavior from the minimal chat path, not from copied helpers.
