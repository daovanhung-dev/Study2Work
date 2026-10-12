---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "38"
api_name: "Lấy achievement/badge nếu có"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — không có bảng achievements trong ERD V1/checked-in DDL. |
| Logical table | Achievement response projection |
| Operation | SELECT từ dữ liệu hiện có — source/rule chưa xác định |
| Data Mapping step | 2–4 |

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

> Các bảng/cột chỉ là candidate inputs được nhìn thấy trong DB design và AC-18; không xác nhận chúng là nguồn award. Đây không phải SQL hoặc persisted Achievement mapping. Checked-in DDL không xác nhận live schema.

| No | Table | Candidate column | Type theo checked-in DDL | Candidate use | Source / status |
|---:|---|---|---|---|---|
| 1 | lesson_progress | user_id | BIGINT NULL | Candidate principal scope. | DB guide/DB.sql — DESIGN_ONLY |
| 2 | lesson_progress | lesson_id | BIGINT NULL | Candidate relation tới lesson. | DB guide/DB.sql — DESIGN_ONLY |
| 3 | lesson_progress | status | VARCHAR(20) NULL | Candidate learning rule input. | Award rule chưa xác nhận |
| 4 | lesson_progress | progress_percent | SMALLINT NULL | Candidate learning rule input. | Award threshold chưa xác nhận |
| 5 | lesson_progress | completed_at | TIMESTAMP NULL | Candidate event time. | Không xác nhận awarded_at source |
| 6 | lessons | id | BIGSERIAL | Candidate join key. | DB guide/DB.sql — DESIGN_ONLY |
| 7 | lessons | course_id | BIGINT NULL | Candidate course relation. | Filter semantics chưa chốt |
| 8 | quiz_attempts | user_id | BIGINT NULL | Candidate principal scope. | DB guide/DB.sql — DESIGN_ONLY |
| 9 | quiz_attempts | quiz_id | BIGINT NULL | Candidate relation tới quiz. | DB guide/DB.sql — DESIGN_ONLY |
| 10 | quiz_attempts | status | VARCHAR(20) NULL | Candidate assessment rule input. | Award rule chưa xác nhận |
| 11 | quiz_attempts | submitted_at | TIMESTAMP NULL | Candidate event time. | Không xác nhận awarded_at source |
| 12 | quiz_attempts | score | NUMERIC(6,2) NULL | Candidate assessment rule input. | Threshold chưa xác nhận |
| 13 | quizzes | id | BIGSERIAL | Candidate join key. | DB guide/DB.sql — DESIGN_ONLY |
| 14 | quizzes | course_id | BIGINT NULL | Candidate course relation. | Filter semantics chưa chốt |
| 15 | assignment_submissions | user_id | BIGINT NULL | Candidate principal scope. | DB guide/DB.sql — DESIGN_ONLY |
| 16 | assignment_submissions | assignment_id | BIGINT NULL | Candidate relation tới assignment. | DB guide/DB.sql — DESIGN_ONLY |
| 17 | assignment_submissions | status | VARCHAR(20) NULL | Candidate submission rule input. | Award rule chưa xác nhận |
| 18 | assignment_submissions | submitted_at | TIMESTAMP NOT NULL | Candidate event time. | Không xác nhận awarded_at source |
| 19 | assignment_submissions | score | NUMERIC(6,2) NULL | Candidate grading rule input. | Threshold chưa xác nhận |
| 20 | assignments | id | BIGSERIAL | Candidate join key. | DB guide/DB.sql — DESIGN_ONLY |
| 21 | assignments | course_id | BIGINT NULL | Candidate course relation. | Filter semantics chưa chốt |

## Query and mutation boundary

- Không có achievement table, award registry hoặc query SQL được xác nhận trong nguồn đã đọc.
- DB guide ghi achievements được tính từ dữ liệu hiện có; không bổ sung bảng persistence bằng DD này.
- Candidate input tables chưa có predicates hoặc transformation rule được phê duyệt.
- INSERT mapping: N/A.
- UPDATE mapping: N/A.
- DELETE mapping: N/A.
- No table, column, migration or persistent aggregate is added by this DD.
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
