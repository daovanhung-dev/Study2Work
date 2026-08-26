---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/lessons/{lesson_id}` từ actor `Student` trong AC-14.

- Source: `AC-14` / ERD / API Index theo nội dung bước.
### 2. Kiểm tra authentication/authorization phù hợp precondition của AC-14; HTTP/error code cụ thể để `TBD` nếu AC không chỉ rõ.

- Source: `AC-14` / ERD / API Index theo nội dung bước.
### 3. Đọc path parameter: `lesson_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-14` / ERD / API Index theo nội dung bước.
### 4. Check access and publish state.

- Source: `AC-14` / ERD / API Index theo nội dung bước.
### 5. Read lesson and content metadata.

- Source: `AC-14` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-14` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `lessons` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
