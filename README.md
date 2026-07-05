# Study2Work

Study2Work is a rebuilt polyglot monorepo for two independent product subsystems:

- **Study**: learning, courses, lessons, assessment, progress, and evidence issuance.
- **Work**: career profile, CV, portfolio, jobs, applications, and recruiter workflow.

The repository intentionally no longer uses the old BD/DD/checklist governance. Architecture docs and versioned contracts are the source of truth for this foundation pass.

## Runtime Map

| Area | Path | Stack |
|---|---|---|
| Study web | `apps/study-web` | Vue 3, TypeScript, Vite |
| Study API | `apps/study-api` | FastAPI, Python, SQLAlchemy, Alembic |
| Work web | `apps/work-web` | React, TypeScript, Vite |
| Work API | `apps/work-api` | NestJS, Fastify, Prisma |
| Platform identity | `apps/platform-identity` | Local JWKS and identity notes |
| Contracts | `contracts` | OpenAPI placeholders, event JSON Schema, skill taxonomy |
| Infra | `infra`, `docker-compose.yml` | Local PostgreSQL, Redis, MinIO, Mailhog |

## Commands

Install JavaScript dependencies:

```powershell
corepack pnpm install
```

Validate contracts and JavaScript apps:

```powershell
corepack pnpm lint
corepack pnpm typecheck
corepack pnpm test
corepack pnpm build
```

Run Study API checks:

```powershell
cd apps/study-api
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

Validate local compose:

```powershell
docker compose config
```

## API Baseline

Both APIs expose:

- `GET /health/live`
- `GET /health/ready`

All new API responses use the standard envelope:

```json
{
  "success": true,
  "businessCode": "CODE",
  "message": "Safe message",
  "data": {},
  "meta": {},
  "traceId": "uuid"
}
```

## Scope Guard

`../L2E` is legacy reference only. Root-level `../docs` is external planning input only. This repo owns the new runnable foundation.
