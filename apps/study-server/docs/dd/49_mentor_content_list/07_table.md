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

# Định nghĩa table — READ-ONLY API

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `courses`, `contents` trong legacy Study DDL artifact |
| Logical table | Course và Content nodes |
| Operation | SELECT; không ghi |
| Data Mapping step | 2 |
| Evidence | API #49 query module, `DB.sql`, migration 006; live schema chưa xác minh |

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

- N/A — API #49 không xóa record. API #53 là endpoint delete riêng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có DELETE. |

## Read mapping

| No | Source/table | Column | Schema type | Contract field/use | Evidence/status |
|---:|---|---|---|---|---|
| 1 | `courses` | `id` | BIGSERIAL | Q1 course lookup by path ID | Legacy DDL and current query; live schema unverified |
| 2 | `courses` | `mentor_id` | BIGINT | Q1 direct-owner comparison | Runtime owner check; assignment relation not included |
| 3 | `contents` | `id` | BIGSERIAL | `data[].id` | Legacy DDL/migration 006; live schema unverified |
| 4 | `contents` | `course_id` | BIGINT | Query scope and `data[].course_id` | FK → `courses.id` |
| 5 | `contents` | `content_type` | TEXT | `data[].content_type` | Open string; enum values unspecified |
| 6 | `contents` | `title` | TEXT | `data[].title` | Direct projection |
| 7 | `contents` | `payload` | JSONB object | `data[].payload` | DDL check requires object; subtype keys unspecified |
| 8 | `contents` | `status` | TEXT | `data[].status` | Open string; all values returned |
| 9 | `contents` | `parent_id` | BIGINT NULL | `data[].parent_id` | Composite same-course FK; null omitted in response |
| 10 | `contents` | `content_order` | INTEGER | `data[].order` | Direct alias; sorts before ID tie-breaker |
| 11 | `contents` | `deleted_at` | TIMESTAMP NULL | Active tree predicate | API filters `deleted_at IS NULL`; physical soft-delete date |
| 12 | V1-PILOT `chapters` / `lessons` / `content_blocks` | UUID/versioned fields | Pilot schema | No direct mapping | Kept separate from legacy BIGINT API model |

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
