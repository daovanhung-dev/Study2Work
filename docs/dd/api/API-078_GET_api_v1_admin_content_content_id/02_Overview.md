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
| API ID | `API-078` |
| Method | `GET` |
| Endpoint | `/api/v1/admin/content/{content_id}` |
| Actor(s) | `Admin` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Duyệt nội dung** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-33 — Duyệt nội dung** · Actor: `Admin`

## 4. Preconditions

- **AC-33**: Có content ở trạng thái pending review.

## 5. Postconditions

- **AC-33**: Content được approve hoặc reject với lý do.

## 6. Dependency / data source

- ERD tables: `SOURCE_REQUIRED`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không xác định được nguồn bảng/cột hợp lệ từ ERD V1 cho endpoint này; DB/data source được đánh dấu `SOURCE_REQUIRED`.
