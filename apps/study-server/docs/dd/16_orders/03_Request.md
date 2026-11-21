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
| HTTP method | `POST` |
| URI | `/api/v1/orders` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Content type | `Content-Type` | Yes | `application/json` | JSON request body theo contract | [05_Data_Mapping.md](./05_Data_Mapping.md#11-get-request-header) |
| 2 | Authorization | `Authorization` | Yes | `Bearer <JWT>` | Student authentication theo contract | [05_Data_Mapping.md](./05_Data_Mapping.md#11-get-request-header) |

## Path parameters

- N/A — endpoint không khai báo path parameter.

## Query parameters

- N/A — endpoint không khai báo query parameter.

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Course ID | `course_id` | `int64` | Yes | N/A — not declared | N/A — not declared | N/A | Integer | N/A — contract does not specify range beyond int64 | N/A | Course cần tạo Order | [05_Data_Mapping.md](./05_Data_Mapping.md#12-get-request-data) |
| 2 | Payment provider | `payment_provider` | `PaymentProvider` | Yes | N/A — not declared | N/A — not declared | N/A | Enum name declared; member values SOURCE_REQUIRED | SOURCE_REQUIRED — enum values not listed | N/A | Provider field theo request contract; purpose/storage relationship chưa được chốt | [05_Data_Mapping.md](./05_Data_Mapping.md#12-get-request-data) |

> Không thêm rule positive ID, provider allowlist, unknown-field behavior hoặc validation message khi nguồn chưa khai báo.

## Ví dụ Request data

Ví dụ dưới đây chỉ minh họa JSON shape. `<SOURCE_REQUIRED>` không phải giá trị provider hợp lệ; thay bằng enum value đã được phê duyệt trước khi dùng request thực tế.

```json
{
  "course_id": 123,
  "payment_provider": "<SOURCE_REQUIRED>"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md.
- Sheet logic: 1.Request.

