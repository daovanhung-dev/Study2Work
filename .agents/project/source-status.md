# Source status và discrepancy

Repository deep-context được đối chiếu tại source commit
`9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` ngày 2026-09-18.

## Tài liệu thiết kế

```text
DD_STATUS: NOT_FOUND
CANONICAL_BD_STATUS: NOT_FOUND
BUSINESS_CODE_STATUS: CREATED_FROM_CURRENT_RUNTIME
DIAGRAM_API_CONTRACT_STATUS: APPROVED_DESIGN_CONTRACT
```

- Root README/contract README có chỗ trỏ `docs/BD/`, nhưng directory đó không có trong source snapshot.
- Không dùng template, diagram hoặc Git history để tự hoàn thiện request/response/business rule/database mapping thiếu.
- `docs/lists/list_api.md` và `apps/study-server/docs/diagrams/AC_UNICA/` là
  approved V1 design contract theo yêu cầu được phê duyệt; các schema và
  `DESIGN_*` code ở đó vẫn là `DESIGN_PROPOSAL`, không phải runtime/OpenAPI
  evidence.
- Study DD và business-code artifacts hiện có dưới
  `apps/study-server/docs/dd/` và `apps/study-server/docs/business_code/`.
  Chúng là design/documentation evidence, không tự biến thành runtime wiring.
- Work có hai contract file nhưng runtime source hiện tại khớp
  `contracts/openapi/work/legacy-web.openapi.json`; `openapi.json`/README mô tả
  target health/domain surface chưa được Express route đăng ký.
- Study OpenAPI chỉ có placeholder README; AI không có OpenAPI hiện hành.

## Context system

```text
ROOT_ROUTER: AGENTS.md
CONTEXT_REGISTRY: .agents/AGENTS.md
MANIFEST: .agents/context-manifest.json
VALIDATOR: scripts/validate-agent-context.mjs
STUDY_LEGACY_AGENT_CONTEXT: REMOVED; canonical context is under `.agents/server-study/`
```

Deep scopes:

- `server-study`: `.agents/server-study/AGENTS.md`
- `server-work`: `.agents/server-work/AGENTS.md`
- `server-ai`: `.agents/server-ai/AGENTS.md`
- `db-admin`: `.agents/db-admin/AGENTS.md`
- `web-work`: `.agents/web-work/AGENTS.md`
- `mobile-work`: `.agents/mobile-work/AGENTS.md`

Mọi project context phải nằm dưới `.agents/`; `apps/` không chứa `.agent/` hoặc
`AGENTS.md`.

## Study server

```text
RUNTIME_STATUS: VERIFIED_IMPORT; CURRENT_ROUTE_SOURCE_BACKED
TEST_STATUS: COLLECTION_VERIFIED_AFTER_NAMESPACE_RENAME
BUSINESS_MODULE_STATUS: SOURCE_BACKED_REGISTER_VERIFY_LOGIN_REFRESH_CATEGORIES_COURSES_SEARCH
DATABASE_SCHEMA_STATUS: SOURCE_REQUIRED; LIVE_STATUS_NOT_VERIFIED_HERE
```

Current evidence:

- `app.main` imports successfully and composes 13 current routes.
- `app/api/v1.py` wires `POST /api/v1/auth/register` to
  `app.modules.guest.register_account.*`; `/auth` ở đây là public endpoint
  contract, không phải Python namespace.
- `app/api/v1.py` also wires public API #2 verify-email dispatch through the
  injectable provider stub, API #5 categories, API #6 courses and API #7 course
  search; these flows
  have focused HTTP tests and no live DB verification claim.
- `app/api/v1.py` wires `GET /api/v1/users/me` to
  `app.modules.guest.users_me.*`; the route verifies the current API#3 JWT
  `sub`/`roles` shape, requires `STUDENT`, and reads only public profile
  columns from `users`.
- `register_account/validate.py` is empty/unwired; current model validators
  remain in `models.py`.
