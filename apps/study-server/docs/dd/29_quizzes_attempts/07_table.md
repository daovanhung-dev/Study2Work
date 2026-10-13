---
title: "Định nghĩa table"
order: 7
dd_id: "29"
api_name: "Tạo attempt"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_attempts |
| Logical table | Lần làm bài kiểm tra |
| Operation | INSERT |
| Data Mapping step | 3. Insert attempt |

## Update mapping

N/A — API #29 creates an attempt; no UPDATE is defined.

## Insert mapping

**Áp dụng khi**

- Eligibility succeeds under the policy approved for API #29.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | id | Attempt ID | BIGSERIAL | N/A | N/A | Yes | ● | Generated key candidate. | DB_UNICA_TABLES.md / DB.sql | 3 | Runtime key generation is not verified. |
| 2 | quiz_id | Quiz ID | BIGINT | N/A | N/A | TBD |  | Path quiz_id. | API catalog / AC-16 / DB design | 3 | DB table design says required; checked-in DDL permits NULL. |
| 3 | user_id | Student ID | BIGINT | N/A | N/A | TBD |  | Authenticated Student principal; exact claim mapping SOURCE_REQUIRED. | Student Bearer contract / DB design | 3 | DB table design says required; checked-in DDL permits NULL. |
| 4 | started_at | Start time | TIMESTAMP | N/A | N/A | Yes |  | Candidate start timestamp; clock source/timezone SOURCE_REQUIRED. | DB.sql | 3 | DDL declares NOT NULL; generation policy is not specified. |
| 5 | submitted_at | Submission time | TIMESTAMP | N/A | N/A | No |  | Candidate NULL before submission. | DB_UNICA_TABLES.md / DB.sql | 3 | Nullable in checked-in DDL; exact insert omission/null policy not confirmed. |
| 6 | score | Score | NUMERIC | 6 | 2 | No |  | Candidate NULL before grading. | DB_UNICA_TABLES.md / DB.sql | 3 | Nullable in checked-in DDL; logical response serializes score as decimal-string. |
| 7 | status | Attempt status | VARCHAR | 20 | N/A | TBD |  | IN_PROGRESS per AC-16; explicit insert versus DB default is unresolved. | AC-16 / DB_UNICA_TABLES.md / DB.sql | 3 | DDL default is IN_PROGRESS but does not declare NOT NULL. |

## Delete mapping

N/A — API #29 does not define deletion.

> Physical mappings are candidate design evidence only. No live schema or API #29 persistence method has been verified.

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
