---
title: "Định nghĩa table"
order: 7
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

API chỉ đọc; không có mutation table mapping.

## Read mapping — local runtime

| Thứ tự | Relation | Column | Vai trò | Bằng chứng/trạng thái |
|---:|---|---|---|---|
| 1 | courses | id | Tìm course theo required path | Legacy DDL; live schema chưa xác minh. |
| 1 | courses | mentor_id | Kiểm tra direct owner theo JWT sub | Legacy DDL; DERIVED access rule. |
| 2 | lessons | id | Nối lesson_progress.lesson_id | Legacy DDL. |
| 2 | lessons | course_id | Giới hạn lesson trong course | Legacy DDL. |
| 2 | lessons | status | Chỉ lấy PUBLISHED lesson | Legacy DDL; cùng convention #65. |
| 3 | users | id | Nối lesson_progress.user_id | Legacy DDL. |
| 3 | users | role | Chỉ đếm Student actor | Legacy DDL; giá trị STUDENT theo source #65. |
| 4 | lesson_progress | user_id | Một phần khóa cặp hoạt động | Legacy DDL. |
| 4 | lesson_progress | lesson_id | Một phần khóa cặp hoạt động | Legacy DDL. |
| 4 | lesson_progress | last_accessed_at | Dấu truy cập gần nhất còn lưu | Legacy DDL current state; không phải event history. |

## Logical aggregate

- Một record analytics proxy ứng với một cặp user_id/lesson_id phân biệt có timestamp truy cập.
- Duplicate progress rows cùng cặp được gộp bằng GROUP BY; timestamp cặp là MAX(last_accessed_at).
- Trả tracked_lesson_accesses = số cặp, students_with_activity = số user Student phân biệt, last_activity_at = timestamp lớn nhất.
- V1-PILOT block_progress_facts.last_event_id, lesson_progress_facts, progress_snapshots, audit_events và outbox_events không được truy vấn.
- Không có bảng/cột learning-event ledger trong các DDL đã rà soát; không thể khôi phục số lần truy cập từ state hiện có.

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
