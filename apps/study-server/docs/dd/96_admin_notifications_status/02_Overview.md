---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #96 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | `GET` |
| Endpoint | `/api/v1/admin/notifications/{notification_id}/status` |
| Purpose | Admin xem trạng thái delivery của một notification. |
| Actor | Admin; AC-36 yêu cầu notification-management permission. |
| Authentication | Bearer JWT |
| Input | `notification_id:int64!` trong path; không body/query. |
| Direct response | `ApiEnvelope<Notification>` |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| Current implementation | `UNWIRED / NOT_FOUND`: không có route, module hoặc test #96 trong Study source. |
| Mutation | N/A — read-only API. |

## Nguồn

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #96, `Notification`, `NotificationDelivery`, `OperationStatus`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-36 actor, precondition, postcondition và API #92–#96.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — status branch #96, bước đọc delivery aggregate và reload management.
- [DD #92 list](../92_admin_notifications_list/02_Overview.md), [#93 create](../93_admin_notifications_create/02_Overview.md), [#94 update](../94_admin_notifications_update/02_Overview.md), [#95 delete/cancel](../95_admin_notifications_delete/02_Overview.md) — connected AC-36 contracts and open questions.
- [DD #64 Mentor notification status](../64_mentor_notifications_status/02_Overview.md) — precedent về delivery intent và response/schema mismatch; không chuyển Mentor policy sang Admin.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) và [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — schema candidates, không xác nhận live/Admin persistence.
- Current [Study router](../../../app/api/v1.py) và [middleware](../../../app/core/middleware.py) — source wiring và error-code dispatch hiện tại.
- [Study DD workflow](../../../../../.agents/server-study/workflows/README.md) và [Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — Markdown-only Study deliverable, 8 sheet roles.

## Đọc/ghi dữ liệu

- Logical resource cần đọc: Admin Notification theo `notification_id`; physical relation/grain chưa được duyệt.
- Logical delivery summary trong catalog: `NotificationDelivery` có `notification_id`, `status`, `queued`, `sent`, `failed`; catalog không quy định đây là response của #96.
- Ghi dữ liệu/provider: không có; API #96 là GET/read-only.

## Contract interpretation

- `DIRECT`: method/path, Admin Bearer, path int64 bắt buộc, không body/query, `ApiEnvelope<Notification>`, HTTP 200 và đúng bốn lỗi catalog.
- `DIRECT` từ AC-36: sau nhánh STATUS có bước “Đọc delivery aggregate”, rồi reload notification management.
- `DISCREPANCY`: bước aggregate không có physical relation/query/grain; response Notification không có queued/sent/failed hoặc per-channel delivery results.
- `DERIVED` cần duyệt: nếu tổng hợp delivery vào response, chỉ có thể chiếu qua `Notification.status` hiện hữu mà không đổi shape; rule projection và status token vẫn chưa có nguồn.
- `SOURCE_REQUIRED`: Admin data model, NotificationChannel/NotificationStatus/OperationStatus values, aggregation policy, permission predicate, empty/missing behavior.

## Xung đột và giới hạn

| Nguồn A | Nguồn B | Xung đột | Tác động |
|---|---|---|---|
| AC-36 diagram | Catalog #96 | Diagram đọc delivery aggregate; catalog trả `Notification`. | Không có contract cho counts/per-channel results. |
| Reusable `NotificationDelivery` | Reusable `Notification` | Delivery summary có counts nhưng không phải response type của #96. | Không thêm các field `queued/sent/failed` vào `Notification`. |
| Legacy `notifications` | Notification schema | Legacy có `is_read` nhưng thiếu `channels/status/read_at/scheduled_at`. | Không thể map response đầy đủ từ row legacy. |
| V1-PILOT delivery | BIGINT Admin contract | Pilot IDs là UUID và delivery grain khác. | Không ghép schema hoặc ID. |
| Catalog #93 | Operation tracking summary | Notification response so với Operation response/UUID tracking. | Giữ thành open issue của macro-review AC-36. |

## Tình trạng AC-36

Macro-review #92–#96 đã hoàn tất ở mức tài liệu với trạng thái `VERIFIED_WITH_OPEN_QUESTIONS`; xem [AC-36_MACRO_REVIEW.md](./AC-36_MACRO_REVIEW.md). Các quyết định về list/create/update/delete/status, Operation bridge và schema dùng chung vẫn mở.
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

