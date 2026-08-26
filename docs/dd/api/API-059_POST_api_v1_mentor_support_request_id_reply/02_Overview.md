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
| API ID | `API-059` |
| Method | `POST` |
| Endpoint | `/api/v1/mentor/support/{request_id}/reply` |
| Actor(s) | `Mentor` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Hỗ trợ học viên** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-24 — Hỗ trợ học viên** · Actor: `Mentor`

## 4. Preconditions

- **AC-24**: Mentor có request hỗ trợ thuộc phạm vi phụ trách.

## 5. Postconditions

- **AC-24**: Phản hồi được gửi và request có thể được resolved.

## 6. Dependency / data source

- ERD tables: `SOURCE_REQUIRED`
- External service: Không được khẳng định nếu AC không mô tả.

## 7. Known gaps / confirmation points

- Không xác định được nguồn bảng/cột hợp lệ từ ERD V1 cho endpoint này; DB/data source được đánh dấu `SOURCE_REQUIRED`.
- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
