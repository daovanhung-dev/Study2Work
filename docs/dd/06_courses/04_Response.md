---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch: `200/422/500` | `N/A` | Protocol status; không phải property JSON |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `N/A` | Uses only contract `DESIGN_*` codes |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw SQL/internal detail |
| 5 | `data` | Course page | `data` | `object` | `No` | `courses/users` | `N/A` | `5.1/5.2` | Map `Page<Course>` | `{}` on error | `ApiEnvelope<Page<Course>>` |
| 5.1 | `data.items` | Course items | `items` | `array` | `No` | `courses/users` | `N/A` | `5.1` | Map each published course | `[]` when empty | `Course[]` |
| 5.1.1 | `data.items[].id` | Course ID | `id` | `int64` | `No` | `courses` | `id` | `4.1` | Direct mapping from BIGSERIAL | `N/A` | |
| 5.1.2 | `data.items[].title` | Course title | `title` | `string` | `No` | `courses` | `name` | `4.1` | Alias `c.name` to contract `title` | `N/A` | ERD physical/logical name discrepancy |
| 5.1.3 | `data.items[].description` | Course description | `description` | `string` | `Yes` | `courses` | `description` | `4.1` | Direct mapping | `null` when source is NULL | Optional contract field |
| 5.1.4 | `data.items[].thumbnail_url` | Thumbnail URL | `thumbnail_url` | `uri` | `Yes` | `courses` | `thumbnail_url` | `4.1` | Direct mapping | `null` when source is NULL | Optional contract field |
| 5.1.5 | `data.items[].price` | Course price | `price` | `decimal-string` | `No` | `courses` | `price` | `4.1` | Serialize NUMERIC(12,2) as decimal string | `N/A` | No floating-point JSON number |
| 5.1.6 | `data.items[].status` | Course status | `status` | `CourseStatus` | `No` | `courses` | `status` | `4.1` | Direct mapping; query restricts to `PUBLISHED` | `N/A` | Enum values not fully catalogued |
| 5.1.7 | `data.items[].mentor` | Mentor summary | `mentor` | `object` | `No` | `users` | `N/A` | `4.2` | Build `UserSummary` from joined user | `N/A` | Required contract object |
| 5.1.7.1 | `data.items[].mentor.id` | Mentor ID | `id` | `int64` | `No` | `users` | `id` | `4.2` | Direct mapping | `N/A` | |
| 5.1.7.2 | `data.items[].mentor.full_name` | Mentor full name | `full_name` | `string` | `No` | `users` | `full_name` | `4.2` | Direct mapping | `N/A` | |
| 5.1.7.3 | `data.items[].mentor.avatar_url` | Mentor avatar URL | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `4.2` | Direct mapping | `null` when source is NULL | Optional contract field |
| 5.1.8 | `data.items[].category` | Course category | `category` | `Category` | `Yes` | `N/A — relation TBD` | `N/A` | `5.1` | Omit until category–course source is confirmed | Omit | Optional contract field; no fabricated object |
| 5.2 | `data.pagination` | Pagination metadata | `pagination` | `object` | `No` | `N/A` | `N/A` | `5.2` | Map `PageMeta` | `{}` on error | |
| 5.2.1 | `data.pagination.page` | Page number | `page` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Effective query page | `TBD` when query default absent | Default not contract-confirmed |
| 5.2.2 | `data.pagination.size` | Page size | `size` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Effective query size | `TBD` when query default absent | Default not contract-confirmed |
| 5.2.3 | `data.pagination.total` | Total matching courses | `total` | `int64` | `No` | `courses` | `COUNT(*)` | `4.3` | Count with same published/filter conditions | `0` when empty | |
| 5.2.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Derived from total and effective size | `TBD` for empty/default-size convention | Contract does not define convention |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | No extra metadata contract |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Request correlation/generator | `TBD — exact generator chưa đặc tả` | `ApiEnvelope` field |

> Error response dùng cùng các field `success`, `businessCode`, `message`, `data`, `meta`, `traceId` của `ApiEnvelope`; không tạo `error_code` hoặc `error_message_id` riêng.
>
> `HTTPStatus` trong bảng là protocol status, không phải property JSON.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Courses retrieved",
  "data": {
    "items": [
      {
        "id": 101,
        "title": "Introduction to Programming",
        "description": "Fundamentals of programming",
        "thumbnail_url": "https://cdn.example.test/courses/101.png",
        "price": "0.00",
        "status": "PUBLISHED",
        "mentor": {
          "id": 7,
          "full_name": "Nguyen Van Mentor",
          "avatar_url": null
        }
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
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

## Ví dụ empty result — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "No published courses",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 0,
      "total_pages": 0
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

> `page=1`, `size=20` và `total_pages=0` trong examples là giá trị minh họa; default/range và empty-page convention vẫn cần xác nhận trong contract.

## Ví dụ lỗi validation — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Invalid pagination or filter query",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

## Ví dụ lỗi hệ thống — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Courses could not be retrieved",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000004"
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
