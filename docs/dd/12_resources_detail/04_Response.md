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
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch: `200/404/500` | `N/A` | Protocol status, không phải property JSON. |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field. |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `N/A` | Dùng `DESIGN_*` code theo list_api.md. |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | Text chưa có message catalog | Không trả raw SQL/stack trace. |
| 5 | `data` | Resource data | `data` | `object` | `No` | `resources` | `N/A` | `5.1` | Map `Resource` | `{}` on error | `ApiEnvelope<Resource>`. |
| 5.1 | `data.id` | Resource ID | `id` | `int64` | `No` | `resources` | `id` | `4.1` | Direct mapping | `N/A` | |
| 5.2 | `data.name` | Resource name | `name` | `string` | `No` | `resources` | `name` | `4.1` | Direct mapping | `N/A` | |
| 5.3 | `data.type` | Resource type | `type` | `ResourceType` | `No` | `resources` | `resource_type` | `4.1` | Alias `resource_type` → `type` | `N/A` | Enum catalog chưa được đặc tả. |
| 5.4 | `data.url` | Resource URL | `url` | `uri` | `Yes` | `resources` / Object Storage | `url` / signer result | `4.1/4.2` | Direct URL hoặc signed URL map vào cùng field | `null` nếu source URL là `NULL` và không có signer result | Contract không có field `signed_url`; ERD ghi `url NOT NULL`. |
| 5.5 | `data.visibility` | Resource visibility | `visibility` | `ResourceVisibility` | `No` | `N/A — source missing` | `N/A` | `5.1` | `TBD — không suy ra từ URL` | `TBD — contract required` | ERD không có `resources.visibility`. |
| 5.6 | `data.lesson_id` | Lesson ID | `lesson_id` | `int64` | `Yes` | `resources` | `lesson_id` | `4.1` | Direct mapping | `null` khi source là `NULL` | Contract optional; ERD ghi FK `NOT NULL`. |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | Không thêm expiry field khi contract chưa định nghĩa. |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Request correlation UUID | Generator chưa đặc tả | |

> `data.url` chứa URL trực tiếp hoặc signed URL do Object Storage signer trả về. Không thêm `data.signed_url`.
>
> `data.visibility` được giữ trong contract mapping nhưng chưa có source; không tự tạo giá trị enum hoặc cột DB.
>
> `HTTPStatus` là protocol status, không phải property JSON.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Resource metadata retrieved",
  "data": {
    "id": 9001,
    "name": "Course reference PDF",
    "type": "DOCUMENT",
    "url": "https://cdn.example.test/signed/resources/9001.pdf?expires=1760000000",
    "visibility": "<TBD — resources.visibility chưa có source>",
    "lesson_id": 1001
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> Chuỗi `<TBD ...>` trong ví dụ chỉ là placeholder design-only để giữ JSON hợp lệ; không phải runtime enum value.

## Ví dụ lỗi không tìm thấy — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Resource not found",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi hệ thống — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Resource could not be retrieved",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/04_Response.md`.
- Sheet logic: `2.Response`.
