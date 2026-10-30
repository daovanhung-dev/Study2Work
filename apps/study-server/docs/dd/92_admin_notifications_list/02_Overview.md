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
| Consumer/Actor | Admin có notification-management permission theo AC-36 |
| Authentication | Bearer JWT |
| Authorization | Runtime dùng role `ADMIN`; permission chuyên biệt và visibility scope chưa được xác nhận. |
| Basis | Endpoint/query/status/errors DIRECT; Page response, legacy/outbox projection và pagination DERIVED. |
| Status | Draft — Needs Confirmation |
| Current implementation | `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS`: route/module/test API #92 đã wired trong Study. |
| Transaction | Read-only; không commit khi thành công; rollback khi query hoặc mapping lỗi. |
| Side effects | Không ghi DB hoặc gọi delivery provider. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #92–#96, `Notification`, `NotificationDelivery`, `Operation`, `Page<T>`.
- [AC/API index, AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin permission, postcondition và năm endpoint.
- [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #92 query notifications rồi rẽ nhánh Create/Update/Delete/Status.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy notification row, recipient/sender relations và delivery-schema status.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) và migration 009 — BIGINT notifications/delivery outbox candidate; không chứng minh live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID learner notification/delivery riêng, không gộp với legacy.
- [API #43 Student notification list](../43_users_me_notifications/02_Overview.md), [API #63 Mentor create](../63_mentor_notifications_create/02_Overview.md), [API #64 Mentor status](../64_mentor_notifications_status/02_Overview.md) — precedent có giới hạn.
- [AC-36 create/status rows #93/#96](../../../../../docs/lists/list_api.md) và [macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md) — các discrepancy response/schema/permission vẫn mở.
- Current [Study router](../../../app/api/v1.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; appendix template được giữ nguyên.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `notifications` | `id`, `title`, `content`, `created_at` | BIGINT design candidate; row grain là notification theo recipient, không phải campaign đã duyệt. |
| Legacy `notification_deliveries` | `notification_id`, `channel`, `status`, `updated_at` | Migration 009/API #63 outbox candidate; mỗi row theo notification/channel. |
| V1-PILOT `notifications` | UUID `id`, `learner_id`, `title`, `body`, `read_at`, `created_at` | Learner-scoped model; không dùng cho runtime fallback #92. |
| V1-PILOT `notification_deliveries` | UUID notification FK, per-channel `status` | Mô hình delivery riêng, không tương thích BIGINT notification ID. |

## Tables write

Không có — API #92 là GET/read-only; không INSERT/UPDATE/DELETE và không gọi provider.

## Mục chú ý

- Catalog response trực tiếp là `ApiEnvelope<Notification>`; runtime trả `ApiEnvelope<Page<Notification>>` theo list intent/query `page`. Đây là `DISCREPANCY / DERIVED`, không phải catalog approval.
- Runtime chỉ liệt kê legacy notification có ít nhất một delivery row để đủ `channels` và `status`; mỗi item giữ grain một `notifications.id`.
- `channels` lấy từ outbox; `status` aggregate dùng thứ tự ưu tiên của API #64: `QUEUED`, sau đó `FAILED`, rồi `SENT`. Mapping này là local fallback, chưa phải enum rule được duyệt cho Admin.
- Bộ lọc status/channel so sánh exact với aggregate; không trim, đổi case hay áp enum allowlist.
- Page bắt đầu từ 1, mặc định 1, fixed size 20, sort `created_at DESC, id DESC`; các lựa chọn này là `DERIVED`.
- `read_at` và `scheduled_at` bị bỏ qua vì schema legacy không có hai timestamp này; không đổi `is_read` hoặc `expires_at` sang timestamp.
- Actor/recipient IDs, legacy `type`, `is_read`, `operation_id` và provider data không được trả.
- 503 chỉ áp dụng cho `OperationalError` hoặc connection-invalidated DB error; lỗi SQL/mapping khác trả 500. 422 cho page không hợp lệ là fallback ngoài error set trực tiếp.

## Assumptions

- API list được triển khai thành Page, không trả một Notification đầu tiên hoặc singleton giả.
- Admin role hiện có được dùng làm local authorization fallback; permission code/tenant scope còn SOURCE_REQUIRED.
- Legacy/outbox candidate được dùng chỉ vì BIGINT ID và field/channel/status có bằng chứng cục bộ trong #63/migration 009; live availability chưa xác nhận.
- API #92 không giải quyết Notification-vs-Operation ID bridge của #93.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #92 | API name/AC-36/page query | Response trực tiếp là `Notification` đơn nhưng endpoint có ý nghĩa list | Runtime `Page<Notification>` là fallback; cần owner/catalog quyết định. |
| `Notification` schema | Legacy `notifications`/outbox | Legacy thiếu `read_at`/`scheduled_at`; channel/status nằm ở delivery grain | Runtime chỉ trả fields có projection hợp lệ; scheduled/read timestamps bị omit. |
| AC-36 #93 | Operation tracking summary | #93 response Notification so với Operation | Để mở ở macro-review; #92 không suy ID bridge. |
| Catalog 503 | AC-36 list flow | Catalog có 503 nhưng diagram chỉ ghi query | Runtime ánh xạ lỗi kết nối DB sang 503 theo tên code; trigger chưa được owner duyệt. |

## Security note

- Runtime xác thực Bearer/JWT và role `ADMIN` trước khi parse page hoặc query.
- AC-36 permission chuyên biệt và global/tenant visibility chưa có policy source; dùng role ADMIN chỉ là `DERIVED` fallback.
- Không nhận role/actor ID/quyền từ query/body; không trả recipient/sender IDs, provider IDs, raw SQL hoặc stack trace.

## Performance note

- Runtime chạy một count và một page query, dùng chung filter/predicate; page size cố định 20 và sort ổn định.
- AC-36 không nêu latency/SLA/cache; không có claim về query plan/index/live performance.

## Contract interpretation

- `DIRECT`: method/path, Admin Bearer, query names/types, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, catalog response type và exact errors 401/403/503/500.
- `DERIVED`: Page cardinality, page defaults/size/order, legacy/outbox projection, status/channel mapping, empty result, 422 page validation và DB connection→503.
- `SOURCE_REQUIRED`: Admin campaign grain, permission scope, Notification enum approval, scheduled/read semantics, live DB/migration state.
- `DISCREPANCY`: list intent so với singleton response; Admin Notification fields so với legacy/pilot schemas; #93 Notification so với Operation.

## Tình trạng nhóm AC-36

- Macro-review #92–#96 là `VERIFIED_WITH_OPEN_QUESTIONS`; #92–#95 hiện wired/tested locally, #96 còn unwired, và các owner decisions của group chưa được giải quyết. Xem [báo cáo nhóm](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md).
- Flow trực tiếp: #92 query → #93 create/send → #94 update → #95 delete/cancel → #96 status. Operation polling xuất hiện riêng và chưa có Admin #93 ID bridge.
- Không dùng #92 để suy ra campaign schema, recipient grouping, delivery lifecycle hoặc operation result.

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
