---
task_id: "2026-10-26-implement-api90-admin-quizzes-delete"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #90 Admin quiz delete

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 83 available; selected three; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN auth before raw path parsing; preserve extensive dirty worktree; checked-in legacy schema and fake DB tests are not live DB evidence.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` is SQL constants only; `view.py` owns transaction and response mapping; keep business boundaries exact.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Shared ADMIN guard does not prove AC-specific permission; derived body/status/schema decisions remain Draft; atomic transaction and validation before commit.
- Additional direct dependencies reviewed: API #90 DD authoring worklog, API #87–#89 and #86 delete source/DD, AC-35 and AC-16 diagram nodes, legacy/V1-PILOT schema candidates, API #29 DD boundary.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Source precedence followed: AC-35 diagram → infrastructure/schema → API catalog.
- AC-35 direct flow selects `DELETE /api/v1/admin/quizzes/{quiz_id}` and says “Soft delete nếu đã có attempts”; it does not define the no-attempt branch or physical tombstone.
- Catalog #90: Admin Bearer JWT; required `quiz_id:int64` path; no body/query; HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>`; exact errors 401/403/404/422/500 and their catalog business codes.
- Existing API #90 DD is `Draft — Needs Confirmation`; it proposes `DELETED` + `updated_at` for the soft branch and child-first hard deletion only when no history exists. These remain DERIVED, not owner-approved.

## CURRENT_BEHAVIOR (pre-edit)

- API #90 has no route/module/tests. API #89 already wires `PUT /api/v1/admin/quizzes/{quiz_id}`; `/api/v1/admin/quizzes/{quiz_id}` is already in `DESIGN_CONTRACT_PATHS`, so DELETE can share the existing path template without a middleware change.
- Shared `validate_current_user_request(..., role="ADMIN")` exists and is used before raw input parsing by #89. A separate AC-35 quiz-management permission policy is not source-backed.
- API #87 excludes `status='DELETED'`; API #89 rejects tombstones and attempt/answer history. API #86/#77 use `status='DELETED'` plus `updated_at` as local delete candidates. These do not approve quiz deletion policy.
- Checked-in legacy BIGINT DDL defines `quizzes`, `quiz_questions`, `quiz_choices`, `quiz_attempts`, and `quiz_answers`, but has no `deleted_at` or explicit `ON DELETE CASCADE`; FK columns in DDL are nullable. V1-PILOT uses a separate UUID/versioned assessments model. Neither proves live schema/deployment.
- AC-16/API #29 create-attempt source is unwired; its DD leaves quiz-open state, identity mapping, transaction and concurrency unresolved. API #30–#32 and #91 depend on retained history.
- Existing worktree is extensively dirty (605 status entries at checkpoint); preserve it, do not clean, stage, or commit.

## SOURCE_TRACE

