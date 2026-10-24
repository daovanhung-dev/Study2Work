---
title: "Overview"
order: 2
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #92 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-36 |
| Method | GET |
| Endpoint | `/api/v1/admin/notifications` |
| Purpose | Admin tra cứu notification để chọn nhánh tạo/gửi, cập nhật, xóa/hủy hoặc xem delivery status. |
| Consumer/Actor | Admin có notification-management permission |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog; AC-36 yêu cầu notification-management permission. Study chưa có Admin guard/policy. |
| Basis | Endpoint/query/response/status/errors DIRECT; list cardinality, filter mapping và pagination chưa được xác nhận. |
| Status | Draft — Needs Confirmation |
| Current implementation | `UNWIRED / NOT_FOUND`: không có route, module hoặc test API #92 trong Study source. |
| Transaction | N/A — GET chỉ đọc. |
| Side effects | N/A — API không ghi DB hoặc gọi delivery provider theo diagram #92. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, `Notification`, `NotificationDelivery`, `Operation`, `Page<T>`.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin permission, postcondition và năm endpoint.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #92 query notifications rồi rẽ nhánh Create/Update/Delete/Status.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy notification row, recipient/sender relations và delivery-schema status.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT `notifications`; không chứng minh live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `notifications` và `notification_deliveries`; mô hình riêng, không gộp vào catalog BIGINT.
- [API #43 Student notification list](../43_users_me_notifications/02_Overview.md), [API #63 Mentor create](../63_mentor_notifications_create/02_Overview.md), [API #64 Mentor status](../64_mentor_notifications_status/02_Overview.md) — precedent và các schema/ID discrepancy.
- [AC-36 create/status rows #93/#96](../../../../../docs/lists/list_api.md) và reusable `Operation` — #93 response/tracking mismatch đã được rà trong macro-review; quyết định vẫn mở.
- Current [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; manifest hash trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Tables/entities đọc

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `notifications` | `id`, `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at` | BIGINT design candidate; mỗi row không chứng minh campaign/group projection. |
| V1-PILOT `notifications` | UUID `id`, `learner_id`, `category`, `title`, `body`, `read_at`, `created_at` | Mô hình learner-scoped; không phải nguồn runtime đã xác nhận cho Admin. |
| V1-PILOT `notification_deliveries` | UUID `notification_id`, `channel`, delivery `status` | Channel/status thuộc từng delivery; ID và grain khác API #92. |
| `NotificationRecipient` | Logical relation trong AC flow | Không có bảng legacy cùng tên được xác nhận. |

## Tables/entities ghi

Không có — API #92 là GET/read-only; không INSERT/UPDATE/DELETE và không gọi provider.

## Mục chú ý

- Catalog response trực tiếp là `ApiEnvelope<Notification>` dạng một object, trong khi API name, query `page` và AC-36 intent là danh sách. Giữ nguyên contract và nêu `ApiEnvelope<Page<Notification>>` như proposal riêng.
- `NotificationChannel` và `NotificationStatus` không có value set trong catalog. Không suy `notifications.type` thành `channels` hoặc `notification_deliveries.status` thành Notification-level `status`.
- Legacy `is_read` là boolean, không ánh xạ thành `status` hoặc `read_at`; pilot `read_at` gắn learner notification, không mặc nhiên là trạng thái đọc của Admin campaign.
- Không có `scheduled_at` trong hai DDL được rà soát. `expires_at` ở pilot không tương đương `scheduled_at`.
- AC-36 #92 node chỉ nêu query; 503 là error code trực tiếp trong catalog/diagram nhưng trigger dependency chưa được chỉ rõ.
- #93 row trả `Notification` ở HTTP 202, còn Operation tracking summary nói notification POST trả `Operation`; không giải quyết discrepancy trong #92.

## Assumptions

- Nếu owner duyệt response Page, đề xuất page bắt đầu 1, fixed size 20, sort `created_at DESC, id DESC`, theo cách phân trang design-only của API #43. Không chuyển rule Student ownership của #43 sang Admin.
- Nếu owner duyệt field mapping, status là exact match và channel là phần tử chính xác trong `channels[]`; enum/token/case/normalization vẫn cần xác nhận trước khi dùng.
- Mọi assumption là `DERIVED`; không dùng làm contract đã duyệt.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #92 | API name/AC-36/page query | Response là `Notification` đơn nhưng endpoint có ý nghĩa list | Chưa có collection/pagination contract. |
| `Notification` schema | Legacy `notifications` | Thiếu `channels`, `status`, `read_at`, `scheduled_at` | Không map đầy đủ từ legacy row. |
| `Notification` schema | V1-PILOT notifications/deliveries | UUID, learner grain, `body`, delivery-level channel/status; không tương thích BIGINT contract | Không ghép thành schema runtime. |
| AC-36 #93 | Operation tracking summary | POST response Notification so với Operation | Client flow/ID handoff remains open after document macro-review. |
| Catalog 503 | AC-36 list flow | Code có nhưng diagram chỉ ghi query | Trigger chưa biết; giữ `SOURCE_REQUIRED`. |
| API Guidelines | Current response helper | Guideline yêu cầu error `data:null`; helper mặc định `{}` | Conditional discrepancy nếu route được wire. |

## Security note

- Xác thực Bearer JWT và authorize Admin cùng notification-management permission trước khi đọc dữ liệu.
- Không nhận role, actor ID hoặc quyền từ query/body; API không có body.
- Không expose recipient IDs, provider message IDs, raw provider error, SQL hoặc stack trace trong list.
- Phạm vi Admin/tenant/recipient visibility chưa có policy source; không tự mở rộng thành mọi notification toàn hệ thống trong implementation.

## Performance note

- AC-36 không nêu sort, page size, total count, cache hoặc latency objective.
- Q1 chưa đủ source để chọn query/grouping an toàn; không tạo index/SLA hoặc giới hạn batch khi chưa có nguồn.
- Page-size 20 và sort trong proposal chỉ là `DERIVED`, không phải runtime fact.

## Contract interpretation

- `DIRECT`: method/path, Admin Bearer, query names/types, `ApiEnvelope<Notification>`, HTTP 200 và đúng errors 401/403/503/500.
- `DERIVED`: response Page thay thế, page=1/size=20, stable order và cách match filter sau khi schema được duyệt.
- `SOURCE_REQUIRED`: active table/grain, enum values, field projection, Admin permission policy, 503 trigger và empty-result semantics.
- `DISCREPANCY`: list intent so với singleton response; logical Notification so với legacy/pilot schemas; #93 response so với Operation tracking summary.

## Tình trạng nhóm AC-36

- Macro-review #92–#96 đã hoàn tất ở mức tài liệu với trạng thái `VERIFIED_WITH_OPEN_QUESTIONS`; xem [báo cáo nhóm](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md). Các quyết định về list cardinality, schema và #93 Operation bridge vẫn mở.
- Flow trực tiếp: #92 query → #93 create/send → #94 update → #95 delete/cancel → #96 status. Operation polling xuất hiện riêng trong index/summary và chưa có bridge ID được xác nhận ở Admin #93.
- Chưa dùng notification list để suy ra campaign schema, recipient grouping, delivery state hoặc operation result.

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
