---
title: "Cover"
order: 0
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
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
| API ID | 23 |
| API name | Khởi tạo/lưu lần bắt đầu học |
| HTTP method | POST |
| Endpoint | /api/v1/lessons/{lesson_id}/start |
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
Khởi tạo/lưu lần bắt đầu học
~~~

## Nguồn chính

- [API catalog](../../../../../docs/lists/list_api.md) — contract thiết kế API #23.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-14 actor, precondition, postcondition và API sequence.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #23 và bước UPSERT lesson progress = IN_PROGRESS.
- [DB design](../../diagrams/DB_UNICA_TABLES.md) và [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate Lesson/lesson_progress schema; chưa xác nhận live database.
- [Current router](../../../app/api/v1.py) và [Study tests](../../../tests/) — đối chiếu trạng thái runtime hiện tại.

## Trạng thái xác nhận

Catalog và AC-14 xác nhận contract mong đợi ở mức endpoint/flow. Khóa upsert, cột cập nhật, state transition khi gọi lại, response source và semantics 403/404/422 chưa được chốt; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [00_Cover.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md).
- Sheet nguồn: Cover.
