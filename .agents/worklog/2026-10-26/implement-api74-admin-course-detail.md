---
task_id: "2026-10-26-implement-api74-admin-course-detail"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement Study Server API #74 Admin course detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 67 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve the dirty worktree; query.py contains SQL constants only; views own DB orchestration; checked-in migrations and fake DB tests do not prove live schema.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Keep legacy BIGINT separate from V1-PILOT UUID schema; use role-aware shared auth and parameterized SQL; explicitly label derived behavior.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Reuse Course/asset projection where appropriate; read linked API/DD evidence before coding; preserve all existing worktree changes and report live-schema limits.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Implement `GET /api/v1/admin/courses/{course_id}` for AC-32 from API #74 DD. Require Bearer JWT/Admin role; return `ApiEnvelope<Page<Course>>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; supported errors 401/403/404/500 with catalog codes.
- Source order required by the user objective: AC-32 activity diagram → infra/schema → `docs/lists/list_api.md`; then use the simplest clear fallback where sources remain unresolved.
- API #74 DD is Draft. It proposes a one-item `Page<Course>`, all-status Admin visibility, legacy course/mentor projection, optional category omitted without a relation, and no counters until their contract is defined.

## CURRENT_BEHAVIOR (pre-edit)

- Source/config: API #74 route/module/test are absent. API #73 wires `GET /api/v1/admin/courses`; middleware `DESIGN_CONTRACT_PATHS` does not yet contain the parameterized #74 route. Shared auth accepts explicit `ADMIN` role. API #69 demonstrates raw signed-int64 path parsing after auth and catalog 404 on invalid path.
- Schema evidence: `infra/postgres/study-server/DB.sql` has legacy BIGINT `courses`/`users`, with nullable `mentor_id`, `description`, `thumbnail_url`, `price` and `status`; the V1-PILOT course model uses UUID identity and versioned `course_versions`. Neither artifact verifies the live DB. The legacy ERD/table guide has no course-category relation.
- Related behavior: API #73 uses the shared `map_course` decimal-string projection and returns 500 for missing mentor integrity; API #08 returns a singleton `CoursePage`, but filters `PUBLISHED` for public reads; Admin APIs #68–#73 use role `ADMIN` before DB access.
- Contract gaps: AC-32 says “course + owner + counters” without defining counters or response fields. Catalog #74 directly requires `Page<Course>` and only errors 401/403/404/500. Dedicated course-management permission, live schema, category, status enum and orphan-course recovery remain unresolved.
- Worktree: `develop` has extensive modified and untracked Study Server/context/DD/schema files. All pre-existing changes are out of scope for cleanup and must be preserved.

## SOURCE_TRACE

