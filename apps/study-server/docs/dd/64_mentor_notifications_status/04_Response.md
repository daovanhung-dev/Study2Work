---
title: "Response"
order: 4
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
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
| HTTP success | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Contract type | `ApiEnvelope<Operation>` |

## Các trường response — reusable Operation schema trực tiếp

| Không | Path | Logical name | Physical name | Type | Nullable | Source | Transform / null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | Mã HTTP | `HTTPStatus` | integer | Không | Catalog | Cố định 200 | `DESIGN_RESOURCE_RETRIEVED`. |
| 2 | `success` | Cờ thành công | `success` | boolean | Không | Envelope | `true` khi đọc thành công | Không chứng minh delivery thành công. |
| 3 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | Không | Catalog | Giá trị cố định | `DESIGN_RESOURCE_RETRIEVED`. |
| 4 | `message` | Thông điệp | `message` | string | Không | Ứng dụng | Nội dung an toàn | Câu chữ chưa được quy định. |
| 5 | `data` | Operation | `data` | Operation | Không | Schema dùng chung | Ánh xạ theo schema | Query source và notification→Operation mapping chưa có. |
| 5.1 | `data.id` | Operation ID | `id` | uuid | Không | Operation schema | UUID theo schema | Không đồng nhất với path `notification_id:int64`. |
| 5.2 | `data.kind` | Operation kind | `kind` | OperationKind | Không | Operation schema | Giữ enum trực tiếp | Enum members chưa được định nghĩa. |
| 5.3 | `data.status` | Operation status | `status` | OperationStatus | Không | Operation schema | Trạng thái Operation | Không được suy là delivery status. |
| 5.4 | `data.owner_id` | Operation owner | `owner_id` | int64 | Không | Operation schema | Owner ID | Mapping Mentor principal chưa có. |
| 5.5 | `data.submitted_at` | Thời điểm nhận | `submitted_at` | date-time | Không | Operation schema | ISO-8601 theo convention | Source/precision chưa xác nhận. |
| 5.6 | `data.updated_at` | Thời điểm cập nhật | `updated_at` | date-time | Không | Operation schema | ISO-8601 theo convention | Lifecycle chưa xác nhận. |
| 5.7 | `data.completed_at` | Thời điểm hoàn tất | `completed_at` | date-time? | Tùy chọn | Operation schema | Optional theo schema | Semantics chưa xác nhận. |
| 5.8 | `data.result` | Operation result | `result` | Payment? | Tùy chọn | Operation schema | Giữ đúng schema | Payment không biểu diễn trạng thái gửi notification. |
| 5.8.1 | `data.result.id` | Payment ID | `id` | int64 | Bắt buộc nếu có Payment | Payment schema | Field nested trực tiếp | Không có ý nghĩa delivery. |
| 5.8.2 | `data.result.order_id` | Order ID | `order_id` | int64 | Bắt buộc nếu có Payment | Payment schema | Field nested trực tiếp | Không có ý nghĩa delivery. |
| 5.8.3 | `data.result.provider` | Payment provider | `provider` | PaymentProvider | Bắt buộc nếu có Payment | Payment schema | Enum direct | Không có ý nghĩa delivery. |
| 5.8.4 | `data.result.amount` | Payment amount | `amount` | decimal-string | Bắt buộc nếu có Payment | Payment schema | Serialize decimal thành string | Không có ý nghĩa delivery. |
| 5.8.5 | `data.result.status` | Payment status | `status` | PaymentStatus | Bắt buộc nếu có Payment | Payment schema | Enum direct | Không có ý nghĩa delivery. |
| 5.8.6 | `data.result.transaction_code` | Mã giao dịch | `transaction_code` | string? | Tùy chọn | Payment schema | Optional field | Không có ý nghĩa delivery. |
| 5.8.7 | `data.result.paid_at` | Thời điểm thanh toán | `paid_at` | date-time? | Tùy chọn | Payment schema | ISO-8601 | Không có ý nghĩa delivery. |
| 6 | `meta` | Metadata | `meta` | object | Không | Envelope | `{}` chỉ để minh họa | Field riêng API chưa khai báo. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | Không | Envelope convention | UUID trace của request | Route #64 chưa wired. |

## Khoảng trống so với mục tiêu delivery

- AC-25 yêu cầu UI hiển thị delivery status theo `notification_id`; API row lại trả `Operation`.
- `NotificationDelivery` reusable schema có `notification_id:int64`, `status:OperationStatus`, `queued:int32`, `sent:int32`, `failed:int32`, nhưng không được khai báo là response của #64.
- Không có source để ánh xạ `notification_id:int64` sang `Operation.id:uuid`, hoặc lấy `Operation.result` (đang là `Payment?`).
- Nếu contract đổi sang `NotificationDelivery`, cần xác nhận enum semantics, counts grain và status khi chưa có delivery record trước khi implementation.

## Ví dụ thành công — minh họa cấu trúc Operation

Ví dụ chỉ minh họa schema direct. Enum placeholders không phải giá trị được duyệt; Operation ID không được suy ra từ path notification ID.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "<SAFE_MESSAGE>",
  "data": {
    "id": "00000000-0000-4000-8000-000000000064",
    "kind": "<OperationKind_SOURCE_REQUIRED>",
    "status": "<OperationStatus_SOURCE_REQUIRED>",
    "owner_id": 1001,
    "submitted_at": "2026-10-24T00:00:00Z",
    "updated_at": "2026-10-24T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000065"
}
```

## Ví dụ lỗi — resource không tìm thấy

API Guidelines dùng `data:null`; helper hiện tại mặc định `{}` nếu không truyền data. API #64 chưa wired nên đây chưa phải behavior runtime.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "<SAFE_MESSAGE>",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000066"
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
