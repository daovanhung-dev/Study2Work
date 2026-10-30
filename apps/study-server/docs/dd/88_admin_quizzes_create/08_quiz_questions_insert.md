---
title: "Định nghĩa table — quiz_questions INSERT"
order: 8
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_questions INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_questions |
| Logical table | QuizQuestion |
| Operation | INSERT |
| Data Mapping step | [M2 — Step 4](./05_Data_Mapping.md#step-4-insert-question-and-choice-children) |
| Source | Legacy DB.sql plus migration 013 candidate |
| Live schema status | Chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — API #88 tạo câu hỏi; update thuộc API #89.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #88 không UPDATE bảng. |

## Insert mapping

**Áp dụng khi**

- Một row cho mỗi phần tử questions[] sau khi toàn bộ request đã validate.
- quiz_id lấy từ Quiz parent tạo trong cùng transaction.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Question ID | BIGSERIAL / int64 | N/A | N/A | Y | PK | Database generated | Legacy DB.sql | 4 | Live schema unverified. |
| 2 | quiz_id | Parent Quiz ID | BIGINT | 8 bytes | N/A | Y by API | FK | Generated quizzes.id | Legacy relation + M1 | 4 | DDL nullable; write supplies parent. |
| 3 | question_text | Question text | TEXT | N/A | N/A | Y |  | questions[i].text | QuizQuestion.text + legacy DDL | 4 | Direct logical text alias. |
| 4 | question_type | Question type | VARCHAR | 24 | N/A | Y for API #88 |  | questions[i].type | Migration 013; V1-PILOT vocabulary | 4 | Nullable for old rows; new API writes a checked non-null value. |
| 5 | sort_order | Question order | INT | 4 | N/A | Y by API |  | Zero-based array index | Legacy DDL default 0 | 4 | Preserve request order. |
| 6 | score | Question score | NUMERIC | 5 | 2 | N by API |  | Leave legacy default 1 | Legacy DB.sql | 4 | No score field in QuizQuestion/body. |

## Delete mapping

**Áp dụng khi**

- N/A — API #88 không xóa questions; replacement semantics thuộc API #89.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE in API #88. |
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
