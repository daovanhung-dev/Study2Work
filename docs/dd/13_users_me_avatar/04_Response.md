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
| Format | `JSON — response representation cần xác nhận` |
| Character encoding | `TBD — response encoding chưa được contract xác nhận` |
| Content-Type | `TBD — response media type chưa được contract xác nhận` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch: `201/401/403/422/500` | `N/A` | Protocol status, không phải property JSON. |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field. |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch | `N/A` | Dùng `DESIGN_*` code theo contract design. |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Fixed by branch | `TBD — message catalog chưa có` | Không trả raw storage/DB detail. |
| 5 | `data` | User profile | `data` | `object` | `No` | `N/A — profile source chưa có` | `N/A` | `5.1` | `ApiEnvelope<UserProfile>` theo contract | `{}` on error | Full profile mapping chưa được source xác nhận trong upload-only flow. |
| 5.1 | `data.id` | User ID | `id` | `int64` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Contract yêu cầu `UserProfile`, nhưng API #13 không có profile query. |
| 5.2 | `data.full_name` | Full name | `full_name` | `string` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự lấy từ `users`. |
| 5.3 | `data.email` | Email | `email` | `email` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Contract type `email`; profile source chưa có. |
| 5.4 | `data.role` | Role | `role` | `string` | `No` | `N/A — token validation only` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Token role dùng authorization, chưa đủ làm full profile source. |
| 5.5 | `data.avatar_url` | Avatar URL | `avatar_url` | `uri` | `Yes` | `Object Storage` | `TBD — storage result field chưa có` | `3.2/5.1` | `SOURCE_REQUIRED — map storage result nếu contract được bổ sung` | `TBD` | Không tự tạo URL hoặc storage-key rule. |
| 5.6 | `data.bio` | Biography | `bio` | `string` | `Yes` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `Omit when no source` | Contract optional; không có source trong API #13 flow. |
| 5.7 | `data.phone` | Phone | `phone` | `string` | `Yes` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `Omit when no source` | Contract optional; không có source trong API #13 flow. |
| 5.8 | `data.status` | Account status | `status` | `string` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự gán `ACTIVE`. |
| 5.9 | `data.created_at` | Created time | `created_at` | `date-time` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự tạo timestamp profile. |
| 5.10 | `data.updated_at` | Updated time | `updated_at` | `date-time` | `No` | `N/A — không reload profile` | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | API #13 không update DB theo plan. |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Empty object | `{}` | Không thêm storage metadata ngoài contract. |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3/5.4` | Request correlation UUID | `TBD — generator chưa được đặc tả` | Envelope field. |

> `ApiEnvelope<UserProfile>` được giữ nguyên theo contract. Do quyết định upload-only, DD không tự reload profile, không tự update `users.avatar_url` và đánh dấu các mapping chưa có source là `SOURCE_REQUIRED`.

## Ví dụ thành công — HTTP 201

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Avatar upload accepted",
  "data": {
    "id": 1001,
    "full_name": "Example Student",
    "email": "student@example.test",
    "role": "STUDENT",
    "avatar_url": "https://storage.example.test/avatar/example-1001.png",
    "status": "ACTIVE",
    "created_at": "2026-09-06T00:00:00Z",
    "updated_at": "2026-09-06T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> Các giá trị profile/storage trong ví dụ chỉ là dữ liệu minh họa để giữ JSON hợp lệ; chúng không xác nhận schema persistence, storage URL hoặc response reload behavior.

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

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/04_Response.md`.
- Sheet logic: `2.Response`.
