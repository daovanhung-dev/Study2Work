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
| API ID | `API-065` |
| Method | `GET` |
| Endpoint | `/api/v1/mentor/courses/{course_id}/students/{student_id}/progress` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Theo dõi tiến độ** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-26 — Theo dõi tiến độ** · Actor: `Mentor`

## 4. Preconditions

- **AC-26**: Mentor có quyền xem analytics của course.

## 5. Postconditions

- **AC-26**: Tiến độ lớp, từng Student và analytics được hiển thị.

## 6. Dependency / data source

- ERD tables: `courses`, `enrollments`, `lessons`, `lesson_progress`, `quiz_attempts`, `assignment_submissions`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
