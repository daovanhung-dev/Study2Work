# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 15 |
| API name | Kiểm tra trạng thái enrollment |
| Endpoint | GET /api/v1/courses/{course_id}/enrollment-status |
| Status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/15_courses_enrollment_status/ |
| Basis | DIRECT — approved design contract + AC-12 + checked-in schema evidence |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/query/test API #15 |
| Tables read | courses, enrollments |
| Tables write | N/A — read-only |
| Business code delta | N/A — dùng DESIGN_RESOURCE_RETRIEVED, DESIGN_RESOURCE_NOT_FOUND và DESIGN_INTERNAL_ERROR |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md).
- [AC_02_STUDENT_LEARNING.drawio](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [00_AC_API_INDEX.md](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql).
- [DB_UNICA_TABLES.md](../../../docs/diagrams/DB_UNICA_TABLES.md).
- [v1.py](../../../app/api/v1.py).
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Locked decisions

- Dùng endpoint canonical `/api/v1/courses/{course_id}/enrollment-status` từ list_api.md, AC index và diagram; không dùng path rút gọn bị thiếu suffix trong một dòng của execution plan.
- Giữ Public; no Bearer token theo contract.
- Chỉ nhận course_id từ path.
- Không thêm user identity vào request.
- Chỉ map các cột hiện có của enrollments.
- Không tự chọn enrollment khi có nhiều row.
- Giữ 07_table.md là read-only N/A mapping.
- Không tạo route, source code, migration, column, index hoặc business code mới.

## Open gaps

- User identity/predicate để chọn enrollment trong endpoint Public.
- Semantics của HTTP 404.
- Course visibility predicate PUBLISHED.
- Multiple enrollment selection/uniqueness.
- enrollments.status enum.

## Verification result

- 8 sheet files được author theo template baseline.
- Request Usage, Query, Mutation và Response Source matrices được ghi.
- Expected/current discrepancy và runtime UNWIRED / NOT_FOUND được ghi.
- Static Markdown/JSON/link/template checks được cập nhật trong VERIFICATION_REPORT.md.
