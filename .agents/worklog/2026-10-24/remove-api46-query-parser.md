---
task_id: "2026-10-24-remove-api46-query-parser"
date: "2026-10-24"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Remove API #46 query parser helper

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/api46-mentor-courses.md`
    - carry_forward: Preserve the approved API #46 request/response behavior and existing implementation; only remove the redundant parser function.
  - path: `.agents/worklog/2026-10-24/load-study-server-coding-context.md`
    - carry_forward: Keep the change within Study Server and preserve unrelated worktree state.
  - path: `.agents/worklog/2026-10-12/merge-viet-dev-into-develop.md`
    - carry_forward: Keep Study scope narrow and do not infer live schema behavior from local artifacts.
- shortage: `none` (selector found 34 coding worklogs and selected 3)

## EXPECTED_BEHAVIOR

- Requirement: Remove `parse_mentor_courses_query` and its dependency wrapper from the API #46 route while preserving the same query names, defaults, schema metadata, validation behavior, and Mentor course response.
- Canonical contract/approved DD: API #46 behavior remains as approved and recorded in `.agents/worklog/2026-10-24/api46-mentor-courses.md`; this request changes only route wiring structure.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` defines a standalone query parser that receives `status`, `page`, and `size`, constructs `MentorCourseQuery`, and is wrapped by `mentor_courses_query_dependency`; the route consumes that dependency.
- Runnable tests: The current API #46 route tests cover auth, query validation, list results, response mapping, pagination, SQL binding, and failures; baseline full suite has 261 passing tests.
- Runtime wiring: `GET /api/v1/mentor/courses` calls `get_mentor_courses(...)` in the Mentor module; query validation, SQL, auth, and response behavior are outside the parser helper.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses -> route parses status/page/size -> MentorCourseQuery is assembled in the route
-> auth/validation -> count/page queries -> CoursePage response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Query parser is a thin adapter | Function only packages FastAPI-parsed fields into `MentorCourseQuery`; route can declare those fields directly | CONFIRMED | Remove the extra function/dependency layer without changing the endpoint contract. |

## CHANGES

- Files changed: `apps/study-server/app/api/v1.py`; this worklog.
- CONTEXT_UPDATES: No endpoint contract change; the route now declares its query fields directly, and uses shared page/size defaults. Removed `parse_mentor_courses_query` and `mentor_courses_query_dependency`.
- Context pages changed: None; existing API #46 context describes the externally visible route and remains accurate.
- Assumptions: Keep `MentorCourseQuery` for module validation/view signatures; do not refactor auth, SQL, response, or other route parsers.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | Existing API #46 changes and prior untracked context worklog are present and will be preserved | VERIFIED |
| Worklog selector and review | Three same-type coding worklogs selected and read; no shortage | VERIFIED |
| `.venv/bin/pytest tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py -q` | `28 passed`, one existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/pytest -q` (`apps/study-server`) | `261 passed`, one existing Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app/api/v1.py` | `All checks passed!` | VERIFIED |
| Import/OpenAPI probe | API #46 still composes with `status`, `page`, `size`, and `Authorization`; defaults are `1` and `20`, status enum remains `DRAFT`/`PUBLISHED` | VERIFIED |
| Search for `parse_mentor_courses_query` and `mentor_courses_query_dependency` | No references remain in Study source or Study context | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |

## HANDOFF

- Remaining blockers: None for this scoped route refactor.
- Next owner/action: The helper removal is complete; retain the pre-existing API #46 implementation/context changes and the earlier context-loading worklog.
