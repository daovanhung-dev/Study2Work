---
task_id: "2026-10-25-implement-api72-admin-user-delete"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #72 Admin user delete

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 65 coding worklogs available; selected/read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve all existing dirty worktree changes; use checked-in legacy BIGINT schema only as a candidate; do not imply live schema/deployment; preserve safe error/trace behavior.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns DB work, transactions and response; preserve caller-owned commit/rollback; fake-session tests do not prove live schema.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Resolve contract conflicts in diagram → infra → API catalog order; record every DERIVED fallback; preserve existing tree and separate legacy BIGINT from V1-PILOT UUID schema.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Direct catalog: `DELETE /api/v1/admin/users/{user_id}`, Bearer JWT/Admin, required `user_id:int64`, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`; exact errors 401/403/404/422/500 and corresponding `DESIGN_*` codes.
- `DeleteResult`: `id:int64`, `status:"deleted"`, `deleted_at:date-time`.
- AC-31 diagram: DELETE branch applies soft-delete/anonymize policy, then reloads user list/detail. Hard delete is not required by the diagram.
- The API #72 DD is `Draft — Needs Confirmation`; it records physical policy, deletion timestamp source, dependency behavior, idempotency and Admin policy as unresolved.

## CURRENT_BEHAVIOR

- Worktree: 389 modified/untracked entries at task start. Preserve all changes outside the scoped API #72 implementation, its DD/context/worklog and narrowly required linked API review.
- Runtime: APIs #68–#71 have local routes/modules/tests and shared ADMIN JWT guard; API #72 route/module/test is absent. `/api/v1/admin/users/{user_id}` is already in `DESIGN_CONTRACT_PATHS`; the DELETE method itself is unwired.
- Legacy DDL: `users.id BIGSERIAL`, `status VARCHAR(20) DEFAULT 'ACTIVE'` (nullable), `created_at`, `updated_at`; no user `deleted_at`. User-linked rows include courses, enrollments, progress, attempts/submissions, discussions, notifications, payments and refresh tokens. V1-PILOT has a separate UUID identity lifecycle and is not the API int64 target.
- Auth/runtime: API #03 login and refresh require `status == ACTIVE`; access-JWT guard checks claims/roles without current account lookup. API #71 accepts only current/target ACTIVE or SUSPENDED, so it will reject a `DELETED` state. API #68/#69 currently expose rows irrespective of status; API #70 updates profile/role but not status.
- Linked delete precedent: API #53 soft-deletes `contents` using its existing `deleted_at`; its schema is not a source for a user deletion column.
- Tests: current server-study context records 791 passing Study tests and no API #72 tests; these are baseline evidence, not API #72 verification.

## SOURCE_TRACE

```text
DELETE route -> shared ADMIN JWT guard -> raw signed-int64 path validation -> one conditional UPDATE users.status/updated_at -> map DeleteResult(id, "deleted", updated_at as event deleted_at) -> commit -> ApiEnvelope; no physical delete or dependent-row mutation
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Implementation impact |
|---|---|---|---|
| Physical policy | Diagram specifies soft-delete/anonymize according to policy; no approved PII transformation or hard-delete rule. | `DERIVED_FALLBACK` | Choose soft-delete marker only; retain profile and related records; do not anonymize or physically delete. Keep DD Draft. |
| Status marker | Legacy `users.status` is unconstrained `VARCHAR(20)`; API #03 only permits ACTIVE for login/refresh; API #71 rejects states outside ACTIVE/SUSPENDED. | `DERIVED / SOURCE_REQUIRED` | Set `users.status='DELETED'`; value fits the existing field but is not an approved complete UserStatus enum. |
| `deleted_at` persistence | DeleteResult requires a timestamp; legacy users has no dedicated column; V1-PILOT `deleted_at` belongs to a different UUID model. | `DERIVED_FALLBACK` | Use the same DB `CURRENT_TIMESTAMP` written to existing `updated_at`, returned as `deleted_at` for this mutation response. Do not create a column/migration; document that timestamp is not separately persisted. |
| Dependencies | Diagram/catalog mention constraint review; legacy DDL has user-linked FKs but no rule says which should block. Soft-delete leaves referenced user rows intact. | `DERIVED_FALLBACK / SOURCE_REQUIRED` | Preserve every dependent row; do not cascade or invent relation-specific blockers. No physical FK is broken by a status update. |
| Repeat delete | DD leaves idempotency open; catalog has 404 and no 409. | `DERIVED_FALLBACK` | Conditional update excludes existing `DELETED`; no returned row maps to 404 (missing or already marked). |
| Admin policy | Catalog/diagram say Admin; APIs #68–#71 use shared ADMIN JWT guard; no dedicated permission source. | `DERIVED_POLICY_MAPPING` | Reuse shared guard before path parsing and DB; do not add self/last-admin/tenant/MFA policies. |
| Path parsing | Catalog includes 422; API #70/#71 map malformed signed-int64 to 422. | `DERIVED_WITH_DIRECT_CODE` | Reuse signed-int64 bounds and `DESIGN_VALIDATION_ERROR`. |
| Session boundary | API #03 rejects non-ACTIVE login/refresh; access-token guard does not read account status. | `CURRENT_SOURCE_LIMITATION` | No new token mutation; new login/refresh is denied by DELETED status, but existing access JWT can remain usable until expiry. |
| Live schema | Only checked-in legacy/PILOT artifacts are present. | `NOT_VERIFIED` | No claim of live metadata, migration application or deployment. |

