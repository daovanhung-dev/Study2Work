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
| API ID | 16 |
| API name | Tạo đơn hàng cho paid course |
| HTTP method | POST |
| Endpoint | /api/v1/orders |
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
Tạo đơn hàng cho paid course
```

## Nguồn chính

- [list_api.md](../../../../../docs/lists/list_api.md) — contract thiết kế API #16 và schema dùng chung `Order`.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12, nhánh paid course.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — trạng thái thiết kế bảng `payments` và ghi chú chưa có bảng `orders`.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — ERD V1 không tách bảng `orders`.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — schema SQL hiện có bảng `payments`, không có `orders`.
- [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) — route surface Study hiện hành; API #16 chưa được khai báo.

## Trạng thái tài liệu

- Contract và flow AC-12 là expected design, chưa chứng minh runtime.
- Persistence của Order và allowed values của `PaymentProvider` là `SOURCE_REQUIRED`.
- Completion: `PARTIALLY COMPLETED`; decision status: `NEEDS USER DECISION`.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md.
- Sheet logic: Cover.

