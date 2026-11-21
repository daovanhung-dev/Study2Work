---
title: "Request"
order: 3
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/users/me/progress |
| Character encoding | UTF-8 |
| Content-Type | N/A — request không có body |
| Accept | N/A — contract không khai báo riêng |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Xác thực Student theo contract. | 05_Data_Mapping.md — step 0 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Endpoint không có path parameter. | N/A |

## Query parameters

Catalog khai báo nguyên văn: course_id list hoặc aggregate?:string. Cách phân tách field, kiểu course_id list, optionality và semantics chưa rõ; giữ gap này thay vì chuẩn hóa thành một query shape.

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Progress query selector — raw catalog declaration | SOURCE_REQUIRED — see Q-21-01 | string is the declared suffix; course_id list type is SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | Preserve the catalog phrase course_id list hoặc aggregate?:string; field grammar and behavior are unresolved. | 05_Data_Mapping.md — step 1 |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET contract không khai báo request body. | N/A |

## Ví dụ Request

~~~http
GET /api/v1/users/me/progress HTTP/1.1
Authorization: Bearer <token>
~~~

> Không đưa query example vì contract chưa xác định field name/grammar, kiểu course_id list và ý nghĩa aggregate. Bearer token là placeholder.

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
