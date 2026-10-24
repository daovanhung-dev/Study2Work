---
title: "Định nghĩa table"
order: 7
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "5. Table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical entity | Admin Notification |
| Candidate physical table | Legacy notifications only; not approved for API #94 |
| Source | infra/postgres/study-server/DB.sql and DB_UNICA_TABLES.md |
| Runtime status | No API #94 persistence source verified |
| Mutation | Logical UPDATE per AC-36; concrete column set unresolved |

## Candidate legacy columns

| Column | Legacy type/constraint | Candidate relation to API | Status |
|---|---|---|---|
| id | BIGSERIAL PRIMARY KEY | Candidate for Notification.id:int64 | Compatible type candidate; active Admin model unverified |
| user_id | BIGINT NULL REFERENCES users(id) | One recipient on a legacy row | Cannot represent campaign recipient association by itself |
| sender_id | BIGINT NULL REFERENCES users(id) | Possible actor/sender relation | Do not set from token without approved actor mapping |
| title | VARCHAR(200) NOT NULL | Candidate for Notification.title | Candidate only; no live constraint confirmation |
| content | TEXT NOT NULL | Candidate for Notification.content | Candidate only |
| type | VARCHAR(30) NULL | Legacy notification category | Not proven equivalent to channels[] |
| is_read | BOOLEAN DEFAULT FALSE | Legacy read flag | Not equivalent to Notification.status or read_at |
| created_at | TIMESTAMP NOT NULL | Candidate for Notification.created_at | Preserve on update; active table/precision unverified |

## Insert mapping

N/A — API #94 is an UPDATE endpoint. No insert is specified by AC-36.

## Update mapping

| Logical input/output | Candidate column | Proposed operation | Status |
|---|---|---|---|
| notification_id / data.id | notifications.id | Locate existing row | Candidate mapping; target model unapproved |
| title | notifications.title | Replace value if body is approved | DERIVED field; candidate column only |
| content | notifications.content | Replace value if body is approved | DERIVED field; candidate column only |
| channels[] | No compatible legacy column found | No physical update mapping | SOURCE_REQUIRED |
| status | No compatible legacy column found | No physical update mapping | SOURCE_REQUIRED |
| scheduled_at | No compatible legacy column found | No physical update mapping | SOURCE_REQUIRED |
| read_at | No compatible legacy column found | Preserve/no mutation specified | SOURCE_REQUIRED |
| created_at | notifications.created_at | Preserve original value | Candidate only; do not update |
| Recipient association | notifications.user_id is singular per row | Do not infer campaign relationship from it | No approved mapping |

No SQL or new table/column is proposed. Legacy schema is a design candidate, not evidence of live persistence.

## Delete mapping

N/A — API #94 does not declare DELETE. Cancellation belongs to the adjacent #95 design and is not inferred here.

## Physical mapping boundary

- V1-PILOT notifications and notification_deliveries use a separate UUID learner/delivery model; they are not candidate targets for this BIGINT Admin contract without an explicit architecture decision.
- No channels, campaign status, scheduled_at or Admin recipient association is present in the reviewed legacy table.
- The owner must select a persistence model and define the full update transaction before this mapping can be implementation-ready.

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
