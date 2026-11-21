---
title: "Định nghĩa table"
order: 7
dd_id: "33"
api_name: "Lấy đề bài/rule/deadline"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | assignments |
| Logical table | Assignment |
| Operation | SELECT only; no mutation mapping |
| Data Mapping step | 2 |

## Read mapping

| No | Physical column | Logical field | Type | Nullable in DDL | Key/constraint | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---:|---|
| 1 | id | id | BIGSERIAL / int64 | No | PK | 2 | Candidate lookup key; design-only. |
| 2 | course_id | course_id | BIGINT / int64 | Yes | FK to courses.id | 2 | Logical contract requires a value; ERD/table note versus DDL discrepancy. |
| 3 | name | title | VARCHAR(200) / string | No | — | 2 | Physical name maps to logical `Assignment.title`. |
| 4 | description | description | TEXT / string | Yes | — | 2 | Optional response field. |
| 5 | due_at | due_at | TIMESTAMP / date-time | Yes | — | 2 | No timezone/serialization rule specified. |
| 6 | max_score | max_score | NUMERIC(6,2) / decimal-string | Yes | DEFAULT 10 | 2 | Logical response requires value; DDL permits NULL. |

## Update mapping

**Áp dụng khi**

- N/A — API #33 không update dữ liệu.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Insert mapping

**Áp dụng khi**

- N/A — API #33 không insert dữ liệu.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Delete mapping

**Áp dụng khi**

- N/A — API #33 không delete dữ liệu.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | Read-only API. |

> Đây là candidate read mapping từ checked-in design DDL; không xác nhận schema live hoặc query runtime.
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

