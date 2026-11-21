---
title: "Response"
order: 4
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---
# Response

## Format

| Thuộc tính       | Giá trị        |
| ------------------ | ---------------- |
| Format             | JSON             |
| Character encoding | UTF-8            |
| Content-Type       | application/json |

## Response fields

|  No | Path           | Logical name   | Physical name | Type         | Nullable                                       | Source table                      | Source column   | Source step | Transform                                             | Null/empty/omit rule           | Remarks                                                    |
| --: | -------------- | -------------- | ------------- | ------------ | ---------------------------------------------- | --------------------------------- | --------------- | ----------- | ----------------------------------------------------- | ------------------------------ | ---------------------------------------------------------- |
|   1 | HTTPStatus     | HTTP status    | HTTPStatus    | integer      | No                                             | N/A                               | N/A             | 4.1–4.4    | Fixed by branch: 200/401/403/404/500                  | N/A                            | Transport status; status-specific code is in businessCode. |
|   2 | success        | Success flag   | success       | boolean      | No                                             | ApiEnvelope<T></t> schema         | success         | 4.1–4.4    | true on success; false on error per reusable envelope | N/A                            | API #22 runtime serialization is not verified.             |
|   3 | businessCode   | Business code  | businessCode  | string       | No                                             | API catalog                       | N/A             | 4.1–4.4    | Fixed by branch                                       | N/A                            | Preserve codes declared for API #22.                       |
|   4 | message        | Message        | message       | string       | No                                             | SOURCE_REQUIRED                   | SOURCE_REQUIRED | 4.1–4.4    | SOURCE_REQUIRED                                       | N/A                            | Exact message text is not specified.                       |
|   5 | data           | Lesson         | data          | object       | Required by `ApiEnvelope<Lesson>` on success | API catalog schema                | N/A             | 3/4.1       | `Lesson` generic payload                            | Error-branch shape unspecified | Keep the declared generic type; do not add access fields.  |
| 5.1 | data.id        | Lesson ID      | id            | int64        | No                                             | lessons — candidate, DESIGN_ONLY | id              | 3/4.1       | Direct candidate mapping                              | Required by Lesson schema      | API #22 selection/query is not confirmed.                  |
| 5.2 | data.course_id | Course ID      | course_id     | int64        | No                                             | lessons — candidate, DESIGN_ONLY | course_id       | 3/4.1       | Direct candidate mapping                              | Required by Lesson schema      | Parent relationship is design evidence only.               |
| 5.3 | data.title     | Lesson title   | title         | string       | No                                             | lessons — candidate, DESIGN_ONLY | name            | 3/4.1       | `name` maps to logical `title` in DB design       | Required by Lesson schema      | API #22 selection/query is not confirmed.                  |
| 5.4 | data.content   | Lesson content | content       | string       | Optional                                       | lessons — candidate, DESIGN_ONLY | content         | 3/4.1       | Direct candidate mapping                              | Null/omit behavior unspecified | Optional in reusable Lesson schema.                        |
| 5.5 | data.video_url | Video URL      | video_url     | uri          | Optional                                       | lessons — candidate, DESIGN_ONLY | video_url       | 3/4.1       | Direct candidate mapping                              | Null/omit behavior unspecified | Optional in reusable Lesson schema.                        |
| 5.6 | data.order     | Lesson order   | order         | int32        | No                                             | lessons — candidate, DESIGN_ONLY | sort_order      | 3/4.1       | `sort_order` maps to logical `order` in DB design | Required by Lesson schema      | API #22 selection/query is not confirmed.                  |
| 5.7 | data.status    | Lesson status  | status        | LessonStatus | No                                             | lessons — candidate, DESIGN_ONLY | status          | 3/4.1       | Direct candidate mapping                              | Required by Lesson schema      | Enum values are not enumerated in the contract.            |
|   6 | meta           | Metadata       | meta          | object       | No                                             | ApiEnvelope<T></t> schema         | meta            | 4.1–4.4    | Object per reusable envelope                          | Members unspecified            | API #22 declares no pagination metadata.                   |
|   7 | traceId        | Trace ID       | traceId       | uuid         | No                                             | ApiEnvelope<T></t> schema         | traceId         | 4.1–4.4    | UUID per reusable envelope                            | Required by schema             | API #22 runtime trace behavior is not verified.            |

## Business code by status

| HTTP status | Business code                  | Contract meaning                                                                                    |
| ----------: | ------------------------------ | --------------------------------------------------------------------------------------------------- |
|         200 | DESIGN_RESOURCE_RETRIEVED      | Retrieved resource.                                                                                 |
|         401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT missing or invalid.                                                                      |
|         403 | DESIGN_ACCESS_DENIED           | Role or access denied; AC-14 diagram says denial includes a reason, whose wire shape is unresolved. |
|         404 | DESIGN_RESOURCE_NOT_FOUND      | Resource not found; API-specific resource condition is unresolved.                                  |
|         500 | DESIGN_INTERNAL_ERROR          | Internal error.                                                                                     |

## Ví dụ thành công — HTTP 200

```json
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
    "status": "<LessonStatus>"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> JSON minh họa schema `ApiEnvelope<Lesson>`. Message và giá trị `<LessonStatus>` là placeholder; example không quy định status visibility hay access predicate.

## Ví dụ lỗi — HTTP 403

```json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Message text and reason shape are not specified by the contract.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

> Envelope lỗi và `data: {}` chỉ là sơ đồ JSON để minh họa code HTTP/business đã khai báo. Catalog chưa định nghĩa error payload; AC-14 chỉ yêu cầu “lý do” mà chưa nêu field hoặc vị trí. Không dùng ví dụ này làm wire contract.

---

## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
