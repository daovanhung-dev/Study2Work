---
task_id: "2026-10-23-create-study-api45-dd"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Create Study API #45 DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Preserve catalog contract, mark unsupported inference DERIVED, and keep missing physical columns SOURCE_REQUIRED; API #41 is part of AC-19, not AC-20.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: Existing DDs may use a derived singleton Page<T>, but missing response fields and schema gaps remain explicit; API #42 closed AC-19 review.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: AC-20 #43–#45 is one notification group; #43 documents recipient/read-state and response-source gaps, with macro review pending after #45.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create one source-aware Vietnamese Markdown DD for API #45, after a plan and diagram review; then reconcile the connected APIs #43–#45 as one group.
- Canonical contract/approved DD: API #45 in `docs/lists/list_api.md`; AC-20 index and activity diagram; notification DB guide, ERD and checked-in DDL; related DDs #43/#44; registered `createDD-markdown` skill and Study Markdown-only workflow.

## CURRENT_BEHAVIOR

- Source/config: No API #45 route, module or focused test is present in `apps/study-server`; current router/context covers #01–#09 and #12–#14. The reusable `validate_current_user_request` helper takes a positive numeric `users.id` from the Student JWT. `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio` and `infra/postgres/study-server/DB.sql` agree on the older notification shape: `id BIGSERIAL`, nullable `user_id`, `sender_id`, `title`, `content`, nullable `type`, boolean `is_read`, and `created_at`; there is no `NotificationRecipient` or `read_at`. A second checked-in V1-PILOT artifact, `infra/postgres/02_study_db.sql`, defines a different UUID/`learner_id` notification model with `read_at` and a `notification_deliveries` table; it does not align with the catalog's int64 notification ID or the current numeric JWT principal. Neither DDL proves live schema. `Notification` contract fields `channels` and `status` still lack a single approved mapping across these schema designs.
- Runnable tests: Not run; docs-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #45. A scoped search across current Study app and tests found no notification route/module/query/test.

## SOURCE_TRACE

```text
Student Bearer principal -> resolve notification-recipient scope -> update all applicable read state -> map catalog response -> return success/error envelope
```

## PLAN BEFORE DD AUTHORING

1. Preserve the exact catalog contract: `PATCH /api/v1/notifications/read-all`, Student Bearer JWT, empty `body{}`, `ApiEnvelope<Page<Notification>>`, 200 `DESIGN_RESOURCE_UPDATED`, and only 401/403/422/500 errors.
2. Follow AC-20: notification center loads API #43; the ALL branch calls API #45; the backend bulk-updates unread recipient state; UI then synchronizes badge/read state. Preserve every node and edge.
3. Keep expected schema evidence separate: AC-20's logical `NotificationRecipient.read_at`; legacy DB guide/ERD/`infra/postgres/study-server/DB.sql` with direct user rows and `is_read`; parallel V1-PILOT `infra/postgres/02_study_db.sql` with UUID `learner_id`, `read_at`, and delivery rows. Do not silently combine these models.
4. Reuse API #43/#44's safe principal scoping, `is_read` proposal, response-field gap, trace/error envelope notes, and API #42 singleton-Page precedent only where applicable. For #45, propose updating direct-recipient unread rows only; zero matches is a successful no-op because the endpoint has no resource ID.
5. Propose the response as one derived Page containing every row actually changed by the bulk statement; set page=1 and size/total to the changed-row count, with total_pages=0 when empty and 1 otherwise. Mark unbounded response size and all unresolved `Notification` fields as OPEN_QUESTIONS.
6. Treat `body{}` as an empty JSON object proposal; do not invent request fields. Record empty-body requiredness/extra-property behavior and the catalog 422 trigger as DERIVED/open.
7. Record the API Requirement Matrix and all four pre-authoring matrices below before creating any file in the API #45 DD folder.
8. Author eight template sheets and three reports under the API #45 folder only; Study output is Markdown-only.
9. Validate the API #45 pack, then reconcile API #43/#44/#45 contracts, state transitions, response semantics, error sets, ownership and DB-schema alternatives. Update only the connected DD/report/worklog files where evidence requires it.

### Pre-authoring matrices (completed before DD folder authoring)

#### API Requirement Matrix

