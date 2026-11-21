---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các status và business code bên dưới được giữ nguyên từ API #20 trong catalog. Nội dung message, field error chi tiết và điều kiện chính xác của status/page validation chưa được đặc tả. Không thêm lỗi 404 hoặc 409 vì API #20 contract không khai báo các status này.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Token thiếu, sai định dạng hoặc không hợp lệ theo contract | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — message catalog chưa có | 05_Data_Mapping.md, step 0 | No | Design contract; endpoint #20 chưa wired. |
| 2 | Authorization | Yes | Student role | Authenticated principal không có role Student | 403 | DESIGN_ACCESS_DENIED | N/A — message catalog chưa có | 05_Data_Mapping.md, step 0 | No | Design contract; endpoint #20 chưa wired. |
| 3 | Query validation | SOURCE_REQUIRED | status | Giá trị status không hợp lệ theo rule cần được phê duyệt | 422 | DESIGN_VALIDATION_ERROR | N/A — message catalog chưa có | 05_Data_Mapping.md, step 1.1 | No | String type đã khai báo; enum và điều kiện invalid chưa có nguồn. |
| 4 | Query validation | SOURCE_REQUIRED | page | Không parse được int32 hoặc vi phạm constraint được phê duyệt | 422 | DESIGN_VALIDATION_ERROR | N/A — message catalog chưa có | 05_Data_Mapping.md, step 1.2 | No | Int32 đã khai báo; min/max/default chưa có nguồn. |
| 5 | System error | No | Query/response mapping | Database read hoặc mapping lỗi nội bộ | 500 | DESIGN_INTERNAL_ERROR | N/A — message catalog chưa có | 05_Data_Mapping.md, steps 2–4 | No | Design code; không trả raw SQL/stack trace. |

> Không có mutation nên không có rollback. Error response payload và message text theo runtime chưa được xác minh cho API #20.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
