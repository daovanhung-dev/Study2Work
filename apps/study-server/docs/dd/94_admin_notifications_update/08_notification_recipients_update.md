---
title: "Recipient association mapping"
order: 8
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "3. Data mapping — supplementary logical mutation"
status: "Draft — Needs Confirmation"
---

# Recipient association — update boundary

## Mapping metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical operation | No recipient association mutation in current API #94 fallback |
| Trigger | Catalog/diagram do not declare recipients or segment in PUT body |
| Candidate target | No approved Admin campaign-recipient table found |
| Runtime behavior | Body accepts only title/content; recipients and segment are rejected as extra fields |
| Status | Physical audience replacement remains SOURCE_REQUIRED |
| Related API | [#93 create notification](../93_admin_notifications_create/08_notification_recipients_insert.md) |

## Preserved association

- The checked-in legacy `notifications.user_id` represents one nullable recipient per row. API #94 addresses that row by `notification_id` and does not change `user_id`.
- Existing `notification_deliveries` rows and their channel/status are locked and preserved.
- V1-PILOT UUID learner relations are not used as an Admin association mapping.
- API #94 adds no insert/delete of recipient rows and does not modify delivery history.

## Future owner decisions

If recipient replacement is required, the owner must select the Admin campaign grain, recipient relation, segment predicate, validation/deduplication rules, delivery-history behavior, and transaction boundary. No physical mutation is specified here.

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
