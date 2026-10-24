---
title: "Recipient association mapping"
order: 8
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "3. Data mapping — supplementary logical mutation"
status: "Draft — Needs Confirmation"
---

# Recipient association — logical UPDATE mapping

## Mapping metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical operation | Replace notification recipient association |
| Trigger | Request body proposal DERIVED; not present in direct catalog contract |
| Candidate target | No approved Admin campaign-recipient table found |
| Status | Logical mapping only; SOURCE_REQUIRED for persistence |
| Related API | [#93 create notification](../93_admin_notifications_create/08_notification_recipients_insert.md) |

## Logical input mapping

| Logical field | Type | Proposed use | Validation/source status |
|---|---|---|---|
| notification_id | int64 | Identify the existing notification whose audience is changed | Direct path; physical target unresolved |
| recipients | int64[] | Explicit audience candidate | Reused from #93; XOR/empty/duplicate/eligibility rules DERIVED or SOURCE_REQUIRED |
| segment | AudienceSegment | Segment audience candidate | Reused from #93; token set and expansion predicate SOURCE_REQUIRED |
| channels[] | NotificationChannel[] | Delivery channels are part of the proposed request, not a recipient relation key unless approved | Enum/storage mapping SOURCE_REQUIRED |

## Proposed mutation semantics — DERIVED

- Require exactly one audience selector: explicit recipients or segment.
- Treat the selected audience as a full replacement only if the request body proposal is approved.
- Do not infer a physical DELETE followed by INSERT; delivery history and idempotency behavior are unknown.
- Do not modify or delete already-created delivery records without an approved lifecycle policy.
- Use the same transaction as Notification metadata update only if the owner selects a persistence model and defines transaction ownership.

## Candidate evidence

| Source | Evidence | Why it is not a direct mapping |
|---|---|---|
| Legacy notifications | One nullable user_id per row; sender_id may identify sender | Does not establish campaign grain or a separate recipient relation |
| V1-PILOT notification_deliveries | UUID notification ID and delivery-level channel/status | Learner/delivery model differs from Admin BIGINT Notification contract |
| AC-36/#93 | Logical Notification + recipient flow and optional recipients/segment request fields | Does not define a physical relation, audience predicate, replacement semantics or delivery-history behavior |

No physical table, column, SQL statement, new error code or runtime behavior is invented in this mapping.

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
