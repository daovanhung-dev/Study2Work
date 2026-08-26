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
| API ID | `API-036` |
| Method | `GET` |
| Endpoint | `/api/v1/users/me/progress/{course_id}` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Theo dõi tiến độ học tập** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-18 — Theo dõi tiến độ học tập** · Actor: `Student`

## 4. Preconditions

- **AC-18**: Student đã đăng nhập.

## 5. Postconditions

- **AC-18**: Dashboard tiến độ và thành tích được hiển thị.

## 6. Dependency / data source

- ERD tables: `courses`, `enrollments`, `lessons`, `lesson_progress`, `quiz_attempts`, `assignment_submissions`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
