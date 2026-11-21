---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các nhánh dưới đây phản ánh API #18 current source và catalog đã reconcile cho SH-07: role không được phép là 403; missing hoặc non-owner operation là 404.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Credential is missing or invalid per common catalog error definition. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — no message ID in catalog | 0.1/0.3 | No | API #18 requires Bearer JWT. Token parsing details are not specified here. |
| 2 | Authorization | Yes | Role | Caller role is not Student, Mentor or Admin. | 403 | DESIGN_ACCESS_DENIED | N/A — no message ID in catalog | 0.1/0.3 | No | A supported role still must own the operation. |
| 3 | Not found | Yes | Owner-bound Operation | Requested operation does not exist or is not owned by the authenticated caller. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — no message ID in catalog | 2.1/4.4 | No | Missing and wrong-owner cases share the response to avoid disclosing another owner's operation. |
| 4 | System error | No | Operation lookup | Unexpected query or processing failure. | 500 | DESIGN_INTERNAL_ERROR | N/A — no message ID in catalog | 4.2 | No | Do not expose raw database or stack details. |

> API #18 does not list 422, 409 or 503. Do not add them without an approved catalog/diagram change.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.
