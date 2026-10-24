---
title: "Table — quiz_questions delete"
order: 9
dd_id: "90"
api_name: "Xóa quiz"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `quiz_questions` DELETE

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | Legacy candidate `quiz_questions` |
| Logical table | QuizQuestion |
| Operation | DELETE |
| Data Mapping step | [Step 4B.3 — xóa questions](./05_Data_Mapping.md#step-4b-khong-co-attempts-candidate-hard-delete) |
| Basis | No-attempt hard-delete branch là DERIVED; relation lấy từ legacy DDL/ERD. |

## Delete mapping

**Áp dụng khi**

- Q2 không tìm thấy attempt nào cho quiz.
- M2 đã xóa choices thuộc question set.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | `quiz_id` | `=` | `:quiz_id` từ path | Step 4B.3 | BIGINT FK candidate; legacy DDL cho phép NULL dù DB guide ghi required. |

## Relation/condition

- Không xóa câu hỏi khi có attempt; giữ IDs để API #30–#32 tham chiếu lịch sử.
- Xóa sau choices và trước quiz parent.
- Không dùng pilot UUID `quiz_questions.assessment_id` cho API int64.

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
