---
task_id: "2026-10-26-implement-api89-admin-quizzes-update"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement Study Server API #89 Admin quiz update

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 82 available; selected 3; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve the dirty worktree; use shared ADMIN auth before raw input/query; legacy BIGINT and fake DB evidence do not establish live schema.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` is SQL constants only; `view.py` owns transactions and response mapping; bind parameters and retain DERIVED/Draft boundaries.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Use diagram → infrastructure → catalog order; atomic writes; shared ADMIN role does not implement AC-specific permission; report migration/live DB limits.
- Additional direct dependency reviewed: `.agents/worklog/2026-10-26/implement-api88-admin-quizzes-create.md` and API #87–#89 source/DD; API #88's request validator and insert SQL define the current local nested Quiz proposal.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- AC-35 Admin UPDATE branch calls `PUT /api/v1/admin/quizzes/{quiz_id}` and updates Quiz/question set.
- Direct catalog contract: Bearer JWT with role Admin; required `quiz_id:int64` path; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Quiz>`; exact errors 401/403/404/422/500. Catalog defines no body.
- Existing API #89 DD proposes reusing #88's outer `{config:string, questions:string}` body and nested shape as `DERIVED`; it proposes full replacement and rejects updates when attempts/answers could reference old child IDs.
- AC-35 #90 directly requires soft-delete when attempts exist. #90/#91 DDs propose the `DELETED` tombstone; API #87 already hides that candidate by default. These remain unapproved local design choices.

## CURRENT_BEHAVIOR (pre-edit)

- API #89 has no route/module/test. API #87/#88 own `/api/v1/admin/quizzes`; middleware has the fixed path but not `/api/v1/admin/quizzes/{quiz_id}`.
- Shared `validate_current_user_request(..., role="ADMIN")` is available; no fine-grained AC-35 quiz-management claim/policy is source-backed. Error helper emits `data:null` and field errors in `meta.fieldErrors`.
- AC-35 activity diagram says `UPDATE quiz/question set`, with path-only #89 input and Quiz response. It defines no body, replacement, history, course-move, tombstone, or locking policy.
- Legacy BIGINT DDL defines `quizzes`, `quiz_questions`, `quiz_choices`, `quiz_attempts`, and `quiz_answers`; attempts reference quizzes, answers reference attempts/questions/choices. Migration 013 provides local DERIVED question type/order columns. `quizzes.updated_at` is NOT NULL without a default. No live schema/migration deployment is verified.
- API #88 validator defines the current local embedded JSON proposal, strict scalar types, score/title storage bounds, optional `duration_minutes` and optional choice `is_correct=false`; its SQL constants create identical replacement child projections. Student APIs #29/#30 are DD-only and no current attempt/answer runtime module exists.
- API #90/#91 DDs propose `DELETED`, #89 not updating tombstones, and history retention; fine-grained permission and concurrency remain open. Their auth text has stale claims that the shared ADMIN guard is missing.
- Worktree is extensively dirty under `develop...origin/develop`; all unrelated modifications must remain untouched. Do not stage, commit, or clean.

## SOURCE_TRACE

