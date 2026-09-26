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
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` — current Study response convention. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3/6.4/6.5` | Fixed by branch: `200/401/403/422/500` | `N/A` | Protocol status, không phải JSON property. |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3/6.4/6.5` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field. |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3/6.4/6.5` | Fixed by branch | `N/A` | `DESIGN_RESOURCE_UPDATED` on success; `DESIGN_*` on errors. |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3/6.4/6.5` | Fixed by branch | `TBD — message catalog chưa có` | Không trả raw DB/provider detail. |
| 5 | `data` | User profile | `data` | `object` | `No` | `users` | Safe profile projection | `5.1/6.1` | Map thành `UserProfile` | `{}` on error | Full response source bị giới hạn bởi `bio` gap. |
| 5.1 | `data.id` | User ID | `id` | `int64` | `No` | `users` | `id` | `5.1` | Direct mapping | Không omit khi success | Không lấy từ request body. |
| 5.2 | `data.full_name` | Full name | `full_name` | `string` | `No` | `users` | `full_name` | `5.1` | Direct mapping sau update | Không omit khi success | Source-backed column. |
| 5.3 | `data.email` | Email | `email` | `email` | `No` | `users` | `email` | `5.1` | Direct mapping | Không expose password fields | Safe profile projection. |
| 5.4 | `data.role` | Role | `role` | `string` | `No` | `users` | `role` | `5.1` | Direct mapping | Không omit khi success | Role dùng thêm cho authorization. |
| 5.5 | `data.avatar_url` | Avatar URL | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `4.1/5.1` | Direct mapping; URI validation semantics TBD | `null` có thể xảy ra theo current schema; contract semantics TBD | Không tự tạo URL. |
| 5.6 | `data.bio` | Biography | `bio` | `string` | `Yes` | `N/A — source missing` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED`; có thể omit sau decision | Không có `users.bio` trong DB.sql/ERD/current API #4. |
| 5.7 | `data.phone` | Phone | `phone` | `string` | `Yes` | `users` | `phone` | `4.1/5.1` | Direct mapping | `null` có thể xảy ra theo current schema; request requiredness TBD | Contract/schema discrepancy. |
| 5.8 | `data.status` | Account status | `status` | `string` | `No` | `users` | `status` | `5.1` | Direct mapping | Không omit khi success | Không cho request cập nhật status. |
| 5.9 | `data.created_at` | Created time | `created_at` | `date-time` | `No` | `users` | `created_at` | `5.1` | ISO-8601 serialization | Không omit khi success | Không update trong API #14. |
| 5.10 | `data.updated_at` | Updated time | `updated_at` | `date-time` | `No` | `users` | `updated_at` | `4.1/5.1` | ISO-8601 serialization | Không omit khi success | Set by update operation/current timestamp. |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3/6.4/6.5` | Empty object unless approved metadata is added | `{}` | Không thêm field ngoài contract. |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `0.1/6.1/6.2/6.3/6.4/6.5` | Request trace or generated trace | `TBD` only if runtime generator policy changes | Current middleware owns trace propagation. |

> `UserProfile` response giữ contract, nhưng `data.bio` chưa có source. Không dùng `SOURCE_REQUIRED` để ngầm xác nhận một column hoặc runtime mapping.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Profile updated.",
  "data": {
    "id": 1001,
    "full_name": "Nguyen Van A",
    "email": "student@example.test",
    "role": "STUDENT",
    "avatar_url": "https://storage.example.test/avatars/student-1001.png",
    "phone": "+84901234567",
    "status": "ACTIVE",
    "created_at": "2026-09-15T12:00:00Z",
    "updated_at": "2026-09-23T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> `bio` được omit trong ví dụ success vì current source không có response source; đây không phải quyết định loại bỏ field khỏi contract.

## Ví dụ lỗi — HTTP 401

```json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi — HTTP 403

```json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

## Ví dụ lỗi — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Profile input is invalid.",
  "data": {},
  "meta": {
    "fieldErrors": [
      {
        "field": "full_name",
        "code": "INVALID_VALUE",
        "message": "full_name is invalid."
      }
    ]
  },
  "traceId": "00000000-0000-0000-0000-000000000004"
}
```

## Ví dụ lỗi — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Profile could not be updated.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000005"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md`.
- Sheet logic: `2.Response`.

