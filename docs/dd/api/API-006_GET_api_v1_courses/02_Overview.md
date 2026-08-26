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
| API ID | `API-006` |
| Method | `GET` |
| Endpoint | `/api/v1/courses` |
| Actor(s) | `Guest` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Ready for Review` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem danh sách khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-03 — Xem danh sách khóa học** · Actor: `Guest`

## 4. Preconditions

- **AC-03**: Hệ thống có khóa học ở trạng thái công khai.

## 5. Postconditions

- **AC-03**: Danh sách khóa học được hiển thị theo filter/pagination.

## 6. Dependency / data source

- ERD tables: `courses`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không có gap nguồn đã phát hiện ở mức tài liệu hiện tại.
