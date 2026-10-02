---
task_id: "2026-09-28-study-middleware-single-exception-path"
date: "2026-09-28"
primary_task_type: "fix"
secondary_task_types: ["coding", "test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Chuyển exception 500 về handler FastAPI

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-27/remove-study-exceptions-module.md`
    - carry_forward: Keep Study exception handlers in `app/core/middleware.py` and preserve error status, business code, safe body and trace ID.
  - path: `.agents/worklog/2026-09-18/work-server-constants.md`
    - carry_forward: Work Server is a separate scope; use Study source and Study validation workflow for this task.
- shortage: `1 missing`

## EXPECTED_BEHAVIOR

- Requirement: Keep trace setup/header/context reset in `TraceIdMiddleware`, let the registered FastAPI `Exception` handler serialize unhandled 500 errors, remove duplicate `HTTPException` handler registration, and preserve response contract.
- Canonical contract/approved plan: The approved plan requests a focused middleware simplification, per-test non-raising TestClient usage for escaped 500 cases, runtime context update and regression verification.

## CURRENT_BEHAVIOR

- Source/config: `TraceIdMiddleware.dispatch` catches every exception from downstream middleware and calls `unhandled_exception_handler`; `create_app` also registers that handler for `Exception`, so Starlette's `ServerErrorMiddleware` is a fallback. `HTTPException` is registered at app composition and redundantly registered again at the end of `create_app`.
- Runnable tests: The shared `client` fixture uses TestClient defaults. `test_health.py` and API #1 registration include endpoint tests whose unexpected exceptions currently get swallowed by `TraceIdMiddleware`; most module-level business failures return `ApiError` directly.
- Runtime wiring: Starlette invokes the registered generic handler at its outer `ServerErrorMiddleware` boundary and re-raises the exception afterward. The handler reads the trace ID from `request.state`; `ApiError` adds it to the response header.

## SOURCE_TRACE

```text
route unexpected exception -> TraceIdMiddleware.dispatch (current catch) -> unhandled_exception_handler -> ApiError JSONResponse
after change: route unexpected exception -> ServerErrorMiddleware registered Exception handler -> unhandled_exception_handler -> ApiError JSONResponse
successful route -> TraceIdMiddleware.dispatch -> X-Trace-Id response header
create_app -> HTTPException handler (single registration)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Duplicate HTTP handler registration | Same handler is registered before router composition and again before `create_app` returns | VERIFIED | Remove the trailing registration and stale comment. |
| TestClient behavior for escaped 500 | Default TestClient re-raises after Starlette sends its configured 500 response; current middleware catches first and prevents re-raise | VERIFIED | Add a separate non-raising client fixture and use it only in tests exercising the global handler. |
| API #6 invalid-row test setup | Its `find_published_courses` mock omitted the positional `db` argument, so it raised `TypeError` before testing row mapping | RESOLVED | Accept the `db` argument so the test verifies the intended safe row-mapping response. |

## CHANGES

- Files changed: `middleware.py`, `main.py`, Study test fixture and escaped-500 tests, API #6 invalid-row mock, Study core runtime context and this worklog.
- CONTEXT_UPDATES: Core runtime documentation now describes exception handling at Starlette's `ServerErrorMiddleware` boundary and trace behavior.
- Context pages changed: `.agents/server-study/core/runtime.md`.
- Assumptions: Public HTTP response status, envelope, business code, safe message, trace ID and successful-response trace header remain unchanged.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type fix --limit 3` | Selected and read two available matching fix worklogs; shortage 1 | VERIFIED |
| `/tmp/study-server-codex-venv/bin/python -m pytest -q tests/test_health.py tests/core/test_exceptions.py tests/modules/guest/api_01_auth_register/test_register.py` | 27 passed, 1 upstream Starlette/httpx deprecation warning | VERIFIED |
| First full `/tmp/study-server-codex-venv/bin/python -m pytest -q` | 162 passed, 1 failed because API #6 invalid-row mock omitted its positional `db` argument | RESOLVED_AFTER_TEST_FIX |
| `/tmp/study-server-codex-venv/bin/python -m pytest -q` after mock correction | 163 passed, 1 upstream Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `/tmp/study-server-codex-venv/bin/mypy app` | No issues in 62 source files | VERIFIED |
| Study import/OpenAPI probe | FastAPI imported; 13 OpenAPI paths, including courses and register | VERIFIED |
| `git diff --check` and `grep -c 'app.add_exception_handler(HTTPException' apps/study-server/app/main.py` | Clean diff; exactly one HTTPException handler registration remains | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: pre-existing missing DB Admin context/source paths and stale source snapshots, including Study files predating this task | CONTEXT_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Still fails only on missing DB Admin context/source paths; no task-specific registry/page-graph error reported | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: Repository-wide context validation is red because DB Admin context/source paths are missing and tracked source snapshots are stale; focused Study tests and code checks pass.
- Next owner/action: Restore/refresh the unrelated DB Admin context and repository source snapshots in a separate maintenance task if a green global validator is required.
