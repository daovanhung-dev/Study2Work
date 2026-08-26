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
| API ID | `API-090` |
| Method | `GET` |
| Endpoint | `/api/v1/admin/quizzes/{quiz_id}/statistics` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý kiểm tra** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-35 — Quản lý kiểm tra** · Actor: `Admin`

## 4. Preconditions

- **AC-35**: Admin có quiz management permission.

## 5. Postconditions

- **AC-35**: Quiz được tạo/cập nhật/xóa; statistics có thể được xem.

## 6. Dependency / data source

- ERD tables: `quizzes`, `quiz_attempts`, `quiz_answers`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
