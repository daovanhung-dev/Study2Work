---
title: "Định nghĩa table"
order: 7
dd_id: "67"
api_name: "Lấy tiến độ Student"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

N/A — READ-ONLY API. API #67 không INSERT, UPDATE hoặc DELETE nên không có mutation mapping.

## Candidate read source boundary

| Logical role | Relation | Dữ liệu cần có | Trạng thái |
|---|---|---|---|
| Course scope | Legacy candidate `courses` | Course ID và Mentor owner | DESIGN_ONLY; Mentor identity/assignment chưa xác nhận. |
| Learner eligibility | Legacy candidate `enrollments`, `users` | Course/Student membership và learner role | DESIGN_ONLY; status/privacy policy chưa xác nhận. |
| Curriculum | Legacy candidate `lessons` | Lesson ID, course ID, title, order, status | Checked-in DDL candidate; API #9 current source filters PUBLISHED. |
| Per-lesson state | Legacy candidate `lesson_progress` | Student/lesson key, status, percent, accessed/completed timestamps | DESIGN_ONLY; không có unique `(user_id, lesson_id)` trong DDL. |
| Alternate progress source | V1-PILOT `lesson_progress_facts`, `progress_snapshots` | UUID enrollment facts and course-version aggregates | Khác ID model; lesson_progress_facts không có percent; live deployment chưa xác minh. |

Không tạo table, column, SQL hoặc index mới. Không coi progress snapshot/fact là learning-event log cho API #66.

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
