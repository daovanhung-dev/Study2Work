# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 20 |
| API name | Lấy danh sách khóa học đã đăng ký |
| Endpoint | GET /api/v1/users/me/courses |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/20_users_me_courses/ |
| Basis | DIRECT — approved design contract + AC-13 + checked-in DB design |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/query/test API #20 |
| Tables read | enrollments, courses — DESIGN_ONLY |
| Tables write | N/A — read-only |
| Business code delta | N/A — giữ codes đã có trong catalog |
| Packaging | Markdown folder only; Study workflow không yêu cầu ZIP |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #20, reusable schemas, status/error codes.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-12/AC-13 API map.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — toàn bộ AC-13 flow.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — query status DESIGN_ONLY và table relations.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL; chưa phải live schema proof.
- [v1.py](../../../app/api/v1.py), [auth.py](../../../app/utils/auth.py), [responses.py](../../../app/core/responses.py) — current route/auth/envelope evidence.
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — template and authoring rules.

## Locked decisions

- Endpoint, method, Student JWT requirement, query fields, response type, status codes và business codes được giữ đúng catalog.
- AC-13 ghi Enrollment JOIN Course; API #21 progress được gọi riêng và client ghép theo diagram.
- Không tự đổi UserProfile thành Page<Course>; không thêm phần trăm progress.
- Không invent enum status, defaults, page size, sort, empty wire shape, hoặc query projection.
- DD có đủ tám sheet; 07_table.md giữ N/A — READ-ONLY API.
- Không thay đổi runtime, API catalog, diagram, DB schema hoặc migration; không tạo ZIP.

## Open gaps

- Response UserProfile không khớp use case danh sách Course: [Q-20-01](./OPEN_QUESTIONS.md#q-20-01).
- Status semantics và valid values: [Q-20-02](./OPEN_QUESTIONS.md#q-20-02).
- Page, pagination metadata, ordering và page size: [Q-20-03](./OPEN_QUESTIONS.md#q-20-03).
- Empty result wire shape: [Q-20-04](./OPEN_QUESTIONS.md#q-20-04).
- JWT subject/query binding tới enrollments.user_id: [Q-20-05](./OPEN_QUESTIONS.md#q-20-05).

## Verification result

- Static DD checks and source coverage are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Runtime tests: NOT_RUN — documentation-only scope and API #20 is not wired.
- Context validator: NOT_REQUIRED — no canonical context page or manifest changed.
