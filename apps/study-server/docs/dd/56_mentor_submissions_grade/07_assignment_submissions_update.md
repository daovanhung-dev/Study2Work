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
| Operation | UPDATE |
| Data Mapping step | 3 |
| Evidence | Checked-in legacy DDL candidate; live schema unverified |

## Update mapping

Applied after the submission row is locked, direct-owner check succeeds, and the DERIVED score range passes. The row can be graded again under the current fallback; no prior-status condition is enforced.

| No | Column | Item name | Type | Length | Scale | Setting content | Source | Remarks |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | id | Submission ID | BIGSERIAL candidate | N/A | N/A | Predicate only | Path submission_id | Not updated |
| 2 | score | Graded score | NUMERIC | 6 | 2 | :score cast to NUMERIC(6,2) | Body score:int32 | Strict integer; DERIVED 0 <= score <= assignments.max_score |
| 3 | status | Submission status | VARCHAR | 20 | N/A | GRADED | AC-23 grade/status node | Only score and status are written |
| 4 | feedback | Existing feedback | TEXT | N/A | N/A | Preserved | Locked current row | Not changed; API #57 owns feedback mutation |

### Implemented SQL shape

~~~sql
UPDATE assignment_submissions AS s
SET
    score = CAST(:score AS NUMERIC(6,2)),
    status = 'GRADED'
WHERE s.id = :submission_id
  AND s.assignment_id = :assignment_id
  AND EXISTS (
      SELECT 1
      FROM assignments AS a
      JOIN courses AS c ON c.id = a.course_id
      WHERE a.id = s.assignment_id
        AND c.mentor_id = :mentor_id
  )
RETURNING
    s.id, s.assignment_id, s.user_id, s.content, s.file_url,
    s.submitted_at, s.score, s.feedback, s.status;
~~~

The application holds the submission row lock through authorization, score validation, UPDATE and response projection. It commits after projection validation and rolls back failures. SQL is source-verified but has not been run against a live database.

## Rubric scope

The request requires rubric_items as a string under a DERIVED wire key, but there is no approved persistence table, column or relation. It is currently accepted and discarded. No rubric mutation is claimed.

## Insert mapping

N/A — API #56 updates an existing submission.

## Delete mapping

N/A — API #56 does not delete a submission.

## Scope exclusions

- No rubric table or UUID assessment join.
- No feedback write; API #57 remains separate.
- No updated_at or audit/history column is inferred.
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
