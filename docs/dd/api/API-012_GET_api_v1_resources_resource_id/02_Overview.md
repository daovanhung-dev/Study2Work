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
| API ID | `API-012` |
| Method | `GET` |
| Endpoint | `/api/v1/resources/{resource_id}` |
| Actor(s) | `Guest` |
| Authentication | `Not asserted by Guest AC; endpoint-specific access rule may apply` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Xem tài nguyên** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-06 — Xem tài nguyên** · Actor: `Guest`

## 4. Preconditions

- **AC-06**: Tài nguyên được phép xem public hoặc user có quyền truy cập.

## 5. Postconditions

- **AC-06**: Tài nguyên/file URL hợp lệ được mở hoặc tải xuống.

## 6. Dependency / data source

- ERD tables: `resources`, `lessons`, `courses`, `enrollments`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- ERD stores resources.url only; object key/private-storage metadata is not modeled.
