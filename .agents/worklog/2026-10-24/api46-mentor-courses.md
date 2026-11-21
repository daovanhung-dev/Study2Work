---
task_id: "2026-10-24-api46-mentor-courses"
date: "2026-10-24"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #46 Mentor courses

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/load-study-server-coding-context.md`
    - carry_forward: Preserve this existing untracked context-loading worklog; keep runtime/test claims distinct from documentation baselines.
  - path: `.agents/worklog/2026-10-12/merge-viet-dev-into-develop.md`
    - carry_forward: Keep Study scope narrow; do not claim checked-in DDL proves live schema; this task's full-suite run later verified API #08/#09 tests in the current tree.
  - path: `.agents/worklog/2026-10-11/centralize-study-auth-token-helpers.md`
    - carry_forward: Use `app/utils/auth.py` bearer/claim primitives, preserve response contracts, and keep DB transaction ownership in the view/caller.
- shortage: `none` (selector found 33 coding worklogs and selected 3)

## EXPECTED_BEHAVIOR

- Requirement: Implement read-only `GET /api/v1/mentor/courses` according to API #46 and the user-approved decisions: numeric JWT `sub`, role `MENTOR`, direct ownership through `courses.mentor_id`, allowed status values `DRAFT`/`PUBLISHED`, API #6 pagination/order convention, and `data: null` for Study error envelopes.
- Canonical contract/approved DD: `apps/study-server/docs/dd/46_mentor_courses/` and `docs/lists/list_api.md`; user decisions in this task resolve direct-owner scope, identity, status members, list behavior, and shared error data shape.

## CURRENT_BEHAVIOR

- Source/config: `/api/v1/mentor/courses` is absent from `app/api/v1.py`; no Mentor module or API #46 test exists. `app/utils/auth.py` validates positive numeric `sub` and normalized role claims, while its existing request guard is Student-only. API #6 reads the legacy `courses`/`users` projection through parameterized SQL and shared Course/Page mapping. `tests/conftest.py` builds an isolated `TestClient`; API #4 tests mock token decoding and verify role rejection before lookup. Checked-in DDLs conflict; no live schema check is part of this task.
- Runnable tests: API #6 tests cover pagination, mapping, query failure and validation patterns. `error_response()` currently serializes omitted `data` as `{}`; response and exception helper tests contain affected assertions. Full current test status will be measured during verification.
- Runtime wiring: `DESIGN_CONTRACT_PATHS` currently omits API #46, so framework validation/unhandled exceptions would use generic business codes until the route is registered there. `validate_current_user_request()` cannot be reused because it requires `STUDENT`; the Mentor module validator will compose the shared bearer extraction, claim validation and JWT decoder with the approved `MENTOR` role check.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses -> parse MentorCoursesQuery -> validate Bearer/JWT numeric sub + MENTOR role
-> validate status/page/size -> view -> parameterized owner-scoped count + page reads
-> shared Course mapping + Pagination -> success envelope; direct 401/403/422/500 error response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD #46 was draft with assignment/schema/status/pagination questions | User approved legacy numeric identity, direct-owner only, `DRAFT`/`PUBLISHED`, and API #6 pagination behavior | RESOLVED_BY_USER | Implement only the approved direct-owner API; do not include assigned courses. |
| Error data shape differs | API guideline/DD says `null`; current Study helper/tests produce `{}` | RESOLVED_BY_USER | Update shared Study helper and affected tests to serialize `null`. |
| Live DB schema | Legacy and V1-PILOT artifacts differ; no live metadata probe requested | NOT_VERIFIED_HERE | Implement source against legacy model used by API #6; make no live database/deployment claim. |

## CHANGES

- Files changed:
  - `apps/study-server/app/api/v1.py`
  - `apps/study-server/app/core/middleware.py`
  - `apps/study-server/app/core/responses.py`
  - `apps/study-server/app/modules/mentor/__init__.py`
  - `apps/study-server/app/modules/mentor/api_46_mentor_courses/{__init__,models,query,validate,view}.py`
  - `apps/study-server/tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py`
  - `apps/study-server/tests/core/test_responses.py`
  - `apps/study-server/tests/core/test_exceptions.py`
  - `.agents/context-manifest.json`
  - `.agents/server-study/{AGENTS.md,architecture.md,apis/declared-routes.md,core/runtime.md,modules/README.md,tests.md}`
  - `.agents/worklog/2026-10-24/api46-mentor-courses.md`
- CONTEXT_UPDATES: Added API #46 to route/module/runtime/test context and manifest. Updated error envelope contract to `data: null`; full-suite verification also confirmed API #08/#09 HTTP tests pass in the current tree.
- Context pages changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `modules/README.md`, `tests.md`, and `.agents/context-manifest.json`.
- Assumptions: No assignment relation, schema migration, client, API #47/#48, or live database change is in scope.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; pre-existing untracked `load-study-server-coding-context.md` preserved | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected three same-type worklogs; all selected files were read | VERIFIED |
| Source trace: router/auth/API #4/API #6/database/response/tests | Confirmed route/module absence, numeric role claims, shared mapping/query patterns, Student-only shared guard, error path mapping and affected response helper assertions | VERIFIED |
| `.venv/bin/pytest tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py tests/core/test_responses.py tests/core/test_exceptions.py -q` | `38 passed`, one existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/pytest -q` (`apps/study-server`) | `261 passed`, one existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check .` (`apps/study-server`) | `All checks passed!` | VERIFIED |
| Import/OpenAPI probe | `create_app()` composed `/api/v1/mentor/courses`; OpenAPI exposed 16 `/api/v1` paths | VERIFIED |
| Context manifest JSON parse | `.agents/context-manifest.json` parsed successfully | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID` remains due missing DB Admin pages/source roots and broad existing source-snapshot drift. Output contains no API #46 missing-source/manifest error. | BASELINE_FAILURE |

## HANDOFF

- Remaining blockers: Repository-wide context validator remains invalid on the existing DB Admin checkout gaps and source-snapshot drift; live Study schema/deployment were not checked.
- Next owner/action: API #46 implementation and local verification are complete. Preserve the pre-existing untracked `.agents/worklog/2026-10-24/load-study-server-coding-context.md`.
