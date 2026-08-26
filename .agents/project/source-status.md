# Source status và discrepancy

Trạng thái được kiểm tra trên working tree ngày 2026-08-26.

## Tài liệu thiết kế

```text
DD_STATUS: NOT_FOUND
CANONICAL_BD_STATUS: NOT_FOUND
BUSINESS_CODE_STATUS: CREATED_FROM_CURRENT_RUNTIME
```

- Root `README.md` và một số contract README vẫn trỏ tới `docs/BD/`, nhưng
  directory đó không tồn tại.
- `.agent/docs/dd/` chỉ có template/example không thuộc Study2Work runtime.
- Không dùng template, diagram hoặc Git history để tự hoàn thiện request,
  response, business rule hay database mapping còn thiếu.
- Work có contract hiện hành giới hạn tại `contracts/openapi/work/openapi.json`
  và hai event schema trong `contracts/events/study-work/`.
- Study chỉ có placeholder `contracts/openapi/study/README.md`, chưa có OpenAPI.

## Study server

```text
SOURCE_CHANGED
CONTEXT_STALE
BUSINESS_MODULE_STATUS: NONE
DECLARED_ROUTES: 10
RUNNABLE_ROUTES: 0
DATABASE_SCHEMA_STATUS: NOT_FOUND
```

Các blocker đã xác minh:

- `app/api/v1.py` import package `app.module.*` không tồn tại.
- `app/core/responses.py` không định nghĩa `success_response`/`error_response`
  nhưng `main.py` và `exceptions.py` import chúng.
- `app/core/middleware.py` import ba tên trace không tồn tại trong
  `app/core/trace.py`.
- `alembic.ini` và Dockerfile trỏ/copy directory `alembic/` không tồn tại.
- Test collection import `app.main`, nên bị chặn trước khi chạy; nhiều test còn
  dùng API response/security đã bị đổi tên hoặc xóa.
- `apps/study-server/.agent/context/` và
  `apps/study-server/docs/codebase/README.md` mô tả snapshot cũ. Chúng là bằng
  chứng lịch sử về intent, không phải contract/source hiện tại.

Đọc `.agents/server-study/AGENTS.md` trước mọi task Study.

## AI server

- Runtime route chat hoạt động theo flow tối giản khi dependency được cài, nhưng
  không đăng ký copied core middleware/response/security/database.
- Copied core cần nhiều package không được khai báo trong
  `apps/ai-server/pyproject.toml`; không coi nó là runtime-active.
- Không có DD, schema/migration, business-code catalog, test, Docker/Compose hay
  standard response contract cho AI server.

## Work server

- Source, tests và Work OpenAPI cùng mô tả ba foundation endpoint.
- Prisma hiện chỉ có `system_records`; không có Work domain model.
- Redis mới chỉ là config/status label, chưa có client/probe.
- Study event contract tồn tại nhưng consumer/HMAC/idempotency/snapshot chưa
  được implement.
- DD public-domain được README nhắc tới nhưng nguồn `docs/BD` đang thiếu.

## Root-level drift

- `tests/smoke_test.py` import top-level `app`, gọi auth routes và schema tạm
  không thuộc một package runnable ở repository root; không dùng nó như verified
  contract.
- Root runtime map không liệt kê AI server dù root Python workspace có member
  `apps/ai-server`.
- Các deletion đang có trong working tree là user-owned; không restore trong
  task khác nếu chưa được yêu cầu rõ.
