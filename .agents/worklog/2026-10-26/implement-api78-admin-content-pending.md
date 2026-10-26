---
task_id: "2026-10-26-implement-api78-admin-content-pending"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #78 Admin pending Content queue

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 71 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN role guard and raw query/path handling patterns; keep schema candidates separate from live DB and preserve the dirty worktree.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns database orchestration and transaction behavior; use the current checked-in legacy schema only as a candidate.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Reuse the shared Course/Content read projection where appropriate; preserve the AC-32/AC-33 endpoint boundaries and mark unsupported policies DERIVED.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- AC-33 directly describes an Admin moderation queue, selects Content with `status=PENDING_REVIEW`, then hands off to API #79 detail and API #80 approve or #81 reject before reloading the queue.
- Catalog #78 directly declares `GET /api/v1/admin/content/pending`, Bearer JWT/Admin, optional query `type:string`, `course:int64`, `page:int32`, no body, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Content>`, and errors 401/403/500.
- Reusable Content fields are `id`, `course_id`, `content_type`, `title`, `payload`, `status`, optional `parent_id`, and `order`.
- The endpoint name, queue flow and `page` query imply a collection, while catalog response is one Content object. User authorizes the simplest clear fallback for unresolved conflicts; local list behavior remains DERIVED, not a catalog rewrite. DD remains `Draft — Needs Confirmation`.

## CURRENT_BEHAVIOR (pre-edit)

- The API #78 route, module and HTTP test are absent from current `app/api/v1.py`, middleware path set, `app/modules/admin/` and Admin tests.
- The checked-in legacy candidate `infra/postgres/study-server/DB.sql` and migrations 006/007 define `contents` and `content_versions`. `contents` has BIGINT `id/course_id`, `content_type`, `title`, object JSONB `payload`, text `status`, `parent_id`, `content_order`, and `deleted_at`; no status CHECK or review metadata columns are defined.
- Current API #49 reads active `contents` rows (`deleted_at IS NULL`) and maps the reusable Content projection. API #50 inserts `PENDING_REVIEW`; API #51 snapshots prior logical state to `content_versions`, then changes the current `contents` row to `PENDING_REVIEW`; API #52 changes publication state; API #53 soft-deletes `contents` by `deleted_at`. This is local source/DDL evidence, not proof of live DB availability.
- Current shared `validate_current_user_request(..., role="ADMIN")` is used by APIs #68–#77. The API #78 DD's statement that the current guard is Student-only and that generic `contents` is absent is stale relative to current source.
- API #73 provides the closest Admin list fallback: authenticate before raw query parsing, exact filters, fixed page size 20, `id ASC`, count/page queries with identical filters, 422 validation errors, HTTP 200 for empty/out-of-range pages and read-only behavior.
- Current `error_response()` serializes omitted data as JSON `null`; API #78 DD's `{}` statement is stale. `DESIGN_CONTRACT_PATHS` lacks the new fixed route, so it must be registered for DESIGN error envelopes.
- Related #79–#81 DDs remain Draft and leave revision identity, author/version metadata, approve/reject persistence and audit mapping unresolved. API #78 will return only reusable Content fields and will not implement those operations.
- Worktree is extensively dirty/untracked on `develop...origin/develop`; preserve all existing files and do not stage, commit or clean.

## SOURCE_TRACE

