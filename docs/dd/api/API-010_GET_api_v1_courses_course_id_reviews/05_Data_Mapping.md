---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/courses/{course_id}/reviews` từ actor `Guest` trong AC-05.

- Source: `AC-05` / ERD / API Index theo nội dung bước.
### 2. Đọc path parameter: `course_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-05` / ERD / API Index theo nội dung bước.
### 3. Đọc query parameter explicit từ AC: `page`, `rating`.

- Source: `AC-05` / ERD / API Index theo nội dung bước.
### 4. Nguồn dữ liệu/persistence không có table hợp lệ trong ERD V1: `SOURCE_REQUIRED`; không tạo SQL giả.

- Source: `AC-05` / ERD / API Index theo nội dung bước.
### 5. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-05` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `SOURCE_REQUIRED` | TBD | Không có table hợp lệ trong ERD V1 | Không tạo table/column giả |

## Source gaps

- ERD defines no reviews table/source. Review list and aggregate rating are SOURCE_REQUIRED.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
