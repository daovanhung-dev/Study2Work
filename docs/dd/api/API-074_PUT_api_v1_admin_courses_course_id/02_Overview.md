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
| API ID | `API-074` |
| Method | `PUT` |
| Endpoint | `/api/v1/admin/courses/{course_id}` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-32 — Quản lý khóa học** · Actor: `Admin`

## 4. Preconditions

- **AC-32**: Admin có quyền course management.

## 5. Postconditions

- **AC-32**: Course được cập nhật trạng thái/nội dung quản trị hoặc xóa theo policy.

## 6. Dependency / data source

- ERD tables: `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
