---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `DELETE /api/v1/admin/courses/{course_id}` từ actor `Admin` trong AC-32.

- Source: `AC-32` / ERD / API Index theo nội dung bước.
### 2. Kiểm tra authentication/authorization phù hợp precondition của AC-32; HTTP/error code cụ thể để `TBD` nếu AC không chỉ rõ.

- Source: `AC-32` / ERD / API Index theo nội dung bước.
### 3. Đọc path parameter: `course_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-32` / ERD / API Index theo nội dung bước.
### 4. Thực hiện đọc/ghi trên entity được ERD hỗ trợ: `courses`, `users`. Exact SELECT/INSERT/UPDATE/DELETE condition chỉ được chốt khi AC khóa đủ; phần chưa có evidence được đánh `TBD`.

- Source: `AC-32` / ERD / API Index theo nội dung bước.
### 5. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-32` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `courses` | DELETE / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `users` | DELETE / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
