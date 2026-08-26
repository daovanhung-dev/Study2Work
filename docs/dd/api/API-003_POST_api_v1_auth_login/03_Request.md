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
POST /api/v1/auth/login
```

## 2. Header / authentication

| Header | Required | Rule |
|---|---|---|
| `Authorization: Bearer <token>` | `TBD / conditional` | Theo actor/precondition của AC; Guest flow không mặc định yêu cầu token. |
| `Content-Type: application/json` | `Yes` | Chỉ áp dụng khi request body JSON được dùng; upload có thể dùng media type khác và được để TBD nếu AC không khóa. |

## 3. Path parameters

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| N/A | - | - | - | Endpoint không có path parameter. |

## 4. Query parameters

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| N/A / TBD | Query | - | - | Không có query field explicit trong evidence đã khóa; không suy diễn. |

## 5. Request body

| Field | Location | Type | Required | Validation / source |
|---|---|---|---|---|
| `email` | Body | `TBD` | TBD | Explicitly named in AC flow |
| `password` | Body | `TBD` | TBD | Explicitly named in AC flow |

## 6. Validation policy

- Chỉ validation được Activity Diagram ghi explicit mới được coi là contract.
- Type, length, enum, regex hoặc required flag chưa có nguồn được ghi `TBD`; không suy diễn từ thói quen REST.
