# Study2Work

Study2Work is a rebuilt polyglot monorepo for two independent product subsystems:

- **Study**: learning, courses, lessons, assessment, progress, and evidence issuance.
- **Work**: career profile, CV, portfolio, jobs, applications, and recruiter workflow.

The five canonical Markdown files in [`docs/BD`](docs/BD) are the product and target-design source of truth for V1-PILOT. OpenAPI documents, database migrations, event schemas, tests, and runtime code are executable contracts derived from that Basic Design and must not contradict it. Historical implementation notes outside `docs/BD` are non-normative unless a canonical BD file links to them explicitly.

## Canonical Basic Design

| File | Ownership |
|---|---|
| [`01_TONG_QUAN_DU_AN.md`](docs/BD/01_TONG_QUAN_DU_AN.md) | Scope, business rules, permissions, architecture, security, NFR, rollout, and end-to-end traceability |
| [`02_BIEU_DO_HE_THONG.md`](docs/BD/02_BIEU_DO_HE_THONG.md) | Use-case, activity, class, and sequence diagrams |
| [`03_THIET_KE_CO_SO_DU_LIEU.md`](docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md) | Canonical three-database model, constraints, indexes, locking, retention, and migration policy |
| [`04_DAC_TA_API.md`](docs/BD/04_DAC_TA_API.md) | Public, internal, webhook, event, and realtime contracts |
| [`05_DAC_TA_MAN_HINH.md`](docs/BD/05_DAC_TA_MAN_HINH.md) | Sitemap and screen behavior for every actor and state |

Run `corepack pnpm docs:validate` after changing any canonical BD file. The root `lint` command also runs this quality gate.

## Runtime Map

| Area | Path | Stack |
|---|---|---|
| Study web | `apps/study-client` | Vue 3, TypeScript, Vite |
| Study API | `apps/study-server` | FastAPI, Python, SQLAlchemy, Alembic |
| Work web | `apps/work-client/web` | React, TypeScript, Vite |
| Work API | `apps/work-server` | NestJS, Fastify, TypeScript, PostgreSQL, Redis |
| Contracts | `contracts` | OpenAPI baselines, event JSON Schema, skill taxonomy |
| Infra | `infra`, `docker-compose.yml` | Local PostgreSQL, Redis, MinIO, Mailhog |

The Work applications are intentionally independent deployables. `apps/work-server`
owns HTTP APIs, persistence, and Work integrations; `apps/work-client/web` owns the
browser UI and calls the API through `VITE_WORK_API_URL`. The API does not serve the
web application's static files, templates, or routes.

## Commands

Install JavaScript dependencies:

```powershell
corepack pnpm install
```

Validate contracts and JavaScript apps:

```powershell
corepack pnpm lint
corepack pnpm docs:validate
corepack pnpm typecheck
corepack pnpm test
corepack pnpm build
```

Run Study API checks:

```powershell
cd apps/study-server
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

Run the Work applications locally:

```powershell
corepack pnpm dev:work-server
corepack pnpm dev:work-web
```

Validate local compose:

```powershell
docker compose config
```

Run the separated Work stack in containers:

```powershell
docker compose up --build work-api work-web
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
