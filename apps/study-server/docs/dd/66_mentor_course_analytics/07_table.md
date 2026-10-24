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

N/A — READ-ONLY API. API #66 không ghi, sửa hoặc xóa dữ liệu nên không có mutation table mapping.

## Candidate read source boundary

| Logical role | Relation | Dữ liệu cần có | Trạng thái |
|---|---|---|---|
| Course scope/access | Legacy candidate courses | Course ID và owner relation | DESIGN_ONLY; identity/assignment predicate DERIVED/SOURCE_REQUIRED. |
| Learning-event source | Chưa được xác định | Event thuộc course, actor Student, occurrence time, dedup identity | SOURCE_REQUIRED; không tạo tên bảng/cột. |

Legacy lesson_progress và V1-PILOT progress facts/snapshots lưu trạng thái/fact tổng hợp, không phải event history. Generic audit/outbox relations không được xem là learner event source nếu chưa có domain mapping được phê duyệt.

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
