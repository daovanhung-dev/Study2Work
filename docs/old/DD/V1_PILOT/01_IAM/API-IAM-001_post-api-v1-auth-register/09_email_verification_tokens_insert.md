---
title: "Định nghĩa table"
order: 9
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: "markdown"
dd_id: "API-IAM-001"
api_name: "POST /api/v1/auth/register"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
| ---: | --- |
| Physical table | `email_verification_tokens` |
| Logical table | `TBL-IAM-004` |
| Operation | `INSERT` |
| Data Mapping step | [S05](./05_Data_Mapping.md#s05) |

## Mutation mapping

> SOURCE_REQUIRED — catalog names this table in a mutation flow but does not provide per-column setting/value mapping. This file deliberately does not invent one.

| No | Physical column | Logical name | Type | Remarks |
| ---: | --- | --- | --- | --- |
| 1 | `SOURCE_REQUIRED` | No individual column named in source | `SOURCE_REQUIRED` | Do not invent a column mapping. |

## Schema source

- [03_THIET_KE_CO_SO_DU_LIEU.md](../../../../BD/03_THIET_KE_CO_SO_DU_LIEU.md): `L125`.
- Endpoint source: `docs/BD/04_DAC_TA_API.md:L87`.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/09_email_verification_tokens_insert.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `table`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
