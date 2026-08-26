---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/quizzes/{quiz_id}` từ actor `Student` trong AC-16.

- Source: `AC-16` / ERD / API Index theo nội dung bước.
### 2. Kiểm tra authentication/authorization phù hợp precondition của AC-16; HTTP/error code cụ thể để `TBD` nếu AC không chỉ rõ.

- Source: `AC-16` / ERD / API Index theo nội dung bước.
### 3. Đọc path parameter: `quiz_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-16` / ERD / API Index theo nội dung bước.
### 4. Read Quiz + rule + question set.

- Source: `AC-16` / ERD / API Index theo nội dung bước.
### 5. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-16` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `quizzes` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `quiz_questions` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `quiz_choices` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `quiz_attempts` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- ERD has no max-attempts column; attempts_left rule is SOURCE_REQUIRED.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
