---
title: "Định nghĩa mapping xóa Content"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "53"
api_name: "Xóa nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa mapping xóa Content

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| API ID | #53 |
| Logical entity | Content |
| Physical table | SOURCE_REQUIRED — không có generic Content table tương thích trong DDL hiện có. |
| Operation | Soft delete |
| Logical key | id:int64 theo reusable Content; physical key chưa xác nhận. |
| Dependencies | Content.parent_id là quan hệ parent-child trực tiếp được catalog khai báo. |
| Transaction | Một logical mutation; physical transaction chưa xác nhận. |
| History | Giữ Content/version/review history theo proposal; storage chưa xác nhận. |

## Update mapping

N/A — API #53 dùng logical soft delete; không định nghĩa UPDATE columns khi physical schema chưa có.

## Insert mapping

N/A — API #53 không tạo Content hoặc record nghiệp vụ khác.

## Delete mapping

| No | Logical target | Logical field | Value source | Rule | Physical mapping/status |
|---:|---|---|---|---|---|
| 1 | Content target | id | Path content_id | Chọn target đã được xác thực và Mentor có quyền quản lý | Physical relation/key SOURCE_REQUIRED. |
| 2 | Content target | Deleted marker | Soft-delete action | Đánh dấu target không còn hoạt động; không hard-delete | Marker/column/value SOURCE_REQUIRED; logical effect DIRECT. |
| 3 | Content target | deleted_at result | Thời điểm thao tác thành công | Trả trong DeleteResult; không giả định cột lưu | Field DIRECT; generator/storage DERIVED/SOURCE_REQUIRED. |
| 4 | Content child | parent_id | Stored Content relation | Nếu còn child chưa xóa, 422 candidate; không cascade/reparent | Field DIRECT; active predicate DERIVED; physical relation SOURCE_REQUIRED. |
| 5 | Content target | status | Stored Content status | Nếu PUBLISHED, đề xuất gọi #52 unpublish; không gán DELETED | Gate DERIVED; enum/storage chưa đầy đủ. |
| 6 | Content/version/review history | Existing logical state | Soft-delete operation | Giữ history, không xóa revision/review decision | DERIVED; physical retention/audit SOURCE_REQUIRED. |

Không có SQL mutation vật lý được đưa ra vì schema Content và soft-delete columns chưa được xác nhận. Chi tiết: [05_Data_Mapping.md](./05_Data_Mapping.md).

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
