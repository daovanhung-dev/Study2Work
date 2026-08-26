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
| API ID | `API-002` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/verify-email/send` |
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

- ERD tables: `SOURCE_REQUIRED`
- External service: Có/conditional theo AC; xem Data Mapping.

## 7. Known gaps / confirmation points

- No verification-token/outbox table is defined in ERD; persistence model is SOURCE_REQUIRED.
