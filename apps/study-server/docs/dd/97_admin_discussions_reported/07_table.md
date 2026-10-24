---
title: "Table Mapping"
order: 7
dd_id: "97"
api_name: "Lấy reported discussions"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Table mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Table Mapping

## Read mapping inventory

| Query | Source/relation | Candidate fields | Condition / join | Purpose | Status |
|---|---|---|---|---|---|
| Q1 | Logical report source | Report identity, discussion key, reason, severity, report state and timestamps are not defined | AC-37 says read reports + discussion summary | Select moderation queue | `SOURCE_REQUIRED`; do not name/create a physical table |
| Q1a | Legacy `discussions` | `id`, `course_id`, `user_id`, `parent_id`, `content`, `status`, `created_at`, `updated_at` | Candidate row read; report predicate unavailable | Discussion projection candidate | Legacy DDL only; live schema unverified |
| Q1b | Legacy `users` | `id`, `full_name`, `avatar_url` | Candidate `users.id = discussions.user_id` | `UserSummary` author candidate | Join/null semantics unresolved |
| Q1c | Legacy `discussions` child alias | `id`, `parent_id`, `user_id`, `content`, `created_at` | Candidate child-to-parent self-reference | `DiscussionComment[]` candidate | Queue comment extent unresolved |
| Q2 | Logical count source | Queue item count | Same report filters and dedup rule as Q1, not specified | `PageMeta.total` | `SOURCE_REQUIRED` |

## Write mapping

| Operation | Target | Fields | Status |
|---|---|---|---|
| INSERT | N/A | No row created | N/A — read-only |
| UPDATE | N/A | No report/discussion state changed | N/A — read-only |
| DELETE | N/A | No report/discussion deleted | N/A — read-only |

## Schema boundary

- `infra/postgres/study-server/DB.sql` is a legacy checked-in schema artifact, not live schema verification.
- It defines `discussions(id, course_id, user_id, parent_id, content, status, created_at, updated_at)`; `course_id`, `user_id`, `parent_id` are nullable as declared in the DDL.
- No discussion report relation or `reason`/`severity` columns are declared in that DDL.
- The logical response requires `Discussion.title`; no title column exists in the legacy guide/DDL. Do not derive it from `content`.
- No schema changes or SQL are part of this DD.

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
