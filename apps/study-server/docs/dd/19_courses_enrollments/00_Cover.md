---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work — Online Learning System |
| Module | STUDENT / LEARNING & INTERACTION |
| Loại tài liệu | API Detail Design |
| API ID | 19 |
| API name | Tạo quyền học |
| HTTP method | POST |
| Endpoint | /api/v1/courses/{course_id}/enrollments |
| Version | V1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex (AI authoring agent) |
| Reviewed by | TBD — chưa được cung cấp |
| Approved by | TBD — chưa được cung cấp |
| Created date | 2026-10-11 |
| Updated date | 2026-10-11 |

## Tên hiển thị

~~~text
Study2Work API design
Tạo quyền học
~~~

## Nguồn chính

- [list_api.md](../../../../../docs/lists/list_api.md) — approved design contract cho API #19 và schema Enrollment.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #19 thuộc AC-12.
- [AC-12 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — luồng miễn phí/đã thanh toán, tạo Enrollment và khởi tạo Progress.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — thiết kế bảng enrollments và lesson_progress.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — quan hệ giữa users, courses, lessons, enrollments và lesson_progress.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in Study schema/design; live metadata chưa được xác minh.

