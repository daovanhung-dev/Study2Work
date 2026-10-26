---
title: "Định nghĩa table"
order: 7
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `notifications` + `notification_deliveries` — legacy BIGINT candidate |
| Logical table | Notification + per-channel delivery aggregate |
| Operation | SELECT only |
| Data Mapping step | Q1/Q2 tại `05_Data_Mapping.md#step-2-đọc-notification-và-delivery-aggregate` |

## Read mapping — candidate only

| No | Table | Column | Type in checked-in DDL | Use | Status/remarks |
|---:|---|---|---|---|---|
| 1 | `notifications` | `id` | BIGSERIAL | Notification ID and stable sort tie-breaker | Candidate; not live evidence |
| 2 | `notifications` | `title` | VARCHAR(200) | Response `title` | Candidate |
| 3 | `notifications` | `content` | TEXT | Response `content` | Candidate |
| 4 | `notifications` | `created_at` | TIMESTAMP | Response timestamp and page order | Candidate; timezone behavior unverified |
| 5 | `notification_deliveries` | `notification_id` | BIGINT | Join and group key | Migration 009/API #63 candidate |
| 6 | `notification_deliveries` | `channel` | VARCHAR(16) | Aggregate response/filter channels | DDL check `PUSH`/`EMAIL`; DERIVED Notification mapping |
| 7 | `notification_deliveries` | `status` | VARCHAR(16) | Count queued/sent/failed states | DDL check; aggregate precedence from API #64 |
| 8 | `notification_deliveries` | `updated_at` | TIMESTAMPTZ | Not projected | Migration field; not selected by #92 |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có mutation. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có mutation. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | Không có mutation. |

## Query-only note

- Runtime chỉ query notification có tối thiểu một outbox delivery để dựng required channels/status.
- Một item tương ứng một `notifications.id`; không gom theo `operation_id` hoặc campaign.
- Không query/map `user_id`, `sender_id`, `type`, `is_read`, `operation_id`, pilot UUID fields hoặc provider data.
- DDL/migration chỉ là checked-in candidate; không thêm schema, migration hoặc ERD relation trong task #92.

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
