---
task_id: "2026-10-25-remove-errordetail-study-server"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Bỏ ErrorDetail khỏi Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/api46-mentor-courses.md`
    - carry_forward: Giữ nguyên business code/response contract API #46; bảo toàn thay đổi có sẵn và ghi rõ validator baseline DB Admin/snapshot drift.
  - path: `.agents/worklog/2026-10-24/load-study-server-coding-context.md`
    - carry_forward: Giữ phạm vi Study Server, nạp đúng context scope và không sửa ngoài task.
  - path: `.agents/worklog/2026-10-24/remove-api46-query-parser.md`
    - carry_forward: Giữ nguyên API behavior, tests và các thay đổi worktree không liên quan.
- shortage: `none` (selector có 35 coding worklogs và trả đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: Xóa `ErrorDetail` khỏi runtime code và tests của Study Server; dùng `error_response(...)` để dựng HTTP lỗi tại validator/view boundary.
- Canonical contract: Giữ nguyên status, business code, message, fieldErrors shape, trace ID, data/meta, headers và side effect hiện tại.

## CURRENT_BEHAVIOR

- Source/config at task start: `ErrorDetail` được khai báo trong `app/core/responses.py`; middleware, shared validation/auth, course catalog helpers, API validators/views và tests tạo hoặc kiểm tra instance của class đó. `error_response(errors=...)` serialize model vào `meta.fieldErrors`.
- Runnable tests: Scope context ghi 273 tests pass trước task; full suite sau thay đổi hiện có 274 tests pass.
- Runtime wiring: Request validators, views, shared helpers và global request-validation handler chuyển lỗi qua `error_response(...)`; các API caller cần giữ response mapping và trace ID.

## SOURCE_TRACE

```text
request/API validator -> shared helper result -> API validator/view error_response(...) -> JSONResponse envelope
FastAPI RequestValidationError -> middleware field-error mappings -> error_response(...) -> JSONResponse envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Error representation | Current source uses `ErrorDetail` objects; approved rule requires no class in runtime/tests. | `RESOLVED_IN_TASK` | Replace with mappings/sentinels while retaining serialized response shape. |
| Global context validator | Previous task reports missing DB Admin context/source and broad snapshot drift. | `BASELINE_TO_RECHECK` | Re-run validator and record current findings without expanding into DB Admin repair. |

## CHANGES

- Files changed: `apps/study-server/app/core/responses.py`, `app/core/middleware.py`, `app/core/security/password.py`, `app/utils/{auth,validate}.py`, course catalog helpers, validators/views cho API #1/#2/#3/#6/#7/#8/#13/#14/#46, `tests/core/test_responses.py`, `tests/utils/test_validate.py`, API #13 tests, `tests/test_security.py`, Study Server context pages, codebase README, and this worklog.
- CONTEXT_UPDATES: Removed the class-based error description rule, documented mapping input for `error_response(errors=...)`, and refreshed full-suite count to 274. Tightened a pre-existing bare catch in bcrypt encoding to `UnicodeEncodeError` and added a regression test so full Ruff passes.
- Context pages changed: `.agents/server-study/AGENTS.md`, `modules/README.md`, `core/runtime.md`, `core/database-security.md`, `workflows/README.md`, and `tests.md`; also updated `apps/study-server/docs/codebase/README.md`.
- Assumptions: `error_response(errors=...)` accepts field-error mappings; helpers return ordinary values or simple failure data for API boundary mapping.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read all three matching coding worklogs. | VERIFIED |
| Focused response/middleware/validation/API tests (`pytest -q` on core responses/exceptions, utils validation, security and APIs #1/#2/#3/#6/#7/#8/#13/#14/#46) | 200 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q` | 274 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/ruff check app tests` | All checks passed after replacing the pre-existing bare catch in bcrypt encoding with `UnicodeEncodeError`. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Python scan for `ErrorDetail` in `apps/study-server/app` and `tests` | No references remain. | VERIFIED |
| Python scan for `ValueError` in `apps/study-server/app` and `tests` | No references remain. | VERIFIED |
| Context validator full + `--skip-drift` | Pending final rerun after context/worklog updates. | PENDING |

## HANDOFF

- Remaining blockers: None identified for Study Server implementation; context validator baseline will be rechecked.
- Next owner/action: Complete source/tests/context updates and record verification results.
