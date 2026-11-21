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
| Logical entity | Admin Notification (recipient-level fallback) |
| Candidate physical table | Legacy notifications and notification_deliveries |
| Source | infra/postgres/study-server/DB.sql; migration 009_notification_delivery_outbox.sql |
| Runtime status | API #94 targets these checked-in candidates; deployed schema unverified |
| Mutation | UPDATE `notifications.title/content` only; read/lock delivery rows |

## Legacy candidate columns

| Column | Legacy type/constraint | API #94 mapping |
|---|---|---|
| id | BIGSERIAL PRIMARY KEY | `notification_id` and `data.id` candidate. |
| user_id | BIGINT NULL REFERENCES users(id) | Existing recipient is preserved; no audience update. |
| sender_id | BIGINT NULL REFERENCES users(id) | Preserved; not set from token. |
| title | VARCHAR(200) NOT NULL | Updated from required body title. |
| content | TEXT NOT NULL | Updated from required body content. |
| type | VARCHAR(30) NULL | Preserved; not mapped to channels. |
| is_read | BOOLEAN DEFAULT FALSE | Preserved; not mapped to read_at/status. |
| created_at | TIMESTAMP NOT NULL | Returned and preserved; never updated. |

## Delivery candidate columns

| Column | Candidate type/constraint | API #94 mapping |
|---|---|---|
| notification_id | BIGINT FK to notifications.id | Filter and lock target delivery rows. |
| channel | VARCHAR(16), PUSH/EMAIL | Return distinct ordered channels; do not update. |
| status | VARCHAR(16), QUEUED/SENT/FAILED | Require all rows QUEUED; return QUEUED. |

## Update mapping

| Logical field | Candidate column | Runtime action | Status |
|---|---|---|---|
| id | notifications.id | SELECT FOR UPDATE and same ID in response | DERIVED candidate mapping. |
| title | notifications.title | UPDATE bound title value | DERIVED body mapping. |
| content | notifications.content | UPDATE bound content value | DERIVED body mapping. |
| channels/status | notification_deliveries | SELECT FOR UPDATE only | DERIVED response/editability projection. |
| recipients, schedule, read state | None | No mutation | Not supported by fallback. |
| created_at | notifications.created_at | Preserve original | No UPDATE assignment. |

No table, column, migration, or index is added. The checked-in legacy DDL is a candidate and does not prove live persistence.

## Physical mapping boundary

- V1-PILOT notifications/deliveries remain a separate UUID learner model and are not used.
- API #94 works at the legacy recipient-row grain; this does not establish campaign-level semantics.
- The body/editability fallback remains DERIVED until the owner approves the contract and Admin model.

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
