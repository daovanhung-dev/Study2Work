---
title: "Table Delete — quiz_questions"
order: 9
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quiz_questions DELETE

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical table | QuizQuestion |
| Physical table | legacy quiz_questions |
| Operation | DELETE |
| Data Mapping step | [M3 — Step 6](./05_Data_Mapping.md#step-6-delete-old-questions) |
| Basis | Candidate relation từ legacy DDL/ERD; live schema/FK behavior chưa xác minh. |

## Điều kiện xóa

- Xóa question rows có quiz_id = quiz_id.
- Xóa sau khi choice rows cũ được xử lý.
- Chỉ chạy khi Q2/Q3 không phát hiện attempt/answer history theo policy proposal.

## Column mapping

| No | Physical column | Logical name | Type | Length | Scale | Required | PK | FK | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | id | Question ID | BIGSERIAL | N/A | N/A | Yes | Yes | No | Delete matching rows | Existing quiz_questions | Step 6 | ID cũ không dùng lại. |
| 2 | quiz_id | Quiz ID | BIGINT | N/A | N/A | Nullable in DDL | No | quizzes.id | quiz_id | Path parameter | Step 6 | DDL nullable; ERD nói required. |
| 3 | question_text | Question text | TEXT | N/A | N/A | Yes | No | No | Delete matching rows | Existing quiz_questions | Step 6 | Candidate full replacement. |
| 4 | sort_order | Question order | INT | N/A | N/A | DDL default 0 | No | No | Delete matching rows | Existing quiz_questions | Step 6 | New order from array index proposal. |
| 5 | score | Question score | NUMERIC | 5 | 2 | DDL default 1 | No | No | Delete matching rows | Existing quiz_questions | Step 6 | Không có field request tương ứng. |

## Safety conditions

- Candidate Q3 kiểm tra quiz_answers.question_id trỏ tới câu hỏi của Quiz.
- Nếu có answer/attempt history, dừng trước delete; không làm mất historical results.
- Legacy model không có version/audit field để lưu question set cũ.
- FK/DB failure → rollback toàn transaction; không mặc định cascade.
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
