---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/operations/{operation_id} |
| Character encoding | UTF-8 |
| Content-Type | N/A — GET không có request body |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Catalog requires Bearer JWT; exact claim-to-owner mapping is unresolved. | 05_Data_Mapping.md, step 0 |
| 2 | Content type | Content-Type | No | N/A — no request body | No JSON request body is sent. | 05_Data_Mapping.md, step 1 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Operation ID | operation_id | DISCREPANCY: int64 in API row; UUID in shared convention, Operation.id and AC diagrams | Yes | N/A — not specified | N/A — not specified | Path segment; scalar format unresolved | N/A — type conflict | N/A | Identifies the Operation to retrieve. A canonical accepted type must be approved before implementation. | 05_Data_Mapping.md, steps 1.1–1.2 |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | The catalog declares no query parameters. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET endpoint has no request body. | N/A |

> Do not add owner_id, user_id, status filters or other inputs that are absent from the catalog.

## Ví dụ Request data

~~~http
GET /api/v1/operations/{operation_id} HTTP/1.1
Host: api.example.test
Authorization: Bearer <token>
~~~

The route placeholder is not a concrete ID example. Replace it only after the owner resolves the int64/UUID conflict.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md.
- Sheet logic: 1.Request.
