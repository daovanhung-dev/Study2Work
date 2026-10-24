---
title: "Định nghĩa table"
order: 7
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "5. Table mapping"
status: "Draft — Needs Confirmation"
---

# Notification logical delete mapping

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical entity | Admin Notification |
| Candidate physical table | Legacy notifications only; not approved for API #95 |
| Source | infra/postgres/study-server/DB.sql and DB_UNICA_TABLES.md |
| Runtime status | No API #95 persistence source verified |
| Mutation | Logical DELETE/mark cancelled per AC-36; physical marker unresolved |

## Candidate legacy columns

| Column | Legacy type/constraint | Candidate relation to API | Status |
|---|---|---|---|
| id | BIGSERIAL PRIMARY KEY | Candidate for DeleteResult.id:int64 | Compatible type candidate; active Admin model unverified |
| user_id | BIGINT NULL REFERENCES users(id) | One recipient on a legacy row | Does not establish campaign recipient grouping |
| sender_id | BIGINT NULL REFERENCES users(id) | Possible creator/sender relation | Do not infer actor mapping |
| title | VARCHAR(200) NOT NULL | Notification display content | Not mutated by this API |
| content | TEXT NOT NULL | Notification body | Not mutated by this API |
| type | VARCHAR(30) NULL | Legacy category | Not a lifecycle status |
| is_read | BOOLEAN DEFAULT FALSE | Legacy read flag | Not a deletion/cancellation marker |
| created_at | TIMESTAMP NOT NULL | Creation timestamp | Not a deletion timestamp |

## Logical mutation mapping

| Logical target/effect | Candidate column | Proposed operation | Status |
|---|---|---|---|
| Notification identity | notifications.id | Locate target by notification_id | Candidate only |
| Draft removal | No compatible column found | Tombstone/hidden marker not defined in legacy table | DERIVED intent; SOURCE_REQUIRED storage |
| Scheduled cancellation | No compatible column found | Cancelled state not defined in legacy table | DERIVED intent; SOURCE_REQUIRED storage |
| DeleteResult.deleted_at | No compatible column found | Return approved action-completion timestamp | Direct output field; physical source SOURCE_REQUIRED |
| Notification deliveries | No legacy Admin relation found | Preserve prior history; no cascade delete | No target mapping |

No SQL, new table, column, enum or trigger is proposed. The legacy table is not an approved Admin campaign model.

## Hard delete mapping

N/A as a proposed default. Retain notification/history records through an approved logical marker so that delivery status and audit history are not erased. This preservation rule is DERIVED and requires confirmation.

## Physical mapping boundary

- V1-PILOT notifications uses UUID learner ownership and includes read_at/expires_at, but no Admin tombstone or DeleteResult.deleted_at.
- V1-PILOT notification_deliveries uses UUID IDs and is explicitly append-only; it is not an Admin mapping target.
- Do not map legacy is_read or type to NotificationStatus.
- Owner must choose Admin schema, tombstone semantics and timestamp source before implementation.

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
