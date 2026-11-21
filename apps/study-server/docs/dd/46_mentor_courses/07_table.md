---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — N/A — READ-ONLY API

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — không ghi dữ liệu |
| Logical table | Course list cho Mentor |
| Operation | `SELECT` only |
| Data Mapping step | 2 |
| Evidence | API #46 catalog, AC-21, API #6 precedent; schema candidate chưa xác nhận live |

## Update mapping

**Áp dụng khi**

- N/A — API #46 không cập nhật bảng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có UPDATE. |

## Insert mapping

**Áp dụng khi**

- N/A — API #46 không tạo record.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có INSERT. |

## Delete mapping

**Áp dụng khi**

- N/A — API #46 không xóa record.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không có DELETE. |

## Read source candidates

| No | Table | Column | Purpose | Evidence status |
|---:|---|---|---|---|
| 1 | `courses` | `id` | Course ID. | Legacy candidate; pilot DDL uses UUID. |
| 2 | `courses` | `name` | Map to Course.title. | API #6 precedent. |
| 3 | `courses` | `description` | Optional description. | Legacy candidate. |
| 4 | `courses` | `thumbnail_url` | Optional thumbnail. | Legacy candidate. |
| 5 | `courses` | `price` | Required contract price. | Legacy column nullable. |
| 6 | `courses` | `status` | Course status and optional filter. | Enum values unresolved. |
| 7 | `courses` | `mentor_id` | Candidate owner scope and Mentor join. | Legacy only; assignment source absent. |
| 8 | `courses` | `created_at` | Candidate default order. | Legacy candidate; sort `DERIVED`. |
| 9 | `users` | `id` | Course.mentor.id. | API #6 projection precedent. |
| 10 | `users` | `full_name` | Course.mentor.full_name. | Required summary field. |
| 11 | `users` | `avatar_url` | Optional Mentor avatar. | API #6 projection precedent. |

## Mapping gaps

| Contract item | Candidate source | Status | Impact |
|---|---|---|---|
| `Course.category` | No course-category relation found | SOURCE_REQUIRED | Omit optional field until source exists. |
| Mentor assignment | No assignment table/relation found in inspected artifacts | SOURCE_REQUIRED | Direct `mentor_id` does not cover assigned courses. |
| `CourseStatus` values | Catalog type only | SOURCE_REQUIRED | Filter validation cannot be finalized. |
| Live schema | Not inspected/verified | NOT_FOUND | DDL remains candidate evidence only. |
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
