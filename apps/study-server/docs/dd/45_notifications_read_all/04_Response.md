---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "04 Response"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| Success HTTP status | 200 |
| Success business code | `DESIGN_RESOURCE_UPDATED` |
| Success data type | `ApiEnvelope<Page<Notification>>` theo API catalog. |
| Error contract | Chỉ các lỗi 401/403/422/500 theo API catalog. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 4 | `true` khi thành công | N/A | Shared envelope. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | API catalog | N/A | 4 | `DESIGN_RESOURCE_UPDATED` | N/A | Catalog HTTP 200. |
| 3 | `message` | Message | `message` | string | No | N/A | N/A | 4 | Safe client message | Literal chưa được khóa | Không chứa chi tiết nội bộ. |
| 4 | `data` | Data | `data` | `Page<Notification>` | No | `notifications` candidate | N/A | 3 | Page các row vừa đổi | Empty Page khi không có row — DERIVED | Page semantics chưa được catalog định nghĩa. |
| 5 | `data.items[]` | Notification vừa đánh dấu | `items` | `Notification[]` | No | `notifications` candidate | `UPDATE ... RETURNING` rows | 3 | Tất cả row vừa chuyển unread→read | `[]` khi không có row — DERIVED | Không phải full list notification của Student. |
| 6 | `data.items[].id` | Notification ID | `id` | int64 | No | `notifications` legacy candidate | `id` | 3 | Map trực tiếp | Required | BIGSERIAL ở legacy DDL; UUID ở V1-PILOT DDL. |
| 7 | `data.items[].title` | Tiêu đề | `title` | string | No | `notifications` legacy candidate | `title` | 3 | Map trực tiếp | Required | Legacy DDL có `VARCHAR(200)`; pilot DDL cũng có title nhưng identity model khác. |
| 8 | `data.items[].content` | Nội dung | `content` | string | No | `notifications` legacy candidate | `content` | 3 | Map trực tiếp | Required | Legacy DDL `TEXT`; pilot DDL dùng `body`, không tự đổi tên. |
| 9 | `data.items[].channels` | Kênh gửi | `channels` | `NotificationChannel[]` | No | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không map từ `type` hoặc join pilot delivery nếu chưa chọn schema | Field bắt buộc theo Notification schema | Enum/source chưa thống nhất. |
| 10 | `data.items[].status` | Trạng thái notification | `status` | `NotificationStatus` | No | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không suy từ `is_read` hoặc delivery status | Field bắt buộc theo Notification schema | Enum semantics chưa thống nhất. |
| 11 | `data.items[].read_at` | Thời điểm đọc | `read_at` | date-time? | Có — optional theo schema | AC-20 logical recipient / pilot DDL alternative | Chưa có nguồn tương thích với API ID/principal | SOURCE_REQUIRED | Không dựng timestamp từ boolean | Null/omit rule cần xác nhận | Diagram yêu cầu recipient timestamp. |
| 12 | `data.items[].scheduled_at` | Thời điểm dự kiến gửi | `scheduled_at` | date-time? | Có — optional theo schema | N/A | N/A | SOURCE_REQUIRED | Không có cột trong hai DDL đã kiểm tra | Null/omit rule cần xác nhận | Không lấy từ `created_at`. |
| 13 | `data.items[].created_at` | Thời điểm tạo | `created_at` | date-time | No | `notifications` legacy candidate | `created_at` | 3 | Serialize ISO-8601 sau khi timezone được xác nhận | Required | Legacy DDL là `TIMESTAMP` không timezone. |
| 14 | `data.pagination` | Pagination metadata | `pagination` | `PageMeta` | No | Returned row set | N/A | 3 | Derived one-page representation | Required | Không có query/page input. |
| 15 | `data.pagination.page` | Trang hiện tại | `page` | int32 | No | DERIVED | N/A | 3 | Fixed `1` | Required | Một response page. |
| 16 | `data.pagination.size` | Kích thước trang | `size` | int32 | No | M1 returned count | `updated_count` | 3 | Số row trả về; `0` khi empty | DERIVED | Có thể không phù hợp nếu PageMeta định nghĩa size cố định. |
| 17 | `data.pagination.total` | Tổng số item | `total` | int64 | No | M1 returned count | `updated_count` | 3 | Số row transitioned | DERIVED | `UPDATE RETURNING` row count. |
| 18 | `data.pagination.total_pages` | Tổng số trang | `total_pages` | int32 | No | Calculated | `updated_count` | 3 | `0` khi rỗng, `1` khi có item | DERIVED | Tất cả row được trả trong một page không giới hạn. |
| 19 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 4 | `{}` khi không có metadata riêng | N/A | Shared envelope. |
| 20 | `traceId` | Trace ID | `traceId` | uuid | No | Request trace | N/A | Current trace convention | UUID string | N/A | API #45 chưa wired. |

## Ví dụ thành công — có row unread

> Ví dụ JSON hợp lệ về cú pháp. `SOURCE_REQUIRED_*` là marker tài liệu, không phải giá trị enum đã xác nhận; response chưa thể map đầy đủ từ schema hiện có.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Đã đánh dấu thông báo là đã đọc.",
  "data": {
    "items": [
      {
        "id": 1001,
        "title": "Thông báo mẫu",
        "content": "Nội dung thông báo mẫu.",
        "channels": [
          "SOURCE_REQUIRED_CHANNEL"
        ],
        "status": "SOURCE_REQUIRED_STATUS",
        "created_at": "2026-10-23T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 1,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000045"
}
~~~

## Ví dụ thành công — không có unread row

> Empty result là no-op thành công theo đề xuất `DERIVED`, không phải 404.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Không có thông báo chưa đọc.",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 0,
      "total": 0,
      "total_pages": 0
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000045"
}
~~~

## Ví dụ lỗi

> Shape theo API guidelines. Current helper có discrepancy: khi data không truyền, `error_response()` trả `{}`; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Request body must be an empty JSON object.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000045"
}
~~~

## Response gap

- `channels` và `status` bắt buộc trong `Notification` chưa có một physical source thống nhất.
- `read_at` có trong AC-20 và V1-PILOT DDL nhưng không có trong legacy schema; V1-PILOT `learner_id`/ID là UUID, chưa map được với catalog/current JWT numeric IDs.
- `scheduled_at` không có physical source trong các DDL đã kiểm tra.
- `created_at` của legacy schema không xác định timezone.
- `Page` của mutation không có semantics trong catalog; proposal trả mọi row vừa đổi trong một page, không giới hạn kích thước.
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