| API ID | Method / endpoint | Actor / auth | Request | Response | Success and exact errors |
|---|---|---|---|---|---|
| #45 | `PATCH /api/v1/notifications/read-all` | `Student` / Bearer JWT | `body{}` (empty object; no declared fields) | `ApiEnvelope<Page<Notification>>` | 200 `DESIGN_RESOURCE_UPDATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` |

#### Request Usage Matrix

| Request item | Source | Validation / proposal | Query or branch use | Response use | Gap |
|---|---|---|---|---|---|
| `Authorization` | HTTP header | Reuse Student Bearer/JWT helper pattern; principal is numeric user ID in current Study source | Scope every mutation to the authenticated principal | Never return token/principal | API #45 is unwired; UUID V1-PILOT learner mapping conflicts. |
| Empty JSON object | Catalog `body{}` and AC-20 node | Proposal: accept `{}` with no fields; empty-body requiredness and unknown-property policy need confirmation | No body value enters SQL | No response field | Catalog lists 422 but trigger is unspecified; proposed empty-object validation is DERIVED. |

#### Query Matrix

| ID | Type | Candidate source | Column / condition | Rule | Evidence status |
|---|---|---|---|---|---|
| M1 | `UPDATE` | `notifications AS n` (legacy Study DDL candidate) | `SET n.is_read = TRUE` | Mark unread direct-recipient notifications as read. | DERIVED; AC-20 says `NotificationRecipient.read_at`. |
| M1 | `WHERE` | `notifications AS n` | `n.user_id = :principal_id` | Never update another user's row or a NULL/broadcast row. | DERIVED; principal source is current Student helper, recipient schema unresolved. |
| M1 | `WHERE` | `notifications AS n` | `n.is_read = FALSE` | Only transition currently unread rows; repeat call is a no-op. | DERIVED from “all unread” in AC-20. |
| M1 | `RETURNING` | `notifications AS n` | `n.id` | Candidate response item ID. | Direct candidate from legacy DDL; conflicts with UUID V1-PILOT. |
| M1 | `RETURNING` | `notifications AS n` | `n.title` | Candidate response title. | Direct candidate from legacy DDL. |
| M1 | `RETURNING` | `notifications AS n` | `n.content` | Candidate response content. | Direct candidate from legacy DDL. |
| M1 | `RETURNING` | `notifications AS n` | `n.created_at` | Candidate creation time. | Direct column candidate; legacy timestamp timezone unresolved. |

#### Mutation Matrix

| ID | Operation | Target | Condition | Changed field | Value | Transaction / no-op |
|---|---|---|---|---|---|---|
| M1 | Mark all unread as read | `notifications` (legacy DDL candidate) | `user_id=:principal_id` AND `is_read=FALSE` (each is a separate condition above) | `is_read` | `TRUE` | One caller-owned atomic update; zero matching rows returns success with an empty Page; repeat call changes no state. |

#### Response Source Matrix

