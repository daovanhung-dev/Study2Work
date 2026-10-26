---
title: "Overview"
order: 2
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #95 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | DELETE |
| Endpoint | /api/v1/admin/notifications/{notification_id} |
| Purpose | Xóa draft/cancel notification nếu policy cho phép; catalog không định nghĩa state machine. |
| Consumer/Actor | Admin theo catalog; AC-36 còn yêu cầu notification-management permission. |
| Authentication | Bearer JWT |
| Authorization | Local fallback dùng shared `ADMIN` guard; fine-grained permission và tenant/global scope chưa được wire. |
| Direct request | Path `notification_id:int64!`; không body/query. |
| Direct response | HTTP 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`. |
| DeleteResult | `id:int64`, `status:"deleted"`, `deleted_at:date-time`. |
| Direct errors | 401/403/404/422/500 đúng business codes trong catalog. |
| Current implementation | WIRED locally: raw-path route, shared ADMIN guard, signed-int64 parser, parent/delivery locks, queued-only delete, fake-DB tests. |
| Transaction | View locks parent then deliveries, deletes parent and commits after response projection; local fallback. |
| Side effects | Deletes one path-selected legacy notification. Candidate FK cascades its delivery rows. External scheduler/provider cancellation is not called or verified. |
| DD status | Draft — Needs Confirmation |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, DeleteResult and Notification contracts.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin permission, postcondition and notification APIs.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #95 → `DELETE/mark cancelled` → reload management.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) and [migration 009](../../../../../infra/postgres/study-server/migrations/009_notification_delivery_outbox.sql) — BIGINT recipient row; delivery FK has `ON DELETE CASCADE`, statuses are QUEUED/SENT/FAILED; no notification lifecycle/tombstone timestamp.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — separate UUID learner notification/delivery model; not used by #95.
- [DD #92](../92_admin_notifications_list/02_Overview.md), [DD #93](../93_admin_notifications_create/02_Overview.md), [DD #94](../94_admin_notifications_update/02_Overview.md) — local list/create/update fallbacks and remaining AC-36 questions.
- [DELETE precedent #90](../90_admin_quizzes_delete/02_Overview.md) — DeleteResult and DB-returned timestamp pattern.
- [Current Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).

## Tables/entities read

| Relation/entity | Candidate fields | Basis/status |
|---|---|---|
| Legacy `notifications` | id, user_id, sender_id, title, content, type, is_read, created_at, operation_id | Current #93/#94 fallback target; recipient-level BIGINT row; no lifecycle status or tombstone. Local #95 uses path id only. |
| Legacy `notification_deliveries` | id, notification_id, channel, status, queued_at, updated_at | Migration 009 candidate; channel/status checked; parent FK cascades on DELETE. Live deployment is unverified. |
| V1-PILOT notifications/deliveries | UUID notification/learner/delivery fields | Separate learner model; not queried or changed by #95. |
| Logical Notification lifecycle | Draft, Scheduled, cancelled/deleted, dispatch-started | Catalog/diagram do not define tokens or transitions; no lifecycle field exists in legacy row. |

## Tables write

Local fallback executes `DELETE FROM notifications WHERE id = :notification_id RETURNING id, CURRENT_TIMESTAMP AS deleted_at`. It first locks the parent and all its delivery rows. The checked-in legacy FK `notification_deliveries.notification_id ... ON DELETE CASCADE` removes only that parent's outbox rows in the same transaction. No DDL or migration is changed; checked-in DDL is not live-schema evidence.

## Mục chú ý

- Catalog purpose is conditional; AC-36 says `DELETE/mark cancelled` but does not specify draft/scheduled state or persistence method.
- Local `DERIVED` eligibility requires at least one valid delivery and every locked delivery status to be `QUEUED`; no delivery or any `SENT`/`FAILED` row returns the existing 422 code.
- The endpoint deletes the single recipient-level row identified by `notification_id`; it does not delete sibling rows sharing an `operation_id`.
- DeleteResult keeps direct literal `status="deleted"`; `deleted_at` maps to database `CURRENT_TIMESTAMP` from DELETE RETURNING, not a stored tombstone.
- The route uses shared `ADMIN` role auth. AC-36 fine-grained permission is `SOURCE_REQUIRED` and not locally enforced.
- #96 response is Notification without a delivery aggregate; eligibility reads the local legacy outbox and is `DERIVED`.
- #93 Operation response/ID bridge and batch cancellation semantics remain open. #95 accepts no Operation ID.
- No scheduler/provider cancellation call is present. Queued-only row state is not proof that an external send was prevented.

## Assumptions

- `DERIVED`: checked-in legacy BIGINT table/outbox are used because they are the model currently written by #93 and edited by #94.
- `DERIVED`: a notification is locally cancellable only when it has at least one delivery and every delivery is QUEUED; a missing delivery cannot establish eligibility.
- `DERIVED`: physical delete is the simplest mapping supported by the checked-in FK cascade and direct DeleteResult. The action affects one recipient row and its outbox only.
- `DERIVED`: deleted_at is the database transaction timestamp; a later repeated DELETE receives 404 because no tombstone remains.
- These choices are implementation fallbacks, not owner-approved lifecycle or retention policy. They do not prove live schema, worker behavior or external cancellation.

## Conflicts

| Source A | Source B | Conflict | Impact |
|---|---|---|---|
| Catalog #95 purpose | AC-36 DELETE node | Conditional draft delete/cancel vs generic DELETE/mark cancelled | Eligibility and physical-vs-logical lifecycle remain unresolved; local rule is DERIVED. |
| DeleteResult | Cancellation wording | Literal says deleted while diagram also says cancelled | Direct response shape retained; external cancellation is not claimed. |
| Legacy notification DDL | Desired lifecycle | No state, schedule or tombstone timestamp | Use current #93/#94 recipient row only as a local candidate. |
| Legacy delivery FK | History preservation proposal in earlier DD | FK cascades child delivery rows on hard delete | Local queued rows are removed; retention policy needs owner approval. |
| API #96 | Delivery-start eligibility | Response has no aggregate fields | #95 reads locked legacy outbox; this remains DERIVED. |
| AC permission | Current Study auth | Shared guard checks ADMIN role, no dedicated notification permission | Fine-grained permission remains SOURCE_REQUIRED. |

## Security note

- Authenticate Bearer JWT and apply the shared ADMIN role guard before path parsing or resource lookup.
- Do not expose target existence to unauthorized callers. Dedicated permission and tenant/global scope remain unverified.
- Do not log or return recipient PII, provider details, delivery IDs or SQL errors.
- Do not accept actor ID, permission, action override or Operation ID from request input.

## Performance and transaction note

- The view uses bounded row-locking reads for one parent and its delivery rows, ordered by channel, then one parent DELETE.
- Parent lock precedes child locks to match API #94 and block new FK-linked delivery inserts during the transaction. Live PostgreSQL lock behavior and any worker lock order are not verified here.
- Scheduler cancellation timeout/retry behavior is not implemented.

## Contract interpretation

- DIRECT: DELETE/path/auth role/path int64/no body or query/DeleteResult/HTTP 200/exact catalog 401/403/404/422/500; AC-36 permission and DELETE/mark-cancelled/reload intent.
- DERIVED: positive-int64 parsing to 422, shared ADMIN guard fallback, legacy recipient-row target, at-least-one/all-QUEUED eligibility, physical parent delete/cascade, DB timestamp and repeat-delete 404.
- SOURCE_REQUIRED: approved lifecycle/retention policy, dedicated Admin permission, live schema, scheduler/worker protocol, dispatch race and Operation bridge.
- DISCREPANCY: diagram uses cancellation language but response says deleted; external cancellation is not represented in response.

## Tình trạng nhóm AC-36

Macro-review #92–#96 remains `VERIFIED_WITH_OPEN_QUESTIONS`: #92–#95 are locally wired, while #96 remains unwired. The current fallbacks do not resolve catalog response/cardinality questions, shared schema, fine-grained permission, Operation bridge or live deployment. See [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
