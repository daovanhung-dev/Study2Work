---
title: "Cover"
order: 0
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work |
| Module | STUDENT / LEARNING & INTERACTION |
| Loại tài liệu | API Detail Design |
| API ID | 25 |
| API name | Lưu vị trí và trạng thái |
| HTTP method | PATCH |
| Endpoint | `/api/v1/lessons/{lesson_id}/progress` |
| Version | 0.1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex (AI authoring agent) |
| Reviewed by | Chưa có |
| Approved by | Chưa có |
| Created date | 2026-10-11 |
| Updated date | 2026-10-11 |

## Tên hiển thị

```text
Study2Work API design
Lưu vị trí và trạng thái
```

## Nguồn chính

- [API catalog](../../../../../docs/lists/list_api.md) — request, response và status/business codes của API #25.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor và precondition AC-14.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — progress update, course aggregate và nhánh hoàn thành.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) và [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — schema candidate `lesson_progress`; không xác nhận live schema.
- [v1.py](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu runtime wiring hiện tại.

## Trạng thái xác nhận

Contract catalog được giữ nguyên. AC-14 mô tả cập nhật lesson progress và course aggregate; field mapping, khóa upsert, access predicate, aggregate semantics và response assembly chưa được xác nhận. API #25 chưa có route/module/query/focused test trong Study source hiện tại. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [00_Cover.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md).
- Sheet nguồn: Cover.
