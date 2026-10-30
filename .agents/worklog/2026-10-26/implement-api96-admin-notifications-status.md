---
task_id: "2026-10-26-implement-api96-admin-notifications-status"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-36 APIs #92–#95; API #96 reads the delivery rows written/read by the connected notification endpoints"]
status: "VERIFIED"
---

# Worklog: Implement API #96 Admin notification delivery status

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 89 worklogs available; selected 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Trace direct contract and current source before edits; preserve dirty worktree; keep live database/deployment unverified.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Follow shared ADMIN authentication and SQL-only `query.py` / orchestration-owning `view.py` conventions; record discrepancies explicitly.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Keep implementation narrow, add focused and linked regression coverage, update scope context when source wiring changes.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: `GET /api/v1/admin/notifications/{notification_id}/status`, Bearer/Admin, required `notification_id:int64` path, no request body or query, success `200 DESIGN_RESOURCE_RETRIEVED` with `ApiEnvelope<Notification>`, exact errors 401/403/404/500.
- Canonical contract/approved DD: Catalog row #96 and AC-36 node `STATUS`; diagram explicitly runs “Đọc delivery aggregate” before “Reload notification management”. DD #96 is `Draft — Needs Confirmation`, with no approved physical Admin model or aggregate policy.
- User decision: choose the most reasonable/easy-to-understand implementation where DD gaps remain; clearly mark derived choices.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` has routes #92–#95 but no #96; middleware design-contract path set has `/admin/notifications` and `/admin/notifications/{notification_id}`, but no `/status` path. API #92 already reads legacy BIGINT `notifications` joined to `notification_deliveries`, projects `channels` and `status`, and excludes notifications without deliveries. API #64 similarly returns 404 when a status resource has no deliveries.
- Runnable tests: #92 tests cover Admin auth, list projection, read-only behavior and DB errors; #95 tests cover path handling and connected deletion. No focused API #96 tests exist.
- Runtime wiring: API #96 is `UNWIRED / NOT_FOUND`; checked-in DDL/migration are source candidates only and do not prove the deployed schema.

## SOURCE_TRACE

```text
GET route (new) -> shared ADMIN JWT guard -> raw positive signed-int64 path parser -> one SQL query for the notification plus its delivery aggregate -> validate/map the existing Notification schema -> success envelope or catalog 404/500 -> focused API #96 tests + linked #92–#95 regression
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `Notification` response vs diagram aggregate | Catalog requires `ApiEnvelope<Notification>`; AC-36 says read an aggregate; reusable delivery counts are not fields of `Notification`. | `DISCREPANCY` | Do not add counts or per-channel fields to the response. |
| Physical Admin notification schema | Legacy DDL and migration define BIGINT notifications/deliveries; #92–#95 already use these as a local fallback. Live schema is unknown. | `DERIVED / SOURCE_REQUIRED` | Reuse the current local model consistently, state that it is not owner-approved or deployed proof. |
| Aggregate-to-status projection | API #92 already applies `QUEUED` if any queued, else `FAILED` if any failed, else `SENT` when all deliveries are sent; #64 treats no deliveries as status-resource 404. | `DERIVED` | Reuse the current adjacent API fallback for #96; retain enum/priority and empty-state questions in DD. |
| Admin fine-grained permission | Catalog requires Admin; AC-36 precondition mentions notification-management permission, but current Study guard supports role ADMIN only. | `SOURCE_REQUIRED` | Use shared ADMIN guard and keep the finer permission unresolved. |
| Malformed path handling | Catalog error set excludes 422; API #64 maps malformed signed-int64 status ID to 404. | `DERIVED` | Keep #96 error set exact and map invalid/out-of-range path to 404 after auth. |

## IMPLEMENTATION_PLAN

