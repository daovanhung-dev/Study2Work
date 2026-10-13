---
title: "Cover"
order: 0
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work — Online Learning System |
| Module | STUDENT / LEARNING & INTERACTION |
| Loại tài liệu | API Detail Design |
| API ID | 28 |
| API name | Lấy metadata/câu hỏi được phép hiển thị |
| HTTP method | GET |
| Endpoint | /api/v1/quizzes/{quiz_id} |
| Version | V1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | TBD — chưa được cung cấp |
| Approved by | TBD — chưa được cung cấp |
| Created date | 2026-10-12 |
| Updated date | 2026-10-12 |

## Tên hiển thị

~~~text
Study2Work API design
Lấy metadata/câu hỏi được phép hiển thị
~~~

## Nguồn chính

- [API catalog](../../../../../docs/lists/list_api.md) — contract design-only cho API #28.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-16 actor, precondition, postcondition và API flow.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — bước đọc Quiz, rule và question set; nhánh eligibility.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate table, fields và quan hệ.
- [Checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — schema design evidence; không xác nhận live schema.
- [Current router](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu runtime wiring hiện tại.

> API #28 hiện được mô tả như design-only trong catalog. Không tìm thấy route, module hoặc test runtime cho quiz trong Study Server. Các bảng quiz chỉ là evidence thiết kế; không xác nhận schema đang chạy.
