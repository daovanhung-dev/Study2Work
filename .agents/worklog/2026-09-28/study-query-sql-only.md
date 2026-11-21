---
task_id: "2026-09-28-study-query-sql-only"
date: "2026-09-28"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Giữ query.py chỉ chứa SQL trong Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Preserve current Study response contracts and use the Study virtual environment for verification.
  - path: `.agents/worklog/2026-09-28/study-apierror-factory.md`
    - carry_forward: Keep API #1–#7 error/status mappings intact and record context drift separately from runtime verification.
  - path: `.agents/worklog/2026-09-27/document-study-main-functions.md`
    - carry_forward: Preserve unrelated Study `main.py` documentation and use Deno for context validation when Node is unavailable.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: every Study `query.py` contains only SQL string constants; DB helper functions and execution imports belong in `view.py`.
- Canonical contract/approved plan: move existing helpers from API #1, #4, #5, #6 and #7 into their views, preserve helper names and behavior, and update module context.

## CURRENT_BEHAVIOR

- Source/config: API #1, #4, #5, #6 and #7 query modules contained functions that executed `query_one`/`query_many`; API #3 already held SQL constants only.
- Runnable tests: targeted API #1/#4/#5/#6/#7 tests and the full Study suite are runnable in `apps/study-server/.venv`.
- Runtime wiring: each affected view imports query helpers from its sibling query module; API #6/#7 unit tests call their query helpers through that module.

## SOURCE_TRACE

```text
router -> view helper/orchestrator -> query_one/query_many(SQL constant) -> caller-owned Session transaction -> response -> API module tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Query-module responsibility | Five query modules combined SQL and Python execution helpers despite the module-layer context assigning execution to views | RESOLVED | Helpers moved to views; all six query modules contain only SQL string constants |
| Full context validation | Validator reports tracked source drift against the 2026-09-18 snapshot across Study and other scopes | CONTEXT_STALE | Registry/page/worklog structure passes with drift checking skipped |

## CHANGES

- Files changed: API #1/#4/#5/#6/#7 `query.py` and `view.py`; API #6/#7 tests; Study module context and this worklog.
- CONTEXT_UPDATES: Defined `query.py` as SQL constants only and updated register-account flow ownership.
- Context pages changed: `.agents/server-study/modules/README.md`, `.agents/server-study/modules/register-account.md`.
- Assumptions: Keep SQL text, helper names/signatures, sort allowlist, parameter binding, result defaults, and transaction ownership unchanged.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read three matching coding worklogs; no shortage | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest tests/modules/guest/api_01_auth_register/test_register.py tests/modules/guest/api_04_users_me/test_users_me.py tests/modules/guest/api_05_categories/test_categories.py tests/modules/guest/api_06_courses/test_courses.py tests/modules/guest/api_07_courses_search/test_courses_search.py -q` | 81 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 161 passed; one existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `cd apps/study-server && .venv/bin/mypy app` | No issues found in 56 source files | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.main import app; assert len(app.openapi()["paths"]) == 13; print("composition ok: 13 paths")'` | App imported; OpenAPI contains 13 paths | VERIFIED |
| Study `query.py` AST scan | All six files contain only uppercase-name assignments to string constants | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | Reports `CONTEXT_STALE` across tracked source against the existing snapshot | CONTEXT_STALE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK`; registry and page graph valid | VERIFIED |

## HANDOFF

- Remaining blockers: Full context drift validation remains stale against the repository snapshot; runtime, tests, typing and lint checks pass.
- Next owner/action: None.
