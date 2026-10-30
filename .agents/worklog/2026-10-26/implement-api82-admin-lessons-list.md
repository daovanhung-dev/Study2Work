---
task_id: "2026-10-26-implement-api82-admin-lessons-list"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-34 APIs #83–#86; public Lesson projection precedent API #09; Admin list precedent API #78"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #82 Admin lessons list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 75 coding worklogs available; selected #74, #75, #76; all three read; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN guard and raw int64 parsing exist; use current role-based auth; legacy BIGINT remains a candidate; preserve dirty worktree and distinguish derived choices.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` is SQL constants only; `view.py` owns orchestration; preserve read/write boundaries and current transaction conventions.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Keep shared ADMIN role as a limited fallback for finer AC-34 permission; use current helper and preserve Draft/live-schema boundaries.
  - path: `.agents/worklog/2026-10-24/create-study-api82-dd.md`
    - carry_forward: Preserve direct catalog fields and error set as source; clearly mark list cardinality, filter semantics and schema mapping as derived/source-required; don't invent a `type` column or pagination.
- related_current_artifacts_reviewed: AC-34 index and full diagram flow; API #82 DD package; AC-34 #83–#86 DD boundaries; API catalog #82 and reusable Lesson; legacy `lessons` DDL, table guide and ERD; V1-PILOT UUID Lesson DDL; API #09 Lesson model/query/view/tests; API #78 Admin list module/tests; current Admin auth, middleware, response helper, route and OpenAPI composition.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-34 APIs #83–#86; API #09 reusable Lesson mapping; API #78 Admin list/auth/filter precedent]
```

## EXPECTED_BEHAVIOR

- AC-34 diagram: Admin with lesson-management permission opens the lesson list, queries lessons, selects detail/update/status/delete, then reloads the list. #82 is read-only.
- Catalog #82 direct contract: `GET /api/v1/admin/lessons`; Bearer JWT/Admin; optional `course:int64`, `status:string`, `type:string`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; response `ApiEnvelope<Lesson>`; exact direct errors 401/403/500.
- Reusable Lesson has seven fields: `id`, `course_id`, `title`, optional `content`, optional `video_url`, `order`, `status`. No `type` field or pagination input is declared.
- API #82 DD is `Draft — Needs Confirmation` and records response-cardinality and `type`-schema discrepancies. This task implements a documented DERIVED fallback while retaining Draft and owner questions.

## CURRENT_BEHAVIOR (PRE-CODE)

- OpenAPI imports successfully and exposes 47 unique `/api/v1` paths / 52 operations. `/api/v1/admin/lessons` and all Admin lesson routes are absent.
- No API #82 module or focused test directory exists. Middleware `DESIGN_CONTRACT_PATHS` has no `/api/v1/admin/lessons` entry.
- Current source has `validate_current_user_request(..., role="ADMIN")`; AC-34's finer lesson-management permission is not represented by a separate policy.
- `app/core/responses.py` emits error `data:null`; middleware maps request validation on registered DESIGN paths to 422 `DESIGN_VALIDATION_ERROR`.
- API #09 exposes a reusable `Lesson` model and SQL aliases `name -> title`, `sort_order -> order`, but its `PUBLISHED` predicate is public-curriculum behavior. API #78 demonstrates raw query forwarding, auth before query validation and a read-only Admin list.
- AC-34 only describes querying lessons. Legacy BIGINT DDL has `id`, nullable `course_id`, `name`, nullable `content`, nullable `video_url`, nullable/defaulted `sort_order`, nullable/defaulted `status`, and timestamps; it has no `type`. The table guide describes `course_id` as required, which conflicts with current `DB.sql`. V1-PILOT lessons use UUID/course-version fields and no compatible legacy `type` or `status`; live schema is unverified.
- Worktree is extensively modified/untracked across Study API code, tests, DDs, diagrams, DDL and context. Preserve all current changes; do not stage, commit or clean.

## SOURCE_TRACE

```text
GET /api/v1/admin/lessons
  -> thin raw Request/header/query route -> API #82 view
  -> shared Bearer/JWT guard requiring role ADMIN -> signed-int64 `course` parse
  -> reject supplied `type` explicitly until a compatible Lesson type source exists
  -> one bound SELECT from legacy BIGINT `lessons` candidate using optional exact course/status predicates
  -> stable `course_id, sort_order, id` ordering; no PUBLISHED filter, pagination, count, join or write
  -> map rows through reusable API #09 Lesson model; malformed required projection -> safe 500 + rollback
  -> 200 DESIGN_RESOURCE_RETRIEVED with direct Lesson[] data (DERIVED list fallback), including [] when empty
  -> TestClient auth/query/filter/mapping/read-only/OpenAPI and AC-34 linked-route regression checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| List response shape | AC-34/API name say query/list; catalog declares `ApiEnvelope<Lesson>`. | `DISCREPANCY / DERIVED` | Return `ApiEnvelope<Lesson[]>` for the list operation; no `Page` because catalog has no page inputs. Keep DD Draft and do not alter catalog. |
