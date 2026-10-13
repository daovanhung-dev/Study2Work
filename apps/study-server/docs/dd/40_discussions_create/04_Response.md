---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "40"
api_name: "Tạo topic/câu hỏi mới"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |
| Success HTTP status | `201` |
| Success business code | `DESIGN_RESOURCE_CREATED` |
| Success data type | `Page<Discussion>` theo approved catalog; page semantics chưa được định nghĩa cho create response. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success flag | `success` | `boolean` | No | N/A | N/A | Envelope | Fixed `true` on success | N/A | API envelope. |
| 2 | `businessCode` | Business code | `businessCode` | `string` | No | N/A | N/A | Envelope | `DESIGN_RESOURCE_CREATED` | N/A | Catalog HTTP 201. |
| 3 | `message` | Message | `message` | `string` | No | N/A | N/A | Envelope | Client-safe text | N/A | Exact text not defined. |
| 4 | `data.items[]` | Created Discussion item | `items` | `Discussion[]` | No | `discussions` / `users` | Candidate projection | Insert result | Candidate page item | SOURCE_REQUIRED | Catalog does not define comments projection or PageMeta for create. |
| 4.1 | `data.items[].id` | Discussion ID | `id` | `int64` | No | `discussions` | `id` | Insert result | Candidate generated ID | N/A | DDL declares BIGSERIAL; live generation unverified. |
| 4.2 | `data.items[].course_id` | Course ID | `course_id` | `int64` | No | `discussions` | `course_id` | Insert result | Direct mapping candidate | N/A | DDL permits NULL; guide/ERD say required. |
| 4.3 | `data.items[].title` | Topic title | `title` | `string` | No | N/A | N/A | SOURCE_REQUIRED | N/A | SOURCE_REQUIRED | No `discussions.title` column in ERD/DDL; response mapping unresolved. |
| 4.4 | `data.items[].content` | Topic content | `content` | `string` | No | `discussions` | `content` | Insert result | No conversion rule | SOURCE_REQUIRED | Response schema string; request declares int64; DDL column is TEXT. |
| 4.5 | `data.items[].author` | Author summary | `author` | `UserSummary` | No | `users` | Candidate profile fields | Principal lookup | Candidate mapping | SOURCE_REQUIRED | Query/lookup behavior not specified. |
| 4.5.1 | `data.items[].author.id` | Author ID | `id` | `int64` | No | `users` | `id` | Auth principal / candidate row | Candidate direct mapping | N/A | Current helper parses JWT `sub` as numeric user ID; API #40 is unwired. |
| 4.5.2 | `data.items[].author.full_name` | Author name | `full_name` | `string` | No | `users` | `full_name` | Candidate user lookup | Direct candidate | SOURCE_REQUIRED | Current access token claims do not include profile fields. |
| 4.5.3 | `data.items[].author.avatar_url` | Author avatar | `avatar_url` | `uri` | Yes | `users` | `avatar_url` | Candidate user lookup | Direct candidate | SOURCE_REQUIRED | Omit or null policy not endpoint-defined. |
| 4.6 | `data.items[].status` | Discussion status | `status` | `DiscussionStatus` | No | `discussions` | `status` | Insert result | DDL default `ACTIVE` is candidate only | SOURCE_REQUIRED | Allowed enum and create policy unresolved. |
| 4.7 | `data.items[].comments[]` | Comments | `comments` | `DiscussionComment[]` | No | `discussions` / `users` | N/A | Not defined | No projection rule | SOURCE_REQUIRED | API #42 reloads topic + comments; create response inclusion unresolved. |
| 4.8 | `data.pagination` | Pagination metadata | `pagination` | `PageMeta` | No | N/A | N/A | N/A | No source | SOURCE_REQUIRED | Create request has no page input or PageMeta policy. |
| 4.8.1 | `data.pagination.page` | Page number | `page` | `int32` | No | N/A | N/A | N/A | SOURCE_REQUIRED | N/A | No create-response page rule. |
| 4.8.2 | `data.pagination.size` | Page size | `size` | `int32` | No | N/A | N/A | N/A | SOURCE_REQUIRED | N/A | No create-response size rule. |
| 4.8.3 | `data.pagination.total` | Total items | `total` | `int64` | No | N/A | N/A | N/A | SOURCE_REQUIRED | N/A | No create-response count rule. |
| 4.8.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | No | N/A | N/A | N/A | SOURCE_REQUIRED | N/A | No page-size or calculation rule. |
| 5 | `meta` | Metadata | `meta` | `object` | No | N/A | N/A | Envelope | `{}` unless field errors apply | N/A | Follow API guidelines. |
| 6 | `traceId` | Trace ID | `traceId` | `uuid` | No | N/A | N/A | Request trace | Propagated trace ID | N/A | `X-Trace-Id` follows shared API guidelines. |

## Ví dụ thành công — HTTP 201

> Values are illustrative and do not establish a page policy, status enum, content conversion, author lookup, or comments projection. `content` in the request remains `int64` per catalog; `Discussion.content` in this response remains `string` per reusable schema.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Discussion created",
  "data": {
    "items": [
      {
        "id": 4001,
        "course_id": 101,
        "title": "Câu hỏi minh họa",
        "content": "Nội dung minh họa; chưa xác định chuyển đổi từ request int64",
        "author": {
          "id": 7,
          "full_name": "Người dùng minh họa",
          "avatar_url": null
        },
        "status": "SOURCE_REQUIRED",
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
  "traceId": "00000000-0000-4000-8000-000000000040"
}
```

## Ví dụ lỗi xác thực — HTTP 401

```json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000040"
}
```

## Response gaps

- `Page<Discussion>` is retained exactly from the catalog even though this is a synchronous create operation; pagination values have no source.
- `Discussion.title` is required by logical schema but has no physical column in the checked-in ERD/DDL.
- Request `content:int64!`, response `Discussion.content:string`, and DDL `content TEXT` have no approved conversion rule.
- `DiscussionStatus`, comments inclusion, author lookup and null/omit policy are not fully defined.
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
