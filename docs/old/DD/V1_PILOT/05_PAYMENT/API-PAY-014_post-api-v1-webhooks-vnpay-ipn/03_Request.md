---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-PAY-014"
api_name: "POST /api/v1/webhooks/vnpay/ipn"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| ---: | --- |
| HTTP method | `POST` |
| URI | `/api/v1/webhooks/vnpay/ipn` |
| Character encoding | `UTF-8` |
| Content-Type | SOURCE_REQUIRED — provider-specific inbound webhook carrier. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Provider signature/authentication | SOURCE_REQUIRED | Yes | SOURCE_REQUIRED — provider-specific signature and optional IP allowlist | Inbound webhook; exact header/query/form carrier and canonical signing input are not locked by the endpoint row. | [S02](./05_Data_Mapping.md#s02) |
| 2 | Idempotency key | Idempotency-Key | Yes | 16–128 random characters | BD §2.4. | [S05](./05_Data_Mapping.md#s05) |

## Path parameters

N/A — endpoint has no path placeholder.

## Query parameters

N/A — no query location is source-confirmed.

## Request body

N/A — no complete physical request-body schema is source-confirmed.

## Contract items chưa materialize thành field

| No | Source phrase | Missing contract detail | Handling |
| ---: | --- | --- | --- |
| 1 | Truy vấn/biểu mẫu gốc đúng theo nhà cung cấp | Physical key, location, type or rule | `SOURCE_REQUIRED`; not included in JSON example. |

## Contract source

> Truy vấn/biểu mẫu gốc đúng theo nhà cung cấp → xác nhận theo yêu cầu nhà cung cấp

## Ví dụ Request data

N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
