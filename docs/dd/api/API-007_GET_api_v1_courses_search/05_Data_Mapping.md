---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/courses/search` từ actor `Guest` trong AC-04.

- Source: `AC-04` / ERD / API Index theo nội dung bước.
### 2. Đọc query parameter explicit từ AC: `q`, `category`, `page`, `sort`.

- Source: `AC-04` / ERD / API Index theo nội dung bước.
### 3. Validate keyword/filter.

- Source: `AC-04` / ERD / API Index theo nội dung bước.
### 4. Search only PUBLISHED courses.

- Source: `AC-04` / ERD / API Index theo nội dung bước.
### 5. Return results or empty state.

- Source: `AC-04` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-04` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `courses` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- AC allows search index / DB; concrete search-engine dependency is not fixed.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
