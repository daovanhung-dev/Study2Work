# Study2Work Backend Architecture

## Architectural Model

The Study2Work backend is a FastAPI modular monolith shaped by Clean Architecture, Ports and Adapters, and DDD bounded contexts.

The full canonical server documentation lives in `docs/architecture/SERVER_ARCHITECTURE.md`. This file is a compact coding reference for agents.

Dependencies point inward:

```text
presentation -> application -> domain
infrastructure -> application/domain ports
domain -> no framework dependency
```

FastAPI, SQLAlchemy, Redis, Celery, object storage, LLM providers, and email/push providers are infrastructure details. Domain and application code must not depend on FastAPI request/response objects or SQLAlchemy sessions directly.

## Runtime Layout

```text
services/api/
|-- app/
|   |-- core/
|   |   |-- api.py
|   |   |-- config.py
|   |   |-- database.py
|   |   |-- exceptions.py
|   |   |-- logging.py
|   |   |-- middleware.py
|   |   |-- responses.py
|   |   `-- trace.py
|   |-- modules/
|   |   |-- identity/
|   |   |-- profile/
|   |   |-- learning/
|   |   |-- assessment/
|   |   |-- project/
|   |   |-- mentor/
|   |   |-- ai/
|   |   |-- notification/
|   |   |-- community/
|   |   `-- platform/
|   |-- shared/
|   |-- workers/
|   `-- main.py
|-- alembic/
|-- tests/
`-- pyproject.toml
```

Each business module uses this internal structure:

```text
module/
|-- domain/          # entities, value objects, domain services, repository ports
|-- application/     # commands, queries, DTOs, use case handlers, mappers
|-- infrastructure/  # SQLAlchemy models/repositories, provider adapters, jobs
`-- presentation/    # FastAPI routes, schemas, dependencies
```

## API Rules

- Prefix all endpoints with `/api/v1`.
- Return the standard envelope:
  - success: `businessCode`, `message`, `timestamp`, `traceId`, `data`
  - error: `businessCode`, `message`, `timestamp`, `traceId`, `errors`
- Accept or generate `X-Trace-Id`; always return it as a response header.
- Protected endpoints must check authentication, RBAC, ownership/scope, validation, and state transition.
- Business logic must live in application/domain layers, not route handlers.
- List endpoints must paginate.
- Mutation APIs must document transaction, idempotency, audit, events, and async side effects in the API DD.

## Persistence Rules

- Use PostgreSQL.
- Use SQLAlchemy 2.0 async models and repositories in infrastructure.
- Use Alembic for all schema changes.
- Use UUID primary keys, UTC timestamps, and snake_case database names.
- Use database constraints for uniqueness and relationships.
- Store uploaded artifacts through `file_asset`; do not store raw object-storage URLs as business references.

## Async Rules

- Use Celery with Redis for AI, grading orchestration, email/push, analytics aggregation, and other long-running work.
- The Redis server may run Redis 7; keep the Python Redis client in the Celery/Kombu-compatible range declared in `services/api/pyproject.toml`.
- Publish cross-context facts only after the source transaction commits.
- Prefer outbox-style retry-safe dispatch.
- Untrusted learner code must run only in the isolated grader runner, never in the API process.

## Adding A Business API

1. Confirm the API exists in `docs/checklists/API.md`.
2. Create or read the API DD under `docs/api-dd/<module>/<api-code>/`.
3. Do not implement until DD status is `APPROVED`, unless the user explicitly requests a prototype.
4. Add presentation route/schema.
5. Add application command/query handler.
6. Add domain invariants/state transitions.
7. Add infrastructure repository/adapters.
8. Add tests: unit, integration/API, and negative permission/state cases as appropriate.
9. Update checklist, worklog, and DD changelog if the design changed.

## Current Public Foundation API

`GET /api/v1/health`

Returns:

```json
{
  "businessCode": "SYSTEM-HEALTH-SUCCESS",
  "message": "Service is healthy.",
  "timestamp": "2026-07-01T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "data": {
    "status": "ok",
    "service": "study2work-api",
    "version": "0.1.0",
    "environment": "local"
  }
}
```
