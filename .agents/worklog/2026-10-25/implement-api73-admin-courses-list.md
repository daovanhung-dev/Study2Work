---
task_id: "2026-10-25-implement-api73-admin-courses-list"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #73 Admin course list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 66 coding worklogs available; selected/read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve dirty worktree changes; query.py is SQL-only; views own transaction; fake DB and local migrations do not prove live DB/storage.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Use current source and the reusable course projection; keep legacy BIGINT separate from V1-PILOT UUID; record every fallback.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: AC-32 and schema gaps must be explicit; detail/list authorization and response contracts remain separate; preserve existing changes.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Direct contract: `GET /api/v1/admin/courses`; Bearer JWT role Admin; optional query `status:string`, `mentor:int64`, `category:int64`, `page:int32`; `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; exact errors 401/403/422/500 and corresponding `DESIGN_*` codes.
- AC-32 diagram: Admin course-management precondition; query course list, then continue to #74 detail and #75/#76/#77 actions/reload.
- API #73 DD remains Draft and proposes exact status/mentor/category filters, page 1 default, fixed size 20, `courses.id ASC`, all-status default, empty-page 200, Course mapping with UserSummary, and no writes.

## INITIAL_CURRENT_BEHAVIOR (pre-edit)

- Worktree: 398 modified/untracked entries before API #73 task edits. Preserve all existing changes outside API #73 runtime/tests, its DD/context/worklog, and directly necessary AC-32 report synchronization.
- Runtime at task start: no API #73 route/module/focused test existed; Admin APIs #68–#72 used shared `ADMIN` guard. `DESIGN_CONTRACT_PATHS` lacked `/api/v1/admin/courses`.
- Diagram → infra → catalog review: AC-32 lists status/mentor/category/page and query-courses flow. Legacy and V1-PILOT DDL/ERD have no course-category relation; legacy target is BIGINT `courses/users`, pilot courses are UUID/versioned. Catalog directly requires category and `Page<Course>`.
- API #06 source: public course list filters only `PUBLISHED`, uses shared Course mapping and exact decimal-string price, detects required mentor integrity, and rejects category with 422 because no relation exists. API #68 pattern: role `ADMIN` before raw query parsing/DB, exact filters, page default 1/fixed size 20, `id ASC`, count/page queries and fake-session HTTP tests.
- Error helper currently emits `data:null`; older API #73 DD text saying `{}` is stale. Current error middleware uses exact/route-template membership and lacks the #73 contract path.
- AC-32 linked DD review: #74–#77 remain source-unwired and have open wrapper/counter, body, status/audit, visibility/dependency and schema questions. API #73 must not implement those operations or invent counters.

## SOURCE_TRACE

