---
title: "Cover"
order: 0
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
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
| API ID | 26 |
| API name | Lấy tài nguyên đính kèm |
| HTTP method | GET |
| Endpoint | /api/v1/lessons/{lesson_id}/resources |
| Version | V1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex (AI authoring agent) |
| Reviewed by | TBD — chưa được cung cấp |
| Approved by | TBD — chưa được cung cấp |
| Created date | 2026-10-11 |
| Updated date | 2026-10-11 |

## Tên hiển thị

```text
Study2Work API design
Lấy tài nguyên đính kèm
```

## Nguồn chính

- [API catalog](../../../../../docs/lists/list_api.md) — API #26 contract và reusable schema.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-15 actor, precondition, postcondition và API flow.
- [AC-15 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #26 và bước đọc lesson resources.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) và [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — candidate resource schema; design-only.
- [v1.py](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu current runtime wiring.

> API #26 chưa được wire trong Study runtime. Catalog/diagram khai báo `ApiEnvelope<Lesson>` dù mục đích là lấy tài nguyên; DD giữ nguyên contract và ghi mâu thuẫn để owner xác nhận.