- `tests/modules/guest/test_register.py` imports
  `app.modules.guest.register_account.models/view` to stay aligned with the
  runtime namespace.
- `alembic.ini` references a missing migration directory; this is not schema
  evidence.
- `apps/study-server/docs/codebase/README.md` and design DD remain
  non-authoritative when they conflict with current source.

## Work server

```text
RUNTIME_STATUS: SOURCE_CHANGED_STUDY_STYLE_COMPATIBILITY_API
OPENAPI_STATUS: LEGACY_WEB_ALIGNED; SYSTEM_ROUTES_VERIFIED; TARGET_DOMAIN_DISCREPANCY
DATABASE_SCHEMA_STATUS: VERIFIED_PRISMA_12_MODELS
HEALTH_ROUTE_STATUS: VERIFIED_INJECTED_PROBE
```

- `src/main.ts` loads typed config from the tracked static
  `src/utils/constants.ts`, binds the local listener to `127.0.0.1:3002`,
  creates injected dependencies, connects Prisma before listening and gracefully
  disconnects on shutdown; `src/app.ts` exposes `createApp(options)` for
  fake-dependency HTTP tests. `.env` and `process.env` are not runtime config
  sources.
- `src/core/` owns typed config, Prisma factory, trace context, response/error
  envelopes, centralized exception mapping and HS256 security helpers.
- `src/api/v1.ts` only composes route modules. Auth, students, businesses, jobs,
  CV and applications use `models/validate/view/query`; `src/routes/api_routes.ts`
  is a compatibility re-export.
- `GET /api/v1`, `/health/live`, and `/health/ready` are wired. Ready probes the
  injected Prisma dependency and returns `503 DEPENDENCY_UNAVAILABLE` on failure.
- Current API routes cover student/business login, student registration, public
  jobs, `/me`, student CV/applications and business jobs/applications/CV detail.
  Chat, notifications, interviews, university, TopCV/TopJD and Admin routes are
  not wired.
- JWT Bearer parsing is optional at app level; protected routes use
  `ensureAuthenticated`/`checkRole` and always return JSON `401/403`. There is no
  cookie/session auth or HTML redirect.
- Prisma source is the 12-model legacy Work schema. Supabase config/dependency,
  callback auth helper and empty chat/notification/top services are declared but
  not used by the current route graph.
- `test/app.test.ts` provides injected Supertest coverage; normal npm/pnpm
  scripts are declared, while this shell uses a Deno fallback because Node is
  unavailable.

## Work web

```text
RUNTIME_STATUS: VERIFIED_REACT_VITE_SOURCE
API_STATUS: VERIFIED_RELATIVE_API_CLIENT
TEST_STATUS: SOURCE_TESTS_PRESENT; TYPECHECK_TEST_BUILD_PASS_VIA_DENO_FALLBACK
DESIGN_STATUS: SOURCE_BACKED_COBALT_BASELINE_IMPLEMENTED
```

- `src/app/router.tsx` owns public, student and business routes with role guards;
  unsupported workspace destinations render static/placeholder pages.
- `src/shared/api/work.ts` uses relative `/api/v1`, Zod envelope parsing,
  React Query consumers and Zustand `access_token` persistence. Requests omit
  cookies and send a single optional Bearer header.
- Vite development binds Work Web to `127.0.0.2:3001` and proxies `/api`,
  `/uploads` and `/img` to Work server `127.0.0.1:3002`. Current tests cover
  role access and the Bearer/401 token boundary.
- The presentation layer now has Cobalt semantic tokens, shared UI primitives,
  responsive public/workspace menus and reduced-motion/focus rules. This is a
  presentation-only change; route, API, auth and page-local data flow remain
  unchanged.

## Work mobile

```text
RUNTIME_STATUS: SOURCE_BACKED_DIRECT_NEON
CLIENT_SERVER_STATUS: NOT_HTTP_WIRED_TO_WORK_SERVER
TEST_STATUS: UNIT_TESTS_PRESENT; FLUTTER_TOOLCHAIN_UNAVAILABLE; NETWORK_SMOKE_OPT_IN
DESIGN_STATUS: SOURCE_BACKED_COBALT_BASELINE_IMPLEMENTED
```

