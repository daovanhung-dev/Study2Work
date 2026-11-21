---
task_id: "2026-10-26-implement-api79-admin-content-detail"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["API #78 pending queue; AC-33 APIs #80 approve and #81 reject; current Content/version flow #49–#53"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #79 Admin Content detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 72 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN guard, raw signed-int64 detail parsing, exact catalog error set, safe one-row projection and dirty-tree preservation.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: SQL-only query constants, view-owned DB orchestration, response validation before transaction completion, and DERIVED fallbacks kept separate from direct contract.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Keep actor/author semantics evidence-based; physical checked-in schema is not live-schema proof; preserve AC-33 mutation boundaries.
- additional_related_worklog_reviewed: `.agents/worklog/2026-10-26/implement-api78-admin-content-pending.md`
  - carry_forward: Use current `contents`/`content_versions` candidates and API #49 Content projection; keep #79/#80/#81 revision identity and author mapping unresolved; ensure static `/admin/content/pending` is registered before dynamic detail route.
- prior API #79 implementation worklog: `NOT_FOUND`; the existing API #79 DD package and verification report were read instead.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [API #78 queue, current Content APIs #49–#53, AC-33 APIs #80/#81]
```

## EXPECTED_BEHAVIOR

- AC-33 direct flow: Admin selects a Content from #78; `GET /api/v1/admin/content/{content_id}` reads `content/version/author`; then the workflow proceeds to #80 approve or #81 reject and reloads the queue.
- Catalog #79 direct contract: Bearer JWT/Admin; required `content_id:int64`; no body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>` with reusable fields `id`, `course_id`, `content_type`, `title`, `payload`, `status`, optional `parent_id`, and `order`; errors exactly 401/403/404/500.
- API #79 is read-only; it does not approve/reject, update status, or write audit/reason data.
- DD #79 is Draft and names AC-33 version/author metadata, but the catalog response does not define version/author fields.

## CURRENT_BEHAVIOR (pre-edit)

- Route, module and focused test for API #79 are absent. API #78's fixed `/admin/content/pending` route is already registered near the end of `app/api/v1.py`; the new dynamic `/admin/content/{content_id}` route must be added after it so the static queue route remains reachable.
- Current `validate_current_user_request(..., role="ADMIN")` is used by APIs #68–#78. API #69 provides the closest one-row Admin detail pattern: authenticate before raw signed-int64 parse, invalid ID/no row → catalog 404, safe 500 with rollback, no commit.
- Checked-in legacy `DB.sql` and migrations 006/007 define `contents` and `content_versions`. `contents` contains the reusable Content fields plus `deleted_at`; it has no author/creator field. `content_versions` stores pre-update snapshots and `archived_by`/`archived_at`.
- Current APIs #49–#53 use `contents`; #49 reads active rows and maps `ContentResponse`; #50 inserts Content without a creator key; #51 archives the prior row then updates the current row to `PENDING_REVIEW`; #52 updates publish state; #53 soft-deletes via `deleted_at`.
- API #51 binds `archived_by` to the Mentor performing the later update. The table guide explicitly says this is not the original Content author. `content_versions` does not identify a selected revision in the #79 request/response.
- API #78 currently reads active `PENDING_REVIEW` rows; the latest full Study suite recorded immediately before this task is 933 passed. No #79 runtime behavior exists.
- `error_response()` defaults error `data` to JSON null. `DESIGN_CONTRACT_PATHS` lacks `/api/v1/admin/content/{content_id}`.
- Worktree is heavily modified/untracked on `develop...origin/develop`; preserve all pre-existing work and do not stage, commit or clean.

## SOURCE_TRACE

```text
GET /api/v1/admin/content/{content_id}
  -> shared ADMIN Bearer/JWT guard
  -> parse raw content_id as signed int64 after auth; invalid/out-of-range -> catalog 404
  -> bound read of current non-deleted legacy-candidate contents row by id
  -> validate row identity and reusable Content projection/payload
  -> ApiEnvelope<Content>, DESIGN_RESOURCE_RETRIEVED; no row -> catalog 404
  -> DB/projection failure -> safe DESIGN_INTERNAL_ERROR + rollback
  -> no write/commit; focused HTTP/OpenAPI and linked #78/#49–#53 regressions
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| AC-33 metadata | Diagram says read content/version/author; direct catalog/reusable Content response has only eight Content fields. | `DIRECT / DISCREPANCY` | Keep direct `ApiEnvelope<Content>`; implement only source-backed Content projection. Do not add fields or metadata to `meta`; keep version/author read/response need open in Draft DD. |
| Content physical source | Older DD #79 says no compatible generic Content relation; current legacy DDL/migrations 006/007 and APIs #49–#53 define and use `contents`/`content_versions`. | `STALE_DD / CURRENT_SOURCE` | Use checked-in legacy `contents` candidate for current Content row; do not edit schema/migration or claim live deployment. Update DD #79's stale source statements. |
| Version history | #51 archives the pre-update state to `content_versions`; no version selector exists in #79 request or response, and current logical row has no version number. | `CURRENT_SOURCE / SOURCE_REQUIRED` | Read only current `contents`; no version query/selector or `archived_by` interpretation. Record diagram metadata limitation. |
| Author | No creator field exists in `contents` or #50 insert; `content_versions.archived_by` is the updater that archived the prior row, not original author. | `SOURCE_REQUIRED` | Do not infer author from course mentor, updater, reviewer, or pilot UUID identities; do not return author PII. |
| Status between queue/detail | #78 selects `PENDING_REVIEW`; #79 catalog is detail by ID and does not state a status predicate; DD proposes current status without re-filtering. | `DERIVED` | Return the current row's stored status without a status gate; keep stale-queue behavior open for #80/#81. |
| Deleted visibility | API #49 lists active Content and API #53 sets `deleted_at`; catalog #79 has a detail 404. | `DERIVED` | Exclude `deleted_at` rows; missing or soft-deleted row maps to catalog 404. |
| Path validation | Catalog #79 allows 404 and omits 422; API #69 maps malformed/out-of-range signed-int64 detail path to 404. | `DERIVED` | Pass raw path, authenticate first, map invalid signed-int64 and absent row to 404; do not expose framework 422. |
| Admin permission | Catalog/diagram require Admin; current shared guard supports `ADMIN`, not a finer moderation permission. | `CURRENT_SOURCE / SOURCE_REQUIRED` | Use shared ADMIN guard before parsing/query; do not claim separate moderation policy. |
| Error integration | Direct errors are 401/403/404/500; middleware lacks parameterized #79 path; helper emits `data:null`. | `DIRECT / CURRENT_SOURCE` | Add route template to `DESIGN_CONTRACT_PATHS`; use shared error helpers and exact direct business codes. |
| Route precedence | API #78 fixed `/admin/content/pending` exists before a new dynamic detail route is appended. | `CURRENT_SOURCE` | Add #79 after #78 and test both URL patterns. |
| Live schema | DDL/migrations are checked-in candidate artifacts; tests use fake DB sessions. | `NOT_VERIFIED_HERE` | Make no live schema, grant or deployment claim. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Follow required evidence order: AC-33 diagram/index → legacy DDL/migrations and ERD/table guide → API #79 catalog/reusable Content → current #49–#53/#69/#78 source/tests and #80/#81 boundary → API #79 Draft DD. Preserve all existing worktree state.
2. Record this plan before runtime, DD or context implementation changes; retain the direct catalog response/error set and API #79 Draft status.
3. Add `admin/api_79_admin_content_detail/models.py` with a strict success envelope reusing API #49 `ContentResponse`; keep declarative models only and do not add version/author properties.
4. Add `query.py` with one SQL constant selecting the eight reusable Content fields from the active `contents` candidate by bound ID; no joins or version/author query. Keep `query.py` SQL-only.
5. Add `validate.py` with shared ADMIN auth and signed-int64 parsing for raw path text; no input error outside the catalog set, so malformed/out-of-range ID maps to 404.
6. Implement `view.py`: authenticate before parse/query, use one bound read, treat missing/deleted as 404, validate exact row ID and payload/model projection, return safe 500 with rollback on SQL/projection failures, construct `DESIGN_RESOURCE_RETRIEVED`, never commit or mutate.
7. Wire GET `/admin/content/{content_id}` after the static #78 queue endpoint, pass raw `Request.path_params`, document int64 path and Authorization in OpenAPI with exactly catalog 401/403/404/500 responses, and register the path template in `DESIGN_CONTRACT_PATHS`.
8. Add focused HTTP tests for ADMIN auth/ordering, malformed/overflow path, current Content projection across stored statuses, missing/soft-deleted row, query/projection/payload errors and rollback, read-only behavior, trace/envelope/OpenAPI, plus a regression proving `/admin/content/pending` still reaches API #78.
9. Update all 11 API #79 Markdown artifacts: replace stale no-Content/Student-only/helper claims with current evidence; document current `contents` candidate, active-row detail mapping, exact response, invalid path/missing row 404, and unresolved diagram version/author metadata. Preserve the direct catalog discrepancy, Draft status, all eight template appendix suffixes, and no-ZIP policy. Review #80/#81 handoff without implementing them or treating `archived_by` as author.
10. Update affected Study Server route/runtime/security/database/module/test/workflow context, project source status and manifest paths/counts for API #79. Keep dynamic path template, operations and tests synchronized.
11. Run focused API #79 HTTP tests, linked #49–#53/#78/#79 regression, full Study suite, Ruff, import/OpenAPI checks, DD package/static/link/example/appendix/fingerprint validation, `git diff --check`, and Deno context validator `--skip-drift`; separate DB Admin baseline failures.
12. Review scoped diff/status, preserve unrelated changes and do not stage/commit. Report unresolved AC-33 metadata and fake-DB/live-schema limits; next API is #80.

## PRE-CODE CHECKPOINT

- Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, worklog rules, Study Server entry/index and relevant scope pages were read. The exact coding selector returned #74/#75/#76; all three were read before deep source review. API #78 implementation worklog and API #79 DD were also reviewed; old API #79 implementation worklog was not found.
- AC-33 diagram was inspected first. Then checked-in legacy `contents`/`content_versions` DDL, migrations 006/007 and DB table guide were inspected. The exact catalog #79 row and reusable Content schema were then read, followed by current APIs #49–#53/#69/#78 source and API #79/#80/#81 DD boundaries.
- Source evidence confirms a current Content candidate, but does not identify the original author or a revision selector. `archived_by` is the updater of the old snapshot and must not be mislabeled.
- The fallback and plan above are recorded before implementation edits. No source, DD or context files for API #79 have been edited yet.

## CHANGES

- Added `apps/study-server/app/modules/admin/api_79_admin_content_detail/` with a strict envelope reusing API #49 `ContentResponse`, a single bound active-row SELECT from checked-in legacy `contents`, ADMIN-before-path validation, signed-int64 parsing, safe catalog 404/500 handling and read-only response orchestration.
- Wired GET `/api/v1/admin/content/{content_id}` after API #78 static queue route with int64/Authorization OpenAPI metadata and exact catalog errors; added route template to `DESIGN_CONTRACT_PATHS`.
- Added 13 focused HTTP tests for auth order, projection/status, malformed/overflow/missing/deleted behavior, rollback, read-only behavior, route precedence and OpenAPI.
- Updated all 11 API #79 Markdown artifacts, preserving Draft status and 8 template appendix suffixes. DD now reflects current `contents` source candidate and keeps version/author/revision identity unresolved.
- Updated Study Server routes/runtime/database/security/module/test/workflow context, project source status and manifest; registered 6 API #79 source/test paths.
- No migration, catalog, diagram, client, stage, commit or cleanup changes.

## VERIFICATION

- Focused API #79 HTTP suite: 13 passed.
- Linked API #49–#53/#78/#79 regression: 149 passed.
- Full Study suite: 946 passed, one upstream Starlette/httpx deprecation warning.
- Ruff `check app tests`: all checks passed.
- OpenAPI: 45 unique `/api/v1` templates / 50 operations; both `/admin/content/pending` and `/admin/content/{content_id}` are present.
- DD static check: 11 Markdown files (8 sheets + 3 reports), 8/8 appendix byte matches, 2 valid JSON examples, 165 authored tables outside appendices/report, 5 balanced code fences, 32 local links and 16 anchors resolve, no trailing whitespace, final newline on every file.
- Template SHA-256: `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.
- DD payload SHA-256: `93b3b470233c1087ac8c322b1e4e24a83f1766b229300c6025ee2b12c1b28195`.
- Context validator `deno run -A scripts/validate-agent-context.mjs --skip-drift`: reports missing DB Admin context/source roots only; no Study Server errors. This is outside the requested scope and is consistent with the existing checkout boundary.
- Local fake-DB tests and checked-in DDL do not prove live schema, migration deployment, moderation-specific policy or revision identity.

## HANDOFF

API #79 is locally wired and verified. AC-33 version/author projection and stable revision identity remain open; the response intentionally follows the direct Content catalog. Next API in the broader sequence is #80. Preserve the dirty worktree; do not stage/commit/clean.
