# PLAN_RESULT — Study API #45

## Kết quả

- API ID: 45 — `PATCH /api/v1/notifications/read-all`.
- DD folder: `apps/study-server/docs/dd/45_notifications_read_all/`.
- Trạng thái DD: `Draft — Needs Confirmation`.
- Trạng thái runtime: `UNWIRED / NOT_FOUND`.
- Basis: API catalog và nhánh ALL của AC-20; legacy `is_read` update/Page semantics là DERIVED proposal.
- Deliverable: 8 template sheets và 3 report Markdown; không tạo ZIP theo Study workflow.

## Input Manifest và Coverage

| ID | Source | Đơn vị trong phạm vi | Đã đọc | Trạng thái | Vai trò |
|---|---|---|---|---|---|
| S1 | `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md` | Router/context flow | Có | VERIFIED | Scope và task classification. |
| S2 | Worklog README, selector, selected logs #41–#43 | 3 worklogs | 3/3 | VERIFIED | Preflight/carry-forward. |
| S3 | `.agents/server-study/AGENTS.md`, INDEX, workflow, declared routes, database, tests | Study scope pages | Có | VERIFIED | Runtime boundary, schema/test evidence, Markdown-only. |
| S4 | Context manifest, skill index, `createDD-markdown` entry | Registry and skill | Có | VERIFIED | Skill/workflow wired for server-study. |
| S5 | `DD_API_Template_MD/00–07` | 8 Markdown sheets and fingerprints | 8/8 | VERIFIED | Baseline structure and source appendices. |
| S6 | `docs/lists/list_api.md` | APIs #43–#45, Page/Notification schemas | Có | VERIFIED | Exact contract and error sets. |
| S7 | AC/API index and AC-20 page in `AC_02_STUDENT_LEARNING.drawio` | AC-20 nodes and edges | Full relevant page | VERIFIED | ONE/ALL actions, bulk update and UI update. |
| S8 | `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio`, `infra/postgres/study-server/DB.sql` | Notification table, relation, DDL | Có | VERIFIED | Legacy numeric ID/`is_read` candidate; live schema unknown. |
| S9 | `infra/postgres/02_study_db.sql` and database contexts | Notification and identity model | Relevant definitions | VERIFIED | Alternative UUID/`learner_id`/`read_at` model; conflicts recorded. |
| S10 | Current Study router, auth/response helpers, app and test search | Route/helper/match inventory | Có | VERIFIED | API #45 is unwired; current principal is numeric user ID. |
| S11 | API guidelines, API #42 response/Page precedent, DD #43/#44 | Relevant contract/DD pages | Có | VERIFIED | Envelope, Page proposal and AC-20 group baseline. |
| S12 | Scoped ZIP/XLSX/XLSM search | Study docs/app/tests and skill template tree | Có | None found | No source archive in scope. |

## API Requirement Matrix

| API ID | Method / endpoint | Actor/auth | Request | Response | Success and errors |
|---|---|---|---|---|---|
| #45 | `PATCH /api/v1/notifications/read-all` | Student / Bearer JWT | `body{}` | `ApiEnvelope<Page<Notification>>` | 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/422/500 exactly as catalog. |

## Request Usage Matrix

| Request item | Source | Validation / proposal | Mutation use | Response use | Gap |
|---|---|---|---|---|---|
| `Authorization` | HTTP header | Bearer/JWT; require Student | Principal owner predicate | No token/principal output | UUID pilot mapping conflicts with numeric current principal. |
| Empty object body | `body{}` | Propose `{}` with no fields; body requiredness/unknown-property policy open | No SQL value | None | 422 trigger unspecified; exact body behavior is DERIVED. |

## Query Matrix

