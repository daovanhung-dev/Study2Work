# Worklog - 0002 context_backend_refactor

| Field | Value |
|---|---|
| Session | `0002` |
| Time | `2026-07-01 Asia/Saigon` |
| Module | `GLOBAL_CONTEXT/BACKEND` |
| Feature/function | Agent context migration and FastAPI backend foundation |
| Status | `DONE` |

## Goal

Move agent context into `.agent`, make agent-facing context English, replace the empty NestJS-like backend skeleton with the canonical Study-only FastAPI foundation, and publish backend architecture context for future Codex work.

## Context Read

- BD: `docs/BD/Study2Work_Study_BD_Codex_Ready.md`
- DD: no approved business API DD; only foundation health endpoint was implemented
- Checklist: `docs/checklists/API.md`
- Architecture context: `.codex/PROJECT_CONTEXT.md`, `.codex/BACKEND_ARCHITECTURE.md`

## Files Created Or Modified

| Path | Action | Note |
|---|---|---|
| `AGENTS.md` | modified | Root English bootstrap that points agents to `.agent/AGENT_GUIDE.md`. |
| `.agent/` | created/moved | Agent guide, workflow, context index, status model, skills index and worklog moved from the legacy documentation directories. |
| `.codex/PROJECT_CONTEXT.md` | created | English project scope and technology context for future coding agents. |
| `.codex/BACKEND_ARCHITECTURE.md` | created | English backend architecture guide for FastAPI modular monolith work. |
| `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | modified | Remaining Vietnamese context phrases translated to English without changing rule IDs or business semantics. |
| `services/api/` | created | FastAPI, Pydantic v2, SQLAlchemy async, Alembic, Celery, Redis, Ruff, mypy and pytest foundation. |
| `docker-compose.yml` | modified | Development runtime for API, PostgreSQL and Redis. |
| `docs/adr/ADR-001-canonical-study-backend-fastapi.md` | created | Records FastAPI/Python as canonical Study backend. |
| `docs/adr/ADR-002-sqlalchemy-alembic.md` | created | Records SQLAlchemy 2.0 async and Alembic. |
| `docs/adr/ADR-003-celery-redis-worker.md` | created | Records Celery + Redis worker direction. |
| `docs/adr/ADR-004-uv-ruff-pytest-tooling.md` | created | Records uv, Ruff, mypy and pytest tooling. |
| `docs/DD/Study2Work_API_DD_Template/` | modified | Template translated to English and guarded for Study-only API DD use. |
| `docs/checklists/API.md` | modified | Added `SYSTEM-HEALTH-001` foundation endpoint evidence. |
| `docs/architecture/BACKEND_ARCHITECTURE_USAGE_VI.md` | created | Vietnamese backend architecture usage guide. |
| Legacy backend and out-of-scope placeholders | deleted | Removed empty legacy backend and removed-scope placeholders. |

## Logic Changed

- Added FastAPI application factory, `GET /api/v1/health`, trace middleware, standard success/error envelope helpers, structured logging, configuration, exception handling and module router registration.
- Added Study-only backend module skeletons: `identity`, `profile`, `learning`, `assessment`, `project`, `mentor`, `ai`, `notification`, `community`, `platform`.
- Added SQLAlchemy async base/session foundation, Alembic skeleton and Celery app foundation.
- Resolved dependency compatibility by using the Celery/Kombu-compatible Python Redis client range `redis>=5.0.3,<6.5`.
- Kept all Study business APIs unimplemented until their API DD reaches `APPROVED`.

## Tests Run

| Command/check | Result | Evidence |
|---|---|---|
| `uv sync` | PASS | Dependencies resolved after Redis client range was corrected. |
| `uv run ruff check .` | PASS | `All checks passed!` |
| `uv run ruff format --check .` | PASS | `69 files already formatted` |
| `uv run mypy app` | PASS | `Success: no issues found in 66 source files` |
| `uv run pytest` | PASS | `4 passed`; one Starlette/httpx deprecation warning from dependency stack. |
| `docker compose config` | PASS | Compose file resolved for API, PostgreSQL and Redis services. |
| `git diff --check` | PASS | No whitespace errors; Git reported line-ending conversion warnings only. |
| Old context reference search | PASS | No active references to legacy context paths remain. |
| Buildable banned-scope search | PASS | No removed-scope placeholder code remains under buildable app/service paths. |
| Project context language scan | PASS | No Vietnamese diacritics or mojibake found in `.agent`, `.codex`, canonical BD, DD template, checklists or backend files. |

## Bugs Found

| ID | Status | Description | Link |
|---|---|---|---|
| `BUG-0002-001` | `FIXED` | Initial `uv sync` failed because `redis>=7.0.0` conflicted with `celery[redis]`/Kombu requirements. | `services/api/pyproject.toml` |
| `BUG-0002-002` | `FIXED` | Initial pytest run could not import `app`; pytest `pythonpath` was added. | `services/api/pyproject.toml` |
| `BUG-0002-003` | `FIXED` | `.codex/BACKEND_ARCHITECTURE.md` had box-drawing mojibake; replaced with ASCII tree. | `.codex/BACKEND_ARCHITECTURE.md` |

## Risks Or Unverified Points

- Docker Compose file was created but not started in this session.
- `pytest` reports a dependency deprecation warning: FastAPI/Starlette TestClient currently suggests `httpx2` for the future.
- No business API implementation was attempted because no business API DD is approved.

## Next Work

- Start Phase S1 by creating/approving DDs for `AUTH-REGISTER-001`, `AUTH-LOGIN-001`, `AUTH-VERIFY-001` and `USER-PROFILE-001`.
- Add initial Alembic migration only after the first approved domain/data slice is selected.

## Suggested Commit Message

`refactor(backend): establish study fastapi foundation and agent context`
