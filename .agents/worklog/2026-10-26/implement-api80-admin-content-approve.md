---
task_id: "2026-10-26-implement-api80-admin-content-approve"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-33 APIs #78/#79/#81; Mentor Content lifecycle APIs #49–#53, especially #51/#52; shared Admin JWT guard and API #76 audit transaction pattern"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #80 Admin Content approval

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 73 coding worklogs available; selected #74, #75, #76; all three read; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN guard precedes raw int64 parsing/query; parameterized reads, reusable response projections, safe errors and fake DB/live-schema limits.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: SQL-only query constants; `view.py` owns orchestration/transaction; validate response before commit; keep derived rules visible.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Shared ADMIN guard yields numeric JWT `sub`; row lock/update/audit/projection/commit belong to one transaction; checked-in legacy BIGINT audit schema is a DERIVED candidate, not live proof.
- additional_related_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api78-admin-content-pending.md`
    - carry_forward: AC-33 queue reads active legacy `contents` rows in `PENDING_REVIEW`; current schema candidates and revision identity limitations are explicit.
  - path: `.agents/worklog/2026-10-26/implement-api79-admin-content-detail.md`
    - carry_forward: API #79 returns only current eight-field Content; #80 has no revision ID, so exact revision continuity cannot be inferred; keep the static queue route reachable and preserve current source evidence.
  - path: `.agents/worklog/2026-10-24/create-study-api80-dd.md`
    - carry_forward: Preserve exact #80 catalog contract, AC-33 status/audit intent, no body/query, Content response and error set; prior DD correctly left status/schema unresolved before current source review.
- related DDs reviewed: API #80 package, API #81 Overview/Mapping/Table/Open Questions, API #79 unresolved revision questions, API #52 publication flow.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-33 APIs #78/#79/#81, Content APIs #49–#53, shared ADMIN guard and API #76 audit transaction pattern]
```

## EXPECTED_BEHAVIOR

- Diagram/index AC-33: Admin selects a pending Content, reads detail, calls `PATCH /api/v1/admin/content/{content_id}/approve`, then performs logical status `APPROVED/PUBLISHED` plus audit and reloads #78.
- Direct catalog #80: Bearer JWT/Admin; required path `content_id:int64`; no body/query; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Content>` with the exact reusable eight-field Content projection; errors exactly 401/403/404/422/500 and catalog codes.
- Direct #81 boundary: rejection request carries required `reason:string`; diagram sets status `REJECTED` plus review reason. This task does not wire API #81.
- API #80 DD remains `Draft — Needs Confirmation`; document DERIVED choices and unresolved revision identity/live deployment rather than upgrading the DD status.

## CURRENT_BEHAVIOR (pre-edit)

- Current OpenAPI has 45 `/api/v1` path templates and 50 operations; full Study suite last verified at 946 passed. Routes, modules and tests exist through #79; API #80 route/module/test do not exist. `DESIGN_CONTRACT_PATHS` contains queue #78 and dynamic detail #79, but not the #80 action path.
- Legacy `DB.sql` and migrations 006/007 define BIGINT `contents`/`content_versions`. `contents.status` is TEXT without a status CHECK; there is no legacy Content review/audit table. `content_versions` stores pre-update snapshots and `archived_by`/`archived_at`, not Admin decision audit.
- API #51 locks current Content/Course, archives the prior row, then sets current `contents.status='PENDING_REVIEW'`. API #52 locks the row and supports `APPROVED → PUBLISHED` and `PUBLISHED → APPROVED`; the separate Mentor publication route therefore supports choosing `APPROVED` as Admin's approval result, while that choice remains DERIVED against AC-33's ambiguous `APPROVED/PUBLISHED` wording.
- API #78 lists active rows with `PENDING_REVIEW`; API #79 reads the current active row but carries no revision token. API #80 cannot prove it is deciding on the exact revision shown in #79.
- V1-PILOT `content_review_decisions` has UUID resource version/reviewer IDs, `expected_row_version`, reason codes/comment and append-only trigger; this artifact does not map directly to the current BIGINT `contents.id` or numeric JWT `sub`.
- Shared auth now supports role `ADMIN` and returns numeric JWT subject; API #76 provides a local row-lock/status/audit/rollback pattern. Shared `error_response()` returns `data:null`.
- API #81 requires a rejection reason; a common legacy audit candidate can reserve a nullable reason field so #81 can later persist its direct reason without implementing #81 here.
- Worktree is heavily modified/untracked on `develop...origin/develop`; preserve it. Do not stage, commit, clean or revert unrelated files.

## SOURCE_TRACE

