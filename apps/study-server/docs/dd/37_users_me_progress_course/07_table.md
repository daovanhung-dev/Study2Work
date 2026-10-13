---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "37"
api_name: "Lấy tiến độ chi tiết course"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — nhiều candidate read tables |
| Logical table | Course progress source candidates |
| Operation | SELECT candidates only; design-only |
| Data Mapping step | 2.1–2.5 |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | No mutation. |

## Candidate read projection

> Bảng và cột dưới đây chỉ ghi nhận schema design/checked-in DDL làm nguồn đọc có thể xem xét. Đây không phải SQL, không chốt predicate, aggregate, join type hoặc response mapping. Live schema chưa được kiểm chứng.

| No | Table | Candidate column | Type theo checked-in DDL | Candidate use | Source / status |
|---:|---|---|---|---|---|
| 1 | lesson_progress | user_id | BIGINT | Candidate principal scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 2 | lesson_progress | lesson_id | BIGINT | Relation candidate tới lesson. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 3 | lesson_progress | status | VARCHAR(20) | Candidate lesson state. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 4 | lesson_progress | progress_percent | SMALLINT | Candidate lesson progress value. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 5 | lesson_progress | last_accessed_at | TIMESTAMP NULL | Candidate activity time. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 6 | lesson_progress | completed_at | TIMESTAMP NULL | Candidate completion time. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 7 | lessons | id | BIGSERIAL | Candidate lesson join key. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 8 | lessons | course_id | BIGINT | Candidate course scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 9 | courses | id | BIGSERIAL | Candidate course identity. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 10 | quizzes | id | BIGSERIAL | Candidate quiz join key. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 11 | quizzes | course_id | BIGINT | Candidate quiz scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 12 | quiz_attempts | user_id | BIGINT | Candidate principal scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 13 | quiz_attempts | quiz_id | BIGINT | Candidate relation to quiz. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 14 | quiz_attempts | submitted_at | TIMESTAMP NULL | Candidate submission/completion marker. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 15 | quiz_attempts | score | NUMERIC(6,2) NULL | Candidate score. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 16 | quiz_attempts | status | VARCHAR(20) | Candidate attempt state. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 17 | assignments | id | BIGSERIAL | Candidate assignment join key. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 18 | assignments | course_id | BIGINT | Candidate assignment scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 19 | assignment_submissions | user_id | BIGINT | Candidate principal scope. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 20 | assignment_submissions | assignment_id | BIGINT | Candidate relation to assignment. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 21 | assignment_submissions | submitted_at | TIMESTAMP | Candidate submission time. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 22 | assignment_submissions | score | NUMERIC(6,2) NULL | Candidate grade. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |
| 23 | assignment_submissions | status | VARCHAR(20) | Candidate submission state. | DB_UNICA_TABLES.md; DB.sql — DESIGN_ONLY |

## Query and mutation boundary

- No executable SQL statement is defined in this file.
- SELECT sources remain candidate until query predicates and aggregate rules are approved.
- INSERT mapping: N/A.
- UPDATE mapping: N/A.
- DELETE mapping: N/A.
- No table, column, migration or persistent aggregate is added by this DD.

---
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
