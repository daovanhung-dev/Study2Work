---
task_id: "2026-10-23-create-study-api44-dd"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Create Study API #44 DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Preserve the catalog contract and label unsupported inference `DERIVED`; AC-19's read/write flows remain separate, and a missing counter source must not become a fabricated update.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: The #39–#42 macro reconciliation uses explicit access boundaries and a singleton `Page<T>` only as `DERIVED`; missing response fields remain `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: AC-20 #43–#45 is a distinct notification group. API #43 recorded the recipient/read timestamp discrepancy and missing Notification response sources; recheck that gap against #44.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue the user's all-remaining-Study-API-DD goal with API #44 only in this session. Write the DD in Vietnamese, make a plan before authoring, inspect AC-20 carefully, use existing API DDs as precedent, then immediately validate the pack and the directly connected #43 read-state contract.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #44; AC-20 index and activity diagram; `notifications` DB guide/ERD/checked-in DDL; related API #43 DD and API #45 catalog/diagram branch; registered `createDD-markdown` skill and Study Markdown-only workflow.

## CURRENT_BEHAVIOR

- Source/config: No API #44 route/module/query match was found under `apps/study-server/app`; no notification-specific test or #44 DD folder exists. `app/utils/auth.py` has the current Student Bearer/JWT helper, but #44 does not call it. Notification DB guide/ERD/DDL define `notifications.user_id` nullable and `is_read BOOLEAN DEFAULT FALSE`; no physical `NotificationRecipient` or `read_at` exists. Live schema is unverified. `error_response()` currently serializes omitted/None `data` as `{}`, while API guidelines specify `null`.
- Runnable tests: Not run; docs-only task and no API #44 implementation/test exists.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #44.

## SOURCE_TRACE

```text
Student Bearer JWT -> notification_id path -> candidate atomic UPDATE notifications.is_read=TRUE WHERE id=:notification_id AND user_id=:principal_id -> RETURNING the updated notification projection -> ApiEnvelope<Page<Notification>> -> UI applies the one-item read change; later API #43 refresh must show synchronized state
```

The SQL, owner predicate, one-item page and UI update mapping below are `DERIVED` candidates, not current runtime behavior or approved SQL.

## PLAN BEFORE DD AUTHORING

### API Requirement Matrix

| API ID | Name | Method / endpoint | Actor / auth | Request field | Response / success | Errors |
|---|---|---|---|---|---|---|
| #44 | Đánh dấu một thông báo đã đọc (`Conditional`) | `PATCH /api/v1/notifications/{notification_id}/read` | `Student` / Bearer `JWT` | `Authorization` | `ApiEnvelope<Page<Notification>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` |
| #44 | Đánh dấu một thông báo đã đọc (`Conditional`) | Same | Same | `notification_id:int64!` path | Same contract | Same catalog error set only |

### Request Usage Matrix

| Request field | Source | Validation / normalization | SQL or branch use | Response use | Gap |
|---|---|---|---|---|---|
| `Authorization` | HTTP header | Bearer/JWT; require Student; take principal ID from token | Owner predicate `n.user_id=:principal_id` | Never echo token/user ID | API #44 has no route; shared helper exists. |
| `notification_id` | Required path `int64` | Parse as int64; invalid/out-of-range follows declared 422; do not add an unsupported positivity rule | Target `n.id=:notification_id` | `data.items[0].id` from returned row | Ownership and broadcast recipient model unresolved. |

### Query Matrix

| ID | Purpose | Type | Base table / alias | Column / condition | Value source | Result / branch | Evidence status |
|---|---|---|---|---|---|---|---|
| M1 | Mark the owned notification as read and return its display projection | `UPDATE ... RETURNING` | `notifications AS n` | `SET n.is_read=TRUE` | AC-20 action mapped to existing boolean read flag | Updated notification row | `DERIVED`; diagram instead says `read_at`. |
| M1 | Same | `WHERE` | `notifications AS n` | `n.id=:notification_id` | Path | Require one target row | Direct key + request contract |
| M1 | Same | `WHERE` | `notifications AS n` | `n.user_id=:principal_id` | Authenticated Student principal | Prevent cross-user update; no matching row maps to 404 | `DERIVED` from recipient-per-user diagram; nullable/broadcast rows excluded |
| M1 | Same | `RETURNING` | `notifications AS n` | `id` | Updated row | `notification_row.id` | Direct candidate |
| M1 | Same | `RETURNING` | `notifications AS n` | `title` | Updated row | `notification_row.title` | Direct candidate |
| M1 | Same | `RETURNING` | `notifications AS n` | `content` | Updated row | `notification_row.content` | Direct candidate |
| M1 | Same | `RETURNING` | `notifications AS n` | `created_at` | Updated row | `notification_row.created_at` | Candidate; timezone unresolved |

