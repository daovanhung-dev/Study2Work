---
title: "Response"
order: 4
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
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
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 4.1–4.5 | Fixed by branch: 201/401/403/404/422/500 | N/A | Transport status from API catalog. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> schema | success | 4.1–4.5 | true on success; false on error per reusable envelope | N/A | API #23 runtime serialization is not verified. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 4.1–4.5 | Fixed by branch | N/A | Preserve the codes declared for API #23. |
| 4 | message | Message | message | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4.1–4.5 | SOURCE_REQUIRED | N/A | Exact message text is not specified. |
| 5 | data | Lesson | data | object | Required by ApiEnvelope<Lesson> on success | API catalog schema | N/A | 3/4.1 | Lesson generic payload | Error branch shape unspecified | The diagram only states ApiEnvelope; keep catalog response type and track discrepancy. |
| 5.1 | data.id | Lesson ID | id | int64 | No | lessons — candidate, DESIGN_ONLY | id | 3/4.1 | Direct candidate mapping | Required by Lesson schema | API #23 response query/projection is not confirmed. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | lessons — candidate, DESIGN_ONLY | course_id | 3/4.1 | Direct candidate mapping | Required by Lesson schema | Parent relationship is design evidence only. |
| 5.3 | data.title | Lesson title | title | string | No | lessons — candidate, DESIGN_ONLY | name | 3/4.1 | name maps to logical title in DB design | Required by Lesson schema | API #23 response query is not confirmed. |
| 5.4 | data.content | Lesson content | content | string | Optional | lessons — candidate, DESIGN_ONLY | content | 3/4.1 | Direct candidate mapping | Null/omit behavior unspecified | Optional in reusable Lesson schema. |
| 5.5 | data.video_url | Video URL | video_url | uri | Optional | lessons — candidate, DESIGN_ONLY | video_url | 3/4.1 | Direct candidate mapping | Null/omit behavior unspecified | Optional in reusable Lesson schema. |
| 5.6 | data.order | Lesson order | order | int32 | No | lessons — candidate, DESIGN_ONLY | sort_order | 3/4.1 | sort_order maps to logical order in DB design | Required by Lesson schema | API #23 response query is not confirmed. |
| 5.7 | data.status | Lesson status | status | LessonStatus | No | lessons — candidate, DESIGN_ONLY | status | 3/4.1 | Direct candidate mapping | Required by Lesson schema | Enum values are not enumerated in this API contract. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> schema | meta | 4.1–4.5 | Object per reusable envelope | Members unspecified | No API-specific metadata is declared. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> schema | traceId | 4.1–4.5 | UUID per reusable envelope | Required by schema | Runtime trace behavior is not verified. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 201 | DESIGN_RESOURCE_CREATED | Resource created per catalog; relationship to an existing progress row in the UPSERT flow needs confirmation. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT missing or invalid. |
| 403 | DESIGN_ACCESS_DENIED | Student role or access denied; API #23-specific rule/reason wire shape is unresolved. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource not found; API-specific condition is unresolved. |
| 422 | DESIGN_VALIDATION_ERROR | Request validation error; exact path validation condition is not specified. |
| 500 | DESIGN_INTERNAL_ERROR | Internal error. |

## Ví dụ thành công — HTTP 201

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 101,
    "course_id": 9001,
    "title": "Example lesson",
    "content": "Lesson content example",
    "video_url": "https://example.test/lesson.mp4",
    "order": 1,
    "status": "<LessonStatus>"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> Ví dụ minh họa schema ApiEnvelope<Lesson> theo catalog. Message, LessonStatus và việc trả Lesson trong payload cần được đối chiếu với contract serialization; ví dụ không khẳng định response lấy từ query nào.

## Ví dụ lỗi — HTTP 403

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Message text and error payload shape are not specified by the contract.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

> Ví dụ chỉ minh họa code HTTP/business. Catalog không định nghĩa error payload; data={} không phải wire contract. AC-14 ghi “403 + lý do” ở bước access check nhưng chưa quy định vị trí hoặc cấu trúc lý do.

---
## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
