---
title: "Định nghĩa table"
order: 7
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

N/A — READ-ONLY API. API #65 không tạo, sửa hoặc xóa dữ liệu. Không có mutation table/column mapping cần phê duyệt.

## Candidate read relations — chưa phải mapping đã duyệt

| Logical role | Legacy candidate | Dữ liệu cần đọc | Trạng thái |
|---|---|---|---|
| Course/access | courses | Course ID, owner Mentor ID | DESIGN_ONLY; owner predicate DERIVED. |
| Enrollment roster | enrollments | Course ID, learner ID | DESIGN_ONLY; status/uniqueness policy SOURCE_REQUIRED. |
| Learner profile | users | ID, full name, avatar URL | Candidate for UserSummary; role/null/deletion policy unresolved. |
| Denominator | lessons | ID, course ID, status | Published filter DERIVED from API #9. |
| Per-lesson progress | lesson_progress | Learner ID, lesson ID, status, percent | Key/enums/aggregation and live schema unverified. |

V1-PILOT relations course_enrollments, lesson_progress_facts, and progress_snapshots use UUID/versioned design and are not interchangeable with the catalog int64 IDs or legacy candidate above.

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
