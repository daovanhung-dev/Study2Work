---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các status/business-code pair dưới đây được khai báo trong API #19 row của list_api.md. Điều kiện chính xác của resource-not-found và state-conflict chưa được chốt; không bổ sung status hoặc business code mới.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Credential is missing or invalid. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — no message ID in catalog | 0.1/0.3 | No | Exact token failure mapping follows the shared auth boundary; API #19 is unwired. |
| 2 | Authorization | Yes | Student role/access | Caller role or access is denied. | 403 | DESIGN_ACCESS_DENIED | N/A — no message ID in catalog | 0.1/0.3 | No | API catalog requires role=Student; ownership/access details are otherwise unspecified. |
| 3 | Not found | Yes | Resource required by API #19 | Required resource cannot be resolved. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — no message ID in catalog | 2.1/3/5.2 | No | Exact missing resource and direct-call lookup semantics need confirmation. |
| 4 | Validation | Yes | Request fields | Request fails a supported required/type validation. | 422 | DESIGN_VALIDATION_ERROR | N/A — no message ID in catalog | 1.1–1.3/5.2 | No | Keep path/body course_id and JWT identity ambiguities open; do not invent range rules. |
| 5 | State conflict | Yes | Enrollment state | Request conflicts with the approved enrollment state/duplicate rule. | 409 | DESIGN_STATE_CONFLICT | N/A — no message ID in catalog | 2.2/3/4.3/5.2 | TBD — conflict timing unresolved | AC-12 requests anti-duplicate behavior; the exact predicate and concurrency guarantee are SOURCE_REQUIRED. |
| 6 | System/transaction | No | Enrollment/Progress mutation | Unexpected processing or database failure. | 500 | DESIGN_INTERNAL_ERROR | N/A — no message ID in catalog | 4.1–4.3/5.2 | Yes after transaction begins | Error envelope uses current shared response shape; database details must not be exposed. |

> API #19 contract does not list 400, 503 or additional business codes. Do not add them without an approved contract change.

---
## Template reference

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.

