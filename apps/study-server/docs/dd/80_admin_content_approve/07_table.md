---
title: "Định nghĩa table"
order: 7
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical tables | `contents`; `content_review_audit_logs` |
| Logical table | Content moderation decision |
| Operation | Lock + UPDATE + audit INSERT trong một transaction |
| Data Mapping step | Steps 2–6; xem [Data Mapping](./05_Data_Mapping.md#2-get-và-khóa-content) |
| Schema status | Legacy BIGINT candidate; migration 011 là DERIVED, live chưa verify |

> AC-33 trực tiếp yêu cầu approval kèm audit. Legacy `contents` là checked-in runtime candidate. `content_review_audit_logs` là physical fallback DERIVED. V1-PILOT UUID `content_review_decisions` không map trực tiếp vào Content ID/JWT subject hiện tại.

## Read mapping — `contents`

| Column | Kiểu | Ràng buộc | Sử dụng |
|---|---|---|---|
| `id` | BIGINT/BIGSERIAL | PK | Khóa từ `content_id`; equality check sau query. |
| `course_id` | BIGINT | FK `courses.id`, NOT NULL | Response `course_id`. |
| `content_type` | TEXT | NOT NULL | Response `content_type`; không tự giới hạn enum. |
| `title` | TEXT | NOT NULL | Response `title`. |
| `payload` | JSONB | NOT NULL, object check | Response `payload`; validate object shape. |
| `status` | TEXT | NOT NULL | Lock precondition `PENDING_REVIEW`; target `APPROVED`. |
| `parent_id` | BIGINT | Nullable | Response `parent_id`; NULL bị omit. |
| `content_order` | INTEGER | NOT NULL | Map sang response `order`. |
| `deleted_at` | TIMESTAMP | Nullable | Row active khi NULL. |

## Update mapping — `contents`

| Predicate | Assignment | Result |
|---|---|---|
| `id=:content_id AND deleted_at IS NULL AND status='PENDING_REVIEW'` | `status='APPROVED'` | `RETURNING` tám field reusable Content; không update `content_versions`. |

`PENDING_REVIEW` eligibility và `APPROVED` target là fallback DERIVED theo AC-33/#78 và API #52 current transition. Exact revision identity vẫn chưa có input contract.

## Insert mapping — `content_review_audit_logs`

| Column | Kiểu | Khóa/ràng buộc | Value/API #80 |
|---|---|---|---|
| `id` | BIGSERIAL | PK | DB-generated. |
| `content_id` | BIGINT | FK `contents.id`, NOT NULL, RESTRICT | Path ID đã parse. |
| `actor_user_id` | BIGINT | FK `users.id`, NOT NULL, RESTRICT | Numeric JWT `sub` từ shared ADMIN guard. |
| `previous_status` | TEXT | NOT NULL | `PENDING_REVIEW`. |
| `new_status` | TEXT | NOT NULL | `APPROVED`. |
| `reason` | TEXT | Nullable | `NULL` cho approve; API #81 hiện ghi rejection reason vào decision row riêng. |
| `recorded_at` | TIMESTAMPTZ | NOT NULL, default current timestamp | DB timestamp. |

Indexes: `(content_id, recorded_at DESC, id DESC)` và `(actor_user_id, recorded_at DESC, id DESC)` hỗ trợ history lookups. Đây là DERIVED candidate, chưa có live performance evidence.

## Transaction boundary

- Lock current active row.
- Nếu không tồn tại/đã xóa → 404; nếu status không pending → 422.
- Update rồi validate returned Content; append audit với old/new state và actor.
- Commit chỉ sau khi audit và projection thành công; lỗi query/mapping/audit/commit phải rollback.
- API #81 được wire locally trong task riêng và dùng cùng audit relation để lưu reason với trạng thái `REJECTED`; mapping này là DERIVED, còn chờ owner review và live schema verification.
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
