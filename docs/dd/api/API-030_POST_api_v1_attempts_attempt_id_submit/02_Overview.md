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
| API ID | `API-030` |
| Method | `POST` |
| Endpoint | `/api/v1/attempts/{attempt_id}/submit` |
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

- ERD tables: `quiz_attempts`, `quiz_answers`, `quiz_questions`, `quiz_choices`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
