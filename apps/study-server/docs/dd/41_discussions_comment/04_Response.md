---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "41"
api_name: "Thêm bình luận/trả lời"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP status | 201 |
| Success business code | DESIGN_RESOURCE_CREATED |
| Success data type | Page<Discussion> theo approved catalog; DERIVED proposal: một root thread và pagination 1/1/1/1. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | success | Success flag | success | boolean | No | N/A | N/A | Envelope | true on success | N/A | Shared envelope. |
| 2 | businessCode | Business code | businessCode | string | No | N/A | N/A | Envelope | DESIGN_RESOURCE_CREATED | N/A | Catalog HTTP 201. |
| 3 | message | Message | message | string | No | N/A | N/A | Envelope | Client-safe text | N/A | Exact text not defined. |
| 4 | data.items[] | Updated Discussion thread | items | Discussion[] | No | discussions / users | Candidate projection | Parent thread and children after insert | DERIVED: one updated thread item | Needs confirmation | Page<Discussion> is fixed by catalog; diagram then reloads through API #42. |
| 4.1 | data.items[].id | Topic ID | id | int64 | No | discussions | id | Parent lookup | Direct mapping candidate | N/A | Assumes discussion_id identifies root topic. |
| 4.2 | data.items[].course_id | Course ID | course_id | int64 | No | discussions | course_id | Parent row | Inherit parent course | N/A | Derived same-course reply; DDL nullable. |
| 4.3 | data.items[].title | Topic title | title | string | No | N/A | N/A | SOURCE_REQUIRED | N/A | SOURCE_REQUIRED | Required by schema but no physical column. |
| 4.4 | data.items[].content | Topic content | content | string | No | discussions | content | Parent row | Direct candidate | SOURCE_REQUIRED | DDL TEXT; title/content design source gaps persist. |
| 4.5 | data.items[].author | Topic author | author | UserSummary | No | users | Candidate profile fields | Parent author lookup | Candidate mapping | SOURCE_REQUIRED | Query and null policy not endpoint-defined. |
| 4.6 | data.items[].status | Topic status | status | DiscussionStatus | No | discussions | status | Parent row | Direct candidate | SOURCE_REQUIRED | Enum/visibility policy unknown. |
| 4.7 | data.items[].comments[] | Thread comments | comments | DiscussionComment[] | No | discussions / users | Candidate child rows | Child query after insert | All direct ACTIVE children, including the new child; created_at ASC, id ASC | DERIVED; Needs confirmation | Same projection/order proposed by API #42; AC-19 still calls #42 to reload. |
| 4.7.1 | data.items[].comments[].id | Comment ID | id | int64 | No | discussions | child id | Child query after insert | Direct candidate | N/A | Includes every direct ACTIVE child; stable chronological ordering is DERIVED. |
| 4.7.2 | data.items[].comments[].discussion_id | Parent topic ID | discussion_id | int64 | No | discussions | child parent_id | Child query after insert | Map parent_id to logical field | N/A | Derived direct-child relation. |
| 4.7.3 | data.items[].comments[].content | Comment content | content | string | No | discussions | child content | Child query after insert | Decimal string from request int64 | Needs confirmation | Explicit contract/schema/DDL type discrepancy. |
| 4.7.4 | data.items[].comments[].author | Comment author | author | UserSummary | No | users | id, full_name, avatar_url | Authenticated user lookup | Candidate direct mapping | SOURCE_REQUIRED | Current JWT helper exposes ID/role, not display profile. |
| 4.7.5 | data.items[].comments[].created_at | Comment creation time | created_at | date-time | No | discussions | child created_at | Insert result | Server timestamp candidate | DERIVED; Needs confirmation | Checked-in DDL requires timestamp and has no default. |
| 4.8 | data.pagination | Pagination metadata | pagination | PageMeta | No | N/A | N/A | N/A | DERIVED proposal: page=1,size=1,total=1,total_pages=1 | Needs confirmation | One updated topic is a simple interpretation; diagram does not define page semantics. |
| 5 | meta | Metadata | meta | object | No | N/A | N/A | Envelope | {} unless metadata is specified | N/A | No endpoint-specific metadata is declared. |
| 6 | traceId | Trace ID | traceId | uuid | No | Request trace | N/A | Current trace helper convention | UUID string | N/A | Shared API envelope. |

## Example success response

> Illustrative only. The page interpretation, title source, content conversion and author projection below are derived/provisional; see [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Created",
  "data": {
    "items": [
      {
        "id": 320,
        "course_id": 101,
        "title": "SOURCE_REQUIRED: topic title from parent",
        "content": "123",
        "author": {
          "id": 42,
          "full_name": "Nguyen Van A",
          "avatar_url": null
        },
        "status": "ACTIVE",
        "comments": [
          {
            "id": 321,
            "discussion_id": 320,
            "content": "123",
            "author": {
              "id": 42,
              "full_name": "Nguyen Van A",
              "avatar_url": null
            },
            "created_at": "2026-10-23T10:00:00Z"
          }
        ]
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
  "traceId": "00000000-0000-4000-8000-000000000041"
}
~~~

> title ở ví dụ là marker nêu thiếu nguồn, không phải giá trị có thể trả runtime. status=ACTIVE, decimal-string conversion, mọi direct ACTIVE comment và page metadata đều là candidate/DERIVED. Activity diagram yêu cầu client tiếp tục GET API #42.
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