| `type` filter | Catalog declares string query; reusable Lesson, legacy `lessons`, and V1-PILOT lesson model have no compatible type field. | `SOURCE_REQUIRED / DERIVED INTEGRATION FALLBACK` | Preserve parameter in OpenAPI; if supplied, return explicit 422 `DESIGN_VALIDATION_ERROR` before DB instead of silently ignoring or inventing a join/column. |
| Invalid `course` | Catalog says int64 but omits 422; current Study middleware uses 422 `DESIGN_VALIDATION_ERROR` for input validation. | `DIRECT TYPE / DERIVED ERROR` | Parse raw text as signed int64 after ADMIN auth; malformed/out-of-range returns 422 with field error, documented as an additional derived status. |
| Filter semantics | Catalog gives names/types only; legacy DDL has `course_id` and `status`. | `DERIVED` | Exact equality for supplied course/status; omit each predicate when absent; don't add status whitelist or public `PUBLISHED` predicate. |
| Schema choice | Contract is int64; legacy DDL is BIGINT with mostly reusable fields; V1-PILOT is UUID/versioned and incompatible. | `DERIVED / NOT_VERIFIED_HERE` | Query only the checked-in legacy candidate; no schema change and no live-schema claim. |
| Nullable required fields | `DB.sql` permits null `course_id`, `sort_order`, `status`; Lesson contract requires int64/int32/status. Table guide differs on `course_id`. | `DISCREPANCY / DERIVED ERROR` | Fail the full response with safe 500 on malformed required projection rather than silently dropping rows or inventing defaults; preserve nullable optional content/video as null. |
| Admin permission | Catalog role Admin and AC-34 lesson-management permission; current helper enforces only role `ADMIN`. | `DIRECT ROLE / SOURCE_REQUIRED FINER POLICY` | Use shared ADMIN guard before parsing/query; don't claim a separate lesson-management permission. |
| Pagination/result size | No page/size/limit/order parameters in catalog; AC-34 only says query list. | `SOURCE_REQUIRED` | Return all matching rows with stable derived ordering; add no pagination. Keep maximum-result/performance decision open. |
| Deleted lesson visibility | Legacy schema has no compatible delete marker; #86 policy remains open. | `SOURCE_REQUIRED` | Add no deleted filter or marker. |
| Error envelope | API guideline and current helper use `data:null`; old DD says `{}`. | `CURRENT SOURCE OVERRIDES STALE DD` | Use `error_response` and update DD to current `data:null`; no custom error envelope. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Preserve the dirty worktree. Apply conflict order and record evidence: AC-34 diagram/index → current legacy/V1-PILOT DDL plus DB table guide/ERD → API catalog row #82/reusable Lesson. Keep source, runnable test and design evidence distinct.
2. Add `admin/api_82_admin_lessons_list/models.py` with a typed raw-normalized query model and success envelope containing `list[Lesson]`; reuse API #09 Lesson without changing public behavior. Keep model file declarative.
3. Add `query.py` with one SQL-only SELECT constant using known legacy columns, optional bound `course_id`/`status` predicates and stable `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`; no `type`, count, pagination, joins, PUBLISHED predicate or mutation.
4. Add `validate.py` for role-aware shared ADMIN auth and signed-int64 `course` parsing. Explicitly reject supplied `type` with a field-level 422 DESIGN error because no compatible source exists; no extra constraints on `status` or positive course IDs.
5. Add `view.py`: authenticate before query validation; perform one `query_many`; map list rows through API #09 `Lesson`; return 500 and safely rollback query/projection errors; return direct list data and empty `[]` without commit on success.
6. Wire GET `/admin/lessons` in `app/api/v1.py` using raw query values; declare Authorization plus `course:int64`, `status:string`, `type:string`; list 422 as DERIVED alongside exact direct 401/403/500. Add fixed path to middleware DESIGN set so framework/unhandled errors use canonical envelope.
7. Add focused TestClient tests: auth before validation/query; ADMIN vs non-ADMIN; course signed-int64 bounds; exact course/status predicates and no PUBLISHED; explicit unsupported-type 422 with no DB call; Lesson aliases/optional nulls; `[]` empty result; required projection failure; safe query errors/rollback; success no-commit; trace, error envelope, OpenAPI, and #09/#78/#83–#86 route boundary.
8. Update API #82 DD with actual local behavior and DERIVED choices, retaining 11-file package, Draft status and exact eight template appendix suffixes. Preserve direct catalog contract as a documented discrepancy; update stale Admin-guard, route, middleware and error-data statements.
9. Macro-review AC-34 #82–#86 boundaries and API #09/#78 behavior; update only directly affected API #86 macro-review note if it still describes #82 as unwired. Keep #83–#86 future behavior and unresolved deletion policy separate.
10. Update Study Server route/architecture/runtime/database/module/test/workflow context, global source-status and context manifest with current route/module/test evidence and recounted OpenAPI/test totals. No database/diagram/catalog edits planned.
11. Verify focused API #82 TestClient suite, linked #09/#78/#82 AC-34 regression, full Study suite, scoped Ruff, OpenAPI import/schema, DD links/JSON/tables/fences/template appendix parity, `git diff --check` and `node scripts/validate-agent-context.mjs` (use Deno fallback only if Node unavailable); separate the known DB Admin checkout baseline.
12. Review exact scoped diff and status, preserve all unrelated existing changes, and do not stage or commit.

