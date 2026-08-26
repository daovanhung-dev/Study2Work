---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Request"
format: markdown
---

# Request

## 1. HTTP request

```http
PUT /api/v1/attempts/{attempt_id}/answers
```

## 2. Header / authentication

| Header | Required | Rule |
|---|---|---|
| `Authorization: Bearer <token>` | `Yes` | Theo actor/precondition của AC; Guest flow không mặc định yêu cầu token. |
| `Content-Type: application/json` | `Yes` | Chỉ áp dụng khi request body JSON được dùng; upload có thể dùng media type khác và được để TBD nếu AC không khóa. |

## 3. Path parameters

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| `attempt_id` | Path | `TBD` | Required | Identifier from endpoint path; exact type/validation not specified by index |

## 4. Query parameters

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| N/A / TBD | Query | - | - | Không có query field explicit trong evidence đã khóa; không suy diễn. |

## 5. Request body

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| `TBD / SOURCE_REQUIRED` | Body | - | - | Activity/API index không khóa field-level body; không tự tạo schema. |

## 6. Validation policy

- Chỉ validation được Activity Diagram ghi explicit mới được coi là contract.
- Type, length, enum, regex hoặc required flag chưa có nguồn được ghi `TBD`; không suy diễn từ thói quen REST.
