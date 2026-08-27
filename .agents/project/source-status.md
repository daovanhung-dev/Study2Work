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
RUNTIME_STATUS: VERIFIED_FOUNDATION
OPENAPI_STATUS: VERIFIED_FOUNDATION
DATABASE_SCHEMA_STATUS: VERIFIED_FOUNDATION
```

- Ba endpoint hiện hành: `/api/v1`, `/health/live`, `/health/ready`.
- Global Nest auth guard tồn tại nhưng cả ba foundation controller đều public.
- Readiness probe PostgreSQL bằng Prisma `SELECT 1`.
- Redis chỉ được parse/configure và report label; chưa có Redis client/probe.
- Prisma chỉ có `system_records`; chưa có Work domain models/callers.
- Study event consumer/HMAC/idempotency/local snapshot chưa được implement.

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

## Drift rule

Nếu tracked source của deep scope thay đổi sau `sourceCommit`, validator báo `CONTEXT_STALE`. Khi đó phải đọc source mới và cập nhật context; không chỉ đổi commit trong manifest để làm validator xanh.
