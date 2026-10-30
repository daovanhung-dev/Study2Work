---
task_id: "2026-10-26-implement-api95-admin-notifications-delete"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-36 APIs #92–#96; #93 recipient/outbox creation, #94 editability locks, #96 status projection"]
status: "VERIFIED"
---

# Worklog: Implement API #95 Admin notification delete/cancel

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 88 coding worklogs available; 3 selected; shortage `none`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve exact catalog response/input shape, strict raw path parsing and the shared ADMIN guard before data lookup.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Keep view orchestration separate from SQL-only query constants; commit only after validating the complete response projection.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Preserve user worktree changes; distinguish a source-backed fallback from owner-approved business policy and record unresolved status in DD/context.
  - path: `.agents/worklog/2026-10-26/implement-api94-admin-notifications-update.md`
    - carry_forward: Lock the legacy BIGINT notification parent before its delivery rows, require valid outbox projections, use shared `ADMIN` auth and keep live schema/provider behavior unverified.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement API #95 `DELETE /api/v1/admin/notifications/{notification_id}` from its DD while preserving exact method, Bearer/Admin role, positive int64 path, no body/query, HTTP 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>` and catalog 401/403/404/422/500 errors.
- Canonical contract/approved DD: Catalog #95 and AC-36 diagram are direct sources. The DD remains `Draft — Needs Confirmation`; lifecycle, storage and scheduler rules are not approved. Apply the server-study coding fallback convention and label any local lifecycle rule `DERIVED`.
- Cross-API boundary: #93 writes one legacy notification per recipient and one `QUEUED` outbox row per channel; #94 locks notification then delivery rows and permits text edits only when all deliveries are `QUEUED`; #96 returns Notification without a delivery aggregate. #95 addresses only the path-selected notification row, not every row sharing a derived `operation_id`.

## CURRENT_BEHAVIOR

- Source/config: AC-36 has a `DELETE/mark cancelled` node followed by management reload. Legacy `DB.sql` and migration 009 define BIGINT `notifications` and `notification_deliveries`, with an `ON DELETE CASCADE` FK and statuses `QUEUED`, `SENT`, `FAILED`; notifications have no lifecycle/tombstone/deleted timestamp. V1-PILOT UUID tables are a different model.
- Runnable tests before changes: #92–#94 focused fake-DB HTTP tests; #94 follows parent-then-delivery locking. API #95 had no module, route or tests. Existing API #90 demonstrates int64 validation, rollback and DeleteResult timestamp mapping.
- Runtime wiring after changes: `app/api/v1.py` wires #92–#95 (55 paths / 66 operations). API #95 tests use fake DB projections. No Study-side scheduler/provider cancellation worker was found; local source does not establish live DB schema or deployment.

## SOURCE_TRACE

```text
Planned DELETE route in app/api/v1.py
  -> API #95 view: shared ADMIN guard, then signed-int64 path validation
  -> query.py SQL constants: lock notifications parent, lock its delivery rows in stable channel order, inspect status, DELETE parent with RETURNING
  -> legacy FK ON DELETE CASCADE removes that notification's outbox rows in the same DB transaction
  -> validate required DeleteResult projection, build success envelope, then commit
  -> fake-DB route tests: auth/validation/not-found/eligibility/success/rollback/OpenAPI
```

Existing current path: API #94 route -> update view -> shared ADMIN guard and raw validation -> parent/delivery locks -> title/content update -> Notification response -> API #94 fake-DB tests.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Physical lifecycle | Catalog says draft delete/cancel conditionally; AC-36 says `DELETE/mark cancelled`; legacy DDL has no status/tombstone, but has a cascading delivery FK | `DISCREPANCY`; use hard delete of a path-selected legacy row only as a clearly labeled `DERIVED` local fallback | Do not claim owner-approved lifecycle or preserve removed delivery rows |
| Delete eligibility | Current #93 creates one or more `QUEUED` outbox rows; DDL status check has `QUEUED/SENT/FAILED`; no scheduler/worker contract is present | `DERIVED`: permit only when at least one valid delivery exists and all are `QUEUED`; otherwise return catalog 422 | This is a conservative local gate, not proof a provider call was not started |
| External cancellation | AC-36 says cancel; no scheduler/provider API/worker found | `SOURCE_REQUIRED / NOT_FOUND` | Return does not confirm external job/provider cancellation |
| DeleteResult timestamp | Reusable schema requires `deleted_at`; hard DELETE can return DB `CURRENT_TIMESTAMP` with deleted row | `DERIVED` mapping, following API #90 precedent | Timestamp is transaction DB time, not a persistent tombstone |
| Retry semantics | Physical row and cascading deliveries are removed; no tombstone | `DERIVED`: repeat request after deletion returns catalog 404 | No idempotency key/soft-delete behavior is sourced |
| Fine-grained permission | Catalog role Admin; AC-36 asks for notification-management permission; source has shared ADMIN guard only | `SOURCE_REQUIRED`; use shared ADMIN fallback consistently with #92–#94 | Does not prove dedicated permission enforcement |

