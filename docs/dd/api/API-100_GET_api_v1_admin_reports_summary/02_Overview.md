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
| API ID | `API-100` |
| Method | `GET` |
| Endpoint | `/api/v1/admin/reports/summary` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Báo cáo tác động cộng đồng** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-38 — Báo cáo tác động cộng đồng** · Actor: `Admin`

## 4. Preconditions

- **AC-38**: Admin có quyền xem báo cáo/analytics.

## 5. Postconditions

- **AC-38**: Báo cáo tổng hợp được hiển thị hoặc export.

## 6. Dependency / data source

- ERD tables: `users`, `courses`, `enrollments`, `lesson_progress`, `quiz_attempts`, `assignment_submissions`, `discussions`, `notifications`, `payments`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
