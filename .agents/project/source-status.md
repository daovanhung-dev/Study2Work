# Source status và discrepancy

Work deep-context được đối chiếu tại source commit `97ca23fc506653db3c67b91480c476dec52f8b63` ngày 2026-09-16.

## Tài liệu thiết kế

```text
DD_STATUS: NOT_FOUND
CANONICAL_BD_STATUS: NOT_FOUND
BUSINESS_CODE_STATUS: CREATED_FROM_CURRENT_RUNTIME
DIAGRAM_API_CONTRACT_STATUS: APPROVED_DESIGN_CONTRACT
```

- Root README/contract README có chỗ trỏ `docs/BD/`, nhưng directory đó không có trong source snapshot.
- Không dùng template, diagram hoặc Git history để tự hoàn thiện request/response/business rule/database mapping thiếu.
- `docs/lists/list_api.md` và `docs/diagrams/AC_UNICA/` là approved V1 design contract theo yêu cầu được phê duyệt; các schema và `DESIGN_*` code ở đó vẫn là `DESIGN_PROPOSAL`, không phải runtime/OpenAPI evidence.
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
STUDY_LEGACY_AGENT_CONTEXT: PRESENT_OUTSIDE_SCOPE; not changed in Work sync
```

Deep scopes:

- `server-study`: `.agents/server-study/AGENTS.md`
- `server-work`: `.agents/server-work/AGENTS.md`
- `server-ai`: `.agents/server-ai/AGENTS.md`
- `db-admin`: `.agents/db-admin/AGENTS.md`
- `web-work`: `.agents/web-work/AGENTS.md`
- `mobile-work`: `.agents/mobile-work/AGENTS.md`

Work Web và Work Mobile hiện là source-backed; Study legacy agent context không
được dọn trong task này.

## Study server

```text
RUNTIME_STATUS: DECLARED_NOT_RUNNABLE
BUSINESS_MODULE_STATUS: NOT_FOUND
DATABASE_SCHEMA_STATUS: NOT_FOUND
```

Blocker tại snapshot:

- `app/api/v1.py` import `app.module.auth.*` và `app.module.ai.log.*`, nhưng `app/module/` không tồn tại.
- `app/main.py` import `success_response`, nhưng `app/core/responses.py` chỉ còn `ApiResponse.success_payload()`/`raise_error()`.
- `app/core/exceptions.py` import `error_response`, cũng không tồn tại trong responses hiện hành.
- `app/core/middleware.py` import `normalize_trace_id`, `set_current_trace_id`, `reset_current_trace_id`, trong khi `trace.py` expose `validate_trace_id`, `set_trace_id`, `reset_trace_id`.
- `alembic.ini`/Dockerfile tham chiếu directory migration không tồn tại.
- Test collection đi qua `app.main`, nên blocker import xảy ra trước khi các health/security assertion có thể được tin là runnable.
- `apps/study-server/docs/codebase/README.md` là historical/non-authoritative nếu khác current source.

## Work server

```text
RUNTIME_STATUS: VERIFIED_EXPRESS_JSON_API
OPENAPI_STATUS: SOURCE_ALIGNED_LEGACY_WEB; TARGET_CONTRACT_DISCREPANCY
DATABASE_SCHEMA_STATUS: VERIFIED_PRISMA_12_MODELS
HEALTH_ROUTE_STATUS: NOT_FOUND
```

- `src/main.ts` connects the shared Prisma client before listening on port 3000;
  `src/app.ts` mounts JSON/static/upload middleware and only `/api/v1`.
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
- Vite development proxies `/api`, `/uploads` and `/img` to Work server port
  3000. Current tests cover role access and the Bearer/401 token boundary.
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

- Student and business are separate Flutter apps with package name `work_server`.
  Both start at `DangNhap`, use direct Neon PostgreSQL through a singleton
  `NeonDatabase`, and keep account/lookup data in SQLite.
- Chat reads/writes `Chat` and `DoanChat` directly, polls every three seconds,
  deduplicates by message `id`, and cancels screen timers in `dispose()`.
- Both apps call Gemini directly from `AIService`; this is independent of the
  Work server and `apps/ai-server`. URL/row/model normalization and polling
  tests exist; connection smoke tests require an explicit Dart define.
- Each standalone app now owns a local Material 3 Cobalt theme and UI
  primitives under `lib/theme/`. The refresh changes presentation only; direct
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
AUDIT_STATUS: BOUNDED_IN_MEMORY_AND_STRUCTURED_LOG
```

- `apps/db-admin-web/` is an Angular app in the pnpm workspace. Its local
  `dev`/`start` launcher starts FastAPI and proxies same-origin `/api` calls.
- `apps/db-admin-server/` remains a separate FastAPI runtime/security boundary
  and is not mounted by Study/Work/AI. Its routes, response envelope,
  permission dependencies and transaction safety are verified by its local test
  suite.
- No live Neon schema or migration was added. Catalog metadata is read from the
  configured database at runtime; no audit table is created.
- `docs/business_code/code_http.md` is `NOT_FOUND` in the current working tree;
  DB Admin business codes are currently owned/documented by its API source and
  README until the repository catalog is restored.

## Drift rule

Nếu tracked source của deep scope thay đổi sau `sourceCommit`, validator báo `CONTEXT_STALE`. Khi đó phải đọc source mới và cập nhật context; không chỉ đổi commit trong manifest để làm validator xanh.
