---
task_id: "2026-10-26-implement-api86-admin-lesson-delete"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement API #86 Admin lesson delete

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: shared ADMIN guard, raw signed-int64 path parsing, and BIGINT legacy versus UUID V1-PILOT separation.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: keep `query.py` SQL-only and transaction ownership in `view.py`; preserve dirty worktree.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: atomic mutation handling and explicit DERIVED status for schema fallbacks.
  - path: `.agents/worklog/2026-10-26/implement-api85-admin-lesson-status.md`
    - carry_forward: AC-34 API #85 owns status/audit; lesson delete must preserve its audit history and exclude the tombstone from active lesson reads/writes.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: implement `DELETE /api/v1/admin/lessons/{lesson_id}` for API #86.
- Canonical contract/approved DD: AC-34 permits “soft delete / delete theo policy”; catalog #86 requires progress/reference checks, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`, and exact 401/403/404/422/500 error set. User authorized a reasonable, clear local fallback where the artifacts do not decide the physical policy.
- Selected fallback: use legacy BIGINT `lessons.status='DELETED'` plus database `updated_at` as the persisted tombstone timestamp, following API #77. Return that timestamp as `DeleteResult.deleted_at`. Return 404 for absent/already-deleted Lesson. Block when any legacy `lesson_progress`, `resources`, or `lesson_uploads` row references the Lesson; return catalog 422 and leave all rows unchanged. Keep `lesson_status_audit_logs` as history and do not make it a blocker or delete it.
- Visibility: hide `DELETED` lessons in Admin #82/#83, reject #84/#85 changes to them, and prevent Mentor #48 / Resource #12 reads from exposing the tombstoned Lesson. Other public progress/curriculum readers already require `PUBLISHED`.

## CURRENT_BEHAVIOR

- Source/config: API #86 route/module/test are absent. API #77 provides the local soft-delete precedent. Legacy DDL has BIGINT Lesson status and `updated_at`, plus progress/resource/upload references; it has no Lesson `deleted_at`. API #85 history uses `ON DELETE RESTRICT`. V1-PILOT uses separate UUID/versioned Lesson and is not compatible with this int64 contract.
- Runnable tests: APIs #82–#85, #48, #12 and #77 have HTTP test modules; API #86 has none before this task. These use fake DB sessions and do not verify live schema or migration deployment.
- Runtime wiring: Admin #82–#85 and Mentor #48 / Resource #12 are composed in the Study router. Shared ADMIN role auth exists; AC-34's finer lesson-management permission has no current policy implementation.

## SOURCE_TRACE

```text
DELETE route -> API #86 view -> shared ADMIN guard + signed-int64 parser
-> SELECT FOR UPDATE legacy lessons -> EXISTS progress/resources/lesson_uploads
-> UPDATE status/updated_at -> validate DeleteResult -> commit -> 200 envelope
Related reads/writes: Admin #82/#83/#84/#85, Mentor #48, Resource #12
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Physical deletion policy | AC-34 allows soft-delete or policy delete; API #77 already uses the legacy `DELETED` marker | DERIVED fallback authorized by user | Keep history; do not add schema or hard-delete |
| Blocker set | Catalog says progress/reference; legacy DDL exposes `lesson_progress`, `resources`, `lesson_uploads` | DERIVED | Any matching relation maps to catalog 422; no child data returned or changed |
| `deleted_at` source | DeleteResult requires it; legacy Lesson has `updated_at` only | DERIVED by API #77 precedent | Return DB `updated_at` from the atomic update; live schema remains unverified |
| Admin fine-grained permission | AC-34 says lesson-management permission; current shared guard implements ADMIN role only | DISCREPANCY / SOURCE_REQUIRED | Do not invent a permission code; retain visible limitation |
| Live database | Checked-in DDL/migration and fake-session tests only | UNVERIFIED | No claim of deployed schema/runtime compatibility |

## CHANGES

- Implemented API #86 in `app/modules/admin/api_86_admin_lesson_delete/` and wired DELETE into `app/api/v1.py`.
- Added 15 API #86 HTTP tests and tombstone regression assertions for Admin #82–#85, Mentor #48 and Resource #12. Updated the corresponding reader/writer SQL predicates.
- Updated API #86 DD package and directly linked DDs for #12, #48, and #82–#85. DD remains `Draft — Needs Confirmation`.
- CONTEXT_UPDATES: updated Study Server/project architecture, route, database, module, test, workflow and source-status pages, plus `.agents/context-manifest.json`. The context records the local tombstone mapping and retains live-schema and fine-grained authorization limits.
- Assumptions: no migration; no hard delete/cascade; no delete audit beyond existing #85 history; repeat delete returns 404; API #82 requested `status=DELETED` still returns an empty list.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `.venv/bin/pytest -q tests/modules/admin/api_86_admin_lesson_delete/test_admin_lesson_delete.py` | 15 passed | PASS |
| Linked #09/#12/#47/#48/#77/#82–#86 HTTP regression | 180 passed; one upstream Starlette/httpx warning | PASS |
| `.venv/bin/pytest -q` | 1093 passed; one upstream Starlette/httpx warning | PASS |
| `.venv/bin/ruff check app tests` | All checks passed | PASS |
| OpenAPI composition and API #86 contract | 50 route templates / 57 operations; DELETE documents int64 path, no body, Authorization and 401/403/404/422/500 | PASS |
| DD package static check | 11 files, 33 tables / 377 body rows, 18 balanced fence markers, 3 JSON blocks, 36 local links/anchors; appendix parity 8/8 | PASS — STATIC |
| `git diff --check` | No diagnostics | PASS |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | PARTIAL: unrelated missing `.agents/db-admin/*` and `apps/db-admin-*` paths, broken DB Admin links, and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no API #86/server-study missing-path finding | PARTIAL — BASELINE |

## HANDOFF

- Remaining limits: live DB metadata, applied migration/schema state, FK/lock behavior, and dedicated AC-34 permission are not verified by local artifacts or fake-session tests.
- Next owner/action: continue the one-API-per-session sequence with API #87; keep API #86 DD Draft until its open questions receive evidence/approval.
