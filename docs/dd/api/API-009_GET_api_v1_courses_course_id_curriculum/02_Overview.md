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
| API ID | `API-009` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}/curriculum` |
| Actor(s) | `Guest` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem chi tiết khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-05 — Xem chi tiết khóa học** · Actor: `Guest`

## 4. Preconditions

- **AC-05**: course_id hợp lệ và khóa học công khai.

## 5. Postconditions

- **AC-05**: Trang chi tiết tổng hợp course, curriculum và reviews.

## 6. Dependency / data source

- ERD tables: `courses`, `lessons`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- ERD V1 does not define a sections table; section grouping is SOURCE_REQUIRED and must not be invented.
