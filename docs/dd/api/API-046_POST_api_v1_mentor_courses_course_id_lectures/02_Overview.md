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
| API ID | `API-046` |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/courses/{course_id}/lectures` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đăng bài giảng** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-21 — Đăng bài giảng** · Actor: `Mentor`

## 4. Preconditions

- **AC-21**: Mentor đăng nhập và sở hữu/được phân công course.

## 5. Postconditions

- **AC-21**: Lecture mới được tạo và hiển thị trong course.

## 6. Dependency / data source

- ERD tables: `courses`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
