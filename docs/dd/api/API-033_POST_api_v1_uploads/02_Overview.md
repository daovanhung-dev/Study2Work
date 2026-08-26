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
| API ID | `API-033` |
| Method | `POST` |
| Endpoint | `/api/v1/uploads` |
| Actor(s) | `Mentor, Student` |
| Authentication | `Required by AC precondition` |
| Status | `Draft — Needs Confirmation` |

## 2. Mục đích và phạm vi

API này thuộc use case **Nộp bài tập** và được định danh trực tiếp trong AC/API Index. DD giữ nguyên contract endpoint từ diagram target design.

## 3. Activity / Use Case liên quan

- **AC-17 — Nộp bài tập** · Actor: `Student`
- **AC-21 — Đăng bài giảng** · Actor: `Mentor`

## 4. Preconditions

- **AC-17**: Assignment còn hạn và Student có quyền nộp.
- **AC-21**: Mentor đăng nhập và sở hữu/được phân công course.

## 5. Postconditions

- **AC-17**: Submission được tạo và có trạng thái nhận bài.
- **AC-21**: Lecture mới được tạo và hiển thị trong course.

## 6. Dependency / data source

- ERD tables: `SOURCE_REQUIRED`
- External service: Có/conditional theo AC; xem Data Mapping.

## 7. Known gaps / confirmation points

- Không xác định được nguồn bảng/cột hợp lệ từ ERD V1 cho endpoint này; DB/data source được đánh dấu `SOURCE_REQUIRED`.
- Activity/API index không khóa đầy đủ request body field; schema body được để `TBD / SOURCE_REQUIRED` thay vì suy diễn.
