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
| 1 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 2 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `N/A` | Uses `DESIGN_*` contract code |
| 3 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw SQL/internal detail |
| 4 | `data` | Course page | `data` | `object` | `No` | `courses/users` | `N/A` | `5.1/5.2` | Map `Page<Course>` | `{}` on error | `ApiEnvelope<Page<Course>>` |
| 4.1 | `data.items` | Course items | `items` | `array` | `No` | `courses/users` | `N/A` | `5.1` | Map each published course | `[]` when empty | `Course[]` |
| 4.1.1 | `data.items[].id` | Course ID | `id` | `int64` | `No` | `courses` | `id` | `3.1` | Direct mapping from BIGSERIAL | `N/A` | |
| 4.1.2 | `data.items[].title` | Course title | `title` | `string` | `No` | `courses` | `name` | `3.1` | Alias `c.name` to contract `title` | `N/A` | Physical/logical name discrepancy |
| 4.1.3 | `data.items[].description` | Course description | `description` | `string` | `Yes` | `courses` | `description` | `3.1` | Direct mapping | `null` when source is NULL | Optional contract field |
| 4.1.4 | `data.items[].thumbnail_url` | Thumbnail URL | `thumbnail_url` | `uri` | `Yes` | `courses` | `thumbnail_url` | `3.1` | Direct mapping | `null` when source is NULL | Optional contract field |
| 4.1.5 | `data.items[].price` | Course price | `price` | `decimal-string` | `No` | `courses` | `price` | `3.1` | Serialize NUMERIC as decimal string | `N/A` | No floating-point JSON number |
| 4.1.6 | `data.items[].status` | Course status | `status` | `CourseStatus` | `No` | `courses` | `status` | `3.1` | Direct mapping; query restricts to `PUBLISHED` | `N/A` | Full enum catalog TBD |
| 4.1.7 | `data.items[].mentor` | Mentor summary | `mentor` | `object` | `No` | `users` | `N/A` | `3.2` | Build `UserSummary` from joined user | `N/A` | Required contract object |
| 4.1.7.1 | `data.items[].mentor.id` | Mentor ID | `id` | `int64` | `No` | `users` | `id` | `3.2` | Direct mapping | `N/A` | |
| 4.1.7.2 | `data.items[].mentor.full_name` | Mentor full name | `full_name` | `string` | `No` | `users` | `full_name` | `3.2` | Direct mapping | `N/A` | |
| 4.1.7.3 | `data.items[].mentor.avatar_url` | Mentor avatar URL | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `3.2` | Direct mapping | `null` when source is NULL | Optional contract field |
| 4.1.8 | `data.items[].category` | Course category | `category` | `Category` | `Yes` | `N/A — relation TBD` | `N/A` | `5.1` | Omit until category–course relation is confirmed | Omit | Optional contract field; no fabricated object |
| 4.2 | `data.pagination` | Pagination metadata | `pagination` | `object` | `No` | `N/A` | `N/A` | `5.2` | Map `PageMeta` | `{}` on error | |
| 4.2.1 | `data.pagination.page` | Page number | `page` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Effective query page | `1` when omitted | Default design-only |
| 4.2.2 | `data.pagination.size` | Page size | `size` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Fixed design-only default | `20` | API #7 has no `size` query |
| 4.2.3 | `data.pagination.total` | Total matching courses | `total` | `int64` | `No` | `courses` | `COUNT(*)` | `3.3` | Count with same published/search/filter conditions | `0` when empty | |
| 4.2.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | `No` | `N/A` | `N/A` | `5.2` | `ceil(total / 20)` | `0` when total is `0` | Derived from design-only size |
| 5 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | No extra metadata contract |
| 6 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Request correlation/generator | `TBD — exact generator chưa đặc tả` | `ApiEnvelope` field |

> `HTTPStatus` là protocol status và không phải property JSON của `ApiEnvelope`.
>
> Error response dùng `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; không tạo `error_code` hoặc `error_message_id` riêng.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Courses search completed",
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
  "message": "No published courses matched the search",
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

## Ví dụ lỗi validation — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Invalid search query",
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
  "message": "Internal error",
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
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 10 | `B10` | Code ký tự |  |
| 11 | `B11` | Content-Type |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 19 | `B19` | Trường hợp thành công |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 26 | `B26` | Ví dụ |  |

</details>