```text
GET /api/v1/admin/courses/{course_id}
  -> shared ADMIN Bearer/JWT guard
  -> parse raw path as signed int64 (invalid/out-of-range -> catalog 404)
  -> one parameterized read of legacy candidate courses LEFT JOIN users, by course ID and without a status filter
  -> map through shared Course decimal-string mapper
  -> singleton Page<Course> envelope; no writes or commit
  -> TestClient/OpenAPI checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-32 counters | Diagram requests course + owner + counters; catalog/reusable `Course` defines no counter fields or meanings. | `SOURCE_REQUIRED / DERIVED_FALLBACK` | Do not invent counter fields or queries; retain the discrepancy in DD and Open Questions. |
| Admin permission | Diagram/catalog require Admin with course-management permission; current source has shared role `ADMIN` but no dedicated permission policy. | `DERIVED` | Enforce shared `ADMIN` role before parsing/DB access; do not claim a separate course-management permission check. |
| Response cardinality | Catalog declares `ApiEnvelope<Page<Course>>` for an ID detail route; no page inputs. | `DERIVED` | Return one item with page metadata 1/1/1/1, following API #08 and the existing DD proposal. |
| Schema selection | API contract uses int64; legacy course/user candidate uses BIGINT; V1-PILOT uses UUID and versioned course records. | `DERIVED / NOT_VERIFIED_HERE` | Query only the checked-in legacy candidate; do not alter schema or claim live availability. |
| Category | `Course.category` is optional but no course-category relation is source-backed. | `SOURCE_REQUIRED` | Omit the optional category field; add no join. |
| Status visibility | Admin AC-32 follows all-status course management; API #08's PUBLISHED predicate is public-specific. | `DERIVED` | Do not filter status; return stored status string without inventing enum members. |
| Path error mapping | #74 catalog omits 422; #69 Admin detail uses signed-int64 raw parser and 404; API #08 also maps invalid detail IDs to 404. | `DERIVED` | Map malformed/out-of-range signed-int64 path to 404. |
| Required mentor/price | Reusable Course requires mentor and price; legacy DDL allows nullable mentor_id/price; shared mapper rejects missing values. | `DERIVED` | Map incomplete required projection to safe 500; keep the orphan recovery question open. |
| Error envelope | API #74 DD says helper emits `{}`; current shared error helper emits `data:null`. | `DISCREPANCY` | Follow current runtime helper and update DD wording. |

## IMPLEMENTATION_PLAN

1. Complete source precedence review: inspect the AC-32 node/edges and ERD/table guide; compare legacy BIGINT and V1-PILOT UUID course schemas; read the exact API #74 catalog/reusable schema; review #73 course list, #69 Admin detail, #08 public detail, shared mapper/auth/middleware/response helpers, and linked #75–#77 DD boundaries.
2. Add the module-local declarative response envelope, SQL-only `FIND_ADMIN_COURSE_DETAIL` constant and validation helpers for shared ADMIN auth plus raw signed-int64 parsing. Do not add a migration, category relation, counters or status allowlist.
3. Implement the read-only view: authorize before path parsing; return 404 for malformed/out-of-range path or absent course; query one legacy candidate row by bound ID without a publication predicate; map through shared `map_course`; return safe 500 for DB/projection failures with rollback; return `Page<Course>` singleton on success without commit.
4. Wire the raw path route in `app/api/v1.py` with an explicit OpenAPI int64 path parameter and exactly the catalog 401/403/404/500 responses. Add the parameterized path template to `DESIGN_CONTRACT_PATHS`.
5. Add focused TestClient coverage for auth ordering/roles, signed-int64 boundary and not-found behavior, all-status/nullable/decimal mapping, no category/counters, projection and DB failures, rollback/no-commit, envelope/trace and OpenAPI.
6. Update the API #74 DD while preserving its registered template appendix and Draft status; record each implementation fallback and unresolved owner decision. Review #75–#77 references and make only directly stale AC-32 status notes current.
7. Update `.agents/context-manifest.json`, relevant `server-study` pages, project source status and this worklog with the new route/module/test evidence.
8. Run focused API #74 tests, linked #08/#69/#73 regressions, full Study Server suite, Ruff, import/OpenAPI inspection, DD static checks, `git diff --check` and `node scripts/validate-agent-context.mjs` (using the documented available fallback if Node cannot start). Separate repository-baseline validator issues from API #74 results.
9. Review the final diff against this scope, preserve unrelated worktree entries and report that local tests do not prove live DB schema, migration, authorization policy or deployment.

## PRE-CODE CHECKPOINT

- Read root router, global context map, full server-study entry/index and relevant scope pages; selector worklogs were read above.
- Read API #74 DD, AC-32 diagram and linked #75–#77 boundaries; inspected legacy/V1-PILOT course schema and API catalog in the required conflict order.
- Traced current API #73, #69 and #08 route/view/query/model/test conventions plus shared Course mapper, auth guard, middleware and error helper.
- The implementation plan was recorded before code edits. API #74 route/module/test, DD and context updates followed that checkpoint; no migration/catalog/diagram changes were made.

## CHANGES

- Files changed: API #74 route/module/test; DD #74; stale AC-32 #75–#77 integration notes; server-study context/manifest; project source status; this worklog.
- CONTEXT_UPDATES: Added API #74 source/test paths and ownership/runtime/database/security/test notes; updated current API count to 42 templates/45 operations and full Study test count to 845.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`, `.agents/context-manifest.json`.
- Assumptions: Shared `ADMIN` role is the local fallback for the catalog's Admin requirement; no dedicated course-management permission was invented. Legacy schema candidate and singleton Page behavior remain `DERIVED` and unverified live.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Worklog preflight | Selector found 67 coding logs; selected and read the three listed above. | `VERIFIED_PREFLIGHT` |
| API #74 focused tests | `.venv/bin/pytest -q tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py`: 15 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| Linked regression | #06/#08/#69/#73/#74 focused set: 80 passed, one upstream deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| Full Study suite | `.venv/bin/pytest -q`: 845 passed, one upstream deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| Ruff | `.venv/bin/ruff check app tests`: all checks passed. | `VERIFIED_STATIC` |
| API route/OpenAPI | GET #74 present; signed-int64 path and catalog error set verified by tests; OpenAPI count 42 paths / 45 operations. | `VERIFIED_LOCAL_SOURCE` |
| Context validator | Deno fallback with `--skip-drift` reports repo-wide missing DB Admin context/source roots and broken DB Admin links; no Study API #74 path failure identified. | `BASELINE_FAIL_OUT_OF_SCOPE` |
| DD/template/static and diff checks | All 8 template appendix suffixes match HEAD byte-for-byte; JSON fences parse; `git diff --check` passes. | `VERIFIED_STATIC` |

## HANDOFF

- Remaining owner decisions: live schema/deployment, dedicated Admin course-management permission, counter definitions, category relation, CourseStatus casing and orphan/null projection behavior.
- Next owner/action: API #75 in a separate task/session; preserve this dirty worktree and the existing draft status.
