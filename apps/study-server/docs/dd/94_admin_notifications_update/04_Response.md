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

Direct success response is ApiEnvelope<Notification> with HTTP 200 and business code DESIGN_RESOURCE_UPDATED. The catalog defines the logical schema, but no approved Admin persistence model can supply all fields.

## HTTP success

| HTTP status | Business code | Data type | Source/status |
|---:|---|---|---|
| 200 | DESIGN_RESOURCE_UPDATED | Notification | Direct catalog contract |

## Response fields

| No | Field | Type | Required | Source/transform | Status |
|---:|---|---|---:|---|---|
| 1 | success | boolean | Yes | Shared envelope; true on successful update | Envelope convention |
| 2 | businessCode | string | Yes | DESIGN_RESOURCE_UPDATED | DIRECT |
| 3 | message | string | Yes | Human-readable success message; exact text unspecified | SOURCE_REQUIRED |
| 4 | data.id | int64 | Yes | Notification identity from target resource | DIRECT type; physical source unresolved |
| 5 | data.title | string | Yes | Updated title if body proposal is approved | Logical field DIRECT; input/persistence mapping DERIVED/SOURCE_REQUIRED |
| 6 | data.content | string | Yes | Updated content if body proposal is approved | Logical field DIRECT; input/persistence mapping DERIVED/SOURCE_REQUIRED |
| 7 | data.channels[] | NotificationChannel[] | Yes | Updated channels if body proposal is approved | Enum and storage projection SOURCE_REQUIRED |
| 8 | data.status | NotificationStatus | Yes | Status of updated notification | Enum and transition SOURCE_REQUIRED |
| 9 | data.read_at | date-time | Optional | Existing read timestamp; this API does not propose changing read state | Physical source/omit-vs-null SOURCE_REQUIRED |
| 10 | data.scheduled_at | date-time | Optional | Proposed schedule value if body is approved | DERIVED input; physical source and null rule SOURCE_REQUIRED |
| 11 | data.created_at | date-time | Yes | Original creation timestamp; update must not replace it | Physical source/precision SOURCE_REQUIRED |
| 12 | traceId | string | Convention | Request trace context | Shared convention; #94 route absent |
| 13 | meta | object | Convention | Envelope metadata follows API Guidelines | Exact schema SOURCE_REQUIRED |

Do not add updated_at, recipient lists or Operation fields to the direct Notification response; they are not in the reviewed reusable schema.

## Structural success example — logical shape

This example illustrates only the catalog envelope and Notification fields. The status/channel strings are placeholders, not approved enum values.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Notification updated.",
  "data": {
    "id": 901,
    "title": "Lịch học đã cập nhật",
    "content": "Thời gian học đã được điều chỉnh.",
    "channels": ["<approved-NotificationChannel>"],
    "status": "<approved-NotificationStatus>",
    "scheduled_at": "2026-10-25T09:00:00+07:00",
    "created_at": "2026-10-20T03:00:00Z"
  },
  "meta": {
    "traceId": "00000000-0000-0000-0000-000000000094"
  }
}
~~~

## Response discrepancy

- Catalog says ApiEnvelope<Notification>; preserve this exact cardinality and shape.
- No approved Admin campaign table maps all Notification fields. Legacy is_read is not read_at or status; legacy type is not proven to be channels.
- NotificationStatus and NotificationChannel tokens remain undefined in reviewed sources.
- API #93 Operation tracking prose conflicts with its Notification response and IDs. #94 does not invent an Operation field or ID bridge.

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
