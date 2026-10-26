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
| Q1 | `discussion_reports` | `id`, `discussion_id`, `reason_code`, `severity`, `status`, `created_at` | `status IN ('OPEN','IN_REVIEW')`; exact optional filters; latest active report | Select unique Discussion queue | Migration 014 `DERIVED`; deployment/writer unverified |
| Q1a | Legacy `discussions` | `id`, `course_id`, `user_id`, `content`, `status` | Join `discussion_reports.discussion_id = discussions.id`; supports root or reply targets | Discussion summary | Legacy DDL candidate; nullable required fields fail mapping |
| Q1b | Legacy `users` | `id`, `full_name`, `avatar_url` | `users.id = discussions.user_id` | `UserSummary` author | Legacy candidate; missing author returns 500 |
| Q1c | Legacy `discussions` child alias | Not queried | Queue summary does not expand thread | `comments=[]` | `DERIVED`; full thread belongs to #98 |
| Q2 | `discussion_reports` + `discussions` | `COUNT(DISTINCT discussions.id)` | Same status/reason/severity predicates as Q1 | `PageMeta.total` | `DERIVED`; queue grain is Discussion |

## Write mapping

| Operation | Target | Fields | Status |
|---|---|---|---|
| INSERT | N/A | No row created | N/A — read-only |
| UPDATE | N/A | No report/discussion state changed | N/A — read-only |
| DELETE | N/A | No report/discussion deleted | N/A — read-only |

## Schema boundary

- `infra/postgres/study-server/DB.sql` is a checked-in legacy schema artifact, not live schema verification.
- Migration `014_discussion_reports.sql` adds `discussion_reports` with BIGINT FK to `discussions.id` (`ON DELETE RESTRICT`), BIGINT reporter FK to `users.id` (`ON DELETE RESTRICT`), free-form reason/severity, report state and timestamp. This is a local `DERIVED` candidate that preserves report evidence; API #100 must account for the FK before any hard-delete behavior.
- Queue-active states are `OPEN` and `IN_REVIEW`; terminal tokens are `RESOLVED` and `DISMISSED`. The status set follows the generic Work DDL as a design precedent, not a runtime dependency.
- `Discussion.title` is absent in legacy DDL and is derived from normalized content (120 chars). `comments[]` is empty in the list projection; #98 loads thread detail.
- The API does not create reports. Migration availability and any external report writer are unverified.

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
