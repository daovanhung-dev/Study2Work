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
| URI | /api/v1/courses/{course_id}/enrollments |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | API catalog yêu cầu xác thực và role Student. | 0.1–0.3 |
| 2 | Content type | Content-Type | Yes | application/json | Request có body theo API catalog. | 1.1 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Course ID | course_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Path integer | Positive/range rule chưa được khai báo | N/A | ID của course trong endpoint. Contract cũng lặp course_id trong body; cách đối chiếu hai giá trị chưa được chốt. | 1.2; Q-19-01 |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | API catalog không khai báo query parameters. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Course ID | course_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Numeric | JSON integer | N/A | N/A | Body course_id trùng tên với path parameter; precedence/equality rule chưa được khai báo. | 1.2; Q-19-01 |
| 2 | User identity from JWT | SOURCE_REQUIRED — catalog phrase: user từ JWT | string | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Text | JWT-derived value; exact claim/wire representation unresolved | SOURCE_REQUIRED | N/A | Catalog đặt thông tin này trong body notation nhưng nói nguồn là JWT; không xác định JSON key, claim hoặc có cần gửi field từ client hay không. | 0.2; 1.3; Q-19-01 |

> Contract hiện ghi nguyên dạng body{course_id:int64!, user từ JWT:string!}. Không đổi thành một JSON field hoặc JWT claim cụ thể khi chưa có quyết định.

## Ví dụ Request data

Ví dụ dưới đây minh họa JSON hợp lệ. SOURCE_REQUIRED_user_field là placeholder giải thích cho field identity chưa có tên wire; không phải field đã được phê duyệt.

~~~json
{
  "course_id": 101,
  "SOURCE_REQUIRED_user_field": "42"
}
~~~

~~~
POST /api/v1/courses/101/enrollments HTTP/1.1
Host: api.example.test
Authorization: Bearer <token>
Content-Type: application/json
~~~

The placeholder field and value must not be copied into a client until Q-19-01 is resolved.

