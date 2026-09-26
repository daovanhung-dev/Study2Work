---
task_id: "2026-09-26-refactor-study-api3-validation"
date: "2026-09-26"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Refactor validation Study API #3 vào utils

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-26/load-study-server-coding-context.md`
    - carry_forward: Study composition import và test collection đã verified; API #3 hiện đi qua module `validate.py` và `app/utils/validate.py`; live DB chưa được xác minh.
  - path: `.agents/worklog/2026-09-23/split-study-api-dd-folders.md`
    - carry_forward: Giữ namespace API-ID, public route/response/SQL/transaction contract và không sửa ngoài phạm vi.
  - path: `.agents/worklog/2026-09-22/implement-study-api2-verify-email-send.md`
    - carry_forward: Dùng `.venv` của Study cho focused/full checks và giữ canonical envelope/trace; không suy diễn runtime từ schema artifact.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Đưa `normalize_login_email`, `validate_login_password` và `validate_refresh_token` vào `app/utils/validate.py` để tái sử dụng; API #3 import trực tiếp từ utils; xóa `api_03_auth_login/validate.py`.
- Contract: Giữ nguyên LoginRequest/RefreshRequest fields, Pydantic validation behavior, HTTP routes, error codes, auth flow và transaction behavior.

## CURRENT_BEHAVIOR

- Source: API #3 `models.py` import ba wrapper từ `api_03_auth_login/validate.py`; wrapper chỉ gọi `strip_email`, `reject_blank_password`, `reject_blank_value` trong utils.
- Callers: grep trong `apps/study-server` xác nhận chỉ `models.py` gọi module validator; không có caller khác.
- Tests: utility tests hiện mới cover ba generic helper; API #3 tests cover model normalization/rejection và HTTP validation envelope.

## SOURCE_TRACE

```text
LoginRequest/RefreshRequest
-> app.utils.validate shared validators
-> Pydantic field_validator
-> /api/v1/auth/login|refresh
-> unchanged view/query/security/response/transaction
-> API #3 tests + utils tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #3 validator location | Current wrappers are module-local but have no unique logic | RESOLVED_FOR_IMPLEMENTATION | Move semantic validators to utils and delete wrapper file |
| Public behavior | User requires reuse only; no route/response/security change | NO_DISCREPANCY | Preserve existing request and HTTP contract |
| Live database | Not involved in validation refactor | OUT_OF_SCOPE / LIVE_NOT_VERIFIED | No DB or migration changes |

## CHANGES

- Files changed: Moved the three API #3 validator functions to `app/utils/validate.py`, exported them from `app/utils/__init__.py`, updated `api_03_auth_login/models.py` to import directly from utils, deleted the unused module-local `validate.py`, and added utility tests.
- CONTEXT_UPDATES: Updated `server-study` validation ownership pages and removed the deleted source path from `.agents/context-manifest.json`.
- Context pages changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/architecture.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/workflows/README.md`, `.agents/context-manifest.json`.
- Assumptions: Kept existing validator names and error messages; did not refactor API #1 or other modules; no DB/schema/runtime auth flow changes.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read 3 matching coding worklogs | VERIFIED |
| Caller/definition grep | Only API #3 `models.py` calls the module wrappers | VERIFIED |
| `.venv/bin/pytest tests/modules/guest/api_03_auth_login/test_auth_login.py tests/utils/test_validate.py -q` | 18 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/pytest -q` | 137 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `.venv/bin/mypy app` | No issues found in 59 source files | VERIFIED |
| composition import + API path check | API #3 imports and login/refresh paths remain available | VERIFIED |
| deleted-file/reference check | Module `validate.py` absent; no legacy import remains; validators exist only in utils | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Repository-wide pre-existing `CONTEXT_STALE`, including Study snapshot drift | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Full context validator remains stale against the repository snapshot; this is pre-existing and does not affect the focused context registry validation. One Starlette/httpx deprecation warning remains.
- Next owner/action: Review the API #3 utility boundary; no application implementation work remains for this request.
