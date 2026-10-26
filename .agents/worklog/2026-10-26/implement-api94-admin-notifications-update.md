---
task_id: "2026-10-26-implement-api94-admin-notifications-update"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-36 APIs #92–#96, especially #93 and #95–#96"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #94 Admin notification update

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 87 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Reuse established Admin route, response projection, auth, and fake-session test conventions; preserve dirty files.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Keep SQL constants in `query.py`, orchestration/transaction in `view.py`, bind values, validate response before commit, and report schema as candidate rather than live fact.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Use shared ADMIN guard, exact catalog business errors, strict model validation, Vietnamese source comments/docstrings, and explicit DERIVED/open decisions.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-36 APIs #92–#96, especially #93 and #95–#96]
```

## EXPECTED_BEHAVIOR

- AC-36 diagram declares `PUT /api/v1/admin/notifications/{notification_id}`, Admin, required `notification_id:int64`, `ApiEnvelope<Notification>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and errors 401/403/404/422/500. The action is only “UPDATE Notification”; no request body, fields, eligibility rule, schedule behavior, or transaction is specified.
- API catalog likewise declares path-only input and `ApiEnvelope<Notification>` with the exact status/error set. Its prose references conditional draft/scheduled update but does not define payload or status values.
- Existing API #94 DD is `Draft — Needs Confirmation`, describes a proposed full replacement payload, and leaves runtime/schema unwired. It is not approved behavior.

## CURRENT_BEHAVIOR (pre-edit)

- API #94 route/module/test are absent. APIs #92 and #93 are wired on `/api/v1/admin/notifications`; current Study OpenAPI baseline is 54 path templates / 64 operations, so #94 is expected to add one path and operation.
- Shared `validate_current_user_request(..., role="ADMIN")` is the available role guard; AC-36's finer notification-management permission is not implemented/source-verified.
- Legacy checked-in DDL candidate has recipient-level BIGINT `notifications` rows with writable `title` and `content`; migration 009 adds recipient/channel `notification_deliveries` rows with `PUSH|EMAIL` and `QUEUED|SENT|FAILED`. It has no campaign, notification status, schedule, update timestamp, scheduler, or recipient association for campaign updates. V1-PILOT UUID tables are a distinct incompatible model.
- API #92 projects notification rows with delivery rows into shared `AdminNotificationResponse`; API #93 creates one legacy notification per explicit recipient and QUEUED outbox rows. Neither verifies a live database or resolves the Admin model.
- `DESIGN_CONTRACT_PATHS` includes the collection path but not the dynamic #94 path. API #95/#96 are not wired and do not provide a policy or aggregate bridge.
- Preserve all pre-existing dirty/untracked worktree contents; do not clean, stage, or commit.

## SOURCE_TRACE

