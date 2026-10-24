---
title: "Định nghĩa table — quiz_choices INSERT"
order: 9
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_choices INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quiz_choices |
| Logical table | QuizChoice chưa được định nghĩa đầy đủ |
| Operation | INSERT |
| Data Mapping step | [M3 — Step 4](./05_Data_Mapping.md#step-4-insert-question-and-choice-children) |
| Source | Legacy infra/postgres/study-server/DB.sql candidate |
| Live schema status | Chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — API #88 tạo choices; update thuộc API #89.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #88 không UPDATE bảng. |

## Insert mapping

**Áp dụng khi**

- Một row cho mỗi choices[] trong mỗi question.
- question_id lấy từ question row trong cùng transaction.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Choice ID | BIGSERIAL / int64 | N/A | N/A | Y | PK | Database generated | Legacy DB.sql | 4 | Output property chưa được QuizChoice định nghĩa. |
| 2 | question_id | Parent question ID | BIGINT | 8 bytes | N/A | Y by API | FK | Generated quiz_questions.id | Legacy relation + M2 | 4 | DDL nullable; write supplies parent ID. |
| 3 | choice_text | Choice text | TEXT | N/A | N/A | Y |  | choices[j].text | Derived QuizChoice input + legacy DDL | 4 | Logical input property is proposal. |
| 4 | is_correct | Correct answer flag | BOOLEAN | 1 | N/A | Y by proposal |  | choices[j].is_correct | Legacy DB.sql answer-key column | 4 | Not in reusable QuizChoice output schema. |

## Delete mapping

**Áp dụng khi**

- N/A — API #88 không xóa choices hiện có.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Existing-choice update/removal thuộc API #89. |

## Ordering gap

Legacy quiz_choices không có position/sort_order. Array order có thể dùng khi dựng create response; thứ tự truy vấn bền vững cho API #28/#87/#89 chưa được định nghĩa.
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
