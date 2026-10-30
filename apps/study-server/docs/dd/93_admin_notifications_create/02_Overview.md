---
title: "Overview"
order: 2
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #93 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | POST |
| Endpoint | `/api/v1/admin/notifications` |
| Purpose | Tạo notification cho recipients tường minh và xếp delivery vào local outbox |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Runtime dùng shared `ADMIN` role guard; permission riêng chưa có source |
| Basis | Catalog/diagram DIRECT; gửi ngay là DERIVED |
| Status | Draft — Needs Confirmation |
| Transaction | Một transaction cho toàn bộ notification và delivery rows; commit trước 202 (DERIVED) |
| Side effects | Ghi legacy BIGINT `notifications` và `notification_deliveries`; không gọi provider |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — #93, reusable schemas, Operation tracking.
- [AC-36 API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio).
- [DB guide](../../diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql).
- [Current router](../../../app/api/v1.py); [#92 DD](../92_admin_notifications_list/02_Overview.md); [#63](../63_mentor_notifications_create/05_Data_Mapping.md); [#64](../64_mentor_notifications_status/OPEN_QUESTIONS.md); [#18](../18_operations/OPEN_QUESTIONS.md).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).

## Tables read

- Audience membership and Operation store — SOURCE_REQUIRED; no approved source found.

## Tables write

- Logical Notification and recipient association per AC-36.
- No approved physical target; legacy notifications is only a partial candidate.

## Mục chú ý

- Catalog row and AC-36 node return ApiEnvelope<Notification> at HTTP 202.
- Operation tracking summary says Admin POST returns data: Operation.
- Diagram dispatches Push/Email if action is Send, but request has no action or scheduled_at.
- Immediate create-and-send is a DERIVED proposal, not approved behavior.
- AudienceSegment, NotificationChannel and NotificationStatus values are not defined in reviewed sources.
- Current source: route/module wired; fake-DB HTTP tests verify local behavior. Live DB/schema/worker chưa verify.
- Runtime chỉ nhận `recipients` tường minh; `segment` được trả 422 đến khi enum và audience predicate có nguồn.
- Ghi một legacy notification cho mỗi recipient, dùng chung UUID `operation_id`; thêm một delivery `QUEUED` cho mỗi recipient/channel.
- 202 xác nhận transaction/outbox đã commit, không xác nhận Push/Email đã gửi.

## Assumptions

- Các rule recipient, channel, nội dung, fan-out và metadata bổ sung là DERIVED fallback để chạy local; chưa thay thế contract catalog.
- Do not merge legacy BIGINT and V1-PILOT UUID notification models.

## Conflicts

- Notification vs Operation response and missing ID bridge: DISCREPANCY.
- Conditional Send vs absent action field: DISCREPANCY.
- API #18 operation_id is UUID in schema/diagram but int64 in its row.

## Security note

- Shared Bearer JWT guard yêu cầu role `ADMIN` trước parse body và query recipients.
- Không có fine-grained permission hoặc Admin-specific tenant scope được kiểm tra.

## Performance note

- Recipient/fan-out limits, provider dispatch rate, timeout and retry policy are unspecified.
---
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