```text
PUT raw route (path/header/body bytes)
  -> API #89 shared ADMIN guard before path/body validation or SQL
  -> parse positive signed-int64 quiz_id; reuse #88 validator for the DERIVED config/questions shape
  -> SELECT active Quiz FOR UPDATE (tombstone/absent -> 404)
  -> lock existing question then choice rows; check any attempt or answer reference before writes (history -> catalog 422)
  -> lock/check target course; update parent metadata and updated_at
  -> DELETE old choices then questions; INSERT replacement questions then choices in input order
  -> map complete Admin Quiz response using generated IDs; commit last
  -> rollback all failures and return catalog-only safe errors; focused HTTP/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned local handling |
|---|---|---|---|
| Request body | Catalog/diagram specify path only; diagram says update Quiz/question set; API #88 has the only concrete config/questions shape. | `DISCREPANCY / DERIVED` | Reuse #88 outer strings and validator; document body as proposal in OpenAPI/DD, not direct contract. |
| PUT semantics | No child IDs in candidate body; AC-35 update needs question set. | `DERIVED` | Full replacement; absent/null `duration_minutes` maps to NULL; allow empty arrays because no minimum is sourced. |
| Attempt/answer history | DDL references quiz/question/choice IDs; #90 requires soft-delete with attempts; #89 DD proposes preserving referenced IDs. | `DERIVED / SOURCE_REQUIRED` | Reject the whole update with catalog 422 if any attempt or related answer exists; perform all checks before writes. |
| Concurrency | FK candidate relations protect attempt and answer references; #29/#30 do not have runtime locking source. | `DERIVED / NOT_VERIFIED_HERE` | Lock Quiz, then current questions/choices before history check; this serializes candidate FK writers. Fake DB tests cannot prove PostgreSQL lock behavior. |
| Tombstone | #87 excludes `DELETED`; #90/#91 propose the same marker and say #89 rejects tombstones. | `DERIVED` | Treat `status IS DISTINCT FROM 'DELETED'` as update eligibility; absent/tombstone maps to catalog 404. |
| Course move | Reused `config.course_id`; legacy FK exists; no course-move policy is defined. | `DERIVED` | Require and key-share-lock an existing course; allow moving to another existing course; do not check publication/enrollment. |
| Field semantics | #88 validator and DDL define title 200, NUMERIC(5,2), int32 duration, type vocabulary/order; score/status/description are not request fields. | `DERIVED / CURRENT #88 FALLBACK` | Reuse the validator; update only course/name/score/duration/updated_at, retain status/description and default question score. |
| Authorization | AC-35 says quiz-management permission; current source has only shared ADMIN guard. | `SOURCE_REQUIRED / LOCAL LIMITATION` | Enforce ADMIN before parsing and DB; do not claim fine-grained permission. |
| Error envelope | Current helper and API guidelines require `data:null`; linked #89 DD still has stale `{}` wording. | `DISCREPANCY` | Follow current helper and correct the DD. |
| Legacy/live DB | Checked-in legacy schema and migration 013 match the API int64 model; V1-PILOT is UUID and incompatible. | `DERIVED / NOT_VERIFIED_HERE` | Target checked-in legacy candidate only; add no schema/migration in #89; do not infer deployment. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete source-priority and caller/callee review: AC-35 node/index → legacy DDL, DB guide/ERD, migration 013 and FK chain → exact catalog row/reusable Quiz schema → #87/#88 source/tests → #90/#91 lifecycle and #29/#30 attempt boundaries. Preserve direct-versus-DERIVED status.
2. Keep API #89 DD Draft. Use its registered Markdown template baseline, correct stale ADMIN/error-helper/schema statements, and record each implemented fallback after source changes.
3. Add `admin/api_89_admin_quizzes_update/` with SQL-only `query.py`, raw path/body validation, a response envelope reusing #88's Quiz data projection, and `view.py` transaction ownership. Reuse #88's strict request parser and question/choice INSERT constants rather than duplicating nested contract rules.
4. Add bound SQL constants for active Quiz `FOR UPDATE`, child question/choice row locks, combined attempt/answer EXISTS, target Course `FOR KEY SHARE`, parent UPDATE/RETURNING, child-first DELETE/RETURNING. Do not modify schema or touch answer/history rows.
5. Implement one transaction: authenticate/validate first; lock parent and children; reject tombstone/missing Quiz and any history before mutation; verify target course; update metadata/timestamp; delete old choices then questions; insert ordered replacement rows; validate every returned row and full Quiz response; commit last. Every post-lock error rolls back; only catalog 404/422/500 are added beyond shared 401/403.
6. Wire raw `PUT /admin/quizzes/{quiz_id}` beside #87/#88; add its dynamic path template to `DESIGN_CONTRACT_PATHS`; publish explicit derived body schema, int64 path, response model, HTTP 200 and exact catalog errors in OpenAPI. Keep auth ahead of path/body parsing.
7. Add HTTP tests for auth-before-parse/DB, path bounds, body validation, missing/tombstone, attempt and answer history, course existence, full parent/child replacement/order/response, empty child arrays, mapping/query/commit rollback, no partial writes, trace/error envelope and OpenAPI.
8. Update API #89 DD sheets/reports, directly stale #90/#91 permission/path references if required, server-study context pages, source-status and context manifest. Preserve existing DD appendix tails and Draft status.
9. Run focused #89 tests, linked #87–#90 and #28/#29/#30 regression, full Study suite, Ruff, OpenAPI/import, SQL/ERD and DD static checks, `git diff --check`, and Deno context validator. State fake-DB/live-locking/schema/deployment limits.
10. Review final diff and worktree; do not stage, commit, or clean.

