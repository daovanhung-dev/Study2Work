# Dependency map

## Server map

```text
apps/study-server/app/main.py
  -> app/api/v1.py
       -> app.modules.guest.register_account.* (register route)
  -> app/core/* (current composition)
  -> PostgreSQL settings; Redis is config-only
  -> app/service/ai/OllamaService (no live caller)

apps/ai-server/app/main.py
  -> app/api/v1.py
  -> app/module/chat/{chat,model,view}.py
  -> app/service/ai/ollama_service.py
  -> Ollama /api/generate
  x copied app/core/* is UNWIRED

apps/work-client/web/src/main.tsx
  -> React App -> AuthProvider/Zustand + React Query
  -> relative `/api/v1` fetch boundary
  -> apps/work-server/src/app.ts

apps/work-client/mobile/flutter_{student,business}/lib/main.dart
  -> login/home views and controllers
  -> helper_db -> NeonDatabase -> Neon PostgreSQL
  -> SQLite session/cache helpers
  -> AIService -> Gemini HTTP API

apps/work-server/src/main.ts
  -> shared Prisma `$connect()`
  -> Express app -> `/api/v1` JSON router
  -> Prisma -> Work PostgreSQL/Neon

apps/db-admin-web/src/main.ts
  -> Angular standalone routes/material UI/CodeMirror
  -> same-origin `/api/v1/admin/*` through Angular dev proxy
  -> local launcher starts apps/db-admin-server before serving the UI
  -> in-memory access token only

apps/db-admin-server/app/main.py
  -> FastAPI routes and canonical response envelope
  -> `app/core/constants.py` -> SQLAlchemy + psycopg3 -> one Neon database
  -> OIDC/JWKS identity provider for server-side permissions
```

## Client/server boundaries

- Work web uses a relative `/api/v1` base; Vite binds at `127.0.0.2:3001` and
  proxies `/api`, `/uploads`, and `/img` to the Express server at
  `127.0.0.1:3002` in development. Work API does not render browser views.
- Study client and Study API are separate packages, nhưng current Study OpenAPI
  không đủ để suy diễn client/server contract.
- Work mobile apps use direct Neon SQL and are not HTTP consumers of Work server.

## Contract dependencies

| Producer/owner | Contract | Consumer | Implementation status |
|---|---|---|---|
| Work API | `contracts/openapi/work/legacy-web.openapi.json` | Work Web | Matches current Express route source |
| Work target contract | `contracts/openapi/work/openapi.json` | Future Work API | DISCREPANCY / not wired to current source |
| Study | `study.evidence.upserted.v1.schema.json` | Work | Consumer missing |
| Study | `study.evidence.revoked.v1.schema.json` | Work | Consumer missing |
| Shared | `skill-taxonomy.v1*.json` | Future domain modules | No current server caller |
| DB Admin | `/api/v1/admin/*` | `apps/db-admin-web/` | Implemented locally; no shared contract file yet |

Event contract yêu cầu signature-first validation, JSON Schema, idempotency và
local snapshot. Không có nghĩa các helper/table tương ứng đã tồn tại.

## Test dependencies

- Study `app.main` hiện import được; register flow nằm dưới
  `app.modules.guest.register_account.*` và test tương ứng dùng cùng namespace.
- AI không có tests.
- Work Web has Vitest tests for role guards and Bearer API boundary. Work server
  has no checked-in test runner; TypeScript/Prisma commands are validation checks.
- Root `tests/smoke_test.py` là stale standalone artifact, không phải test router
  cho package hiện hành.
