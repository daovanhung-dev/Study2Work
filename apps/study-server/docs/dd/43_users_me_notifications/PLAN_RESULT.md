# PLAN_RESULT — Study API #43

## Kết quả

- API ID: 43.
- DD folder: apps/study-server/docs/dd/43_users_me_notifications/.
- Trạng thái DD: Draft — Needs Confirmation.
- Trạng thái runtime: UNWIRED / NOT_FOUND.
- Basis: API catalog + AC-20 diagram + current DB design; pagination/order là DERIVED.
- Kết luận: Tạo đủ 8 sheet và 3 report. Contract giữ nguyên; required Notification fields chưa có nguồn vật lý nên chưa chuyển sang Ready/Final.

## Input Manifest và Coverage

| ID | Source | Đơn vị trong phạm vi | Đã đọc | Trạng thái | Vai trò |
|---|---|---|---:|---|---|
| S1 | AGENTS.md, .agents/AGENTS.md, context-map.md | Project routing | Có | VERIFIED | Phân loại task và boundary. |
| S2 | server-study AGENTS, INDEX, workflow, declared routes | Study scope pages | Có | VERIFIED | Runtime boundary, Markdown-only workflow. |
| S3 | .agents/context-manifest.json | Skill/workflow entries | Có | VERIFIED | createDD-markdown wired cho server-study. |
| S4 | createDD_MARKDOWN_SKILL.md | Toàn bộ skill, 2,324 dòng | Có | VERIFIED | Tạo source-backed API DD. |
| S5 | DD_API_Template_MD/00–07 | 8 Markdown template files | 8/8 | VERIFIED | Giữ headings, order, audit appendices. |
| S6 | docs/lists/list_api.md | API #43–#45 và reusable Page/Notification schemas | Có | VERIFIED | Contract/error set. |
| S7 | AC_UNICA/00_AC_API_INDEX.md | AC-20 section | Có | VERIFIED | Actor, precondition, postcondition, API list. |
| S8 | AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Toàn page AC-20 | Có | VERIFIED | Node/edge flow: load, recipient read, render, one/all actions. |
| S9 | DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio | notifications section/node/relations | Có | VERIFIED | Logical/physical field evidence. |
| S10 | infra/postgres/study-server/DB.sql | notifications table definition | Có | VERIFIED | Checked-in DDL; live schema unverified. |
| S11 | contracts/api-guidelines/README.md | Envelope/error/trace rules | Có | VERIFIED | Expected response conventions. |
| S12 | app/api/v1.py, app/utils/auth.py, app/core/responses.py; notification source/test search | Exact route/helper/search scope | Có | VERIFIED | Current implementation boundary; no #43 implementation. |
| S13 | API #10 mapping, API #38 response, API #42 read-only mapping | Relevant precedent sheets | Có | VERIFIED | Page convention and read-only style. |
| S14 | ZIP/XLSX/XLSM search under Study docs/source scope | File inventory | Có | No archive found | No source archive was supplied or required by this local scope. |

## API Requirement Matrix

| API ID | Method / endpoint | Actor/auth | Request field | Response | Success / errors |
|---|---|---|---|---|---|
| #43 | `GET` `/api/v1/users/me/notifications` | `Student` / Bearer `JWT` | `Authorization` | `ApiEnvelope<`Page<Notification>`>` | 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` |
| #43 | `GET` `/api/v1/users/me/notifications` | `Student` / Bearer `JWT` | `unread_only`?:boolean | `ApiEnvelope<`Page<Notification>`>` | Same catalog `success`/error set. |
| #43 | `GET` `/api/v1/users/me/notifications` | `Student` / Bearer `JWT` | page?:int32 | `ApiEnvelope<`Page<Notification>`>` | Same catalog `success`/error set. |

## Request Usage Matrix

| Request field | Source | Query/branch use | Response use | Gap/`status` |
|---|---|---|---|---|
| `Authorization` | Bearer `JWT` | Validate `Student`; get principal ID | No direct response field | Direct contract; API #43 unwired. |
| `unread_only` | Query boolean | true → candidate `n.`is_read` = FALSE`; false/omitted → no unread predicate | No corresponding catalog field | Predicate DERIVED; per-user read storage unresolved. |
| page | Query int32 | `LIMIT`/`OFFSET` after derived page rule | `data.pagination.page` | Default 1 and size 20 DERIVED; invalid/nonpositive behavior open. |

## Query Matrix

