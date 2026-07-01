# Study2Work Agent Guide

Study2Work in this repository is standardized for the Study scope only: learning, practice, assessment, mentor workflow, teamwork, AI learning support, notifications, community, and platform governance.

`docs/BD/Study2Work_Study_BD_Codex_Ready.md` is the canonical Study business source. Do not expand into recruitment, employer, job, CV, interview, matching, shortlist, offer, or hiring workflows unless a separate approved BD/DD exists.

## Source Of Truth

1. Approved BD -> approved API DD -> accepted ADR/decision -> current code as implementation evidence.
2. Current code is not automatically correct business truth when it conflicts with BD/DD/ADR.
3. If documents conflict, write `CONFLICT` or `OPEN_QUESTION`; do not decide business rules silently.
4. Do not code against a `DRAFT` or `IN_REVIEW` API DD unless the user explicitly requests a prototype.

## Canonical Stack

- Backend: Python 3.12+ with FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL, Redis, Celery.
- Backend location: `services/api`.
- Web dashboards: Vue 3 + TypeScript + Vite.
- Mobile: Flutter.
- Legacy `backend/` NestJS-like skeleton is not canonical for Study backend implementation.
- Worker/grading/AI/email/analytics are asynchronous; untrusted code never runs in the main API process.

## Commands

| Task | Command | Notes |
|---|---|---|
| Discover files | `rg --files` | Use before opening many files. |
| Search docs/code | `rg "<keyword>" <path>` | Search by module, feature, business code, or file path. |
| Backend install | `uv sync` from `services/api` | Creates/updates the Python environment. |
| Backend lint | `uv run ruff check .` from `services/api` | Does not rewrite files. |
| Backend format check | `uv run ruff format --check .` from `services/api` | Use check mode unless formatting is requested. |
| Backend type check | `uv run mypy app` from `services/api` | Static typing gate. |
| Backend tests | `uv run pytest` from `services/api` | Unit/API tests. |
| Whitespace check | `git diff --check` | Run before final response. |

## Code Rules

- Before code changes, identify module, feature/function, actor, source BD/DD/checklist, affected files, and expected tests.
- Keep business logic out of FastAPI route handlers. Routes parse, authorize, call application services, and map responses.
- Domain/application layers own invariants and state transitions.
- Protected APIs must check authentication, RBAC, ownership/scope, validation, state transition, and return the standard response envelope.
- Response envelopes must include `businessCode`, `message`, `timestamp`, `traceId`, and `data` or `errors`.
- Do not log or document secrets, tokens, passwords, OAuth secrets, hidden tests, raw prompts with sensitive data, or private PII.
- Use `file_asset` for uploaded artifacts; never store raw object-storage URLs as the business reference.
- Use outbox/retry-safe async dispatch for cross-context effects.

## Documentation Rules

- Read context progressively; do not read the entire repo or entire `docs/` tree blindly.
- Every change must trace to BD, API DD, checklist, worklog, issue, or ADR.
- Dynamic implementation status belongs in checklists/worklogs, not in root `AGENTS.md`.
- If design changes, update the relevant DD changelog or record an `OPEN_QUESTION`.
- Do not create duplicate module checklists.
- Agent-facing context must be English, except intentionally Vietnamese user-facing guides.

## Required Workflow

- Start with `AGENTS.md`, `.agent/AGENT_GUIDE.md`, `.agent/context/CONTEXT_INDEX.md`, and `.agent/worklog/INDEX.md`.
- Before coding, read the relevant checklist, BD sections, approved API DD, diagrams, `.codex` context, and affected code.
- After coding, run relevant checks, create a new worklog, update `.agent/worklog/INDEX.md`, update checklists, and update DD/ADR docs if design changed.
- Full workflow: `.agent/context/WORKFLOW.md`.

