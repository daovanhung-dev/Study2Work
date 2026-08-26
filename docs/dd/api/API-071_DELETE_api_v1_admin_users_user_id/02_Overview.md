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
| API ID | `API-071` |
| Method | `DELETE` |
| Endpoint | `/api/v1/admin/users/{user_id}` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý người dùng** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-31 — Quản lý người dùng** · Actor: `Admin`

## 4. Preconditions

- **AC-31**: Admin đăng nhập và có quyền user management.

## 5. Postconditions

- **AC-31**: Danh sách/chi tiết user được cập nhật theo thao tác quản trị.

## 6. Dependency / data source

- ERD tables: `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
