---
task_id: "2026-10-25-restore-errordetail-study-server"
date: "2026-10-25"
primary_task_type: "fix"
secondary_task_types: ["coding", "docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Khôi phục ErrorDetail trong Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/remove-unicode-encode-catch-access-token.md`
    - carry_forward: Giữ response 401/status, business code, message, trace ID; giữ các thay đổi khác và ghi rõ context validator baseline.
  - path: `.agents/worklog/2026-10-25/remove-valueerror-study-server.md`
    - carry_forward: Dùng `error_response(...)` cho lỗi HTTP; không đưa lỗi non-HTTP thành `JSONResponse`; bảo toàn các thay đổi worktree không liên quan.
  - path: `.agents/worklog/2026-09-28/study-middleware-single-exception-path.md`
    - carry_forward: Giữ envelope, status, business code, safe message, field-error metadata và trace header.
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Đảo ngược riêng phần bỏ `ErrorDetail`; giữ thay đổi không liên quan như bcrypt Unicode error fix.
- shortage: `none` (selector có 5 fix worklogs; 3 file cùng loại được chọn và đọc)

## EXPECTED_BEHAVIOR

- Requirement: Khôi phục `ErrorDetail` và cách sử dụng đã bị thay đổi trong task trước trên toàn Study Server source, tests và context.
- Canonical contract: Giữ nguyên wire response hiện tại, gồm status, business code, message, fieldErrors, trace ID, data/meta, headers và side effects.

## CURRENT_BEHAVIOR

- Source/config: `ErrorDetail` được khôi phục trong `responses.py`; `error_response(errors=...)` nhận `Sequence[ErrorDetail]` và serialize qua `model_dump()`. Middleware, shared validation/auth, course-catalog helpers, API validators/views và tests dùng lại model này.
- Runnable tests: Sau khôi phục, focused suite có 201 tests pass và full Study suite có 275 tests pass.
- Runtime wiring: Request-validation middleware chuyển Pydantic errors thành `ErrorDetail`; helper/API giữ nguyên ánh xạ response, status, business code, field errors và trace ID.

## SOURCE_TRACE

```text
request -> shared helper returns ErrorDetail/sentinel -> API validator/view maps with error_response -> JSONResponse envelope
RequestValidationError -> middleware ErrorDetail list -> error_response -> JSONResponse envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Current error representation | Current source now uses `ErrorDetail` objects at helper/API boundaries and in the response serializer. | `RESOLVED_IN_TASK` | Restore typed helper results and serializer support without changing wire response. |
| Repository-wide context validator | Previous runs report missing DB Admin context/source and source-snapshot drift. | `BASELINE_TO_RECHECK` | Re-run after context update; keep unrelated DB Admin repair out of scope. |

## CHANGES

- Files changed for this restoration: `apps/study-server/app/core/responses.py`, `app/core/middleware.py`, `app/utils/{auth,validate}.py`, course catalog helpers, API #1/#2/#3/#6/#7/#13/#14/#46 validators/views and API #08 detail view, response/validation/API #13 tests, `.agents/server-study/{AGENTS.md,modules/README.md,core/runtime.md,core/database-security.md,workflows/README.md,tests.md}`, and `apps/study-server/docs/codebase/README.md`.
- CONTEXT_UPDATES: Restored the `ErrorDetail` response model and usage rule, removed a contradictory context sentence that prohibited the model, and refreshed the current Study suite count to 275. Existing `ValueError` prohibition remains in Study Server context.
- Unrelated changes preserved: bcrypt `UnicodeEncodeError` handling and its test, API #46 implementation/context, JWT/config/trace work, and all other dirty worktree files.
- Assumptions: Restore all ErrorDetail-related changes from the prior task only; retain the bcrypt `UnicodeEncodeError` fix and all other unrelated worktree changes.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3` | Selected and read all three matching fix worklogs; also reviewed the prior ErrorDetail-removal worklog. | VERIFIED |
| Focused response/middleware/validation/security/API tests | 201 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q` | 275 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/ruff check app tests` | All checks passed. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| `node scripts/validate-agent-context.mjs` and `--skip-drift` | Both report existing `AGENT_CONTEXT_INVALID`: DB Admin context/source roots and referenced files are missing. Full validation also reports broad source-snapshot drift across Study Server and other scopes. | BASELINE_FAILURE |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains invalid due to missing DB Admin context/source and broad snapshot drift; this task changes only server-study context.
- Next owner/action: None; restoration and scoped verification are complete.
