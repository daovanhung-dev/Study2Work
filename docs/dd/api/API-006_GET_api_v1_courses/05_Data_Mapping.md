---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/courses` từ actor `Guest` trong AC-03.

- Source: `AC-03` / ERD / API Index theo nội dung bước.
### 2. Đọc query parameter explicit từ AC: `category`, `page`, `size`, `sort`.

- Source: `AC-03` / ERD / API Index theo nội dung bước.
### 3. Validate and normalize filter/pagination.

- Source: `AC-03` / ERD / API Index theo nội dung bước.
### 4. Read only PUBLISHED courses; do not return draft/private courses.

- Source: `AC-03` / ERD / API Index theo nội dung bước.
### 5. Return paginated result or empty collection.

- Source: `AC-03` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-03` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `courses` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
