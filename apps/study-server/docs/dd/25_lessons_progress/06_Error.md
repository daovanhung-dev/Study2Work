---
title: "Error"
order: 6
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status/business code dưới đây được giữ nguyên theo API #25 trong catalog. Trigger API-specific, error message/payload và transaction rollback chưa được runtime hoặc canonical contract xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication failure per contract; exact runtime trigger not verified. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-authorization) | SOURCE_REQUIRED — write chưa được xác nhận là bắt đầu ở nhánh này. | Contract design; API #25 chưa wired. |
| 2 | Authorization | Yes | Student role/access | Role/access denied per contract; direct-call entitlement predicate unresolved. | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog không có message/reason schema | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-authorization) | SOURCE_REQUIRED — transaction/rollback chưa xác định. | Không suy ra API #22 call là authorization của endpoint này. |
| 3 | Not found | Yes | Lesson/progress resource | Catalog declares resource-not-found; exact missing-resource condition unresolved. | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#2-read-progress-context) | SOURCE_REQUIRED — thứ tự read/write chưa xác định. | Không chọn 404 cho lesson, progress row hay visibility condition. |
| 4 | Validation | Yes | Path/body fields | Catalog declares validation error; exact type/range/relationship trigger is unresolved. | 422 | `DESIGN_VALIDATION_ERROR` | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#1-request-validation) | N/A — mutation chưa được xác nhận đã chạy trước validation. | Không thêm `position`/`percent` range rule. |
| 5 | System error | No | Progress/aggregate update | Internal processing failure per contract. | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog không có message ID | [05_Data_Mapping.md](./05_Data_Mapping.md#4-result-and-error-mapping) | SOURCE_REQUIRED — atomicity and rollback unspecified. | No API #25 runtime to verify exception/error mapping. |

> Catalog không định nghĩa error-specific `data`, `message` hoặc reason fields. Response example không tạo error wire contract mới.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
