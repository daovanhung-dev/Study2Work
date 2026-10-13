# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #21 — GET /api/v1/users/me/progress |
| Output | apps/study-server/docs/dd/21_users_me_progress/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Runtime implementation | UNWIRED / NOT_FOUND — current Study router/module/test chưa có API #21 |
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
| docs/lists/list_api.md | Yes | API #21 endpoint, Student Bearer JWT, raw query declaration, response type, codes and reusable schemas. |
| AC_UNICA/00_AC_API_INDEX.md | Yes | API references for AC-13 and AC-18. |
| AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Yes | AC-13 API #20/#21 sequence, client merge and empty state; AC-18 API #21 aggregate and separate #37/#38 calls. |
| DB_UNICA_TABLES.md | Yes | lesson_progress fields/relations and query #21/#37 status DESIGN_ONLY. |
| DB.sql | Yes | Checked-in DDL for lesson_progress, lessons and courses; not live-schema proof. |
| Current Study route/auth/response source | Yes | v1.py, shared auth helper and current envelope; API #21 is not wired. |
| Current Study module/test inventory | Yes | No API #21 module, route or focused test found. |
| createDD-markdown and DD_API_Template_MD | Yes | Skill plus all eight template files inspected and fingerprinted above. |
| Prior docs worklogs | Yes | Selector-selected #16–#18 worklogs read; no shortage. |

## Contract checks

- [x] API ID, method, endpoint, actor, auth requirement and raw query declaration match the catalog.
- [x] Response type ApiEnvelope<UserProfile> and HTTP/business codes 200/401/403/500 are preserved.
- [x] No 422, 404, query fields, progress fields or business codes were added.
- [x] AC-13 keeps Course loading and progress loading separate and documents client-side merge.
- [x] AC-18 keeps API #37 course detail and API #38 achievements as separate calls.
- [x] lesson_progress and lesson/course relations remain DESIGN_ONLY evidence; no aggregate formula/query is invented.
- [x] Expected behavior and current behavior are kept separate.
- [x] Runtime status is UNWIRED / NOT_FOUND; no API runtime test is claimed.
- [x] No API catalog, diagram, runtime, DB schema or migration was changed.

## Structural checks

- [x] Eight sheets exist in template order; 07_table.md is marked N/A — READ-ONLY API.
- [x] OPEN_QUESTIONS.md, PLAN_RESULT.md and VERIFICATION_REPORT.md exist.
- [x] Markdown tables have consistent row widths; code fences are paired.
- [x] JSON examples parse.
- [x] Relative links resolve and every declared question anchor exists.
- [x] Authored files have no trailing whitespace; git diff --check passes.
- [x] No ZIP was created.

## Output fingerprints

SHA-256 of authored DD and supporting documents. This report is excluded to avoid a self-referential digest.

| File | SHA-256 |
|---|---|
| 00_Cover.md | 5fb889c480fc5ef6e6caeed2f4d54b20512675f1e452ce544c0f13429e72512a |
| 01_Lich_su.md | ca1ff83c9ab53ab7607b57da5db8791aba892de92facac3230bc915e894a52a3 |
| 02_Overview.md | 8375fac2dc232e18545b2d022d33affb1f0791576237ac00d6c5ff2cce56e4f7 |
| 03_Request.md | 42451f2095a3cb38960c5ce8576f3a78e52e7ae65973fa25bc6fd830fc55b34a |
| 04_Response.md | 4b4846172947f3da481e5f872559aca057b75ea58aebe44267c3481c39846cc1 |
| 05_Data_Mapping.md | bf7242d71f653c3162c3d446e2ea3f9f2d97424a4cb6f139a26b099affa2fd49 |
| 06_Error.md | 9ad6e98fa0c37d9b3a399a7e9ec0414c7818cdfc4722dbf80d94438172045bce |
| 07_table.md | 736f1158767a3c9ff76dbe81a7ea5d447750367e1b9b3b1ebdc53219030f5662 |
| OPEN_QUESTIONS.md | edc01a0f97954c9b3b64d3bd231f6f397ee20d5fb1c1d0fe0af08b3ec0481d60 |
| PLAN_RESULT.md | 7636125caf3e138c4113a5ac6463159f0fa5d87020ab03c86833069d5ef5feb5 |

## Verification executions

| Check | Result |
|---|---|
| API #21 route/module/test inventory | NOT_FOUND — read-only inventory check; endpoint is not wired. |
| Markdown structure/table/code-fence/JSON/link checker | PASS — 11 deliverables, eight ordered sheets, 41 local links and anchors, two valid JSON examples, zero structural errors. |
| Authored-file whitespace check | PASS — no trailing whitespace in DD or worklog files. |
| git diff --check | PASS |
| Study runtime tests | NOT_RUN — DD-only scope; API #21 is not wired. |
| Context validator | NOT_REQUIRED — no canonical context page or manifest changed. |

## Known gaps retained

- Query phrase does not define parameter grammar, course_id list serialization or aggregate semantics.
- Aggregate source, scope, formula and rounding are not specified.
- Catalog UserProfile does not define progress payload fields or the client merge key.
- JWT sub to lesson_progress.user_id binding is not verified for API #21.
- AC-13 UI empty state has no API wire-shape definition.
- DB query is DESIGN_ONLY; live database metadata was not checked.

## Final assessment

PARTIALLY COMPLETED / NEEDS USER DECISION — the DD preserves the current catalog and AC flows; unresolved contract decisions are listed in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