```text
PUT /api/v1/admin/notifications/{notification_id}
  -> shared ADMIN JWT guard before parsing raw path/body
  -> validate signed BIGINT path and strict {title, content} fallback request
  -> lock one recipient-level notifications row, then its delivery rows
  -> missing notification -> 404; no delivery or any non-QUEUED delivery -> 422
  -> update only title/content; retain created_at, recipients and delivery channels
  -> project existing AdminNotificationResponse with QUEUED status and channel rows
  -> validate complete response, then commit; query/map/commit failure -> rollback + safe 500
  -> focused HTTP tests cover guard, validation, locking, mutation, projection and error paths
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| Request payload | Diagram/catalog declare path only; the DD's full body is unapproved. | `DISCREPANCY / DERIVED` | Use strict `{title, content}` because these are the only writable legacy notification fields; retain Draft status and document this as a local fallback. |
| Audience/channels/schedule | No campaign/recipient relation, channel field, schedule column, or scheduler exists in the compatible BIGINT candidate. | `SOURCE_REQUIRED / DERIVED` | Preserve existing recipient and delivery rows; reject unknown body fields; do not claim audience, channels, or schedule can be changed. |
| Editable lifecycle | Catalog prose says draft/scheduled; physical notification has no status and delivery outbox is the only lifecycle evidence. | `DISCREPANCY / DERIVED` | Permit only rows with at least one delivery and all rows `QUEUED`; map response status to existing `QUEUED`, never call it Draft/Scheduled. |
| Physical schema | Checked-in legacy DDL is a candidate; deployed schema is unknown. | `NOT_VERIFIED_HERE` | Use existing candidate tables only; no migration and no live-schema claim. |
| Permission | Diagram requires notification-management permission; available guard checks ADMIN role only. | `SOURCE_REQUIRED / DERIVED` | Use shared ADMIN guard and leave finer permission open in DD. |
| Response cardinality | Catalog says singular `Notification`; legacy grain is per recipient. | `DERIVED` | Return the addressed recipient-level row using shared #92 response model; preserve channels/status projection from outbox. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete source-order review already started: AC-36 diagram → legacy and V1-PILOT schemas/outbox → catalog → #94 DD → #92/#93 implementation/tests and #95/#96 boundary. Confirm current test locations, database helper semantics, macro-review row, and template appendix bytes.
2. Record this plan before source, test, DD, or context edits. Keep direct contract distinct from local DERIVED fallback and preserve all preexisting modifications.
3. Add `api_94_admin_notifications_update` models/validation with only `title` and `content`, nonblank values, 200-character title limit from candidate DDL, extra fields forbidden, and signed-int64 path validation. Reuse the #92 Admin notification response/envelope types where compatible.
4. Add SQL-only constants for locking the notification and delivery rows, updating only title/content, and reading back the existing row/outbox projection. Bind every SQL value.
5. Implement view orchestration with ADMIN check before parsing raw path/body; lock in stable order; reject missing, no-delivery, or non-QUEUED targets with catalog errors; build and validate response before commit; rollback safely on query, mapping, or commit failures; use `run_in_threadpool` at route boundary.
6. Register PUT route with exact catalog response codes and add `/api/v1/admin/notifications/{notification_id}` to middleware contract paths. Update linked #92/#93 OpenAPI operation-count assertions and add #94 OpenAPI checks.
7. Add focused HTTP tests for auth precedence/role, path/body validation, forbidden fields, missing/ineligible resources, SQL bindings/lock order, recipient/channel preservation, response projection, rollback/error paths, trace, and OpenAPI.
8. Update API #94 DD to describe only this local fallback and its exact evidence; retain `Draft — Needs Confirmation`, unresolved audience/scheduling/permission/schema questions, and all eight standard template appendix suffixes. Update PLAN_RESULT/VERIFICATION_REPORT and AC-36 macro-review; do not present derived behavior as owner approval.
9. Update directly affected `.agents/server-study` routes, architecture, runtime, database-security, database, module, tests and workflow pages, project source-status, and context manifest. Record final path/operation and test counts from current source. Run context validator using available Deno path and record out-of-scope baseline errors accurately.
10. Run focused #94 tests, linked #92–#94 regressions, full Study Server suite, Ruff, OpenAPI/source/DD checks, `git diff --check`, and final worktree review. Do not stage or commit.

## CHANGES

- Files changed: Added API #94 module and HTTP tests; wired PUT route and middleware path; updated #92/#93 OpenAPI count assertions; revised 12-file DD package and AC-36 macro-review; updated server-study context/manifest and this worklog.
- CONTEXT_UPDATES: recorded API #94 route/module/auth/schema/test boundaries, 55/65 OpenAPI counts, and the 1263-test Study result.
- Context pages changed: `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`, `.agents/project/source-status.md`, `.agents/context-manifest.json`.
- Assumptions: fallback is DERIVED from the only compatible writable columns and delivery outbox; it is not approval of the DD's proposed body or lifecycle semantics. Existing dirty/untracked files were preserved; nothing was staged or committed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Deno coding worklog selector and review | 87 available; #74/#75/#76 selected and read; shortage none. | `VERIFIED_PREFLIGHT` |
| `.venv/bin/pytest -q tests/modules/admin/api_94_admin_notifications_update/test_admin_notifications_update.py` | 20 passed. | `VERIFIED_LOCAL_HTTP_TESTS` |
| `.venv/bin/pytest -q tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_93_admin_notifications_create tests/modules/admin/api_94_admin_notifications_update` | 66 passed. | `VERIFIED_LINKED_HTTP_TESTS` |
| `.venv/bin/pytest -q` | 1263 passed; one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_TESTS` |
| `.venv/bin/ruff check app tests` and scoped `ruff format --check ...` | All checks passed; 10 scoped files already formatted. | `VERIFIED_STATIC` |
| API #94 OpenAPI test | 55 `/api/v1` paths / 65 operations; exact 200/401/403/404/422/500 and strict DERIVED body. | `VERIFIED_LOCAL_SOURCE` |
| DD package static check | 12 Markdown files; 2 JSON examples parse; local links/anchors, fences, whitespace and front matter pass; all 9 sheet appendix suffixes match templates. | `VERIFIED_STATIC` |
| `git diff --check` | No whitespace errors. | `VERIFIED_STATIC` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Study context passed; validator reports only pre-existing missing DB Admin scope files/roots/links outside this task. | `BASELINE_FAIL_OUT_OF_SCOPE` |

## LIMITATIONS

- Checked-in DDL and fake-session tests cannot establish deployed schema, grants, runtime, fine-grained notification permission, scheduling, or provider delivery.
- All fallback payload and QUEUED editability rules remain DERIVED pending owner approval; DD stays Draft.

## HANDOFF

- Remaining blockers: owner confirmation of API #94 payload, target model/grain, editable-state policy, schedule/audience mutation, and fine-grained permission. These do not block the local DERIVED fallback implementation.
- Next owner/action: review the Draft DD and decide whether to approve or replace the local fallback.
