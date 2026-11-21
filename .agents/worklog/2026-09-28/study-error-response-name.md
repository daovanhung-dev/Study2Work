---
task_id: "2026-09-28-study-error-response-name"
date: "2026-09-28"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Đổi tên ApiError thành error_response trong Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Preserve the standard response behavior and keep the independent AI Server copy out of this Study change.
  - path: `.agents/worklog/2026-09-28/study-apierror-direct-json.md`
    - carry_forward: Error construction returns `JSONResponse` directly; preserve the six-key envelope, HTTP/business mappings, trace header and field errors.
  - path: `.agents/worklog/2026-09-28/study-apierror-factory.md`
    - carry_forward: Preserve error defaults, status/business mappings and current trace behavior while updating call sites.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Rename Study's direct JSON error factory `ApiError(...)` to `error_response(...)` and update all active Study source, tests, documentation and project context references.
- Canonical contract/approved plan: Keep the same function signature, `JSONResponse` return type and HTTP behavior. Do not add an `ApiError` alias, rewrite historical worklogs, or change the independent AI/Work Server implementations.

## CURRENT_BEHAVIOR

- Source/config: `app/core/responses.py` defines `error_response(...)`; application handlers, token helpers, validators, views, shared course helpers and the Study Ollama adapter import/call it directly.
- Runnable tests: `tests/core/test_responses.py` verifies status, standard envelope, field errors, extra headers and trace behavior under the renamed function. Study suite contains 163 tests.
- Runtime wiring: Returned `JSONResponse` values propagate to FastAPI routes; exception handlers use the same direct response factory. No `ApiError` class or raised custom exception remains in Study runtime.
- Pre-existing worktree: clean before worklog creation.

## SOURCE_TRACE

```text
validator/view/security/helper or FastAPI exception handler -> responses.error_response(...) -> JSONResponse -> route/client
tests and current Study docs/context -> import/name and behavior contract
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Public helper name | Approved requirement specifies `error_response`; current Study source and active context now use that name | RESOLVED | Definition and all active Study call sites/docs/context were renamed without changing response behavior. |
| Similar symbols in other scopes/history | Work Server and AI Server define independent `ApiError`; AI context documents its copied core; historical worklogs record prior Study designs | OUT_OF_SCOPE | Leave those files unchanged. |

## CHANGES

- Files changed: `app/core/responses.py`; current Study middleware, security, validators/views and Ollama adapter callers; affected Study tests; Study README/codebase guide; this worklog.
- CONTEXT_UPDATES: Current Study context and app/codebase documentation now identify `error_response(...)` as the direct error response builder and describe returned JSON responses accurately.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `core/database-security.md`, `core/runtime.md`, `modules/README.md`, `modules/register-account.md`, `services/ai.md`, `tests.md`, `workflows/README.md`.
- Assumptions: No compatibility alias; error response signature and wire contract remain unchanged. Historical worklogs are immutable audit records.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read three matching coding worklogs; no shortage | VERIFIED |
| `/tmp/study-server-codex-venv/bin/python -m pytest -q tests/core/test_responses.py tests/core/test_exceptions.py tests/modules/guest/api_03_auth_login/test_auth_login.py tests/modules/guest/api_04_users_me/test_users_me.py tests/service/ai/test_ollama_service.py` | 42 passed, 1 dependency deprecation warning | PASS |
| `/tmp/study-server-codex-venv/bin/python -m pytest -q` | 163 passed, 1 dependency deprecation warning | PASS |
| `.venv/bin/ruff check app tests` | All checks passed | PASS |
| `/tmp/study-server-codex-venv/bin/mypy app` | Success: no issues found in 62 source files | PASS |
| Import/OpenAPI probe (`create_app().openapi()`) | Imported app; OpenAPI 3.1.0 generated with 13 paths | PASS |
| `git grep -n -E 'ApiError|api_error' -- apps/study-server .agents/server-study` | No matches (exit 1 means no matching legacy symbol) | PASS |
| `git diff --check` and AI/Work scope status check | No whitespace errors; no AI Server or Work Server files changed | PASS |
| `deno run -A scripts/validate-agent-context.mjs` | Fails on pre-existing missing DB Admin context/source paths and stale source snapshots across scopes, including Study; earlier 2026-09-28 worklogs record this repository baseline | CONTEXT_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Still fails on the pre-existing missing DB Admin context/source paths; no Study page-graph-specific error is reported | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains red because DB Admin context/source paths are absent and tracked source snapshots are stale; this is recorded in earlier context worklogs and does not block the Study rename.
- Next owner/action: Implementation and Study-specific verification are complete; refresh the repository-wide context registry/snapshots in a separate maintenance task if a green global validator is required.
