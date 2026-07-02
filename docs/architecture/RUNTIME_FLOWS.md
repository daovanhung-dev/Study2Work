# Study2Work Runtime Flows

| Field | Value |
|---|---|
| Status | Canonical |
| Updated | 2026-07-02 |
| Scope | Server/client runtime flow |

## 1. Synchronous API Flow

```text
Client app
-> /api/v1 HTTP request
-> trace middleware accepts or creates X-Trace-Id
-> FastAPI route validates request shape
-> auth dependency identifies actor
-> authorization checks role and ownership/scope
-> application command/query handler
-> domain rules apply invariants and state transitions
-> repository/provider port
-> infrastructure adapter
-> database/cache/provider
-> response mapper
-> standard envelope with traceId
-> Client app state and UI update
```

## 2. Mutation Flow

```text
Client command
-> API validation and authorization
-> application handler opens transaction
-> domain entity changes state
-> repository persists changes
-> audit/outbox record is written when relevant
-> transaction commits
-> response envelope is returned
```

Mutation APIs must define idempotency, concurrency, audit and event behavior in their API DD before implementation.

## 3. Async Worker Flow

```text
API transaction commits source-of-truth data
-> outbox/event/job is published after commit
-> Celery worker receives job
-> worker calls provider or long-running operation
-> worker persists result or failure evidence
-> notification/event may be emitted
-> client reads result through API
```

Async work is required for AI provider calls, grading orchestration, notification dispatch and analytics aggregation.

## 4. Database Migration Flow

```text
Approved API DD or data design
-> SQLAlchemy model/repository change
-> Alembic migration
-> local migration validation
-> tests
-> deployment migration
```

Migrations are not created for speculative modules. They follow approved implementation slices.

## 5. Error And Trace Flow

```text
Failure
-> domain/application or infrastructure exception
-> registered exception handler
-> safe error envelope
-> X-Trace-Id response header
-> structured server log with traceId
-> client support/debug surface
```

Errors must not leak passwords, tokens, private PII, hidden tests, raw prompts with sensitive data or provider secrets.

## 6. API DD Gate

```text
BD/API checklist row
-> API DD draft
-> review and approval
-> server implementation
-> client consumption
-> tests and worklog evidence
```

The health endpoint is the only implemented foundation API. Study business APIs stay blocked until approved API DD exists or the user explicitly asks for a prototype.
