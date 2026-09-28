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
| API ID | 15 |
| API name | Kiểm tra trạng thái enrollment |
| HTTP method | GET |
| Endpoint | /api/v1/courses/{course_id}/enrollment-status |
| Version | V1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex (AI authoring agent) |
| Reviewed by | TBD — chưa được cung cấp |
| Approved by | TBD — chưa được cung cấp |
| Created date | 2026-09-23 |
| Updated date | 2026-09-23 |

## Tên hiển thị

```text
Study2Work API design
Kiểm tra trạng thái enrollment
```

## Nguồn chính

- [list_api.md](../../../../../docs/lists/list_api.md) — contract API #15, Enrollment, status/error codes.
- [AC_02_STUDENT_LEARNING.drawio](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12 sequence.
- [00_AC_API_INDEX.md](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-12 API mapping.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — current checked-in courses/enrollments schema.
- [DB_UNICA_TABLES.md](../../../docs/diagrams/DB_UNICA_TABLES.md) — enrollment columns and design-only status.
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — authoring and verification gates.

> Contract Public; no Bearer token được giữ nguyên. Vì Enrollment có user_id nhưng request không cung cấp identity, DD giữ PARTIALLY COMPLETED / NEEDS USER DECISION.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md.
- Sheet logic: Cover.
- Bộ file baseline: 00_Cover.md đến 07_table.md.
