---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### 1. Nhận `GET /api/v1/resources/{resource_id}` từ actor `Guest` trong AC-06.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 2. Đọc path parameter: `resource_id`; type/range validation chưa được diagram khóa thì để `TBD`.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 3. Check visibility/access rule.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 4. Read resource metadata/URL.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 5. If storage is private, external object storage may create signed URL.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 6. Tạo response chỉ từ output đã được nguồn xác nhận; field chưa xác nhận giữ `TBD` và không tự bổ sung.

- Source: `AC-06` / ERD / API Index theo nội dung bước.
### 7. Nếu gặp nhánh lỗi explicit, kết thúc theo error mapping tại `06_Error.md`.

- Source: `AC-06` / ERD / API Index theo nội dung bước.

## DB / storage interaction matrix

| Table / Source | Operation | Evidence | Condition / Remarks |
|---|---|---|---|
| `resources` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `lessons` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `courses` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |
| `enrollments` | READ / exact operation TBD | ERD-backed entity | Exact predicate/mutation only where AC explicitly fixes it |

## Source gaps

- ERD stores resources.url only; object key/private-storage metadata is not modeled.

## Traceability rule

`Request → Validation/Authorization → ERD/External Source → Transform/Aggregate → Response → Error`

Mọi mắt xích chưa có evidence được giữ `TBD / SOURCE_REQUIRED`; tài liệu không bổ sung schema hoặc business rule ngoài diagram.
