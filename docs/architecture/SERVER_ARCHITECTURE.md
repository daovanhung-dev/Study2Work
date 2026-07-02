# Study2Work Server Architecture

| Field | Value |
|---|---|
| Status | Canonical |
| Updated | 2026-07-02 |
| Server root | `services/api` |
| Framework | FastAPI |

## 1. Responsibility

`services/api` is the only canonical backend. It owns HTTP APIs, application use cases, domain rules, persistence adapters, migrations, async worker configuration and backend tests.

No Study business API may be implemented until its API Detail Design is approved, except for explicitly requested prototypes. The current implemented foundation endpoint is `GET /api/v1/health`.

## 2. Runtime Layout

```text
services/api/
|-- app/
|   |-- core/          # config, logging, database, response envelope, errors, middleware
|   |-- modules/       # Study bounded contexts
|   |-- shared/        # cross-module primitives with no business ownership
|   |-- workers/       # Celery app and worker bootstrap
|   `-- main.py        # FastAPI application factory
|-- alembic/           # migration environment and migration scripts
|-- tests/             # pytest suite
|-- Dockerfile
|-- pyproject.toml
`-- uv.lock
```

Each module follows this structure:

```text
module/
|-- presentation/      # FastAPI routers, schemas, auth dependencies, response mapping
|-- application/       # commands, queries, DTOs, use case handlers, ports
|-- domain/            # entities, value objects, rules, domain events
`-- infrastructure/    # SQLAlchemy models/repos, provider adapters, worker jobs
```

## 3. Request Flow

```text
Client
-> FastAPI route in presentation
-> parse and validate request
-> authenticate, authorize, check ownership/scope
-> application command/query handler
-> domain rules and state transitions
-> repository/provider port
-> infrastructure adapter
-> database/cache/provider
-> standard response envelope
```

Presentation code must stay thin. It maps HTTP to application input and maps application output to the standard envelope. Business rules belong in application/domain layers.

## 4. Response Envelope

Success responses use:

```json
{
  "businessCode": "MODULE-ACTION-SUCCESS",
  "message": "Safe client message.",
  "timestamp": "2026-07-02T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "data": {}
}
```

Error responses use:

```json
{
  "businessCode": "MODULE-ACTION-ERROR",
  "message": "Safe client message.",
  "timestamp": "2026-07-02T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "errors": []
}
```

## 5. Persistence And Migrations

- PostgreSQL is the server source of truth.
- SQLAlchemy 2.0 async models/repositories live in module infrastructure.
- Alembic is the only migration mechanism.
- Domain/application code should use repository ports, not direct SQLAlchemy sessions.
- Migrations are added only after an approved domain/data slice exists.

## 6. Async And Workers

Celery with Redis is used for long-running or retryable work:

```text
API mutation
-> database transaction
-> outbox/domain event after commit
-> Celery job
-> provider/worker action
-> persisted result or notification
```

Use async workers for AI provider calls, grading orchestration, notifications, analytics aggregation and other slow side effects. Untrusted learner code must run only in an isolated grader boundary, never in the API process.

## 7. Server Verification

Run from `services/api`:

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

Run from the repository root:

```powershell
docker compose config
```