```text
PATCH /api/v1/admin/content/{content_id}/approve
  -> shared ADMIN Bearer/JWT guard (numeric actor subject)
  -> parse raw signed-int64 path; malformed/out-of-range -> catalog 422
  -> lock one active legacy-candidate contents row by ID
  -> missing/soft-deleted -> catalog 404; status other than PENDING_REVIEW -> catalog 422
  -> update current contents.status to APPROVED with repeated pending/deleted predicates
  -> append one content_review_audit_logs row (actor, old/new status, nullable reason)
  -> validate exact reusable Content projection; commit only after both writes/projection succeed
  -> return HTTP 200 DESIGN_RESOURCE_UPDATED with direct ApiEnvelope<Content>
  -> SQL/audit/projection/commit failure -> rollback + safe 500
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| APPROVED versus PUBLISHED | AC-33 says `APPROVED/PUBLISHED`; AC-22 API #52 is a separate publication route and current source allows publishing from `APPROVED`. | `DISCREPANCY / DERIVED` | Set Admin approval to `APPROVED`; leave `PUBLISHED` to API #52. Keep DD Draft and label the choice derived. |
| Pending eligibility | AC-33 precondition and #78 queue use `PENDING_REVIEW`; API #80 catalog includes 422 but gives no trigger. | `DIRECT_PRECONDITION / DERIVED` | Require current status `PENDING_REVIEW`; existing non-pending Content returns catalog 422. |
| Path parsing | Required int64 path and catalog 422; API #76 maps malformed/overflow Admin IDs to 422. | `DERIVED` | Authenticate first; map malformed/out-of-range int64 to 422 without DB access. |
| Content schema | Legacy BIGINT `contents` matches catalog ID and current APIs #49–#53/#78/#79; V1-PILOT model uses UUID. | `CURRENT_SOURCE_CANDIDATE / NOT_VERIFIED_HERE` | Use active checked-in legacy `contents`; do not claim it is live. |
| Review audit schema | AC-33 directly requires audit; no compatible legacy table exists; V1-PILOT decisions use UUID version keys. | `DIRECT_LOGICAL_EFFECT / DERIVED_PHYSICAL_FALLBACK` | Add migration 011 `content_review_audit_logs` with BIGINT Content/actor FKs, old/new status, timestamp and nullable reason; mirror in legacy DDL, DB guide and ERD. Preserve live-schema limitation. |
| Actor identity | Shared ADMIN guard returns numeric JWT `sub`; legacy users use BIGINT ID. | `CURRENT_SOURCE / DERIVED_MAPPING` | Bind authenticated `sub` as `actor_user_id`; never accept actor from request. |
| Atomicity | AC-33 requires both status update and audit, without transaction detail; API #76 makes status+audit atomic. | `DERIVED` | Lock, update, append, validate response, then commit once; rollback any failure. |
| Revision continuity | #79 and #80 contracts have no revision identifier or expected row version; #51 can create a newer pending revision. | `SOURCE_REQUIRED / OPEN` | Operate on the active row locked at #80 time; do not claim it is necessarily the exact revision viewed in #79. No invented version field. |
| Response | Catalog reuses singular Content; no audit/reason/reviewer/version fields. | `DIRECT` | Return exactly the reusable Content projection with status `APPROVED`. |
| API #81 boundary | Catalog requires `reason:string`; its diagram updates status and review reason; no route/test exists yet. | `DIRECT CONTRACT / NOT_IMPLEMENTED` | Make audit `reason` nullable for approval and available to future rejection; update only directly affected #81 DD schema notes; do not wire #81. |
| Live DB | Checked-in legacy DDL/migrations and fake DB tests do not establish deployed schema. | `NOT_VERIFIED_HERE` | Add no live DB claim; report migration as local candidate only. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Preserve the verified current worktree and this plan before runtime/schema/DD/context edits. Keep exact catalog request/response/errors and Draft DD status.
2. Add `admin/api_80_admin_content_approve/models.py` with a success envelope reusing API #49 `ContentResponse`; no request body model or metadata fields.
3. Add `query.py` SQL constants only: `SELECT ... FOR UPDATE` for one active Content row, conditional `UPDATE ... SET status='APPROVED' ... AND status='PENDING_REVIEW' RETURNING` the eight Content fields, and one insert into the audit candidate. Bind every value.
4. Add `validate.py`: shared ADMIN guard before parsing; parse raw signed-int64 path; use catalog 422 for malformed/overflow input with a safe field error. No body/query or new error code.
5. Implement `view.py`: authorize, parse, lock, validate row/status, return 404 for absent/deleted and 422 for non-pending; update status and append audit under one transaction; validate returned Content; commit last; safely rollback query/audit/projection/commit failures to catalog 500. Never write `content_versions`, publish notifications, infer author or add reason/version fields to response.
6. Wire PATCH `/admin/content/{content_id}/approve` after existing #79 route in `app/api/v1.py`; document path/header and exact 401/403/404/422/500 OpenAPI responses; register its unique path in `DESIGN_CONTRACT_PATHS`.
7. Add migration `011_content_review_audit_logs.sql`, mirror the table/indexes in legacy `DB.sql`, and update DB table guide/ERD. Mark schema/column/actor mapping as DERIVED and live deployment unknown. Use nullable `reason` to support the direct #81 rejection reason in the shared audit record; do not implement #81.
8. Add focused HTTP tests for auth order, invalid int64, 404 missing/deleted, 422 non-pending, successful pending→APPROVED response and audit bindings, no request body, query/update/audit/projection/commit failures and rollback, trace, middleware and OpenAPI. Add regression that #78 pending and #79 detail remain reachable.
9. Update all 11 API #80 Markdown files with source-backed current behavior, chosen DERIVED transitions/physical fallback, response mappings, exact errors, and unresolved revision/live policy. Preserve all 8 registered appendix suffixes and Draft status. Update only directly affected API #81 DD references to the new shared audit candidate/reason boundary while keeping #81 runtime unimplemented and Draft.
10. Update relevant Study Server context pages, project source status and `.agents/context-manifest.json`; add module/test/migration required paths and recount route/operation/full-suite totals from current source/output. Update this worklog after verification.
11. Run focused API #80 tests; linked #49–#53/#52/#76/#78/#79/#80 tests; full Study suite; Ruff; import/OpenAPI inspection; migration/DB.sql/ERD consistency checks; #80 DD static package/link/JSON/appendix/fingerprint validation; `git diff --check`; and Deno context validator with `--skip-drift`. Separate existing DB Admin baseline failures.
12. Review scoped diff/status. Preserve all unrelated dirty files; do not stage or commit. Report APPROVED-vs-PUBLISHED choice, audit migration as DERIVED, exact revision gap, fake DB/live-schema limits and next API #81.

## PRE-CODE CHECKPOINT

- Read root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, worklog contract, Study Server entry/index and the task pages from routes, architecture, runtime, database-security, database, modules, tests and workflows.
- The exact coding selector returned #74/#75/#76; all three were read in full. Also read API #78/#79 implementation worklogs and the prior API #80 DD worklog.
- Read AC-33 index and full diagram before schema; then inspected legacy `contents`/`content_versions`, migrations 006/007/010, V1-PILOT `content_review_decisions`, DB table guide/ERD; then read catalog #80/#81 and Content schema.
- Traced current APIs #49–#53, #76, #78/#79, shared Admin auth, response/DB helpers, route middleware and related API #52/#81 DD boundaries. Evidence supports `APPROVED` as the intermediate state before #52 publication, but #80 cannot bind to the revision viewed in #79.
- The source review and detailed implementation/schema/DD/context plan above are complete before any API #80 runtime, schema, DD or context edits.

## CHANGES

- Added API #80 ADMIN/path validation, row lock, conditional `PENDING_REVIEW` → `APPROVED` update, nullable-reason audit insert, response projection and route/middleware registration.
- Added migration 011 and mirrored the DERIVED BIGINT audit candidate in legacy DB.sql, the table guide and ERD.
- Updated the API #80 DD and directly affected API #81 physical-reason notes; appendices and Draft status are being preserved.
- Updated the Study route/architecture/runtime/security/database/module/test/workflow context, project source status and manifest with API #80 paths and verified counts.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Focused API #80 suite | 22 passed; one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| Linked AC-33/API #52/API #76 regression | APIs #49–#53, #76, #78–#80: 189 passed; same upstream warning. | `VERIFIED_LOCAL_TESTS` |
| Full Study suite | 968 passed; one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| Ruff | `.venv/bin/ruff check app tests`: all checks passed. | `VERIFIED_STATIC` |
| OpenAPI/import | 46 unique `/api/v1` path templates / 51 operations; #80 PATCH exists, has no request body and documents catalog errors. | `VERIFIED_LOCAL_SOURCE` |
| Migration/DDL/ERD | Migration 011 and `DB.sql` contain matching audit columns/indexes; ERD parses with unique IDs and both relations; table guide includes the candidate table. `git diff --check` passes. | `VERIFIED_STATIC` |
| API #80 DD package | 11 Markdown files; all 8 template appendix suffixes byte-exact; 32 relative links valid; 0 JSON examples in the package. DD remains Draft. | `VERIFIED_STATIC` |
| Context validator | `deno run --allow-read --allow-env scripts/validate-agent-context.mjs --skip-drift` reports only the pre-existing missing DB Admin scope roots/pages/contracts; no Study API #80 issue was reported. | `BASELINE_FAIL_OUT_OF_SCOPE` |

## HANDOFF

API #80 local implementation and scoped static/runtime verification are complete. The API #80 DD remains Draft — Needs Confirmation; migration 011 is a checked-in candidate only and has not been applied to a live database. Revision continuity from #79 and deployed schema/permission policy remain open. Context validation is still blocked by the unrelated missing DB Admin scope baseline. Next API in the sequence is #81.
