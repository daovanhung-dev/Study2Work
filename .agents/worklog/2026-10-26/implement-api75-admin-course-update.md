---
task_id: "2026-10-26-implement-api75-admin-course-update"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-32 APIs #74/#76/#77 share course-management boundary and /admin/courses/{course_id} route template"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #75 Admin course update

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 69 coding worklogs available; selected and read all 3; no shortage. The active API #75 worklog was itself in the selected set and was reviewed as the pre-code plan.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Use shared `ADMIN` JWT guard, route-template matching, Course mapper and Page singleton; keep #74's candidate choices derived and preserve the dirty worktree.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: This active worklog contains the implementation plan and source-trace decisions; no API #75 code existed at this preflight checkpoint.
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: `query.py` is SQL constants only; `view.py` owns orchestration/transaction; checked-in migrations and fake DB tests do not prove live schema.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-32 APIs #74/#76/#77; shared /api/v1/admin/courses/{course_id} path]
```

## EXPECTED_BEHAVIOR

- Requirement: Implement `PUT /api/v1/admin/courses/{course_id}` for AC-32, following the approved source order: activity diagram → schema/infrastructure → API catalog. If the body remains absent from direct sources, use the clearest fallback and record it as `DERIVED`.
- Direct catalog/diagram contract: Admin Bearer JWT; required signed-int64 `course_id`; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Page<Course>>`; errors 401/403/404/422/500 with catalog codes. AC-32 assigns metadata update to #75, status plus audit to #76, and soft-delete to #77.
- Existing DD #75 proposal: full-replacement JSON body `title`, `description`, `thumbnail_url`, `price`; map to legacy `courses.name`, `description`, `thumbnail_url`, `price`; update `updated_at`; preserve status and mentor; return singleton CoursePage as #74. DD remains `Draft — Needs Confirmation`.

## CURRENT_BEHAVIOR (pre-edit)

- Runtime: API #75 route, module and focused tests are absent. API #74 already registers `PUT`-compatible path template `/api/v1/admin/courses/{course_id}` in middleware through the current GET route; shared auth supports role `ADMIN`.
- Schema: Legacy `courses` has BIGINT ID, `name VARCHAR(200) NOT NULL`, nullable `description`/`thumbnail_url`, nullable `price NUMERIC(12,2)`, `status`, `mentor_id`, and required `updated_at`. V1-PILOT uses UUID/versioned Course and is incompatible with the API int64 candidate. Neither proves live DB schema.
- Related source: API #70 demonstrates a strict Pydantic body, shared ADMIN auth, signed-int64 parsing, safe error mapping and commit/rollback. API #73/#74 provide the shared Course mapper and response contract. API #14 provides a parameterized update/commit pattern but is not an Admin policy source.
- Related API boundary: API #74 uses the same detail path for GET; #76/#77 use separate paths/operations. #75 must not change status, mentor, counters, category or audit.
- Worktree: `develop...origin/develop` is already extensively modified/untracked across Study APIs, DDs, schema artifacts and context. Preserve all existing changes; do not stage, commit or clean.

## SOURCE_TRACE

