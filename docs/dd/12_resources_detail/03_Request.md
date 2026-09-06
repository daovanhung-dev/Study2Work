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
| HTTP method | `GET` |
| URI | `/api/v1/resources/{resource_id}` |
| Character encoding | `UTF-8` |
| Content-Type | `N/A — request không có body` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `No` | `N/A — public endpoint` | Không yêu cầu Bearer token theo contract. | [`0.1`](./05_Data_Mapping.md#01-public-endpoint) |
| 2 | Accept | `Accept` | `No` | `application/json` | Client có thể yêu cầu JSON response. | [`1.2`](./05_Data_Mapping.md#12-get-request-header) |
| 3 | Content type | `Content-Type` | `No` | `N/A — không có request body` | GET endpoint không nhận body. | [`1.2`](./05_Data_Mapping.md#12-get-request-header) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Resource ID | `resource_id` | `int64` | `Yes` | `N/A — chưa đặc tả` | `N/A — chưa đặc tả` | Integer path segment | `N/A` | `N/A` | ID của resource cần lấy metadata hoặc URL. | [`2.1`](./05_Data_Mapping.md#21-validate-resource_id) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có query parameter theo contract. | `N/A` |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | GET endpoint không có request body. | `N/A` |

> Mỗi field nằm trên một row riêng. `resource_id` là input duy nhất do client gửi trong contract.

## Ví dụ Request

```http
GET /api/v1/resources/9001 HTTP/1.1
Host: api.example.test
Accept: application/json
```

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/03_Request.md`.
- Sheet logic: `1.Request`.
