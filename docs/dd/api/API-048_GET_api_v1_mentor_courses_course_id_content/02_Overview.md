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
| API ID | `API-048` |
| Method | `GET` |
| Endpoint | `/api/v1/mentor/courses/{course_id}/content` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý nội dung** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-22 — Quản lý nội dung** · Actor: `Mentor`

## 4. Preconditions

- **AC-22**: Mentor có quyền quản lý course.

## 5. Postconditions

- **AC-22**: Nội dung được tạo/cập nhật/xóa/publish theo thao tác.

## 6. Dependency / data source

- ERD tables: `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
