---
title: "Cover"
order: 0
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
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
| API ID | 24 |
| API name | Nạp nội dung bài học / Lấy nội dung chính |
| HTTP method | GET |
| Endpoint | /api/v1/lessons/{lesson_id} |
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
Nạp nội dung bài học / Lấy nội dung chính
~~~

## Nguồn chính

- [API catalog](../../../../../docs/lists/list_api.md) — contract thiết kế API #24 và schema `Lesson`/`ApiEnvelope`.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #24 thuộc AC-14 và AC-15.
- [AC-14/AC-15 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — vị trí API #24 trong luồng học và bước kiểm tra access/trạng thái publish.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) và [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — thiết kế bảng Lesson; không xác nhận schema live hoặc query API #24.
- [v1.py](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu trạng thái runtime hiện tại.

## Trạng thái xác nhận

Contract method/path/actor/request/response/status được ghi theo catalog. AC-15 yêu cầu kiểm tra access và trạng thái publish, nhưng predicate, JWT-to-enrollment binding, điều kiện 403/404, query/projection và null serialization chưa được xác nhận. API #24 chưa có route/module/query/test trong Study source hiện tại; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [00_Cover.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md).
- Sheet nguồn: Cover.
