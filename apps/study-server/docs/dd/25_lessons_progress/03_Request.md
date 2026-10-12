---
title: "Request"
order: 3
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PATCH |
| URI | `/api/v1/lessons/{lesson_id}/progress` |
| Character encoding | UTF-8 |
| Content-Type | `application/json` trong ví dụ body; catalog không chốt media type. |
| Accept | N/A — catalog không khai báo riêng. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | API catalog yêu cầu actor Student. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-authorization) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Lesson ID | `lesson_id` | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | SOURCE_REQUIRED | N/A | Định danh Lesson; catalog chỉ chốt kiểu int64 và bắt buộc. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| 1 | Vị trí học | `position` | int32 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Number | Integer | SOURCE_REQUIRED | N/A | Vị trí cần lưu; đơn vị và mapping vật lý chưa được xác nhận. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |
| 2 | Phần trăm tiến độ | `percent` | int32 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Number | Integer | SOURCE_REQUIRED | N/A | Phần trăm tiến độ theo field contract; range và mapping vật lý chưa được xác nhận. | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) |
| 3 | Hoàn thành | `completed` | boolean | Yes | N/A | N/A | Boolean | JSON boolean | `true` / `false` | N/A | Cờ hoàn thành theo contract; mapping trạng thái/timestamp cần xác nhận. | [05_Data_Mapping.md](./05_Data_Mapping.md#3-update-lesson-progress-and-aggregate) |

## Ví dụ Request data

~~~http
PATCH /api/v1/lessons/101/progress HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "position": 120,
  "percent": 45,
  "completed": false
}
~~~

> Ví dụ chỉ minh họa tên field và kiểu dữ liệu. `120` không xác định đơn vị `position`; `45` không chốt range/rounding của `percent`; các giá trị không tạo validation rule mới.

> `<token>` là placeholder minh họa header Bearer; format/claim ngoài yêu cầu Bearer JWT của catalog không được đặc tả ở đây.

> Header `Content-Type` trong ví dụ minh họa body JSON; catalog không ghi rõ media type.

> Catalog liệt kê HTTP 422 `DESIGN_VALIDATION_ERROR` nhưng không định nghĩa trigger hoặc field constraints. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [03_Request.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md).
- Sheet nguồn: 1.Request.
