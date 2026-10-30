---
title: "Response"
order: 4
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields — direct contract và current fallback

Catalog khai báo `ApiEnvelope<Notification>`; runtime hiện dùng `ApiEnvelope<Page<Notification>>` để đáp ứng list intent/query `page`. Page là `DERIVED` và cần owner/catalog confirmation.

| No | Path | Logical name | Physical name | Type | Nullable | Candidate source | Source step | Transform/null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | Catalog | Branch | 200 success hoặc status trong error catalog | Không thêm status trực tiếp; runtime 422 page là DERIVED. |
| 2 | `success` | Cờ thành công | `success` | boolean | No | ApiEnvelope | Envelope | true success, false error | Direct schema. |
| 3 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | No | Catalog | Branch | Giữ literal catalog | DIRECT. |
| 4 | `message` | Thông điệp | `message` | string | No | Application | Branch | Message an toàn | Runtime message có/không có item. |
| 5 | `data` | Notification page | `data` | object (`Page<Notification>`) | No | API #92 runtime fallback | Q1 | Gồm `items` và `pagination` | DERIVED; khác catalog singleton. |
| 5.1 | `data.items[]` | Notification item | `items[]` | array of object | No | Legacy notifications + delivery outbox | Q1-L | Một item trên mỗi `notifications.id` có delivery | Recipient/campaign grain vẫn cần xác nhận. |
| 5.1.1 | `data.items[].id` | Notification ID | `id` | int64 | No | `notifications.id` | Q1-L | BIGSERIAL candidate | Không trả operation UUID. |
| 5.1.2 | `data.items[].title` | Tiêu đề | `title` | string | No | `notifications.title` | Q1-L | Direct candidate | Legacy candidate. |
| 5.1.3 | `data.items[].content` | Nội dung | `content` | string | No | `notifications.content` | Q1-L | Direct candidate | Legacy candidate. |
| 5.1.4 | `data.items[].channels[]` | Kênh gửi | `channels` | NotificationChannel[] | No | `notification_deliveries.channel` | Q1-L | Aggregate ordered distinct channel rows | `PUSH`/`EMAIL` là local API #63/DDL fallback. |
| 5.1.5 | `data.items[].status` | Trạng thái notification | `status` | NotificationStatus | No | Delivery status aggregate | Q1-L | API #64 precedence QUEUED → FAILED → SENT | Mapping Notification-level status is DERIVED. |
| 5.1.6 | `data.items[].read_at` | Thời điểm đọc | `read_at` | date-time | Yes | N/A | Q1-L | Omit; legacy only has boolean `is_read` | Optional in reusable schema. |
| 5.1.7 | `data.items[].scheduled_at` | Thời điểm lên lịch | `scheduled_at` | date-time | Yes | N/A | Q1-L | Omit; no candidate column | Do not map pilot `expires_at`. |
| 5.1.8 | `data.items[].created_at` | Thời điểm tạo | `created_at` | date-time | No | `notifications.created_at` | Q1-L | Serialize stored timestamp | Timezone semantics follow DB driver; live behavior unverified. |
| 5.2 | `data.pagination.page` | Trang hiện tại | `page` | int32 | No | Validated query | Q1 | Echo requested page | Default 1 DERIVED. |
| 5.3 | `data.pagination.size` | Kích thước trang | `size` | int32 | No | Fixed local constant | Q1 | 20 | DERIVED. |
| 5.4 | `data.pagination.total` | Tổng số notification | `total` | int64 | No | Count query | Q1 | Same exact status/channel predicates as item query | DERIVED. |
| 5.5 | `data.pagination.total_pages` | Tổng số trang | `total_pages` | int32 | No | Count + size | Q1 | ceil(total / 20); 0 when total is 0 | DERIVED. |
| 6 | `meta` | Metadata | `meta` | object | No | ApiEnvelope | Envelope | `{}` | No separate operation metadata. |
| 7 | `traceId` | Trace ID | `traceId` | uuid string | No | Request context | Envelope | Shared trace convention | Direct envelope. |

## Ví dụ thành công

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Notifications retrieved.",
  "data": {
    "items": [
      {
        "id": 501,
        "title": "Thông báo lịch học",
        "content": "Lịch học được cập nhật.",
        "channels": ["EMAIL", "PUSH"],
        "status": "QUEUED",
        "created_at": "2026-10-26T08:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

`read_at` và `scheduled_at` được bỏ qua vì optional và không có nguồn legacy được xác nhận. Danh sách rỗng vẫn trả HTTP 200 với `items: []`.

## Ví dụ lỗi — DB unavailable

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "Notifications are temporarily unavailable.",
  "data": null,
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

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
