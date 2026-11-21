# Worklog — API #97 Admin reported discussions

## Task classification

```text
primary_task_type: coding
secondary_task_types:
  - test
  - docs
project_scopes:
  - server-study
cross_scope_dependencies:
  - AC-37 Admin discussion queue/detail/moderation/delete (#97–#100)
```

## Goal and scope

Implement `GET /api/v1/admin/discussions/reported` from the current Study API
catalog and AC-37 diagram, then review linked APIs #98–#100 and run focused,
linked and full Study checks. Keep this change within `apps/study-server/` and
the canonical Study Server context/worklog. Do not stage or commit. Preserve
all pre-existing worktree changes.

## Prior worklog review

Preflight used `deno run --allow-read --allow-env scripts/select-worklogs.mjs
--type coding --limit 3`. Selector status was `READY`; 90 coding worklogs were
available and no shortage was reported. Read all selected files:

- `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
- `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
- `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`

Carry-forward: preserve the dirty worktree; keep `query.py` SQL-only and
`view.py` as DB orchestration owner; use the shared explicit `ADMIN` JWT guard;
fake DB/HTTP tests do not prove deployed schema or live database behavior.

## Source and contract findings

### Direct contract

- Catalog #97: `GET /api/v1/admin/discussions/reported`.
- Bearer JWT, role Admin.
- Query: optional `reason:string`, `severity:string`, `page:int32`.
- HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Discussion>>`.
- Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`,
  500 `DESIGN_INTERNAL_ERROR`.
- AC-37 diagram: Admin opens a reported discussion queue, reads reports plus a
  discussion summary, and can open #98 detail before #99 moderation or #100
  deletion. #97 is read-only.

### Current source and schema

- #97 has no route, module or test in the current Study source; middleware's
  design-error path allowlist also omits this route.
- Study legacy DDL has `discussions(id BIGSERIAL, course_id, user_id, parent_id,
  content, status, created_at, updated_at)`; it has no title, report relation,
  report key, reason or severity. The checked-in DDL is not live-schema proof.
- V1-PILOT Study `report_snapshots` is for AC-38 analytics, not discussion
  reports.
- Work DB `moderation_reports` has a generic UUID `resource_id`; Study
  discussion IDs are BIGSERIAL. Project DB context confirms three physical DBs
  with no cross-database FK; Study's runtime connection is scoped to Study DB.
  Work's current runtime Prisma schema has no `moderation_reports` model or
  migration. That table appears only in the V1-PILOT Work DDL, so it is not a
  verified runtime source or usable join source for this Study endpoint.
- Catalog `Discussion` requires `title`, `course_id`, `author` and
  `comments[]`; the legacy Study schema cannot safely populate `title` and
  does not settle null-relation or queue-comment policy.
- DD #97 is `Draft — Needs Confirmation`; `OPEN_QUESTIONS.md` records report
  persistence/grain, response report data, filter meaning, pagination, title,
  comment projection, Admin auth, and error integration as unresolved.

## Discrepancies / selected fallback

`DISCREPANCY`: AC-37 requires a report-backed queue, but neither the Study
schema nor the catalog defines a physical report source or join key. The only
nearby generic report relation belongs to Work DB and uses an incompatible UUID
resource key; it is not usable from Study. The user directed us to select the
most reasonable fallback.

### Selected `DERIVED` fallback

- Keep reports in Study DB and add a legacy BIGINT `discussion_reports` table
  linked by `discussion_id` to `discussions.id`; do not cross-query Work DB.
- Store `reporter_user_id`, free-form `reason_code`, free-form `severity`,
  `status`, and `created_at` so the list can filter and order report-backed
  discussions. No value taxonomy or reporter identity mapping beyond the
  legacy `users.id` FK is claimed as approved.
- Queue grain is one unique Discussion with at least one `OPEN` or `IN_REVIEW`
  report. `reason` and `severity` are exact-match AND filters on the same active
  report. Sort by latest matching active report time descending, then
  `discussion_id` descending.
- Pagination defaults to page 1 and fixed size 20; empty total has
  `total_pages=0`. Invalid/non-positive/out-of-int32 page returns 422
  `DESIGN_VALIDATION_ERROR` as a documented local fallback.
