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
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Fixed by branch: `200/422/500` | `N/A` | Protocol status; không phải property JSON |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | `DESIGN_RESOURCE_RETRIEVED`, `DESIGN_VALIDATION_ERROR` or `DESIGN_INTERNAL_ERROR` | `N/A` | Chỉ dùng code đã có trong contract |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw SQL/internal detail |
| 5 | `data` | Category page | `data` | `object` | `No` | `N/A — schema design-only` | `N/A` | `5.1` | Map `Page<Category>` | `{}` on error | `ApiEnvelope<Page<Category>>` |
| 5.1 | `data.items` | Category items | `items` | `array` | `No` | `N/A — category source TBD` | `N/A` | `4.2/4.3` | Map each active category | `[]` when empty | `Category[]` |
| 5.1.1 | `data.items[].id` | Category ID | `id` | `int64` | `No` | `N/A — category source TBD` | `N/A` | `4.3` | Direct mapping | `N/A` | Contract field |
| 5.1.2 | `data.items[].name` | Category name | `name` | `string` | `No` | `N/A — category source TBD` | `N/A` | `4.3` | Direct mapping/locale-aware source when supported | `N/A` | Contract field |
| 5.1.3 | `data.items[].slug` | Category slug | `slug` | `string` | `No` | `N/A — category source TBD` | `N/A` | `4.3` | Direct mapping | `N/A` | Contract field |
| 5.1.4 | `data.items[].description` | Category description | `description` | `string` | `Yes` | `N/A — category source TBD` | `N/A` | `4.3` | Direct mapping | `TBD — null/omit rule` | Optional contract field |
| 5.2 | `data.pagination` | Pagination metadata | `pagination` | `object` | `No` | `N/A` | `N/A` | `5.1/5.2` | Implicit single-page metadata | `{}` on error | `PageMeta` |
| 5.2.1 | `data.pagination.page` | Page number | `page` | `int32` | `No` | `N/A` | `N/A` | `5.1` | Fixed `1` | `N/A` | Single-page convention |
| 5.2.2 | `data.pagination.size` | Page size | `size` | `int32` | `No` | `N/A` | `N/A` | `5.1` | `total` item count | `0` when empty | Single-page convention |
| 5.2.3 | `data.pagination.total` | Total count | `total` | `int64` | `No` | `N/A` | `N/A` | `4.3` | Count of returned active categories | `0` when empty | Single-page convention |
| 5.2.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | `No` | `N/A` | `N/A` | `5.1` | `1` even when `total=0` | `1` | Single-page convention |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | `{}` | `{}` | No extra operation metadata |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Request correlation/generator | `TBD — exact generator chưa đặc tả` | `ApiEnvelope` field |

> Error response dùng cùng các field `success`, `businessCode`, `message`, `data`, `meta`, `traceId` của `ApiEnvelope`; không tạo `error_code` hoặc `error_message_id` riêng.
>
> `HTTPStatus` trong bảng là protocol status, không phải property JSON.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Categories retrieved",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Programming",
        "slug": "programming",
        "description": "Courses about programming"
      },
      {
        "id": 2,
        "name": "Design",
        "slug": "design",
        "description": null
      }
    ],
    "pagination": {
      "page": 1,
      "size": 2,
      "total": 2,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

## Ví dụ empty page — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "No active categories",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 0,
      "total": 0,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Invalid locale",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

## Ví dụ lỗi — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Categories could not be retrieved",
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
