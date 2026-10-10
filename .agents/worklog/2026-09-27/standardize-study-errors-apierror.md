---
task_id: "2026-09-27-standardize-study-errors-apierror"
date: "2026-09-27"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Chuẩn hóa lỗi Study Server qua ApiError

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-26/add-validate-docstrings.md`
    - carry_forward: `app/utils/validate.py` là shared pure validation boundary; giữ behavior của API khi thay đổi error mapping.
  - path: `.agents/worklog/2026-09-26/load-study-server-coding-context.md`
    - carry_forward: Dùng `.venv` của Study; composition và suite từng collect được; API #1–#7 là runtime scope hiện tại.
  - path: `.agents/worklog/2026-09-26/refactor-study-api3-validation.md`
    - carry_forward: API #3 dùng shared validators trong Pydantic; giữ request contract và validation behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: mọi lỗi do mã ứng dụng Study tạo ra được ném/serialize dưới dạng `ApiError`; không lộ lỗi framework/thư viện hoặc exception nội bộ qua HTTP.
- Canonical contract: giữ status, business code, message và field errors hiện tại của API #1–#7; response lỗi có đủ `success`, `businessCode`, `message`, `data`, `meta`, `traceId` và `X-Trace-Id`.
- Approved plan: lỗi Pydantic nội bộ được handler chuyển thành `ApiError`; context-free `ApiError` có defaults an toàn; bỏ envelope legacy và sửa import API #4.

## CURRENT_BEHAVIOR

- Source/config: `ApiError` chưa có defaults/data/meta; handler validation/HTTP/unhandled và middleware còn serialize lỗi độc lập; `error_payload()` vẫn tồn tại.
- Error types: app đang ném `TokenError`, `ValueError`, TypeError và exception riêng cho Ollama/email; API callers ánh xạ một phần các lỗi đó.
- Runtime wiring: `api_04_users_me/__init__.py` dùng `from models import *`, có thể chặn package import.
- Runnable tests: test files có response, token, config, API #1–#7, Ollama và utilities; verification sẽ chạy bằng `.venv` Study.

## SOURCE_TRACE

```text
request/Pydantic or route -> API view -> validation/security/provider/DB helpers
-> ApiError mapping -> global handler -> canonical error_response -> HTTP envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Error boundary | HTTP, validation and unexpected exception handlers now construct `ApiError`; middleware delegates escaped errors to the shared handlers | RESOLVED | One response serializer and trace header |
| Legacy envelope | `error_payload()` and its unit test were removed | RESOLVED | No legacy error shape remains |
| API #4 import | package `__init__.py` now re-exports `.models.UserProfile` | RESOLVED | Import composition succeeds |

## CHANGES

- Files changed: `apps/study-server/app/core/{config,exceptions,middleware,responses}.py`; `app/core/security/{__init__,access_token,refresh_token}.py` (removed `exceptions.py`); shared course helpers/views; API #3 and #4 views/package; AI/email provider exports; shared validation utilities; focused tests for errors, config, security, APIs, provider and utilities.
- CONTEXT_UPDATES: Updated Study error boundary, security/config behavior, AI error mapping, test status and the API #4 import/runtime notes.
- Context pages changed: `.agents/server-study/{AGENTS,architecture,tests}.md`, `.agents/server-study/core/{runtime,database-security}.md`, `.agents/server-study/services/ai.md`.
- Assumptions: scope is all `apps/study-server`; Pydantic may use internal validation exceptions only when the HTTP boundary converts them to `ApiError`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read three matching coding worklogs; no shortage | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest tests/core/test_responses.py tests/core/test_exceptions.py tests/core/test_config.py tests/core/test_security_tokens.py tests/utils/test_validate.py tests/modules/guest/api_01_auth_register/test_register.py tests/modules/guest/api_02_auth_verify_email_send/test_verify_email_send.py tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/guest/api_04_users_me/test_users_me.py tests/modules/guest/api_05_categories/test_categories.py tests/modules/guest/api_06_courses/test_courses.py tests/modules/guest/api_07_courses_search/test_courses_search.py tests/service/ai/test_ollama_service.py -q` | 146 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 160 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest --collect-only -q` | 160 tests collected | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `cd apps/study-server && .venv/bin/mypy app` | No issues found in 57 source files | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.main import app; assert len(app.openapi()["paths"]) == 13; print("composition ok: 13 paths")'` | App imported; OpenAPI contains 13 paths | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK`; registry and page wiring valid | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | Reports `CONTEXT_STALE` in Study and other scopes against the existing 2026-09-18 source snapshot | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Full context validation reports source drift across multiple scopes; the Study snapshot predates the current source. Runtime/tests/static checks are green.
- Next owner/action: no implementation work remains; run the no-drift context validation to confirm registry/page wiring.
