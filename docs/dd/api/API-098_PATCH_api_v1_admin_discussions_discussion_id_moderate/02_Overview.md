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
| API ID | `API-098` |
| Method | `PATCH` |
| Endpoint | `/api/v1/admin/discussions/{discussion_id}/moderate` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Kiểm duyệt ý kiến** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-37 — Kiểm duyệt ý kiến** · Actor: `Admin`

## 4. Preconditions

- **AC-37**: Có discussion bị report hoặc cần moderation.

## 5. Postconditions

- **AC-37**: Discussion được giữ/ẩn/khóa/xóa theo quyết định moderation.

## 6. Dependency / data source

- ERD tables: `discussions`, `users`, `courses`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
