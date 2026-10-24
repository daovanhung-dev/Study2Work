---
title: "Response"
order: 4
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |

## HTTP success

| HTTP status | Business code | Direct response type | Source |
|---:|---|---|---|
| 202 | `DESIGN_OPERATION_ACCEPTED` | `ApiEnvelope<Notification>` | Catalog #93 and AC-36 node |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table/column | Step | Mapping/null rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|
| 1 | `success` | Success | `success` | boolean | No | Envelope | Step 5 | Envelope convention | Helper not wired |
| 2 | `businessCode` | Code | `businessCode` | string | No | Catalog | Step 5 | Fixed | `DESIGN_OPERATION_ACCEPTED` |
| 3 | `message` | Message | `message` | string | Unspecified | Application | Step 5 | Exact text unspecified | SOURCE_REQUIRED |
| 4 | `data` | Notification | `data` | object | No | No approved target | Step 5 | Direct catalog shape | Conflicts with Operation summary |
| 5 | `data.id` | ID | `id` | int64 | No | No approved target | Step 5 | Allocator unknown | SOURCE_REQUIRED |
| 6 | `data.title` | Title | `title` | string | No | Request/Notification | Steps 3,5 | Logical copy | Physical projection unknown |
| 7 | `data.content` | Content | `content` | string | No | Request/Notification | Steps 3,5 | Logical copy | Physical projection unknown |
| 8 | `data.channels[]` | Channel | `channels[]` | NotificationChannel | No | No approved target | Steps 4,5 | Enum/storage unknown | SOURCE_REQUIRED |
| 9 | `data.status` | Status | `status` | NotificationStatus | No | No approved target | Step 5 | Initial value unknown | SOURCE_REQUIRED |
| 10 | `data.read_at` | Read time | `read_at` | date-time | Optional | No approved Admin target | Step 5 | Omit/null unknown | Optional schema field |
| 11 | `data.scheduled_at` | Scheduled time | `scheduled_at` | date-time | Optional | No request/target | Step 5 | Omit/null unknown | Optional schema field |
| 12 | `data.created_at` | Created time | `created_at` | date-time | No | No approved target | Step 5 | Clock/timezone unknown | SOURCE_REQUIRED |
| 13 | `meta` | Metadata | `meta` | object | Unspecified | Envelope convention | Step 5 | Shape unspecified | No operation metadata added |
| 14 | `traceId` | Trace ID | `traceId` | string | Unspecified | Request context | Steps 0,5 | Propagate by convention | Route absent |

## Structural success example

Angle-bracket values are explanatory placeholders, not accepted literal values.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "<message unspecified>",
  "data": {
    "id": 123,
    "title": "Thông báo minh họa",
    "content": "Nội dung minh họa",
    "channels": ["<NotificationChannel: token chưa xác nhận>"],
    "status": "<NotificationStatus: giá trị chưa xác nhận>",
    "created_at": "<ISO-8601 date-time>"
  },
  "meta": {},
  "traceId": "<trace identifier>"
}
~~~

## Response discrepancy

- Catalog row and diagram say ApiEnvelope<Notification> with int64 Notification ID.
- Operation tracking summary says data: Operation with UUID Operation ID.
- The operation-status node is separate and has no edge from create.
- Do not infer an ID bridge. See [Q-93-01](./OPEN_QUESTIONS.md#q-93-01-notification-or-operation-response).
---
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
