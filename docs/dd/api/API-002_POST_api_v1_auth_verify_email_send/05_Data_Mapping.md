---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `POST /api/v1/auth/verify-email/send` từ actor `Guest` trong AC-01.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 2. Đọc request body field explicit từ AC: `user_id`, `email`.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 3. Request verification delivery if verification is enabled.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 4. Invoke email provider.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 5. If provider send fails, log/retry without creating duplicate account.

- Source: `AC-01` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-01` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `SOURCE_REQUIRED` | TBD | Không có table hợp lệ trong ERD V1 | Không tạo table/column giả |

## Source gaps

- No verification-token/outbox table is defined in ERD; persistence model is SOURCE_REQUIRED.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
