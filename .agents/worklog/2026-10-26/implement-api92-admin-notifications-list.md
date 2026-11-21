---
task_id: "2026-10-26-implement-api92-admin-notifications-list"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #92 Admin notification list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 85 available; selected and read all 3; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve dirty files; query.py is SQL constants only; views own orchestration; checked-in schema/fake DB tests do not prove live availability.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Separate expected contract from derived body/projection choices; reuse shared Admin guard and current runtime conventions.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Bind SQL values; preserve DERIVED boundaries and Draft DD status; do not mix legacy BIGINT with V1-PILOT UUID schema.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

Logical linked boundary reviewed in-scope: AC-36 APIs #92–#96 and Mentor notification APIs #63–#64. No other project scope is required.

## EXPECTED_BEHAVIOR

- Direct catalog contract: `GET /api/v1/admin/notifications`; Bearer JWT/Admin; optional `status:string`, `channel:string`, `page:int32`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Notification>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable `Notification`: required `id:int64`, `title:string`, `content:string`, `channels:NotificationChannel[]`, `status:NotificationStatus`, `created_at:date-time`; optional `read_at` and `scheduled_at`.
- AC-36 diagram: Admin with notification-management permission opens management, calls #92 to query notifications, then chooses #93 create/send, #94 update, #95 delete/cancel, or #96 status. It does not define list response cardinality, query predicate, sorting, page size or a physical campaign model.
- Project conflict priority: diagram → infra/schema → API catalog → simplest clear fallback. Keep direct catalog facts and implementation fallbacks distinct; do not change catalog/diagram/schema without approval.

## CURRENT_BEHAVIOR (pre-edit)

- Current Study app composes 53 `/api/v1` templates and 62 operations; full suite checkpoint is 1197 passed. API #92 has no route/module/test, and `/api/v1/admin/notifications` is absent from `DESIGN_CONTRACT_PATHS`.
- Shared guard `validate_current_user_request(..., role="ADMIN")` is used by Admin APIs #68–#91; there is no source-backed notification-management permission policy.
- Legacy candidate `notifications` is BIGINT and has `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at`, and migration-009 `operation_id`. Migration 009 / checked-in `DB.sql` add BIGINT `notification_deliveries` with one row per notification/channel and `PUSH|EMAIL`, `QUEUED|SENT|FAILED`, queued/update timestamps. None proves live schema or worker execution.
- V1-PILOT notifications/deliveries use UUID, learner grain, `body`, `read_at`, `expires_at`, and different channels/status model; not interchangeable with the Admin int64 contract.
- API #63 creates one legacy notification per recipient, shared `operation_id` per dispatch batch, and one delivery row per channel. API #64 derives one dispatch status from outbox rows with precedence QUEUED, FAILED, SENT and checks Mentor sender ownership; that ownership rule is not transferred to Admin.
- AC-36 macro-review #92–#96 is `VERIFIED_WITH_OPEN_QUESTIONS`: list cardinality/schema/status-channel projection, permission, global scope and #93 Operation bridge remain unresolved. API #93–#96 DDs remain Draft.
- Worktree has 625 changed/untracked entries on branch `develop`, including prior API implementations and context changes. Preserve all; no cleanup/staging/commit.

## SOURCE_TRACE

```text
GET #92 raw query/header -> shared ADMIN Bearer/JWT guard -> validate optional page as positive signed-int32 -> read count + one deterministic 20-row page from checked-in legacy BIGINT notification/outbox candidates -> aggregate outbox channel/status per notification row -> map Notification items + PageMeta -> 200 DESIGN_RESOURCE_RETRIEVED
```

