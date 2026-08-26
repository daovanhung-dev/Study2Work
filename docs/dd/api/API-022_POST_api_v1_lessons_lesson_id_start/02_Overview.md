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
| API ID | `API-022` |
| Method | `POST` |
| Endpoint | `/api/v1/lessons/{lesson_id}/start` |
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

- ERD tables: `lesson_progress`, `lessons`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
