# Study2Work Work API

This module is the Express backend for Study2Work Work Web. It owns the JSON API,
Prisma schema, Neon PostgreSQL integration, JWT Bearer authentication, and upload
handling for student and business flows. The React frontend lives in
`apps/work-client/web` and is a separate deployable.

## Features

- Student registration plus student/business sign-in flows; business registration remains unwired.
- Role-based protected routes for students and businesses.
- Student job browsing, CV creation/update, and applications through `/api/v1`.
- Business job posting, job management, applicant list, and CV detail through `/api/v1`.
- React owns all browser pages; no server-side view engine is mounted.
- Admin remains unwired because no Admin API is exposed by the current server.
- Prisma data models and migrations for Neon PostgreSQL persistence.

## Stack

- Node.js, TypeScript, Express
- React frontend is a separate Vite package at `apps/work-client/web`.
- JWT Bearer authentication (`Authorization: Bearer <token>`)
- Prisma ORM and Neon PostgreSQL
- Multer for runtime uploads
- Supabase client configuration for existing integrations

## Structure

```text
.
+-- prisma/       # Prisma schema and migrations
+-- public/       # Static assets
+-- src/
|   +-- api/v1.ts     # Versioned route composition only
|   +-- core/         # Config, DI, trace, responses, exceptions, security
|   +-- modules/      # models/validate/view/query per wired domain
|   +-- config/       # Upload and legacy integration config
|   +-- middleware/   # JWT authentication boundary
|   +-- routes/       # Compatibility re-export for old imports
|   +-- services/     # Legacy/unwired services kept for compatibility
+-- uploads/      # Runtime uploads, ignored except .gitkeep
```

The request lifecycle is intentionally Study-style while remaining Express and
Prisma-native:

```text
main -> createApp -> config/middleware/trace/auth -> api/v1
     -> models/validate -> view/use-case -> query/repository -> Prisma
     -> canonical response or centralized exception handler
```

## Setup

```bash
npm install
npm run prisma:generate
npm run prisma:migrate:deploy
npm run s2w
```

From the repository root, the equivalent split development commands are:

```bash
corepack pnpm --filter work_server prisma:validate
corepack pnpm --filter work_server prisma:generate
corepack pnpm --filter work_server typecheck
corepack pnpm --filter work_server test
corepack pnpm --filter work_server s2w
corepack pnpm --filter work-web dev
```

Vite runs on `http://127.0.0.2:3001` and proxies `/api`, `/uploads`, and `/img`
to the Express server on `127.0.0.1:3002`. Production should use a same-origin reverse
proxy for these paths. The React client never receives the Neon credential. The
Express server exposes JSON APIs and does not serve browser HTML.

The React API boundary is `/api/v1` and returns the envelope
`success`, `businessCode`, `message`, `data`, `meta`, and `traceId`. The detailed
API contract is in
[`contracts/openapi/work/legacy-web.openapi.json`](../../contracts/openapi/work/legacy-web.openapi.json).

PowerShell:

```powershell
npm install
npm run prisma:generate
npm run prisma:migrate:deploy
npm run s2w
```

The server reads typed runtime configuration from the static
`src/utils/constants.ts` through `src/core/config.ts`; it does not load
`.env` or read configuration from `process.env`. Required constants are
validated during bootstrap.

Prisma migration commands use the direct Neon endpoint through the local CLI
wrapper. `APP_ENV` and `REDIS_URL` are optional; Redis is reported as
configured/not_configured by readiness and does not add a runtime Redis
dependency.

System routes are now wired:

- `GET /api/v1` → `SYSTEM_ROOT_LOADED`
- `GET /health/live` → `SYSTEM_HEALTH_LIVE`
- `GET /health/ready` → `SYSTEM_HEALTH_READY`, or `503 DEPENDENCY_UNAVAILABLE`

The target Work catalog still contains domains that are deliberately not wired
in this compatibility refactor (tenant, billing, university, interview,
storage and webhook operations).

## Configuration and authentication

| Constant                | Purpose                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| `PORT`                | HTTP port for the Express server (`3002` locally).                |
| `DATABASE_URL`        | Pooled Neon PostgreSQL connection string used by Prisma runtime. |
| `DIRECT_DATABASE_URL` | Direct Neon PostgreSQL connection string used by Prisma CLI.     |
| `JWT_SECRET`          | Secret for JWT helpers.                                          |
| `JWT_EXPIRES`         | JWT expiration value.                                            |
| `JWT_STORAGE_KEY`     | Browser local-storage key for the access token.                  |
| `SUPABASE_URL`        | Supabase project URL.                                            |
| `SUPABASE_ANON_KEY`   | Supabase anonymous key for legacy, unwired modules.              |

`DATABASE_URL`, `DIRECT_DATABASE_URL` and `JWT_SECRET` are required static
constants.
`JWT_SECRET` must contain at least 32 characters. `PORT` defaults to `3000` and
`JWT_EXPIRES` defaults to `1d`. Keep all credentials out of logs,
documentation, tests and tracked source files.

Passwords are stored as bcrypt hashes. Existing legacy plaintext rows remain
login-compatible and are opportunistically rehashed after a successful login.
Protected requests must send exactly one `Authorization: Bearer <JWT>` header.
The server does not authenticate from cookies or maintain server-side sessions.
Logout removes the token from the browser, while already-issued JWTs remain
valid until they expire.
