# ADR-003: Celery And Redis For Async Work

| Field | Value |
|---|---|
| Status | `ACCEPTED` |
| Date | `2026-07-01` |
| Decision owner | Backend/DevOps |
| Scope | Study backend async processing |

## Context

The Study BD requires AI, grading orchestration, notifications, and analytics aggregation to run asynchronously. The main API process must not run long AI calls or untrusted code.

## Decision

Use Celery with Redis as the broker/result backend for Study backend async workers.

## Consequences

- Long-running work is queued through Celery.
- Cross-context side effects should be emitted after commit and handled retry-safely.
- Grading code execution remains outside the API process in an isolated runner.
- Worker tasks must propagate `traceId`.

