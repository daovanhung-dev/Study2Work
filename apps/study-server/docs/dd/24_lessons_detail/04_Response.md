---
title: "Response"
order: 4
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | API catalog | N/A | 4.1–4.4 | Fixed by branch: 200/401/403/404/500 | N/A | Transport status from API #24 catalog row. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> schema | success | 4.1–4.4 | Envelope field | Error serialization not verified | Reusable envelope schema declares boolean. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 4.1–4.4 | Fixed by branch | N/A | Use only API #24 codes listed below. |
| 4 | message | Message | message | string | SOURCE_REQUIRED | ApiEnvelope<T> schema | message | 4.1–4.4 | SOURCE_REQUIRED | Exact text not specified | Reusable schema names the field but gives no message policy. |
| 5 | data | Lesson payload | data | object | Required on success | API catalog schema | N/A | 3/4.1 | `ApiEnvelope<Lesson>` | Error branch shape unspecified | Catalog is more specific than the diagram's generic `ApiEnvelope`. |
| 5.1 | data.id | Lesson ID | id | int64 | No | lessons — candidate, DESIGN_ONLY | id | 3/4.1 | Direct candidate mapping | Required by reusable Lesson schema | API #24 query/projection not confirmed. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | lessons — candidate, DESIGN_ONLY | course_id | 3/4.1 | Direct candidate mapping | Required by reusable Lesson schema | DDL nullability differs from DB design notes; see [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). |
| 5.3 | data.title | Lesson title | title | string | No | lessons — candidate, DESIGN_ONLY | name | 3/4.1 | `name` maps to logical `title` | Required by reusable Lesson schema | Candidate mapping from DB design documentation. |
| 5.4 | data.content | Lesson content | content | string | Optional | lessons — candidate, DESIGN_ONLY | content | 3/4.1 | Direct candidate mapping | Null/omit behavior unspecified | Optional in reusable Lesson schema; nullable in checked-in DDL. |
| 5.5 | data.video_url | Video URL | video_url | uri | Optional | lessons — candidate, DESIGN_ONLY | video_url | 3/4.1 | Candidate conversion from TEXT to URI | Null/omit and validation behavior unspecified | Optional in reusable Lesson schema; nullable in checked-in DDL. |
| 5.6 | data.order | Lesson order | order | int32 | No | lessons — candidate, DESIGN_ONLY | sort_order | 3/4.1 | `sort_order` maps to logical `order` | Required by reusable Lesson schema | DDL default is 0; query and serialization are not confirmed. |
| 5.7 | data.status | Lesson status | status | LessonStatus | No | lessons — candidate, DESIGN_ONLY | status | 3/4.1 | Candidate direct mapping | Enum values not specified | Catalog names `LessonStatus` without listing allowed values. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> schema | meta | 4.1–4.4 | Envelope field | Members unspecified | API-specific metadata is not declared. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> schema | traceId | 4.1–4.4 | Envelope field | Required by reusable schema | Runtime trace behavior for API #24 is not verified. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Lesson retrieved per catalog. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT missing or invalid per catalog meaning. |
| 403 | DESIGN_ACCESS_DENIED | Student role/access denied; API-specific predicate and error payload are unresolved. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource not found per catalog; exact lesson/visibility condition is unresolved. |
| 500 | DESIGN_INTERNAL_ERROR | Internal error. |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 101,
    "course_id": 9001,
    "title": "Example lesson",
    "content": "Lesson content example",
    "video_url": "https://example.test/lesson.mp4",
    "order": 1,
    "status": "PUBLISHED"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> Ví dụ minh họa `ApiEnvelope<Lesson>` theo catalog. `PUBLISHED` chỉ là giá trị ví dụ được nhắc trong nguồn design; enum đầy đủ, message text, query projection và null/omit behavior chưa được xác nhận.

## Ví dụ lỗi — HTTP 403

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Error message and payload shape are not specified by the contract.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

> Ví dụ chỉ minh họa HTTP/business code. Catalog không định nghĩa error-specific `data` shape; `data: {}` không phải wire contract. AC-14 nhắc reason ở bước access của API #22; không áp cấu trúc reason đó sang API #24.

---
## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
