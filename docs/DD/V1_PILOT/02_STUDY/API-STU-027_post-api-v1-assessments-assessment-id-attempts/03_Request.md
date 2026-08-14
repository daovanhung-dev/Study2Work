---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: "markdown"
dd_id: "API-STU-027"
api_name: "POST /api/v1/assessments/{assessmentId}/attempts"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| ---: | --- |
| HTTP method | `POST` |
| URI | `/api/v1/assessments/{assessmentId}/attempts` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Bearer access token | Authorization | Yes | Bearer access-token | BD §2.2 public authentication. | [S02](./05_Data_Mapping.md#s02) |
| 2 | Idempotency key | Idempotency-Key | Yes | 16–128 random characters | BD §2.4. | [S05](./05_Data_Mapping.md#s05) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `assessmentId` | `assessmentId` | `string` | Yes | N/A | N/A | Path segment | SOURCE_REQUIRED | N/A | DIRECT from URI. | [S01](./05_Data_Mapping.md#s01) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `draftVersion` | `draftVersion` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | DIRECT physical key; source does not lock complete type/location validation. | [S01](./05_Data_Mapping.md#s01) |

## Request body

N/A — no complete physical request-body schema is source-confirmed.

## Contract items chưa materialize thành field

| No | Source phrase | Missing contract detail | Handling |
| ---: | --- | --- | --- |
| 1 | tùy chọn; cho phép tải tin trực tiếp theo loại; đồng ý nộp | Physical key, location, type or rule | `SOURCE_REQUIRED`; not included in JSON example. |

## Contract source

> `draftVersion` tùy chọn; cho phép tải tin trực tiếp theo loại; đồng ý nộp → lượt làm/kết quả bất biến

## Ví dụ Request data

N/A — a complete physical JSON request is not sufficiently source-confirmed for this Draft DD.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/03_Request.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `1.Request`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