- Derive the required `Discussion.title` from normalized `content`, clipped to
  120 characters. Return `comments=[]` in this queue summary; #98 owns full
  thread detail. These transformations are explicit `DERIVED` behavior because
  the legacy Discussion table has no title and AC-37 calls this a summary.
- A new report-ingest endpoint is outside #97. This table is a local schema
  candidate and does not prove deployed schema or report ingestion.

## Detailed plan

1. [x] Load root router, Study scope instructions/context map, coding worklog
   preflight, scope index/workflow, #97–#100 contracts, current middleware/auth,
   and the exact schema candidates.
2. [x] Trace candidate report sources and verify ID compatibility; review the
   Study `discussions` legacy relation and the Work generic report relation.
3. [x] Confirm #97 import/route/test is absent and keep #98–#100 outside this
   endpoint's mutation scope.
4. [x] Resolve missing physical mapping using the user's delegated fallback:
   Study-local BIGINT `discussion_reports`, unique Discussion queue grain,
   exact reason/severity filters, page 1/20, title snippet and empty comments.
   Label these implementation choices `DERIVED` in DD/context.
5. [x] Implement the local fallback in these exact files: add
   `app/modules/admin/api_97_admin_discussions_reported/{__init__,models,validate,query,view}.py`;
   register the raw-query route in `app/api/v1.py` before any future dynamic
   discussion-ID route; add its path to `app/core/middleware.py`; add migration
   `infra/postgres/study-server/migrations/014_discussion_reports.sql` and keep
   the legacy reference DDL in `infra/postgres/study-server/DB.sql` aligned.
   Use shared `ADMIN` auth before parsing page or querying DB; keep `query.py`
   SQL-only and GET read-only.
6. [x] Add
   `tests/modules/admin/api_97_admin_discussions_reported/test_admin_discussions_reported.py`
   for successful list/projection, unique queue grain, exact filters, default
   and invalid page, empty/out-of-range pages, auth ordering, malformed DB rows,
   DB errors and read-only transaction behavior using fake DB rows.
7. [x] Review #98–#100 open questions and table mappings for queue grain and
   report mapping conflicts. The same report relation/title gap blocks #98;
   #99/#100 also need separately approved moderation/audit/delete state rules.
   Keep these endpoints outside #97's implementation scope.
8. [x] Update #97 DD pages, Study `database.md`, `apis/declared-routes.md`,
   architecture/runtime/modules/tests/workflow pages, registry/status counts
   and DB table guide only where current behavior changed. Run focused/linked
   tests, full Study suite, Ruff, OpenAPI and the Deno context validator; record
   outcomes and live-schema limits.

## Progress / verification

- Source implementation is complete: API #97 is composed with a shared ADMIN
  guard, read-only count/list SQL, fixed Page mapping, the DERIVED Study-local
  migration candidate and a fake-DB HTTP suite. No live schema change has been
  applied.
- Linked API review: #98 confirms the same report relation, report-detail and
  title gaps; #99 needs action/state/audit rules; #100 needs delete marker,
  timestamp, audit and queue-visibility rules. Migration 014's FK
  `ON DELETE RESTRICT` also requires #100 to retain/reconcile report evidence
  before hard delete. See their `OPEN_QUESTIONS.md` and `07_table.md` pages.
- After the user initially selected an approved source, a full-workspace search
  found none usable; the user then delegated the missing-source choice. The
  selected Study-local relation/projection is explicitly `DERIVED` and is
  documented in DD/context; Work's UUID table is not joined.
- Focused #97 tests: 15 passed; linked #92–#95/#97 regression: 102 passed;
  full Study suite: 1315 passed with one upstream Starlette/httpx warning.
  The first full run exposed four pre-existing #92–#95 OpenAPI assertions
  fixed at the former 56/67 totals; updated those assertions to 57/68 and then
  reran both linked and full suites successfully.
  `ruff check app tests` passes and all touched Python files pass scoped format
  check. Repo-wide `ruff format --check app tests` reports 60 out-of-scope
  files that would be reformatted; no formatter was run over those files.
  OpenAPI import reports 57 `/api/v1` path templates / 68 operations.
- Deno context validation ran. It exits invalid on pre-existing DB Admin
  missing context/source paths and references, plus unavailable base commit
  `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` for source-drift checks. It did
  not report missing API #97 source/context paths.
- Pre-existing dirty changes were preserved; no files were staged or committed.
