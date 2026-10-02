---
task_id: "2026-09-28-study-apierror-factory"
date: "2026-09-28"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Chuyển ApiError thành hàm factory

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Keep `success_response` as the success builder, preserve Study error response behavior, and use `.venv` for verification.
  - path: `.agents/worklog/2026-09-27/document-study-main-functions.md`
    - carry_forward: Preserve unrelated `main.py` documentation and use the Deno context-validation command when Node is unavailable.
  - path: `.agents/worklog/2026-09-27/standardize-study-errors-apierror.md`
    - carry_forward: Keep API #1–#7 status/business-code/message mappings and the shared error handler/serializer behavior unchanged.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: public `ApiError(...)` is a function factory; existing `raise ApiError(...)` call sites and HTTP error contract remain unchanged.
- Canonical contract/approved plan: the factory returns a private `_ApiError(Exception)` used by FastAPI registration, `except`, type hints and serializer; zero-argument construction produces safe internal 500 defaults.

## CURRENT_BEHAVIOR

- Source/config: `ApiError` was an exception class with a classmethod `internal`; FastAPI and callers caught/registered that class directly.
- Runnable tests: response, configuration, token, provider, validation and API #1–#7 tests are available in the Study virtual environment.
- Runtime wiring: `create_app` registers the application error handler; `TraceIdMiddleware` catches escaped application errors and serializes them with the shared response builder.

## SOURCE_TRACE

```text
API/helper -> ApiError(...) factory -> raise _ApiError -> FastAPI handler or TraceIdMiddleware -> error_response -> HTTP envelope
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Exception identity | `ApiError` is now a function and cannot itself be used by `raise` handling APIs; private `_ApiError` is the raised instance type | RESOLVED | Updated handler registration, catches, annotations and tests while preserving `raise ApiError(...)` |
| Context source drift | Full validator reports tracked source drift from the 2026-09-18 snapshot across Study and other scopes | CONTEXT_STALE | Registry/page graph separately passes with drift checking skipped |

## CHANGES

- Files changed: Study `responses.py`, middleware/composition, security/config/services/API helper and view call sites, related tests and response documentation.
- CONTEXT_UPDATES: Documented `ApiError` as a factory and `_ApiError` as its internal exception type; updated linked architecture/test context.
- Context pages changed: `.agents/server-study/{architecture,core/runtime,tests}.md`.
- Assumptions: Keep all current exception parameters/defaults, status and business mappings, trace behavior, and the external `raise ApiError(...)` syntax.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read three matching coding worklogs; no shortage | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest tests/core/test_responses.py -q` | 6 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 161 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app tests` | All checks passed after removing two unused test imports | VERIFIED |
| `cd apps/study-server && .venv/bin/mypy app` | No issues found in 56 source files | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.main import app; assert len(app.openapi()["paths"]) == 13; print("composition ok: 13 paths")'` | App imported; OpenAPI contains 13 paths | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | Reports `CONTEXT_STALE` across tracked source in multiple scopes against the existing snapshot | CONTEXT_STALE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK`; registry and page graph valid | VERIFIED |

## HANDOFF

- Remaining blockers: Full context validation remains stale because the source snapshot predates current tracked code; no runtime/test/static-check blocker remains.
- Next owner/action: None.