| ID | Type | Source | Column/condition | Rule | Status |
|---|---|---|---|---|---|
| M1 | UPDATE SET | `notifications AS n` legacy candidate | `n.is_read = TRUE` | Mark matching unread notifications read. | DERIVED; diagram uses `read_at`. |
| M1 | WHERE | `notifications AS n` | `n.user_id = :principal_id` | Scope to direct recipient. | DERIVED. |
| M1 | WHERE | `notifications AS n` | `n.is_read = FALSE` | Update only unread rows; NULL does not match. | DERIVED. |
| M1 | RETURNING | `notifications AS n` | `n.id` | Candidate ID. | Direct legacy candidate; pilot UUID conflict. |
| M1 | RETURNING | `notifications AS n` | `n.title` | Candidate title. | Direct legacy candidate. |
| M1 | RETURNING | `notifications AS n` | `n.content` | Candidate content. | Direct legacy candidate. |
| M1 | RETURNING | `notifications AS n` | `n.created_at` | Candidate creation timestamp. | Timezone unresolved. |

## Mutation Matrix

| ID | Operation | Target | Conditions | Field/value | Transaction / no-op |
|---|---|---|---|---|---|
| M1 | Mark all unread read | legacy `notifications` candidate | `user_id=:principal_id`; `is_read=FALSE` | `is_read=TRUE` | One caller-owned atomic statement; zero returned rows is successful no-op. |

## Response Source Matrix

| Response field | Candidate source | Transform/rule | Status |
|---|---|---|---|
| `data.items[].id` | legacy notifications.id | Direct; pilot UUID conflicts | DISCREPANCY |
| `data.items[].title` | legacy notifications.title | Direct candidate | Candidate |
| `data.items[].content` | legacy notifications.content | Direct candidate; pilot uses body | DISCREPANCY |
| `data.items[].channels` | No approved source | Do not map legacy type or combine schemas | SOURCE_REQUIRED |
| `data.items[].status` | No approved source | Do not infer from read or delivery status | SOURCE_REQUIRED |
| `data.items[].read_at` | AC-20 concept / pilot alternative | No compatible current principal mapping | SOURCE_REQUIRED |
| `data.items[].scheduled_at` | None | No physical column found | SOURCE_REQUIRED |
| `data.items[].created_at` | Legacy notifications.created_at | ISO-8601; timezone open | SOURCE_REQUIRED for timezone |
| `data.pagination.page` | DERIVED | Fixed 1 | DERIVED |
| `data.pagination.size` | M1 returned count | `updated_count` | DERIVED; unbounded |
| `data.pagination.total` | M1 returned count | `updated_count` | DERIVED |
| `data.pagination.total_pages` | M1 returned count | 0 if empty, otherwise 1 | DERIVED |

## Conflict and assumptions

| ID | Finding | Treatment |
|---|---|---|
| C1 | AC-20 names `NotificationRecipient.read_at`; legacy schema has `user_id`/`is_read`, no recipient table or timestamp. | Use direct-recipient boolean update only as DERIVED candidate; no broadcast updates. |
| C2 | V1-PILOT DDL uses UUID notification IDs and UUID learner IDs, while API catalog/current auth use int64/numeric user IDs. | Preserve as schema-generation conflict; do not invent UUID/int64 mapping. |
| C3 | `Notification.channels`/`status` have no aligned physical source. | Keep SOURCE_REQUIRED; do not map `type`, `is_read`, or pilot delivery status silently. |
| C4 | API #45 response Page has no pagination semantics and no request page. | Propose all changed rows in one Page; unbounded response needs confirmation. |
| C5 | Catalog declares `body{}` and 422 without rules. | Propose an empty JSON object and mark strictness as DERIVED/open. |
| C6 | Error guideline says `data:null`, shared helper defaults to `{}`. | Preserve as runtime/design discrepancy. |
| C7 | Zero unread rows. | Treat as 200 success with empty Page; idempotent no-op, DERIVED. |

## Verification boundary

- Current route/module/test evidence establishes API #45 as `UNWIRED / NOT_FOUND`; runtime tests are not run.
- No live DB metadata, deployment, migration application or performance plan was checked.
- Macro review of APIs #43–#45 is recorded in `VERIFICATION_REPORT.md` after final edits.
