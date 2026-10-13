---
title: "Error"
order: 6
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status và business code dưới đây được giữ nguyên theo API #22 trong catalog. AC-14 nêu nhánh 403 có “lý do”, nhưng không định nghĩa field, message hoặc allowed reason values. Điều kiện 404 cũng chưa được gắn với một resource cụ thể.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Bearer JWT is missing or invalid per contract. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), step 0 | No | Design contract; endpoint chưa wired. |
| 2 | Authorization | Yes | Student role/access | Role or access is denied per contract; AC-14 associates denial with enrollment/prerequisite check. | 403 | DESIGN_ACCESS_DENIED | N/A — message/reason catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), steps 0 and 2 | No | Exact predicate and reason wire shape are open questions. |
| 3 | Not found | Yes | Lesson/resource | A resource is not found per contract; API-specific condition is unresolved. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), step 2 | No | Do not select missing lesson/course/visibility semantics without confirmation. |
| 4 | System error | No | Access or Lesson retrieval | Internal processing failure. | 500 | DESIGN_INTERNAL_ERROR | N/A — message catalog chưa có | [05_Data_Mapping.md](./05_Data_Mapping.md), steps 2–5 | No | No raw database error or stack trace in response. |

> API #22 là GET và không có mutation được mô tả, nên rollback không áp dụng. Contract không khai báo 422; không thêm validation/business code ngoài catalog.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