### Mutation Matrix

| ID | Operation | Target | Changed column | Value | Transaction / failure |
|---|---|---|---|---|---|
| M1 | Mark read | `notifications` | `is_read` | `TRUE` | One atomic statement in caller-owned transaction; commit when matched, no data change on 404, rollback on DB failure. No `read_at` column exists. |

The M1 row conditions are recorded separately in Query Matrix (`id=:notification_id` and `user_id=:principal_id`), one condition per row.

### Response Source Matrix

| Response field | Contract type | Candidate source / transform | Null / page rule | Status |
|---|---|---|---|---|
| `success` | boolean | Fixed `true` | Required | Direct envelope convention |
| `businessCode` | string | `DESIGN_RESOURCE_UPDATED` | Required | Direct catalog |
| `message` | string | Safe message | Literal not specified | Needs wording only |
| `data.items[]` | Notification[] | One updated row from M1 | Exactly one item on matched success | `DERIVED` singleton page proposal, API #42 precedent |
| `data.items[].id` | int64 | `notification_row.id` | Required | Direct candidate |
| `data.items[].title` | string | `notification_row.title` | Required | Direct candidate |
| `data.items[].content` | string | `notification_row.content` | Required | Direct candidate |
| `data.items[].channels` | `NotificationChannel[]` | No physical source; do not map `type` | Required by schema | `SOURCE_REQUIRED` |
| `data.items[].status` | `NotificationStatus` | No physical source; do not infer enum/read-state meaning | Required by schema | `SOURCE_REQUIRED` |
| `data.items[].read_at` | date-time? | Diagram target has no DDL source; do not derive timestamp | Optional/omission rule open | `DISCREPANCY / SOURCE_REQUIRED` |
| `data.items[].scheduled_at` | date-time? | No physical source | Optional/omission rule open | `SOURCE_REQUIRED` |
| `data.items[].created_at` | date-time | `notification_row.created_at` | Required; timezone rule open | `SOURCE_REQUIRED` for timezone |
| `data.pagination.page` | int32 | Fixed 1 | Singleton page | `DERIVED` |
| `data.pagination.size` | int32 | Fixed 1 | Singleton page | `DERIVED` |
| `data.pagination.total` | int64 | Fixed 1 | One updated resource | `DERIVED` |
| `data.pagination.total_pages` | int32 | Fixed 1 | One updated resource | `DERIVED` |
| `meta` | object | Empty metadata | `{}` | Envelope convention |
| `traceId` | uuid | Current request trace | Required | Shared convention; endpoint unwired |

### Planned DD structure and review boundary

