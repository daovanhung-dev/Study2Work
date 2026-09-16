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
| Work API | `apps/work-server` | Express, TypeScript, Prisma, Neon PostgreSQL, JWT |
| Contracts | `contracts` | OpenAPI baselines, event JSON Schema, skill taxonomy |
| Infra | `infra`, `docker-compose.yml` | Local PostgreSQL, Redis, MinIO, Mailhog |

The Work applications are intentionally independent deployables. `apps/work-server`
owns the Express JSON API, persistence, and upload/static-file endpoints;
`apps/work-client/web` owns the React browser UI. The browser uses relative
`/api/v1`, `/uploads`, and `/img` paths, with Vite proxying those paths to the API
in development and a same-origin reverse proxy expected in production.

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
corepack pnpm --filter work_server prisma:validate
corepack pnpm --filter work_server prisma:generate
corepack pnpm dev:work-server
corepack pnpm dev:work-web
```

Work API listens on port `3000`; Work Web listens on Vite port `5174`. Work
authentication is JWT Bearer-only with the browser token stored under
`access_token`. No Work runtime reads `.env`, cookies, or server-side sessions.

For local Work development, run the API and React dev server as two processes;
the repository does not require a Work container or a browser-side database
connection for this flow.

## Work API boundary

The target Work OpenAPI catalog remains in
[`contracts/openapi/work/openapi.json`](contracts/openapi/work/openapi.json), but
its target-only routes are not mounted by the current Express backend. React
uses the current route contract in
[`contracts/openapi/work/legacy-web.openapi.json`](contracts/openapi/work/legacy-web.openapi.json).
Those JSON responses use the standard envelope:

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
