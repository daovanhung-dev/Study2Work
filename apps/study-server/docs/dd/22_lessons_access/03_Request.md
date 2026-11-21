---
title: "Request"
order: 3
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/lessons/{lesson_id}/access |
| Character encoding | UTF-8 |
| Content-Type | N/A — request không có body. |
| Accept | N/A — contract không khai báo riêng. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Contract yêu cầu Student Bearer JWT. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-check-quyen) — step 0 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Lesson ID | lesson_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | SOURCE_REQUIRED | N/A | Định danh lesson cần kiểm tra; contract chỉ xác định int64 bắt buộc. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-usage-and-validation) — step 1 |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API #22 catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/lessons/101/access HTTP/1.1
Authorization: Bearer <token>
~~~

> `101` và `<token>` chỉ là giá trị minh họa. Contract chưa quy định range/format bổ sung cho `lesson_id`.

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
