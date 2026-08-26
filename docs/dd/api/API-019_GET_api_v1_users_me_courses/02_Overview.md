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
| API ID | `API-019` |
| Method | `GET` |
| Endpoint | `/api/v1/users/me/courses` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng ký khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-12 — Đăng ký khóa học** · Actor: `Student`
- **AC-13 — Xem khóa học đã đăng ký** · Actor: `Student`

## 4. Preconditions

- **AC-12**: Student đăng nhập; course tồn tại.
- **AC-13**: Student đã đăng nhập và có thể có enrollment.

## 5. Postconditions

- **AC-12**: Enrollment được tạo; khóa học xuất hiện trong danh sách của Student.
- **AC-13**: Danh sách khóa học kèm tiến độ được hiển thị.

## 6. Dependency / data source

- ERD tables: `enrollments`, `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
