---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-INT-004"
api_name: "POST work /internal/v1/evidence-export-results"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| ---: | --- |
| HTTP method | `POST` |
| URI | `/internal/v1/evidence-export-results` |
| Character encoding | `UTF-8` |
| Content-Type | SOURCE_REQUIRED — protocol-specific carrier. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Service authentication | SOURCE_REQUIRED | Yes | mTLS + service JWT/signature | Internal convention confirms the mechanisms, not a named carrier. | [S02](./05_Data_Mapping.md#s02) |

## Path parameters

N/A — endpoint has no path placeholder.

## Query parameters

N/A — no query location is source-confirmed.

## Request body

N/A — no complete physical request-body schema is source-confirmed.

## Contract items chưa materialize thành field

| No | Source phrase | Missing contract detail | Handling |
| ---: | --- | --- | --- |
| 1 | ID yêu cầu/đơn ứng tuyển, từng mục / + ảnh chụp/mã kiểm tra/mã lý do an toàn tối thiểu bất biến | Physical key, location, type or rule | `SOURCE_REQUIRED`; not included in JSON example. |

## Contract source

> ID yêu cầu/đơn ứng tuyển, từng mục `READY`/`UNAVAILABLE` + ảnh chụp/mã kiểm tra/mã lý do an toàn tối thiểu bất biến

## Ví dụ Request data

N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
