---
task_id: "2026-10-26-implement-api76-admin-course-status"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-32 APIs #74/#75/#77; shared /api/v1/admin/courses/{course_id} path and Course projection"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #76 Admin course status

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 69 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Reuse shared Course projection and singleton Page pattern; keep shared ADMIN role as a DERIVED permission fallback; preserve the dirty worktree.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Keep query.py SQL-only and view.py transaction owner; preserve status/metadata/delete boundaries; path template is already registered; legacy BIGINT remains a candidate, not live-schema proof.
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Bind all SQL values; fake-session tests and checked-in migrations do not prove deployed schema or external runtime.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-32 APIs #74/#75/#77; shared /api/v1/admin/courses/{course_id} path and Course projection]
```

## EXPECTED_BEHAVIOR

- AC-32 diagram direct flow: Admin with course-management permission selects STATUS; `PATCH /api/v1/admin/courses/{course_id}/status` updates course status and writes an audit log, then reloads course management.
- Catalog direct contract: Bearer/Admin, required `course_id:int64`, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500 with catalog codes. The request body is not directly declared.
- Catalog status labels are draft/published/suspended. API #75 owns metadata; #76 owns status plus audit; #77 owns soft-delete.
- Existing API #76 DD is Draft and says body, enum/casing, physical audit mapping, transitions and live schema are unresolved.

## CURRENT_BEHAVIOR (pre-edit)

- API #76 route/module/tests are absent. `/api/v1/admin/courses/{course_id}` is already registered by #74/#75 and middleware matches the FastAPI route template; no duplicate middleware allowlist entry is needed.
- Shared `validate_current_user_request(..., role="ADMIN")` returns numeric JWT `sub` as an integer. Current role guard does not implement AC-32's separate course-management permission.
- Legacy Study DDL defines BIGINT `courses.id`, `users.id`, `courses.status VARCHAR(20)`, and `updated_at`; no course audit relation exists. V1-PILOT `audit_events` uses UUID actor/resource keys and versioned UUID courses, incompatible with this int64 API path.
- API #74 provides `FIND_ADMIN_COURSE_DETAIL` and the shared Course mapper; #75 demonstrates bound course mutation/readback, response projection before commit, rollback and safe errors. #71 demonstrates shared ADMIN validation and status update orchestration but its user/token behavior is not a course rule.
- AC-32 draw.io says `UPDATE status + audit log` and links API #76 → that action → reload. AC-32 does not specify audit columns, request body, enum casing, transition matrix, no-op semantics or physical relation.
- Worktree is already heavily modified/untracked under `develop...origin/develop`; preserve all prior work, do not stage/commit/clean.

## SOURCE_TRACE

```text
PATCH /api/v1/admin/courses/{course_id}/status
  -> strict candidate body {status}; shared ADMIN JWT guard yields numeric actor user ID
  -> validate signed-int64 course_id and candidate status values
  -> lock courses row; missing row -> 404
  -> if target differs: UPDATE status + updated_at and append course_status_audit_logs(old,new,actor) in same transaction
  -> read #74 Course/mentor projection, map allowlisted Course and singleton Page<Course>
  -> commit only after required audit and response mapping succeed
  -> DB/audit/projection/commit failure -> rollback + safe 500; target equal to current -> success without duplicate audit row (DERIVED idempotent no-op)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| Request body | Catalog and diagram declare only path; status operation needs a target. | `DISCREPANCY / DERIVED` | Strict JSON `{status}` body, unknown fields forbidden; preserve DD Draft and do not rewrite catalog/diagram. |
