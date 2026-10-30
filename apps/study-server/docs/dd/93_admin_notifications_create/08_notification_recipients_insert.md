---
title: "Recipient association insert mapping"
order: 8
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "additional logical mutation mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Recipient association — logical INSERT mapping

## Mapping metadata

| Property | Value |
|---|---|
| Physical table | `notifications` — checked-in legacy candidate |
| Logical entity | Notification-to-recipient association represented by one row per recipient |
| Operation | Local INSERT fallback; not an approved campaign schema |
| Data Mapping step | [Step 2](./05_Data_Mapping.md#step-2-resolve-audience) and [Step 3](./05_Data_Mapping.md#step-3-create-notification-and-delivery-rows) |

## Recipient mapping

| No | Logical value | Source | Physical column | Type/constraint | Status |
|---:|---|---|---|---|---|
| 1 | Notification reference | Generated notification row | `notifications.id` | BIGSERIAL / int64 | Candidate DDL; returned ID |
| 2 | Recipient reference | One ID from explicit `recipients[]` | `notifications.user_id` | Nullable BIGINT FK to `users.id` | Runtime inserts one row for each supplied user |
| 3 | Batch reference | App-generated UUID shared by batch | `notifications.operation_id` | Nullable UUID | Migration 009 candidate; no Operation store bridge |

## Resolution behavior

- The runtime rejects missing, empty, duplicate, non-positive, out-of-range, or unknown recipient IDs with catalog 422.
- A recipient existence query reads only `users.id`; it does not enforce learner role, account status, course membership, or segment rules.
- Each `notifications.user_id` row also stores the shared title/content/sender values. There is no separate `notification_recipients` physical table in this fallback.
- Insert order follows the request order. All recipient rows and their delivery rows share one transaction.

## Candidate evidence and limits

- Legacy `notifications.user_id` stores a recipient on a notification row; it does not represent a campaign with a separate recipient table.
- AC-36 requires Notification + recipients but names no physical table, keys, uniqueness, or partial-write behavior.
- V1-PILOT UUID learner notifications are not the Admin campaign relation.
- This mapping documents current DERIVED local behavior only. Owner confirmation and live schema verification remain open.
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
