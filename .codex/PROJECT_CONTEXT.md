# Study2Work Project Context

## Scope And Runtime Split

Study2Work in this repository implements the Study scope only:

- Identity and profile
- Learning journey
- Practice and assessment
- Mentor workflow
- Project and teamwork
- AI learning support
- Community, notification, admin, and platform governance

Do not implement removed non-Study workflows unless a future approved BD, ADR and API DD expand scope.

The project has two runtime sides:

- Server: `services/api`
- Client: `apps/*`

## Source Of Truth

| Priority | Source |
|---|---|
| 1 | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| 2 | Approved API DD under `docs/api-dd/` |
| 3 | Accepted ADR under `docs/adr/` |
| 4 | `docs/architecture/PROJECT_ARCHITECTURE.md` |
| 5 | `docs/architecture/SERVER_ARCHITECTURE.md` and `docs/architecture/CLIENT_ARCHITECTURE.md` |
| 6 | `.codex/BACKEND_ARCHITECTURE.md` for compact backend coding rules |
| 7 | Current code as implementation evidence |

When sources conflict, preserve BD scope and write `CONFLICT` or `OPEN_QUESTION`.

## Canonical Technology

- Backend: Python 3.12+ with FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic, PostgreSQL, Redis, Celery.
- Python Redis client version follows the Celery/Kombu-compatible range in `services/api/pyproject.toml`; Redis server can run Redis 7 in Docker Compose.
- Backend location: `services/api`.
- Web client locations: `apps/web-public`, `apps/web-student`, `apps/web-mentor`, `apps/web-admin`.
- Web stack when implemented: Vue 3 + TypeScript + Vite, with Vue Router and Pinia.
- Mobile client location: `apps/mobile-app`.
- Mobile stack when implemented: Flutter.
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

## Current Client State

`apps/*` contains Study-scope skeleton folders only. Client apps are intentionally not runnable yet in the current architecture refactor.

## Required Session Workflow

1. Read `AGENTS.md`.
2. Read `.agent/AGENT_GUIDE.md`.
3. Read `.agent/context/CONTEXT_INDEX.md`.
4. Read `.agent/worklog/INDEX.md`.
5. Read `docs/architecture/PROJECT_ARCHITECTURE.md`.
6. Read the relevant checklist and BD/API DD/diagram context.
7. Implement only the requested scope.
8. Run relevant checks.
9. Update worklog and checklist evidence.
