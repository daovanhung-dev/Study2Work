---
task_id: "2026-09-27-remove-study-exceptions-module"
date: "2026-09-27"
primary_task_type: "fix"
secondary_task_types: ["coding", "docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Remove the Study exceptions module without changing error behavior

## PRIOR_WORKLOG_REVIEW

- primary_task_type: fix
- selector_command: `deno run -A scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-18/work-server-constants.md`
    - carry_forward: Study is a separate scope; use current Study source and its own validation workflow. The prior log recorded context drift for Work and does not establish Study runtime behavior.
- shortage: `2 missing`

## EXPECTED_BEHAVIOR

- Requirement: Remove `apps/study-server/app/core/exceptions.py` while preserving all error status, business code, message, trace header, field-error metadata and safe exception behavior.
- Canonical contract/approved DD: Keep `ApiError` serialization through `error_response`; `main.py` registers handlers and `TraceIdMiddleware` routes escaped errors through the common handlers.

## CURRENT_BEHAVIOR

- Source/config: `exceptions.py` defines `_validation_field` and four FastAPI exception handlers. `main.py` imports/registers all handlers; `middleware.py` imports and calls the ApiError and unhandled handlers.
- Runnable tests: Existing `tests/core/test_exceptions.py` and API #5 category tests import handlers from `app.core.exceptions`; the Study virtual environment has pytest, Ruff and mypy executables.
- Runtime wiring: HTTP protocol and request-validation handlers are registered by `create_app`; middleware handles escaped `ApiError` and unexpected exceptions. All handlers serialize via `error_response(ApiError)` and have no database/provider side effects.

## SOURCE_TRACE

```text
main.create_app -> handlers (currently app.core.exceptions) -> error_response(ApiError) -> JSONResponse
TraceIdMiddleware.dispatch -> api_error_handler / unhandled_exception_handler -> JSONResponse
tests/core/test_exceptions.py and API #5 category tests -> handler functions
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Module removal | Current runtime and tests import `app.core.exceptions`; deleting without relocation would break app composition and tests | VERIFIED | Move the unchanged handler implementation into `app.core.middleware` and update every active caller before deleting the old module |

## CHANGES

- Files changed: Deleted `apps/study-server/app/core/exceptions.py`; moved the unchanged handler implementation into `app/core/middleware.py`; updated composition/test imports, Study core documentation, business-code references and this worklog.
- CONTEXT_UPDATES: Exception-handler ownership and runtime wiring now point to `app/core/middleware.py`.
- Context pages changed: `.agents/server-study/architecture.md`, `.agents/server-study/core/runtime.md`.
- Assumptions: Exception-handler behavior and public API contract remain byte-for-byte equivalent at the JSON field/value level; relocating handlers to `middleware.py` is the smallest destination because middleware already calls two of them.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `./.venv/bin/python -m pytest tests/core/test_exceptions.py tests/modules/guest/api_05_categories/test_categories.py` | 11 passed | PASS |
| `./.venv/bin/python -m pytest` | 160 passed; one upstream Starlette/httpx deprecation warning | PASS |
| `./.venv/bin/ruff check .` | All checks passed | PASS |
| `./.venv/bin/mypy app` | No issues in 56 source files | PASS |
| `./.venv/bin/python -c 'from app.main import app; print(type(app).__name__)'` | `FastAPI` | PASS |
| `git diff --check` and active-reference scan | Clean diff; no active `app.core.exceptions` or old source-path references; module file absent | PASS |
| `node scripts/validate-agent-context.mjs` | Node is unavailable in this environment | DECLARED_NOT_RUNNABLE |
| `deno run -A scripts/validate-agent-context.mjs` | Reports existing `CONTEXT_STALE` source snapshots across Study and other scopes | CONTEXT_STALE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Agent context registry and page graph pass | PASS |

## HANDOFF

- Remaining blockers: Exact context validator remains red because repository-wide source snapshots are already stale; its drift-skipped registry/page-graph validation passes.
- Next owner/action: Refresh global source snapshots separately if a clean exact context-validator run is required.
