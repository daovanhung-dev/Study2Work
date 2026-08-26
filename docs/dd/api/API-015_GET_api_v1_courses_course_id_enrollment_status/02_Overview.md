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
| API ID | `API-015` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}/enrollment-status` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng ký khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-12 — Đăng ký khóa học** · Actor: `Student`

## 4. Preconditions

- **AC-12**: Student đăng nhập; course tồn tại.

## 5. Postconditions

- **AC-12**: Enrollment được tạo; khóa học xuất hiện trong danh sách của Student.

## 6. Dependency / data source

- ERD tables: `enrollments`, `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
