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
| API ID | `API-062` |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/notifications` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Gửi thông báo** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-25 — Gửi thông báo** · Actor: `Mentor`

## 4. Preconditions

- **AC-25**: Mentor có quyền gửi thông báo tới học viên thuộc course.

## 5. Postconditions

- **AC-25**: Notification được tạo và trạng thái phát được theo dõi.

## 6. Dependency / data source

- ERD tables: `notifications`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