1. Preserve API #44 catalog method/path/actor/path field/response/status/error set exactly.
2. Trace the AC-20 `ONE` edge: API #44 then `UPDATE read_at cho notification recipient`, then UI badge/read-state update. Preserve this logical target as expected behavior.
3. Because current physical design has only `notifications.is_read`, propose a single atomic `UPDATE ... SET is_read=TRUE WHERE id=:notification_id AND user_id=:principal_id RETURNING ...` as a simple physical candidate. Mark the mismatch with logical `NotificationRecipient.read_at`; do not add a table or column. Treat no owner-matching row (missing, other user, or broadcast with `user_id IS NULL`) as 404 to avoid exposing another user's notification. Repeating the state assignment is idempotent.
4. Do not add a body, query, user ID, status field, or undocumented error code. Map invalid int64 syntax/range to the catalog's 422; a well-formed ID with no owner-matching row maps to catalog 404.
5. Use API #42's single-resource `Page<T>` precedent to propose one updated notification in a one-item page (`page=1,size=1,total=1,total_pages=1`), all labeled `DERIVED`. The response still cannot be fully populated because required `channels`/`status` have no source; `read_at` also conflicts with DDL. Preserve those gaps as `SOURCE_REQUIRED` and open questions. Later API #45 must use consistent read-state and response semantics.
6. Build the request, mutation/query, response, error, and `07_notifications_mark_read.md` mappings; one request field, SQL field/condition and error case per row. Keep the whole DD `Draft — Needs Confirmation`.
7. Create eight template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` only under `apps/study-server/docs/dd/44_notifications_mark_read/`; no ZIP/runtime/schema/catalog/diagram edits.
8. Immediately verify the exact file set, front matter, API contract/status/errors, AC-20 trace, one-field/condition/error-per-row matrices, JSON, Markdown, local links, code fences, and source status. Update API #43 only if review finds a concrete contradiction; keep broader AC-20 macro review for API #45's DD session.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Logical recipient/read timestamp | AC-20 says `NotificationRecipient` and `read_at`; DB guide/ERD/DDL only have nullable `notifications.user_id` and `is_read`. | `DISCREPANCY / SOURCE_REQUIRED` | Candidate direct-user boolean update cannot persist a per-user timestamp or handle broadcast recipients. |
| Complete Notification response | Catalog requires `channels` and `status`; physical design has `type` and `is_read` only. `read_at`/`scheduled_at` are also absent. | `SOURCE_REQUIRED` | A fully contract-valid updated `Notification` cannot be assembled from the documented schema. |
| Page response semantics | Catalog and diagram specify `Page<Notification>` but no page semantics for a single-item mutation. | `DERIVED / OPEN_QUESTION` | Propose a one-item page based on API #42; require confirmation and reconcile with #45. |
| Idempotency header | API guideline mentions `Idempotency-Key` for retryable mutations; API #44 catalog declares only the path parameter and assignment-to-TRUE is state-idempotent. | `OPEN_QUESTION` | Do not invent a header; confirm whether guideline requires one here. |
| Error envelope | API guideline specifies `data:null`; current helper returns `{}` when `data` is None. | `DISCREPANCY` | Record current/expected response difference; API #44 is unwired. |
| API #44 implementation | No route/module/query/test found. | `UNWIRED / NOT_FOUND` | DD is design-only. |

## CHANGES

- Files changed: This worklog only so far; no API #44 DD files have been authored yet.
- CONTEXT_UPDATES: None planned; the work is docs-only.
- Context pages changed: None planned.
- Assumptions: Prefer simple and understandable derived behavior, but keep all current schema/diagram conflicts visible and never label a candidate as runtime behavior.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Selected and read #41, #42 and #43 matching `docs` worklogs; no shortage. | `VERIFIED` |
| Context and registered skill | Read router/map, server-study entry/index/workflow/declared routes, manifest and skill registry; `createDD-markdown` is registered for `server-study`. | `VERIFIED` |
| Template gate | Read eight baseline Markdown sheets; SHA-256 matches API #43's recorded template fingerprints. Study requires Markdown-only. | `VERIFIED` |
| AC-20 diagram | Parsed all AC-20 nodes and edges: GET/list, recipient read, branch ONE/API #44, `UPDATE read_at`, UI update; API #45 is the ALL branch. | `VERIFIED` |
| Catalog/DB/current source coverage | Read #43–#45 contracts, reusable Notification/Page schemas, DB guide/ERD/DDL, current router/auth/error helper and searched app/tests for notifications. | `VERIFIED` |
| Archive inventory | No ZIP/XLSX/XLSM found in Study docs/app, Study PostgreSQL schema or registered DD skill tree. | `VERIFIED` |
| DD authoring and validation | Pending. | `PENDING` |
| Runtime tests | Not run; no API #44 implementation/test source. | `NOT_RUN` |

## HANDOFF

- Remaining design questions: Recipient table/read timestamp versus boolean source; required Notification channel/status mappings; mutation `Page<Notification>` meaning; retry/idempotency header policy; error-envelope discrepancy. See the API #44 `OPEN_QUESTIONS.md` after authoring.
- Next owner/action: Complete API #44 DD, then in API #45's session reconcile all three AC-20 endpoint flows, write semantics and response shape.
