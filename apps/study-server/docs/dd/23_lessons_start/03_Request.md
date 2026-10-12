---
title: "Request"
order: 3
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | POST |
| URI | /api/v1/lessons/{lesson_id}/start |
| Character encoding | UTF-8 |
| Content-Type | N/A — catalog không khai báo request body. |
| Accept | N/A — contract không khai báo riêng. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Contract yêu cầu Student Bearer JWT. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-authorization) — step 0 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Lesson ID | lesson_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | SOURCE_REQUIRED | N/A | Định danh lesson cần bắt đầu; catalog chỉ chốt int64 bắt buộc. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) — step 1 |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | POST contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
POST /api/v1/lessons/101/start HTTP/1.1
Authorization: Bearer <token>
~~~

> 101 và <token> là giá trị minh họa. Không gửi body theo catalog; API không quy định thêm range/format cho lesson_id.

> Catalog liệt kê 422 DESIGN_VALIDATION_ERROR nhưng không định nghĩa điều kiện validation ngoài kiểu int64 bắt buộc; không suy ra rule mới từ ví dụ này.

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
