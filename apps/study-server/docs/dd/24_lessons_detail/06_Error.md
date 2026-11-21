---
title: "Error"
order: 6
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status/business code dưới đây được giữ nguyên theo API #24 trong catalog. Catalog không mô tả chi tiết error payload/message hoặc điều kiện API-specific cho 403/404. API #24 chưa có runtime route để xác minh mapping.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication failure per contract; exact runtime trigger not verified. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only | Contract design; API #24 chưa wired. |
| 2 | Authorization | Yes | Student role/access | Role/access denied per contract; entitlement and publish predicate unresolved. | 403 | DESIGN_ACCESS_DENIED | N/A — catalog không có message/reason schema | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only | Không chuyển reason wire shape của API #22 sang API #24. |
| 3 | Not found | Yes | Lesson/resource visibility | Catalog declares resource-not-found; exact lesson, parent-course or visibility condition unresolved. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#2-read-lesson-data) | N/A — GET read-only | Không chọn 403/404 split khi unpublished hoặc inaccessible. |
| 4 | System error | No | Lesson/access read processing | Internal processing failure per contract. | 500 | DESIGN_INTERNAL_ERROR | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#4-result-and-error-mapping) | N/A — GET read-only | Không khẳng định exception mapping/payload từ source API #24. |

> Catalog không liệt kê 422 cho API #24 và không công bố schema lỗi hoặc message ID. Bảng này không tạo wire payload/business code mới.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
