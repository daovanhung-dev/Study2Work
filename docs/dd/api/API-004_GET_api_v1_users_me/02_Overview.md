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
| API ID | `API-004` |
| Method | `GET` |
| Endpoint | `/api/v1/users/me` |
| Actor(s) | `Guest, Student` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng nhập** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-02 — Đăng nhập** · Actor: `Guest`
- **AC-11 — Quản lý hồ sơ cá nhân** · Actor: `Student`

## 4. Preconditions

- **AC-02**: Tài khoản đã tồn tại và không bị khóa.
- **AC-11**: Student đã đăng nhập.

## 5. Postconditions

- **AC-02**: Client nhận token, profile và điều hướng theo role.
- **AC-11**: Profile/avatar được cập nhật và phản ánh trên UI.

## 6. Dependency / data source

- ERD tables: `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
