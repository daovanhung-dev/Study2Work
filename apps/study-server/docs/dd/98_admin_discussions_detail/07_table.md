---
title: "Table Mapping"
order: 7
dd_id: "98"
api_name: "Lấy đầy đủ thread + report detail"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Table mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Table Mapping

## Read mapping inventory

| Query | Source/relation | Candidate fields | Condition / join | Purpose | Status |
|---|---|---|---|---|---|
| Q1 | Logical report target | Report ID, discussion ID and relation unknown | AC-37 selected report/thread detail | Resolve request target | `SOURCE_REQUIRED`; no physical relation approved |
| Q1a | Legacy `discussions` | `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, `created_at`, `updated_at` | Candidate `id = :discussion_id` | Discussion projection | Legacy DDL only; title missing; nullable FKs |
| Q2 | Logical discussion reports | Reason, severity, reporter, status, created time unknown | Join key and report grain unknown | AC-37 report detail | `SOURCE_REQUIRED`; do not guess a table |
| Q3 | Legacy `discussions` child alias | `id`, `parent_id`, `user_id`, `content`, `status`, `created_at` | Candidate `child.parent_id = root.id` | `DiscussionComment[]` | `DERIVED` from #42; no Admin visibility filter approved |
| Q4 | Legacy `users` | `id`, `full_name`, `avatar_url` | Candidate `users.id = discussions.user_id` | `UserSummary` | Candidate only; required relation/null handling unresolved |
| Q5 | Logical PageMeta | `page`, `size`, `total`, `total_pages` | One-item Page proposal | Catalog response shape | `DERIVED` from #42, not approved |

## Write mapping

| Operation | Target | Fields | Status |
|---|---|---|---|
| INSERT | N/A | No row created | N/A — read-only |
| UPDATE | N/A | No discussion/report state changed | N/A — read-only |
| DELETE | N/A | No discussion/report deleted | N/A — read-only |

## Schema boundary

- `infra/postgres/study-server/DB.sql` is a checked-in legacy schema artifact, not live database verification.
- It defines `discussions(id, course_id, user_id, parent_id, content, status, created_at, updated_at)`; course/user/parent keys are nullable in DDL.
- No discussion-report relation or report-detail fields are declared in that schema; `report_snapshots` in V1-PILOT is analytics and is not a discussion report source.
- The logical response requires `Discussion.title`; no title column exists in the legacy guide/DDL. Do not derive it from `content`.
- This DD defines no SQL or schema change.

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
