# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 22 |
| API name | Kiểm tra quyền truy cập lesson |
| Endpoint | GET /api/v1/lessons/{lesson_id}/access |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/22_lessons_access/ |
| Basis | DIRECT — approved design contract + AC-14 + checked-in DB design |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/query/focused test API #22 |
| Tables read | `lessons`, `enrollments` — candidate design only; query chưa xác nhận |
| Tables write | N/A — GET; không có mutation được mô tả |
| Business code delta | N/A — giữ codes hiện có trong catalog |
| Packaging | Markdown folder only; Study workflow không yêu cầu ZIP |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #22 contract, reusable Lesson và ApiEnvelope schemas.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-14 actor, precondition, postcondition và API list.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — enrollment/prerequisite check, 403 + reason, API #23/#24 follow-up.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — candidate lesson/enrollment mappings and design/runtime status.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL; live metadata chưa xác minh.
- [v1.py](../../../app/api/v1.py), [auth.py](../../../app/utils/auth.py) — current route/helper evidence; API #22 not wired.
- [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) — predicate, identity binding, 403 reason, 404 semantics and query/schema baseline.

## Locked decisions

- Giữ endpoint, Student Bearer JWT, path `lesson_id:int64!`, `ApiEnvelope<Lesson>` và các mã 200/401/403/404/500 từ catalog.
- AC-14 chỉ xác nhận kiểm tra enrollment/prerequisite và nhánh từ chối 403 + lý do; không tự định nghĩa predicate hoặc reason payload.
- Không thêm query/body, 422, response field, status rule, publish filter, SQL hoặc side effect.
- Phân biệt API #22 access check với API #23 lesson start; API #22 không có mutation mapping.
- Giữ runtime status `UNWIRED / NOT_FOUND`; checked-in DDL/ERD là design evidence, live schema chưa xác minh.
- Tạo tám sheet template và ba report; không tạo ZIP theo Study workflow.

## Open gaps

- Access rule, enrollment eligibility và prerequisite: [Q-22-01](./OPEN_QUESTIONS.md#q-22-01).
- JWT identity to enrollment binding: [Q-22-02](./OPEN_QUESTIONS.md#q-22-02).
- 403 reason wire shape: [Q-22-03](./OPEN_QUESTIONS.md#q-22-03).
- 404 resource semantics: [Q-22-04](./OPEN_QUESTIONS.md#q-22-04).
- Query/projection/schema baseline: [Q-22-05](./OPEN_QUESTIONS.md#q-22-05).

## Verification result

- Template fingerprints and static DD checks are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Application tests: NOT_RUN — documentation-only scope and API #22 is not wired.
- Context validator: NOT_REQUIRED — no canonical context page or manifest changed.
