# Study2Work Agent Guide

This repository is the rebuilt Study2Work monorepo. Do not restore the old BD/DD/checklist/worklog governance.

## Source Of Truth

1. `docs/architecture/PROJECT_ARCHITECTURE.md`
2. `docs/architecture/API_CONVENTIONS.md`
3. `contracts/`
4. Current code

Root `../docs` may be used as reference material, but changes in this repo should be expressed through architecture docs, contracts, code, and tests.

## Runtime Boundaries

- Study and Work have separate frontend, backend, database, Redis, and deployment concerns.
- Study API does not query Work database.
- Work API does not query Study database.
- Integration happens through signed/versioned contracts under `contracts/events/study-work`.
- Shared code is allowed for tooling and contracts, not business runtime logic across Python and TypeScript.

## Required Checks

- `docker compose config`
- `corepack pnpm lint`
- `corepack pnpm typecheck`
- `corepack pnpm test`
- `corepack pnpm build`
- From `apps/study-api`: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy app`, `uv run pytest`

## Edit Rules

- Keep API responses on the standard envelope.
- Keep `X-Trace-Id` propagation in every API.
- Keep business logic out of route/controller handlers.
- Do not commit secrets, raw tokens, password hashes, signed URLs, or private PII.
- `../L2E` remains untouched unless the user explicitly asks for a legacy migration task.