| ID | Type | Source | Query item | Rule | Status |
|---|---|---|---|---|---|
| Q1 | `SELECT` | notifications AS n | n.id | Select notification identifier. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.`title` | Select notification `title`. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.`content` | Select notification `content`. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.`created_at` | Select creation time. | Timezone unresolved |
| Q1 | `WHERE` | notifications AS n | `n.`user_id` = :principal_id` | Owner predicate. | DERIVED |
| Q1 | `WHERE` | notifications AS n | `n.`is_read` = FALSE` | Add only for `unread_only`=true. | DERIVED |
| Q1 | `ORDER BY` | notifications AS n | `n.`created_at` DESC` | Newest first. | DERIVED |
| Q1 | `ORDER BY` | notifications AS n | `n.id DESC` | Stable tie-breaker. | DERIVED |
| Q1 | `LIMIT` | N/A | 20 | Fixed page size. | DERIVED |
| Q1 | `OFFSET` | N/A | (`effective_page` - 1) * 20 | Page `offset`. | DERIVED |
| Q2 | `SELECT` | notifications AS n | `COUNT(*)` | Count matching rows. | DERIVED |
| Q2 | `WHERE` | notifications AS n | `n.`user_id` = :principal_id` | Same owner predicate as Q1. | DERIVED |
| Q2 | `WHERE` | notifications AS n | `n.`is_read` = FALSE` | Add only for `unread_only`=true. | DERIVED |

## Mutation Matrix

| API operation | Mutation target | Status |
|---|---|---|
| API #43 `GET` list | N/A | N/A — READ-ONLY API; #44/#45 remain separate operations. |

## Response Source Matrix

| Response field | Candidate source | Transform | Status |
|---|---|---|---|
| `data.`items`[].id` | notifications.id | Direct | DIRECT candidate |
| `data.`items`[].title` | notifications.`title` | Direct | DIRECT candidate |
| `data.`items`[].content` | notifications.`content` | Direct | DIRECT candidate |
| `data.`items`[].created_at` | notifications.`created_at` | ISO-8601 needs timezone rule | SOURCE_REQUIRED for timezone |
| `data.`items`[].channels` | None | No mapping from `type` | SOURCE_REQUIRED |
| `data.`items`[].status` | None | No mapping from `type` or `is_read` | SOURCE_REQUIRED |
| `data.`items`[].read_at` | None | Do not derive from boolean | SOURCE_REQUIRED |
| `data.`items`[].scheduled_at` | None | No physical column | SOURCE_REQUIRED |
| `data.pagination.page` | page input | Omitted defaults to 1 | DERIVED |
| `data.pagination.size` | Fixed value 20 | No size request field | DERIVED |
| `data.pagination.total` | Q2 `COUNT(*)` | Same owner/unread predicates as Q1 | DERIVED |
| `data.pagination.total_pages` | `total` and size | ceil(`total`/20); zero when `total`=0 | DERIVED |

## Tables read/write

- Candidate read table: notifications.
- Request identity source: authenticated `Student` principal.
- users is not queried by this API proposal; user ID is taken from `JWT`.
- Tables write: N/A.
- No physical `NotificationRecipient` table was found.

## Conflicts and assumptions

| ID | Finding | Treatment |
|---|---|---|
| C1 | AC-20 says `NotificationRecipient`; physical guide/ERD/DDL only have nullable notifications.`user_id`. | Use direct recipient rows as DERIVED candidate; NULL/broadcast semantics remain SOURCE_REQUIRED. |
| C2 | Required `channels`/`status` and optional `read_at`/`scheduled_at` lack physical fields. | Preserve catalog; do not equate `type`/`is_read` to contract fields. |
| C3 | page exists but size is absent from request. | Propose page 1, fixed size 20, newest-first as DERIVED, based on API #10 precedent. |
| C4 | DDL `created_at` is `TIMESTAMP` without timezone. | Keep response serialization timezone open. |
| C5 | API #44 diagram updates `read_at`, but DDL has only `is_read`. | Defer read timestamp reconciliation to macro review after #44/#45 DDs. |
| C6 | API guideline error body says data:null; current helper fallback emits {}. | Record runtime/design discrepancy; API #43 has no route using the helper. |

## Verification

- Required folder/file set, contract/error table, Markdown/`JSON`/link checks are recorded in VERIFICATION_REPORT.md.
- This DD is design-only. Runtime tests were not run.
- Macro review of APIs #43–#45 remains open until the #44 and #45 DDs exist.
