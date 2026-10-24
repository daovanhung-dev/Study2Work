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

## Response fields — direct catalog contract

Catalog mô tả `ApiEnvelope<Notification>` (một `Notification` object). Đây là contract phải giữ nguyên trong DD; phần list/page bên dưới chỉ là proposal.

| No | Path | Logical name | Physical name | Type | Nullable | Candidate source | Source step | Transform/null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | Catalog | Branch | 200 success hoặc status trong error catalog | Không thêm status. |
| 2 | `success` | Cờ thành công | `success` | boolean | No | ApiEnvelope | Envelope | true success, false error | Direct schema. |
| 3 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | No | Catalog | Branch | Giữ literal catalog | DIRECT. |
| 4 | `message` | Thông điệp | `message` | string | No | Application | Branch | Nội dung an toàn; exact text chưa chỉ định | DERIVED. |
| 5 | `data` | Notification | `data` | object (`Notification`) | No | Chưa có source hoàn chỉnh | Q1 | Giữ direct object; không tự đổi thành array/Page | DISCREPANCY với list intent. |
| 5.1 | `data.id` | Notification ID | `id` | int64 | No | Legacy `notifications.id` | Q1-L | BIGSERIAL là candidate; campaign identity chưa xác nhận | SOURCE_REQUIRED cho Admin grain. |
| 5.2 | `data.title` | Tiêu đề | `title` | string | No | Legacy/pilot notification `title` | Q1-L/Q1-P | Map candidate theo model tương ứng | Hai model không được gộp. |
| 5.3 | `data.content` | Nội dung | `content` | string | No | Legacy `notifications.content` | Q1-L | Pilot field là `body`; không tự alias khi chưa duyệt | Legacy candidate. |
| 5.4 | `data.channels[]` | Kênh gửi | `channels` | `NotificationChannel[]` | No | Pilot delivery channel, không tương đương notification-level channels | Q1-P | Không map legacy `type`; enum values chưa có | SOURCE_REQUIRED. |
| 5.5 | `data.status` | Trạng thái notification | `status` | `NotificationStatus` | No | Không có nguồn Notification-level được duyệt | Q1 | Không map `is_read` hoặc delivery status | SOURCE_REQUIRED. |
| 5.6 | `data.read_at` | Thời điểm đọc | `read_at` | date-time | Yes | Pilot learner notification | Q1-P | Không có trong legacy; pilot là learner-scoped | Optional theo schema, Admin meaning chưa rõ. |
| 5.7 | `data.scheduled_at` | Thời điểm dự kiến gửi | `scheduled_at` | date-time | Yes | Không thấy trong legacy/pilot DDL đã rà soát | N/A | Không map `expires_at` | SOURCE_REQUIRED. |
| 5.8 | `data.created_at` | Thời điểm tạo | `created_at` | date-time | No | Legacy/pilot notification `created_at` | Q1-L/Q1-P | Candidate; timezone/grain phụ thuộc schema được chọn | Live schema chưa xác minh. |
| 6 | `meta` | Metadata | `meta` | object | No | ApiEnvelope | Envelope | Giữ object; member chưa định nghĩa | Không tự gắn PageMeta vào meta. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Request context | Envelope | Theo trace request | Endpoint chưa được wire. |

## Ví dụ thành công — direct contract

Giá trị enum bên dưới là placeholder minh họa kiểu JSON, không phải enum token được duyệt.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy notification.",
  "data": {
    "id": 1205,
    "title": "Thông báo lịch học",
    "content": "Lịch học mới đã được cập nhật.",
    "channels": ["<NotificationChannel>"],
    "status": "<NotificationStatus>",
    "scheduled_at": "2026-11-01T02:00:00Z",
    "created_at": "2026-10-24T02:00:00Z"
  },
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

> Ví dụ giữ `data` là một object theo catalog; nó không giải quyết ý nghĩa list hoặc pagination.

## Ví dụ thành công — Page proposal `DERIVED`, chưa được duyệt

Chỉ dùng ví dụ này nếu API owner sửa contract sang `ApiEnvelope<Page<Notification>>`. Các token enum vẫn là placeholder giải thích ở trên.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy danh sách notification.",
  "data": {
    "items": [
      {
        "id": 1205,
        "title": "Thông báo lịch học",
        "content": "Lịch học mới đã được cập nhật.",
        "channels": ["<NotificationChannel>"],
        "status": "<NotificationStatus>",
        "created_at": "2026-10-24T02:00:00Z"
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

## Ví dụ lỗi — 503

HTTP 503 và code dưới đây là direct catalog values; điều kiện dependency của API GET #92 chưa được diagram chỉ ra.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "Dịch vụ phụ thuộc hiện không khả dụng.",
  "data": null,
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

> API guideline yêu cầu error `data=null`; current helper serialize `None` thành `{}`. Đây là discrepancy có điều kiện, không phải API #92 runtime behavior.

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
