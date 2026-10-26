task_id: "2026-10-26-implement-api85-admin-lesson-status"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Implement Admin Lesson Status API #85

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selected worklogs reviewed: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`, `implement-api75-admin-course-update.md`, and `implement-api76-admin-course-status.md`.
- additional adjacent log reviewed: `.agents/worklog/2026-10-26/implement-api84-admin-lesson-update.md`.
- carry_forward: shared ADMIN guard and raw signed-int64 path handling; `query.py` remains SQL-only; status update and audit belong in one transaction; map/validate projection before commit; safely rollback failures; retain DERIVED/open questions and no live-schema claim.
- shortage: `none` (selector reported 78 available coding worklogs and selected the required three).

## EXPECTED_BEHAVIOR

- Catalog #85 and AC-34 directly define `PATCH /api/v1/admin/lessons/{lesson_id}/status`, Bearer JWT/Admin, `lesson_id:int64!`, direct `ApiEnvelope<Lesson>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and exact errors 401/403/404/422/500.
- AC-34 diagram node n9 calls the status API; n10 says `UPDATE status + audit`; successful branch reloads the lesson list through API #82.
- Catalog and diagram omit request body, enum, transition matrix, no-op/retry policy, physical audit schema, and actor mapping.
- Explicit DERIVED fallback for this task: strict one-field JSON body `{status}` with allowed values `DRAFT`, `PUBLISHED`, `SUSPENDED`, reusing the adjacent Study Admin course-status API #76 set because no lesson-specific set exists. DD remains `Draft — Needs Confirmation` and records this as DERIVED, not approval.
- Physical fallback: target the existing legacy BIGINT `lessons` mapping used by APIs #82–#84; append to new `lesson_status_audit_logs` with `lesson_id`, `actor_user_id`, previous/new status, and changed timestamp, following checked-in #76/#80 legacy audit conventions. Add migration `012_lesson_status_audit_logs.sql`; this is source, not evidence of deployment.
- Lock lesson row with `SELECT ... FOR UPDATE`; update `status` and legacy `updated_at`; write audit only on an actual change. Same-status requests return the current Lesson without duplicate audit and commit the read transaction to release the row lock.
- Validate response mapping before commit; any update/audit/projection/commit failure returns safe catalog 500 and rolls back status plus audit atomically.

## CURRENT_BEHAVIOR

- At task start API #84 is wired; API #85 has no route/module/test. Middleware design-contract route set lists `/admin/lessons` and `/admin/lessons/{lesson_id}` but not the `/status` route.
- Shared `validate_current_user_request(... role="ADMIN")` returns numeric actor user ID and is used by #76/#80/#84.
- API #76 already uses a lock → update → audit transaction and treats same-status as no-op; migration 010 is a DERIVED legacy BIGINT audit-table precedent. API #80 and migration 011 provide a second legacy status-review audit precedent.
- Legacy `infra/postgres/study-server/DB.sql` has BIGINT `lessons`, `status VARCHAR(20) DEFAULT 'DRAFT'`, and `updated_at`; it has no lesson status audit table. V1-PILOT UUID Lesson has no status column and its audit resource ID is UUID. These schemas remain separate and live target is unverified.
- Reusable API #09 `Lesson` requires id, course_id, title, order and status; content/video_url are nullable. APIs #82–#84 use this legacy projection.
- API #84 is PUT on the same path template without `/status`; #86 owns deletion. #82 is the list reload boundary.

## SOURCE_TRACE

```text
Strict JSON model validation in FastAPI -> PATCH route -> ADMIN authentication and raw signed-int64 path validation -> SELECT legacy lesson FOR UPDATE -> no-op projection or UPDATE ... RETURNING -> append lesson_status_audit_logs in the same Session transaction -> validate reusable API #09 Lesson -> commit -> ApiEnvelope<Lesson>
```

- Read caller/callee and side effects: router to status view; shared auth; SQL helpers; reusable Lesson model; status and audit writes. Do not change #82 list, #83 detail, #84 metadata update, or #86 delete behavior beyond route-template/context inventory.
- Route registration also requires adding the literal path to middleware's design-contract route set so the handler receives the configured design envelope.
- Tests will cover auth before query for valid body, signed-int64 parse, status/body validation, success and no-op, missing lesson, malformed projection, lock/update/audit/commit failures and rollback, exact error envelope, OpenAPI path/body/error codes, and linked #82–#84/#86 route boundaries.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Body | Catalog/diagram path only | `DERIVED` | Add strict `{status}` request model; retain Draft DD. |
| Status values | No lesson-specific enum; API #76 documents three values; legacy column is VARCHAR(20) | `DERIVED` | Reuse `DRAFT/PUBLISHED/SUSPENDED`; document source and reconsider if owner specifies another set. |
| Audit | Diagram requires audit; no compatible checked-in table for legacy BIGINT Lesson | `DERIVED` | Add legacy BIGINT audit table migration patterned after #76/#80; no claim of application to live DB. |
| Active schema | Legacy BIGINT and V1-PILOT UUID/versioned definitions differ | `SOURCE_REQUIRED` for deployment | Follow current runtime/API #82–#84 mapping; keep schemas distinct and report live DB unverified. |
| Actor mapping | Shared ADMIN auth currently returns integer user ID from JWT `sub` | `SOURCE_BACKED` current implementation | Use validated actor ID in audit row; no new claim about external identity provider. |
| AC-34 fine-grained lesson-management permission | Diagram precondition; current guard checks ADMIN role | `DISCREPANCY` | Reuse current shared ADMIN guard; record that separate permission policy remains unimplemented/unverified. |
| Same status | API #76 precedent has no-op/no duplicate audit | `DERIVED` | Apply same behavior to avoid redundant audit. |
| Response fields | Reusable Lesson has required `course_id`; legacy DDL allows NULL | `DISCREPANCY` | Reject an incomplete projection with safe 500 and rollback; do not substitute values. |
| Error data shape | Current helper returns `data: null` for error responses | `SOURCE_BACKED` | DD should describe current helper accurately. |

