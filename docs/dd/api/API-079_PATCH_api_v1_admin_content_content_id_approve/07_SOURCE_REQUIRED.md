---
title: "DB Mapping — SOURCE_REQUIRED"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# DB Mapping — `SOURCE_REQUIRED`

## 1. Trạng thái

- API: `PATCH /api/v1/admin/content/{content_id}/approve`
- ERD V1 không cung cấp table/column đủ để khóa persistence/data source cho API này.
- Theo quyết định 3A, tài liệu **không tạo table/column giả**.

## 2. Hành động cần xác nhận

- Data source / external service / derived rule: `TBD / SOURCE_REQUIRED`.
- Khi source-of-truth được bổ sung, cập nhật file này và trace ngược sang Request/Data Mapping/Response/Error.
