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
| API ID | `API-005` |
| Method | `GET` |
| Endpoint | `/api/v1/categories` |
| Actor(s) | `Guest` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem danh sách khóa học** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-03 — Xem danh sách khóa học** · Actor: `Guest`
- **AC-04 — Tìm kiếm khóa học** · Actor: `Guest`

## 4. Preconditions

- **AC-03**: Hệ thống có khóa học ở trạng thái công khai.
- **AC-04**: Người dùng đang ở khu vực khám phá khóa học.

## 5. Postconditions

- **AC-03**: Danh sách khóa học được hiển thị theo filter/pagination.
- **AC-04**: Kết quả tìm kiếm phù hợp từ khóa/bộ lọc được hiển thị.

## 6. Dependency / data source

- ERD tables: `SOURCE_REQUIRED`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- ERD defines no categories table/source. Data source is SOURCE_REQUIRED.