1. Add an API #96 module with a SQL-only query constant selecting one notification ID and aggregating its delivery rows using the same precedence as API #92. Keep SQL to one read query; do not mutate or call a provider.
2. Reuse API #92's `AdminNotificationResponse` model so #96 emits only the existing Notification fields; add an exact success envelope for #96 and validate the mapped projection before returning it.
3. Add a raw positive signed-int64 parser; authenticate ADMIN first, then parse the path. Return 404 for malformed/out-of-range IDs and for absent notifications or notifications without deliveries; return safe 500 for query/projection errors. Do not add 422 or 503.
4. Wire the GET path in `app/api/v1.py` with only the direct contract's errors and path/header OpenAPI parameters; add the exact route template to `DESIGN_CONTRACT_PATHS` so framework validation stays in the catalog error envelope.
5. Add focused fake-DB tests for projection, all status branches, channel ordering, missing/no-delivery resources, invalid ID, auth-before-parse/query, malformed rows, DB failure and GET read-only behavior; extend contract/OpenAPI checks and run linked #92–#95 regression.
6. Update DD #96 to record this implementation as a local `DERIVED` fallback, preserve its direct contract, open questions, Draft status, and all eight source-workbook appendices. Update AC-36 macro-review, scope context/manifest, and this worklog with verified counts/results.
7. Run focused and linked tests, full Study Server tests, Ruff, OpenAPI count/contract inspection, DD static checks, diff checks, and `deno run -A scripts/validate-agent-context.mjs --skip-drift`; report live DB/deployment as unverified.

## CHANGES

- Files changed: API #96 module and route/middleware wiring; API #96 HTTP/OpenAPI tests; linked API #92/#93/#94/#95 path-count assertions; API #96 DD and AC-36 macro-review; Study Server context pages and source manifest.
- CONTEXT_UPDATES: refreshed current route/operation and full-test counts, module/runtime/security/database/test guidance, source-status and manifest registration for API #96.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`.
- Assumptions: user authorized a reasonable local fallback; existing API #92 projection is the nearest source-backed convention. Its status policy, legacy schema use, Admin permission granularity, and empty-delivery behavior remain `DERIVED`/`SOURCE_REQUIRED`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` | 89 available, 3 selected, no shortage | PASS — PREFLIGHT |
| Inspect #96 catalog, AC-36 diagram, legacy DDL/migration, API #92/#64/#95 source, router/middleware and nearby tests | Completed before implementation plan | PASS — SOURCE REVIEW |
| `.venv/bin/pytest -q tests/modules/admin/api_96_admin_notifications_status tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_94_admin_notifications_update tests/modules/admin/api_95_admin_notifications_delete` | 77 passed; includes #96 and linked read/update/delete but excludes #93 create | PASS — FOCUSED |
| `.venv/bin/pytest -q tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_93_admin_notifications_create tests/modules/admin/api_94_admin_notifications_update tests/modules/admin/api_95_admin_notifications_delete tests/modules/admin/api_96_admin_notifications_status` | 103 passed; full #92–#96 regression | PASS — LINKED |
| `.venv/bin/pytest -q` | 1300 passed; one upstream Starlette/httpx TestClient deprecation warning | PASS — FULL LOCAL SUITE |
| `.venv/bin/pytest -q tests/modules/admin/api_96_admin_notifications_status` | 16 passed after final OpenAPI response-schema/error-description assertions; production source unchanged since full suite | PASS — FINAL FOCUSED |
| `.venv/bin/ruff check app tests` and scoped `.venv/bin/ruff format --check ...` | All checks passed; 12 changed Python files already formatted | PASS — LINT/FORMAT |
| OpenAPI assertions in #96 and linked count tests | 56 `/api/v1` paths / 67 operations; #96 exact 200/401/403/404/500, no body/query | PASS — LOCAL CONTRACT |
| DD static check | 12 Markdown files; 8 appendix bodies match #49 after terminal-whitespace normalization; 2 JSON examples, 3 fences, 20 local links and whitespace pass | PASS — STATIC |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Exit 1 only for absent `.agents/db-admin/` and `apps/db-admin-*` entries; no Study/API #96 path errors | PARTIAL — OUT-OF-SCOPE BASELINE |
| Live database/deployment/provider | Not checked | NOT_CHECKED |

## HANDOFF

- Remaining blockers: none for local API #96; owner approval, fine-grained permission and live schema verification remain outstanding.
- Next owner/action: implement and verify API #96; then proceed to API #97 under the larger APIs #48–#103 goal.