No write, commit, or provider call. Query/response/cardinality/status aggregation and global visibility are implementation fallbacks, not approved AC-36 semantics.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Local handling |
|---|---|---|---|
| List cardinality | Endpoint/name and `page` plus diagram's “Query notifications” imply collection; catalog directly returns one `Notification`. | `DISCREPANCY / DERIVED_FALLBACK` | Return `Page<Notification>`; keep catalog and DD Draft. |
| Legacy vs pilot model | Legacy BIGINT row plus #63 outbox fit int64 ID and channel/status; pilot model is UUID/learner-grain and incompatible. | `DERIVED / NOT_VERIFIED_HERE` | Query legacy candidates only; no schema change/live claim. |
| Notification grain/global visibility | Legacy rows are recipient-specific; no Admin campaign or tenant relation/policy is approved. | `SOURCE_REQUIRED / DERIVED_FALLBACK` | One result per legacy notification row with outbox; shared ADMIN sees those rows. Do not expose recipient/sender IDs. |
| `channels` and `status` | Legacy base row lacks both; #63 outbox stores channel/status; #64 has an explicit local aggregate precedence. | `DERIVED` | Aggregate existing outbox per notification; channels use stored order `channel ASC`; status uses #64 precedence. These are not owner-approved Notification enum rules. |
| `read_at` / `scheduled_at` | Legacy only has boolean `is_read`; neither timestamp exists. Both fields are optional in Notification. | `SOURCE_REQUIRED` | Omit both; never convert `is_read` to a timestamp or `expires_at` to scheduled time. |
| Filters | Catalog names only; enum values and semantics unspecified. | `DERIVED` | Exact status comparison against local aggregate; exact channel membership. No normalization/allowlist. |
| Pagination | Query has page only; no response PageMeta/size/sort. API #43 and other Study lists use fixed 20. | `DERIVED` | Page defaults to 1; fixed size 20; order `created_at DESC, id DESC`; empty/out-of-range page is 200 with `items: []`. |
| Admin permission | AC-36 asks notification-management permission; current guard only has role ADMIN. | `DERIVED / SOURCE_REQUIRED` | Use shared ADMIN role before query parsing/DB; fine-grained permission remains open. |
| 422 and 503 | Catalog errors list no 422 but page is int32; catalog includes 503 with no trigger. | `DISCREPANCY / DERIVED` | Invalid page returns 422 validation; SQL connection-unavailable returns 503, other SQL/mapping failures 500. |
| #93 bridge | Catalog/diagram #93 return Notification while operation prose says Operation. | `DISCREPANCY` | Do not infer or expose `operation_id`; leave the group issue open. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Load the registered `createDD-markdown` skill and verify all eight canonical template files/hashes; retain Study's Markdown-only delivery rule and existing #92 template appendices.
2. Before source edits, create this worklog with the complete expected/current trace and explicit fallback plan.
3. Add only API #92 module files: declarative notification/query/page/envelope models; SQL constants for matching count and list using a grouped delivery CTE; input validator that authenticates ADMIN before parsing `page`; view that owns DB calls, projection validation, rollback/error mapping, and the read-only response.
4. Use the checked-in legacy `notifications` + migration-009 `notification_deliveries` candidate. Require at least one delivery row to provide required `channels` and `status`; never select `user_id`, `sender_id`, `type`, `is_read`, or UUID pilot fields into response. Aggregate delivery state by the tested #64 precedence; bind exact optional status/channel filters and pagination parameters.
5. Wire `GET /admin/notifications` in `app/api/v1.py` using raw Request query/header values so ADMIN auth precedes custom parsing; add the fixed path to `DESIGN_CONTRACT_PATHS`; declare catalog response/errors plus clearly marked DERIVED 422 and Page schema in OpenAPI.
6. Add focused HTTP tests for Admin auth/role ordering, default/page/filter behavior, mapping/empty rows, malformed count/rows/channels/status, SQL failure→500/503, read-only behavior, trace/envelope, exact route and OpenAPI.
7. Update only directly affected #92 DD sheets/report, keeping all template appendix suffixes unchanged and status `Draft — Needs Confirmation`; document implementation vs direct catalog discrepancies and retain AC-36 macro-review open decisions. Update relevant server-study context pages, project source-status, context manifest and worklog counts/source paths.
8. Verify focused API #92 tests, linked #63/#64/#87 regression, full Study suite, Ruff, OpenAPI route/schema/errors, DD static/template/link/JSON checks, manifest/context validator (using documented Deno fallback if Node is unavailable), and `git diff --check`.
9. Review the scoped diff and preserve all prior worktree changes; do not stage or commit.

