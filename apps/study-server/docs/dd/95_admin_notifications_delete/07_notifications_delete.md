---
title: "Định nghĩa table"
order: 7
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "5. Table mapping"
status: "Draft — Needs Confirmation"
---

# Notification delete mapping

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical entity | Admin Notification at the path-selected recipient-row grain |
| Candidate physical table | Legacy `notifications`; same candidate currently written by #93 and updated by #94 |
| Related table | Legacy `notification_deliveries` from migration 009 |
| Source | `infra/postgres/study-server/DB.sql`, migration 009 and current #93/#94 source |
| Runtime status | API #95 wired locally; fake-DB tests do not prove live schema/deployment |
| Mutation | Physical DELETE of one eligible parent row; child outbox rows cascade under checked-in FK candidate |

## Candidate legacy columns

| Column | Legacy type/constraint | Candidate relation to API | Status |
|---|---|---|---|
| `notifications.id` | BIGSERIAL PRIMARY KEY | Path `notification_id` and DeleteResult.id | Current local mapping; live schema unverified |
| `notifications.user_id` | BIGINT NULL REFERENCES users(id) | One recipient on the legacy row | Establishes local row grain only; no batch expansion |
| `notifications.sender_id` | BIGINT NULL REFERENCES users(id) | Sender candidate | Not used to authorize actor |
| `notifications.operation_id` | UUID NULL | Shared derived batch metadata from #93 | Not used as delete key; sibling rows remain |
| `notifications.title/content` | VARCHAR(200)/TEXT NOT NULL | Existing notification data | Not read or mutated by #95 |
| `notifications.type/is_read/created_at` | Legacy category/read/create fields | Existing notification fields | Not lifecycle or deletion marker |
| `notification_deliveries.notification_id` | BIGINT NOT NULL FK, `ON DELETE CASCADE` | Child rows for the selected parent | Checked-in DDL supports local cascade; live behavior unverified |
| `notification_deliveries.channel/status` | CHECK: PUSH/EMAIL; QUEUED/SENT/FAILED | Eligibility projection | Local fallback requires unique channels and all QUEUED |

## Mutation mapping

| Logical target/effect | Candidate source | Operation | Status |
|---|---|---|---|
| Notification identity | `notifications.id` | Bind path ID; lock parent; delete exactly this row | DERIVED target mapping based on current #93/#94 |
| Cancellable local outbox | `notification_deliveries` | Lock by parent and require one or more rows, all `QUEUED` | DERIVED eligibility; not provider proof |
| Delivery-row removal | FK `ON DELETE CASCADE` | Parent DELETE cascades its child delivery rows in the same transaction | Direct checked-in DDL behavior; live schema unverified |
| DeleteResult.id | DELETE RETURNING `id` | Return deleted parent identity | DIRECT output type; local mapping DERIVED |
| DeleteResult.deleted_at | SQL `CURRENT_TIMESTAMP` in DELETE RETURNING | Return transaction DB timestamp; do not persist it | DIRECT output type; local timestamp mapping DERIVED |

No new SQL schema, table, column, enum or trigger is added. The implementation uses the currently checked-in legacy candidate, not a claim that it is an owner-approved or deployed Admin campaign model.

## Delete scope and history

- #93 creates one legacy notification row per explicit recipient and one delivery row per requested channel; #95 deletes only the row addressed by path ID.
- Rows for other recipients, including rows with the same `operation_id`, are not selected or deleted.
- The queued delivery rows for the selected parent are removed by the FK cascade; SENT/FAILED deliveries are rejected before parent DELETE.
- This local hard-delete does not preserve the selected row/outbox as an audit trail. Retention and cancellation history require an owner-approved model and policy.

## Physical mapping boundary

- V1-PILOT UUID learner notification/delivery tables are not queried or changed by API #95.
- Do not map legacy `is_read` or `type` to NotificationStatus.
- Do not infer scheduler/provider acknowledgement from `QUEUED` or from a successful local commit.
- Current DDL/migration files and fake-DB tests do not prove live schema or cascade behavior.

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
