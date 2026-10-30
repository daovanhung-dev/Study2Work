---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "43"
api_name: "Lấy notification list"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP `status` | 200 |
| Success business code | `DESIGN_RESOURCE_RETRIEVED` |
| Success data `type` | `ApiEnvelope<Page<Notification>>` theo API catalog. |
| Error contract | Chỉ các lỗi 401/403/500 tại API catalog. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 6.1 | true khi thành công | N/A | Envelope theo API guideline. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 6.1 | `DESIGN_RESOURCE_RETRIEVED` | N/A | Code theo API catalog. |
| 3 | message | Message | message | string | No | N/A | N/A | 6.1 | Message an toàn | Nội dung cụ thể chưa được contract khóa | Không trả dữ liệu nội bộ. |
| 4 | data | Data | data | `Page<Notification>` | No | notifications candidate | N/A | 5.1, 5.2 | Map `items` và `PageMeta` | N/A | Response hợp đồng chưa thể map đầy đủ do SOURCE_REQUIRED fields. |
| 5 | data.items[] | Notification item | `items` | Notification[] | No | notifications candidate | N/A | 5.1 | Mỗi item thuộc principal đã xác thực | [] khi không có row phù hợp — DERIVED | Hàng broadcast chưa được xét. |
| 6 | `data.items[].id` | Notification ID | id | int64 | No | notifications | id | 5.1 | Map nguyên giá trị | N/A | `BIGSERIAL` PRIMARY KEY; design-only. |
| 7 | `data.items[].title` | Tiêu đề | `title` | string | No | notifications | `title` | 5.1 | Map nguyên giá trị | Bắt buộc theo DDL | `VARCHAR(200)` NOT NULL; design-only. |
| 8 | `data.items[].content` | Nội dung | `content` | string | No | notifications | `content` | 5.1 | Map nguyên giá trị | Bắt buộc theo DDL | `TEXT` NOT NULL; design-only. |
| 9 | `data.items[].channels` | Kênh gửi | `channels` | `NotificationChannel[]` | No | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không có mapping được xác nhận | Field bắt buộc của schema Notification | DDL chỉ có `type`; không ánh xạ `type` sang `channels`. |
| 10 | `data.items[].status` | Trạng thái notification | `status` | `NotificationStatus` | No | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không có mapping được xác nhận | Field bắt buộc của schema Notification | DDL có `is_read` và `type`, không có `status`; enum chưa được định nghĩa. |
| 11 | `data.items[].read_at` | Thời điểm đọc | `read_at` | date-time | Có — optional theo schema | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không suy ra timestamp từ boolean | Omission/null rule cần xác nhận | DDL chỉ có `is_read`; API #44 diagram nhắc `read_at`. |
| 12 | `data.items[].scheduled_at` | Thời điểm dự kiến gửi | `scheduled_at` | date-time | Có — optional theo schema | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Không có mapping | Omission/null rule cần xác nhận | Không có cột trong DDL. |
| 13 | `data.items[].created_at` | Thời điểm tạo | `created_at` | date-time | No | notifications | `created_at` | 5.1 | Serialize theo ISO-8601 sau khi timezone rule được xác nhận | Bắt buộc theo Notification schema | DDL là `TIMESTAMP` không chỉ định timezone. |
| 14 | data.pagination | Pagination metadata | pagination | `PageMeta` | No | N/A | N/A | 5.2 | Tính từ page query/count query | N/A | Page size 20 là DERIVED. |
| 15 | `data.pagination.page` | Trang hiện tại | page | int32 | No | Query input | page | 3.1, 5.2 | Request page; omitted dùng 1 | Range chưa được contract xác nhận | Không tạo thêm query field. |
| 16 | `data.pagination.size` | Kích thước trang | size | int32 | No | DERIVED | N/A | 5.2 | Cố định 20 | N/A | Không có size input trong API catalog. |
| 17 | `data.pagination.total` | Tổng số bản ghi | `total` | int64 | No | Query result | `COUNT(*)` | 4.2 | Tổng row thỏa cùng owner/unread filters | 0 khi không có row — DERIVED | Query count không áp dụng limit/`offset`. |
| 18 | `data.pagination.total_pages` | Tổng số trang | `total_pages` | int32 | No | Calculated | `total`, size 20 | 5.2 | ceil(`total` / 20); 0 nếu `total` bằng 0 | N/A | Công thức DERIVED. |
| 19 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 6.1 | {} khi không có metadata riêng | N/A | Envelope theo API guideline. |
| 20 | `traceId` | Trace ID | `traceId` | uuid | No | Request trace | N/A | Current trace convention | `UUID` string | N/A | Middleware convention; API #43 chưa wired. |

## Ví dụ thành công

> `JSON` dưới đây hợp lệ về cú pháp. SOURCE_REQUIRED_* là marker tài liệu, không phải giá trị enum hợp lệ; ví dụ không chứng minh có thể dựng response đầy đủ từ DDL. `read_at` và `scheduled_at` được lược khỏi ví dụ nhưng omission rule vẫn cần xác nhận.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã tải danh sách thông báo.",
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
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000043"
}
~~~

## Ví dụ lỗi

> Đây là shape theo API guideline. Current shared error helper có discrepancy về data fallback; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

~~~json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000043"
}
~~~

## Response gap

- Catalog yêu cầu `channels` và `status`, nhưng DB guide/ERD/DDL không có mapping vật lý.
- Catalog khai báo optional `read_at` và `scheduled_at`; DDL không có cột tương ứng.
- Không map notifications.type thành `channels`.
- Không map notifications.is_read thành `status` hoặc tạo `read_at` từ boolean.
- notifications.created_at có kiểu `TIMESTAMP` không timezone; contract cần date-time ISO-8601.
- Vì các field bắt buộc `channels` và `status` chưa có nguồn, physical response chưa thể triển khai chính xác trước khi gap được giải quyết.
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