```text
GET /api/v1/admin/content/pending
  -> shared ADMIN Bearer/JWT guard -> parse raw type/course/page query
  -> COUNT + ordered page SELECT from active legacy-candidate contents
     where status='PENDING_REVIEW' and identical optional content_type/course filters
  -> validate count/row/payload projections -> map reusable Content
  -> return local DERIVED Page<Content> in DESIGN_RESOURCE_RETRIEVED envelope
  -> query/mapping failure -> rollback + safe DESIGN_INTERNAL_ERROR
  -> no write/commit; focused HTTP and AC-33 linked regression tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| Response cardinality | Diagram and catalog declare `ApiEnvelope<Content>`; AC-33 queue + page query imply collection. | `DIRECT / DISCREPANCY / DERIVED` | Preserve catalog; implement `ApiEnvelope<Page<Content>>` locally with fixed 20-size Page and keep DD Draft/open for owner/catalog correction. |
| Physical source | DD #78 says generic Content relation absent, but current legacy DDL/migrations and APIs #49–#53 use `contents`. | `CURRENT_SOURCE_OVERRIDES_STALE_DD` | Use only current checked-in legacy `contents` candidate; do not add schema/migration or claim live deployment. |
| Queue row/version | API #50/#51 set the current logical row to PENDING_REVIEW; #51 stores prior state in `content_versions`; catalog has no version selector. | `DERIVED / SOURCE_REQUIRED` | List current `contents` rows only; do not join archived snapshots or select a version in API #78. Keep #79/#80/#81 revision identity open. |
| Deleted visibility | AC-33 does not state deletion filter; APIs #49/#53 treat `deleted_at IS NULL` as active content. | `DERIVED` | Exclude soft-deleted rows from queue using `deleted_at IS NULL`; record as local fallback. |
| Filters | Catalog exposes `type` and `course`; physical candidate columns are `contents.content_type` and `contents.course_id`. | `DERIVED` | Apply exact-match filters and no ContentType whitelist; unknown string returns no matches. |
| Pagination/order | Catalog has `page` but no size/sort; endpoint is a queue. API #73 uses page 1/default, size 20 and `id ASC`. | `DERIVED` | Reuse that deterministic simple convention; page <=0 or out-of-int32 and invalid course int64 return 422 `DESIGN_VALIDATION_ERROR` as a derived validation branch absent from #78 row. |
| Admin authorization | Catalog/diagram require Admin; shared current source guard supports role ADMIN but not finer moderation permission. | `CURRENT_SOURCE / SOURCE_REQUIRED` | Use shared ADMIN guard before parsing/query; do not claim a separate content-moderation permission. |
| Error integration | #78 direct errors omit 422; current shared helper defaults data=null; route template is not registered. | `DIRECT / DERIVED` | Keep 401/403/500; add 422 only for derived query parsing, use current helper, add fixed route to DESIGN allowlist and label DD discrepancy. |
| Queue empty | Catalog has no 404 and list semantics imply an empty collection. | `DERIVED` | Return 200 Page with empty items and zero totals; no 404. |
| Linked review operations | Diagram assigns detail/version/author to #79 and mutations/audit/reason to #80/#81. | `DIRECT_BOUNDARY / SOURCE_REQUIRED` | Return only Content fields; no author/version/review metadata, mutation, audit or reason handling in #78. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Follow user source precedence and record evidence: AC-33 diagram/index → checked-in legacy DDL/migrations plus current APIs #49–#53 → exact API #78/catalog reusable schemas → DD #78 and linked #79–#81; preserve all existing worktree state.
2. Record this plan before source/DD/context implementation edits. Keep the catalog/diagram unchanged and preserve the DD's eight template sheets, appendices and Draft status.
3. Add `admin/api_78_admin_content_pending` models with declarative query/Page/envelope classes; reuse API #49's `ContentResponse` projection where compatible. Add SQL-only matching count/list constants against active `contents` rows.
4. Add `validate.py` for the shared ADMIN guard and raw optional query parsing. Exact `type`/`course` filters; int64 course; page defaults to 1, is positive int32, fixed size 20; invalid numeric/page input maps to local DERIVED 422 without DB access.
5. Implement `view.py`: authenticate before parsing; execute count/list with the exact same PENDING_REVIEW, active-row and optional filters; stable `id ASC`; validate count, list, each row and JSON payload; map only reusable Content fields; return safe 500 with rollback on query/projection errors; never commit or mutate.
6. Wire GET `/admin/content/pending` before any future dynamic `/admin/content/{content_id}` registration, pass raw `Request` query/header plus DB/trace, declare int64/int32 query OpenAPI metadata and direct/derived response codes, and add the fixed path to `DESIGN_CONTRACT_PATHS`.
7. Add focused TestClient HTTP coverage for ADMIN auth before query parsing/DB, invalid int64/int32, exact filters, default/page-2 offsets, page bounds, empty/out-of-range page, projection/payload failures, DB rollback/safe 500, read-only behavior, trace/envelope and OpenAPI. Use fake sessions and label live DB limits.
8. Update all 11 API #78 Markdown DD files to replace stale current-source claims, record the chosen DERIVED collection/source/filter/pagination/deleted/error behavior, preserve the direct catalog discrepancy and open revision/permission/live-schema questions, and retain the registered template suffixes. Review #79–#81 boundaries without implementing them.
9. Update relevant Study Server route/runtime/security/database/module/test/workflow context, project source status and manifest paths for API #78; keep route templates and operations distinct and record fresh test count.
10. Run focused #78 HTTP tests, linked #49–#53/#73–#78 regressions, full Study suite, Ruff, OpenAPI/source checks, DD static/link/example/appendix checks, `git diff --check` and Deno context validation with `--skip-drift`; separate pre-existing DB Admin baseline errors.
11. Inspect the scoped diff/status; preserve unrelated dirt and do not stage/commit. Report derived contract/schema limits and next API #79.

## PRE-CODE CHECKPOINT

- Root instructions, `.agents/AGENTS.md`, context map, exact `coding` worklog selector, all three selected logs, `server-study/AGENTS.md` and `INDEX.md` were read before deep source inspection.
- AC-33 diagram/index was read before infrastructure; legacy `contents`/`content_versions` DDL and migrations 006/007 were then read before API #78 catalog; only then was DD #78 reviewed.
- Current #49–#53 Content projection/lifecycle and #73 Admin list/auth/page/error conventions were traced. DD #78's no-Content/Admin-guard statements are stale against current source; exact response cardinality, revision/version selection, owner permission and live DB remain unresolved.
- The fallback and plan above are recorded before runtime, DD or context implementation changes.

## CHANGES

- Added `apps/study-server/app/modules/admin/api_78_admin_content_pending/` with query models, ADMIN/query validation, SQL constants and read-only count/page orchestration over active `contents` candidate rows in `PENDING_REVIEW`.
- Wired `GET /api/v1/admin/content/pending` in `app/api/v1.py` and registered the path with `DESIGN_CONTRACT_PATHS` in `app/core/middleware.py`.
- Added focused HTTP coverage in `tests/modules/admin/api_78_admin_content_pending/test_admin_content_pending.py` for auth ordering, exact filters, pagination, empty pages, projections, rollback/errors, read-only behavior, trace and OpenAPI.
- Updated all 11 Markdown artifacts in DD #78, including local DERIVED behavior, source discrepancy, open owner decisions and verification report. Preserved all eight registered template appendix suffixes and Draft status; no catalog/diagram/DDL/migration/client/ZIP changes.
- Updated Study Server context pages, project source status and manifest with API #78 route/module/test evidence; all 269 required Study Server source paths exist.
- No staging, commit or cleanup performed; existing unrelated dirty worktree state was preserved.

## VERIFICATION

- Focused API #78 HTTP suite: `23 passed` (one upstream Starlette/httpx deprecation warning).
- Linked regression `#49–#53/#73/#78`: `160 passed`.
- Full Study Server suite: `933 passed`, one upstream Starlette/httpx TestClient deprecation warning.
- Ruff on API #78 changed files and full Study source/tests: all checks passed.
- OpenAPI import/inspection: `44` unique `/api/v1` route templates, `49` operations; API #78 is GET-only.
- DD static checks: 11 Markdown files, 8/8 appendix byte matches, 3/3 JSON examples parse, 21 authored Markdown table blocks, balanced fences, 42 local links and 19 anchor references resolve, no trailing whitespace, final newlines present. Registered template SHA-256 `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; DD payload SHA-256 `a91661b098475b0a90329f5824b56d3e96cda531f9bfa2e24907989f5b9e42a0`.
- Deno context validator `--skip-drift`: no Study Server errors; it reports missing `.agents/db-admin/*`, `apps/db-admin-web/` and `apps/db-admin-server/` entries/source paths outside this task scope.
- Manifest JSON parses and all 269 `server-study.requiredSourcePaths` exist; `git diff --check` passes.
- Fake DB sessions and checked-in candidate DDL do not verify live PostgreSQL schema, grants, deployment or dedicated moderation permission. Response cardinality/page/filter/deleted-row/422 choices remain DERIVED and DD remains Draft.

## HANDOFF

API #78 is locally wired and verified within the recorded boundaries. The catalog/diagram still declare `ApiEnvelope<Content>` while the local queue returns `Page<Content>`; keep this discrepancy and the pagination/filter rules visible until an owner confirms them. Next API in the sequence is #79; inspect its current source/DD and preserve unresolved revision identity/author metadata assumptions before implementing.
