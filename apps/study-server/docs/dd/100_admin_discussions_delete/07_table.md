---
title: "Định nghĩa table"
order: 7
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `discussions` — candidate từ legacy DDL |
| Logical table | Discussion / thread / reply |
| Operation | `UPDATE` candidate cho soft-delete; không physical `DELETE` |
| Data Mapping step | 2–4 |
| Schema status | Legacy checked-in DDL; không chứng minh live schema |

## Candidate schema fields used/reviewed

| Column | Type | Constraint/default in legacy DDL | Use/status |
|---|---|---|---|
| `id` | `BIGSERIAL` | Primary key | Candidate target key for `discussion_id`; live mapping unverified |
| `status` | `VARCHAR(20)` | Default `ACTIVE`; nullable because no `NOT NULL` | Candidate soft-delete marker; stored token `DELETED` is DERIVED, approval required |
| `updated_at` | `TIMESTAMP` | `NOT NULL` | Candidate operation time only; not a dedicated delete timestamp |

Legacy DDL also has `course_id`, `user_id`, `parent_id`, `content`, and `created_at`; API #100 does not need to update these fields on direct evidence.

## Update mapping

**Áp dụng khi** Admin xóa mềm một target hợp lệ. Physical mapping vẫn là proposal, chưa được duyệt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `status` | Soft-delete state | `VARCHAR` | 20 | N/A | No in legacy DDL | No | Candidate value `DELETED` | Approved state decision | 3 | DERIVED only; enum/state transition SOURCE_REQUIRED |
| 2 | `updated_at` | Operation timestamp | `TIMESTAMP` | N/A | N/A | Yes in legacy DDL | No | Candidate server time | Operation clock | 3 | Mapping to `DeleteResult.deleted_at` is DERIVED only |

## Delete mapping

**Áp dụng khi** Không physical DELETE vì AC-37 yêu cầu soft delete.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | Không hard-delete row theo diagram |

## Audit mapping

- Logical requirement: preserve audit trail (`DIRECT`, AC-37).
- Legacy physical audit relation for this Discussion is not found in `DB.sql`.
- Pilot `admin_adjustments.target_id` and `audit_events.resource_id` use UUID; no approved BIGINT mapping exists.
- Append event, actor/resource identifiers, retention and atomicity remain `SOURCE_REQUIRED`; no physical table/column is invented here.

## Response field gap

`DeleteResult.deleted_at` is required by the catalog schema, but legacy `discussions` has no `deleted_at` column. Reusing `updated_at` for the response is a `DERIVED` proposal, not an approved persistence mapping.
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