## CHANGES

- Files changed: API route and the five-file `api_95_admin_notifications_delete` module; #95 tests; linked #92–#94 OpenAPI-count assertions; API #95 DD, #92–#94 current AC-36 status notes and #92–#96 macro-review; server-study context pages, project source status and context manifest.
- CONTEXT_UPDATES: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`, and `.agents/context-manifest.json` updated to #95 / 55 paths / 66 operations / 1284 tests.
- Plan execution: all seven pre-code steps completed. No catalog, DDL or diagram changes; no staging/commit.
- Assumptions: local fallback is deliberately DERIVED and uses current legacy BIGINT + outbox behavior because they are the only model implemented by #93/#94. It affects one recipient row. It does not establish scheduler cancellation, live schema, external provider state, owner approval, or fine-grained permission.
- CONTEXT_UPDATES: planned for Study server route/module/database/test pages, project source status, context manifest and AC-36 macro-review after source verification.
- Context pages changed: none yet.
- Assumptions: the local fallback is deliberately DERIVED and uses current legacy BIGINT + outbox behavior because they are the only model implemented by #93/#94. It affects one notification recipient row only. It does not establish scheduler cancellation, live schema, external provider state, owner approval, or fine-grained permission.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` | 88 available, three selected and reviewed; no shortage | PASS — preflight |
| AC-36 diagram parse, catalog #95, legacy DDL/migration 009, #93/#94 code/tests, #90 DELETE precedent | Confirmed exact API/error contract, recipient-row/outbox candidate, cascade FK and absence of scheduler source | PASS — source review |
| `.venv/bin/pytest -q tests/modules/admin/api_95_admin_notifications_delete/test_admin_notifications_delete.py` | 21 passed after formatting; one upstream Starlette/httpx warning | PASS |
| `.venv/bin/pytest -q tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_93_admin_notifications_create tests/modules/admin/api_94_admin_notifications_update tests/modules/admin/api_95_admin_notifications_delete` | 87 passed; one upstream Starlette/httpx warning | PASS |
| `.venv/bin/pytest -q` | 1284 passed; one upstream Starlette/httpx warning | PASS (run before formatting-only cleanup; API #95 focused suite rerun afterward) |
| `.venv/bin/ruff check app tests` | All checks passed | PASS |
| Scoped `.venv/bin/ruff format --check ...` for route/module and linked #92–#95 tests | 10 files already formatted | PASS |
| `.venv/bin/ruff format --check app tests` | 62 files would be reformatted before scoped cleanup; unrelated pre-existing files left untouched | NOT CLEAN — repository-wide baseline |
| API #95 OpenAPI test | Direct errors/body/path/schema and 55 paths / 66 operations | PASS |
| DD static audit | 12 files; 9/9 template appendix suffixes byte-identical; 9/9 front matter; 1 JSON example; tables/fences and 33 local links/anchors pass | PASS |
| `git diff --check` | No whitespace errors after removing trailing blank lines in three DD reports | PASS |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_INVALID`; all reported failures are existing missing db-admin pages/source roots/contracts outside server-study; no Study issue reported | PARTIAL — repository baseline |

## HANDOFF

- Remaining decisions: owner confirmation of lifecycle/retention, queued-only rule, live Admin schema, dedicated permission, scheduler/worker coordination and idempotency. These do not block the locally tested fallback and remain visible in the Draft DD.
- Next task: API #96; preserve the current DERIVED boundary and existing worktree state.
