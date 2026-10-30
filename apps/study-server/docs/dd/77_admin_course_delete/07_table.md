---
title: "Định nghĩa table"
order: 7
dd_id: "77"
api_name: "Xóa khóa học Admin theo policy AC-32"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | Legacy candidate `courses`; live schema chưa xác nhận. |
| Logical table | Course |
| Operation | `UPDATE` status marker and timestamp (`DERIVED`). |
| Data Mapping step | `3.3` |

## Update mapping

**Áp dụng khi**

- Q1 finds a course not already `DELETED` and Q2 finds no blocking dependency.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `status` | Course lifecycle status | `VARCHAR` | 20 | N/A | Yes in candidate flow | No | Set to `DELETED` | `DERIVED` API #72 precedent; legacy DDL | 3.3 | No dedicated delete marker; live schema unknown. |
| 2 | `updated_at` | Last update/deletion time | `TIMESTAMP` | N/A | N/A | Yes | No | Set by `CURRENT_TIMESTAMP`; return as `deleted_at` | Legacy DDL + API #72 precedent | 3.3/5.1 | DB timestamp returned by UPDATE; no dedicated deleted_at column. |

No `deleted_at` column or migration is added. V1-PILOT `archived_at` is not mapped to this legacy DELETE.

## Insert mapping

**Áp dụng khi**

- N/A — API #77 creates no relation; AC-32 does not specify an audit event for this DELETE branch.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|

## Delete mapping

**Áp dụng khi**

- N/A — HTTP method is DELETE but runtime mutation is an UPDATE marker; no physical `DELETE FROM` or cascade.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|

The view owns the transaction. It locks the course, checks dependencies, performs the UPDATE, validates RETURNING, then commits. Any failure rolls back.

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
