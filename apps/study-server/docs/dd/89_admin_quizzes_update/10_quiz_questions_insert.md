---
title: "Table Insert — quiz_questions"
order: 10
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_questions INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical table | QuizQuestion |
| Physical table | legacy quiz_questions |
| Operation | INSERT |
| Data Mapping step | [M4 — Step 7](./05_Data_Mapping.md#step-7-insert-replacement-question-set) |
| Basis | Candidate mapping từ legacy DDL; live schema chưa xác minh. |

## Insert mapping

| No | Physical column | Logical name | Type | Length | Scale | Required | PK | FK | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | id | Question ID | BIGSERIAL | N/A | N/A | Yes | Yes | No | Database-generated | Database | Step 7 | Candidate generated ID gắn choices. |
| 2 | quiz_id | Quiz ID | BIGINT | N/A | N/A | Nullable in DDL | No | quizzes.id | quiz_id | Path parameter | Step 7 | DDL nullable; ERD required. |
| 3 | question_text | Question text | TEXT | N/A | N/A | Yes | No | No | questions[i].text | Proposed request body | Step 7 | Alias text → question_text. |
| 4 | sort_order | Question order | INT | N/A | N/A | DDL default 0 | No | No | i, zero-based | Request array index | Step 7 | DERIVED theo #88; tie policy open. |
| 5 | score | Question score | NUMERIC | 5 | 2 | DDL default 1 | No | No | Omit; default candidate | Legacy DDL | Step 7 | Không thêm score vào contract. |
| 6 | question_type | Question type | VARCHAR(24) | 24 | N/A | API requires value | No | No | questions[i].type | Migration 013 / #88 validator | Step 7 | Three-value DERIVED vocabulary; nullable for old rows. |

## Question type mapping

- Migration 013 adds nullable legacy `question_type`; API #88 writes the local DERIVED vocabulary.
- API #89 must not map question rows or IDs from V1-PILOT UUID tables.
- Old rows with NULL type are deleted only after the history guard passes; replacement rows always receive the validated local type.
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
