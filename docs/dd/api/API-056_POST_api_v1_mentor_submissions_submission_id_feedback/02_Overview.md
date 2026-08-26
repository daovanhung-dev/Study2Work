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
| API ID | `API-056` |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/submissions/{submission_id}/feedback` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Chấm bài** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-23 — Chấm bài** · Actor: `Mentor`

## 4. Preconditions

- **AC-23**: Mentor có quyền chấm submission của course.

## 5. Postconditions

- **AC-23**: Điểm và feedback được lưu; Student có thể nhận kết quả.

## 6. Dependency / data source

- ERD tables: `assignment_submissions`, `assignments`, `users`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
