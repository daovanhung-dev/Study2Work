---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các lỗi normative của API #16 theo contract design. Không bổ sung HTTP status hoặc business code chưa được catalog khai báo. Validation detail cho enum provider và rollback behavior còn SOURCE_REQUIRED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authorization thiếu hoặc JWT không hợp lệ theo contract | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 0.3 | N/A | Giữ nguyên code API catalog |
| 2 | Authorization | Yes | Student role | Authenticated caller không có role Student | 403 | DESIGN_ACCESS_DENIED | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 0.3 | N/A | Giữ nguyên code API catalog |
| 3 | Request validation | Yes | Request body | Field bắt buộc hoặc kiểu không đáp ứng contract; allowed values của PaymentProvider chưa được source xác nhận | 422 | DESIGN_VALIDATION_ERROR | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 2 | N/A | Không tự thêm giới hạn hoặc message ID |
| 4 | Database/system error | No | Order creation/response mapping | Lỗi không xác định khi xử lý tạo Order hoặc map response | 500 | DESIGN_INTERNAL_ERROR | N/A — ApiEnvelope message | 05_Data_Mapping.md, steps 4–6 | SOURCE_REQUIRED | Transaction/rollback behavior chưa được xác nhận |

> Catalog API #16 chỉ khai báo 401, 403, 422 và 500. Không thêm 404, 409 hoặc 503.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.

