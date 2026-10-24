---
title: "Overview"
order: 2
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #94 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | PUT |
| Endpoint | /api/v1/admin/notifications/{notification_id} |
| Purpose | Cập nhật notification draft/scheduled theo catalog; điều kiện và field cụ thể chưa được AC-36 định nghĩa. |
| Consumer/Actor | Admin có notification-management permission |
| Authentication | Bearer JWT |
| Authorization | Catalog nêu role Admin; AC-36 yêu cầu permission. Study chưa có Admin guard/policy được xác minh. |
| Direct request | Path notification_id:int64!; catalog không khai báo query/body. |
| Direct response | HTTP 200 DESIGN_RESOURCE_UPDATED, ApiEnvelope<Notification>. |
| Current implementation | UNWIRED / NOT_FOUND: không có route/module/test API #94 trong scoped Study source scan. |
| Transaction | Không được mô tả bởi catalog hoặc diagram. |
| Side effects | Diagram yêu cầu UPDATE Notification và reload management; scheduler/delivery effects không được mô tả. |
| DD status | Draft — Needs Confirmation |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, Notification, NotificationChannel, NotificationStatus, AudienceSegment.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin permission, postcondition và các API notification.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh UPDATE gọi #94 rồi reload notification management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT notification row; design candidate, không xác nhận live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID learner notifications/deliveries, mô hình riêng.
- [DD #92](../92_admin_notifications_list/02_Overview.md) và [DD #93](../93_admin_notifications_create/02_Overview.md) — response/schema gaps, audience contract và Admin notification model.
- [Current Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).

## Tables read

| Relation/entity | Candidate fields | Basis/status |
|---|---|---|
| Legacy notifications | id, user_id, sender_id, title, content, type, is_read, created_at | BIGINT row candidate only; no campaign association, channels, status or scheduled_at. |
| V1-PILOT notifications | UUID id, learner/category/title/body/read_at/created_at fields | Learner-scoped model, not the Admin campaign model. |
| V1-PILOT notification_deliveries | UUID notification relation, channel and delivery status | Different ID/grain; not interchangeable with Admin recipient association. |
| Logical NotificationRecipient | Recipient association implied by AC-36/#93 audience | No approved physical relation found. |

## Tables write

Diagram calls for UPDATE Notification. No physical table is approved for this Admin resource. A recipient-association replacement appears only in the DERIVED request proposal and has no compatible physical target identified.

## Mục chú ý

- Catalog #94 declares a path-only request. The body below is not a direct contract.
- The catalog notification description mentions draft/scheduled, but no status enum or transition table defines eligibility.
- NotificationChannel, NotificationStatus and AudienceSegment value sets are not present in reviewed sources.
- Legacy notifications.user_id holds one nullable recipient on a row; it does not prove campaign-level recipient membership.
- V1-PILOT notification_deliveries is learner/delivery-scoped and uses UUID identity. Do not merge it into the legacy BIGINT model.
- No scheduler, queue, operation lifecycle or rescheduling contract was found. The API must not be described as dispatching or cancelling delivery work.
- API #93 Operation response and ID bridge remain unresolved after the AC-36 document macro-review.

## Assumptions

- DERIVED proposal for review: full replacement body reuses #93 audience/title/content/channels fields and adds nullable scheduled_at to express draft versus scheduled intent.
- DERIVED proposal for review: exactly one of recipients or segment; only conceptual Draft/Scheduled targets may be edited; null schedule means Draft and a future schedule means Scheduled.
- The proposed lifecycle names are explanatory labels only. They do not assert values in NotificationStatus.
- No proposal is treated as approved runtime behavior.

## Conflicts

| Source A | Source B | Conflict | Impact |
|---|---|---|---|
| Catalog #94 | AC-36 update intent | Catalog lists path only; diagram says UPDATE Notification | Body and editable field set are unresolved. |
| Catalog Notification schema | Legacy notifications | No channels/status/scheduled_at/read_at projection | Cannot fully map response or mutation to legacy row. |
| Admin campaign intent | V1-PILOT notification/delivery model | UUID learner/delivery grain differs from BIGINT Admin ID | Do not use pilot relation as Admin persistence target. |
| #93 request | #94 scheduled/draft purpose | #93 has no action or scheduled_at; #94 has no direct body | Create/update lifecycle handoff remains open. |
| #93 response/Operation notes | #18 and #96 identifiers | Notification ID int64 and Operation ID UUID/int64 discrepancy | Keep unresolved for group review; #94 adds no bridge. |
| AC permission | Current Study auth source | Admin notification-management guard not verified | Authorization implementation remains source-required. |

## Security note

- Authenticate Bearer JWT and authorize Admin plus notification-management permission before target lookup or mutation.
- Do not accept actor identity, role or permission from request body/query.
- Do not expose recipient personal data or provider/queue internals in the Notification response.
- Permission claim, tenant/global scope and actor audit mapping require an approved policy source.

## Performance note

- AC-36 does not specify recipient batch limits, audience expansion, scheduler latency or update SLA.
- No index, queue operation or write batching is inferred.
- A full recipient replacement could be large; cardinality/transaction strategy requires owner and schema confirmation.

## Contract interpretation

- DIRECT: method/path, Bearer JWT/Admin, path type, no catalog body/query, response envelope, HTTP 200 and exact five error codes; AC-36 UPDATE Notification/reload intent.
- DERIVED: full replacement fields, audience XOR, schedule behavior and conceptual editable states.
- SOURCE_REQUIRED: enum values, Admin policy, target persistence, transaction, audit and scheduler effects.
- DISCREPANCY: update intent without body; logical Notification fields without an approved compatible Admin schema.

## Tình trạng nhóm AC-36

AC-36 macro-review #92–#96 is complete at document level with open questions. #94 body/schedule remain DERIVED; the #93 Operation ID bridge and scheduler state remain unresolved. See [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

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
