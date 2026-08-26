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
| API ID | `API-038` |
| Method | `GET` |
| Endpoint | `/api/v1/discussions` |
| Actor(s) | `Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Đặt câu hỏi / Thảo luận** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-19 — Đặt câu hỏi / Thảo luận** · Actor: `Student`

## 4. Preconditions

- **AC-19**: Student đăng nhập; có quyền tham gia discussion của course.

## 5. Postconditions

- **AC-19**: Topic/comment được tạo và thread được cập nhật.

## 6. Dependency / data source

- ERD tables: `discussions`, `users`, `courses`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
