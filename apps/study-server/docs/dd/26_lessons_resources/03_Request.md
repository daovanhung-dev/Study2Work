---
title: "Request"
order: 3
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | `/api/v1/lessons/{lesson_id}/resources` |
| Character encoding | UTF-8 |
| Content-Type | N/A — GET request không có body theo catalog. |
| Accept | N/A — catalog không khai báo riêng. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | Yes | `Bearer JWT` | API catalog yêu cầu Bearer JWT và role Student. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Lesson ID | `lesson_id` | `int64` | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer path segment | SOURCE_REQUIRED | N/A | Định danh lesson cần lấy tài nguyên đính kèm. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/lessons/101/resources HTTP/1.1
Authorization: Bearer <token>
~~~

> `101` và `<token>` chỉ là dữ liệu minh họa. Catalog không quy định range, positivity rule hoặc status mapping cho `lesson_id` parse lỗi.

