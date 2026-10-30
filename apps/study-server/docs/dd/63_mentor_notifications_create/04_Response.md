---
title: "Response"
order: 4
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| HTTP success | 202 `DESIGN_OPERATION_ACCEPTED` |
| Contract type | `ApiEnvelope<Operation>` |

## Các trường response — Operation schema trực tiếp

| Không | Path | Logical name | Physical name | Type | Nullable | Source | Transform / null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | Mã HTTP | `HTTPStatus` | integer | Không | Catalog | Cố định 202 | `DESIGN_OPERATION_ACCEPTED`. |
| 2 | `success` | Cờ thành công | `success` | boolean | Không | Envelope | `true` khi được tiếp nhận | Không đồng nghĩa delivery thành công. |
| 3 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | Không | Catalog | Giá trị cố định | `DESIGN_OPERATION_ACCEPTED`. |
| 4 | `message` | Thông điệp | `message` | string | Không | Ứng dụng | Nội dung an toàn | Câu chữ chưa được quy định. |
| 5 | `data` | Operation | `data` | Operation | Không | Schema dùng chung | Project từ batch notification đã commit | Local projection; không có Operation table riêng. |
| 5.1 | `data.id` | Operation ID | `id` | uuid | Không | Sinh UUID trước khi ghi notification rows | Dùng chung làm `notifications.operation_id`; API #18 path discrepancy vẫn mở. |
| 5.2 | `data.kind` | Operation kind | `kind` | OperationKind | Không | Fallback cố định `NOTIFICATION_DISPATCH` | Giá trị DERIVED; enum catalog chưa khai báo. |
| 5.3 | `data.status` | Operation status | `status` | OperationStatus | Không | `QUEUED` sau commit outbox | Không suy ra provider đã gửi; giá trị DERIVED. |
| 5.4 | `data.owner_id` | Operation owner | `owner_id` | int64 | Không | Numeric Mentor `sub` | Cùng key với legacy `notifications.sender_id`. |
| 5.5 | `data.submitted_at` | Thời điểm nhận | `submitted_at` | date-time | Không | DB `notifications.created_at` | ISO-8601; DB timestamp precision is preserved. |
| 5.6 | `data.updated_at` | Thời điểm cập nhật | `updated_at` | date-time | Không | Bằng `submitted_at` khi mới QUEUED | Future outbox worker may advance delivery timestamps; not implemented here. |
| 5.7 | `data.completed_at` | Thời điểm hoàn tất | `completed_at` | date-time? | Tùy chọn | Operation schema | Bỏ hoặc null theo serializer được duyệt | Thường chưa có tại 202; semantics chưa chốt. |
| 5.8 | `data.result` | Operation result | `result` | Payment? | Tùy chọn | Operation schema | Giữ nguyên schema trực tiếp | `Payment` không phù hợp notification job; không tự thay bằng NotificationDelivery. |
| 5.8.1 | `data.result.id` | Payment ID | `id` | int64 | Bắt buộc nếu có Payment | Payment schema | Field lồng trực tiếp | Không có ý nghĩa cho notification job. |
| 5.8.2 | `data.result.order_id` | Order ID | `order_id` | int64 | Bắt buộc nếu có Payment | Payment schema | Field lồng trực tiếp | Không có ý nghĩa cho notification job. |
| 5.8.3 | `data.result.provider` | Provider thanh toán | `provider` | PaymentProvider | Bắt buộc nếu có Payment | Payment schema | Enum direct | Không có ý nghĩa cho notification job. |
| 5.8.4 | `data.result.amount` | Payment amount | `amount` | decimal-string | Bắt buộc nếu có Payment | Payment schema | Decimal serialize string | Không có ý nghĩa cho notification job. |
| 5.8.5 | `data.result.status` | Payment status | `status` | PaymentStatus | Bắt buộc nếu có Payment | Payment schema | Enum direct | Không có ý nghĩa cho notification job. |
| 5.8.6 | `data.result.transaction_code` | Transaction code | `transaction_code` | string? | Tùy chọn | Payment schema | Optional field | Không có ý nghĩa cho notification job. |
| 5.8.7 | `data.result.paid_at` | Thời điểm thanh toán | `paid_at` | date-time? | Tùy chọn | Payment schema | ISO-8601 | Không có ý nghĩa cho notification job. |
| 6 | `meta` | Metadata | `meta` | object | Không | Envelope | `{ "notification_ids": [int64, ...] }` | DERIVED handoff; one legacy notification ID per recipient for API #64. |
| 6.1 | `meta.notification_ids[]` | Notification ID theo recipient | `notification_ids` | int64[] | Không | `notifications.id` rows vừa commit | Client gọi API #64 một lần cho mỗi ID; preserve request recipient order. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | Không | Quy ước dùng chung | Truyền tiếp trace của request | Endpoint chưa có route. |

## Khoảng trống trong response contract

- Catalog yêu cầu `ApiEnvelope<Operation>`; direct Operation fields giữ nguyên schema dùng chung.
- `Operation.id` là UUID; mỗi Notification ID int64 được công bố trong `meta.notification_ids` để client gọi API #64 riêng cho từng recipient.
- `Operation.result` hiện chỉ là `Payment?`; không thay bằng `NotificationDelivery` nếu catalog chưa đổi.
- `NotificationDelivery` reusable schema có `notification_id`, `status`, `queued`, `sent`, `failed`, nhưng chưa được khai báo làm Operation result hoặc response #64.
- Node API #18 trong AC-25 có UUID operation_id nhưng không nối trên diagram; API #18 row còn khai báo int64.

## Ví dụ thành công — minh họa cấu trúc

HTTP 202 xác nhận Notification và QUEUED outbox rows đã được commit. Enum values bên dưới là fallback DERIVED; `result` được lược vì là optional và schema hiện khai báo Payment, không phải delivery notification.

```json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "<SAFE_ACCEPTED_MESSAGE>",
  "data": {
    "id": "00000000-0000-4000-8000-000000000063",
    "kind": "NOTIFICATION_DISPATCH",
    "status": "QUEUED",
    "owner_id": 1001,
    "submitted_at": "2026-10-24T00:00:00Z",
    "updated_at": "2026-10-24T00:00:00Z"
  },
  "meta": {"notification_ids": [30001, 30002]},
  "traceId": "00000000-0000-4000-8000-000000000064"
}
```

## Ví dụ lỗi — theo API Guidelines

`error_response(...)` hiện dùng cho API #63; khi không truyền `data`, runtime error envelope chứa `data:null`.

```json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "<SAFE_MESSAGE>",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000065"
}
```
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
