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
- Study Web is an Angular 22 standalone SPA boundary with a readiness root,
  SH-02/SH-03 presentation routes, Guest GS-01–GS-03 route group with #05–#08
  callers, Student ST-11–ST-26 and Admin AD-01–AD-25 route groups. Selected
  Admin GET/POST callers use `AdminApiService`; AD-02 creates users with API #105 then refreshes the same API #68 list query; Guest callers use the generic
  `StudyApiService`. `GS03Page` calls #08 and owns the `?tab=curriculum` view;
  after #08 succeeds it calls API #09 through GS03-local data-access and renders
  only lesson title/order. Focused GS03 tests cover the tab; browser/live
  API/DB runtime remains unverified. Mentor route group/callers remain absent.
  `AdminSessionService` is Admin-only; Shared/Student/Mentor session flows are
  not implemented. The Angular dev proxy forwards relative `/api/v1` to
  `127.0.0.1:3003`. Study OpenAPI is a placeholder, and production routing
  remains unverified.
- Work mobile apps use direct Neon SQL and are not HTTP consumers of Work server.

## Contract dependencies

| Producer/owner | Contract | Consumer | Implementation status |
|---|---|---|---|
| Work API | `contracts/openapi/work/legacy-web.openapi.json` | Work Web | Matches current Express route source |
| Work target contract | `contracts/openapi/work/openapi.json` | Future Work API | DISCREPANCY / not wired to current source |
| Study | `study.evidence.upserted.v1.schema.json` | Work | Consumer missing |
| Study | `study.evidence.revoked.v1.schema.json` | Work | Consumer missing |
| Study API #105 `POST /api/v1/admin/users` | API catalog + FastAPI local route | Study Web AD-02 via `AdminApiService` | Source-wired locally; #68 refresh follows a validated 201; live schema/deployment unverified |
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
