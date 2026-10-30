---
title: "Định nghĩa table"
order: 7
dd_id: "99"
api_name: "Điều chỉnh trạng thái kiểm duyệt discussion"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "5. DB table mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

### Candidate `discussions` — legacy Study DDL only

| Thuộc tính | Giá trị | Basis/status |
|---|---|---|
| Table | `discussions` | Candidate row source from `infra/postgres/study-server/DB.sql` |
| Primary key | `id BIGSERIAL` | Legacy artifact; candidate for `discussion_id` |
| Related table | `users` via `user_id` | Candidate author projection; `user_id` nullable |
| Self relation | `parent_id` → `discussions.id` | Candidate comment/thread relation; nullable |
| State column | `status VARCHAR(20) DEFAULT 'ACTIVE'` | Candidate only; approved moderation state values/transitions absent |
| Audit relation | None in legacy DDL | `SOURCE_REQUIRED` |
| Live schema | Not verified | DDL is not runtime metadata evidence |

### Candidate legacy columns

| Legacy column | Type / constraint | Relevance | Basis/status |
|---|---|---|---|
| `id` | BIGSERIAL PRIMARY KEY | Candidate target key | Legacy DDL only |
| `course_id` | BIGINT REFERENCES `courses(id)` | Required by response `Discussion` | Nullable in legacy DDL |
| `user_id` | BIGINT REFERENCES `users(id)` | Candidate author key | Nullable in legacy DDL |
| `parent_id` | BIGINT NULL REFERENCES `discussions(id)` | Candidate thread/comment relation | Legacy DDL only |
| `content` | TEXT NOT NULL | Candidate response content | Legacy DDL only |
| `status` | VARCHAR(20) DEFAULT `ACTIVE` | Candidate moderation state column | Allowed values/transitions unresolved |
| `created_at` | TIMESTAMP NOT NULL | Candidate response timestamp source | Timezone convention unresolved |
| `updated_at` | TIMESTAMP NOT NULL | Existing candidate timestamp | #99 update behavior is not specified |

The legacy table has no `title`, report linkage, moderator identity, moderation reason or dedicated audit relation.

## Update mapping

| Logical field/effect | Candidate column | Source value | Rule/status |
|---|---|---|---|
| Target row | `discussions.id` | Path `discussion_id` | Candidate key mapping; live schema unverified |
| Moderation action | No approved action column | Body `action` | Logical moderation action direct; accepted token unresolved |
| Moderation state before | Candidate `discussions.status` | Current row | State eligibility and meaning unresolved |
| Moderation state after | Candidate `discussions.status` | Approved action-to-state mapping | Logical state update direct; token/value/transition `SOURCE_REQUIRED` |
| Discussion update timestamp | Candidate `discussions.updated_at` | No rule in catalog/diagram | Do not assume #99 writes it |
| Audit actor | No approved legacy target | Admin principal | Role direct; actor identity/storage `SOURCE_REQUIRED` |
| Audit action | No approved legacy target | Body `action` | Logical audit required; physical mapping `SOURCE_REQUIRED` |
| Audit reason | No approved legacy target | Body `reason` | Logical audit required; physical mapping and constraints `SOURCE_REQUIRED` |
| Audit before state | No approved legacy target | Current Discussion | AC-37 does not define snapshot shape; `SOURCE_REQUIRED` |
| Audit after state | No approved legacy target | Resulting Discussion | AC-37 does not define snapshot shape; `SOURCE_REQUIRED` |
| Audit trace | No approved legacy target | Request trace | Envelope convention; persistence `SOURCE_REQUIRED` |

No executable SQL mapping is approved. Do not treat action text as a status value without an approved action-to-state table.

## Insert mapping

| Logical audit field | Physical target/column | Source | Mapping/status |
|---|---|---|---|
| Actor identity | No selected legacy relation | Admin principal | `SOURCE_REQUIRED` |
| Action | No selected legacy relation | Body `action` | `SOURCE_REQUIRED` |
| Reason | No selected legacy relation | Body `reason` | `SOURCE_REQUIRED` |
| Before state | No selected legacy relation | Target row before mutation | Snapshot shape `SOURCE_REQUIRED` |
| After state | No selected legacy relation | Target row after mutation | Snapshot shape `SOURCE_REQUIRED` |
| Trace identifier | No selected legacy relation | Request trace | `SOURCE_REQUIRED` |
| Event identifier/time | No selected legacy relation | Generator/clock | Key and timestamp policy `SOURCE_REQUIRED` |

V1-PILOT defines `admin_adjustments` and `audit_events`, but both use UUID and versioned subject/resource fields. These artifacts do not establish a compatible FK or key mapping to the legacy BIGINT Discussion row and are not selected by this DD.

## Delete mapping

N/A — API #99 performs no DELETE. If Admin chooses to delete, AC-37 routes the action to API #100. No soft/hard-delete policy is specified here.

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
