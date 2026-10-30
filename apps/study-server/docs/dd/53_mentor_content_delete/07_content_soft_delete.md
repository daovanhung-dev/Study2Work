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
| Physical table | `contents` in legacy DDL/migration 006; live schema unverified. |
| Operation | Soft delete |
| Logical key | `contents.id` BIGINT in the local DDL; live schema unverified. |
| Dependencies | Content.parent_id là quan hệ parent-child trực tiếp được catalog khai báo. |
| Transaction | View-owned transaction; validate RETURNING before commit, rollback on failure. |
| History | Giữ Content/version/review history theo proposal; storage chưa xác nhận. |

## Update mapping

API #53 updates local `contents.deleted_at = CURRENT_TIMESTAMP` and returns the stored timestamp; live schema and migration application remain unverified.

## Insert mapping

N/A — API #53 không tạo Content hoặc record nghiệp vụ khác.

## Delete mapping

| No | Logical target | Logical field | Value source | Rule | Physical mapping/status |
|---:|---|---|---|---|---|
| 1 | Content target | id | Path content_id | Chọn target đã được xác thực và Mentor có quyền quản lý | Local `contents.id`; live schema unverified. |
| 2 | Content target | Deleted marker | Soft-delete action | Đánh dấu target không còn hoạt động; không hard-delete | Local column `contents.deleted_at`; runtime sets it to `CURRENT_TIMESTAMP`; live schema unverified. |
| 3 | Content target | deleted_at result | Database RETURNING value | Trả timestamp được ghi bởi UPDATE trong DeleteResult | Field DIRECT; local implementation returns `contents.deleted_at`; DDL timestamp has no timezone and live interpretation is unverified. |
| 4 | Content child | parent_id | Stored Content relation | Nếu còn child chưa xóa, 422 candidate; không cascade/reparent | Field DIRECT; Active predicate `deleted_at IS NULL` is used by API #49; child-block/cascade policy remains DERIVED. |
| 5 | Content target | status | Stored Content status | Nếu PUBLISHED, đề xuất gọi #52 unpublish; không gán DELETED | Gate DERIVED; enum/storage chưa đầy đủ. |
| 6 | Content/version/review history | Existing logical state | Soft-delete operation | Giữ history, không xóa revision/review decision | DERIVED; physical retention/audit SOURCE_REQUIRED. |

Local API #53 mutation is implemented. The direct-child and PUBLISHED guards, non-PUBLISHED eligibility, repeat-delete semantics, moderation queue behavior, and history/audit retention policy remain open or DERIVED. Chi tiết: [05_Data_Mapping.md](./05_Data_Mapping.md).

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
