---
title: "Request"
order: 3
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/lessons/{lesson_id} |
| Character encoding | UTF-8 |
| Content-Type | N/A — request không có body. |
| Accept | N/A — catalog không khai báo riêng. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | API catalog yêu cầu Student Bearer JWT. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Lesson ID | lesson_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | SOURCE_REQUIRED | N/A | Định danh Lesson cần đọc; catalog chỉ chốt kiểu int64 và bắt buộc. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/lessons/101 HTTP/1.1
Authorization: Bearer <token>
~~~

> `101` và `<token>` là giá trị minh họa. Catalog không quy định range, positivity rule hoặc hành vi parse lỗi cho `lesson_id`; API #24 chưa được wire để xác nhận behavior thực tế.

> Catalog không khai báo HTTP 422 cho API #24; không thêm validation/business code ngoài contract.

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
