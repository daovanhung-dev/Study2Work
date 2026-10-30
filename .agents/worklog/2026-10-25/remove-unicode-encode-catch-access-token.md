---
task_id: "2026-10-25-remove-unicode-encode-catch-access-token"
date: "2026-10-25"
primary_task_type: "fix"
secondary_task_types: ["coding", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Bỏ bắt UnicodeEncodeError khi giải mã access token

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/remove-valueerror-study-server.md`
    - carry_forward: Không dùng built-in `ValueError`; HTTP failures phải qua `error_response(...)`; giữ lỗi ngoài HTTP nội bộ.
  - path: `.agents/worklog/2026-09-28/study-middleware-single-exception-path.md`
    - carry_forward: Giữ nguyên HTTP status, business code, thông điệp an toàn và trace header.
  - path: `.agents/worklog/2026-09-27/remove-study-exceptions-module.md`
    - carry_forward: Giữ response mapping chuẩn qua `error_response(...)`.
- shortage: `none` (selector có 3 fix worklogs)

## EXPECTED_BEHAVIOR

- Requirement: Trong `app/core/security/access_token.py`, bắt `PyJWTError` và trả `_invalid_access_token()`; không dùng `InvalidTokenError`, `TypeError` hoặc `ValueError` tại file đó. Facade tiếp tục bắt `TypeError` để giữ authentication 401 cho claim thời gian sai kiểu.
- Canonical contract/approved plan: Không đổi API HTTP response; invalid/expired/malformed token vẫn trả authentication 401.

## CURRENT_BEHAVIOR

- Source/config: `app/core/security/access_token.py` từ chối chuỗi không ASCII, bắt `PyJWTError` và trả `_invalid_access_token()`; facade `app/utils/auth.py` chỉ bắt `TypeError` còn lại từ JWT decode. PyJWT trong Study venv là 2.13.0.
- Runnable tests: Sau thay đổi, focused security/API #4/API #46 suite có 52 tests pass; toàn Study suite có 273 tests pass.
- Runtime wiring: API callers dùng facade `app.utils.auth.decode_access_token`; API #3/#4/#14 và #46 giữ mapping authentication 401.

## SOURCE_TRACE

```text
Authorization header -> extract_bearer_token -> decode_access_token -> PyJWT decode -> claims or _invalid_access_token -> caller response -> security/API tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Non-ASCII token handling | PyJWT encodes str input as UTF-8; invalid surrogate text can fail before normal JWT decoding. | `RESOLVED_IN_TASK` | ASCII guard returns existing 401 before calling PyJWT. |
| `TypeError` mapping | PyJWT 2.13.0 can raise `TypeError` while validating malformed time claims; this is outside `PyJWTError`. | `RESOLVED_IN_TASK` | Facade catch and regression test keep the 401 response. |
| JWT validation mapping | PyJWT validation exceptions derive from `PyJWTError`. | `RESOLVED_IN_TASK` | Decoder catches the library base class and returns `_invalid_access_token()`. |

## CHANGES

- Files changed: `apps/study-server/app/core/security/access_token.py`, `apps/study-server/app/utils/auth.py`, `apps/study-server/tests/core/test_security_tokens.py`, `.agents/server-study/AGENTS.md`, `.agents/server-study/core/database-security.md`, `.agents/server-study/tests.md`, and this worklog.
- CONTEXT_UPDATES: Security page distinguishes `PyJWTError` mapping in the core decoder from `TypeError` mapping in the application facade; test count refreshed to the latest full suite.
- Context pages changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/core/database-security.md`, `.agents/server-study/tests.md`.
- Assumptions: Compact JWT tokens are ASCII; `PyJWTError` maps to 401 in core and claim-decoding `TypeError` maps to 401 in the facade.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type fix --limit 3` | Selected and read all three available matching fix worklogs. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q tests/core/test_security_tokens.py tests/modules/guest/api_04_users_me/test_users_me.py tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py` | 52 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/pytest -q` | 273 passed; one existing Starlette/httpx deprecation warning. | VERIFIED |
| `cd apps/study-server && ./.venv/bin/ruff check app tests` | All checks passed. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| `grep -nE 'InvalidTokenError|TypeError|ValueError' apps/study-server/app/core/security/access_token.py` | No matches (grep exit 1 as expected). | VERIFIED |
| `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/validate-agent-context.mjs` | Exit 1: baseline missing DB Admin context/source and `CONTEXT_STALE` from older manifest source commit. | BASELINE_BLOCKED |
| `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/validate-agent-context.mjs --skip-drift` | Exit 1: DB Admin context/source entries and links are missing; no Study Server page graph errors reported. | BASELINE_BLOCKED |

## HANDOFF

- Remaining blockers: No Study Server implementation/test blocker. Repository-wide context validation remains red because DB Admin context/source is missing; full validation also reports tracked-source drift against the older manifest commit.
- Next owner/action: Re-run global context validation after the DB Admin baseline is restored and manifest drift is reconciled.
