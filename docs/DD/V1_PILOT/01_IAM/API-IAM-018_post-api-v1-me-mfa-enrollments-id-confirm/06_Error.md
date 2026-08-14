---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: "markdown"
dd_id: "API-IAM-018"
api_name: "POST /api/v1/me/mfa/enrollments/{id}/confirm"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Codes are copied only from endpoint/error catalog. HTTP status is source-confirmed only when a source maps it; otherwise it is SOURCE_REQUIRED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Endpoint business/error code | DIRECT | `MFA_CODE_INVALID` | As specified by API catalog. | `SOURCE_REQUIRED` | `MFA_CODE_INVALID` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L104` |
| 2 | Endpoint business/error code | DIRECT | `MFA_ENROLLMENT_EXPIRED` | As specified by API catalog. | `SOURCE_REQUIRED` | `MFA_ENROLLMENT_EXPIRED` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L104` |

## Global safety rules

- Do not disclose tenant/resource existence across unauthorized scope.
- Do not return stack trace, raw SQL, passwords, tokens, secrets or unsafe PII.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/06_Error.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `4.Error`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
