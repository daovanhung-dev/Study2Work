---
task_id: "2026-09-22-implement-study-api6-courses"
date: "2026-09-22"
primary_task_type: "coding"
secondary_task_types: ["test", "docs", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study API #6 Public Courses

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/implement-study-api2-verify-email-send.md`
    - carry_forward: Bảo toàn thay đổi API #2 trong working tree; giữ canonical envelope, injectable boundary và dùng `apps/study-server/.venv` cho verification.
  - path: `.agents/worklog/2026-09-22/implement-study-api4-users-me.md`
    - carry_forward: Giữ namespace `guest`, parameterized query, transaction ownership và không claim live DB verification từ schema artifact.
  - path: `.agents/worklog/2026-09-22/implement-study-api5-categories.md`
    - carry_forward: Dùng pattern public read-only module, rollback an toàn khi query lỗi, đồng bộ DD/context và giữ migration/live-schema boundary rõ ràng.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement public `GET /api/v1/courses` theo DD `apps/study-server/docs/dd/06_courses`.
- Contract decisions: page mặc định 1, size mặc định 20 và range 1..100; sort allow-list `id|name|price|created_at` với `asc|desc`, default `created_at:desc,id:asc`; category hợp lệ về kiểu nhưng bị từ chối 422 khi được gửi do chưa có course-category relation; chỉ trả `PUBLISHED`; price là decimal-string; missing mentor là 500; empty total_pages là 0.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` chưa expose `/api/v1/courses`; schema artifact có `courses` và `users`, nhưng live metadata chưa được verify.
- Runnable tests: Current Study suite collected 93 tests through `apps/study-server/.venv/bin/pytest`; no API #6 tests exist.
- Runtime wiring: FastAPI + sync SQLAlchemy + canonical response/trace handlers are active; existing API #2 changes are uncommitted user work and remain out of scope.

## SOURCE_TRACE

```text
GET /api/v1/courses
-> CourseQuery dependency and validation
-> courses.view.get_courses
-> courses.query list/count SQL over courses LEFT JOIN users
-> published-course and mentor integrity checks
-> Course/CoursePage mapping with decimal-string price
-> canonical success/error envelope + trace ID
-> focused API #6 tests + full Study checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD #6 status | Cover says `Draft — Needs Confirmation`; user explicitly selected implementation policies | RESOLVED_FOR_IMPLEMENTATION | Sync resolved policies but retain approval status unless formally approved |
| `category` relation | DD and schema artifact have no course-category relation | RESOLVED_FOR_IMPLEMENTATION | Parse query type, return 422 when supplied; do not invent JOIN/schema |
| `mentor_id` nullability | Schema artifact permits nullable FK while DD requires mentor object | RESOLVED_FOR_IMPLEMENTATION | Detect missing joined mentor and map to safe 500 |
| Live courses/users metadata | Only checked-in schema artifact is available | SOURCE_REQUIRED | No migration or live DB claim |
| Existing API #2 worktree changes | Modified/untracked files are present before this task | USER_CHANGES_PRESERVED | Do not overwrite or refactor verify-email files |

## CHANGES

- Files changed: Added `app/modules/guest/courses/{__init__,models,query,view}.py` and `tests/modules/guest/test_courses.py`; wired `/api/v1/courses` and its contract validation path; preserved existing API #2 verify-email changes.
- CONTEXT_UPDATES: Registered API #6 as source-backed, documented pagination/sort/category/mentor policies, recorded course schema/live DB boundary and updated current Study route/test status.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`, `.agents/project/source-status.md`; synced all DD #6 markdown sheets.
- Assumptions: No category-course schema change; query layer remains read-only and never commits; live DB metadata remains unverified; DD approval metadata remains TBD.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3/12 coding worklogs; all 3 read | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest --collect-only -q` | 93 tests collected with existing Starlette/httpx deprecation warning | VERIFIED |
| `git status --short --branch` | Existing API #2/context changes recorded before implementation | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest tests/modules/guest/test_courses.py -q` | 21 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | 114 passed; existing Starlette/httpx deprecation warning | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `cd apps/study-server && .venv/bin/mypy app` | No issues found in 50 source files | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff format --check app tests` | 2 pre-existing legacy files would be reformatted | CONTEXT_BASELINE |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` across deep scopes; no new registry/link failure | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: Live `courses/users` metadata and migration/application state are not verified; full context validator remains stale against the repository snapshot; Starlette/httpx emits one deprecation warning.
- Next owner/action: Verify the target Study database schema before relying on the endpoint in a live environment; no code changes remain for API #6.
