---
task_id: "2026-10-25-reuse-jwt-role-guard"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tái sử dụng JWT guard theo role

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/remove-errordetail-study-server.md`
    - carry_forward: Giữ nguyên các thay đổi worktree không liên quan; không dùng `ValueError`; kiểm tra context validator và ghi nhận baseline DB Admin/snapshot drift.
  - path: `.agents/worklog/2026-10-24/api46-mentor-courses.md`
    - carry_forward: API #46 yêu cầu numeric `sub`/role `MENTOR`; giữ response/business contract, query ownership và side-effect hiện tại.
  - path: `.agents/worklog/2026-10-24/load-study-server-coding-context.md`
    - carry_forward: Giữ scope Study Server; `app/utils/auth.py` là application auth facade; source/test hiện tại ưu tiên hơn context lịch sử.
- shortage: `none` (selector có 36 coding worklogs và trả đủ 3)

## EXPECTED_BEHAVIOR

- Requirement: `validate_current_user_request` nhận role bắt buộc; mọi API Study hiện cần access JWT dùng chung guard và truyền role tường minh. API #46 giữ riêng thông điệp 500 hiện tại.
- Canonical contract: Không đổi status, business code, message, trace ID, side effect hoặc response ngoài việc tái sử dụng auth guard.

## CURRENT_BEHAVIOR

- Source/config: API #4/#13/#14 gọi shared guard Student-only; API #46 trước task tự gọi `extract_bearer_token`, `decode_access_token`, `validate_access_claims` rồi kiểm tra role Mentor. Guard trả `(user_id, roles)` hoặc `JSONResponse`; lỗi 500 mặc định dùng message profile.
- Runnable tests: Trước thay đổi, context ghi 275 tests pass; focused auth/API tests sau thay đổi đạt 87 pass và full Study suite đạt 276 pass.
- Runtime wiring: API #4 gọi guard tại view; API #13/#14 tại API validator; API #46 gọi `validate_mentor_request` trước query trong view. Source scan xác nhận không còn API module tự gọi Bearer/decode/claims helpers.

## SOURCE_TRACE

```text
Authorization -> extract Bearer -> decode JWT -> normalize numeric sub/roles
-> required-role check -> tuple(user_id, roles) or error_response
-> API view/query only after success
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Guard role ownership | Shared guard hard-codes `STUDENT`; API #46 duplicates shared token steps to require `MENTOR`. | `RESOLVED_IN_TASK` | Make requested role explicit and centralize all access-JWT checks. |
| API #46 internal error message | Current validator maps decoder failures to `Mentor courses could not be retrieved.`; shared guard default says `Profile could not be retrieved.` | `RESOLVED_BY_USER` | Add optional message override so API #46 wire message remains unchanged. |

## CHANGES

- Files changed: `apps/study-server/app/utils/auth.py`; API #4 view, API #13/#14 validators, API #46 validator; API #46 auth tests; `.agents/server-study/{AGENTS.md,architecture.md,workflows/README.md,modules/README.md,core/database-security.md,core/runtime.md,tests.md}`; this worklog.
- CONTEXT_UPDATES: Documented the role-aware shared JWT guard and explicit roles for APIs #4/#13/#14/#46; refreshed full-suite count to 276.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `workflows/README.md`, `modules/README.md`, `core/database-security.md`, `core/runtime.md`, `tests.md`.
- Assumptions: `role` is a required keyword-only argument; Student callers pass `STUDENT`, API #46 passes `MENTOR`; API #3 login/refresh does not use the access-JWT request guard. Optional `internal_error_message` preserves API #46’s current 500 message.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read all three same-type worklogs. | VERIFIED |
| Focused tests for APIs #4/#13/#14/#46 | 87 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q` | 276 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/ruff check app tests` | All checks passed. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Source scan for JWT helper use in API modules | Only APIs #4/#13/#14/#46 call `validate_current_user_request`; API #46 no longer invokes Bearer/decode/claims helpers directly. | VERIFIED |
| Context validator full + `--skip-drift` | Both report `AGENT_CONTEXT_INVALID` from missing DB Admin context/source roots. Full validation additionally reports broad `CONTEXT_STALE` snapshot drift across Study Server and other scopes. | BASELINE_FAILURE |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains invalid because DB Admin context/source roots are missing; full mode also reports source snapshot drift across multiple scopes. No Study guard-specific registry/link error appeared.
- Next owner/action: Implementation and scoped verification are complete; preserve the recorded repository context baseline.
