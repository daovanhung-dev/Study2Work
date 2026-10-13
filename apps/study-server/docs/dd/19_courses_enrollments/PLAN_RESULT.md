# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | 19 |
| API name | Tạo quyền học |
| Endpoint | POST /api/v1/courses/{course_id}/enrollments |
| Document status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Output folder | apps/study-server/docs/dd/19_courses_enrollments/ |
| Archive | apps/study-server/docs/dd/19_courses_enrollments.zip |
| Core sheets | 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_enrollments_insert.md, 08_lesson_progress_insert.md |
| Supporting documents | OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md |
| Runtime status | UNWIRED / NOT_FOUND — no Study route/module/query/test found for API #19. |

## Basis and expected behavior

- Canonical contract: [list_api.md](../../../../../docs/lists/list_api.md) marks the API catalog APPROVED_DESIGN_CONTRACT and defines Student Bearer JWT, the endpoint/request notation, ApiEnvelope<Enrollment>, HTTP 201, and errors 401/403/404/422/409/500.
- Flow: [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) maps API #19 to AC-12.
- AC-12: [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) routes free courses directly to API #19 and paid courses after successful payment; the API step says to insert Enrollment and initialize Progress in a transaction with duplicate prevention.
- Logical response schema: Enrollment is id:int64, course_id:int64, user_id:int64, status:EnrollmentStatus, enrolled_at:date-time, and optional completed_at.

## Current behavior

- Current Study route composition: [v1.py](../../../app/api/v1.py) does not register API #19.
- Route/test context: [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) and [tests.md](../../../../../.agents/server-study/tests.md) do not list an API #19 route or test.
- Focused source inventory found no API #19 module, enrollment query or lesson-progress initialization flow under apps/study-server/app or apps/study-server/tests.
- Current Study JWT helper [auth.py](../../../app/utils/auth.py) parses numeric sub to int and reads roles; this is current shared behavior, not API #19 implementation.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql), [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) and [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) are checked-in design evidence; live metadata is not verified.

## Tables read

- courses — candidate lookup for resource/eligibility; exact API #19 predicate SOURCE_REQUIRED.
- enrollments — logical state/duplicate lookup by user and course; exact status policy SOURCE_REQUIRED.
- lessons — candidate lesson set for Progress initialization; selector/cardinality SOURCE_REQUIRED.

## Tables write

- enrollments — DESIGN_ONLY INSERT; see [07_enrollments_insert.md](./07_enrollments_insert.md).
- lesson_progress — DESIGN_ONLY INSERT of one or more rows; see [08_lesson_progress_insert.md](./08_lesson_progress_insert.md).

## Source coverage

| Source | In-scope units reviewed | Result |
|---|---|---|
| [list_api.md](../../../../../docs/lists/list_api.md) | Catalog conventions, reusable ApiEnvelope/Enrollment schema, API #19 row and declared business codes | Read; contract fields preserved. |
| [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) | AC-12 mapping | Read; API #19 trace confirmed. |
| [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | AC-12 actor, precondition, nodes, edges and error/alternate flow | Read; free/paid branch and transaction intent captured. |
| [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) | enrollments and lesson_progress sections, relations, methods and column descriptions | Read; both are DESIGN_ONLY and runtime method is NOT_FOUND. |
| [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) | Enrollment, Lesson, Progress entities and relationships | Read; logical relationships confirmed. |
| [DB.sql](../../../../../infra/postgres/study-server/DB.sql) | users/courses/lessons/enrollments/lesson_progress DDL | Read; schema/design evidence only. |
| Current Study route/auth/test sources | v1.py, auth.py, route context, test context and focused app/tests inventory | Read; API #19 is UNWIRED / NOT_FOUND. |
| createDD-markdown | Skill, eight Markdown template files and API #16–#18 recent DD/worklogs | Read; template and recent delivery convention followed. |

## Assumptions

- Scope is documentation-only for Study Server API #19.
- API #19's request, response, status codes and business codes remain exactly as the current approved design contract declares.
- AC-12's transaction intent covers both Enrollment and Progress mutations; exact runtime transaction implementation is not claimed.
- Unresolved request fields, duplicate rules, schema discrepancies and Progress values remain in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- No runtime, route, API catalog, diagram, DB schema, migration, enum or business-code source is changed.

## Conflicts and open gaps

- Request repeats course_id in path/body and uses the phrase user from JWT:string; exact wire identity mapping is unresolved.
- AC-12 requests duplicate prevention, but DB.sql has no unique enrollment pair constraint or idempotency policy.
- AC-12 says INIT Progress but does not identify lessons, row cardinality, initial values or behavior for an empty lesson set.
- DB_UNICA_TABLES says four user/course/lesson foreign keys are required; DB.sql does not specify NOT NULL on them.
- EnrollmentStatus values, initial status, timestamp source and optional completed_at policy are not defined.
- API #19 internal eligibility checks and the resource represented by 404 remain unresolved.

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) for decision requests.

## Verification result

- DD content, links, Markdown tables, JSON examples and archive integrity: see [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
- Study application tests: NOT_RUN — API #19 is not wired and the approved scope is documentation-only.
- Context validator: NOT_REQUIRED — no canonical .agents context page or manifest was changed.