```text
GET /api/v1/admin/courses -> shared ADMIN JWT guard -> parse raw optional query values -> reject supplied category with 422 because no physical relation exists (same established API #06 fallback) -> COUNT + page SELECT using identical status/mentor predicates -> map shared Course/Page -> read-only envelope -> focused tests/OpenAPI
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Implementation impact |
|---|---|---|---|
| Category filter | Direct catalog/diagram declare category; legacy DDL, ERD and V1-PILOT have no course-category relation; API #06 already returns 422 for category. | `DISCREPANCY / DERIVED_FALLBACK` | Reuse API #06's explicit 422 `DESIGN_VALIDATION_ERROR` before DB access. Do not silently ignore filter or invent schema/JOIN. Update DD #73 while retaining Draft. |
| Admin permission | AC-32/catalog require Admin; APIs #68–#72 use shared `ADMIN` claim; no dedicated course-management permission/tenant source. | `DERIVED` | Reuse shared ADMIN guard before parsing/query; do not claim a dedicated permission check. |
| Pagination/order | Catalog has `page` but no `size`/sort; Page requires size. API #06/#68 use default page 1, fixed 20; #68 uses id ascending. | `DERIVED` | Use page 1, fixed size 20, `id ASC`; validate positive int32 and do not add size/sort inputs. |
| Course status | Legacy DDL/API #06 have DRAFT/PUBLISHED; #76 catalog describes draft/published/suspended; reusable runtime Course status is string. | `SOURCE_REQUIRED` | Exact-match any supplied string; without status filter return all source statuses; do not whitelist or default PUBLISHED. |
| Course/category schema | Legacy BIGINT and V1-PILOT UUID/versioned courses differ; neither defines category relation; live schema is not verified. | `NOT_VERIFIED` | Query only legacy BIGINT candidate; no migration/schema edits. |
| Required mentor/price | Course contract requires mentor and decimal price; legacy mentor_id/price may be NULL. API #06 maps incomplete mentor/price as safe 500. | `DERIVED` | LEFT JOIN to detect missing mentor; map rows via shared mapper; safe 500 on integrity/mapping failure. |
| Empty/out-of-range page | Catalog has no 404; API #06 returns empty page 200 and #68 returns zero-result page. | `DERIVED` | Return 200 with `items=[]`, preserve total metadata. |
| Error envelope | Current `error_response` defaults to `data:null`, unlike older #73 DD text. | `CURRENT_SOURCE` | Use shared helper; do not add custom envelope. |

## IMPLEMENTATION_PLAN

1. Freeze source precedence in this worklog before runtime edits: AC-32 diagram → legacy/V1-PILOT DDL and ERD → API catalog; trace all 11 API #73 DD files, #74–#77 related DDs, API #06 course list/mapping/tests, API #68 Admin list/auth/tests, middleware, response helper, fixtures and context pages.
2. Add API-local declarative models for raw-normalized query values, Page<Course> response and envelope, reusing the existing Course/CoursePage mapping where it preserves the catalog shape. Keep models free of business validation.
3. Add `validate.py`: invoke shared ADMIN guard before raw query parsing; parse page as signed int32 and mentor/category as signed int64; exact-match status; return 422 for invalid values. If valid `category` is supplied, return the established API #06 422 unsupported-category response before DB access because no physical relation is source-backed.
4. Add `query.py` constants only: one count query and one page query over legacy `courses LEFT JOIN users`; bind the same optional status/mentor predicates in both; expose missing-mentor count; order `c.id ASC`; bind `LIMIT 20` and computed offset. Do not add a category JOIN, status whitelist, counters, or schema.
5. Add `view.py`: guard/validate, execute count then page using shared predicates, validate count/rows, fail safely on orphan mentor or invalid Course/price projection using the shared decimal-string mapper, construct PageMeta (page, size 20, total, total_pages), rollback query/mapping failure, never commit, and return standard 200 envelope including empty pages.
6. Wire `GET /admin/courses` in `app/api/v1.py` with raw query/header values, no body, response model and exactly 200/401/403/422/500. Add the exact route to `DESIGN_CONTRACT_PATHS` so framework validation/unhandled errors map to design codes.
7. Add focused HTTP tests for default and exact filters, stable order/limit/offset bindings, empty/out-of-range page, category 422 before DB, invalid/overflow int32/int64, auth-before-query, safe DB/count/row mapping failures, no commit/read-only behavior, trace/envelope and OpenAPI. Run API #73 focused suite, linked #06/#68 regression, full Study suite and Ruff.
8. Update API #73 DD sheets/reports and open questions with the category discrepancy/fallback, source-backed error behavior and local verification; macro-review #74–#77 current-state reports without broadening their runtime scope.
9. Update server-study route/runtime/security/database/architecture/module/test/workflow pages, project source status, manifest with API #73 paths, and this worklog. Recount actual OpenAPI paths/operations and tests from the current tree.
10. Validate DD examples, links/anchors, tables/fences/whitespace and appendix suffix preservation; run `git diff --check` and context validator, separating known DB Admin/snapshot drift from Study findings.

## PRE-CODE CHECKPOINT

Read root/router/context-map, server-study scope/index and task pages, selected coding worklogs, all API #73 DD sheets/reports, AC-32 diagram, legacy/V1-PILOT schema and ERD, API catalog, linked #74–#77 DD summaries, API #06/#68 source/tests, response/parser/auth/middleware helpers and test fixtures. At checkpoint no API #73 source/test edits had been made. Category remained a direct-contract gap; the planned 422 fallback was explicitly DERIVED from existing API #06 behavior.

## CHANGES

- Runtime added: `apps/study-server/app/modules/admin/api_73_admin_courses_list/{__init__,models,query,validate,view}.py`; route wired in `app/api/v1.py`; middleware path added in `app/core/middleware.py`; focused HTTP/OpenAPI tests in `tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py`.
- DD updated: API #73 sheets/reports and open questions; stale AC-32 macro-review notes in #74–#77 updated for the local #73 route/guard/error helper state.
- CONTEXT_UPDATES: Study Server route, runtime, security, database, architecture, modules, tests, workflow, source-status and context manifest updated with API #73 behavior and current verification.
- Assumptions: category 422 fallback, ADMIN role mapping, page 1/size 20/id ascending, exact status/mentor filters and all-status default are DERIVED; none is presented as owner-approved policy. Live schema/deployment remain unverified.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Context/worklog preflight | Read root router/context-map, server-study pages and all three selected coding worklogs; selector found 66 coding logs and selected 3. | `VERIFIED_PREFLIGHT` |
| Diagram → infra → catalog | AC-32 diagram, ERD/legacy/pilot DDL and API #73 catalog/reusable schemas reviewed in requested order. | `VERIFIED_SOURCE_REVIEW` |
| Related API/DD review | API #06/#68 source/tests and #74–#77 AC-32 DD boundaries reviewed. | `VERIFIED_SOURCE_REVIEW` |
| Focused API #73 tests | `.venv/bin/python -m pytest tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py -q` → 24 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL` |
| Linked regression | API #06 + #68 + #73 focused suites → 60 passed, one upstream warning. | `VERIFIED_LOCAL` |
| Full Study suite | `.venv/bin/python -m pytest -q` → 830 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL` |
| Ruff | `.venv/bin/ruff check app tests` → all checks passed. | `VERIFIED_LOCAL` |
| OpenAPI | App introspection → API #73 present; 41 unique `/api/v1` paths and 44 operations. | `VERIFIED_LOCAL` |
| Diff hygiene | `git diff --check` → clean. | `VERIFIED_LOCAL` |
| DD static checks | 11-file package verified; 4 JSON examples and 34 tables pass; 36 local links/anchors, fences, whitespace and final newlines pass; all 8 sheet appendix suffixes byte-match registered templates; output digest recorded in DD report. | `VERIFIED_LOCAL` |
| Context validator | Required `node scripts/validate-agent-context.mjs` could not start (`node` unavailable). Deno fallback reports missing DB Admin scope files and unavailable registered source commit; `--skip-drift` still reports only missing/out-of-scope DB Admin context/source paths. No Study API #73 path error reported. | `FAILED_BASELINE_OUT_OF_SCOPE` |
| Final lint/diff/manifest | Ruff whole Study app/tests passes; `git diff --check` clean; context manifest parses as JSON. | `VERIFIED_LOCAL` |

## HANDOFF

- Remaining boundaries: owner-approved category relation/behavior, dedicated Admin permission/scope, complete CourseStatus enum, orphan-course recovery policy, live schema and deployment remain unverified.
- Next task in the one-API-per-session sequence: API #74.