## IMPLEMENTATION_PLAN — WRITTEN BEFORE SOURCE EDITS

1. Add module `app/modules/admin/api_85_admin_lesson_status/` with strict request/envelope models, SQL-only query constants for row lock/update/audit insert, validator using shared ADMIN auth and signed-int64 parsing, and transaction-owning view.
2. Add migration 012 with BIGINT lesson/user foreign keys, previous/new status fields and lookup indexes; mark as DERIVED source artifact, not deployed schema.
3. Register the PATCH route beside #84, include OpenAPI request/error contract, and add route template to middleware design-contract allowlist.
4. Add focused HTTP tests with fake Session/query doubles, then linked API #82–#84/#86 coverage.
5. Update all 11 Markdown files in DD #85 with the selected DERIVED contract, schema mapping, no-op/atomic audit semantics, accurate current auth/envelope boundaries, test evidence, and remaining deployment/permission questions. Preserve each of the eight template appendix suffixes byte-for-byte.
6. Update `.agents/context-manifest.json` and relevant Study Server route/runtime/module/test/database pages because source, migration, and route inventory change. Do not alter another scope.
7. Verify with focused/linked/full Study tests, Ruff, OpenAPI inspection, DD parity/static checks, `git diff --check`, and `deno run --allow-read --allow-env scripts/validate-agent-context.mjs`. Report pre-existing unrelated validator blockers without changing other scope.

## CHANGES

- Runtime: added `app/modules/admin/api_85_admin_lesson_status/{__init__.py,models.py,query.py,validate.py,view.py}`, registered PATCH in `app/api/v1.py`, and added `/api/v1/admin/lessons/{lesson_id}/status` to `DESIGN_CONTRACT_PATHS` in `app/core/middleware.py`.
- Database source: added `infra/postgres/study-server/migrations/012_lesson_status_audit_logs.sql` as a DERIVED legacy BIGINT audit candidate.
- Tests: added `tests/modules/admin/api_85_admin_lesson_status/test_admin_lesson_status.py` covering success for both mutation values, same-status no-op, auth/path/body validation, missing and malformed rows, lock/update/audit/projection/commit failures, rollback and OpenAPI.
- DD: updated all 11 files in `apps/study-server/docs/dd/85_admin_lesson_status/`; kept `Draft — Needs Confirmation`; preserved each registered template appendix suffix byte-for-byte.
- Context: updated `.agents/context-manifest.json`, `.agents/project/source-status.md`, and Study Server AGENTS, architecture, database, module, test, workflow, runtime and declared-route pages.
- No files outside Study Server/project context were changed by this task; no stage/commit was made.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `.venv/bin/pytest -q tests/modules/admin/api_85_admin_lesson_status/test_admin_lesson_status.py` | 28 passed; one upstream Starlette/httpx deprecation warning | VERIFIED |
| Linked `api_09`, `api_47`, `api_48`, `api_82`, `api_83`, `api_84`, `api_85` suites | 132 passed; one upstream warning | VERIFIED |
| `.venv/bin/pytest -q` from `apps/study-server/` | 1078 passed; one upstream Starlette/httpx deprecation warning | VERIFIED |
| `.venv/bin/ruff check app tests` | All checks passed | VERIFIED |
| `create_app().openapi()` inspection | 50 `/api/v1` templates / 56 operations; #85 body required and 401/403/404/422/500 declared | VERIFIED |
| DD static validation | 11 files; 8/8 exact template appendix suffixes; 37 tables / 430 rows; 18 balanced fence markers; 4 valid JSON blocks; 40 local links; no trailing whitespace | VERIFIED |
| `git diff --check` | No diagnostics | VERIFIED |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | Fails on pre-existing missing `.agents/db-admin`, `apps/db-admin-*` sources and unavailable baseline source commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no API #85/server-study missing-path report | PARTIAL |
| Context validator with `--skip-drift` | Baseline findings are removed; unrelated DB Admin missing context/source findings remain | PARTIAL |

## HANDOFF

- API #85 is implemented and locally verified; DD remains Draft because status values, fine-grained permission, active schema, migration deployment and soft-delete visibility need owner/schema confirmation.
- Fake DB tests and checked-in DDL/migration do not prove live PostgreSQL behavior or deployment.
- Repository context validation remains globally partial due unrelated DB Admin source/context absence; this task did not modify that scope.
- Next sequence item is API #86 Admin lesson delete. Preserve the existing dirty worktree and continue with its own `coding` worklog preflight.
