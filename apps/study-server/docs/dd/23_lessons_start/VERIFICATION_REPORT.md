# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #23 — POST /api/v1/lessons/{lesson_id}/start |
| Output | apps/study-server/docs/dd/23_lessons_start/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED — draft created; contract-owner decisions remain open. |
| Runtime implementation | UNWIRED / NOT_FOUND — no API #23 route/module/query/focused test in current Study source. |
| Packaging | Markdown folder; no ZIP per Study Server workflow. |

## Template fingerprints

SHA-256 of the eight Markdown files in the inspected DD_API_Template_MD folder:

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
| docs/lists/list_api.md | Yes | API #23 method, path, actor, request, response and status/business codes. |
| AC_UNICA/00_AC_API_INDEX.md | Yes | AC-14 actor, precondition, postcondition and API sequence. |
| AC_UNICA/AC_02_STUDENT_LEARNING.drawio | Yes | API #23 contract summary and UPSERT status IN_PROGRESS; adjacent access/detail/progress steps. |
| DB_UNICA_TABLES.md | Yes | Candidate lesson/progress design and source status. |
| infra/postgres/study-server/DB.sql | Yes | Checked-in DDL only; lesson_progress columns and absence of user/lesson unique constraint. |
| Current Study router/modules/tests | Yes | Route/module/query/focused test scan; API #23 not found. |
| .agents/server-study/workflows/README.md and context-manifest.json | Yes | Study API DD folder/no-ZIP rule and createDD-markdown skill wiring. |
| createDD-markdown and DD_API_Template_MD | Yes | Skill and all eight template files reviewed; hashes listed above. |
| Prior docs worklogs | Yes | Selector-selected API #16–#18 worklogs read; no shortage. |

## Contract checks

- [x] API ID, method, endpoint, Student Bearer requirement and lesson_id:int64! match the catalog.
- [x] ApiEnvelope<Lesson> and HTTP/business codes 201/401/403/404/422/500 are preserved.
- [x] No query parameter, request body, business code, field, access predicate or validation rule was added.
- [x] AC-14 UPSERT status IN_PROGRESS is documented without inventing key, timestamp, update fields or transaction behavior.
- [x] Catalog response versus diagram's generic ApiEnvelope and HTTP 201 versus UPSERT are recorded as unresolved.
- [x] Checked-in DDL is marked design-only; live schema and runtime behavior are not asserted.
- [x] Expected behavior and current behavior are kept separate; runtime status is UNWIRED / NOT_FOUND.
- [x] No runtime, API catalog, diagram, DB schema or migration was changed.

## Structural checks

- [x] Eight sheets are present in template order; 07_table.md records the candidate write and unresolved mapping.
- [x] OPEN_QUESTIONS.md, PLAN_RESULT.md and this report are present.
- [x] Markdown tables/code fences/JSON examples and relative links/anchors were checked.
- [x] Authored documents and worklog were checked for trailing whitespace; git diff --check passes.
- [x] No ZIP was created.

## Output fingerprints

SHA-256 of authored DD/supporting documents. This report and the worklog are excluded to avoid self-reference.

| File | SHA-256 |
|---|---|
| 00_Cover.md | ca388627eee7e360a463066281262fb443599ad137417d63918540a2afd5027d |
| 01_Lich_su.md | 943fcf55926ec83f966d4ed2eaf1ae484d59e9b7c193aea866c57d2e82962beb |
| 02_Overview.md | e9f76c5a705e30b8bcd679341f76733ee1147f8b8b096483cdec308794e60345 |
| 03_Request.md | 98522d12652813e7af9c649a8576716b90aa60555088e5dbb2626094f406f706 |
| 04_Response.md | c88677c9c66a4d0e04db271b9905cedc3d9f5703cdd66aaefdb10a4fd2967603 |
| 05_Data_Mapping.md | 98feb7c1116ecfd1ccce13462357b9ebb75050e47d25d3b8bfa0c1ab5669ab05 |
| 06_Error.md | 6f7f0073c53ffc498da3f6af17becc606a0d028077a574b6c9b1a597df3729f3 |
| 07_table.md | 33c2e3e04cfa0a3d39755e0fbda560021a5256627fbc0bf484e3598447ccde19 |
| OPEN_QUESTIONS.md | 85f9771e97d5e5dbb18f6dcd225ed4075a7d544fee6c328fdab26aaeb4c1238f |
| PLAN_RESULT.md | 66a60c81920193bc1c3213b180bb743087838da516df86d806415c0ac7d968f8 |

## Verification executions

| Check | Result |
|---|---|
| Worklog preflight | PASS — selector returned API #16–#18 worklogs; all three were read. |
| Inline static Markdown/JSON/table/link checker | PASS — 11 files; 8 ordered sheets; 2 JSON examples; relative targets and question anchors resolve. |
| API #23 route/module/query/test inventory | UNWIRED / NOT_FOUND — no endpoint implementation or focused test found. |
| Authored-file whitespace scan | PASS — no trailing whitespace in DD/worklog files. |
| git diff --check | PASS. |
| Study Server application tests | NOT_RUN — documentation-only scope; API #23 is not wired. |
| Context validator | NOT_REQUIRED — no canonical context page or manifest changed. |

## Known gaps retained

- Upsert key/uniqueness and concurrent/repeated-start semantics are unresolved.
- Status transition, preservation/reset behavior and timestamp updates are unresolved.
- ApiEnvelope<Lesson> versus diagram payload and response source/projection need confirmation.
- Direct-call access, enrollment/prerequisite and 403/404/422 semantics need confirmation.
- Transaction/failure contract and live database schema are unverified.

## Final assessment

PARTIALLY COMPLETED / NEEDS CONFIRMATION — this draft preserves the catalog and AC-14 flow without asserting unspecified runtime behavior. Resolve [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) before marking the DD Ready/Final or using it as an implementation contract.
