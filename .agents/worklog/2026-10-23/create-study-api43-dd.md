---
task_id: "2026-10-23-create-study-api43-dd"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Create Study API #43 DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Preserve catalog contract and label unsupported inferences `DERIVED`; report source/schema gaps rather than inventing columns.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: The #39–#42 discussion group was reconciled; its read-only `07_table.md` pattern uses explicit N/A mutation sections and candidate source projections.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: Resumed the in-progress API #43 worklog; replaced its pending research/plan section with verified catalog, AC-20, DB/source evidence and pre-authoring matrices.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create one source-aware, Vietnamese Markdown DD for API #43; read relevant diagrams and prior DDs; plan before authoring; then validate the API and any directly connected group.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #43 and its referenced AC/UC diagrams, existing DB design evidence, registered `createDD-markdown` skill, and Study Markdown-only workflow.

## CURRENT_BEHAVIOR

- Source/config: API #43 has no route/module/query/focused test in current Study source (`UNWIRED / NOT_FOUND`). Target DD folder does not exist. AC-20 diagram says to read `NotificationRecipient` by user, but no such physical table exists in the DB guide, ERD or checked-in DDL. The DDL has `notifications(id, user_id NULL, sender_id NULL, title, content, type NULL, is_read DEFAULT FALSE, created_at)`; it has no `channels`, `status`, `read_at`, or `scheduled_at` columns. The live schema is not verified.
- Runnable tests: Not run; documentation-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #43. The shared Student JWT helper and response-envelope helpers exist, but API #43 does not call them.

## SOURCE_TRACE

```text
Student Bearer JWT -> current Student principal -> candidate SELECT notifications WHERE user_id = principal_id and optional is_read = FALSE -> matching COUNT/page -> ApiEnvelope<Page<Notification>> contract mapping -> 200; preserve catalog 401/403/500 errors
```

## PLAN BEFORE DD AUTHORING

1. Preserve the API catalog contract exactly: `GET /api/v1/users/me/notifications`, Student Bearer JWT, `unread_only?:boolean`, `page?:int32`, `ApiEnvelope<Page<Notification>>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, and only the listed 401/403/500 errors.
2. Follow AC-20: open notification center, list the current user's notifications, then let API #44 or #45 update read state. The diagram's `NotificationRecipient` is a logical source only; use `notifications.user_id = current principal` as a DERIVED candidate and leave NULL/broadcast/segment delivery unresolved because no per-recipient table is present.
3. Request Usage Matrix: Authorization supplies the Student principal; `unread_only=true` adds `is_read = FALSE`; false/omitted includes either read state; `page` selects a page. The same owner and unread predicates must be used for list and count.
4. Query Matrix: candidate `Q1` selects `id,title,content,created_at` from `notifications AS n`, with `is_read` used only as the optional unread predicate; candidate `Q2` counts the same filtered rows. Propose fixed `size=20`, page default 1, `created_at DESC, id DESC`, and `OFFSET=(page-1)*20` as DERIVED, following the nearby API #10 Page precedent. Empty/out-of-range page returns an empty page. Do not add a `size` or sort input. Page < 1 behavior remains open because catalog #43 has no 422 error.
5. Mutation Matrix: N/A — API #43 is GET/read-only. The #44/#45 diagram mutations are outside this DD and will be validated together after those DDs exist.
6. Response Source Matrix: map only catalog fields with a direct candidate source (`id`, `title`, `content`, `created_at`). Keep `channels`, `status`, `read_at`, and `scheduled_at` as SOURCE_REQUIRED; do not equate `type` with `channels`, `is_read` with `status`, or `is_read` with `read_at`. Include the required PageMeta contract and mark size/paging behavior DERIVED.
7. Record additional discrepancies: the API #43 `NotificationRecipient` diagram term has no physical table; nullable `notifications.user_id` allows broadcast rows but no user-specific read state; `TIMESTAMP` has no timezone declaration; enum values for `NotificationChannel` and `NotificationStatus` are not defined in sources. Preserve these as OPEN_QUESTIONS.
8. Create eight template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` in `apps/study-server/docs/dd/43_users_me_notifications/`. Put the requirement matrix and four pre-authoring matrices in `PLAN_RESULT.md`; keep all content Vietnamese, `Draft — Needs Confirmation`, use template appendices, include a read-only `07_table.md`, and do not create a ZIP.
9. Validate file set/front matter, catalog method/path/actor/query/response/status/error contract, JSON, local links, Markdown tables, one-field-per-row rules, status labels and scope. Leave the #43–#45 macro review pending for the session that creates #45.

### Pre-authoring matrices

#### API Requirement Matrix

| API ID | Method / endpoint | Actor/auth | Request field | Response / status | Basis |
|---|---|---|---|---|---|
| #43 | GET /api/v1/users/me/notifications | Student / Bearer JWT | Authorization | ApiEnvelope<Page<Notification>>; 200; errors 401/403/500 exactly as catalog | Catalog + AC-20 |
| #43 | GET /api/v1/users/me/notifications | Student / Bearer JWT | unread_only?:boolean | Same response/status contract | Catalog + AC-20 |
| #43 | GET /api/v1/users/me/notifications | Student / Bearer JWT | page?:int32 | Same response/status contract | Catalog + AC-20 |

#### Query Matrix

