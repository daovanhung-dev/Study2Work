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
| API ID | `API-001` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/register` |
| Actor(s) | `Guest` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng ký tài khoản** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-01 — Đăng ký tài khoản** · Actor: `Guest`

## 4. Preconditions

- **AC-01**: Người dùng chưa đăng nhập; email chưa được sử dụng.

## 5. Postconditions

- **AC-01**: Tài khoản được tạo; có thể chuyển sang xác thực email/đăng nhập.

## 6. Dependency / data source

- ERD tables: `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- AC states “INSERT user + hồ sơ mặc định”; ERD has no separate profile table, therefore profile-table mutation is SOURCE_REQUIRED and is not invented.
