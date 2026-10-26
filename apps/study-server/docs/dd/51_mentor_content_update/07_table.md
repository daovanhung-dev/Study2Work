---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `contents` update

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `contents` |
| Logical table | Current Content projection |
| Operation | UPDATE |
| Data Mapping step | 5 |
| Evidence | Legacy migration 006; API #51 DML is implemented locally. |
| Status | DDL is checked in only; live schema/migration not verified. |

## Update mapping

**Áp dụng khi**

- API #51 has locked an active `contents` row and direct owner authorization passed.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `content_type` | Content type | TEXT | N/A | N/A | Y |  | Body `content_type` | Request | 5 | Full replacement; open string; DERIVED body field. |
| 2 | `title` | Title | TEXT | N/A | N/A | Y |  | Body `title` | Request | 5 | Full replacement; no normalization/length rule added. |
| 3 | `payload` | Content payload | JSONB object | N/A | N/A | Y |  | JSON serialization then `CAST(:payload AS JSONB)` | Request | 5 | Object check from migration 006. |
| 4 | `status` | Review status | TEXT | N/A | N/A | Y |  | Fixed `PENDING_REVIEW` | Derived AC-33/#50 | 5 | Lifecycle remains unapproved. |
| 5 | `id` | Content ID | BIGINT | N/A | N/A | Y | ● | `WHERE id = :content_id AND deleted_at IS NULL` | Path | 5 | No identity change. |
| 6 | `course_id` | Course ID | BIGINT | N/A | N/A | Y |  | Preserve locked value | Locked Content | 5 | Used for owner scope. |
| 7 | `parent_id` | Parent ID | BIGINT | N/A | N/A | N |  | Preserve locked value | Locked Content | 5 | Tree position unchanged. |
| 8 | `content_order` | Content order | INTEGER | N/A | N/A | Y |  | Preserve locked value | Locked Content | 5 | Response alias `order`. |

## Insert mapping

- N/A — API #51 does not insert into `contents`; it updates the existing row.

## Delete mapping

- N/A — API #51 does not delete Content.

## SQL mapping

`UPDATE contents SET content_type=:content_type, title=:title, payload=CAST(:payload AS JSONB), status='PENDING_REVIEW' WHERE id=:content_id AND deleted_at IS NULL RETURNING ...`. Course and tree fields are not updated.

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
