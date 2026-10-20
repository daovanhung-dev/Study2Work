---
title: "Error"
order: 6
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bảng dưới giữ nguyên HTTP/business-code set của API #28 trong API catalog. AC-16 activity diagram có nhánh 403/409 khi điều kiện làm quiz không đạt, nhưng catalog API #28 không khai báo HTTP 409; DD không tự thêm code vào contract. API Guidelines quy định error response dùng data=null và không đưa chi tiết nội bộ ra ngoài.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication failure theo contract; runtime trigger chưa xác minh. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | Không suy đoán token claim hoặc handler runtime. |
| 2 | Authorization | Yes | Student role / quiz access | Role/access bị từ chối theo contract; entitlement và open-status predicate chưa rõ. | 403 | DESIGN_ACCESS_DENIED | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | AC-16 có nhánh 403/409; catalog API #28 chỉ liệt kê 403. |
| 3 | Not found | Yes | Quiz resource | DESIGN_RESOURCE_NOT_FOUND có trong contract; condition cụ thể chưa được gắn. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#2-read-quiz-and-question-set) | N/A — GET read-only. | Không tự gán missing/inaccessible/closed quiz vào 404. |
| 4 | System error | No | Read/mapping processing | Lỗi nội bộ theo contract; exception mapping chưa xác minh. | 500 | DESIGN_INTERNAL_ERROR | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#5-return-response) | N/A — GET read-only. | Error data=null; không trả SQL/stack trace. |

> Catalog không khai báo 400, 409, 422 hoặc 503 cho API #28. Path parse, quiz eligibility, hết lượt và hết hạn phải được xác nhận trước khi gắn thêm status/business code.

## Error response envelope

- success = false.
- businessCode = code tương ứng trong bảng Error cases.
- message = safe client message; text cụ thể SOURCE_REQUIRED.
- data = null theo API Guidelines.
- meta = object theo reusable ApiEnvelope schema; API-specific members chưa khai báo.
- traceId = UUID theo reusable ApiEnvelope schema.
