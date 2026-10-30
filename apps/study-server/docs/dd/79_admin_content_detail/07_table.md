---
title: "Định nghĩa table"
order: 7
dd_id: "79"
api_name: "Lấy chi tiết content và metadata review"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

API #79 chỉ đọc một current Content row từ checked-in legacy candidate `contents`; live schema/deployment chưa được xác minh.

| Table | Cột dùng | Ý nghĩa | Điều kiện/ghi chú |
|---|---|---|---|
| `contents` | `id` | Khóa Content | Bind bằng path `content_id`. |
| `contents` | `course_id` | Course owner relation | Trả trực tiếp; không dùng để suy ra author. |
| `contents` | `content_type`, `title`, `payload`, `status` | Content projection | Map sang reusable Content response. |
| `contents` | `parent_id`, `content_order` | Quan hệ cha và thứ tự sibling | `parent_id` nullable; `content_order` map thành `order`. |
| `contents` | `deleted_at` | Soft-delete marker | Chỉ trả row khi `deleted_at IS NULL`. |
| `content_versions` | No columns queried | Snapshot history from migration 007 | No revision selector; not read by API #79. |
| Content author | No source column/relation | AC-33 metadata read intent | No approved mapping; do not infer from updater, reviewer, or course Mentor. |

`contents`/`content_versions` are checked-in legacy schema candidates used by APIs #49–#53 and #78–#79. This does not establish that the schema is deployed. V1-PILOT UUID content artifacts are not interchangeable with this BIGINT projection.

## Update mapping

N/A — API #79 không cập nhật dữ liệu.

## Insert mapping

N/A — API #79 không thêm dữ liệu.

## Delete mapping

N/A — API #79 không xóa dữ liệu. Approve/reject và audit thuộc API #80/#81.

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
