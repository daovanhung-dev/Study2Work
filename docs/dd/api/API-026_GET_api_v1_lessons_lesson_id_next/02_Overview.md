---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## 1. API

| Thuộc tính | Giá trị |
|---|---|
| API ID | `API-026` |
| Method | `GET` |
| Endpoint | `/api/v1/lessons/{lesson_id}/next` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem nội dung bài học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-15 — Xem nội dung bài học** · Actor: `Student`

## 4. Preconditions

- **AC-15**: Student có quyền xem lesson.

## 5. Postconditions

- **AC-15**: Nội dung, tài nguyên và điều hướng bài tiếp theo được hiển thị.

## 6. Dependency / data source

- ERD tables: `lessons`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