## PRE-CODE CHECKPOINT

- Read root and global routing instructions, `.agents/context-map.md`, scope AGENTS/INDEX, workflow/route/runtime/database/security/architecture/module/test context and all three selected coding worklogs.
- Read the full registered Markdown skill and all eight template files; template set is complete. Hashes were computed for all eight.
- Read AC-36 index and diagram node/flow, catalog rows #92–#96 and Notification/Page/Operation schemas, legacy and V1-PILOT DDL, migration 009, DB guide/ERD, #92 DD and #92 pre-existing docs worklog, AC-36 macro-review and linked #93/#96 boundaries, #63/#64 implementation, Admin list #87 and its HTTP test pattern, router/middleware/DB/response helpers.
- The above implementation plan is recorded before code edits. No runtime, test, DD, schema, catalog or context source file has been changed at this checkpoint.

## IMPLEMENTATION_RESULT

- Added `app/modules/admin/api_92_admin_notifications_list/` with declarative contracts, ADMIN-first validation, SQL-only query constants and view-owned query/mapping/error orchestration.
- Wired `GET /api/v1/admin/notifications` in `app/api/v1.py` and added its path to `DESIGN_CONTRACT_PATHS`. The runtime fallback returns `Page<Notification>` from legacy BIGINT notification rows with delivery aggregates; page shape, fixed size/order, status/channel projections, global ADMIN visibility, 422 and DB-connectivity→503 remain DERIVED. No catalog, diagram, schema or migration was changed.
- Added 20 HTTP tests. Updated the #92 Markdown DD/report and AC-36 macro-review row while retaining `Draft — Needs Confirmation`, preserved all eight template appendix suffixes byte-for-byte, and updated the directly affected server-study context/source-status/manifest pages.
- No staging, commit, cleanup or unrelated-scope change was performed.

## VERIFICATION

- API #92 focused HTTP tests: `20 passed`.
- Linked API #63/#64/#87/#92 regression: `85 passed`.
- Full Study suite: `1217 passed` with one upstream Starlette/httpx `TestClient` deprecation warning.
- `ruff check app tests`: passed; scoped `ruff format --check`: 8 files already formatted.
- OpenAPI assertion in API #92 tests: 54 `/api/v1` path templates and 63 operations, with query and error schemas.
- DD static checks: 11 Markdown files, eight template appendix suffixes byte-identical, eight Draft front matters, three JSON examples parse, 33 Markdown tables / 449 table lines, five balanced code fences, 23 file/directory links and five anchors resolve, no trailing whitespace, all files end in newline. Template/output manifest fingerprints are recorded in `VERIFICATION_REPORT.md`.
- `.agents/context-manifest.json` parses as JSON. `git diff --check` passes.
- Ran `deno run -A scripts/validate-agent-context.mjs --skip-drift`; it exits `AGENT_CONTEXT_INVALID` on missing `db-admin` context/source roots and references in the current worktree (`.agents/db-admin/*`, `apps/db-admin-web`, `apps/db-admin-server`). No Study Server or API #92 validation errors were reported. Those unrelated context paths remain untouched.

## HANDOFF_LIMITS

The tests use fake DB sessions. Local DDL and source do not establish PostgreSQL behavior, live schema/migration deployment, outbox worker delivery, fine-grained notification permission, campaign grain or owner approval. The API #92 DD remains `Draft — Needs Confirmation`; AC-36 #92–#96 remains `VERIFIED_WITH_OPEN_QUESTIONS`.
