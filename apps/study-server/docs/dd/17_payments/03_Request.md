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
| HTTP method | POST |
| URI | /api/v1/payments |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Content type | Content-Type | Yes | application/json | JSON request body theo contract | [05_Data_Mapping.md](./05_Data_Mapping.md#11-get-request-header) |
| 2 | Authorization | Authorization | Yes | Bearer JWT | Student authentication theo contract | [05_Data_Mapping.md](./05_Data_Mapping.md#11-get-request-header) |

## Path parameters

- N/A — endpoint không khai báo path parameter.

## Query parameters

- N/A — endpoint không khai báo query parameter.

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Order ID | order_id | int64 | Yes | N/A — not declared | N/A — not declared | N/A | Integer | N/A — contract does not specify range beyond int64 | N/A | Logical Order cần khởi tạo/xác nhận thanh toán | [05_Data_Mapping.md](./05_Data_Mapping.md#12-get-request-data) |
| 2 | Payment provider | provider | string | Yes | N/A — not declared | N/A — not declared | N/A | String | SOURCE_REQUIRED — provider allowlist chưa được công bố | N/A | Provider gửi cùng request; mapping/continuity với API #16 chưa chốt | [05_Data_Mapping.md](./05_Data_Mapping.md#12-get-request-data) |

> Không tự thêm positive-number, max-length, case-normalization, enum allowlist hoặc unknown-field rule khi contract chưa khai báo.

## Ví dụ Request data

Ví dụ chỉ minh họa JSON shape. SOURCE_REQUIRED không phải provider value hợp lệ; thay bằng giá trị do owner phê duyệt trước khi sử dụng request thực tế.

~~~json
{
  "order_id": 123,
  "provider": "<SOURCE_REQUIRED>"
}
~~~

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md.
- Sheet logic: 1.Request.