- Student and business are Android flavors of one Flutter project with package
  name `study2work_mobile`. Both start at role-specific `DangNhap` through the
  shared flavor router, use direct Neon PostgreSQL through a singleton
  `NeonDatabase`, and keep account/lookup data in SQLite.
- Chat reads/writes `Chat` and `DoanChat` directly, polls every three seconds,
  deduplicates by message `id`, and cancels screen timers in `dispose()`.
- The shared core calls Gemini directly from `AIService`; this is independent of the
  Work server and `apps/ai-server`. URL/row/model normalization and polling
  tests exist; connection smoke tests require an explicit Dart define.
- The unified app owns a shared Material 3 Cobalt theme and UI primitives under
  `lib/app/theme/`. The merge preserves direct
  Neon/SQLite/Gemini boundaries and chat polling semantics are preserved.

## AI server

```text
RUNTIME_STATUS: VERIFIED_MINIMAL_CHAT
COPIED_CORE_STATUS: UNWIRED
DATABASE_RUNTIME_USAGE: NONE
TEST_STATUS: NOT_FOUND
```

- Runtime flow: FastAPI -> `/api/v1/chat_log_ai` -> `chat_log_ai()` -> `OllamaService.generate()`.
- `app/core/*` phần lớn là copied infrastructure và không được đăng ký từ `app/main.py`.
- `pyproject.toml` chỉ khai báo FastAPI/httpx/uvicorn; copied DB/security/config code cần package ngoài dependency set hiện tại.
- `query.py` và `validate.py` của chat là empty placeholders.
- Không có schema/migration/business-code catalog/OpenAPI/test cho AI server.

## DB Admin

```text
WEB_STATUS: VERIFIED_LOCAL_ANGULAR_APP_WITH_ONE_COMMAND_LAUNCHER
API_STATUS: VERIFIED_LOCAL_FASTAPI_APP_WITH_INTERNAL_DEV_LAUNCHER
DATABASE_STATUS: CONFIGURED_BY_LOCAL_CORE_CONSTANTS_ONLY
AUTH_STATUS: JWKS_IMPLEMENTED; LOCAL_DEV_AUTH_TEST_ONLY
AUDIT_STATUS: DURABLE_CONTROL_PLANE_WITH_BOUNDED_FALLBACK
```

- `apps/db-admin-web/` is an Angular app in the pnpm workspace. Its local
  `dev`/`start` launcher starts FastAPI and proxies same-origin `/api` calls.
- `apps/db-admin-server/` remains a separate FastAPI runtime/security boundary
  and is not mounted by Study/Work/AI. Its routes, response envelope,
  permission dependencies and transaction safety are verified by its local test
  suite.
- `apps/db-admin-server/sql/db_admin/001_bootstrap.sql` và
  `scripts/bootstrap_access.py` là control-plane bootstrap độc lập; không phải
  Study/Work business migration. Catalog vẫn đọc metadata từ target runtime.
- `app/services/audit.py` có durable `db_admin.admin_audit_events` path khi
  target đã có control-plane schema, cùng bounded in-memory/structured-log
  fallback. Việc live bootstrap đã được apply chưa được xác minh ở đây.
- `apps/study-server/docs/business_code/code_http.md` và
  `code_event_server.md` tồn tại cho Study; chúng phải được phân biệt với
  runtime business-code evidence của Work/AI/DB Admin.
- DB Admin business codes hiện được sở hữu bởi API source/README và local
  contract; không suy diễn chúng từ Study catalog.

## Drift rule

Nếu tracked source của deep scope thay đổi sau `sourceCommit`, validator báo `CONTEXT_STALE`. Khi đó phải đọc source mới và cập nhật context; không chỉ đổi commit trong manifest để làm validator xanh.
