---
title: "Định nghĩa table"
order: 7
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---


# Định nghĩa table — API read-only

## Thông tin mapping

| Thuộc tính | Giá trị |
|---|---|
| API | #64 `GET /api/v1/mentor/notifications/{notification_id}/status` |
| Loại thao tác | `N/A — READ-ONLY API` |
| Mutation | Không có INSERT/UPDATE/DELETE. |
| Bảng đọc | Local #63 legacy `notifications` và `notification_deliveries`. |
| Source status | `DB.sql` + migration 009 là checked-in artifacts; live deployment chưa xác minh. |

## Read mapping

| Table | Column | Purpose | Query use / response mapping | Status |
|---|---|---|---|---|
| `notifications` | `id` | Notification identity | Match path `notification_id:int64`. | Legacy BIGINT DDL. |
| `notifications` | `operation_id` | Group to accepted dispatch | `Operation.id`; NULL means no dispatch status resource. | Added locally by migration 009. |
| `notifications` | `sender_id` | Sending Mentor identity | Compare with numeric JWT `sub`; map to `Operation.owner_id`. | Existing legacy column; ownership use DERIVED from API #63 binding. |
| `notifications` | `created_at` | Accepted notification time | Map to `Operation.submitted_at`. | Existing legacy column. |
| `notification_deliveries` | `notification_id` | Delivery link | LEFT JOIN to the notification row. | Added locally by migration 009. |
| `notification_deliveries` | `status` | Per-channel state | Aggregate `QUEUED`/`SENT`/`FAILED` to Operation.status. | Local constraint; aggregation DERIVED. |
| `notification_deliveries` | `updated_at` | Last channel state timestamp | `MAX(updated_at)` → `Operation.updated_at`. | Added locally by migration 009. |

## Quy tắc

- API #64 does not mutate either table; this read-only prototype has no insert/update/delete columns.
- Do not read `notifications.is_read` as a delivery state.
- Do not join V1-PILOT UUID notification/delivery relations to legacy BIGINT keys.
- The query's per-channel counts are internal to status aggregation; the direct Operation response does not expose `NotificationDelivery` counts.
- See [Data Mapping](./05_Data_Mapping.md#step-3-read-delivery) and [Open Questions](./OPEN_QUESTIONS.md).


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