## IMPLEMENTATION_PLAN

1. Freeze source precedence and the DERIVED fallback above in this worklog before runtime edits. Do not edit catalog/diagram or add a DB column/migration; preserve legacy FK rows.
2. Add API-local declarative `DeleteResult` and success envelope using the catalog's int64/literal/date-time fields.
3. Add request validation that runs the shared `ADMIN` JWT guard before parsing raw `user_id`; malformed/out-of-int64 path returns 422 `DESIGN_VALIDATION_ERROR`. Do not add a body or query parameter.
4. Keep `query.py` to one SQL constant: conditional soft-delete UPDATE of existing `users.status` and `updated_at`, `WHERE id=:user_id AND status IS DISTINCT FROM 'DELETED'`, returning `id` and `updated_at AS deleted_at`. This handles nullable legacy status and repeat calls without hard delete.
5. In `view.py`, map absent/already-deleted row to catalog 404; validate returned ID/timestamp before commit; rollback on query, invalid projection or commit failure and return safe 500. Preserve dependent rows; do not revoke or delete unrelated records.
6. Wire `DELETE /admin/users/{user_id}` in `app/api/v1.py` on the existing path template, declare required int64/header and exact 200/401/403/404/422/500 responses, and keep the template in `DESIGN_CONTRACT_PATHS`.
7. Add focused HTTP tests for auth-before-DB, path range, no body requirement, successful result, missing/already-deleted 404, safe projection, rollback, trace, status persistence bindings and OpenAPI. Run linked API #03/#68–#72 regression, full Study suite and Ruff.
8. Update API #72 DD pages/report to describe the chosen local fallback as DERIVED, keep `Draft — Needs Confirmation`, preserve all Excel appendix suffixes, and document existing access-token/session and dependency limits. Macro-review #68–#72 boundaries; do not change sibling runtime absent a demonstrated dependency.
9. Update canonical server-study route/runtime/security/database/architecture/module/test pages, project source status and manifest with API #72 files/counts; record current source/test state in this worklog.
10. Run DD Markdown/JSON/link/fence checks, OpenAPI/import inspection, `git diff --check`, and context validator. Separate the known repository DB Admin/snapshot-drift baseline from API #72 findings.

## PRE-CODE CHECKPOINT

Reviewed root/context routing and server-study scope/workflow/tests; preflight read all three selected coding worklogs; read the full API #72 DD set and the registered `createDD-markdown` skill/template; traced AC-31 DELETE and reload nodes, catalog row/reusable `DeleteResult`, legacy/PILOT DDL, API #03 auth, APIs #68–#71, API #53 soft-delete precedent, middleware, response helper and adjacent tests. This checkpoint was recorded before runtime edits; the implementation changes are listed below.

## CHANGES

- Runtime: added `app/modules/admin/api_72_admin_user_delete/{__init__,models,query,validate,view}.py`, the DELETE route in `app/api/v1.py`, and focused API #72 tests. Added linked API #03 login/refresh and API #71 lifecycle regression cases.
- DD: updated sheets 00–07 and reports `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; refreshed #69/#70/#71 macro-review status. Excel appendix suffixes remain byte-identical.
- Context: updated server-study route/runtime/security/database/architecture/module/test/workflow pages, project source status, and manifest with six API #72 source/test paths.
- Assumptions: `status='DELETED'`, response timestamp alias from `updated_at`, 404 repeat behavior, preserved linked records and no explicit token revocation are local DERIVED fallbacks, not policy-owner approvals.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | 65 coding worklogs; selected/read #34/#47/#48 before deep source review. | `VERIFIED_PREFLIGHT` |
| Source/contract review and pre-code plan | API #72 catalog/DD/AC-31, legacy/PILOT DDL, API #03/#53/#68–#71 and shared auth/middleware were traced; plan preceded runtime edits. | `VERIFIED_SOURCE_REVIEW` |
| Focused API #72 tests | 11 passed; one upstream TestClient deprecation warning. | `PASS` |
| Linked API #03 + Admin #68–#72 regression | 95 passed. | `PASS` |
| Full Study suite | 806 passed; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Ruff | `./.venv/bin/ruff check app tests` — All checks passed. | `PASS` |
| OpenAPI import/introspection | 40 unique `/api/v1` path templates, 43 operations; DELETE shares `/admin/users/{user_id}` with GET/PUT. | `PASS` |
| DD/static checks | 11 DD files; JSON/links/fences/appendices checked; 8 sheet appendix suffixes preserved byte-for-byte. | `PASS` |
| Context validator `--skip-drift` | Existing DB Admin context/source/link diagnostics remain outside task scope; Study context has no new structural issue. | `PARTIAL — BASELINE` |
| Context validator default | Includes source snapshot `CONTEXT_STALE` from the pre-existing dirty worktree. No snapshot commit changed to hide drift. | `PARTIAL — BASELINE` |
| `git diff --check` | No whitespace diagnostics. | `PASS` |

## HANDOFF

- Remaining owner decisions: delete/anonymize and PII policy, status enum approval, persistent deletion timestamp, relation retention/block rules, retry semantics, dedicated Admin/tenant/MFA/self/last-admin safeguards, audit, immediate access-JWT revocation, live schema and deployment.
- Next task in the one-API-per-session sequence: API #73.
