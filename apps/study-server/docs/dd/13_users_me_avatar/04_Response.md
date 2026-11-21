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
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch: `201/401/403/422/500` | `N/A` | Protocol status, không phải property JSON. |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field. |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch | `N/A` | Dùng `DESIGN_*` code theo contract design. |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch | `Avatar upload accepted` or safe error message | Không trả raw storage detail. |
| 5 | `data` | Avatar upload result | `data` | `object` | `No` | `Object Storage public URL` | `N/A` | `5.1` | `ApiEnvelope<AvatarUploadResult>` | `{}` on error | Thành công chỉ gồm `avatar_url`; không trả UserProfile. |
| 5.1 | `data.avatar_url` | Public avatar URL | `avatar_url` | `uri` | `No` | `Object Storage` | `OBJECT_STORAGE_PUBLIC_BASE_URL + /avatars/{user_id}` | `3.2/5.1` | URL ghép từ public base URL và object key đã upload | Present after successful upload | `AvatarUploadResult` chỉ có field này. |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Empty object | `{}` | Không thêm storage metadata ngoài contract. |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `5.1-5.5` | Request correlation UUID từ middleware | Always present | Envelope field. |

> API #13 chỉ trả URL upload. API #14 vẫn nhận `avatar_url` để cập nhật profile trong bước kế tiếp của AC-11.

## Ví dụ thành công — HTTP 201

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Avatar upload accepted",
  "data": {
    "avatar_url": "https://storage.example.test/avatars/1001"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> URL trong ví dụ là giá trị minh họa; runtime dựng URL từ cấu hình public base URL và `avatars/{user_id}`.

## Ví dụ lỗi — HTTP 401

```json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required",
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
  "message": "Access denied",
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
  "message": "Avatar input is invalid",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000004"
}
```

## Ví dụ lỗi — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Avatar could not be uploaded",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000005"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md`.
- Sheet logic: `2.Response`.
