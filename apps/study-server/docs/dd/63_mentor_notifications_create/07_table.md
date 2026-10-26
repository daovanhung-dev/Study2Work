---
title: "Định nghĩa table"
order: 7
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Notification và delivery outbox

## Thông tin mapping

| Thuộc tính | Giá trị |
|---|---|
| Physical target | Local legacy BIGINT `notifications` plus migration 009 delivery outbox. |
| Operation | Insert one notification per recipient and one delivery row per recipient/channel in one transaction. |
| Data Mapping step | 2–4 |
| Evidence | AC-25 requires Notification + recipients then Push/Email; API #62 returns legacy BIGINT Student IDs; legacy Study DDL has per-user `notifications`; API #64 requires int64 notification ID. |
| Status | `DERIVED_LOCAL_DDL`; live schema/migration unverified; worker/provider absent. |

## Existing table extended: `notifications`

| Column | Local definition | Mapping | State |
|---|---|---|---|
| `id` | `BIGSERIAL PRIMARY KEY` | Generated Notification ID; returned in `meta.notification_ids`. | Existing legacy DDL. |
| `user_id` | `BIGINT NULL REFERENCES users(id)` | One selected Student per notification row. | Existing legacy DDL. |
| `sender_id` | `BIGINT NULL REFERENCES users(id)` | Authenticated Mentor numeric JWT subject. | Existing legacy DDL. |
| `title` | `VARCHAR(200) NOT NULL` | Request title, unchanged. | Existing legacy DDL; API validates max 200. |
| `content` | `TEXT NOT NULL` | Request int64 rendered in base-10. | DERIVED type mapping; semantic conflict remains. |
| `type` | `VARCHAR(30) NULL` | NULL; do not overload as channel. | Existing legacy DDL. |
| `is_read` | `BOOLEAN DEFAULT FALSE` | Read-state only; not delivery status. | Existing legacy DDL. |
| `created_at` | `TIMESTAMP NOT NULL` | DB timestamp used as initial Operation timestamps. | Existing legacy DDL. |
| `operation_id` | `UUID NULL` | Shared group ID for all notification rows created by one accepted request. | Added by migration 009; DERIVED. |

## New table: `notification_deliveries`

| Column | Local definition | Mapping | State |
|---|---|---|---|
| `id` | `BIGSERIAL PRIMARY KEY` | Delivery outbox row key. | DERIVED migration 009. |
| `notification_id` | `BIGINT NOT NULL REFERENCES notifications(id) ON DELETE CASCADE` | Recipient notification. | DERIVED; int64 aligns with legacy ID/API #64. |
| `channel` | `VARCHAR(16) NOT NULL CHECK (channel IN ('PUSH','EMAIL'))` | One delivery target from request `channels`. | DERIVED from AC-25 labels. |
| `status` | `VARCHAR(16) NOT NULL DEFAULT 'QUEUED' CHECK (status IN ('QUEUED','SENT','FAILED'))` | Initial durable outbox state; future worker updates it. | DERIVED state set; no worker in current Study runtime. |
| `queued_at` | `TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP` | Time the API persisted the delivery request. | DERIVED local DDL. |
| `updated_at` | `TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP` | Initial update timestamp for worker lifecycle. | DERIVED local DDL. |

### Constraints/indexes

- Unique `(notification_id, channel)` prevents duplicate delivery intent for the same channel on one Notification.
- Index `(status, queued_at, id)` allows a future worker to claim queued records in stable order.
- Migration 009 is a checked-in artifact only; it is not run against a live database in this task.

## Logical Operation projection

| Response field | Source | Rule | State |
|---|---|---|---|
| `id` | `notifications.operation_id` | UUID shared by all rows in the batch. | Reusable Operation UUID direct; persistence DERIVED. |
| `kind` | Application constant | `NOTIFICATION_DISPATCH`. | DERIVED; enum is not defined in catalog. |
| `status` | Delivery rows at acceptance | `QUEUED` after successful commit. | DERIVED. |
| `owner_id` | `notifications.sender_id` | Numeric Mentor owner. | Local source pattern. |
| `submitted_at` | First inserted `notifications.created_at` | DB timestamp from accepted batch. | DERIVED projection. |
| `updated_at` | Same initial timestamp | No worker has advanced delivery state yet. | DERIVED projection. |
| `completed_at` | None | Omit on an accepted queued job. | Optional schema field. |
| `result` | None | Omit; do not place notification data in Payment schema. | Optional schema field. |

## Handoff to API #64

- `meta.notification_ids` contains each per-recipient `notifications.id` in request order.
- API #64 may use each numeric ID to read that recipient notification's channel delivery rows.
- `Operation.id` is a UUID group key and is not substituted for any numeric notification ID.
- API #18 tracking is not implemented; its catalog path type and Operation lifecycle remain unresolved.

## Exclusions

- No V1-PILOT UUID notification or `notification_deliveries` DDL is mixed into this legacy BIGINT schema.
- `notifications.is_read` is not interpreted as send status.
- No external Push/Email provider, worker, retry/backoff, partial-delivery aggregation or idempotency storage is introduced in this API session.
- No migration is applied to a database; the live schema remains unverified.

---
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
