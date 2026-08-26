---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `PATCH /api/v1/admin/content/{content_id}/approve` từ actor `Admin` trong AC-33.

- Source: `AC-33` / ERD / API Index theo nội dung bước.
### 2. Kiểm tra authentication/authorization phù hợp precondition của AC-33; HTTP/error code cụ thể để `TBD` nếu AC không chỉ rõ.

- Source: `AC-33` / ERD / API Index theo nội dung bước.
### 3. Đọc path parameter: `content_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-33` / ERD / API Index theo nội dung bước.
### 4. Request body field-level chưa đủ nguồn: không suy diễn; đánh dấu `TBD / SOURCE_REQUIRED`.

- Source: `AC-33` / ERD / API Index theo nội dung bước.
### 5. Nguồn dữ liệu/persistence không có table hợp lệ trong ERD V1: `SOURCE_REQUIRED`; không tạo SQL giả.

- Source: `AC-33` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-33` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `SOURCE_REQUIRED` | TBD | Không có table hợp lệ trong ERD V1 | Không tạo table/column giả |

## Source gaps

- Không xác định được nguồn bảng/cột hợp lệ từ ERD V1 cho endpoint này; DB/data source được đánh dấu `SOURCE_REQUIRED`.
- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
