---
title: "Định nghĩa table"
order: 7
dd_id: "31"
api_name: "Khóa attempt và bắt đầu chấm"
source_sheet: "table — quiz_attempts update"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_attempts |
| Logical table | Lần làm bài kiểm tra |
| Operation | UPDATE candidate |
| Data Mapping step | 3. Lock/submit the attempt |

## Update mapping

**Áp dụng khi**

- A candidate attempt is found and submission is accepted under the policy approved for API #31; exact owner/state predicate remains SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | id | Attempt ID | BIGSERIAL | N/A | N/A | Yes | ● | Candidate row identifier from path attempt_id. | API catalog / DB_UNICA_TABLES.md / DB.sql | 3 | Used to select target row; no update to primary key. |
| 2 | status | Attempt status | VARCHAR | 20 | N/A | DDL permits null |  | SUBMITTED per AC-16. | AC-16 / DB_UNICA_TABLES.md / DB.sql | 3 | Other accepted/terminal states and conditional update predicate are unresolved. |
| 3 | submitted_at | Submission time | TIMESTAMP | N/A | N/A | No; nullable in DDL |  | Candidate timestamp set at submit. | AC-16 / DB_UNICA_TABLES.md / DB.sql | 3 | Clock, timezone, precision and repeat-submit behavior SOURCE_REQUIRED. |
| 4 | score | Aggregate score | NUMERIC | 6 | 2 | No; nullable in DDL |  | Candidate aggregate after automatic grading. | DB_UNICA_TABLES.md / DB.sql | 4 | Formula, scale, rounding and PENDING_GRADE behavior SOURCE_REQUIRED. |

**Candidate WHERE**

- quiz_attempts.id = path attempt_id.
- Owner and current-state predicates are SOURCE_REQUIRED.
- Lock/conditional update strategy is SOURCE_REQUIRED.

## Insert mapping

N/A — API #31 does not create a new attempt.

## Delete mapping

N/A — API #31 does not delete an attempt.

> Candidate mapping only. DB artifacts are design evidence; live schema and runtime persistence are not verified.
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
