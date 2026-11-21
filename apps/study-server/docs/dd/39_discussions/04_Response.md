---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "39"
api_name: "Lấy danh sách thread"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Contract type | ApiEnvelope<Page<Discussion>> theo API catalog; design-only, chưa runtime-verified. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 5.1/5.2/5.3 | 200/401/403/500 theo branch | N/A | Business code: 200 DESIGN_RESOURCE_RETRIEVED; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 500 DESIGN_INTERNAL_ERROR. Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1/5.2/5.3 | true khi success; false khi error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1/5.2/5.3 | Theo branch trong catalog | N/A | Không thêm business code. |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1/5.2/5.3 | Client-safe message | Nội dung chưa đặc tả | ApiEnvelope field; xem API guideline. |
| 5 | data | Discussion page | data | Page<Discussion> | No | discussions/users | N/A | 4.1 | Map Page<Discussion> | null trên error theo guideline | Logical response schema. |
| 5.1 | data.items | Thread items | items | array<Discussion> | No | discussions/users | N/A | 2.1/4.1 | Root threads trong course scope được phép; ACTIVE visibility/access là DERIVED | Empty result là [] | Page<T>; enrollment và status proposal cần xác nhận. |
| 5.1.1 | data.items[].id | Discussion ID | id | int64 | No | discussions | id | 2.1 | Direct mapping candidate | N/A | Contract field. |
| 5.1.2 | data.items[].course_id | Course ID | course_id | int64 | No | discussions | course_id | 2.1 | Direct mapping candidate | DDL nullable, contract required | ERD/DDL discrepancy. |
| 5.1.3 | data.items[].title | Thread title | title | string | No | N/A — source missing | N/A | 4.1 | SOURCE_REQUIRED | Không map từ content | Required logical field chưa có cột trong ERD/DDL. |
| 5.1.4 | data.items[].content | Thread content | content | string | No | discussions | content | 2.1 | Direct mapping candidate | N/A | Checked-in DDL field is TEXT NOT NULL. |
| 5.1.5 | data.items[].author | Author | author | UserSummary | No | users | N/A | 2.1/4.1 | Build UserSummary | N/A | Join candidate qua discussions.user_id. |
| 5.1.5.1 | data.items[].author.id | Author ID | id | int64 | No | users | id | 2.1 | Direct mapping candidate | N/A | Source FK is nullable in checked-in DDL. |
| 5.1.5.2 | data.items[].author.full_name | Author name | full_name | string | No | users | full_name | 2.1 | Direct mapping candidate | N/A | DB.sql declares VARCHAR(150) NOT NULL. |
| 5.1.5.3 | data.items[].author.avatar_url | Author avatar | avatar_url | uri | Yes | users | avatar_url | 2.1 | Direct mapping candidate | null when source is NULL | Optional UserSummary field. |
| 5.1.6 | data.items[].status | Discussion status | status | DiscussionStatus | No | discussions | status | 2.1 | Direct mapping candidate | Enum values unresolved | ACTIVE visibility filter is DERIVED; full enum/policy absent. |
| 5.1.7 | data.items[].comments | Comments | comments | array<DiscussionComment> | No | discussions/users | N/A | 2.2/4.1 | All direct child rows with status ACTIVE; created_at ASC, id ASC (DERIVED) | [] when none | Same comment projection/order as API #42; needs confirmation. |
| 5.1.7.1 | data.items[].comments[].id | Comment ID | id | int64 | No | discussions | id | 2.2 | Direct mapping candidate | N/A | Child discussion row ID. |
| 5.1.7.2 | data.items[].comments[].discussion_id | Parent discussion ID | discussion_id | int64 | No | discussions | parent_id | 2.2 | Map parent_id to discussion_id | N/A | Contract field name differs from physical column. |
| 5.1.7.3 | data.items[].comments[].content | Comment content | content | string | No | discussions | content | 2.2 | Direct mapping candidate | N/A | Child row content. |
| 5.1.7.4 | data.items[].comments[].author | Comment author | author | UserSummary | No | users | N/A | 2.2/4.1 | Build UserSummary | N/A | Join candidate via child user_id. |
| 5.1.7.4.1 | data.items[].comments[].author.id | Comment author ID | id | int64 | No | users | id | 2.2 | Direct mapping candidate | N/A | Child FK is nullable in checked-in DDL. |
| 5.1.7.4.2 | data.items[].comments[].author.full_name | Comment author name | full_name | string | No | users | full_name | 2.2 | Direct mapping candidate | N/A | DB.sql declares VARCHAR(150) NOT NULL. |
| 5.1.7.4.3 | data.items[].comments[].author.avatar_url | Comment author avatar | avatar_url | uri | Yes | users | avatar_url | 2.2 | Direct mapping candidate | null when source is NULL | Optional UserSummary field. |
| 5.1.7.5 | data.items[].comments[].created_at | Comment created time | created_at | date-time | No | discussions | created_at | 2.2 | ISO-8601 serialization candidate | N/A | Child row timestamp. |
| 5.2 | data.pagination | Pagination | pagination | PageMeta | No | N/A | N/A | 3.1/4.2 | Map PageMeta | N/A | Required reusable response schema. |
| 5.2.1 | data.pagination.page | Page number | page | int32 | No | N/A | N/A | 1.2/4.2 | Query page; default 1 (DERIVED) | Positive page proposed | Parse/range behavior needs confirmation. |
| 5.2.2 | data.pagination.size | Page size | size | int32 | No | N/A | N/A | 3.1/4.2 | Fixed 20 per API #10 precedent (DERIVED) | N/A | API #39 has no size query parameter. |
| 5.2.3 | data.pagination.total | Total threads | total | int64 | No | discussions | COUNT(*) candidate | 3.1/4.2 | Count roots within identical access/visibility/course scope | N/A | PageMeta field; access policy needs confirmation. |
| 5.2.4 | data.pagination.total_pages | Total pages | total_pages | int32 | No | N/A | N/A | 3.1/4.2 | ceil(total/20); 0 when total=0 (DERIVED) | N/A | Page-size and empty-page proposal needs confirmation. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 5.1/5.2/5.3 | ApiEnvelope metadata | {} per API guideline unless field errors apply | No endpoint-specific metadata defined. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 5.1/5.2/5.3 | Trace correlation ID | N/A | ApiEnvelope field. |

