---
task_id: "2026-09-22-implement-study-api7-courses-search"
date: "2026-09-22"
primary_task_type: "coding"
secondary_task_types: ["docs", "test", "context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study courses/users schema artifact; course-category relation remains absent"]
status: "VERIFIED"
---

# Worklog: Implement Study API #7 course search

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/implement-study-api2-verify-email-send.md`
    - carry_forward: Giữ canonical envelope, provider/route boundaries và dùng `apps/study-server/.venv` cho verification.
  - path: `.agents/worklog/2026-09-22/implement-study-api4-users-me.md`
    - carry_forward: Giữ namespace `guest`, parameterized query, trace handling và không claim live DB verification.
  - path: `.agents/worklog/2026-09-22/implement-study-api5-categories.md`
    - carry_forward: Dùng public read-only module pattern, rollback khi query lỗi, đồng bộ DD/context và không invent schema ngoài quyết định.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `GET /api/v1/courses/search` theo DD API #7, giữ nguyên API #6 và không thay đổi schema/migration.
- Contract decisions: public endpoint; `q` trim/lowercase; `category` gửi lên trả `422`; `page` mặc định `1`; fixed size `20`; sort `field:direction` allow-list; chỉ lấy `PUBLISHED`; canonical `200/422/500` envelope.

## CURRENT_BEHAVIOR

- Source/config: API #6 đã có `guest/courses` models/query/view; API #7 route đã được wire trong `app/api/v1.py`. Schema artifact chỉ xác nhận `courses`, `users` và `courses.mentor_id`; không có course-category relation.
- Runnable tests: Baseline API #6 focused tests pass; after implementation collection is 134 tests. Final verification is recorded below.
- Runtime wiring: New route is composed through `app/api/v1.py`; search page/count queries are read-only and parameterized; no live DB claim.

## SOURCE_TRACE

```text
GET /api/v1/courses/search
-> parse_course_search_query / CourseSearchQuery
-> courses.view.search_courses
-> category pre-query rejection when supplied
-> courses.query search page/count over courses LEFT JOIN users
-> published/mentor integrity checks + CoursePage mapping
-> canonical response + trace ID
-> focused API #7 tests + full Study checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Course-category relation | `DB.sql`/`DB_UNICA_TABLES.md` contain `categories` but no course relation | RESOLVED_FOR_IMPLEMENTATION | Reject supplied `category` with `422`; no fabricated JOIN/table/column |
| Sort contract | DD example was underspecified; API #6 source-backed convention is `field:direction` | RESOLVED_FOR_IMPLEMENTATION | Reuse allow-list and default order from API #6 |
| Mentor join semantics | DD describes `INNER JOIN` but also requires `500` for missing mentor; API #6 uses left join integrity check | DISCREPANCY_RESOLVED | Use `LEFT JOIN` plus `missing_mentor_count` to preserve safe integrity error |
| Live DB metadata | Only checked-in schema/design artifact is available | SOURCE_REQUIRED | No migration or live DB availability claim |
| Test dependency warning | Starlette/httpx emits existing deprecation warning | CONTEXT_BASELINE | Tests pass; dependency upgrade out of scope |

## CHANGES

- Files changed: Added API #7 search model/query/view path, route parser/wiring, focused tests, exception contract path and API #7 DD/context/worklog updates.
- CONTEXT_UPDATES: Registered API #7 as source-backed after verification; documented fixed page size, q predicate, category boundary, sort convention and live DB status.
- Context pages changed: `.agents/server-study/{AGENTS,architecture,apis/declared-routes,core/runtime,modules/README,tests}.md`, `.agents/project/source-status.md`, and `docs/dd/07_courses_search/*`.
- Assumptions: No q length cap because DD did not specify one; extra `size` query is not declared or used; API #6 behavior remains unchanged.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3/13 coding worklogs; all selected logs read | VERIFIED |
| `./.venv/bin/pytest tests/modules/guest/test_courses_search.py -q` | 20 passed; existing Starlette/httpx warning | VERIFIED |
| `./.venv/bin/pytest --collect-only -q` | 134 tests collected | VERIFIED |
| `./.venv/bin/pytest -q` | 134 passed; existing Starlette/httpx warning | VERIFIED |
| `./.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `./.venv/bin/mypy app` | No issues found in 50 source files | VERIFIED |
| `./.venv/bin/ruff format --check app/modules/guest/courses/view.py` | File already formatted | VERIFIED |
| `./.venv/bin/ruff format --check app tests` | Pre-existing `core/constants.py` and `core/database.py` still require formatting | CONTEXT_BASELINE |
| `git diff --check` | No whitespace errors | VERIFIED |
| `python3` DD link/JSON check | 8 DD files; no broken relative links or invalid JSON examples | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Repository-wide pre-existing `CONTEXT_STALE`; drift-free validation passes | CONTEXT_BASELINE |

## HANDOFF

- Remaining blockers: Live `courses/users` metadata and course-category relation are not verified/implemented; full formatter baseline still has two pre-existing files; Starlette/httpx warning remains. These are outside API #7 implementation scope.
- Next owner/action: Verify target Study DB before live deployment; add category relation only through a new approved contract/schema task.
