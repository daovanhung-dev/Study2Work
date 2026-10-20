---
title: "Định nghĩa table"
order: 7
dd_id: "30"
api_name: "Autosave/lưu câu trả lời"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_answers |
| Logical table | Câu trả lời trong lần làm bài |
| Operation | UPSERT candidate per AC-16; physical INSERT/UPDATE branch unresolved. |
| Data Mapping step | 3. Upsert candidate answer |

## Update mapping

AC-16 labels the action as UPSERT AttemptAnswer, but neither ERD nor checked-in DDL defines a unique key for one answer per attempt/question. The lookup key and update fields remain SOURCE_REQUIRED; no concrete UPDATE predicate is asserted.

## Insert mapping

**Áp dụng khi**

- An insert branch is required by the approved upsert policy; exact branch condition is not defined.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | id | Answer row ID | BIGSERIAL | N/A | N/A | Yes | ● | Generated key candidate. | DB_UNICA_TABLES.md / DB.sql | 3 | Physical primary key; generated value strategy not verified at runtime. |
| 2 | attempt_id | Attempt ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Path attempt_id. | API catalog / DB design / DB.sql | 3 | FK to quiz_attempts.id; table design and DDL differ on nullability. |
| 3 | question_id | Question ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Body question_id. | API catalog / DB design / DB.sql | 3 | FK to quiz_questions.id; membership in attempt quiz is SOURCE_REQUIRED. |
| 4 | choice_id | Selected choice ID | BIGINT | N/A | N/A | Design: Yes; DDL: nullable |  | Candidate source from answer only if choice mapping is approved. | DB_UNICA_TABLES.md / DB.sql | 3 | Physical model stores one choice ID; body/logical schema may express string, array or text answer. |
| 5 | is_correct | Correctness | BOOLEAN | N/A | N/A | Yes in DDL |  | No value source defined for API #30. | DB.sql / AC-16 | 3 | DDL requires NOT NULL; AC-16 places submission/grading after autosave at API #31. Blocking schema/flow discrepancy. |
| 6 | score_received | Answer score | NUMERIC | 5 | 2 | No; DDL default 0 |  | DDL default candidate only; autosave assignment is not specified. | DB_UNICA_TABLES.md / DB.sql | 3 | Grading and score semantics are not assigned to API #30. |

## Delete mapping

N/A — API #30 does not define answer deletion.

> This is a candidate physical mapping only. ERD/DDL are design evidence; live schema is not verified. The contract-to-storage conversion and upsert key require owner confirmation.
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

