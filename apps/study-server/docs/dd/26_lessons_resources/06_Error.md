---
title: "Error"
order: 6
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP/business code dưới đây được giữ theo API #26 catalog. Catalog không định nghĩa error payload/message hoặc trigger cụ thể cho access và not-found; API #26 chưa có runtime route để xác minh.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication failure theo contract; runtime trigger chưa xác minh. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | Không ghi giả payload/message. |
| 2 | Authorization | Yes | Student role/access | Role hoặc access bị từ chối theo contract; policy/predicate API #26 chưa rõ. | 403 | DESIGN_ACCESS_DENIED | N/A — catalog không có message/reason schema. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | Không suy diễn enrollment/publish rule. |
| 3 | Not found | Yes | Lesson/resource | Resource not found theo contract; lesson-missing, empty-resource và visibility behavior chưa phân định. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#53-not-found) | N/A — GET read-only. | Không gán empty list thành 404. |
| 4 | System error | No | Read processing | Lỗi nội bộ theo contract; exception mapping chưa xác minh. | 500 | DESIGN_INTERNAL_ERROR | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#54-system-error) | N/A — GET read-only. | Không trả raw SQL/stack trace. |

> Catalog không liệt kê 422 cho API #26; không thêm validation/error code. Error-specific envelope data và message text chưa được nguồn quy định.

