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
| API ID | `API-043` |
| Method | `PATCH` |
| Endpoint | `/api/v1/notifications/{notification_id}/read` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Nhận thông báo** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-20 — Nhận thông báo** · Actor: `Student`

## 4. Preconditions

- **AC-20**: Student đã đăng nhập.

## 5. Postconditions

- **AC-20**: Danh sách thông báo/read state được đồng bộ.

## 6. Dependency / data source

- ERD tables: `notifications`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
