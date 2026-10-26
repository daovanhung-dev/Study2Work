---
title: "Định nghĩa table"
order: 7
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `courses`, `enrollments`, `users` — read only |
| Logical table | Course ownership, active enrollment and Student summary |
| Operation | `SELECT` only |
| Data Mapping step | Q1 at [step 2](./05_Data_Mapping.md#step-2-check-course-scope); Q2 at [step 3](./05_Data_Mapping.md#step-3-doc-active-student-roster) |

## Mapping

N/A — READ-ONLY API. No `INSERT`, `UPDATE`, `DELETE`, schema change or commit is performed. Selected read columns, joins and predicates are listed in [05_Data_Mapping.md](./05_Data_Mapping.md).

| Table | Read columns | Purpose |
|---|---|---|
| `courses` | `id` | Find the requested course. |
| `courses` | `mentor_id` | Check direct owner against the authenticated Mentor. |
| `enrollments` | `course_id` | Match the path course. |
| `enrollments` | `user_id` | Join to Student identity. |
| `enrollments` | `status` | Require `ACTIVE`. |
| `users` | `id` | Recipient ID. |
| `users` | `full_name` | Display name. |
| `users` | `avatar_url` | Optional avatar URI. |
| `users` | `role` | Require `STUDENT`. |

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
