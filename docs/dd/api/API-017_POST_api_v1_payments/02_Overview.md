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
| API ID | `API-017` |
| Method | `POST` |
| Endpoint | `/api/v1/payments` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng ký khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-12 — Đăng ký khóa học** · Actor: `Student`

## 4. Preconditions

- **AC-12**: Student đăng nhập; course tồn tại.

## 5. Postconditions

- **AC-12**: Enrollment được tạo; khóa học xuất hiện trong danh sách của Student.

## 6. Dependency / data source

- ERD tables: `payments`, `users`, `courses`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
