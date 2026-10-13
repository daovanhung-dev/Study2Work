# VERIFICATION_REPORT

## Scope

| Item | Result |
|---|---|
| API | #18 — GET /api/v1/operations/{operation_id} |
| Output | apps/study-server/docs/dd/18_operations/ |
| Document status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Current runtime | UNWIRED / NOT_FOUND |
| Archive | apps/study-server/docs/dd/18_operations.zip |

## Template fingerprint

Baseline files are the eight files in .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/. SHA-256 values are recorded after validation.

| File | SHA-256 |
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

| Source | Read | Role/status |
|---|---:|---|
| docs/lists/list_api.md | Yes | API #18 contract, common schemas/codes, producer rows and tracking summary |
| apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md | Yes | AC mapping for AC-12, AC-25, AC-36 and AC-38 |
| AC_02_STUDENT_LEARNING.drawio | Yes | AC-12 API #18 UUID/owner-only contract text |
| AC_03_MENTOR_TEACHING.drawio | Yes | AC-25 tracking reference and UUID/owner-only contract text |
| AC_04_ADMIN_MANAGEMENT.drawio | Yes | AC-36/AC-38 tracking references and UUID/owner-only contract text |
| DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio | Yes | Study design schema; no Operation table |
| infra/postgres/study-server/DB.sql | Yes | Checked-in Study schema; no operations table; live metadata not verified |
| apps/study-server/app/api/v1.py and .agents/server-study/apis/declared-routes.md | Yes | API #18 route absent |
| apps/study-server/tests and .agents/server-study/tests.md | Yes | API #18 test absent |
| infra/postgres/work-server/schema.sql | Yes | Same-named Work table references work_users; no Study mapping established |
| apps/study-server/docs/dd/17_payments/OPEN_QUESTIONS.md | Yes | Operation persistence/lifecycle and ID conflict carried forward |
| createDD_MARKDOWN_SKILL.md and DD_API_Template_MD/* | Yes | Required authoring rules and eight-sheet baseline |

## Contract checks

- [x] API ID, method, endpoint, Bearer JWT, success response and listed status/business codes match the API #18 row.
- [x] API #18 ID type discrepancy is documented without choosing a canonical type.
- [x] Owner-only versus owner/Admin authorization discrepancy is documented.
- [x] Operation enums, storage, lifecycle, owner mapping and result-by-kind gaps are retained.
- [x] Producer response schema mismatch for API #93 and API #103 is retained.
- [x] 403/404 exist as catalog codes; wrong-owner privacy semantics remain open.
- [x] No Work Server table is mapped to Study API #18.
- [x] Current runtime/test/schema state is separated from expected design.
- [x] No runtime, catalog, schema, migration or diagram was changed.

## Structural checks

- [x] Eight template sheets are present in original order.
- [x] Front matter is present on all eight sheets.
- [x] Both JSON examples parse.
- [x] Markdown table column counts are consistent across 28 tables.
- [x] All 28 relative Markdown links resolve.
- [x] Code fences are closed.
- [x] Placeholders in examples and route templates are explained in surrounding text.
- [x] ZIP contains the eight sheets and three support documents and passes integrity check.
- [x] Output fingerprints recorded below.

## Output fingerprint

SHA-256 values for the eight sheets and three support documents will be recorded after validation. This report is excluded to avoid self-reference.

| File | SHA-256 |
|---|---|
| 00_Cover.md | 83fcb277fd4afb823450de79d4fdf5e224c177d1918026534514aabb36d31328 |
| 01_Lich_su.md | 2330d08b6c2a3efb9c40f04f30ae1ea7ce3567abb8c9e5b89b0ec332fcda2ba1 |
| 02_Overview.md | 56c9350e1abfffb9f7e731976657b4d606b5e79334330f6118d5cf9f3e4dd74c |
| 03_Request.md | c7388c9399fee80045e5b6e7fe9c54a54846e6a0a651d10dab5ea25f835b545c |
| 04_Response.md | 625114af4306689a1876fd9424fd9c7d089d2ea0b694d1329e03bc6f1de2a758 |
| 05_Data_Mapping.md | 554aaaf31cd10e00246ab669157fce6cb56c98c7b644c9fcdf1941bb9d916465 |
| 06_Error.md | 1c7154db3a4c54f622f546ed65e38d7b2951e4b2ccba37cb65fc4ea2a2b0016a |
| 07_table.md | 9f6a9526fcf762f908913dc6f12c80f4fea4dc77b91c657389dcbfc619503478 |
| OPEN_QUESTIONS.md | 3be7f28f6587ef37b49f810ba2d368e2a434daaf0437143ce583787e5a690249 |
| PLAN_RESULT.md | 341954bf79bd62cfcb15de286610293a0055d7b808359537008c2c13cbf7d997 |

## Runtime checks

| Check | Result |
|---|---|
| API #18 route/module/query/test scan | UNWIRED / NOT_FOUND |
| Study application tests | NOT_RUN — excluded by plan; endpoint is not wired |

## Known gaps retained

- operation_id int64/UUID discrepancy.
- owner-only versus owner/Admin discrepancy.
- Operation persistence, enum values, lifecycle and owner identity mapping.
- Operation.result Payment schema versus notification/export producers.
- Producer success response mismatch for API #93/API #103.
- 403/404 wrong-owner/missing-resource semantics.

## Verification executions

| Command/check | Result |
|---|---|
| Inline Python structural validator | PASS — 11 expected Markdown files; 8 sheet front matters/orders and headings checked; 2 JSON examples parsed; 28 tables checked; 28 relative links resolved; no fence, table, or trailing-whitespace issues. |
| Source scan of Study app, tests and infra/postgres/study-server/DB.sql | No API #18 route/operation query/test or Study operations table found; expected UNWIRED / NOT_FOUND evidence. |
| unzip -t apps/study-server/docs/dd/17_payments.zip | PASS — prior related archive read and integrity-checked. |
| git diff --check | PASS for tracked diff; new untracked Markdown files also passed the structural validator trailing-whitespace check. |
| Study application tests | NOT_RUN — API #18 is not wired and application tests were excluded by the approved plan. |

## Final assessment

PARTIALLY COMPLETED — the DD package is a traceable draft; contract owner decisions remain before Final status or implementation.
