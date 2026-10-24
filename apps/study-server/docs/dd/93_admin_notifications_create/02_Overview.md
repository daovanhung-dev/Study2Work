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
| Purpose | Tạo/phát notification; action gửi chưa chốt |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin; AC-36 yêu cầu notification-management permission |
| Basis | Catalog/diagram DIRECT; gửi ngay là DERIVED |
| Status | Draft — Needs Confirmation |
| Transaction | Diagram tạo Notification + recipients; boundary SOURCE_REQUIRED |
| Side effects | Logical writes; Push/Email nếu Send; queue/provider chưa wired |

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
- Current source: UNWIRED / NOT_FOUND.

## Assumptions

- No inferred rule replaces the catalog contract.
- Do not merge legacy BIGINT and V1-PILOT UUID notification models.

## Conflicts

- Notification vs Operation response and missing ID bridge: DISCREPANCY.
- Conditional Send vs absent action field: DISCREPANCY.
- API #18 operation_id is UUID in schema/diagram but int64 in its row.

## Security note

- Authenticate Bearer and authorize Admin permission before resolving recipients.
- Permission key, claim mapping and caller identity are SOURCE_REQUIRED.

## Performance note

- Recipient/fan-out limits, dispatch rate, timeout and retry policy are unspecified.
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
