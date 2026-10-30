---
title: "Delivery outbox insert mapping"
order: 9
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "additional physical mutation mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Notification delivery outbox — INSERT mapping

## Mapping metadata

| Property | Value |
|---|---|
| Physical table | `notification_deliveries` — checked-in legacy candidate |
| Logical entity | One delivery attempt record per Notification/channel |
| Operation | Local INSERT fallback; no provider dispatch in this endpoint |
| Data Mapping step | [Step 3](./05_Data_Mapping.md#step-3-create-notification-and-delivery-rows) |

## Insert mapping

**Applies when**

- For each created Notification and each requested channel, the transaction inserts one `QUEUED` row into the legacy outbox candidate. DDL is present in `DB.sql` and migration 009; live deployment and worker availability are unverified.

| No | Physical column | Type/constraint | Setting/source | Step | Remarks |
|---:|---|---|---|---|---|
| 1 | `id` | BIGSERIAL PRIMARY KEY | Database generated; `RETURNING id` | 3 | Runtime validates projection; not returned by API |
| 2 | `notification_id` | BIGINT NOT NULL FK to `notifications.id` ON DELETE CASCADE | ID returned for this recipient row | 3 | One delivery row per requested channel |
| 3 | `channel` | VARCHAR(16), CHECK `PUSH`/`EMAIL` | Request `channels[]` | 1, 3 | Values are DERIVED from diagram and candidate DDL |
| 4 | `status` | VARCHAR(16), default/check `QUEUED`/`SENT`/`FAILED` | Literal `QUEUED` | 3 | Delivery state; no worker is invoked here |
| 5 | `queued_at` | TIMESTAMPTZ NOT NULL | `CURRENT_TIMESTAMP` | 3 | DB timestamp |
| 6 | `updated_at` | TIMESTAMPTZ NOT NULL | `CURRENT_TIMESTAMP` | 3 | DB timestamp |
| 7 | `(notification_id, channel)` | UNIQUE | One notification/channel pair | 3 | Candidate DDL constraint; request duplicates rejected earlier |

## Transaction and delivery boundary

- Delivery rows and Notification rows are committed atomically. Any SQL or projection error before commit attempts rollback for the full batch.
- A successful 202 means the local transaction committed with outbox rows. It does not mean a Push/Email provider accepted or delivered a message.
- No provider credentials, send worker, retry policy, or live outbox consumer was verified.
- This is not the separate V1-PILOT UUID learner delivery model and is not approved as the final Admin delivery schema.

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
