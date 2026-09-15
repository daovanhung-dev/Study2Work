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
| Project/System | `Study2Work` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Loại tài liệu | `API Detail Design` |
| API ID | `12` |
| API name | `Lấy metadata / signed URL` |
| HTTP method | `GET` |
| Endpoint | `/api/v1/resources/{resource_id}` |
| Version | `V1` |
| Status | `Draft — Needs Confirmation` |
| Created by | `Codex` |
| Reviewed by | `TBD` |
| Approved by | `TBD` |
| Created date | `2026-08-29` |
| Updated date | `2026-08-29` |

## Tên hiển thị

```text
Study2Work API design
Lấy metadata / signed URL
```

## Nguồn chính

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #12 và contract V1.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-06 flow chọn resource, kiểm tra access và tạo signed URL.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-06 precondition/postcondition.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `resources`, `lessons`, `courses` và các khóa ngoại.
- [`createDD_MARKDOWN_SKILL.md`](../../../.agents/skills/create_dd/docs/dd/createDD_MARKDOWN_SKILL.md) — cấu trúc DD Markdown bắt buộc.

> Tài liệu này là design-only; API #12 chưa được xác minh trong runtime hoặc OpenAPI hiện hành.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/00_Cover.md`.
- Sheet logic: `Cover`.
- Bộ file giữ nguyên thứ tự baseline: `00_Cover.md` đến `07_table.md`.
