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
| API ID | `API-013` |
| Method | `PUT` |
| Endpoint | `/api/v1/users/me/profile` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý hồ sơ cá nhân** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-11 — Quản lý hồ sơ cá nhân** · Actor: `Student`

## 4. Preconditions

- **AC-11**: Student đã đăng nhập.

## 5. Postconditions

- **AC-11**: Profile/avatar được cập nhật và phản ánh trên UI.

## 6. Dependency / data source

- ERD tables: `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
