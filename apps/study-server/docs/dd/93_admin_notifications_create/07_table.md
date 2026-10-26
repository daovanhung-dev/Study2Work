---
title: "Định nghĩa table"
order: 7
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `notifications` — checked-in legacy candidate |
| Logical table | Notification row cho một recipient; Admin campaign grain chưa được duyệt |
| Operation | INSERT local fallback; không phải schema/API approval |
| Data Mapping step | [Step 3](./05_Data_Mapping.md#step-3-create-notification-and-delivery-rows) |

## Insert mapping

**Áp dụng khi**

- Local runtime fallback ghi một hàng cho mỗi recipient vào legacy BIGINT table. DDL tồn tại trong `infra/postgres/study-server/DB.sql`; migration 009 bổ sung `operation_id`. Live schema chưa xác minh.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `id` | Notification ID | BIGSERIAL | N/A | N/A | Y | ● | Database generated | `RETURNING id` | 3 | Candidate allocator; int64 response |
| 2 | `user_id` | Recipient ID | BIGINT FK | N/A | N/A | N |  | One row per request recipient | `recipients[]` | 2, 3 | DDL allows NULL; runtime supplies ID |
| 3 | `sender_id` | Admin sender ID | BIGINT FK | N/A | N/A | N |  | Authenticated ADMIN principal ID | Shared auth `sub`/user ID | 0, 3 | Claim-to-users mapping is runtime convention; live identity not checked |
| 4 | `title` | Notification title | VARCHAR | 200 | N/A | Y |  | Preserve request value | `title` | 1, 3 | Runtime rejects blank and length > 200; limit is candidate-derived |
| 5 | `content` | Notification content | TEXT | Unspecified | N/A | Y |  | Preserve request value | `content` | 1, 3 | Runtime rejects blank; no max added |
| 6 | `type` | Legacy type | VARCHAR | 30 | N/A | N |  | `NULL` | No direct channel mapping | 3 | `NotificationChannel` is stored in delivery table |
| 7 | `is_read` | Read flag | BOOLEAN | N/A | N/A | N |  | `FALSE` | Fixed | 3 | Does not represent delivery status |
| 8 | `created_at` | Creation time | TIMESTAMP | N/A | N/A | Y |  | `CURRENT_TIMESTAMP` | Database clock | 3 | Returned for the first response item |
| 9 | `operation_id` | Batch grouping ID | UUID | N/A | N/A | N |  | One app-generated UUID shared by all recipient rows | App UUID | 3 | Added by migration 009 candidate; not an Operation-store record |

## Update mapping

N/A — API #93 does not declare UPDATE.

## Delete mapping

N/A — API #93 does not declare DELETE.

## Physical mapping boundary

- This is the implementation's local fallback against a checked-in legacy schema candidate, not an approved Admin campaign model or verified live database schema.
- The model creates one Notification row per recipient; it has no separate campaign-to-recipient association table.
- V1-PILOT UUID learner notification schema remains a separate model.
- The app commits all candidate Notification and delivery rows in one transaction before returning 202.
---
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
