---
title: "Định nghĩa table"
order: 7
dd_id: "82"
api_name: "Lấy danh sách lesson"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Phạm vi thao tác

N/A — READ-ONLY API. API #82 chỉ đọc danh sách lesson; không có INSERT/UPDATE/DELETE/UPSERT. Các thay đổi thuộc API #84–#86 trong AC-34.

## Candidate read source — legacy `lessons`

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `lessons` |
| Logical table | Lesson |
| Operation | SELECT only |
| Data Mapping step | [Step 2](./05_Data_Mapping.md#2-get-thong-tin) |
| Source evidence | `infra/postgres/study-server/DB.sql` legacy DDL artifact |
| Live schema status | Chưa xác minh |

| Physical column | Candidate response/query mapping | Nullable in legacy DDL | Notes |
|---|---|---:|---|
| `id` | `id` | No | BIGSERIAL primary key. |
| `course_id` | `course_id`; query filter `course` | Yes | Contract `Lesson.course_id` required; discrepancy. |
| `name` | `title` | No | Alias also used by API #09. |
| `content` | `content` | Yes | Optional in reusable schema. |
| `video_url` | `video_url` | Yes | Optional in reusable schema. |
| `sort_order` | `order` | Yes in legacy DDL | DDL default 0; contract requires int32. |
| `status` | `status` and optional filter | Yes in legacy DDL | DDL default `DRAFT`; full enum/casing unknown. |
| `type` | No mapping | N/A | No compatible Lesson type column in inspected source. |

## Non-selected V1-PILOT model

`infra/postgres/02_study_db.sql` defines UUID lessons connected to chapters and course versions, with `title`, `summary`, `position`, `estimated_minutes`, and `is_preview`. It lacks the same BIGINT `course_id`/status model and does not establish `type`; do not use it as if equivalent to the catalog Lesson schema.

## Write mapping

No write SQL or mutation mapping applies. Do not create audit, progress, resource, or type tables for this GET API.

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
