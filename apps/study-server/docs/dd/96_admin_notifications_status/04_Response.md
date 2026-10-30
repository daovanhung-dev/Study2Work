---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| HTTP success | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Direct contract type | `ApiEnvelope<Notification>` |

## Direct response fields

| No | Path | Logical name | Physical name | Type | Nullable | Candidate source | Transform/null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | Không | Catalog | Cố định 200 ở success | `DESIGN_RESOURCE_RETRIEVED`. |
| 2 | `success` | Success flag | `success` | boolean | Không | ApiEnvelope | `true` ở success | Envelope schema trực tiếp. |
| 3 | `businessCode` | Business code | `businessCode` | string | Không | Catalog | Literal theo success/error branch | Không tự đổi code. |
| 4 | `message` | Message | `message` | string | Không | Application | Nội dung an toàn | Exact text chưa được contract quy định. |
| 5 | `data` | Notification | `data` | object | Không | Reusable `Notification` | Giữ đúng schema dưới đây | Response không phải `NotificationDelivery`. |
| 5.1 | `data.id` | Notification ID | `id` | int64 | Không | Legacy candidate `notifications.id` | Preserve signed-int64 positive key | Local candidate; Admin grain chưa được duyệt. |
| 5.2 | `data.title` | Title | `title` | string | Không | Legacy candidate `notifications.title` | Preserve text | Local #92 response model; Admin mapping `DERIVED`. |
| 5.3 | `data.content` | Content | `content` | string | Không | Legacy candidate `notifications.content` | Preserve text | Local #92 response model; Admin mapping `DERIVED`. |
| 5.4 | `data.channels` | Channels | `channels` | `NotificationChannel[]` | Không | Aggregate `notification_deliveries.channel` | ARRAY_AGG ordered by channel; current candidate allows `EMAIL`/`PUSH` and has unique notification/channel | `DERIVED` from #92; catalog enum members remain unapproved. |
| 5.5 | `data.status` | Notification status | `status` | `NotificationStatus` | Không | Aggregate delivery row statuses | `QUEUED` if any queued; else `FAILED` if any failed; else `SENT` when all rows sent | `DERIVED` from #92; values/precedence need owner approval. |
| 5.6 | `data.read_at` | Read time | `read_at` | date-time? | Tùy chọn | Không có column trong legacy candidate | Omit khi absent; không chuyển `is_read` thành timestamp | Optional field không được suy diễn. |
| 5.7 | `data.scheduled_at` | Scheduled time | `scheduled_at` | date-time? | Tùy chọn | Không có column trong legacy candidate | Omit khi absent | Optional field không được suy diễn. |
| 5.8 | `data.created_at` | Creation time | `created_at` | date-time | Không | Legacy candidate `notifications.created_at` | Serialize ISO-8601 | Local #92 response model; live schema chưa xác minh. |
| 6 | `meta` | Metadata | `meta` | object | Không | ApiEnvelope | Schema không quy định keys cho #96 | Không thêm pagination. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | Không | Request trace context | UUID của request | HTTP tests xác minh trace/envelope local. |

## Aggregate boundary

Reusable `NotificationDelivery` có `notification_id:int64`, `status:OperationStatus`, `queued:int32`, `sent:int32`, `failed:int32`. AC-36 yêu cầu đọc aggregate, nhưng catalog #96 trả `Notification` và không định nghĩa field projection, count semantics, delivery grain hoặc channel breakdown. Local fallback dùng channel/status aggregate của #92 để gán `data.channels` và `data.status`; counts không thuộc response và không được thêm.

## Ví dụ success — placeholders là design-only

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "<SAFE_MESSAGE>",
  "data": {
    "id": 123,
    "title": "<SOURCE_REQUIRED>",
    "content": "<SOURCE_REQUIRED>",
    "channels": ["EMAIL", "PUSH"],
    "status": "QUEUED",
    "created_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000096"
}
```

Ví dụ minh họa các token `DERIVED` của fallback #92; giá trị record chỉ mang tính ví dụ. `scheduled_at` là field optional của schema nhưng không có trong legacy projection nên bị lược bỏ. Delivery counts bị lược bỏ vì không thuộc `Notification` schema.

## Ví dụ lỗi — resource không tìm thấy

`error_response` đặt `data:null`; HTTP test của API #96 xác minh hành vi local này.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "<SAFE_MESSAGE>",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000097"
}
```
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

