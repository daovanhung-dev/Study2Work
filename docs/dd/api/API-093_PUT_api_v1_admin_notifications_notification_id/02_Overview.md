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
| API ID | `API-093` |
| Method | `PUT` |
| Endpoint | `/api/v1/admin/notifications/{notification_id}` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Quản lý thông báo** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-36 — Quản lý thông báo** · Actor: `Admin`

## 4. Preconditions

- **AC-36**: Admin có notification management permission.

## 5. Postconditions

- **AC-36**: Notification được tạo/cập nhật/xóa và theo dõi trạng thái.

## 6. Dependency / data source

- ERD tables: `notifications`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
