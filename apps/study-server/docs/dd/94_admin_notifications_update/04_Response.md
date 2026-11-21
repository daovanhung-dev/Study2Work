---
title: "Response"
order: 4
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

Direct success response là `ApiEnvelope<Notification>` HTTP 200 với `DESIGN_RESOURCE_UPDATED`. Runtime tái dùng `AdminNotificationResponse` của API #92. Optional `read_at`/`scheduled_at` bị omit vì candidate schema không cung cấp chúng.

## HTTP success

| HTTP status | Business code | Data type | Source/status |
|---:|---|---|---|
| 200 | DESIGN_RESOURCE_UPDATED | Notification | Direct catalog contract |

## Response fields

| Field | Runtime mapping | Status |
|---|---|---|
| success | true | Shared envelope convention. |
| businessCode | `DESIGN_RESOURCE_UPDATED` | DIRECT. |
| message | `Notification updated.` | Runtime text; wording not specified by catalog. |
| data.id | Locked `notifications.id` | BIGINT candidate; live source unverified. |
| data.title/content | Values returned by UPDATE | DERIVED input mapping to legacy columns. |
| data.channels[] | Distinct channel values from locked delivery rows, ordered by channel | DERIVED projection from candidate outbox. |
| data.status | `QUEUED` only when all delivery rows are QUEUED | Delivery aggregate fallback; not Notification Draft/Scheduled state. |
| data.read_at | Omitted | No compatible legacy timestamp; no read mutation. |
| data.scheduled_at | Omitted | No schedule column or scheduler. |
| data.created_at | Original value returned by UPDATE and checked against locked row | Preserved by SQL; legacy candidate. |
| meta | Empty object | Shared success helper convention. |
| traceId | Request trace context | Shared Study convention. |

The response contains no recipients, sender ID, Operation ID, updated_at, or provider/queue details.

## Success example — runtime fallback shape

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Notification updated.",
  "data": {
    "id": 901,
    "title": "Lịch học đã cập nhật",
    "content": "Thời gian học đã được điều chỉnh.",
    "channels": ["EMAIL", "PUSH"],
    "status": "QUEUED",
    "created_at": "2026-10-20T03:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000094"
}
~~~

## Response discrepancy

- Catalog keeps singular `Notification`; runtime returns one recipient-level legacy row.
- `channels` and `status` come from the existing delivery outbox; only QUEUED rows are eligible.
- `QUEUED` is not asserted to mean Draft/Scheduled Notification.
- #93 Operation tracking and ID bridge remain unresolved; #94 adds no Operation fields.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
