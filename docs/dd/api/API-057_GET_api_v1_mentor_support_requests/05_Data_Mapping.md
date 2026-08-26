---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/mentor/support/requests` từ actor `Mentor` trong AC-24.

- Source: `AC-24` / ERD / API Index theo nội dung bước.
### 2. Kiểm tra authentication/authorization phù hợp precondition của AC-24; HTTP/error code cụ thể để `TBD` nếu AC không chỉ rõ.

- Source: `AC-24` / ERD / API Index theo nội dung bước.
### 3. Nguồn dữ liệu/persistence không có table hợp lệ trong ERD V1: `SOURCE_REQUIRED`; không tạo SQL giả.

- Source: `AC-24` / ERD / API Index theo nội dung bước.
### 4. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-24` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `SOURCE_REQUIRED` | TBD | Không có table hợp lệ trong ERD V1 | Không tạo table/column giả |

## Source gaps

- Không xác định được nguồn bảng/cột hợp lệ từ ERD V1 cho endpoint này; DB/data source được đánh dấu `SOURCE_REQUIRED`.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
