---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "44"
api_name: "Đánh dấu một thông báo đã đọc"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | UTF-8 |
| `Content-Type` | application/json |
| Success `HTTP` `status` | 200 |
| Success business code | `DESIGN_RESOURCE_UPDATED` |
| Success `data` type | `ApiEnvelope<Page<Notification>>` theo API catalog. |
| Error contract | Chỉ các lỗi 401/403/404/422/500 tại API catalog. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 5 | true khi thành công | N/A | API envelope. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 5 | `DESIGN_RESOURCE_UPDATED` | N/A | Catalog `HTTP` 200. |
| 3 | `message` | Message | `message` | string | No | N/A | N/A | 5 | Thông báo an toàn | Literal chưa được catalog khóa | Không chứa chi tiết nội bộ. |
| 4 | `data` | Data | `data` | `Page<Notification>` | No | `notifications` candidate | N/A | 4 | Map một resource vào `Page` | N/A | Hợp đồng chưa thể hoàn chỉnh do required fields thiếu source. |
| 5 | `data`.`items`[] | `Notification` đã cập nhật | `items` | `Notification`[] | No | `notifications` candidate | `UPDATE` `RETURNING` row | 4 | Đúng một item | Không áp dụng khi lỗi | `Page` một item là `DERIVED` theo API #42 precedent. |
| 6 | `data`.`items`[].id | `Notification` ID | id | `int64` | No | `notifications` | id | 3, 4 | Map trực tiếp | Required | PK `BIGSERIAL`; candidate return value. |
| 7 | `data`.`items`[].`title` | Tiêu đề | `title` | string | No | `notifications` | `title` | 3, 4 | Map trực tiếp | Required | `VARCHAR(200)` NOT NULL. |
| 8 | `data`.`items`[].`content` | Nội dung | `content` | string | No | `notifications` | `content` | 3, 4 | Map trực tiếp | Required | TEXT NOT NULL. |
| 9 | `data`.`items`[].`channels` | Kênh gửi | `channels` | `NotificationChannel`[] | No | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không map từ type | Required theo schema | Enum/source table chưa được định nghĩa. |
| 10 | `data`.`items`[].`status` | Trạng thái notification | `status` | `NotificationStatus` | No | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không map từ `is_read` | Required theo schema | Không rõ enum có biểu diễn read state không. |
| 11 | `data`.`items`[].`read_at` | Thời điểm đọc | `read_at` | date-time | Yes — optional | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không suy timestamp từ boolean | Omission/null rule cần xác nhận | Diagram cần update field này; checked-in DDL không có cột. |
| 12 | `data`.`items`[].`scheduled_at` | Thời điểm dự kiến gửi | `scheduled_at` | date-time | Yes — optional | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | N/A | Omission/null rule cần xác nhận | Không có physical column. |
| 13 | `data`.`items`[].`created_at` | Thời điểm tạo | `created_at` | date-time | No | `notifications` | `created_at` | 3, 4 | Serialize ISO-8601 sau khi timezone được xác nhận | Required | DDL `TIMESTAMP` không chỉ định timezone. |
| 14 | `data`.`pagination` | Pagination metadata | `pagination` | `PageMeta` | No | N/A | N/A | 4 | Singleton `Page` proposal | Required | API #44 không nhận `page`. |
| 15 | `data`.`pagination`.`page` | Trang hiện tại | `page` | int32 | No | `DERIVED` | N/A | 4 | Fixed 1 | Required | `Page` singleton. |
| 16 | `data`.`pagination`.`size` | Kích thước trang | `size` | int32 | No | `DERIVED` | N/A | 4 | Fixed 1 | Required | `Page` chứa một notification đã cập nhật. |
| 17 | `data`.`pagination`.`total` | Tổng số item | `total` | `int64` | No | `DERIVED` | N/A | 4 | Fixed 1 | Required | Không phải tổng unread của user. |
| 18 | `data`.`pagination`.`total_pages` | Tổng số trang | `total_pages` | int32 | No | `DERIVED` | N/A | 4 | Fixed 1 | Required | Singleton `Page` proposal. |
| 19 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 5 | {} nếu không có metadata riêng | Required | Shared envelope. |
| 20 | `traceId` | Trace ID | `traceId` | uuid | No | Request trace | N/A | Current trace convention | UUID string | Required | API #44 chưa wired. |

## Ví dụ thành công

> `JSON` hợp lệ về cú pháp. SOURCE_REQUIRED_* là marker tài liệu, không phải enum value đã xác nhận; vì `channels`/`status` bắt buộc và chưa có source, ví dụ chưa chứng minh có thể dựng response hoàn chỉnh. `read_at` và `scheduled_at` được lược vì optional; omission rule cần chốt.

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
  "traceId": "00000000-0000-4000-8000-000000000044"
}
~~~

## Ví dụ lỗi

> Shape theo API guideline; current helper có discrepancy `data`:{}. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Notification not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000044"
}
~~~

## Response gap

- AC-20 yêu cầu `read_at`, nhưng DDL chỉ có `is_read`; không thể trả timestamp nguồn.
- `channels`/`status` bắt buộc trong `Notification` schema nhưng không có physical source/enum; không map type hoặc `is_read`.
- `scheduled_at` không có physical source; null/omit rule cần xác nhận.
- `created_at` có cột nguồn nhưng timezone không được DDL xác định.
- `Page<Notification>` không có semantics mutation trong catalog; `Page` singleton là `DERIVED`.
- API #43 lọc unread theo `is_read` nhưng `Notification` response hiện không expose read state và chưa có `status` mapping; cần chốt để UI đồng bộ sau #44/#45.
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
