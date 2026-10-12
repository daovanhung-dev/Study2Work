---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các lỗi normative của API #17 theo contract design. Không bổ sung HTTP status hoặc business code chưa được catalog khai báo. Chi tiết provider validation, ownership, gateway result và rollback còn SOURCE_REQUIRED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authorization thiếu hoặc JWT không hợp lệ theo contract | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 0.3 | N/A | Giữ nguyên code API catalog |
| 2 | Authorization | Yes | Student role | Authenticated caller không có role Student | 403 | DESIGN_ACCESS_DENIED | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 0.3 | N/A | Order ownership rule chưa được xác nhận |
| 3 | Request validation | Yes | order_id | Field bắt buộc hoặc kiểu không đáp ứng contract | 422 | DESIGN_VALIDATION_ERROR | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 2 | N/A | Không tự thêm positive/range rule |
| 4 | Request validation | Yes | provider | Field bắt buộc hoặc kiểu string không đáp ứng contract; allowlist chưa có nguồn | 422 | DESIGN_VALIDATION_ERROR | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 2 | N/A | Không tự định nghĩa provider values |
| 5 | External dependency | SOURCE_REQUIRED | Payment Gateway | Dependency unavailable theo nhóm lỗi design-only | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | N/A — ApiEnvelope message | 05_Data_Mapping.md, step 4 | SOURCE_REQUIRED | Gateway failure protocol và side-effect boundary chưa được xác nhận |
| 6 | Internal/system error | No | Payment/Operation processing | Lỗi nội bộ không xác định | 500 | DESIGN_INTERNAL_ERROR | N/A — ApiEnvelope message | 05_Data_Mapping.md, steps 4–6 | SOURCE_REQUIRED | Không trả chi tiết nội bộ; rollback chưa được xác nhận |

> Catalog API #17 khai báo 401, 403, 422, 503 và 500. AC-12 nói payment failure/cancel dừng flow nhưng không gán HTTP status/business code; không thêm error case mới cho hai kết quả đó.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.
