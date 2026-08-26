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
| API ID | `API-021` |
| Method | `GET` |
| Endpoint | `/api/v1/lessons/{lesson_id}/access` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Học bài học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-14 — Học bài học** · Actor: `Student`

## 4. Preconditions

- **AC-14**: Student đã enrolled vào course chứa lesson.

## 5. Postconditions

- **AC-14**: Lesson được mở; tiến độ được lưu khi học/hoàn thành.

## 6. Dependency / data source

- ERD tables: `lessons`, `courses`, `enrollments`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Prerequisite model is not defined by ERD; prerequisite-specific rule is SOURCE_REQUIRED.
