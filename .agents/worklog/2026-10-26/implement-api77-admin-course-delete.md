---
task_id: "2026-10-26-implement-api77-admin-course-delete"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-32 #73–#77 course-management flow; DELETE /admin/courses/{course_id}"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #77 Admin course delete

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 70 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: shared ADMIN auth, legacy BIGINT candidate vs V1-PILOT UUID separation, Course projection and singleton Page patterns; preserve dirty worktree and keep derived behavior explicit.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns DB/transaction orchestration; shared `/admin/courses/{course_id}` template is already registered; status/mentor ownership boundaries remain separate.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: course status uses the legacy BIGINT candidate; status + audit is atomic for #76; no audit is specified for #77; fake-session tests and checked-in schema do not prove deployed DB behavior.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-32 #73–#77 course-management flow; shared course identity/status]
```

## EXPECTED_BEHAVIOR

- AC-32 diagram directly assigns `DELETE /api/v1/admin/courses/{course_id}` to “Soft delete theo policy”, then reloads course management.
- Catalog #77 directly requires Bearer JWT/Admin, signed-int64 `course_id`, no body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`, and errors 401/403/404/422/500 with their catalog codes.
- Reusable `DeleteResult` is `{id:int64, status:"deleted", deleted_at:date-time}`.
- Catalog title says conditional deletion with enrollment/content checks; neither source defines exact dependencies or blocker semantics.
- The user authorizes a simple, clear fallback where the direct source leaves implementation details open. Any such behavior stays `DERIVED`, and DD status stays `Draft — Needs Confirmation`.

## CURRENT_BEHAVIOR (pre-edit)

- API #77 route/module/focused tests are absent. API #74 already registers the shared dynamic path template in the design middleware; DELETE should use the existing template.
- Shared `validate_current_user_request(..., role="ADMIN")` is the current authorization pattern; it does not prove AC-32's finer course-management permission.
- Legacy `courses` uses BIGINT identity, `status VARCHAR(20)` and `updated_at`, with no `deleted_at` column. Legacy `enrollments.course_id`, `lessons.course_id`, `contents.course_id`, `quizzes.course_id` and `assignments.course_id` are candidate dependency relations. `contents` has its own `deleted_at` marker.
- V1-PILOT courses use UUID identity and `archived_at`; they are not compatible with the int64 API contract and do not prove a live schema.
- API #72 is an existing soft-delete precedent: set `status='DELETED'`, set `updated_at=CURRENT_TIMESTAMP`, and map returned `updated_at` to `DeleteResult.deleted_at`. API #53 soft-deletes Content with `contents.deleted_at`.
- APIs #73–#76 already handle the same course identity/status; their exact behavior around a `DELETED` course must be recorded in the DD review rather than silently treated as a confirmed policy.
- Worktree is extensively modified/untracked by prior Study tasks on `develop...origin/develop`; preserve all existing entries and do not stage, commit or clean.

## SOURCE_TRACE

