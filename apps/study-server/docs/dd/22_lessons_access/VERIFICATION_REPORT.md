# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #22 — GET /api/v1/lessons/{lesson_id}/access |
| Output | apps/study-server/docs/dd/22_lessons_access/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED — artifact created; contract-owner decisions remain open. |
| Runtime implementation | UNWIRED / NOT_FOUND — no API #22 route/module/query/focused test in current Study source. |
| Packaging | Markdown folder; no ZIP per Study Server workflow. |

## Template fingerprints

SHA-256 of the eight Markdown files in the inspected `DD_API_Template_MD` folder:

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
| `docs/lists/list_api.md` | Yes | API #22 row and reusable `Lesson`/`ApiEnvelope<T>` schemas. |
| `AC_UNICA/00_AC_API_INDEX.md` | Yes | AC-14 actor, precondition, postcondition and endpoint sequence. |
| `AC_UNICA/AC_02_STUDENT_LEARNING.drawio` | Yes | AC-14 enrollment/prerequisite check, allowed branch, denied 403 + reason, and separate APIs #23/#24/#25. |
| `DB_UNICA_TABLES.md` | Yes | Lesson/enrollment relations and current design/runtime status. |
| `DB_UNICA_ERD.drawio` | Yes | Candidate relationships for lessons, courses and enrollments. |
| `infra/postgres/study-server/DB.sql` | Yes | Checked-in DDL only; live schema is not asserted. |
| Current Study router/auth/tests | Yes | `v1.py`, shared `auth.py`, and route/module/test inventory; API #22 absent. |
| `createDD-markdown` and `DD_API_Template_MD` | Yes | Skill and all eight template sheets inspected; baseline hashes listed above. |
| Prior docs worklogs | Yes | Selector-selected #16–#18 worklogs read; no shortage. |

## Contract checks

- [x] API ID, method, endpoint, Student Bearer requirement and `lesson_id:int64!` match the catalog.
- [x] `ApiEnvelope<Lesson>` and HTTP/business codes 200/401/403/404/500 are preserved.
- [x] No query, request body, 422 code, new response field or new business code was added.
- [x] AC-14 enrollment/prerequisite and 403 + reason are described without inventing the predicate or reason payload.
- [x] Candidate lesson/enrollment schema mappings are marked design-only; no SQL or runtime query is claimed.
- [x] API #22 access check remains separate from API #23 start and API #24 content retrieval.
- [x] Expected behavior and current behavior are kept separate.
- [x] Runtime status is UNWIRED / NOT_FOUND; no API #22 application test is claimed.
- [x] No runtime, API catalog, diagram, DB schema or migration was changed.

## Structural checks

- [x] Eight sheets are present in template order; `07_table.md` is N/A — READ-ONLY API.
- [x] `OPEN_QUESTIONS.md`, `PLAN_RESULT.md` and this report are present.
- [x] Markdown table widths and code fences are consistent.
- [x] JSON examples parse; examples are labeled illustrative where the wire shape is unresolved.
- [x] Relative links resolve and each declared question anchor exists.
- [x] Authored DD and worklog files have no trailing whitespace; `git diff --check` passes.
- [x] No ZIP was created.

## Output fingerprints

SHA-256 of authored DD/supporting documents. This report is excluded to avoid a self-referential digest.

| File | SHA-256 |
|---|---|
| 00_Cover.md | a24446dba60493900e97d7d8da56ea443eaefb03db0e1695fc726230808795f1 |
| 01_Lich_su.md | f0817d36b19e4c5531742ff0d9594e87da1fd79b907448169583a9ae53fb0b03 |
| 02_Overview.md | 1b1efe0f962eec94164c3dbde3af7ccf08cf5052d6deb55389b0eb1544cf27c6 |
| 03_Request.md | a1568a5b9b69702769023601b0ce8e581631e10d67c34756e84aaeb9aef6c428 |
| 04_Response.md | 0e53e7e13f8a9a7f714fc78eaf383053259fa3081c03f80c51c91cc95abe27a6 |
| 05_Data_Mapping.md | ee59f56651fb65c8ffc6a41d98ea0538581e57effdf7c9be81e72a9ca6a21c16 |
| 06_Error.md | 34ea67fdea0e61b68f3e61f5031387fae1cd035df1e9e10051ec820675948bf3 |
| 07_table.md | 69537fc71a3e816bb9bb0494185896890bddcf15cf569b4a24dd5b22eb61784d |
| OPEN_QUESTIONS.md | 51ac340d5bd921e19d4c4bddfc43b313b8203c7a0c41e5c636601ad90ae3634d |
| PLAN_RESULT.md | 0ad7d7762f8a713eae50b99bbfe5cbdaaa4132a11c3d3b299d3325fcbea81004 |

## Verification executions

| Check | Result |
|---|---|
| Worklog preflight | PASS — selector returned #16–#18; all three logs were read. |
| Inline static Markdown/JSON/table/link checker | PASS — 11 deliverables, eight ordered sheets, two JSON examples, relative targets and anchors checked. |
| API #22 route/module/test inventory | UNWIRED / NOT_FOUND — no current endpoint implementation or focused test. |
| Authored-file whitespace scan | PASS — no trailing whitespace in DD/worklog files. |
| `git diff --check` | PASS. |
| Study Server application tests | NOT_RUN — documentation-only scope; API #22 is not wired. |
| Context validator | NOT_REQUIRED — no canonical context page or manifest changed. |

## Known gaps retained

- Enrollment status eligibility and prerequisite source/evaluation are unresolved.
- JWT subject to enrollment ownership binding is not defined for API #22.
- The 403 “reason” has no field/location/allowed-values contract.
- The 404 resource condition is unspecified.
- Exact query, selected projection, prerequisite data source and live schema status are unresolved.

## Final assessment

PARTIALLY COMPLETED / NEEDS USER DECISION — the draft preserves the catalog and AC-14 flow. Review [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) and resolve its decisions before marking the DD Ready/Final or using it as an implementation contract.
