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
| Purpose | Cập nhật Notification theo nhánh UPDATE; body trực tiếp không được catalog khai báo. |
| Consumer/Actor | Admin; AC-36 yêu cầu notification-management permission. |
| Authentication | Bearer JWT qua shared ADMIN role guard. |
| Authorization | Fallback kiểm tra role ADMIN; finer notification-management permission chưa được xác minh. |
| Direct request | Path `notification_id:int64!`; catalog/diagram không khai báo body hoặc query. |
| Runtime fallback | Strict `{title, content}`; chỉ notification có delivery rows và mọi status `QUEUED`. Đây là DERIVED. |
| Direct response | HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Notification>`. |
| Current implementation | Wired trong Study source; fake-DB HTTP tests đã chạy. Live schema/deployment chưa xác minh. |
| Transaction | Khóa notification rồi delivery rows; update text và projection trong một transaction. |
| Side effects | Chỉ update `notifications.title/content`; không gọi provider/scheduler, không thay audience/delivery. |
| DD status | Draft — Needs Confirmation |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, Notification, NotificationChannel, NotificationStatus, AudienceSegment.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — UPDATE Notification rồi reload management.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) và [migration 009](../../../../../infra/postgres/study-server/migrations/009_notification_delivery_outbox.sql) — candidate BIGINT notification/outbox columns.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID learner notification model riêng.
- [API #92](../../../app/modules/admin/api_92_admin_notifications_list/) và [API #93](../../../app/modules/admin/api_93_admin_notifications_create/) — shared response projection và legacy recipient/delivery grain.
- [API #94 route](../../../app/api/v1.py), [module](../../../app/modules/admin/api_94_admin_notifications_update/) và [tests](../../../tests/modules/admin/api_94_admin_notifications_update/).

## Tables read and written

| Relation/entity | Candidate fields | Basis/status |
|---|---|---|
| Legacy notifications | id, user_id, sender_id, title, content, type, is_read, created_at | Checked-in BIGINT candidate; live schema unverified. Runtime locks by id and updates title/content only. |
| Legacy notification_deliveries | notification_id, channel, status | Migration 009 candidate. Runtime locks and reads rows; requires at least one row and all statuses QUEUED. |
| V1-PILOT notifications/deliveries | UUID learner and delivery model | Separate grain; not used by this route. |
| Logical NotificationRecipient | Audience association implied by AC-36/#93 | No physical relation is changed by #94. |

## Mục chú ý

- Catalog/diagram still declare no request body. Runtime body is a local DERIVED fallback, not an approved contract change.
- `QUEUED` is an outbox delivery status, not a proven Draft/Scheduled Notification lifecycle state.
- `channels` in response are projected from existing delivery rows; request cannot alter them.
- Current shared auth verifies ADMIN role only. AC-36's finer permission remains open.
- No scheduler, provider dispatch, Operation bridge, campaign relation, or live Admin schema is established here.

## Conflicts

| Source A | Source B | Conflict | Handling |
|---|---|---|---|
| Catalog/diagram | Wired runtime | Direct request is path-only; local runtime requires `{title, content}`. | Keep DD Draft; mark body DERIVED. |
| Draft/scheduled prose | Legacy outbox | No Notification status/schedule column exists; outbox only records delivery state. | Require all delivery rows QUEUED as a narrow fallback; do not call this Draft/Scheduled. |
| AC permission | Shared Study guard | Finer notification-management permission is not implemented/source-verified. | Use shared ADMIN role; retain policy question. |
| Admin logical schema | Legacy BIGINT/V1-PILOT UUID | Neither is an approved campaign model. | Use only checked-in legacy candidate columns and report live schema as unverified. |

## Contract interpretation

- DIRECT: method/path, Bearer/Admin, path type, response envelope, HTTP 200 and exact five error codes; AC-36 UPDATE/reload intent.
- DERIVED runtime fallback: required strict `title`/`content`, nonblank strings, title max 200, positive int64 path, and editability only while every existing delivery row is QUEUED.
- PRESERVED: existing recipient, channels, delivery rows and `created_at`; no scheduling/provider action.
- OPEN: owner approval, Admin permission key, deployed schema, campaign/recipient semantics, schedule and lifecycle policy.

## Tình trạng nhóm AC-36

AC-36 macro-review remains `VERIFIED_WITH_OPEN_QUESTIONS`. APIs #92–#95 are locally wired and fake-DB tested; #96 remains unwired. Shared Admin model, lifecycle/retention, fine-grained permission and Operation decisions remain open. See [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).

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
