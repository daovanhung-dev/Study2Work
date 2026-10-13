---
title: "Response"
order: 4
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
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
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | API catalog | N/A | 5.1–5.4 | Fixed by branch: 200/401/403/404/500 | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | `ApiEnvelope<T>` schema | success | 5.1–5.4 | Envelope field | Serialization chưa runtime-verified. | Catalog reusable schema. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 5.1–5.4 | Fixed by branch | N/A | Chỉ dùng code API #26 bên dưới. |
| 4 | message | Message | message | string | SOURCE_REQUIRED | `ApiEnvelope<T>` schema | message | 5.1–5.4 | SOURCE_REQUIRED | Message policy chưa đặc tả. | Reusable schema nêu field, không quy định text. |
| 5 | data | Lesson payload | data | object (`Lesson`) | Required on success per generic schema | API catalog reusable schema | N/A | 4.1/5.1 | `ApiEnvelope<Lesson>` theo catalog | Query/projection chưa xác nhận. | Mâu thuẫn với endpoint lấy attached resources; xem Q-26-01. |
| 5.1 | data.id | Lesson ID | id | int64 | No | `lessons` — candidate, DESIGN_ONLY | id | 4.1 | Direct candidate mapping | Required theo reusable `Lesson`. | API #26 query chưa xác nhận. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | `lessons` — candidate, DESIGN_ONLY | course_id | 4.1 | Direct candidate mapping | Required theo reusable `Lesson`. | DDL không ghi NOT NULL; xem Q-26-07. |
| 5.3 | data.title | Lesson title | title | string | No | `lessons` — candidate, DESIGN_ONLY | name | 4.1 | `name` → logical `title` | Required theo reusable `Lesson`. | API #26 projection chưa xác nhận. |
| 5.4 | data.content | Lesson content | content | string | Optional | `lessons` — candidate, DESIGN_ONLY | content | 4.1 | Direct candidate mapping | Null/omit rule chưa xác nhận. | Reusable `Lesson` field optional. |
| 5.5 | data.video_url | Video URL | video_url | uri | Optional | `lessons` — candidate, DESIGN_ONLY | video_url | 4.1 | Candidate TEXT → URI | Null/omit/conversion chưa xác nhận. | Reusable `Lesson` field optional. |
| 5.6 | data.order | Lesson order | order | int32 | No | `lessons` — candidate, DESIGN_ONLY | sort_order | 4.1 | `sort_order` → logical `order` | Required theo reusable `Lesson`. | API #26 projection chưa xác nhận. |
| 5.7 | data.status | Lesson status | status | LessonStatus | No | `lessons` — candidate, DESIGN_ONLY | status | 4.1 | Candidate direct mapping | Enum values chưa được liệt kê. | API #26 query/status filter chưa xác nhận. |
| 6 | meta | Metadata | meta | object | No | `ApiEnvelope<T>` schema | meta | 5.1–5.4 | Envelope field | Members unspecified. | API-specific metadata chưa khai báo. |
| 7 | traceId | Trace ID | traceId | uuid | No | `ApiEnvelope<T>` schema | traceId | 5.1–5.4 | Envelope field | Required theo reusable schema. | Runtime trace behavior cho API #26 chưa xác minh. |

> `Resource` fields (`id`, `name`, `type`, `url`, `visibility`, `lesson_id`) không được thêm vào `data` vì API #26 catalog khai báo `Lesson`. ERD/DDL chỉ cung cấp candidate resource columns; chúng chưa xác định response contract.

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Resource retrieved theo catalog; payload projection chưa rõ. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Authentication failure theo contract; trigger runtime chưa xác minh. |
| 403 | DESIGN_ACCESS_DENIED | Role/access denied theo contract; predicate cụ thể chưa rõ. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource not found theo contract; lesson/resource/empty-result condition chưa rõ. |
| 500 | DESIGN_INTERNAL_ERROR | Internal error theo contract. |

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

> Ví dụ chỉ minh họa generic `ApiEnvelope<Lesson>` theo catalog và reusable schema. Nó không xác nhận payload cuối hoặc cách trả resource list; `PUBLISHED` là giá trị ví dụ, không phải enum đầy đủ.

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

> Ví dụ chỉ minh họa HTTP/business code. Catalog không định nghĩa error-specific `data` shape; `data: {}` không phải wire contract.

