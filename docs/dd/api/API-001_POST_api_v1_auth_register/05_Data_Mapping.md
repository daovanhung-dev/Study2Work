---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `POST /api/v1/auth/register` từ actor `Guest` trong AC-01.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 2. Đọc request body field explicit từ AC: `email`, `password`, `full_name`.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 3. Validate schema + password policy.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 4. Check users by email = request.email.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 5. If duplicate email, terminate with 409.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 6. Hash password; create user entity with default STUDENT role and appropriate status.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 7. Insert user data.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 8. Continue to email verification flow if enabled.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 9. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 10. Nếu gặp nhánh lỗi explicit, kết thúc theo error mapping tại `06_Error.md`.

- Source: `AC-01` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `users` | POST / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- AC states “INSERT user + hồ sơ mặc định”; ERD has no separate profile table, therefore profile-table mutation is SOURCE_REQUIRED and is not invented.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
