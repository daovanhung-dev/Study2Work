---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — N/A — READ-ONLY API

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | Legacy `courses` chỉ là candidate cho Q1; Content tree source chưa xác định |
| Logical table | Course content tree / `Content` response theo catalog |
| Operation | SELECT design only; không có write |
| Data Mapping step | 2 |
| Evidence | API #49 catalog, AC-22, DB guide/ERD, pilot DDL; live schema chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — API #49 không cập nhật bảng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có UPDATE. |

## Insert mapping

**Áp dụng khi**

- N/A — API #49 không tạo record. API #50 là endpoint create riêng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có INSERT. |

## Delete mapping

**Áp dụng khi**

- N/A — API #49 không xóa record. API #52 là endpoint delete riêng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có DELETE. |

## Read mapping

| No | Source/table | Column | Schema type | Contract field/use | Evidence/status |
|---:|---|---|---|---|---|
| 1 | Legacy `courses` | `id` | BIGSERIAL | Candidate lookup using path course_id | ERD V1 design only; ID format not live-verified |
| 2 | Legacy `courses` | `mentor_id` | BIGINT | Candidate direct-owner access check | `DERIVED`; Mentor identity/assignment unresolved |
| 3 | Content tree | SOURCE_REQUIRED | SOURCE_REQUIRED | `data.id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `order` | No approved generic relation or mapping |
| 4 | V1-PILOT `chapters` / `lessons` / `content_blocks` | UUID IDs, versioned fields | Pilot schema | Possible conceptual learning hierarchy only | Do not map to API BIGINT `Content` without contract/schema decision |

## Mutation summary

`N/A — READ-ONLY API`; there is no mutation matrix beyond the explicit N/A record in Data Mapping.

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
