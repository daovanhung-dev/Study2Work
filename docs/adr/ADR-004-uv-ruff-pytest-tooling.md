# ADR-004: uv, Ruff, mypy, and pytest

| Field | Value |
|---|---|
| Status | `ACCEPTED` |
| Date | `2026-07-01` |
| Decision owner | Backend Lead |
| Scope | Study backend tooling |

## Context

The backend needs reproducible dependency management, fast lint/format checks, type checking, and test execution.

## Decision

Use:

- `uv` for dependency and environment management.
- `ruff` for lint and format checks.
- `mypy` for static typing.
- `pytest` for backend tests.

## Consequences

- Backend commands run from `services/api`.
- Verification baseline is `uv sync`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy app`, and `uv run pytest`.
- Formatting should be checked unless a task explicitly allows rewriting.

