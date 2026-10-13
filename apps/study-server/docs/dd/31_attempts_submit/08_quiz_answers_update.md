---
title: "Định nghĩa table"
order: 8
dd_id: "31"
api_name: "Khóa attempt và bắt đầu chấm"
source_sheet: "table — quiz_answers update"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_answers |
| Logical table | Câu trả lời trong lần làm bài |
| Operation | UPDATE candidate |
| Data Mapping step | 4. Grade submitted answers |

## Update mapping

**Áp dụng khi**

- An answer belongs to the accepted attempt and an approved automatic-grading rule defines its result; exact selection and grading predicates remain SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | id | Answer row ID | BIGSERIAL | N/A | N/A | Yes | ● | Candidate target row identity. | DB_UNICA_TABLES.md / DB.sql | 4 | API #31 does not define answer-row lookup key in the catalog. |
| 2 | attempt_id | Attempt ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Candidate association to submitted attempt. | DB_UNICA_TABLES.md / DB.sql | 4 | FK to quiz_attempts.id; live constraint not verified. |
| 3 | question_id | Question ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Candidate association to question being graded. | DB_UNICA_TABLES.md / DB.sql | 4 | FK to quiz_questions.id; answer completeness policy unresolved. |
| 4 | is_correct | Correctness | BOOLEAN | N/A | N/A | DDL: Yes, NOT NULL |  | Candidate automatic-grading result. | AC-16 / DB_UNICA_TABLES.md / DB.sql | 4 | API #30 does not define its pre-submit value; manual-grade questions have no approved value. |
| 5 | score_received | Per-answer score | NUMERIC | 5 | 2 | No; DDL default 0 |  | Candidate score derived from question/answer grading. | DB_UNICA_TABLES.md / DB.sql | 4 | Formula, partial credit, scale and rounding SOURCE_REQUIRED. |

**Candidate WHERE**

- quiz_answers.attempt_id = selected quiz_attempts.id.
- Additional answer/question/choice selection predicates are SOURCE_REQUIRED.
- No unique key for attempt_id plus question_id is declared by the checked-in DDL.

## Insert mapping

N/A — AC-16 describes submitting and grading answers already saved by API #30; it does not describe inserting answer rows in API #31.

## Delete mapping

N/A — API #31 does not define answer deletion.

> Candidate mapping only. API #30 answer representation and checked-in storage do not align fully; see OPEN_QUESTIONS.md. Live schema is not verified.
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