> Error response uses success=false, businessCode from the catalog, client-safe message, data=null, meta object and traceId. Do not expose internal query details.

## Ví dụ thành công — HTTP 200

> Example below illustrates JSON shape only. Values are illustrative, not source records, defaults, or an approved enum. The title placeholder documents the missing physical source.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Discussions retrieved",
  "data": {
    "items": [
      {
        "id": 1,
        "course_id": 101,
        "title": "SOURCE_REQUIRED — discussions.title chưa có cột",
        "content": "Nội dung ví dụ, không phải dữ liệu thực",
        "author": {
          "id": 7,
          "full_name": "Tên ví dụ",
          "avatar_url": null
        },
        "status": "TBD — DiscussionStatus",
        "comments": []
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
  "traceId": "00000000-0000-4000-8000-000000000039"
}
~~~

## Ví dụ lỗi xác thực — HTTP 401

~~~json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000039"
}
~~~

## Response gap

- Catalog-required Discussion.title has no source column in the discussions ERD or checked-in DDL.
- Discussion.comments[] is proposed as all direct ACTIVE children in created_at ASC, id ASC order, matching API #42; confirm whether full comments belong in the list response.
- Discussion visibility, status enum values and author relation integrity are not confirmed by runtime evidence.
- PageMeta values use a DERIVED proposal: page defaults to 1, size is fixed at 20, and total_pages is ceil(total/20), or zero for an empty result. Confirm before implementation.
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