| Status values/casing | Catalog says draft/published/suspended; legacy/default and #06 use uppercase DRAFT/PUBLISHED; enum does not enumerate members. | `DERIVED` | Accept uppercase `DRAFT`, `PUBLISHED`, `SUSPENDED`; retain exact labels in DD as an implementation fallback. |
| Transition/readiness policy | Diagram has no transition/readiness gates; course content publish API is separate. | `DERIVED` | Set any listed target directly; no readiness, notification, enrollment or content side effect. |
| Audit persistence | Diagram requires audit log; legacy schema has no audit table; V1-PILOT audit_events has incompatible UUID IDs. | `DERIVED` physical fallback | Add minimal append-only-by-application legacy candidate relation with course_id, actor_user_id, previous_status, new_status, changed_at; mirror in migration 010 and DB.sql. Atomically write it with status update. No live-schema claim. |
| Actor mapping | Shared auth validates numeric JWT `sub`; legacy users/courses use BIGINT. | `DERIVED` | Record authenticated numeric `sub` as `actor_user_id` FK to legacy users.id. |
| Same-status request | Direct sources silent. | `DERIVED` | Idempotent no-op: return current Course and do not change updated_at or append a duplicate audit row. |
| Response cardinality | Catalog returns Page<Course> for a by-ID mutation; #74/#75 use a singleton page. | `DERIVED` | Return one Course in singleton Page. |
| Admin permission | AC-32 requires course-management permission; current guard exposes shared ADMIN role only. | `DERIVED / SOURCE_REQUIRED` | Enforce shared ADMIN role; explicitly leave finer permission policy unverified. |
| Legacy vs pilot/live schema | Legacy schema matches int64; V1-PILOT course/audit identities are UUID; live DB unknown. | `DERIVED / NOT_VERIFIED_HERE` | Target only the checked-in legacy candidate and add an incremental migration; report tests as fake DB only. |
| Status/delete visibility | #77 owns soft-delete and policy; marker/filter unconfirmed. | `SOURCE_REQUIRED` | Do not add deletion checks or visibility side effects beyond existing #74 projection behavior. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete the required source order and current-source trace: AC-32 index and diagram → legacy/V1-PILOT schema and ERD/table guide → API catalog → #76 DD and linked #71/#73–#75/#77 code/tests. Preserve all preexisting worktree changes.
2. Record this plan before any implementation/schema/DD/context edits; retain API #76 DD `Draft — Needs Confirmation` and appendices.
3. Add a strict request model with only `status` and an envelope typed to shared `CoursePage`. Add validation for ADMIN JWT, signed-int64 path, and the three uppercase catalog-derived status candidates; reject extra body fields and map input failures to catalog 422.
4. Add SQL constants only: row lock, status update with `updated_at` and `RETURNING`, audit insert, and reuse #74 detail projection. Bind every value.
5. Add a minimal legacy candidate table `course_status_audit_logs` with BIGINT course/admin foreign keys, previous/new status, and timestamp. Add migration `010_course_status_audit_logs.sql`, mirror it in `infra/postgres/study-server/DB.sql`, and update the Study DB guide/ERD as a DERIVED candidate; do not alter V1-PILOT UUID tables.
6. Implement the view transaction: validate before DB, lock and validate row shape, no-op on same status, update plus audit in one transaction on change, read/map Course, build singleton Page, commit last; safely rollback on missing/malformed/query/audit/projection/commit failures. Return only catalog 401/403/404/422/500 business codes.
7. Register PATCH beside #74/#75 and add its distinct `/admin/courses/{course_id}/status` template to the middleware contract allowlist; declare body, int64 path, auth header and exact catalog error responses in OpenAPI.
8. Add focused HTTP tests for transition success/audit actor+old/new binding, same-status no-op, auth/path/body/status validation, missing course, atomic rollback on audit/projection/commit failure, trace/envelope and OpenAPI. Add no unrelated tests.
9. Update API #76 Markdown DD sources/mappings/assumptions/errors/sequence/open questions/verification, preserving 11-file package and template appendix bytes; keep owner-dependent authorization/live-schema and policy questions open. Macro-review only the linked AC-32 #73–#77 boundary.
10. Update `.agents/server-study` route, architecture/runtime/database-security/database/module/test/workflow/source-status pages and context manifest for API #76, migration and audit relation; remove only exact duplicate API #75 context blocks encountered in directly updated pages. Record counts from current files and validate context.
11. Run focused API #76 HTTP tests, linked #06/#08/#71/#73–#76 regression, full Study suite, Ruff, OpenAPI/source checks, DD static/link/example/appendix checks, SQL/migration consistency review, `git diff --check`, and Deno context validation. Keep fake-DB/schema limitations explicit.
12. Review final diff/status; do not stage or commit.

## CHANGES

- Added API #76 module (`models.py`, `query.py`, `validate.py`, `view.py`) and `PATCH /api/v1/admin/courses/{course_id}/status` route with OpenAPI metadata.
- Added the distinct #76 path template to `DESIGN_CONTRACT_PATHS`; body-validation errors now use the Study DESIGN envelope.
- Added `course_status_audit_logs` to legacy `DB.sql`, migration `010_course_status_audit_logs.sql`, the Study table guide and ERD. The table/mapping is explicitly DERIVED and does not imply a live migration.
- Added focused TestClient HTTP tests for ADMIN auth, body/path validation, status update/audit bindings, no-op, not found, rollback/error branches, trace/envelope and OpenAPI.
- Updated all 11 API #76 Markdown DD files/reports; preserved the 8 Excel-template appendix suffixes and `Draft — Needs Confirmation`.
- Updated `.agents/server-study` route/architecture/runtime/security/database/module/test/workflow pages, `.agents/project/source-status.md`, and `.agents/context-manifest.json`; manifest now tracks 257 Study source paths including #76 module/test/migration files.
- Preserved all preexisting dirty/untracked files; did not stage or commit.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Deno coding worklog selector | 69 available; selected #74, #75, #34; all read; shortage none. | `VERIFIED_PREFLIGHT` |
| `.venv/bin/pytest -q tests/modules/admin/api_76_admin_course_status/test_admin_course_status.py` | 18 passed. | `VERIFIED_LOCAL_HTTP_TESTS` |
| Linked regression `api_06_courses api_08_courses_detail api_71_admin_user_status api_73_admin_courses_list api_74_admin_course_detail api_75_admin_course_update api_76_admin_course_status` | 134 passed. | `VERIFIED_LOCAL_HTTP_TESTS` |
| `.venv/bin/pytest -q` | 890 passed; one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| `.venv/bin/ruff check app tests` | All checks passed. | `VERIFIED_STATIC` |
| Import/OpenAPI | 43 `/api/v1` path templates / 47 operations; API #76 body enum and exact catalog responses present. | `VERIFIED_LOCAL_SOURCE` |
| DDL/migration check | Table columns/FKs and two indexes match between `DB.sql` and migration 010. | `VERIFIED_STATIC` |
| ERD and DD checks | Draw.io XML parses with unique IDs and valid audit relations; 11 DD files, 8 appendices, 2 JSON examples and 18 local links verified. | `VERIFIED_STATIC` |
| `git diff --check` | No whitespace errors. | `VERIFIED_STATIC` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Reports only preexisting missing DB Admin context/source paths and links outside Study scope; no Study #76 errors. | `BASELINE_FAIL_OUT_OF_SCOPE` |

## LIMITATIONS

- HTTP tests use fake sessions/rows and do not execute PostgreSQL. Migration 010 application, live schema, grants, DB immutability, production deployment and dedicated course-management permission remain unverified.
- Body, uppercase status allowlist, same-status no-op, singleton Page and minimal BIGINT audit schema are local DERIVED fallbacks; the API #76 DD remains Draft for owner review.

## HANDOFF

- API #76 is wired and locally verified; the next one-API task may continue at #77.
- Keep current worktree changes intact and keep the DERIVED/live-schema boundary explicit.
