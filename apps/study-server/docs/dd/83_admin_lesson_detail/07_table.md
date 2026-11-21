---
title: "Định nghĩa table"
order: 7
dd_id: "83"
api_name: "Lấy lesson detail"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Phạm vi thao tác

N/A — READ-ONLY API. API #83 chỉ thực hiện SELECT; không có INSERT/UPDATE/DELETE/UPSERT. Các mutation thuộc API #84–#86.

## Candidate read source — legacy `lessons`

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `lessons` |
| Logical table | Lesson |
| Operation | SELECT only |
| Data Mapping step | [Step 2](./05_Data_Mapping.md#step-2-get-thong-tin) |
| Source evidence | `infra/postgres/study-server/DB.sql` legacy DDL artifact |
| Live schema status | Chưa xác minh |

| Physical column | Response field | Legacy DDL type/nullability | Notes |
|---|---|---|---|
| `id` | `id` | BIGSERIAL, primary key | Candidate selector `id = :lesson_id`. |
| `course_id` | `course_id` | BIGINT, nullable FK | API contract requires int64; unresolved NULL handling. |
| `name` | `title` | VARCHAR(200), NOT NULL | Alias used by API #09. |
| `content` | `content` | TEXT, nullable | Optional Lesson field. |
| `video_url` | `video_url` | TEXT, nullable | Optional Lesson field. |
| `sort_order` | `order` | INT, default 0 | Alias used by API #09. |
| `status` | `status` | VARCHAR(20), default DRAFT | LessonStatus values/casing unresolved. |

## Dependency tables not queried

Legacy DDL/ERD show `resources.lesson_id` and `lesson_progress.lesson_id` referencing `lessons.id`. AC-34 does not define a response field or query output for these dependencies. No table mapping/query is added here. API #86 must recheck current dependencies if deletion policy requires it.

## Non-selected V1-PILOT model

The pilot `lessons` table uses UUID `id`, `chapter_id`, `course_version_id`, `title`, `summary`, `position`, `estimated_minutes`, and `is_preview`. It is not interchangeable with the legacy BIGINT model or reusable `Lesson` response. No mapping across the two schemas is proposed.

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