## PRE-CODE CHECKPOINT

- Root/global router, context map, current server-study entry/index/workflow pages and the exact coding worklog preflight were loaded.
- Read selector worklogs #74, #75, #76; additionally reviewed API #88 worklog and API #87/#88 source/tests.
- Read AC-35 UPDATE node and direct #89 catalog contract; inspected BIGINT FK chain, migration 013, Quiz table guide/ERD and API #90/#91 plus #29/#30 lifecycle boundaries.
- Confirmed current source after the plan: API #87/#88 are wired; the #89 dynamic route is absent from `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`, and no #89 module/tests exist. The #89 DD still contains the stale `data=None -> {}` claim in `04_Response.md`; current helper returns `data:null`.
- No runtime/API #89 source edit has been made. The implementation plan above is recorded before coding.

## CHANGES

- Added the `PUT /api/v1/admin/quizzes/{quiz_id}` raw route and middleware path contract; implemented the `api_89_admin_quizzes_update` models, SQL-only query constants, validation and transaction orchestration.
- Added API #89 HTTP tests for auth ordering, path/body validation, missing/tombstoned quizzes, history checks, course lookup, ordered child replacement, response mapping, rollback and OpenAPI.
- Updated the 12 API #89 DD sheets and three reports. Kept the DD `Draft — Needs Confirmation`; body, full replacement, history rejection, tombstone/course behavior and lock order remain DERIVED.
- Updated stale #90/#91 references and server-study/project context pages. Added all six new Python source/test files to both `server-study.trackedRoots` and `requiredSourcePaths` in `.agents/context-manifest.json` (56→62 tracked roots; 330→336 required source paths).
- No schema, migration, API catalog or diagram change. Unrelated dirty worktree changes were preserved; nothing was staged or committed.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Context/worklog preflight | Deno selector chose coding worklogs #74–#76; all three read, shortage none; API #88 worklog and linked #87/#88 source/tests also reviewed. | `VERIFIED_PREFLIGHT` |
| Focused API #89 HTTP suite | 26 passed; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Linked #87–#89 quiz regression | 67 passed. | `PASS` |
| Full Study Server suite | 1160 passed; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Ruff | `.venv/bin/ruff check app tests` passed. | `PASS` |
| OpenAPI | 52 `/api/v1` path templates / 60 operations; API #89 response/error statuses are registered. | `PASS` |
| DD package | 15 Markdown files; 12/12 template appendix tails match byte-for-byte; 3 JSON examples parse; 47 tables / 509 data rows have consistent widths; 59 local links/anchors resolve; fences, whitespace and final newlines pass. Package fingerprint: `9095d00bfda986b86bf12d7741ce51928f7c3922873c658ca548cc847b8af4e6`. | `PASS` |
| Context manifest JSON/source paths | Valid JSON; six #89 module/test paths are in both registered arrays (62 tracked roots / 336 required source paths). | `PASS` |
| `git diff --check` | Passed. | `PASS` |
| Deno context validator | `deno run -A scripts/validate-agent-context.mjs --skip-drift` reports missing `.agents/db-admin/` context and `apps/db-admin-*` sources from the separate db-admin scope. No `server-study` or API #89 path errors were reported. | `BASELINE_SCOPE_FAILURE` |

Fake-session tests do not verify live schema/migration deployment, database grants, PostgreSQL row-lock/FK behavior or fine-grained AC-35 authorization policy. The Deno validator's unrelated db-admin inventory gap remains outside this task's `server-study` scope.

## HANDOFF

- API #89 is complete locally; its contract proposals remain Draft and require owner confirmation.
- API #90 is the next task in the requested API #48–#103 sequence.
- No live DB, migration, deployment, staging or commit operation was performed.