## PRE-CODE CHECKPOINT

- Read root router, global context router, context map, worklog contract, Study Server entry/index and workflow/module context.
- Ran the exact `coding` worklog selector and read all three selected logs; also read the prior API #82 DD-authoring worklog.
- Read API #82 DD package and AC-34 diagram/index before schema; inspected legacy/V1-PILOT lesson DDL, table guide and ERD before rechecking catalog #82.
- Traced API #09 Lesson projection, API #78 Admin list, current Admin auth, middleware validation mapping, response helper, route composition and OpenAPI; confirmed API #82 route/module/tests are absent and current OpenAPI is 47 paths / 52 operations.
- The detailed implementation plan and derived conflict decisions above are recorded before runtime, test, DD or context edits.

## CHANGES

- Runtime files: added `app/modules/admin/api_82_admin_lessons_list/{__init__.py,models.py,query.py,validate.py,view.py}`, registered `GET /api/v1/admin/lessons` in `app/api/v1.py`, and added the path to middleware `DESIGN_CONTRACT_PATHS`.
- Tests: added `tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py` with 15 HTTP/API tests covering auth order, filters, int64 parsing, unsupported type, projection, errors, read-only behavior and OpenAPI.
- DD files: synchronized all eight template sheets plus `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`. Kept Draft status and direct catalog/cardinality discrepancy; preserved all eight template appendix suffixes byte-for-byte.
- AC-34 related report: updated API #86 macro-review to say API #82 is wired locally while #83–#86 remain unwired; retained unresolved deletion visibility.
- Context pages: updated `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`, and `.agents/context-manifest.json`.
- No catalog, diagram, DDL, migration, deployment, staging, or commit change was made.
- Assumptions: local `Lesson[]` is the DERIVED list fallback; exact equality is used for supplied `course`/`status`; unsupported `type` gets explicit 422; all matching rows are returned without pagination; legacy BIGINT schema remains a candidate only.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `.venv/bin/pytest -q tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py` | 15 passed, one upstream Starlette/httpx deprecation warning | PASS |
| `.venv/bin/pytest -q tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py tests/modules/admin/api_78_admin_content_pending/test_admin_content_pending.py tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py` | 47 passed, same upstream warning | PASS |
| `.venv/bin/pytest -q` | 1012 passed, one upstream warning | PASS |
| `.venv/bin/ruff check app/api/v1.py app/core/middleware.py app/modules/admin/api_82_admin_lessons_list tests/modules/admin/api_82_admin_lessons_list` | All checks passed | PASS |
| OpenAPI import/inspection | 48 `/api/v1` paths, 53 operations; #82 exposes Authorization + three query parameters and 200/401/403/422/500 | PASS |
| DD static check | 11 Markdown files; 3 valid JSON examples; 30 tables / 375 data rows; 7 balanced fence pairs; 33 local file links; 8/8 appendix suffixes byte-identical; no trailing whitespace | PASS |
| `deno run --allow-read --allow-run=git --allow-env scripts/validate-agent-context.mjs --skip-drift` | Exits 1 for existing DB Admin missing entry/pages/source roots and broken links; no Study Server/API #82 missing-path finding | BASELINE_FAILURE |
| Full context validator | Same DB Admin baseline plus `CONTEXT_STALE` across currently dirty tracked scopes; shared worktree contains broad uncommitted changes and manifest remains anchored to its prior source commit | BASELINE_FAILURE |
| `git diff --check` | Clean after code, DD, context and worklog edits | PASS |

## HANDOFF

- API #82 is locally wired and HTTP-tested. The catalog response remains a singleton while the implementation returns a collection; the Draft DD records that discrepancy. Fake DB tests do not prove live schema/deployment or the fine-grained AC-34 permission.
- Context validation reports the existing DB Admin gaps and source drift across the shared dirty worktree; no API #82 path is missing and all six new implementation/test paths are registered in the manifest.
- Next API in sequence: #83.
