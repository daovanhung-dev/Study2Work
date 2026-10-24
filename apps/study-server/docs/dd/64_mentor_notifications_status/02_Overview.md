---
title: "Overview"
order: 2
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #64 |
| Module | MENTOR / TEACHING & SUPPORT — AC-25 |
| Method | `GET` |
| Endpoint | `/api/v1/mentor/notifications/{notification_id}/status` |
| Purpose | Đọc trạng thái phát của một notification để UI hiển thị sau khi #63 yêu cầu gửi. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor theo catalog; phạm vi xem từng notification chưa được xác định. |
| Basis | Method/path/input/response/status/errors DIRECT từ catalog; bước đọc delivery status DIRECT từ AC-25; physical query và permission predicate SOURCE_REQUIRED. |
| Status | `Draft — Needs Confirmation` |
| Current runtime state | `UNWIRED / NOT_FOUND` — chưa có route, query, module hoặc delivery provider/test cho API #64 trong Study source. |
| Transaction | N/A — API chỉ đọc; snapshot/consistency contract chưa được quy định. |
| Side effects | Không có mutation hay provider call được đặc tả; đọc trạng thái đã lưu là mục tiêu của flow. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #18, #62–#64, ApiEnvelope, Operation, Notification, NotificationDelivery, Payment.
- [AC/API index, AC-25](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và ba API #62–#64; API #18 cũng được liệt kê trong tracking summary.
- [AC-25 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — #62 roster → #63 tạo/phát → #64 đọc delivery status; node #18 không có edge.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — notifications và trạng thái DESIGN_ONLY cho #63–#64.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT notification ID, recipient/sender, `is_read`; không có delivery table.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID notification và append-only `notification_deliveries`; không được coi là live schema.
- [API #18 Operation overview](../18_operations/02_Overview.md) và [open questions](../18_operations/OPEN_QUESTIONS.md) — operation ID, owner, lifecycle, result và persistence còn bất nhất.
- [API #62 recipient overview](../62_mentor_course_students/02_Overview.md) và [open questions](../62_mentor_course_students/OPEN_QUESTIONS.md) — roster projection và ID chưa chốt.
- [API #63 create notification overview](../63_mentor_notifications_create/02_Overview.md), [response](../63_mentor_notifications_create/04_Response.md), [open questions](../63_mentor_notifications_create/OPEN_QUESTIONS.md) — Operation response chưa bàn giao notification_id.
- [API #43 notification list](../43_users_me_notifications/02_Overview.md) và [API #45 read-all](../45_notifications_read_all/02_Overview.md) — trạng thái đã đọc khác trạng thái delivery.
- Current [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint trong [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- `Notification` — logical resource cần tra notification ID; physical candidate legacy có `id`, `user_id`, `sender_id`, `is_read`, không có delivery state.
- `NotificationDelivery` — logical delivery summary trong reusable schema; pilot có delivery attempts nhưng UUID identity, chưa phải query source được duyệt.
- `Operation` — reusable response schema; Study physical table, ownership relation, enums và lifecycle chưa có nguồn.

## Tables/entities ghi

N/A — READ-ONLY API. API #64 không tạo notification, recipient, delivery hay Operation.

## Mục chú ý

- Giữ direct contract: path `notification_id:int64!`, response `ApiEnvelope<Operation>`, 200 `DESIGN_RESOURCE_RETRIEVED`, đúng bốn lỗi 401/403/404/500.
- AC-25 yêu cầu đọc delivery status; `Operation` biểu diễn job và không có mapping từ int64 notification ID. `NotificationDelivery` gần với intent hơn nhưng không phải response được khai báo.
- API #63 trả Operation UUID, không công bố `notification_id:int64`; client chưa có ID đúng loại để gọi #64.
- Không dùng `notifications.is_read` làm trạng thái gửi; không gọi provider trong GET để tính lại trạng thái.
- Pilot `notification_deliveries` lưu attempt rows, không có recipient ID; không diễn giải số attempt thành số người nhận đã gửi/thất bại.

## Đề xuất DERIVED cần xác nhận

| Chủ đề | Đề xuất đơn giản | Trạng thái |
|---|---|---|
| Mục tiêu #64 | Dùng #64 để trả `NotificationDelivery`; dùng #18 riêng cho trạng thái Operation/job. | DERIVED — cần sửa catalog/diagram và thống nhất với #63. |
| ID handoff | #63 phải cung cấp `notification_id:int64` đã được lưu; giữ `operation_id:uuid` riêng cho #18. | DERIVED — result schema hiện không có mapping. |
| Delivery status | Chốt enum và cách tổng hợp theo recipient/channel; không dùng `OperationStatus` nếu lifecycle khác. | SOURCE_REQUIRED — chưa có trạng thái/aggregate đã duyệt. |
| Permission | Chỉ Mentor có quyền trên notification/course được xem; chọn sender/owner relation sau khi schema và policy được duyệt. | DERIVED — không tự áp dụng candidate `sender_id`. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #64 | AC-25 diagram | Response là `Operation`, nhưng flow cần delivery status theo `notification_id`. | Không có delivery counts/state trong response direct. |
| #64 path | #63 response + #18 | #64 cần int64 notification ID; #63 trả Operation UUID và #18 dùng operation ID; không có cầu nối được công bố. | Client không thể nối create → delivery status một cách chắc chắn. |
| Reusable schemas | V1-PILOT DDL | `NotificationDelivery.status` là OperationStatus; pilot dùng `notification_status`; các ID và channel model khác nhau. | Không tự map enum hoặc vật lý schema. |
| Legacy notifications | AC-25 delivery | Legacy có `is_read` nhưng không có send status/delivery table. | Read receipt không thể thay delivery state. |
| API #18 sources | Operation tracking summary / AC diagrams | Row #18 dùng int64 nhưng quy ước/schema/diagram dùng UUID; owner/Admin access cũng chưa thống nhất. | Job polling vẫn là contract riêng cần macro-review. |
| API guidelines | Current middleware/helper | Error guideline `data:null`; helper mặc định `{}`; path #64 chưa thuộc design allowlist. | Future wiring discrepancy, không phải runtime #64. |

## Security note

- Xác thực Bearer và Mentor role trước khi truy vấn trạng thái.
- Không trả status hoặc số liệu cho notification ngoài phạm vi Mentor được phép.
- Không quyết định sender/owner predicate hoặc 403/404 privacy order khi chưa có policy/schema.
- Không trả provider message ID, raw provider error, SQL, stack trace hay token.

## Reliability note

- GET chỉ đọc trạng thái đã lưu; không gọi Push/Email để tái gửi hoặc kiểm tra trực tiếp.
- Polling interval, cache, trạng thái pending khi chưa có delivery row và SLA chưa được quy định.
- Không kết luận delivery thành công từ việc #63 trả HTTP 202.
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
