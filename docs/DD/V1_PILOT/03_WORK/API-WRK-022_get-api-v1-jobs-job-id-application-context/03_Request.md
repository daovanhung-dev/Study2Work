---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-WRK-022"
api_name: "GET /api/v1/jobs/{jobId}/application-context"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| ---: | --- |
| HTTP method | `GET` |
| URI | `/api/v1/jobs/{jobId}/application-context` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Bearer access token | Authorization | Yes | Bearer access-token | BD §2.2 public authentication. | [S02](./05_Data_Mapping.md#s02) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `jobId` | `jobId` | `string` | Yes | N/A | N/A | Path segment | SOURCE_REQUIRED | N/A | DIRECT from URI. | [S01](./05_Data_Mapping.md#s01) |

## Query parameters

N/A — no query location is source-confirmed.

## Request body

N/A — no complete physical request-body schema is source-confirmed.

## Contract items chưa materialize thành field

| No | Source phrase | Missing contract detail | Handling |
| ---: | --- | --- | --- |
| 1 | N/A | N/A | No additional unmaterialized input phrase detected. |

## Contract source

> → điều kiện đủ, câu hỏi, bản sửa đổi hiện hành, CV mặc định, trạng thái tích hợp minh chứng

## Ví dụ Request data

N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
