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
| API ID | `API-085` |
| Method | `DELETE` |
| Endpoint | `/api/v1/admin/lessons/{lesson_id}` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý bài học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-34 — Quản lý bài học** · Actor: `Admin`

## 4. Preconditions

- **AC-34**: Admin có lesson management permission.

## 5. Postconditions

- **AC-34**: Lesson được cập nhật/trạng thái thay đổi/xóa theo thao tác.

## 6. Dependency / data source

- ERD tables: `lessons`, `courses`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
