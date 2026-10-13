# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #20 — GET /api/v1/users/me/courses |
| Output | apps/study-server/docs/dd/20_users_me_courses/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Runtime implementation | UNWIRED / NOT_FOUND — current Study router/module/test chưa có API #20 |
| Packaging | Markdown folder; không tạo ZIP theo Study workflow |

## Template fingerprints

SHA-256 của tám file Markdown baseline được dùng:

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Source coverage

| Source | Reviewed | Evidence/role |
|---|---:|---|
| docs/lists/list_api.md | Yes | API #20 request/response/status/error contract and reusable ApiEnvelope, UserProfile, Course, Enrollment schemas. |
| AC_UNICA/00_AC_API_INDEX.md | Yes | AC-12/AC-13 route mapping. |
| AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Yes | AC-13 actor, API sequence, Enrollment/Course join, API #21 progress call, client merge and empty state. |
| DB_UNICA_TABLES.md | Yes | enrollments/courses relations and API #20 query status DESIGN_ONLY. |
| DB.sql | Yes | Checked-in DDL for enrollments, courses, lessons and lesson_progress; not live-schema proof. |
| Current Study route/auth/response source | Yes | v1.py, shared auth helper, current response envelope and API #4 UserProfile model; no API #20 endpoint. |
| Current Study module/test inventory | Yes | No API #20 module or focused test found. |
| createDD-markdown and DD_API_Template_MD | Yes | Skill and all eight template files inspected; fingerprinted above. |
| Prior docs worklogs | Yes | Selector-selected #16–#18 and directly relevant #19 worklog reviewed. |

## Contract checks

- [x] API ID, method, endpoint, query fields and role match the approved design contract.
- [x] Response type ApiEnvelope<UserProfile> and status/business codes are preserved.
- [x] Catalog UserProfile vs current API #4 model difference (bio) is recorded; no API #20 model shape is inferred.
- [x] AC-13 progress remains a separate API #21 call; no progress percentage is added to API #20.
- [x] Enrollment/Course join is recorded as design flow, not runtime implementation.
- [x] status enum/target, page semantics, empty-result wire shape and JWT-to-enrollment binding remain open.
- [x] Expected behavior and current behavior are kept separate.
- [x] Runtime status is UNWIRED / NOT_FOUND; no runtime test result is claimed.
- [x] No catalog, diagram, schema, migration or application source was changed.

## Structural checks

- [x] Eight sheets are present in template order, including 07_table.md marked N/A — READ-ONLY API.
- [x] OPEN_QUESTIONS.md, PLAN_RESULT.md and VERIFICATION_REPORT.md are present.
- [x] Markdown tables have consistent row widths.
- [x] JSON examples parse; request example is HTTP only because GET has no body.
- [x] Relative links resolve and declared open-question anchors exist.
- [x] Code fences are paired; no trailing whitespace was found in the authored DD files.
- [x] No ZIP was created.

## Output fingerprints

SHA-256 of authored DD and supporting documents. This report is excluded to avoid a self-referential digest.

| File | SHA-256 |
|---|---|
| 00_Cover.md | beedbfc23588ca1207a46c4cf29317a5face42a40bb58602ca392ca83e96f695 |
| 01_Lich_su.md | 16a595f61f4efdba46438743ff75ca7b5cea94c66801471eb4e5b354e320d6c3 |
| 02_Overview.md | bc2c801cd6c2375bea46ca054bcba3185c9a22e680c99c1c326e6f6d331a01cd |
| 03_Request.md | 29eb378889ec72f4e5a4288a7ec6853840954c1e545ef902cc99d161ce0bcffe |
| 04_Response.md | a834211ccdbf18403952e4657bc6cc403a7d9771cc3d60e3f50843fa3f7b7650 |
| 05_Data_Mapping.md | 56dafd6fd77e66b2e9f3f1b4b0f92b41f6767c120552af386eca7954dfd8c16b |
| 06_Error.md | 7356d3bf76e79fdb3c356281a35dd145c9fd56172fa064a96719b48748b977e8 |
| 07_table.md | fb89a668e1d420630168a1f6a0c577570e5ea377a48454972d45a4de65bae320 |
| OPEN_QUESTIONS.md | ecdf5e667ee12706301f1ecc4f9b1b0826b38cacaa3f17cd505129983746855d |
| PLAN_RESULT.md | a656cb09795a5465e3372d4274f0a14fe82a1d536470faa63bdbbf95bfc87fd0 |

## Verification executions

| Check | Result |
|---|---|
| API #20 route/module/test inventory | NOT_FOUND — read-only inventory check; endpoint is not wired. |
| Markdown structure/table/code-fence/JSON/link checker | PASS — STATIC_VALIDATION_OK; 11 Markdown files, eight ordered sheets and three reports. |
| Authored-file whitespace check | PASS — no trailing whitespace in DD files. |
| git diff --check | PASS — tracked diff has no whitespace errors. |
| Study runtime tests | NOT_RUN — DD-only scope; API #20 is not wired. |
| Context validator | NOT_REQUIRED — no canonical context page or manifest changed. |

## Known gaps retained

- Response generic is UserProfile while AC-13 needs a course list; field projection remains unresolved.
- Catalog UserProfile includes optional bio while current API #4 model omits it; API #20 has no model to resolve the difference.
- status filter target and enum values are not defined.
- page parameter has no page-base, size, ordering or PageMeta contract.
- AC-13 empty state has no corresponding API wire-shape definition.
- JWT sub parsing exists in a shared helper, but API #20 binding to enrollments.user_id is not runtime-verified.
- DB table query documentation is DESIGN_ONLY; live database metadata was not checked.

## Final assessment

PARTIALLY COMPLETED / NEEDS USER DECISION — DD deliverables preserve the current contract and AC-13 flow, while response shape and query semantics remain open in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
