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
| API ID | `API-034` |
| Method | `POST` |
| Endpoint | `/api/v1/assignments/{assignment_id}/submissions` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Nộp bài tập** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-17 — Nộp bài tập** · Actor: `Student`

## 4. Preconditions

- **AC-17**: Assignment còn hạn và Student có quyền nộp.

## 5. Postconditions

- **AC-17**: Submission được tạo và có trạng thái nhận bài.

## 6. Dependency / data source

- ERD tables: `assignments`, `assignment_submissions`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
