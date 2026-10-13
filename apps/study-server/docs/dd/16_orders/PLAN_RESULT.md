# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 16 |
| API name | Tạo đơn hàng cho paid course |
| Endpoint | POST /api/v1/orders |
| Status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/16_orders/ |
| Basis | DIRECT — approved design contract + AC-12 flow; current schema/runtime checked separately |
| Runtime status | UNWIRED / NOT_FOUND — không có route/module/query/test API #16 trong Study |
| Tables read | N/A — endpoint query chưa được xác định |
| Tables write | Logical Order insert theo AC-12; physical table/columns SOURCE_REQUIRED |
| Business code delta | N/A — chỉ dùng design codes đã khai báo cho API #16 |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #16 contract và schema Order.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12 sequence.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — payments mapping và ghi chú orders vắng mặt.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — ERD V1 không tách orders.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in schema.
- [v1.py](../../../app/api/v1.py) — current route composition.
- [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) — current declared API surface.
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — authoring and delivery gates.

## Locked decisions

- Giữ nguyên method, endpoint, actor/RBAC, request fields, response schema, HTTP status và business codes của API #16 trong list_api.md.
- Ghi Order PENDING theo AC-12 và chỉ trong paid-course branch.
- Giữ expected design riêng với current runtime/schema; API #16 hiện UNWIRED / NOT_FOUND.
- Physical Order persistence và các giá trị PaymentProvider là SOURCE_REQUIRED.
- Không map Order sang payments; API #17 là endpoint thanh toán riêng.
- Không tạo route, source code, migration, table, column, enum hoặc business code.

## Open gaps

- Physical Order table/schema và field-to-column mapping.
- Allowed values và vai trò của PaymentProvider; quan hệ với provider nhập lại ở API #17.
- Nguồn/quy tắc tính amount và currency.
- Allowed OrderStatus values ngoài trạng thái tạo PENDING.
- API #16 xử lý direct call cho free course, course không hợp lệ hoặc đã enrolled như thế nào.

## Verification result

- Đủ 8 sheet template và các report được yêu cầu.
- Contract, AC-12 flow, current SQL/ERD và route status đã được đối chiếu riêng.
- Static structure/link/JSON/table review được ghi trong VERIFICATION_REPORT.md.
- Runtime tests không chạy vì API #16 chưa được wired.

