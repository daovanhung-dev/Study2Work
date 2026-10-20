---
title: "Request"
order: 3
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/quizzes/{quiz_id} |
| Character encoding | UTF-8 |
| Content-Type | N/A — GET contract không khai báo request body. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Catalog yêu cầu Student Bearer JWT. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) |
| 2 | Content type | Content-Type | N/A | N/A | Không có request body theo contract. | N/A |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Quiz ID | quiz_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer path segment | SOURCE_REQUIRED | N/A | Định danh quiz cần đọc metadata và question set. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |

> Catalog chỉ xác định quiz_id là int64 bắt buộc; không quy định positivity/range hoặc cách ánh xạ path parse lỗi.

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/quizzes/501 HTTP/1.1
Authorization: Bearer <token>
~~~

> quiz_id 501 và token là dữ liệu minh họa. Contract không quy định range/positivity hoặc status cho path parse lỗi.
