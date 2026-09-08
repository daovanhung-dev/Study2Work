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
| API ID | `13` |
| API name | `Upload avatar nếu có` |
| HTTP method | `POST` |
| Endpoint | `/api/v1/users/me/avatar` |
| Version | `V1` |
| Status | `Draft — Needs Confirmation` |
| Created by | `Codex (AI authoring agent)` |
| Reviewed by | `TBD — chưa được cung cấp` |
| Approved by | `TBD — chưa được cung cấp` |
| Created date | `2026-09-06` |
| Updated date | `2026-09-06` |

## Tên hiển thị

```text
Study2Work API design
Upload avatar nếu có
```

## Nguồn chính

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #13 contract, actor, request, response và status/error codes.
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-11 flow xác thực Student, lưu avatar tại Object Storage và chuyển sang API #14.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-11 precondition, postcondition và API usage.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — thiết kế V1 của `users` và ghi chú không tự thêm bảng/cột.
- [`createDD_MARKDOWN_SKILL.md`](../../../.agents/skills/create_dd/docs/dd/createDD_MARKDOWN_SKILL.md) — cấu trúc DD Markdown và quality gates bắt buộc.

> Tài liệu này là design-only; API #13 chưa được xác minh trong runtime hoặc OpenAPI hiện hành.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/00_Cover.md`.
- Sheet logic: `Cover`.
- Bộ file giữ nguyên thứ tự baseline: `00_Cover.md` đến `07_table.md`.