```text
PUT /api/v1/admin/courses/{course_id}
  -> strict candidate body model + raw path/header route inputs
  -> shared ADMIN guard -> signed-int64 path and decimal/DDL validation
  -> bound UPDATE of metadata only, status/mentor untouched, updated_at=CURRENT_TIMESTAMP
  -> validate UPDATE RETURNING identity -> bound Course/mentor SELECT in same transaction
  -> shared map_course -> singleton Page<Course> -> commit -> DESIGN_RESOURCE_UPDATED envelope
  -> query/projection/commit failure rolls back; no updated row -> 404
  -> focused API #75 and linked AC-32 regression tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog and diagram declare only `course_id`; diagram only says “UPDATE course metadata”; existing DD proposes four fields. | `DISCREPANCY / DERIVED_FALLBACK` | Implement DD's four-field full replacement and keep DD Draft; do not change catalog/diagram. |
| Full replacement/null behavior | DD proposes all four keys required and null clears description/thumbnail; no approved body contract. | `DERIVED` | Require all keys; permit null only for description/thumbnail; reject unknown fields. |
| Title limit | Legacy `courses.name VARCHAR(200)`; no live metadata. | `DERIVED` | Enforce max 200 from checked-in DDL; do not trim or invent nonblank policy. |
| Price format/range | Contract requires decimal-string; legacy DDL candidate is `NUMERIC(12,2)` but permits NULL and has no nonnegative CHECK. | `DERIVED` | Require finite decimal string with at most 2 fraction digits and at most 10 effective integer digits; preserve exact Decimal; allow negative values because no source forbids them. |
| Admin permission | AC-32 says course-management permission; current APIs expose shared role `ADMIN`, no dedicated policy. | `DERIVED` | Enforce shared ADMIN role before path/business validation and DB; do not claim finer permission. |
| Schema selection | Legacy BIGINT and V1-PILOT UUID/versioned schemas conflict. | `DERIVED / NOT_VERIFIED_HERE` | Target checked-in legacy candidate only; no migration and no live-schema claim. |
| Response cardinality | Catalog says Page<Course> for PUT-by-ID with no page inputs; #74 uses singleton Page. | `DERIVED` | Return one updated Course with pagination 1/1/1/1. |
| Status/audit/owner | AC-32 separates #75 metadata from #76 status/audit; no owner transfer field in DD. | `DIRECT_BOUNDARY` | Do not mutate `status`, `mentor_id`, category, counters or audit rows. |
| Path errors | #75 catalog includes 422; #70 maps malformed/out-of-int64 IDs to catalog 422. | `DERIVED` | Map malformed/out-of-int64 path to 422; valid missing ID to 404. |
| Middleware/error | #74 registers shared dynamic route template and helper returns `data:null`. | `CURRENT_SOURCE` | Reuse existing middleware matching; do not add a duplicate path pattern. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete source trace in required precedence: AC-32 diagram/index → legacy and V1-PILOT Course DDL/ERD → API catalog/reusable Course/Page → #75 DD and #70/#73/#74/#14 source/tests.
2. Record the current discrepancy and this plan in the worklog before any source edit; preserve the prior dirty tree.
3. Add a declarative strict request body and success envelope in `admin/api_75_admin_course_update/models.py`; keep response type shared `CoursePage` and do not put runtime validators in models.
4. Add `query.py` SQL constants only: one `UPDATE ... RETURNING id` that changes only `name`, `description`, `thumbnail_url`, `price`, `updated_at`; one SELECT with the existing #74 Course/mentor projection.
5. Add `validate.py` for shared ADMIN guard, signed-int64 path mapping to catalog 422, strict decimal parsing/NUMERIC(12,2) boundary and field-level 422 errors. No URL-host, nonblank, nonnegative-price, status or ownership policy beyond the sources.
6. Implement `view.py`: authorize/validate before DB; execute bound update; return 404 on no returned row; validate returned identity; fetch/map Course projection; build singleton Page; commit only after all response mapping succeeds; safely rollback query/projection/commit failures and return catalog 500.
7. Wire PUT at `/admin/courses/{course_id}` in `app/api/v1.py` with explicit int64 path and Authorization OpenAPI metadata, strict body schema, and exact catalog 401/403/404/422/500 errors. Reuse current middleware route-template entry.
8. Add focused TestClient tests for full replacement/null semantics, exact decimal/limits, unchanged status/mentor, authentication, path/body errors, missing row, query/projection/commit failures, rollback, trace and OpenAPI.
9. Update API #75 DD while preserving its 8 template appendix suffixes and Draft status; state implemented fallbacks and still-open owner decisions. Correct stale #75–#77 macro-review claims about #74/shared auth/middleware/error data only where directly inaccurate.
10. Update server-study manifest/context/test counts and this worklog after implementation. Run focused #75 tests, linked #70/#73/#74 regression, full Study suite, Ruff, import/OpenAPI inspection, DD static checks, `git diff --check` and Deno context validator fallback; separate DB Admin baseline errors.
11. Review diff and report local-test/live-schema boundary. Do not stage or commit.

## CHANGES

- Files changed: API #75 route/module/focused HTTP tests; API #75 DD sheets/reports; server-study context manifest/pages; this worklog.
- CONTEXT_UPDATES: Added six API #75 source/test paths to the manifest (250 required Study paths; all exist); updated route/operation count to 42 templates / 46 operations and full-suite count to 872.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`, `.agents/context-manifest.json`.
- Assumptions: Implemented only the planned DERIVED fallback: strict full-replacement body; legacy BIGINT `courses` candidate; shared role `ADMIN`; decimal constraints based on checked-in `NUMERIC(12,2)`; singleton `Page<Course>`; status/mentor unchanged. No catalog, diagram, DDL, migration or live DB changes.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` | 69 available; selected API #74, this active API #75 plan, and API #34; read all three. | `VERIFIED_PREFLIGHT` |
| `.venv/bin/pytest -q tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py` | 27 passed; one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| `.venv/bin/pytest -q tests/modules/guest/api_06_courses tests/modules/guest/api_08_courses_detail tests/modules/admin/api_70_admin_user_update tests/modules/admin/api_73_admin_courses_list tests/modules/admin/api_74_admin_course_detail tests/modules/admin/api_75_admin_course_update` | 113 passed; one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| `.venv/bin/pytest -q` | 872 passed; one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| `.venv/bin/ruff check app/api/v1.py app/modules/admin/api_75_admin_course_update tests/modules/admin/api_75_admin_course_update` | All checks passed. | `VERIFIED_STATIC` |
| `.venv/bin/ruff check app tests` | All checks passed. | `VERIFIED_STATIC` |
| Import/OpenAPI | 42 `/api/v1` templates / 46 operations; same `/admin/courses/{course_id}` path exposes GET and PUT; PUT body/path/catalog errors verified in OpenAPI and HTTP tests. | `VERIFIED_LOCAL_SOURCE` |
| DD static checks | 11 Markdown files; 8 Draft sheets retain appendices; relative links and JSON examples parse. | `VERIFIED_STATIC` |
| `git diff --check` | No whitespace errors. | `VERIFIED_STATIC` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Fails only on missing DB Admin context/source roots and links outside Study scope; no API #75 source-path failure. | `BASELINE_FAIL_OUT_OF_SCOPE` |

## HANDOFF

- Remaining owner decisions: body/full-replacement semantics and field rules; dedicated course-management permission; live schema/deployment; category/counter/nullable/orphan policy; CourseStatus casing and soft-delete visibility.
- Next owner/action: API #76 in the next task/session; keep the existing worktree intact and preserve the DERIVED/Draft status.
