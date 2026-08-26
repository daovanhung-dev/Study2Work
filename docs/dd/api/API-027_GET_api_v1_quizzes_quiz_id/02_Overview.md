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
| API ID | `API-027` |
| Method | `GET` |
| Endpoint | `/api/v1/quizzes/{quiz_id}` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Làm bài kiểm tra** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-16 — Làm bài kiểm tra** · Actor: `Student`

## 4. Preconditions

- **AC-16**: Student có quyền làm quiz; quiz đang mở.

## 5. Postconditions

- **AC-16**: Attempt được nộp; kết quả/ trạng thái chấm được trả về.

## 6. Dependency / data source

- ERD tables: `quizzes`, `quiz_questions`, `quiz_choices`, `quiz_attempts`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- ERD has no max-attempts column; attempts_left rule is SOURCE_REQUIRED.
