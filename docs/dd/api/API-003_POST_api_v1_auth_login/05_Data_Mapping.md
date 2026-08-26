---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `POST /api/v1/auth/login` từ actor `Guest` trong AC-02.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 2. Đọc request body field explicit từ AC: `email`, `password`.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 3. Find user by email.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 4. Validate account existence/state.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 5. Verify password.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 6. Generate access and refresh tokens; AC states claims include user_id, role, expiry.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 7. Server-side refresh/session persistence is conditional in AC and has no ERD table; do not invent storage.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 8. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-02` / ERD / API Index theo nội dung bước.
### 9. Nếu gặp nhánh lỗi explicit, kết thúc theo error mapping tại `06_Error.md`.

- Source: `AC-02` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `users` | POST / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
