---
title: "Table Delete — quiz_choices"
order: 8
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_choices DELETE

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical table | QuizChoice |
| Physical table | legacy quiz_choices |
| Operation | DELETE |
| Data Mapping step | [M2 — Step 5](./05_Data_Mapping.md#step-5-delete-old-choices) |
| Basis | Candidate relation từ legacy DDL/ERD; live schema/FK behavior chưa xác minh. |

## Điều kiện xóa

- Xóa choices thuộc quiz_questions có quiz_id = quiz_id.
- Thực hiện trước khi xóa question rows.
- Chỉ chạy sau khi candidate Q2/Q3 không thấy attempt/answer history và policy được duyệt.
- Không mặc định dùng CASCADE hoặc giả định DB cascade behavior.

## Relation/condition mapping

| No | Physical column | Logical name | Type | Length | Scale | Required | PK | FK | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | id | Choice ID | BIGSERIAL | N/A | N/A | Yes | Yes | No | Delete matching rows | Existing quiz_choices | Step 5 | Không thay ID. |
| 2 | question_id | Question ID | BIGINT | N/A | N/A | Nullable in DDL | No | quiz_questions.id | Question rows where quiz_id matches | Existing relation | Step 5 | Candidate 1:N; live FK chưa xác minh. |
| 3 | choice_text | Choice text | TEXT | N/A | N/A | Yes | No | No | Delete matching rows | Existing quiz_choices | Step 5 | Không đọc/ghi lại row cũ. |
| 4 | is_correct | Answer key | BOOLEAN | N/A | N/A | DDL default FALSE | No | No | Delete matching rows | Existing quiz_choices | Step 5 | Không expose trong response. |

## Safety conditions

- Candidate Q3 phải xác nhận không có quiz_answers.choice_id tham chiếu choice cũ.
- Nếu có row tham chiếu thì dừng trước DELETE và candidate trả 422; policy cần owner xác nhận.
- FK/DB failure trong transaction → rollback và HTTP 500 DESIGN_INTERNAL_ERROR.
- Không khẳng định physical DELETE/soft-delete là runtime behavior.
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
