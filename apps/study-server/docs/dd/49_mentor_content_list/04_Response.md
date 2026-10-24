---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success contract | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>`. |
| Error contract | HTTP 401/403/404/500; chỉ dùng các code trong API catalog. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 4 | 200 on success | N/A | Error statuses: 401, 403, 404, 500. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4 | true on success; false on error | Required | ApiEnvelope convention. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | literal | 4 | `DESIGN_RESOURCE_RETRIEVED` on success | Required | DIRECT. |
| 4 | message | Message | message | string | No | Application | N/A | 4 | Safe localized text | Exact text unspecified | Do not expose SQL/schema errors. |
| 5 | data | Content | data | object | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | One Content object per catalog | Required | Tree cardinality/nesting unresolved. |
| 5.1 | data.id | Content ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved mapping | Required | No generic Content table in legacy ERD. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved row/path mapping | Required | `course_id` path scopes the request; response mapping needs confirmation. |
| 5.3 | data.content_type | Content type | content_type | ContentType | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No enum mapping | Required | Type members/scalar encoding undefined. |
| 5.4 | data.title | Title | title | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved generic Content source | Required | Chapter/lesson titles in pilot are not automatic Content mapping. |
| 5.5 | data.payload | Payload | payload | object | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No keys or transformation defined | Required object | `{}` in example is a shape placeholder, not default. |
| 5.6 | data.status | Content status | status | ContentStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No enum mapping | Required | ContentStatus values and visibility policy undefined. |
| 5.7 | data.parent_id | Parent ID | parent_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | Optional field per reusable schema | Omit/null rule unresolved | No generic parent-content relation. |
| 5.8 | data.order | Order | order | int32 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved mapping | Required | Order direction/tie-breaker undefined. |
| 6 | meta | Metadata | meta | object | No | Envelope | N/A | 4 | No pagination fields defined | Empty/object policy needs confirmation | Catalog ApiEnvelope. |
| 7 | traceId | Trace ID | traceId | uuid | No | Request trace | trace ID | 4 | Propagate request trace | Required | Runtime route absent. |

## Ví dụ thành công

Đây là ví dụ shape, không phải response có thể dùng để kiểm thử: enum và payload chưa được định nghĩa; giá trị `SOURCE_REQUIRED` chỉ là placeholder.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Nội dung course đã được đọc.",
  "data": {
    "id": 1001,
    "course_id": 501,
    "content_type": "SOURCE_REQUIRED",
    "title": "SOURCE_REQUIRED",
    "payload": {},
    "status": "SOURCE_REQUIRED",
    "order": 1
  },
  "meta": {},
  "traceId": "7b9c43d2-03d1-4f69-baf7-09bc6c1f8741"
}
```

`parent_id` là optional và bị lược trong ví dụ; quy tắc null/omit chưa xác nhận. `payload: {}` chỉ giữ đúng type object, không phải mặc định rỗng. `ContentType`/`ContentStatus` placeholder không đại diện enum hợp lệ.

## Ví dụ lỗi

Ví dụ theo envelope design. Current Study helper được context ghi nhận mặc định `data: {}` khi không truyền `data`, vì vậy error body cần được xác nhận khi API được nối vào runtime.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy tài nguyên.",
  "data": null,
  "meta": {},
  "traceId": "7b9c43d2-03d1-4f69-baf7-09bc6c1f8741"
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
