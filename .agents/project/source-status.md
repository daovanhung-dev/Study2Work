# Source status và discrepancy

Deep-context được đối chiếu tại source commit `5a5c2c826ddcc2931a9398115fdb61448dcb4c57` ngày 2026-08-26.

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
- Work có executable contract tại `contracts/openapi/work/openapi.json` và Study->Work event schemas.
- Study OpenAPI chỉ có placeholder README; AI không có OpenAPI hiện hành.

## Context system

```text
ROOT_ROUTER: AGENTS.md
CONTEXT_REGISTRY: .agents/AGENTS.md
MANIFEST: .agents/context-manifest.json
VALIDATOR: scripts/validate-agent-context.mjs
STUDY_LEGACY_AGENT_CONTEXT: REMOVED
```

Deep scopes:

- `server-study`: `.agents/server-study/AGENTS.md`
- `server-work`: `.agents/server-work/AGENTS.md`
- `server-ai`: `.agents/server-ai/AGENTS.md`
- `db-admin`: `.agents/db-admin/AGENTS.md`

Mobile/Web giữ `SKELETON_ONLY` theo scope đã duyệt.

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
RUNTIME_STATUS: VERIFIED_DOMAIN_API
OPENAPI_STATUS: VERIFIED_DOMAIN_CONTRACT
DATABASE_SCHEMA_STATUS: VERIFIED_DOMAIN_MIGRATED
```

- Foundation endpoints remain `/api/v1`, `/health/live` and `/health/ready`; the
  Work domain route surface is additionally registered by `WorkModule`.
- Global Nest auth guard tồn tại nhưng cả ba foundation controller đều public.
- Readiness probe PostgreSQL bằng Prisma `SELECT 1`.
- Redis chỉ được parse/configure và report label; chưa có Redis client/probe.
- Work configuration is sourced from local-only `apps/work-server/src/constants.ts`
  with `local`, `docker`, and `neon` profiles; Prisma uses its constants wrapper.
- Prisma maps the clean Work domain: 55 application tables plus `system_records`.
- `WorkModule` implements the current public/protected HTTP surface for jobs,
  candidates, tenants, applications, chat, interviews, university, billing and
  operations. Provider-dependent payment/storage settlement remains safely
  unconfigured rather than simulated.
- Neon `prisma migrate deploy` and authenticated HTTP smoke have been verified;
  smoke fixtures were removed afterward. Study event consumer/HMAC remains an
  external integration boundary and is not claimed as implemented.

## Work web

```text
RUNTIME_STATUS: VERIFIED_LIVE_DATA_SHELL
BUILD_STATUS: VERIFIED
BROWSER_SMOKE_STATUS: UNWIRED_NO_BROWSER_SESSION
```

- Existing Work routes now render through a live-data `WorkFeaturePage` using
  the typed Zod/React Query Work API client; public, candidate, enterprise,
  university and operations route families have route-aware screens.
- Production build/typecheck passed. Browser automation could not run because
  the in-app browser returned no available session; Vite HTTP smoke was used.

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
