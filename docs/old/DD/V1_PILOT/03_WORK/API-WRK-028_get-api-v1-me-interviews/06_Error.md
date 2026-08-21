---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: "markdown"
dd_id: "API-WRK-028"
api_name: "GET /api/v1/me/interviews"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Codes are copied only from endpoint/error catalog. HTTP status is source-confirmed only when a source maps it; otherwise it is SOURCE_REQUIRED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SOURCE_REQUIRED | N/A | N/A | Endpoint row does not name a dedicated business code. | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | [S05](./05_Data_Mapping.md#s05) | No | Global failure/safety rules still apply. |

## Global safety rules

- Do not disclose tenant/resource existence across unauthorized scope.
- Do not return stack trace, raw SQL, passwords, tokens, secrets or unsafe PII.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/06_Error.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `4.Error`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
