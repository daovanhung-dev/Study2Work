---
title: "Cover"
order: 0
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
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
| API ID | 22 |
| API name | Kiểm tra quyền truy cập lesson |
| HTTP method | GET |
| Endpoint | /api/v1/lessons/{lesson_id}/access |
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
Kiểm tra quyền truy cập lesson
~~~

## Nguồn chính

- [list_api.md](../../../../../docs/lists/list_api.md) — contract thiết kế API #22 và schema Lesson/ApiEnvelope.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #22 thuộc AC-14; Student đã enrolled vào course chứa lesson.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — bước kiểm tra enrollment/prerequisite và nhánh từ chối 403 kèm lý do.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) và [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — thiết kế bảng lesson/enrollment; không chứng minh query hoặc schema runtime.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — DDL checked-in, chưa xác minh live metadata.
- [v1.py](../../../app/api/v1.py), [auth.py](../../../app/utils/auth.py) và [Study tests](../../../tests/) — trạng thái source hiện tại.

## Trạng thái xác nhận

Contract API #22 được ghi trực tiếp từ catalog. Chi tiết access predicate, JWT-to-enrollment binding, ý nghĩa 404, wire shape của lý do 403 và query mapping còn cần xác nhận; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [00_Cover.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md).
- Sheet nguồn: Cover.
