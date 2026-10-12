---
title: "Response"
order: 4
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
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
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4.1/4.2/4.3 | Fixed by branch: 200/401/403/500 | N/A | Statuses from API #21 catalog; no 422 is declared. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4.1/4.2/4.3 | true on success; false on error | N/A | ApiEnvelope<T> reusable schema; API #21 is not runtime-wired. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4.1/4.2/4.3 | Fixed by branch | N/A | Preserve DESIGN_* codes from catalog. |
| 4 | message | Message | message | string | No | N/A | N/A | 4.1/4.2/4.3 | SOURCE_REQUIRED | N/A | Exact message text is not in the API contract. |
| 5 | data | UserProfile | data | object | No on success | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | ApiEnvelope<UserProfile> per catalog | Success null/empty rule unspecified | DISCREPANCY: progress data in AC-13/AC-18 has no matching declared schema. |
| 5.1 | data.id | User ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Required by schema | No API #21 mapping established. |
| 5.2 | data.full_name | Full name | full_name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Required by schema | No API #21 mapping established. |
| 5.3 | data.email | Email | email | email | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Required by schema | No API #21 mapping established. |
| 5.4 | data.role | User role | role | UserRole | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Required by schema | UserRole values are not enumerated in the reusable schema row. |
| 5.5 | data.avatar_url | Avatar URL | avatar_url | uri | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Null/omit behavior unspecified | No API #21 mapping established. |
| 5.6 | data.bio | Biography | bio | string | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Null/omit behavior unspecified | No API #21 mapping established. |
| 5.7 | data.phone | Phone | phone | string | Optional | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Null/omit behavior unspecified | No API #21 mapping established. |
| 5.8 | data.status | User status | status | UserStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | Per reusable UserProfile schema | Required by schema | UserStatus values are not enumerated in the reusable schema row. |
| 5.9 | data.created_at | Created time | created_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | ISO-8601 per schema | Required by schema | No API #21 mapping established. |
| 5.10 | data.updated_at | Updated time | updated_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3/4.1 | ISO-8601 per schema | Required by schema | No API #21 mapping established. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4.1/4.2/4.3 | ApiEnvelope metadata | Object fields unspecified | No pagination or aggregation metadata is declared. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4.1/4.2/4.3 | ApiEnvelope trace ID | Required by schema | Runtime API #21 trace behavior is not verified. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Retrieved resource |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT is missing or invalid |
| 403 | DESIGN_ACCESS_DENIED | Role/access denied |
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
    "created_at": "2026-10-11T10:00:00Z",
    "updated_at": "2026-10-11T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> Ví dụ chỉ minh họa ApiEnvelope<UserProfile> theo catalog, không phải progress payload đã được xác nhận. Giá trị enum và message là minh họa; UserRole/UserStatus values và message catalog chưa được đặc tả tại contract này.

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

> Envelope minh họa theo ApiEnvelope<T>; message text và error metadata không được API #21 contract chốt.

---
## Phụ lục đối chiếu template Markdown

- Template: [04_Response.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md).
- Sheet nguồn: 2.Response.
