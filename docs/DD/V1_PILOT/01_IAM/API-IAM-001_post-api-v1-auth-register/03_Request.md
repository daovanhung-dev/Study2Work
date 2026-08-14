---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-IAM-001"
api_name: "POST /api/v1/auth/register"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| ---: | --- |
| HTTP method | `POST` |
| URI | `/api/v1/auth/register` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Idempotency key | Idempotency-Key | Yes | 16–128 random characters | BD §2.4. | [S05](./05_Data_Mapping.md#s05) |

## Path parameters

N/A — endpoint has no path placeholder.

## Query parameters

N/A — no query location is source-confirmed.

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `email` | `email` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | DIRECT physical key; source does not lock complete type/location validation. | [S01](./05_Data_Mapping.md#s01) |

## Contract items chưa materialize thành field

| No | Source phrase | Missing contract detail | Handling |
| ---: | --- | --- | --- |
| 1 | Phần thân , mật khẩu 12–128 ký tự, phiên bản thỏa thuận, ngôn ngữ; email chuẩn hóa/không phân biệt hoa thường | Physical key, location, type or rule | `SOURCE_REQUIRED`; not included in JSON example. |

## Contract source

> Phần thân `email`, mật khẩu 12–128 ký tự, phiên bản thỏa thuận, ngôn ngữ; email chuẩn hóa/không phân biệt hoa thường → người dùng chờ xác minh và `verificationExpiresAt`

## Ví dụ Request data

N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
