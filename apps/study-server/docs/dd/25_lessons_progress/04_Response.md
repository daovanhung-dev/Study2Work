---
title: "Response"
order: 4
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | API catalog | N/A | 4.2–4.6 | Fixed by branch: 200/401/403/404/422/500 | N/A | Transport status from API #25 catalog row. |
| 2 | success | Success flag | `success` | boolean | No | ApiEnvelope schema | `success` | 4.2–4.6 | Envelope field | Error serialization not verified | Reusable envelope schema declares boolean. |
| 3 | businessCode | Business code | `businessCode` | string | No | API catalog | N/A | 4.2–4.6 | Fixed by branch | N/A | Use only API #25 codes listed below. |
| 4 | message | Message | `message` | string | SOURCE_REQUIRED | ApiEnvelope schema | `message` | 4.2–4.6 | SOURCE_REQUIRED | Exact text not specified | Reusable schema names the field but gives no message policy. |
| 5 | data | Lesson payload | `data` | object | Required on success | API catalog schema | N/A | 4.2 | `ApiEnvelope<Lesson>` | Error data shape unspecified | Diagram uses generic `ApiEnvelope`; catalog is the specific response contract. |
| 5.1 | `data.id` | Lesson ID | `id` | int64 | No | `lessons` — candidate, DESIGN_ONLY | `id` | 3/4.2 | Direct candidate mapping | Required by reusable Lesson schema | Progress update response query/projection not confirmed. |
| 5.2 | `data.course_id` | Course ID | `course_id` | int64 | No | `lessons` — candidate, DESIGN_ONLY | `course_id` | 3/4.2 | Direct candidate mapping | Required by reusable Lesson schema | DDL nullability differs from DB design; response assembly unresolved. |
| 5.3 | `data.title` | Lesson title | `title` | string | No | `lessons` — candidate, DESIGN_ONLY | `name` | 3/4.2 | `name` maps to logical `title` | Required by reusable Lesson schema | Candidate mapping only; query not confirmed. |
| 5.4 | `data.content` | Lesson content | `content` | string | Optional | `lessons` — candidate, DESIGN_ONLY | `content` | 3/4.2 | Candidate direct mapping | Null/omit behavior unspecified | Optional in reusable Lesson schema and nullable in checked-in DDL. |
| 5.5 | `data.video_url` | Video URL | `video_url` | uri | Optional | `lessons` — candidate, DESIGN_ONLY | `video_url` | 3/4.2 | Candidate conversion from TEXT to URI | Null/omit behavior unspecified | Query and serialization are not confirmed. |
| 5.6 | `data.order` | Lesson order | `order` | int32 | No | `lessons` — candidate, DESIGN_ONLY | `sort_order` | 3/4.2 | `sort_order` maps to logical `order` | Required by reusable Lesson schema | Candidate mapping only; query not confirmed. |
| 5.7 | `data.status` | Lesson status | `status` | LessonStatus | No | `lessons` — candidate, DESIGN_ONLY | `status` | 3/4.2 | Candidate direct mapping | Enum values unspecified | API #25 response assembly and enum values are unresolved. |
| 6 | `meta` | Metadata | `meta` | object | No | ApiEnvelope schema | `meta` | 4.2–4.6 | Envelope field | Members unspecified | API-specific metadata is not declared. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | ApiEnvelope schema | `traceId` | 4.2–4.6 | Envelope field | Required by reusable schema | Runtime trace behavior for API #25 is not verified. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | `DESIGN_RESOURCE_UPDATED` | Progress update accepted per catalog. |
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer JWT missing or invalid per catalog meaning. |
| 403 | `DESIGN_ACCESS_DENIED` | Student role/access denied; API-specific predicate unresolved. |
| 404 | `DESIGN_RESOURCE_NOT_FOUND` | Resource not found per catalog; exact condition unresolved. |
| 422 | `DESIGN_VALIDATION_ERROR` | Validation error per catalog; field constraints/triggers unresolved. |
| 500 | `DESIGN_INTERNAL_ERROR` | Internal error. |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
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

> Ví dụ minh họa `ApiEnvelope<Lesson>` theo catalog. `<LessonStatus>` là placeholder cho enum chưa được liệt kê; Lesson query/projection, message text và null/omit behavior chưa được xác nhận. Payload không khẳng định API trả dữ liệu lesson nào sau mutation.

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

> Ví dụ chỉ minh họa HTTP/business code. Catalog không định nghĩa error-specific `data` shape; `data: {}` không phải wire contract. Điều kiện access của API #25 chưa được xác nhận.

---
## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
