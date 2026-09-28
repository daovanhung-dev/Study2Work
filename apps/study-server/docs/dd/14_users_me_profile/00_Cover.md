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
| Project/System | `Study2Work — Online Learning System` |
| Module | `STUDENT / LEARNING & INTERACTION` |
| Loại tài liệu | `API Detail Design` |
| API ID | `14` |
| API name | `Cập nhật hồ sơ` |
| HTTP method | `PUT` |
| Endpoint | `/api/v1/users/me/profile` |
| Version | `V1` |
| Status | `Draft — Needs Confirmation` |
| Created by | `Codex (AI authoring agent)` |
| Reviewed by | `TBD — chưa được cung cấp` |
| Approved by | `TBD — chưa được cung cấp` |
| Created date | `2026-09-23` |
| Updated date | `2026-09-23` |

## Tên hiển thị

```text
Study2Work API design
Cập nhật hồ sơ
```

## Nguồn chính

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #14 contract, request, response và status/error codes.
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-11 sequence: validate profile, update profile và reload profile.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-11 actor, precondition, postcondition và API mapping.
- [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql) — current checked-in Study schema evidence.
- [`API #4 current-user source`](../../../app/modules/guest/api_04_users_me/query.py) — safe profile projection và current JWT user lookup pattern.
- [`createDD-markdown skill`](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — template, traceability và quality gates.

> Tài liệu này là design-only. API #14 chưa được đăng ký trong current Study router, chưa có module runtime và chưa có test runtime.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md`.
- Sheet logic: `Cover`.
- Bộ file giữ nguyên thứ tự baseline: `00_Cover.md` đến `07_users_update.md`.
