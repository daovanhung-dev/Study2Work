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
| API ID | 17 |
| API name | Khởi tạo/xác nhận thanh toán |
| HTTP method | POST |
| Endpoint | /api/v1/payments |
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
Khởi tạo/xác nhận thanh toán
~~~

## Nguồn chính

- [list_api.md](../../../../../docs/lists/list_api.md) — contract thiết kế API #17, schema Payment/Operation và business codes.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12, nhánh trả phí và Payment Gateway.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — thiết kế bảng payments và trạng thái API #17.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — ERD V1 và các quan hệ được ghi nhận.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in schema thiết kế của payments.
- [database.md](../../../../../.agents/server-study/database.md) — ranh giới schema nguồn và live metadata.
- [v1.py](../../../app/api/v1.py) và [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) — runtime route surface hiện hành.
- [OPEN_QUESTIONS.md API #16](../16_orders/OPEN_QUESTIONS.md) — các quyết định Order/provider/amount còn mở ở API trước đó trong AC-12.

## Trạng thái tài liệu

- Catalog và AC-12 là expected design; API #17 chưa runtime-verified và route hiện chưa được wire.
- Physical mapping của Order, association Order–Payment, nguồn amount/user/course, provider/gateway và Operation là SOURCE_REQUIRED.
- payments chỉ được ghi nhận theo schema thiết kế; không suy ra live availability hoặc thêm cột order_id.
- Completion: PARTIALLY COMPLETED; decision status: NEEDS USER DECISION.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/00_Cover.md.
- Sheet logic: Cover.
