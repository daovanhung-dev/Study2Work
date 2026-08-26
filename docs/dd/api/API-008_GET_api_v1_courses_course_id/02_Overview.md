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
| API ID | `API-008` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}` |
| Actor(s) | `Guest, Student` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem chi tiết khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-05 — Xem chi tiết khóa học** · Actor: `Guest`
- **AC-12 — Đăng ký khóa học** · Actor: `Student`

## 4. Preconditions

- **AC-05**: course_id hợp lệ và khóa học công khai.
- **AC-12**: Student đăng nhập; course tồn tại.

## 5. Postconditions

- **AC-05**: Trang chi tiết tổng hợp course, curriculum và reviews.
- **AC-12**: Enrollment được tạo; khóa học xuất hiện trong danh sách của Student.

## 6. Dependency / data source

- ERD tables: `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
