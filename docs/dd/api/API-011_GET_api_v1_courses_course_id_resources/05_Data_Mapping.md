---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/courses/{course_id}/resources` từ actor `Guest` trong AC-06.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 2. Đọc path parameter: `course_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 3. Resolve course → lessons → resources through ERD relationships.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 4. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-06` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `courses` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `lessons` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `resources` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- ERD resources has no visibility column; visibility output is SOURCE_REQUIRED.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
