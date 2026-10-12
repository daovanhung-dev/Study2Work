---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
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
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4.1/4.2/4.3/4.4 | Fixed by branch: 200/401/403/422/500 | N/A | Protocol status from catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4.1/4.2/4.3/4.4 | true on success; false on error | N/A | ApiEnvelope<T> field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4.1/4.2/4.3/4.4 | Fixed by branch | N/A | Exact design codes are listed below. |
| 4 | message | Message | message | string | No | N/A | N/A | 4.1/4.2/4.3/4.4 | Branch message | Exact text not specified | Do not treat sample text as message catalog. |
| 5 | data | UserProfile | data | object | No on success | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | ApiEnvelope<UserProfile> per catalog | Exact null/empty rule not specified | DISCREPANCY: AC-13 requires a course list, but catalog type is UserProfile. |
| 5.1 | data.id | User ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Required by schema | No confirmed mapping from the Enrollment/Course query. |
| 5.2 | data.full_name | Full name | full_name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Required by schema | No confirmed mapping from the Enrollment/Course query. |
| 5.3 | data.email | Email | email | email | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Required by schema | No confirmed mapping from the Enrollment/Course query. |
| 5.4 | data.role | User role | role | UserRole | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Required by schema | Enum values not declared in this contract row. |
| 5.5 | data.avatar_url | Avatar URL | avatar_url | uri | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Optional field; null/omit behavior unspecified | No confirmed mapping from the Enrollment/Course query. |
| 5.6 | data.bio | Biography | bio | string | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Optional field; null/omit behavior unspecified | No confirmed mapping from the Enrollment/Course query. |
| 5.7 | data.phone | Phone | phone | string | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Optional field; null/omit behavior unspecified | No confirmed mapping from the Enrollment/Course query. |
| 5.8 | data.status | User status | status | UserStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | Per UserProfile schema | Required by schema | Enum values not declared in this contract row. |
| 5.9 | data.created_at | Created time | created_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | ISO-8601 per schema | Required by schema | No confirmed mapping from the Enrollment/Course query. |
| 5.10 | data.updated_at | Updated time | updated_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1/4.1 | ISO-8601 per schema | Required by schema | No confirmed mapping from the Enrollment/Course query. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4.1/4.2/4.3/4.4 | ApiEnvelope metadata | Object content unspecified | Page metadata is not declared for API #20. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4.1/4.2/4.3/4.4 | ApiEnvelope trace ID | Required by shared schema | Current runtime envelope also returns traceId; endpoint #20 is unwired. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Retrieved resource |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT is missing or invalid |
| 403 | DESIGN_ACCESS_DENIED | Role/access denied |
| 422 | DESIGN_VALIDATION_ERROR | Request validation error |
| 500 | DESIGN_INTERNAL_ERROR | Internal error |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 1001,
    "full_name": "Student Example",
    "email": "student@example.test",
    "role": "Student",
    "status": "ACTIVE",
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> Đây là ví dụ theo schema UserProfile đang được catalog tham chiếu, không phải ví dụ payload Course. Mismatch với AC-13 còn mở; message chỉ là placeholder được giải thích, không phải approved message.

## Ví dụ lỗi — HTTP 401

~~~json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Message text is not specified by the contract.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

> Ví dụ minh họa envelope hiện hành; contract không chốt message text hoặc error metadata cụ thể.

---
## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
