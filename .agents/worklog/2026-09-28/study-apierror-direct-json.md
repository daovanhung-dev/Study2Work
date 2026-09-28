---
task_id: "2026-09-28-study-apierror-direct-json"
date: "2026-09-28"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Chuyển lỗi Study Server sang JSONResponse trực tiếp

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Preserve the success envelope and do not modify the separate AI Server implementation.
  - path: `.agents/worklog/2026-09-28/study-apierror-factory.md`
    - carry_forward: Preserve API #1–#7 status/business mappings and safe error messages while changing transport from raised custom errors to returned responses.
  - path: `.agents/worklog/2026-09-28/study-query-sql-only.md`
    - carry_forward: Keep transaction ownership/rollback behavior in views and update module context when validation ownership changes.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: `ApiError(...)` returns a `JSONResponse` directly; remove `_ApiError` and `error_response`; route/business errors return and propagate responses without custom exception instances.
- Canonical contract/approved plan: Preserve the existing six-key error envelope, HTTP status, business codes, field error metadata, optional headers and `X-Trace-Id`. Put shared validators in `app/utils/validate.py`, add a validator module to every guest API #1–#7, and keep request models declarative with type conversion only. Keep OpenAPI validation metadata without executing validation in models.

## CURRENT_BEHAVIOR

- Source/config: `ApiError` constructs `_ApiError`; `error_response` serializes it; direct raises/catches and type annotations are spread across core, security, API views, helpers and the Study Ollama adapter. `http_exception_handler` exists but `create_app` does not register it. Request models contain custom validators/field constraints.
- Runnable tests: Prior coding worklogs report 161 tests while `.agents/server-study/tests.md` reports 160; this change will establish the current count by running the full suite.
- Runtime wiring: `create_app` registers `_ApiError`, request-validation and generic exception handlers; `TraceIdMiddleware` catches `_ApiError` and adds the trace header. Study composition currently has 13 routes according to prior verified worklogs.
- Pre-existing worktree: `git status --short` was empty before edits.

## SOURCE_TRACE

```text
route/view -> ApiError JSONResponse -> TraceIdMiddleware adds X-Trace-Id -> HTTP client
Pydantic/HTTPException/unhandled exception -> FastAPI handler -> ApiError JSONResponse
module validator -> ApiError JSONResponse or normalized value -> view business logic/DB
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| HTTP exception handler wiring | `create_app` now registers `http_exception_handler`; an app-level 404 test checks envelope and trace header | RESOLVED | Starlette HTTP exceptions now use the standard envelope. |
| Study test count | Full suite collected and passed 163 tests; `tests.md` updated | RESOLVED | The earlier 160/161 counts were stale. |
| OpenAPI Study contract | Registry records no canonical Study OpenAPI contract | NOT_FOUND | Preserve existing generated metadata from the current models as route metadata. |

## CHANGES

- `apps/study-server/app/core/responses.py`: `ApiError(...)` now builds and returns the canonical `JSONResponse`; removed the exception class and serializer.
- `app/core/middleware.py` and `app/main.py`: handlers return direct responses; `HTTPException` handling is registered; trace middleware keeps setting the response header.
- `app/api/v1.py` and API #1–#7 modules: route/view return paths propagate `JSONResponse`; each API has `validate.py`; request models now declare data/types, and route OpenAPI metadata preserves prior constraints.
- `app/core/security/*`, `app/utils/auth.py`, and Study `app/service/ai/ollama_service.py`: token/Ollama errors now return and propagate `JSONResponse`; no AI Server files were changed.
- Tests updated for direct responses and validator ownership; route rollback/mapping checks remain.
- Context/readme updates: Study runtime, module ownership, register flow, Ollama boundary, test status/workflow, app README and codebase README; registered every API #1–#7 `validate.py` in `.agents/context-manifest.json`.
- CONTEXT_UPDATES: Completed for response/runtime, validation workflow/module ownership, register flow, Ollama and error/testing contract; final test count and context validator result pending.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `core/runtime.md`, `modules/README.md`, `modules/register-account.md`, `services/ai.md`, `tests.md`, `workflows/README.md`; context manifest source registry updated for validators #2–#7.
- Assumptions: Native framework/library exceptions remain as control-flow signals where required; their HTTP serialization and all custom application error responses use `ApiError`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read three matching coding worklogs; no shortage | VERIFIED |
| Original `apps/study-server/.venv` import | Installed `anyio` and `typing_extensions` files fail with `IndentationError`; did not modify the repository environment | ENVIRONMENT_ISSUE |
| Temporary locked Study env (`/tmp/study-server-codex-venv`) | Created with `uv sync --frozen`; reinstalled malformed cached `anyio`/Pydantic dependencies without cache before checks | READY |
| `/tmp/study-server-codex-venv/bin/pytest -q` | `163 passed, 1 warning` | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `/tmp/study-server-codex-venv/bin/mypy app` | No issues in 62 source files | VERIFIED |
| `.venv/bin/python -m compileall -q app tests` and `git diff --check` | Both passed | VERIFIED |
| Study import/OpenAPI probe | Composition imported, 13 paths found; register/login/verify email formats and course pagination constraints preserved | VERIFIED |
| `git grep -E '_ApiError|error_response|raise ApiError|api_error_handler' -- apps/study-server .agents/server-study` | No matches | VERIFIED |
| `.venv/bin/ruff format --check app tests` | 18 files would be reformatted, including existing untouched files; no repository-wide formatting changes applied | CONTEXT_BASELINE |
| `node scripts/validate-agent-context.mjs` | Node is not installed; ran equivalent script under Deno | ENVIRONMENT_ISSUE |
| `deno run --allow-all scripts/validate-agent-context.mjs` | Reports baseline missing `db-admin` context/source paths and stale tracked roots across scopes | CONTEXT_STALE |
| `deno run --allow-all scripts/validate-agent-context.mjs --skip-drift` | Still reports missing `db-admin` context/source paths; no Study-specific structural issue reported | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: The repository-wide context validator reports missing `db-admin` files and stale roots outside this Study task; the formatter check reports existing formatting drift.
- Next owner/action: Study implementation, tests, route/OpenAPI import and static checks are complete; global context/format findings are recorded for repository maintenance.
