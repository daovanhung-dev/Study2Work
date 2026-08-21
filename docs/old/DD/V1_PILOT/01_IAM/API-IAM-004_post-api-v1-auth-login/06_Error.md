---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: "markdown"
dd_id: "API-IAM-004"
api_name: "POST /api/v1/auth/login"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Codes are copied only from endpoint/error catalog. HTTP status is source-confirmed only when a source maps it; otherwise it is SOURCE_REQUIRED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Endpoint business/error code | DIRECT | `INVALID_CREDENTIALS` | As specified by API catalog. | `401` | `INVALID_CREDENTIALS` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |
| 2 | Endpoint business/error code | DIRECT | `EMAIL_NOT_VERIFIED` | As specified by API catalog. | `SOURCE_REQUIRED` | `EMAIL_NOT_VERIFIED` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |
| 3 | Endpoint business/error code | DIRECT | `ACCOUNT_SUSPENDED` | As specified by API catalog. | `403` | `ACCOUNT_SUSPENDED` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |
| 4 | Endpoint business/error code | DIRECT | `ACCOUNT_DELETION_PENDING` | As specified by API catalog. | `SOURCE_REQUIRED` | `ACCOUNT_DELETION_PENDING` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |
| 5 | Endpoint business/error code | DIRECT | `CREDENTIAL_TEMP_LOCKED` | As specified by API catalog. | `SOURCE_REQUIRED` | `CREDENTIAL_TEMP_LOCKED` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |
| 6 | Endpoint business/error code | DIRECT | `MFA_REQUIRED` | As specified by API catalog. | `403` | `MFA_REQUIRED` | N/A — no legacy error-message ID in BD. | [S05](./05_Data_Mapping.md#s05) | TBD | `docs/BD/04_DAC_TA_API.md:L90` |

## Global safety rules

- Do not disclose tenant/resource existence across unauthorized scope.
- Do not return stack trace, raw SQL, passwords, tokens, secrets or unsafe PII.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/06_Error.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `4.Error`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
