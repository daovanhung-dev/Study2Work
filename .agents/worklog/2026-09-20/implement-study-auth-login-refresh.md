---
task_id: "2026-09-20-implement-study-auth-login-refresh"
date: "2026-09-20"
primary_task_type: "coding"
secondary_task_types: ["test", "db-admin"]
project_scopes: ["server-study", "db-admin"]
cross_scope_dependencies:
  - "Study auth routes <-> users/refresh_tokens schema"
status: "VERIFIED"
---

# Worklog: Implement Study Auth Login và Refresh Token

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-20/publish-develop-to-github.md`
    - carry_forward: Giữ nguyên thay đổi untracked hiện có; không commit hoặc overwrite ngoài phạm vi task.
  - path: `.agents/worklog/2026-09-19/extract-strip-email-utility.md`
    - carry_forward: `app.utils.validate` là boundary shared validation; ghi rõ toolchain/context drift và không suy diễn runtime từ docs.
  - path: `.agents/worklog/2026-09-19/rename-study-auth-guest-namespace.md`
    - carry_forward: Public `/api/v1/auth/*` giữ nguyên; internal module dùng namespace `guest`; test stale phải được ghi nhận/sửa tối thiểu.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement login + refresh rotation, common validation utilities, hashed refresh-token persistence, schema/migration and tests according to the approved user plan.
- Contract decisions: Login/refresh success `200 DESIGN_RESOURCE_RETRIEVED`; invalid credentials/refresh `401 DESIGN_AUTHENTICATION_REQUIRED`; inactive account `403 DESIGN_ACCESS_DENIED`; validation `422 DESIGN_VALIDATION_ERROR`; internal failure `500 DESIGN_INTERNAL_ERROR`.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` only exposes register/hello/db; `core/security` has token/password primitives; `app/utils` and refresh-token table are absent.
- Runnable tests: Existing register test imports stale `app.modules.auth`; current app import is blocked by missing `app.utils.validate`.
- Runtime wiring: No login or refresh orchestration.

## SOURCE_TRACE

```text
POST /api/v1/auth/login
-> auth_login.models/validate
-> auth_login.view
-> auth_login.query SQL + app.core.database
-> app.utils.auth + app.core.security
-> refresh_tokens/users
-> canonical response

POST /api/v1/auth/refresh
-> refresh request validation
-> token hash lookup/revoke/insert
-> new access + rotated refresh token
-> canonical response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Login/refresh routes | Absent from current `app/api/v1.py` | UNWIRED | Add public routes and tests |
| Shared validation utility | `app/utils/validate.py` and package init absent | NOT_FOUND | Add utility and repair register import |
| Refresh persistence | Study DB schema has no refresh-token table | NOT_FOUND | Add schema artifact and idempotent migration |
| Register test namespace | Test imports `app.modules.auth`, runtime uses `app.modules.guest` | DISCREPANCY | Update test imports minimally |
| Live DB | No live migration execution authorized | DECLARED_NOT_RUNNABLE | Create migration only; do not apply externally |

## CHANGES

- Files changed: Added `app/utils/{__init__,auth,validate}.py`, `app/modules/guest/auth_login/{models,validate,query,view}.py`, auth tests and refresh-token migration; updated router, exception mapping, shared register validation import, security helper typing, Study schema and register test imports.
- CONTEXT_UPDATES: Registered wired login/refresh routes, auth module ownership, refresh-token schema/migration status and 58-test verification.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`.
- Assumptions: `utils/auth.py` handles token lifecycle/payload only; `view.py` owns DB writes and transaction. Refresh rotation does not implement reuse detection. Tokens are JSON response fields, not cookies.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3 matching coding worklogs; all read | VERIFIED |
| `git status --short --branch` | Only pre-existing `.agents/worklog/2026-09-20/` untracked | VERIFIED |
| Source inspection of router, security, DB schema, tests | Current gaps recorded above | VERIFIED |
| `.venv/bin/pytest --collect-only -q` | 58 tests collected | VERIFIED |
| `.venv/bin/pytest -q` | 58 passed, 1 dependency deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `.venv/bin/mypy app` | No issues found in 32 source files | VERIFIED |
| `.venv/bin/ruff format --check app tests` | Only pre-existing `core/constants.py` and `core/database.py` need formatting | CONTEXT_BASELINE |
| `python3` migration static assertions | Table, hash, cascade and indexes present in schema/migration | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` in Study/Work/Web/DB Admin snapshots | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Migration has not been applied to live DB by design; full context validator reports pre-existing source snapshot drift; full format check reports two pre-existing legacy files.
- Next owner/action: Apply `migrations/002_refresh_tokens.sql` in the target Study database before deploying the new routes; no further code action required.
