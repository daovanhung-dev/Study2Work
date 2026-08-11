# Work API

`apps/work-server` is the independently deployed backend for the Work
subsystem. It is a NestJS application using Fastify, Prisma, PostgreSQL, and
Redis. Its public API is rooted at `/api/v1`; unauthenticated health checks are
available at `/health/live` and `/health/ready`.

The Work browser application lives separately in
[`apps/work-client/web`](../work-client/web). This API does not serve that
application's HTML, static assets, or client-side routes.

## Commands

From the repository root:

```bash
corepack pnpm --filter work-api prisma:generate
corepack pnpm --filter work-api db:migrate
corepack pnpm --filter work-api start:dev
```

Use `corepack pnpm --filter work-api build` and
`corepack pnpm --filter work-api start` for a production build. The root aliases
`corepack pnpm dev:work-server` and `corepack pnpm dev:work-web` start the two
separate local processes.

## Environment

Copy `.env.example` to `.env` and configure these variables:

| Variable | Purpose |
| --- | --- |
| `WORK_APP_ENV` | `local`, `test`, `staging`, or `production`. |
| `WORK_HOST`, `WORK_PORT` | Bind address and HTTP port (default `8001`). |
| `WORK_DATABASE_URL` | PostgreSQL datasource used by Prisma and the API. |
| `WORK_REDIS_URL` | Optional Redis adapter URL. |
| `WORK_CORS_ORIGINS` | Comma-separated browser origins; local Work web uses `http://localhost:5174`. |
| `WORK_JWKS_URL`, `WORK_JWT_ISSUER`, `WORK_JWT_AUDIENCE` | Identity token-verification configuration. |

## Persistence and legacy cutover

Prisma starts a clean PostgreSQL migration history. It does not connect to,
migrate, or depend on the retired Learn2Earn MySQL schema. Work domain tables
are introduced through canonical-BD-aligned migrations as their modules are
implemented.

The legacy Express/EJS runtime, templates, and static assets were removed from
this backend. Do not reintroduce a web-serving path here; all browser work
belongs in `apps/work-client/web`.
