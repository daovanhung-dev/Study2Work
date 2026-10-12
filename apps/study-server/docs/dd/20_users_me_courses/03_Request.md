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
| URI | /api/v1/users/me/courses |
| Character encoding | UTF-8 |
| Content-Type | N/A — request không có body |
| Accept | N/A — không được khai báo riêng trong contract |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Xác thực Student theo contract. | 05_Data_Mapping.md — step 0 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Endpoint không có path parameter. | N/A |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Enrollment/Course status filter | status | string | No | N/A | N/A | N/A | SOURCE_REQUIRED | SOURCE_REQUIRED | Lọc trạng thái; contract chưa xác định status thuộc Enrollment hay Course, enum và semantics. | 05_Data_Mapping.md — step 1 |
| 2 | Page | page | int32 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | SOURCE_REQUIRED | SOURCE_REQUIRED | Chỉ có kiểu và optionality trong contract; quy tắc pagination chưa được đặc tả. | 05_Data_Mapping.md — step 1 |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/users/me/courses HTTP/1.1
Authorization: Bearer <token>
~~~

> Ví dụ chỉ dùng endpoint và header có trong contract; không đưa query sample vì enum status và pagination chưa được xác nhận.

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