| Response field | Contract type | Candidate source | Transform / proposed rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope | true on success | Direct convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_UPDATED` | Direct |
| `message` | string | Safe literal | Exact wording not specified | Open wording only |
| `data.items[].id` | int64 | legacy `notifications.id` | Direct; UUID V1-PILOT conflicts | DISCREPANCY |
| `data.items[].title` | string | legacy `notifications.title` | Direct candidate | Candidate |
| `data.items[].content` | string | legacy `notifications.content` | Direct candidate | Candidate |
| `data.items[].channels` | `NotificationChannel[]` | No approved single source | Do not map `type` or join pilot delivery rows without schema decision | SOURCE_REQUIRED |
| `data.items[].status` | `NotificationStatus` | No approved single source | Do not infer read state from delivery status or `is_read` | SOURCE_REQUIRED |
| `data.items[].read_at` | date-time? | AC-20 asks for recipient timestamp; legacy schema lacks it; pilot DDL has it with different identity model | Do not synthesize timestamp from boolean | DISCREPANCY / SOURCE_REQUIRED |
| `data.items[].scheduled_at` | date-time? | No source in legacy DDL; pilot notification DDL also lacks this column | Optional omission/null rule open | SOURCE_REQUIRED |
| `data.items[].created_at` | date-time | legacy `notifications.created_at` candidate | ISO-8601 needs timezone rule | SOURCE_REQUIRED for timezone |
| `data.pagination.page` | int32 | Derived | 1 | DERIVED |
| `data.pagination.size` | int32 | M1 returned row count | Equal number of affected rows; 0 when empty | DERIVED; page contract has no bulk semantics |
| `data.pagination.total` | int64 | M1 returned row count | Equal number of affected rows | DERIVED |
| `data.pagination.total_pages` | int32 | M1 returned row count | 0 when empty; otherwise 1 because all affected rows are returned in one page | DERIVED; unbounded response risk |
| `meta` | object | Envelope | `{}` absent endpoint-specific metadata | Direct convention |
| `traceId` | uuid | Request trace | Propagate current trace | Direct convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #45 source | Current router/module/tests scoped search has no API #45 notification implementation | `UNWIRED / NOT_FOUND` | DD is design-only; no runtime behavior is asserted. |
| AC-20 `NotificationRecipient.read_at` versus legacy schema | Diagram uses per-recipient timestamp; DB guide/ERD/legacy DDL only provide `user_id` and boolean `is_read` | `DISCREPANCY / SOURCE_REQUIRED` | Candidate updates only direct-user unread rows; broadcast read state is unsupported. |
| Legacy Study DDL versus V1-PILOT DDL | Legacy notification IDs/principal IDs are BIGINT; V1-PILOT uses UUID notification IDs and UUID `learner_id`, with `read_at` and delivery rows | `DISCREPANCY / SOURCE_REQUIRED` | No safe direct mapping joins catalog IDs/current JWT principal to V1-PILOT. Live schema remains unverified. |
| Notification response/page contract | Catalog requires Page<Notification>; `channels`/`status` lack one aligned physical source; all-rows Page is unbounded | `DISCREPANCY / SOURCE_REQUIRED / DERIVED` | Draft proposal returns all changed rows, with contract/schema decision still needed. |
| Body/error 422 behavior | Catalog says `body{}` and includes 422; no detailed validation rule is specified | `DERIVED / OPEN_QUESTION` | Propose empty JSON object validation without adding fields; exact requiredness/extra-field policy needs confirmation. |
| AC-20 #43–#45 group | #43 and #44 drafts exist; #44 verification report is still pending | `PENDING_MACRO_REVIEW` | Validate and reconcile all three DDs after #45 authoring. |

## CHANGES

- Files changed: This worklog now contains the completed evidence-backed plan and four pre-authoring matrices; DD authoring begins only after this plan.
- CONTEXT_UPDATES: None planned unless source/context discrepancy requires a registered page update.
- Context pages changed: None planned.
- Assumptions: Simple DERIVED rules may be proposed where diagrams are silent; no unsupported table/column/field or behavior will be presented as confirmed.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Selected and read three matching `docs` worklogs (#41–#43); no shortage. | `VERIFIED` |
| Catalog/API Requirement Matrix | API #45 method/path/actor/body/response/status/error set read directly from catalog row 45. | `VERIFIED` |
| AC-20 diagram trace | Parsed all AC-20 nodes and directed edges; ALL edge calls API #45, then bulk update, then UI state update. | `VERIFIED` |
| DB/source comparison | Read DB guide, ERD notification node/relation, both checked-in Study DDL artifacts, current route/auth/response source and scoped notification test search. | `VERIFIED_WITH_DISCREPANCY` |
| Template/skill gate | `createDD-markdown` is registered for `server-study`; opened all eight Markdown templates and fingerprints; Study workflow requires Markdown only. | `VERIFIED` |
| Related DD review | Read the API #43 and #44 sheets/reports and API #42 Page precedent; API #44 final validation remains pending. | `VERIFIED_WITH_PENDING_GROUP_REVIEW` |
| API #45 pack and macro validation | Pending authoring. | `PENDING` |
| Runtime tests | Not run; docs-only task. | `NOT_RUN` |
| Context validator | Pending final worklog/DD update. | `PENDING` |

## HANDOFF

- Remaining blockers: Conflicting notification schema generations; no shared `Notification` field source for channels/status; response Page semantics for mark-all and empty-body/422 details need confirmation. Draft can proceed with explicit DERIVED proposals and SOURCE_REQUIRED markers.
- Next owner/action: Author/validate API #45, finalize #44 verification, update the #43–#45 macro review and run the context validator.
