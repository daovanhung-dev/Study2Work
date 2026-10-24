---
title: "Table Insert — quiz_choices"
order: 11
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_choices INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical table | QuizChoice |
| Physical table | legacy quiz_choices |
| Operation | INSERT |
| Data Mapping step | [M5 — Step 7](./05_Data_Mapping.md#step-7-insert-replacement-question-set) |
| Basis | Candidate mapping từ legacy DDL; QuizChoice output schema chưa định nghĩa. |

## Insert mapping

| No | Physical column | Logical name | Type | Length | Scale | Required | PK | FK | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | id | Choice ID | BIGSERIAL | N/A | N/A | Yes | Yes | No | Database-generated | Database | Step 7 | Output visibility chưa chốt. |
| 2 | question_id | Question ID | BIGINT | N/A | N/A | Nullable in DDL | No | quiz_questions.id | Generated question ID từ M4 | New question row | Step 7 | DDL nullable; ERD required. |
| 3 | choice_text | Choice text | TEXT | N/A | N/A | Yes | No | No | choices[j].text | Proposed request body | Step 7 | DERIVED input mapping. |
| 4 | is_correct | Answer key | BOOLEAN | N/A | N/A | DDL default FALSE | No | No | choices[j].is_correct | Proposed request body | Step 7 | DERIVED; không trả trong response mặc định. |

## Ordering and response gap

- Legacy quiz_choices không có order column; input order không được bảo đảm bền vững.
- QuizChoice fields, ID visibility và answer-key visibility chưa được logical contract định nghĩa.
- Không thêm order column hoặc đổi sang V1-PILOT quiz_options khi chưa có schema approval.
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
