---
title: "Error"
order: 6
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status và business code dưới đây giữ nguyên API #21 trong catalog. Contract không khai báo 404 hoặc 422 cho endpoint này. Message text, error metadata và điều kiện lỗi query chi tiết chưa được đặc tả; không tự thêm nhánh lỗi theo query phrase đang mơ hồ.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication is missing or invalid per design contract | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — message catalog chưa có | 05_Data_Mapping.md, step 0 | No | Design contract; API #21 endpoint chưa wired. |
| 2 | Authorization | Yes | Student role/access | Access is denied per design contract | 403 | DESIGN_ACCESS_DENIED | N/A — message catalog chưa có | 05_Data_Mapping.md, step 0 | No | Exact role/error predicate at API #21 is not runtime-verified. |
| 3 | System error | No | Progress query or response mapping | Internal processing failure | 500 | DESIGN_INTERNAL_ERROR | N/A — message catalog chưa có | 05_Data_Mapping.md, steps 2–4 | No | Design code; không trả raw SQL/stack trace. |

> API #21 chỉ đọc dữ liệu nên không có rollback. Contract không khai báo 422; query validation condition cần được xác nhận cùng query grammar trước khi thêm error case.

---
## Phụ lục đối chiếu template Markdown

- Template: [06_Error.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md).
- Sheet nguồn: 4.Error.
