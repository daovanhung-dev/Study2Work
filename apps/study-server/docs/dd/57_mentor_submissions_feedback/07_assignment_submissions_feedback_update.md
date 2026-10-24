---
title: "Định nghĩa table — assignment_submissions feedback update"
order: 7
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | assignment_submissions |
| Logical table | Bài nộp bài tập |
| Operation | UPDATE candidate |
| Data Mapping step | 3 |

## Update mapping

**Áp dụng khi**

- Candidate submission hiện hữu được xác định và Mentor được xác nhận có quyền trên course.
- Cập nhật field này là DERIVED từ legacy nullable feedback column và AC-23 feedback step; live schema chưa xác minh.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| 1 | feedback | Feedback text | TEXT | SOURCE_REQUIRED | N/A | N | N/A | Thay giá trị hiện tại bằng candidate feedback value | Request descriptor feedback text sau khi wire key được xác nhận | 3 | Existing legacy candidate column; nullable in DDL; overwrite/history semantics unresolved. |

## Insert mapping

**Áp dụng khi**

- SOURCE_REQUIRED — diagram ghi INSERT/UPDATE nhưng không có bảng history hoặc quy tắc insert được duyệt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không đề xuất INSERT khi chưa có target relation | N/A | N/A | Không invent table/cột lịch sử. |

## Delete mapping

**Áp dụng khi**

- N/A — API #57 không khai báo DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | Không có thao tác DELETE. |

## Điều kiện candidate UPDATE

- Khóa candidate: assignment_submissions.id = :submission_id.
- Phạm vi authorization candidate: submission.assignment_id → assignments.course_id → courses.id.
- Predicate owner candidate: courses.mentor_id = authenticated Mentor ID; DERIVED, identity mapping chưa được xác nhận.
- Chỉ candidate column assignment_submissions.feedback được thay đổi.
- Request attachments không có column/relation được ánh xạ ở file này.
- Không thay score hoặc status do API #56 sở hữu.

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