```text
DELETE raw route
  -> shared ADMIN JWT guard before path parse or DB
  -> parse positive signed-int64 quiz_id; invalid -> catalog 422
  -> SELECT quiz row FOR UPDATE, including tombstone state; missing -> 404
  -> if existing DELETED tombstone: preserve timestamp, build DeleteResult, commit no-op
  -> lock questions then choices in the same order as API #89
  -> EXISTS attempt or answer rows linked through this quiz's questions/choices
  -> if history exists: UPDATE quiz status=DELETED + updated_at, retain question/choice/attempt/answer rows
  -> if no history: DELETE choices -> questions -> quiz in one transaction; capture DB operation timestamp for hard-delete result
  -> validate every returned identity/result and DeleteResult before commit
  -> query/projection/commit error rolls back and maps to safe catalog 500
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned local handling |
|---|---|---|---|
| No-attempt behavior | Diagram explicitly says soft-delete when attempts exist; no alternate branch. Legacy FK chain has no declared cascade. | `DERIVED` | Propose child-first hard delete only when no attempt/answer reference exists; keep DD Draft. |
| Tombstone and timestamp | Legacy Quiz has `status` and required `updated_at`, no `deleted_at`; #87/#89 already use the candidate `DELETED` marker. | `DERIVED / NOT_VERIFIED_HERE` | On history branch set `status='DELETED'`, DB `updated_at`, and map to `deleted_at`; live schema/owner approval remain open. |
| Answer references without attempts | DDL allows nullable attempt/question/choice FKs; #89 protects any attempt or answer reference to child IDs. | `DERIVED` | Treat any attached answer as history and preserve the quiz rather than delete referenced children; document this protective fallback. |
| Repeat DELETE | No direct repeat-delete rule; existing DD proposes soft-tombstone no-op. | `DERIVED` | Existing tombstone returns the same stored timestamp with 200 and no mutation; hard-deleted ID returns catalog 404. |
| API #29 race | AC-16 #29 is unwired and its status/lock policy is unresolved; legacy attempt FK can serialize a concurrent insert with parent `FOR UPDATE`. | `SOURCE_REQUIRED / DERIVED LOCK` | Lock quiz before history check and all mutations; document future #29 must reject tombstoned quizzes under a compatible transaction/lock. No 409 is added. |
| Fine-grained authorization | Catalog/AC-35 mention quiz-management permission; current runtime has only shared ADMIN guard. | `SOURCE_REQUIRED` | Enforce shared ADMIN before parsing/DB; do not claim dedicated permission. |
| Live schema | Legacy BIGINT and V1-PILOT UUID models differ; no live metadata checked. | `NOT_VERIFIED_HERE` | Target only legacy candidate; no DDL/migration change. |
| Error helper | Current helper emits error `data:null`; #90 DD incorrectly says `{}`. | `DISCREPANCY` | Follow current helper and correct DD. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Read and trace AC-35 DELETE node/edges; inspect legacy/V1-PILOT relations, constraints and timestamps; then verify exact API #90 catalog row and `DeleteResult`. Read the linked #86/#77 deletion patterns, #87/#89 quiz status/history behavior and AC-16/API #29–#32 boundary. Keep direct and DERIVED evidence separate.
2. Record this worklog's source trace and implementation plan before runtime/DD/context edits. Preserve every pre-existing dirty worktree change.
3. Add `admin/api_90_admin_quizzes_delete/` with declarative strict `DeleteResult`/success envelope models, SQL-only query constants, ADMIN/raw path validation, and `view.py` transaction orchestration. Use no request body and no new schema/migration.
4. Query plan: lock the Quiz row by ID without filtering tombstones; lock current questions then choices by stable ID order; check attempts plus answers linked to those child IDs; in the no-history branch delete choices, questions, then parent with `RETURNING` validation. Use bound parameters throughout.
5. Implement one transaction: ADMIN first; malformed positive signed-int64 -> catalog 422; missing quiz -> 404; existing tombstone -> no-op result with stored timestamp; any history -> soft tombstone preserving all history; otherwise ordered hard delete; validate response before commit. Roll back all post-lock failures and use only catalog 401/403/404/422/500 codes.
6. Wire raw `DELETE /admin/quizzes/{quiz_id}` in `app/api/v1.py`, with path/auth metadata, no body, HTTP 200 and exact catalog errors. Reuse the existing dynamic middleware template registered by #89.
7. Add focused HTTP tests for ADMIN-before-parse/DB, signed-int64 bounds, no body, missing/tombstone/repeat behavior, attempt/answer history, child-first hard delete, returned-ID mismatch, safe rollback on query/projection/commit failure, envelope/trace and OpenAPI.
8. Update all API #90 DD sheets/reports to reflect current wiring and tests, correct stale ADMIN/path/error-envelope claims, preserve all 11 sheet appendix tails, retain `Draft — Needs Confirmation`, and document DERIVED behavior plus #29 race limitations. Do not edit API #29, catalog, diagram or schema.
9. Update `.agents/server-study` route/architecture/runtime/security/database/module/test/workflow pages, project source status, and context manifest for the six API #90 source/test paths. Update current path/operation/test counts from actual verification.
10. Run focused API #90 tests; linked #87–#90 and #86 regression; full Study suite; Ruff; OpenAPI/import; DD static/template/link/example checks; `git diff --check`; and the Deno context validator. Explicitly separate the known db-admin inventory failure from Study results.
11. Review final scoped diff and Git status; preserve all prior work, and do not stage or commit.

## PRE-CODE CHECKPOINT

- Root/global router and context map loaded; `server-study` entry/index plus worklog contract, module/workflow/test context pages reviewed.
- Deno selector returned 83 coding logs and selected #74/#75/#76; all three were read fully; shortage none.
- Read AC-35 #90 path/soft-delete branch and edges, AC-16 attempt-create flow, legacy Quiz/attempt/answer DDL, V1-PILOT UUID assessment contrast, API catalog #90, API #90 DD and its prior authoring worklog, plus API #86/#77 delete and #87–#89 quiz source/DD.
- Confirmed route/module/test are absent, while shared ADMIN guard and dynamic path template are present after API #89. Current response helper serializes error `data` as `null`.
- Plan recorded before any API #90 code/DD/context edit. No API #90 source edit has been made yet.

## CHANGES

- Runtime: wired `DELETE /api/v1/admin/quizzes/{quiz_id}` and added the `api_90_admin_quizzes_delete` model/query/validate/view module. Shared ADMIN auth precedes raw positive signed-int64 parsing and DB access. The transaction locks Quiz → questions → choices, checks attempts and linked answers, chooses soft preservation or child-first hard delete, validates returned IDs/response, and commits or rolls back.
- Tests: added `tests/modules/admin/api_90_admin_quizzes_delete/test_admin_quizzes_delete.py` with 18 HTTP cases covering contract, policy branches, bounds, auth, response mapping and rollback.
- DD: updated all 11 template sheets and 3 report files under `apps/study-server/docs/dd/90_admin_quizzes_delete/`; retained Draft — Needs Confirmation and documented runtime status plus unresolved DERIVED choices.
- Context: updated Study route, architecture, runtime, database/security, module, test and workflow pages, project source status, and both API90 source-path registries in `.agents/context-manifest.json`.
- No schema, migration, catalog, diagram, staging or commit changes. Preserved the pre-existing dirty worktree.
- Assumptions: no-attempt hard delete, tombstone marker/time, repeat-delete behavior, answer-only history protection and lock ordering are DERIVED; API #29 race and fine-grained permission remain unresolved.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Context/worklog preflight | Deno selector chose #74–#76; all three read; shortage none. | `VERIFIED_PREFLIGHT` |
| API #90 focused tests | `.venv/bin/pytest tests/modules/admin/api_90_admin_quizzes_delete/test_admin_quizzes_delete.py -q` — 18 passed. System Python has no pytest; Study virtualenv used. | `VERIFIED_LOCAL_HTTP` |
| Linked regression | API #86–#90 focused modules — 100 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED_LOCAL_HTTP` |
| Full Study suite | `.venv/bin/pytest -q` — 1178 passed, one upstream Starlette/httpx deprecation warning, 160.22 seconds. | `VERIFIED_LOCAL_HTTP` |
| Ruff | `.venv/bin/ruff check app tests` passed. API #90 module/test files and modified `app/api/v1.py` pass targeted Ruff format check. Broad `ruff format --check app tests` reports 60 files would be reformatted; no broad formatting was applied outside scope. | `VERIFIED_SCOPED` |
| OpenAPI | 52 unique `/api/v1` path templates / 61 operations; DELETE shares the #89 path template and has no request body/query. | `VERIFIED_LOCAL_SCHEMA` |
| API #90 DD static check | 14 Markdown files; 11/11 template appendix suffixes preserved; JSON examples, local links, table widths, code fences, final newlines and whitespace pass. | `VERIFIED_STATIC` |
| Context validator | `deno run -A scripts/validate-agent-context.mjs --skip-drift` reports only pre-existing missing `db-admin` pages/source roots/links; no `server-study` or API #90 finding. | `BLOCKED_BY_UNRELATED_SCOPE` |
| Diff check | `git diff --check` passes. Fake DB HTTP tests do not verify live PostgreSQL/schema/migrations/deployment. | `VERIFIED_LOCAL` |

## HANDOFF

- Remaining owner decisions: approve hard delete without history, `DELETED`/timestamp mapping, answer-only preservation and repeat-delete semantics, API #29 coordination and fine-grained AC-35 permission; keep DD `Draft — Needs Confirmation`.
- Status: API #90 implementation and local verification are complete; no live DB/deployment claim is made. Next API in the active sequence is #91.
