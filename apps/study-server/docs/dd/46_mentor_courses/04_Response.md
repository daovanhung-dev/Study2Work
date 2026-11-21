---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
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
| 1 | `HTTPStatus` | HTTP status | N/A | integer | No | N/A | N/A | 5 | Success `200`; errors `401/403/422/500` | N/A | Protocol status, not JSON property. |
| 2 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 5 | `true` success; `false` error | N/A | ApiEnvelope. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 5 | Branch code from catalog | N/A | Do not add business codes. |
| 4 | `message` | Message | `message` | string | No | N/A | N/A | 5 | Safe branch message | Text unspecified | No internal detail. |
| 5 | `data.items` | Course items | `items` | `Course[]` | No | `courses/users` | Q1 projection | 4 | Map each row to Course | `[]` for no result; DERIVED | Category optional and omitted without relation. |
| 5.1 | `data.items[].id` | Course ID | `id` | int64 | No | `courses` | `id` | 4 | Direct legacy candidate | N/A | V1-PILOT ID is UUID. |
| 5.2 | `data.items[].title` | Course title | `title` | string | No | `courses` | `name` | 4 | Alias `name` to `title` | N/A | API #6 precedent. |
| 5.3 | `data.items[].description` | Description | `description` | string | Yes | `courses` | `description` | 4 | Direct mapping | `null` if source NULL | Optional contract field. |
| 5.4 | `data.items[].thumbnail_url` | Thumbnail | `thumbnail_url` | uri | Yes | `courses` | `thumbnail_url` | 4 | Direct mapping | `null` if source NULL | Optional contract field. |
| 5.5 | `data.items[].price` | Price | `price` | decimal-string | No | `courses` | `price` | 4 | Decimal-safe string conversion | Missing source is integrity gap | Legacy column nullable. |
| 5.6 | `data.items[].status` | Status | `status` | CourseStatus | No | `courses` | `status` | 4 | Direct mapping | Missing source is integrity gap | Enum member list unknown. |
| 5.7 | `data.items[].mentor.id` | Mentor ID | `id` | int64 | No | `users` | `id` | 4 | Direct mapping | Missing join is integrity gap | Owner relation candidate. |
| 5.8 | `data.items[].mentor.full_name` | Mentor name | `full_name` | string | No | `users` | `full_name` | 4 | Direct mapping | Missing value is integrity gap | Required by UserSummary. |
| 5.9 | `data.items[].mentor.avatar_url` | Mentor avatar | `avatar_url` | uri | Yes | `users` | `avatar_url` | 4 | Direct mapping | `null` if source NULL | Optional UserSummary field. |
| 5.10 | `data.items[].category` | Category | `category` | Category | Yes | N/A | N/A | 4 | No source-backed relation | Omit | Optional contract field; do not fabricate. |
| 6 | `data.pagination.page` | Page | `page` | int32 | No | N/A | Effective page | 4 | Request or default | `1` when omitted | Default direct. |
| 6.1 | `data.pagination.size` | Page size | `size` | int32 | No | N/A | Effective size | 4 | Request or default | `20` when omitted | Default direct; max 100 derived. |
| 6.2 | `data.pagination.total` | Total | `total` | int64 | No | `courses` | `COUNT(*)` | 3 | Count same owner/status scope as Q1 | `0` if none | Candidate query. |
| 6.3 | `data.pagination.total_pages` | Total pages | `total_pages` | int32 | No | N/A | N/A | 4 | `ceil(total / size)` | `0` when total is 0 | DERIVED. |
| 7 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 5 | Empty metadata unless error detail specified | `{}` candidate | Exact shape for errors unresolved. |
| 8 | `traceId` | Trace ID | `traceId` | uuid | No | N/A | N/A | 5 | Request correlation ID | N/A | ApiEnvelope field. |

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Mentor courses retrieved",
  "data": {
    "items": [
      {
        "id": 101,
        "title": "Introduction to Programming",
        "description": null,
        "thumbnail_url": null,
        "price": "0.00",
        "status": "DRAFT",
        "mentor": {"id": 7, "full_name": "Nguyen Van Mentor", "avatar_url": null}
      }
    ],
    "pagination": {"page": 1, "size": 20, "total": 1, "total_pages": 1}
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> Giá trị `DRAFT` chỉ minh họa chuỗi status; đây không phải xác nhận member hợp lệ của `CourseStatus`.

## Ví dụ danh sách rỗng — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "No courses found",
  "data": {"items": [], "pagination": {"page": 1, "size": 20, "total": 0, "total_pages": 0}},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi validation — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Invalid query parameter",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

> Error guideline yêu cầu `data: null`; current `error_response()` trả `{}` nếu không truyền data — `DISCREPANCY`.
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
