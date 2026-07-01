# Study2Work Project Context

## Scope

Study2Work in this repository implements the Study scope only:

- Identity and profile
- Learning journey
- Practice and assessment
- Mentor workflow
- Project and teamwork
- AI learning support
- Community, notification, admin, and platform governance

Do not implement employer, recruitment, job, application, matching, shortlist, offer, CV builder, AI CV review, or AI interview assistant features.

## Source Of Truth

| Priority | Source |
|---|---|
| 1 | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| 2 | Approved API DD under `docs/api-dd/` |
| 3 | Accepted ADR under `docs/adr/` |
| 4 | `.codex/BACKEND_ARCHITECTURE.md` for backend coding rules |
| 5 | Current code as implementation evidence |

When sources conflict, preserve BD scope and write `CONFLICT` or `OPEN_QUESTION`.

## Canonical Technology

- Backend: Python 3.12+ with FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic, PostgreSQL, Redis, Celery.
- Python Redis client version follows the Celery/Kombu-compatible range in `services/api/pyproject.toml`; Redis server can run Redis 7 in Docker Compose.
- Backend location: `services/api`.
- Web: Vue 3 + TypeScript + Vite.
- Mobile: Flutter.
- API contract: `/api/v1`, JSON by default, standard response envelope, `traceId` on every response.
- Tests: pytest for backend, Vitest/Playwright for web when implemented.

## Current Backend State

`services/api` is a runnable foundation with:

- FastAPI application factory
- Trace middleware
- Standard success/error envelope helpers
- Health endpoint at `GET /api/v1/health`
- SQLAlchemy async database foundation
- Alembic skeleton
- Celery app foundation
- Study-only module folders
- Ruff, mypy, and pytest configuration

No Study business API is implemented until its API DD is `APPROVED`.

## Required Session Workflow

1. Read `AGENTS.md`.
2. Read `.agent/AGENT_GUIDE.md`.
3. Read `.agent/context/CONTEXT_INDEX.md`.
4. Read `.agent/worklog/INDEX.md`.
5. Read the relevant checklist and BD/API DD/diagram context.
6. Implement only the requested scope.
7. Run relevant checks.
8. Update worklog and checklist evidence.
