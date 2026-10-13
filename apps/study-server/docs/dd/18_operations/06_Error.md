---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các error code dưới đây được khai báo trực tiếp trong API #18 row của list_api.md. Điều kiện sở hữu Operation và cách phân biệt 403 với 404 chưa được contract khóa; không tạo thêm status hoặc business code.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Credential is missing or invalid per common catalog error definition. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — no message ID in catalog | 0.1/0.3 | No | API #18 requires Bearer JWT. Token parsing details are not specified here. |
| 2 | Authorization | Yes | Operation access | Access is denied under the approved role/ownership rule. | 403 | DESIGN_ACCESS_DENIED | N/A — no message ID in catalog | 0.1/0.3 | No | Owner versus owner/Admin policy and caller identity mapping are unresolved. |
| 3 | Not found | Yes | Operation | Requested Operation cannot be found. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — no message ID in catalog | 2.1/4.4 | No | Catalog lists the code for a missing resource/operation; hiding non-owner records as 404 is unresolved. |
| 4 | System error | No | Operation lookup | Unexpected query or processing failure. | 500 | DESIGN_INTERNAL_ERROR | N/A — no message ID in catalog | 4.2 | No | Do not expose raw database or stack details. |

> API #18 does not list 422, 409 or 503. Do not add them without an approved catalog/diagram change.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.