| Query | Type | Candidate source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1 | SELECT | notifications AS n | n.id | Notification ID. | Direct column |
| Q1 | SELECT | notifications AS n | n.title | Title. | Direct column |
| Q1 | SELECT | notifications AS n | n.content | Content. | Direct column |
| Q1 | SELECT | notifications AS n | n.created_at | Creation time. | Column direct; timezone unresolved |
| Q1 | WHERE | notifications AS n | n.user_id = :principal_id | Current Student scope. | DERIVED |
| Q1 | WHERE | notifications AS n | n.is_read = FALSE | Conditional on unread_only=true. | DERIVED |
| Q1 | ORDER BY | notifications AS n | n.created_at DESC | Newest first. | DERIVED |
| Q1 | ORDER BY | notifications AS n | n.id DESC | Stable tie-breaker. | DERIVED |
| Q1 | LIMIT | N/A | 20 | Fixed page size. | DERIVED |
| Q1 | OFFSET | N/A | (effective_page - 1) * 20 | Page offset. | DERIVED |
| Q2 | COUNT | notifications AS n | COUNT(*) | Same predicates as Q1. | DERIVED |

#### Mutation Matrix

| Mutation | Target | Fields / condition | Status |
|---|---|---|---|
| None | N/A | N/A | N/A — READ-ONLY API; #44/#45 are separate endpoints |

#### Response Source Matrix

| Response field | Contract type | Candidate source | Mapping status |
|---|---|---|---|
| data.items[].id | int64 | notifications.id | DIRECT candidate |
| data.items[].title | string | notifications.title | DIRECT candidate |
| data.items[].content | string | notifications.content | DIRECT candidate |
| data.items[].created_at | date-time | notifications.created_at | Column candidate; timezone SOURCE_REQUIRED |
| data.items[].channels | NotificationChannel[] | N/A | SOURCE_REQUIRED |
| data.items[].status | NotificationStatus | N/A | SOURCE_REQUIRED |
| data.items[].read_at | date-time? | N/A | SOURCE_REQUIRED |
| data.items[].scheduled_at | date-time? | N/A | SOURCE_REQUIRED |
| data.pagination.page | int32 | Request page | DERIVED default 1 |
| data.pagination.size | int32 | Fixed page size | DERIVED value 20 |
| data.pagination.total | int64 | Q2 COUNT(*) | DERIVED |
| data.pagination.total_pages | int32 | Q2 total / size | DERIVED |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| `NotificationRecipient` versus physical schema | AC-20 node says read recipients by user; DB guide/ERD/DDL only define `notifications.user_id` and `is_read` | `DISCREPANCY / SOURCE_REQUIRED` | Direct-user rows are a candidate; broadcast/segment rows cannot be safely scoped or read-tracked. |
| Notification response fields | Catalog requires `channels`, `status`, and optionally `read_at`/`scheduled_at`; physical table has `type`, `is_read`, and no schedule/read timestamp | `DISCREPANCY / SOURCE_REQUIRED` | Do not invent columns or map similarly named concepts. Full response projection needs an approved source/schema decision. |
| Enum definitions | Catalog uses `NotificationChannel` and `NotificationStatus` but repository search found no enum member definitions | `SOURCE_REQUIRED` | Valid channel/status values remain unresolved. |
| Page rules | Request has `page` only; PageMeta requires `size`; AC-20 does not define size/order/invalid-page behavior | `DERIVED / OPEN_QUESTION` | Proposed page=1, fixed size=20, newest-first order; page<1 handling must not invent an undeclared 422. |
| API #43 implementation | No route/module/query/test match in current Study source | `UNWIRED / NOT_FOUND` | DD is design-only. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/43_users_me_notifications/` (8 template sheets + 3 reports) and this worklog. No source, schema, catalog, diagram, or runtime files changed.
- CONTEXT_UPDATES: None planned; API #43 is expected to be docs-only.
- Context pages changed: None planned.
- Assumptions: Preserve the catalog contract exactly; derive only simple behavior where diagrams and source leave a gap, and mark it DERIVED.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Selected and read #41, #42 and the existing in-progress #43 worklog; no shortage. | `VERIFIED` |
| Context/skill/template gate | `createDD-markdown` is wired to `server-study`; opened the complete skill, all eight Markdown templates and their SHA-256 fingerprints. Study workflow overrides ZIP packaging. | `VERIFIED` |
| Catalog/diagram/DB/source coverage | Read API #43–#45 catalog rows, AC-20 index/diagram nodes+edges, Notification schema, DB guide, ERD, checked-in DDL, current router/auth/response helper and notification source/test scan. | `VERIFIED` |
| Prior DD precedent | Read API #38 Page response and API #10 fixed-size pagination pattern; read API #42 read-only table pattern. | `VERIFIED` |
| Markdown pack validation | 11/11 files, 8/8 front matters and appendices, catalog contract, AC-20 trace, JSON, local links/anchors, table widths, code fences, inline formatting, and field/condition/error row granularity passed; core SHA-256 is recorded in `VERIFICATION_REPORT.md`. | `VERIFIED` |
| Runtime tests | Not run: docs-only task; API #43 is `UNWIRED / NOT_FOUND`. | `NOT_RUN` |
| Context validator | `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID` for pre-existing missing db-admin context/source paths and absent baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no out-of-scope repair made. | `BLOCKED_BY_REPO_BASELINE` |

## HANDOFF

- Remaining design questions: Recipient/broadcast source; channel/status enums and source columns; read/scheduled timestamp source and omission rules; page size/order/range confirmation; timestamp timezone; error-envelope discrepancy. See `OPEN_QUESTIONS.md`.
- Next owner/action: Continue the one-API-per-session sequence with API #44; reconcile the AC-20 #43–#45 group after #45 DD exists.
