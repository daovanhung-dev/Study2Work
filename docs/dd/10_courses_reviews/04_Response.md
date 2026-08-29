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
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch: `200/404/500` | `N/A` | Protocol status; không phải property JSON |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `N/A` | Uses `DESIGN_*` code from contract |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw SQL/stack trace |
| 5 | `data` | Reviews page | `data` | `object` | `No` | `discussions/users` | `N/A` | `5.1/6.1` | Map `Page<Discussion>` | `{}` on error | `ApiEnvelope<Page<Discussion>>` |
| 5.1 | `data.items` | Review items | `items` | `array` | `No` | `discussions` | `N/A` | `4.1/5.1` | Map review roots | `[]` khi không có review | `Discussion[]` |
| 5.1.1 | `data.items[].id` | Review ID | `id` | `int64` | `No` | `discussions` | `id` | `4.1` | Direct mapping | `N/A` | |
| 5.1.2 | `data.items[].course_id` | Course ID | `course_id` | `int64` | `No` | `discussions` | `course_id` | `4.1` | Direct mapping | `N/A` | |
| 5.1.3 | `data.items[].title` | Review title | `title` | `string` | `No` | `N/A — source missing` | `N/A` | `5.1` | `TBD — no discussions.title column` | `TBD — cannot derive from content` | Contract requires field but ERD has no source |
| 5.1.4 | `data.items[].content` | Review content | `content` | `string` | `No` | `discussions` | `content` | `4.1` | Direct mapping | `N/A` | |
| 5.1.5 | `data.items[].author` | Review author | `author` | `object` | `No` | `users` | `N/A` | `4.1/5.1` | Build `UserSummary` | `N/A` | |
| 5.1.5.1 | `data.items[].author.id` | Author ID | `id` | `int64` | `No` | `users` | `id` | `4.1` | Direct mapping from `discussions.user_id` join | `N/A` | |
| 5.1.5.2 | `data.items[].author.full_name` | Author full name | `full_name` | `string` | `No` | `users` | `full_name` | `4.1` | Direct mapping | `N/A` | |
| 5.1.5.3 | `data.items[].author.avatar_url` | Author avatar URL | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `4.1` | Direct mapping | `null` when source is `NULL` | Optional `UserSummary` field |
| 5.1.6 | `data.items[].status` | Review status | `status` | `DiscussionStatus` | `No` | `discussions` | `status` | `4.1` | Filter `ACTIVE`, direct mapping | `N/A` | Visibility assumption |
| 5.1.7 | `data.items[].comments` | Review replies | `comments` | `array` | `No` | `discussions/users` | `N/A` | `4.2/5.1` | Map child discussions | `[]` when no active reply | `DiscussionComment[]` |
| 5.1.7.1 | `data.items[].comments[].id` | Reply ID | `id` | `int64` | `No` | `discussions` | `id` | `4.2` | Direct mapping | `N/A` | |
| 5.1.7.2 | `data.items[].comments[].discussion_id` | Parent discussion ID | `discussion_id` | `int64` | `No` | `discussions` | `parent_id` | `4.2` | Map parent review ID | `N/A` | |
| 5.1.7.3 | `data.items[].comments[].content` | Reply content | `content` | `string` | `No` | `discussions` | `content` | `4.2` | Direct mapping | `N/A` | |
| 5.1.7.4 | `data.items[].comments[].author` | Reply author | `author` | `object` | `No` | `users` | `N/A` | `4.2/5.1` | Build `UserSummary` | `N/A` | |
| 5.1.7.4.1 | `data.items[].comments[].author.id` | Reply author ID | `id` | `int64` | `No` | `users` | `id` | `4.2` | Direct mapping from child `user_id` join | `N/A` | |
| 5.1.7.4.2 | `data.items[].comments[].author.full_name` | Reply author name | `full_name` | `string` | `No` | `users` | `full_name` | `4.2` | Direct mapping | `N/A` | |
| 5.1.7.4.3 | `data.items[].comments[].author.avatar_url` | Reply author avatar | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `4.2` | Direct mapping | `null` when source is `NULL` | Optional `UserSummary` field |
| 5.1.7.5 | `data.items[].comments[].created_at` | Reply created time | `created_at` | `date-time` | `No` | `discussions` | `created_at` | `4.2` | ISO-8601 serialization | `N/A` | |
| 5.2 | `data.pagination` | Pagination metadata | `pagination` | `object` | `No` | `N/A` | `N/A` | `5.2` | Map `PageMeta` | `{}` on error | |
| 5.2.1 | `data.pagination.page` | Page number | `page` | `int32` | `No` | `N/A` | `N/A` | `5.2` | `effective_page` | `1` when omitted | Design-only default |
| 5.2.2 | `data.pagination.size` | Page size | `size` | `int32` | `No` | `N/A` | `N/A` | `5.2` | Fixed `20` | `20` | Not a client query field |
| 5.2.3 | `data.pagination.total` | Total reviews | `total` | `int64` | `No` | `discussions` | `COUNT(*)` | `4.3/5.2` | Count matching review roots | `0` when empty | |
| 5.2.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | `No` | `N/A` | `N/A` | `5.2` | `ceil(total / 20)` | `0` when total is `0` | Design-only page size |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | No aggregate rating extension |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Request correlation UUID | `TBD — exact generator` | `ApiEnvelope` field |

> `Discussion.title`, `rating filter` và aggregate rating được giữ như discrepancy/TBD theo nguồn. Không thêm field rating hoặc aggregate vào JSON khi contract chưa định nghĩa.
>
> Error response dùng cùng các field `success`, `businessCode`, `message`, `data`, `meta`, `traceId` của `ApiEnvelope`; `data = {}` trong ví dụ lỗi.
>
> `HTTPStatus` trong bảng là protocol status, không phải property JSON.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Reviews retrieved",
  "data": {
    "items": [
      {
        "id": 501,
        "course_id": 101,
        "title": "<TBD — discussions.title chưa có source>",
        "content": "Nội dung đánh giá mẫu",
        "author": {
          "id": 7,
          "full_name": "Nguyen Van A",
          "avatar_url": null
        },
        "status": "ACTIVE",
        "comments": [
          {
            "id": 502,
            "discussion_id": 501,
            "content": "Phản hồi mẫu",
            "author": {
              "id": 8,
              "full_name": "Nguyen Van B",
              "avatar_url": null
            },
            "created_at": "2026-08-29T00:00:00Z"
          }
        ]
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

## Ví dụ không có review — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "No reviews found",
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

## Ví dụ lỗi không tìm thấy course — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Published course not found",
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
  "message": "Reviews could not be retrieved",
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
