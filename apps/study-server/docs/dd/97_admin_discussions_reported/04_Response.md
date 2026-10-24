---
title: "Response"
order: 4
dd_id: "97"
api_name: "Lấy reported discussions"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4. Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Success contract

- HTTP status: `200`
- Business code: `DESIGN_RESOURCE_RETRIEVED`
- Body: `ApiEnvelope<Page<Discussion>>`
- Response fields bên dưới theo reusable schema trong API catalog. Candidate physical mapping và các giá trị pagination chưa được xác nhận.

| Field | Type | Required | Candidate source / mapping | Null / status |
|---|---|---:|---|---|
| `success` | boolean | Yes | Envelope success branch | DIRECT envelope convention |
| `businessCode` | string | Yes | Catalog literal | `DESIGN_RESOURCE_RETRIEVED` |
| `message` | string | Yes | Application safe message | Exact wording unspecified |
| `data` | `Page<Discussion>` | Yes | Logical queue result | Report relation/grain `SOURCE_REQUIRED` |
| `data.items` | `Discussion[]` | Yes | Logical queue result | Report relation/grain `SOURCE_REQUIRED` |
| `data.items[].id` | int64 | Yes | Candidate `discussions.id` | Legacy artifact only |
| `data.items[].course_id` | int64 | Yes | Candidate `discussions.course_id` | Legacy DDL allows NULL; required logical field mismatch |
| `data.items[].title` | string | Yes | No approved legacy source | `SOURCE_REQUIRED`; do not derive from content |
| `data.items[].content` | string | Yes | Candidate `discussions.content` | Legacy column is TEXT NOT NULL |
| `data.items[].author` | `UserSummary` | Yes | Candidate join to `users` | Required author; nullable legacy FK makes missing-author policy open |
| `data.items[].author.id` | int64 | Yes | Candidate `users.id` | Physical/live mapping unverified |
| `data.items[].author.full_name` | string | Yes | Candidate `users.full_name` | Physical/live mapping unverified |
| `data.items[].author.avatar_url` | uri? | No | Candidate `users.avatar_url` | Omit when null; candidate only |
| `data.items[].status` | `DiscussionStatus` | Yes | Candidate `discussions.status` | Enum members and queue eligibility unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Yes | Candidate child discussion rows | Summary extent/order/status filter `SOURCE_REQUIRED` |
| `data.items[].comments[].id` | int64 | Yes | Candidate child `discussions.id` | Candidate only |
| `data.items[].comments[].discussion_id` | int64 | Yes | Candidate child `parent_id` | Legacy column nullable; child-parent mapping candidate |
| `data.items[].comments[].content` | string | Yes | Candidate child `discussions.content` | Candidate only |
| `data.items[].comments[].author` | `UserSummary` | Yes | Candidate `users` join | Missing author behavior unresolved |
| `data.items[].comments[].author.id` | int64 | Yes | Candidate child `user_id` → `users.id` | Physical/live mapping unverified |
| `data.items[].comments[].author.full_name` | string | Yes | Candidate `users.full_name` | Physical/live mapping unverified |
| `data.items[].comments[].author.avatar_url` | uri? | No | Candidate `users.avatar_url` | Omit when null; candidate only |
| `data.items[].comments[].created_at` | date-time | Yes | Candidate child `discussions.created_at` | DDL has timestamp without timezone |
| `data.pagination` | `PageMeta` | Yes | Page metadata | Values/default unresolved |
| `data.pagination.page` | int32 | Yes | Page metadata | Value/default unresolved |
| `data.pagination.size` | int32 | Yes | Page metadata | No request size; value unresolved |
| `data.pagination.total` | int64 | Yes | Count of logical queue items | Whether count is discussion or report grain unresolved |
| `data.pagination.total_pages` | int32 | Yes | Page metadata | Calculation/default unresolved |
| `meta` | object | Yes | Envelope | Endpoint-specific members unspecified |
| `traceId` | uuid | Yes | Request trace | Shared envelope convention |

## Example

Ví dụ sau minh họa cấu trúc typed. Số pagination và field marker không phải default, business rule hoặc schema approval.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Reported discussions retrieved.",
  "data": {
    "items": [
      {
        "id": 101,
        "course_id": 55,
        "title": "SOURCE_REQUIRED: discussion title source",
        "content": "Example discussion content",
        "author": {"id": 8, "full_name": "Example author"},
        "status": "SOURCE_REQUIRED: DiscussionStatus",
        "comments": []
      }
    ],
    "pagination": {"page": 1, "size": 20, "total": 1, "total_pages": 1}
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000097"
}
```

Report reason/severity không có field trong response schema `Discussion`; không tự thêm. Example pagination là hình minh họa kiểu dữ liệu, chưa định nghĩa behavior.

## Error contract

| HTTP | Business code | Catalog condition |
|---:|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer/JWT authentication failure |
| 403 | `DESIGN_ACCESS_DENIED` | Authenticated caller lacks Admin authorization |
| 500 | `DESIGN_INTERNAL_ERROR` | Internal query/data mapping failure |

Catalog #97 không khai báo 404 hoặc 422. Error `data` theo API guideline là `null`; current `error_response(...)` chuyển absent/None data thành `{}` (`DISCREPANCY`).

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
