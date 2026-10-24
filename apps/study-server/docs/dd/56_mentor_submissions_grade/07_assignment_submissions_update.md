---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | assignment_submissions |
| Logical table | Submission |
| Operation | UPDATE candidate |
| Data Mapping step | 3.3 |
| Evidence | Legacy DDL and table guide are design artifacts; live schema unverified |

## Update mapping

**Áp dụng khi**

- Candidate submission is located and Mentor access check has passed.
- Repeated-grading/status eligibility is still SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | id | Submission ID | BIGSERIAL candidate | N/A | N/A | Yes in logical contract | Yes, predicate only | N/A; WHERE id = :submission_id | Path submission_id | 3.2 | Not updated; DDL primary key |
| 2 | score | Graded score | NUMERIC | 6 | 2 | Request required; DB column nullable | No | :score | Body score:int32 | 3.3 | Input-to-decimal conversion, fit, range and scale are SOURCE_REQUIRED |
| 3 | status | Submission status | VARCHAR | 20 | N/A | Contract response required; DDL does not declare NOT NULL | No | GRADED | AC-23 node “UPDATE grade + status = GRADED” | 3.3 | Target value DIRECT; full enum/constraint and allowed prior states unresolved |

### Candidate SQL shape

~~~sql
UPDATE assignment_submissions
SET score = :score,
    status = 'GRADED'
WHERE id = :submission_id
RETURNING id, assignment_id, user_id, content, file_url, submitted_at, score, feedback, status;
~~~

This is a design candidate only. It does not persist rubric items and has not been run against a database. Authorization, transaction boundary, score conversion, concurrent deletion and returned files mapping still need approved behavior.

## Insert mapping

**Áp dụng khi**

- N/A — API #56 is an update flow; no insert branch is defined.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT is specified |

## Delete mapping

**Áp dụng khi**

- N/A — API #56 does not delete a submission.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE is specified |

## Scope exclusions

- Rubric items: no approved assignment rubric table or submission rubric detail relation; V1-PILOT assessment rubric tables are a different UUID model.
- Feedback: not updated by this API; API #57 owns the later feedback mutation.
- updated_at: no such column is present in this legacy candidate table.
- Audit/history/version columns: no approved source.
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
