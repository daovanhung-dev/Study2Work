---
title: "Response"
order: 4
dd_id: "99"
api_name: "Điều chỉnh trạng thái kiểm duyệt discussion"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2. Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

Success response giữ contract trực tiếp `ApiEnvelope<Page<Discussion>>`, HTTP 200 và `DESIGN_RESOURCE_UPDATED`. Không thay bằng `ActionResult` hoặc thêm action/reason/report fields vào reusable `Discussion`.

| Field | Type | Description | Basis/status |
|---|---|---|---|
| `success` | boolean | Kết quả xử lý | Envelope convention |
| `businessCode` | string | Business code của nhánh response | DIRECT: `DESIGN_RESOURCE_UPDATED` |
| `message` | string | Message cho consumer | Wording chưa định nghĩa |
| `data` | `Page<Discussion>` | Payload success | DIRECT generic response |
| `data.items[]` | `Discussion` | Discussion records trong page | DIRECT schema; membership/cardinality sau PATCH chưa rõ |
| `data.items` | `Discussion[]` | Danh sách Discussion theo Page schema | DIRECT shape; membership/cardinality sau PATCH chưa rõ |
| `data.pagination` | `PageMeta` | Page metadata | DIRECT schema; values chưa được xác nhận |
| `data.pagination.page` | int32 | Số trang | DIRECT field; request không có page; value `DERIVED` nếu dùng one-item page |
| `data.pagination.size` | int32 | Kích thước trang | DIRECT field; request không có size; value `DERIVED` nếu dùng one-item page |
| `data.pagination.total` | int64 | Tổng record | DIRECT field; mutation-result semantics chưa rõ |
| `data.pagination.total_pages` | int32 | Tổng số trang | DIRECT field; value chưa được xác nhận |
| `meta` | object | Metadata envelope | Endpoint-specific content chưa định nghĩa |
| `traceId` | uuid | Request trace identifier | Envelope convention |

### Discussion fields

| Field | Type | Candidate source | Mapping/null rule | Basis/status |
|---|---|---|---|---|
| `data.items[].id` | int64 | `discussions.id` | Candidate direct mapping | Legacy DDL only |
| `data.items[].course_id` | int64 | `discussions.course_id` | Contract required; legacy DDL nullable | Discrepancy |
| `data.items[].title` | string | No legacy column | Do not derive from `content` | `SOURCE_REQUIRED` |
| `data.items[].content` | string | `discussions.content` | Preserve stored text | Legacy candidate |
| `data.items[].author` | `UserSummary` | Candidate user relation | Required author projection; legacy `user_id` nullable | Candidate/discrepancy |
| `data.items[].author.id` | int64 | Candidate `users.id` via `discussions.user_id` | Required projection; legacy FK nullable | Candidate/discrepancy |
| `data.items[].author.full_name` | string | Candidate `users.full_name` | Required projection | Legacy candidate; live schema unknown |
| `data.items[].author.avatar_url` | uri? | Candidate `users.avatar_url` | Optional; null versus omission unresolved | Legacy candidate |
| `data.items[].status` | `DiscussionStatus` | Candidate `discussions.status` | Return approved value only | Tokens and post-action transition unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Candidate child `discussions` | Admin moderation visibility, nesting and membership unresolved | `SOURCE_REQUIRED` |
| `data.items[].comments[]` | `DiscussionComment` | Child discussion record | Candidate only; membership and nesting unresolved | `SOURCE_REQUIRED` |
| `data.items[].comments[].id` | int64 | Child `discussions.id` | Candidate direct mapping | Legacy candidate |
| `data.items[].comments[].discussion_id` | int64 | Child `discussions.parent_id` | Candidate parent mapping | Legacy candidate; nullable FK |
| `data.items[].comments[].content` | string | Child `discussions.content` | Preserve stored text | Legacy candidate |
| `data.items[].comments[].author` | `UserSummary` | Candidate child author | Required author projection; child `user_id` nullable | Candidate/discrepancy |
| `data.items[].comments[].author.id` | int64 | Candidate child `users.id` | Required projection; child `user_id` nullable | Candidate/discrepancy |
| `data.items[].comments[].author.full_name` | string | Candidate child `users.full_name` | Required projection | Legacy candidate |
| `data.items[].comments[].author.avatar_url` | uri? | Candidate child `users.avatar_url` | Optional; null serialization unresolved | Legacy candidate |
| `data.items[].comments[].created_at` | date-time | Child `discussions.created_at` | Serialize using approved timezone convention | Legacy DDL timestamp has no timezone |

## Ví dụ thành công

Shape minh họa theo catalog. Các Discussion values và `DiscussionStatus` bên dưới là placeholders để thể hiện field shape; chúng không chốt dữ liệu thật, enum hay transition. Pagination `1/1` là proposal `DERIVED` cho một item.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Moderation decision recorded.",
  "data": {
    "items": [
      {
        "id": 123,
        "course_id": 45,
        "title": "<SOURCE_REQUIRED: discussion title>",
        "content": "Nội dung discussion",
        "author": {
          "id": 9,
          "full_name": "Nguyễn An"
        },
        "status": "<SOURCE_REQUIRED: DiscussionStatus>",
        "comments": []
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
  "traceId": "00000000-0000-4000-8000-000000000099"
}
```

`title` and `status` placeholder strings are not literal values. They highlight that the reusable response requires these fields while the current schema evidence does not establish their values. Empty comments, `meta:{}` and the one-item pagination values are not approved runtime rules.

## Ví dụ lỗi

Catalog declares the following examples by status and code. Exact message, error details and `data` null/empty serialization must follow the shared error contract at implementation time.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Discussion not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000099"
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