```text
DELETE /api/v1/admin/courses/{course_id}
  -> shared ADMIN Bearer/JWT guard -> parse raw path as signed int64
  -> lock existing non-DELETED legacy candidate course row
  -> check candidate enrollment/content relations in the same transaction
  -> if any blocker exists, return catalog 422 without mutation
  -> otherwise UPDATE courses.status='DELETED', updated_at=CURRENT_TIMESTAMP
  -> map UPDATE RETURNING id/updated_at to DeleteResult before commit
  -> commit once; missing/already-DELETED row -> catalog 404; DB/projection/commit failure -> rollback + safe catalog 500
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| Physical soft-delete marker | AC-32 says soft delete; legacy `courses` has `status`/`updated_at` but no deletion timestamp; API #72 uses `status='DELETED'` and maps `updated_at` to `deleted_at`. | `DERIVED` | Reuse the existing course status column and timestamp, with no invented column or migration. |
| Dependency set | Catalog names enrollment/content; legacy candidate relations include enrollments, lessons, contents, quizzes and assignments. | `DERIVED` | Treat any enrollment row, any lesson/quiz/assignment row, or any active generic Content row (`contents.deleted_at IS NULL`) as a blocker; return catalog 422. Preserve all rows. |
| Blocked response | Catalog includes 422 but no condition/message. | `DERIVED` | Use 422 `DESIGN_VALIDATION_ERROR` with a generic safe message; no new business code/response field. |
| Repeated DELETE | Direct sources do not define idempotency. | `DERIVED` | A missing or already-`DELETED` course maps to 404; no replay/key behavior. |
| Response timestamp | Catalog requires `deleted_at`; legacy course has only `updated_at`; API #72 maps that DB timestamp. | `DERIVED` | Return the actual `UPDATE ... RETURNING updated_at` value as `deleted_at`; do not use application clock. |
| Admin permission | AC-32 requests course-management permission; current guard supports shared role `ADMIN`. | `DERIVED / SOURCE_REQUIRED` | Enforce shared ADMIN before path parsing/DB; keep finer permission unresolved. |
| Schema target | Legacy BIGINT and V1-PILOT UUID/versioned models conflict; live DB is unknown. | `DERIVED / NOT_VERIFIED_HERE` | Use only checked-in legacy candidate; make no deployment/schema claim. |
| Post-delete visibility/mutation | #73–#76 and Mentor course/content APIs have existing behavior; sources do not define hide/restore rules for #77. | `SOURCE_REQUIRED` | Keep API #77's marker visible as status where existing Admin reads expose it; document linked behavior and risk without silently broadening this one-API task. |
| Audit | AC-32 diagram specifies audit for #76, not #77. | `DIRECT_BOUNDARY` | Do not append #76 audit rows or add another audit table/event for #77. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Required source precedence reviewed before coding: AC-32 activity diagram/index → legacy and V1-PILOT schema/ERD/table guide → API catalog/reusable schemas → current #72/#53 delete patterns and #73–#76 course boundary.
2. Record this checkpoint before runtime/DD/context edits; preserve all existing dirty/untracked files.
3. Add a focused `api_77_admin_course_delete` module with a strict `DeleteResult`/success envelope, SQL constants only, signed-int64/Admin validation, and a view that owns dependency checks, transaction, mapping, commit/rollback and safe errors.
4. Implement the DERIVED policy in one bound query: lock the course row; check all enrollment rows and active `contents` plus legacy lesson/quiz/assignment rows; block with 422 if any exist; otherwise set `status='DELETED'`, update `updated_at`, and return the DB timestamp. No hard delete, cascade, child mutation, audit, migration or new column.
5. Wire DELETE beside APIs #74–#76 in `app/api/v1.py` with raw path handling, int64 OpenAPI metadata, Authorization and exact catalog errors; reuse the existing path-template middleware entry.
6. Add focused TestClient coverage for auth ordering/role, int64 validation, missing/already-deleted row, enrollment/content blockers, success response/bindings/no hard delete, malformed projections, DB failures, rollback/commit, trace and OpenAPI.
7. Update API #77 DD with selected DERIVED mappings while retaining all files, Draft status and template appendices; preserve open questions for owner permission, live schema and linked post-delete visibility/restore behavior. Review #73–#76 DD references and change only statements made stale by #77.
8. Update current server-study route/runtime/database/security/module/test/workflow context, project source status and manifest for #77 source/tests. Keep route-template count and operation count distinct.
9. Run focused #77 HTTP tests, directly linked AC-32 regressions, full Study suite, Ruff, OpenAPI/source checks, DD static/link/example/appendix checks, `git diff --check`, and Deno context validation; report any out-of-scope baseline failures separately.
10. Review final diff/status. Do not stage or commit.

## PRE-CODE CHECKPOINT

- Root instructions, global `.agents` router/context map, server-study scope/index and worklog selector workflow were loaded before deep source review.
- The Deno coding selector chose 70 available logs and exactly #74, #75 and #76; all three were read before source inspection. No shortage.
- AC-32 #77 diagram/catalog, both course schema candidates, DB table guide, current API #72/#53 delete patterns, API #73–#76 SQL/runtime boundaries and current middleware/error helpers were traced.
- The selected fallback and implementation plan above were written before runtime, DD or context implementation edits.

## CHANGES

- Added the API #77 admin-course-delete module: `models.py`, SQL-only `query.py`, `validate.py`, and `view.py`; wired `DELETE /api/v1/admin/courses/{course_id}` in `app/api/v1.py` using the existing shared path template.
- Added 20 HTTP-level tests covering shared auth/order, signed-int64 input, dependency blockers, missing/repeated deletion, success mapping, query/projection/commit errors, rollback, trace and OpenAPI.
- Updated all 11 Markdown files in `apps/study-server/docs/dd/77_admin_course_delete/`; preserved all eight registered template sheets and their appendix suffixes. DD remains `Draft — Needs Confirmation`; DERIVED behavior and open owner/schema/lifecycle questions remain explicit.
- Updated Study Server source/context pages, route inventory, project source status and the `server-study` manifest paths for API #77. Manifest now lists 263 required source paths, including the route, module and test.
- Preserved the existing dirty/untracked worktree; no staging, commit or cleanup performed.

## VERIFICATION

- Focused API #77 HTTP tests: **20 passed**.
- Linked AC regression (`#06/#08/#72–#77`): **143 passed**.
- Full Study suite: **910 passed**, with one upstream Starlette/httpx warning.
- Ruff: `.venv/bin/ruff check app tests` — all checks passed.
- OpenAPI: **43 path templates / 48 operations**; shared `/api/v1/admin/courses/{course_id}` includes GET/PUT/DELETE.
- DD static checks: 11 Markdown files (8 template sheets + 3 report/question files); 8/8 exact trailing template appendix matches; 2 valid JSON examples; 31 table separator rows; 14 balanced fence markers; 26 relative links resolve; 9 local anchors resolve; no whitespace issues. Template SHA-256 `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; output payload SHA-256 `6d070c45f1f135ee7cbbf3f17b3eb6b49b47215411022284c09407ac9e305108`.
- `git diff --check`: passed.
- Deno context validator ran with `--skip-drift` but exits `AGENT_CONTEXT_INVALID` for the existing/missing `db-admin` context/source tree and its links. Its reported missing paths are outside this `server-study` task; no Study Server/API #77 path is reported missing.
- Fake DB sessions and local HTTP tests do not verify live PostgreSQL schema, constraints, locking, deployed permission policy or production behavior. The blocker set, `DELETED` marker, repeat-delete 404 and `updated_at`→`deleted_at` mapping remain DERIVED pending owner confirmation.

## HANDOFF

API #77 is locally wired and verified; no live deployment or approval of the DERIVED policy is claimed. Keep linked API #75/#76 and Mentor-writer handling of deleted courses as open lifecycle work. The next API in the broader sequence is #78.
