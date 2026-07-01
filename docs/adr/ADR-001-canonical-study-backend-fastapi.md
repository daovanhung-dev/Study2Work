# ADR-001: Canonical Study Backend Is FastAPI

| Field | Value |
|---|---|
| Status | `ACCEPTED` |
| Date | `2026-07-01` |
| Decision owner | Tech Lead |
| Scope | Study backend |

## Context

Project inputs previously contained two backend directions: a NestJS-like skeleton and a Python/FastAPI technology proposal. The approved Study BD selects Python 3.12+ and FastAPI for the canonical Study backend.

## Decision

Use Python 3.12+ with FastAPI and Pydantic v2 for the Study backend.

The canonical backend path is `services/api`. The legacy `backend/` skeleton is not used for Study implementation.

## Consequences

- New Study backend code goes under `services/api`.
- Do not mix NestJS controllers and FastAPI in the same deliverable.
- API DD, OpenAPI DTOs, tests, and documentation must target FastAPI.
- Existing NestJS-like folders are treated as superseded placeholders and removed if empty.

