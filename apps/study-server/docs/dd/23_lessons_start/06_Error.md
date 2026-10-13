---
title: "Error"
order: 6
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status/business code dưới đây được giữ nguyên theo API #23 trong catalog. Catalog không mô tả chi tiết error payload, message, rollback hoặc điều kiện API-specific cho 403/404/422.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Bearer JWT missing or invalid per contract. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), step 0 | SOURCE_REQUIRED | Design contract; endpoint chưa wired. |
| 2 | Authorization | Yes | Student role/access | Role or access denied per contract; API #23-specific entitlement predicate unresolved. | 403 | DESIGN_ACCESS_DENIED | N/A — message/reason catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), step 0 | SOURCE_REQUIRED | AC-14 access decision belongs to preceding API #22 step; do not infer direct-call behavior. |
| 3 | Not found | Yes | Lesson/resource | A resource is not found per contract; exact API #23 resource condition unresolved. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), steps 2–4 | SOURCE_REQUIRED | Do not choose lesson, parent course, progress row, or visibility semantics without confirmation. |
| 4 | Validation | Yes | lesson_id/path | Request validation error per catalog. | 422 | DESIGN_VALIDATION_ERROR | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), step 1 | SOURCE_REQUIRED | Catalog does not define a validation condition beyond required int64 path. |
| 5 | System error | No | Progress/response processing | Internal processing failure. | 500 | DESIGN_INTERNAL_ERROR | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), steps 2–5 | SOURCE_REQUIRED | No raw database error or stack trace should be asserted as response contract; rollback rule is unspecified. |

> Catalog không công bố schema lỗi cụ thể hoặc error message ID. Bảng này không định nghĩa wire payload mới.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
