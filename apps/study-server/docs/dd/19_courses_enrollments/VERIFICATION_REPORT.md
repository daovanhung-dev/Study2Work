# VERIFICATION_REPORT

## Deliverable structure

| Expected item | Result |
|---|---|
| Core DD sheets | 9 Markdown files: template order 00–06, plus one mapping per changed table (07 enrollments INSERT, 08 lesson_progress INSERT). |
| Supporting reports | OPEN_QUESTIONS.md, PLAN_RESULT.md and this report. |
| Output archive | apps/study-server/docs/dd/19_courses_enrollments.zip; integrity checked with unzip -t after final packaging. |
| Document status | Draft — Needs Confirmation; unresolved decisions are linked in OPEN_QUESTIONS.md. |

## Template fingerprints

SHA-256 fingerprints of the complete Markdown template baseline used:

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

The 07_table prototype is instantiated separately for each mutated table, as required by createDD-markdown.

## Output fingerprints

SHA-256 for each authored sheet and supporting document, excluding this report to avoid a self-referential digest:

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | 635e75a49c43b82566d351b3556232c81590acf83a05cf74248b927aac721c58 |
| 01_Lich_su.md | 8842813d59bedf4f2aad687e948bd2249e6549599a097d403694d2232ddb7b0f |
| 02_Overview.md | 2dc7ad7ceeb094bbe22b2c54c6931fabbce0e0528ed4fb0812c142afba3e41a4 |
| 03_Request.md | cdfc8615240bbd2a5fc154822f178a5ad5a891edadb4ea2101dc9677df74bdd0 |
| 04_Response.md | 627aac9d77eba8b374fb5be3bb5943f299467ae8890025828486c3be514fa727 |
| 05_Data_Mapping.md | ba6c51d729f7cbedfcfa2aad64277adfa99cc6b2b909d40d7b1763ff0edffeda |
| 06_Error.md | 5fbfcb649a483cf9fa0ee5fd79c886cd4a094f1c2c7ecf46c202a2c7db14e38d |
| 07_enrollments_insert.md | 3986a5ec4255e6525b90d894de378a9c3a29d08a131b93593cebaa0e91760b06 |
| 08_lesson_progress_insert.md | edf493970b809b9fe9903bbb5b6aebfabebfe3d1944c8d28248252563bd76057 |
| OPEN_QUESTIONS.md | 2cff34471ad2702a30a17ae4d586064ef74a50cbbacd9f9851af4a6ecf8908e5 |
| PLAN_RESULT.md | c685f6b23fdbc34bb791e1eb6d4d915069002eb83523514268bae5940831da4c |

## Verification checks

| Check | Result | Status |
|---|---|---|
| Template order/front matter | Core sheets use the template metadata and preserve Cover, History, Overview, Request, Response, Data Mapping and Error order; database mappings follow as 07 and 08. | PASS |
| Request/response coverage | Path/body/header fields, each Enrollment response field, error pairs, query/mutation/response source matrices and both table mappings are represented. | PASS |
| JSON syntax | Three fenced JSON examples (request, success response and error response) parse as JSON. Placeholder keys/values are explicitly identified as non-contract examples. | PASS |
| Markdown tables and code fences | Table row widths and fenced blocks checked; no malformed rows/fences found. | PASS |
| Relative links and anchors | Local source links, mapping links, open-question links and Data Mapping table-of-contents anchors resolve. | PASS |
| Source defects preserved | Request identity/path-body duplication, unique/nullability gaps, unspecified Progress initialization and runtime absence remain explicitly unresolved. | PASS |
| Scope boundary | No route, API catalog, diagram, DB schema or migration was changed. Runtime tests were not run because API #19 is UNWIRED / NOT_FOUND. | PASS |
| ZIP integrity | unzip -t apps/study-server/docs/dd/19_courses_enrollments.zip reports no compressed-data errors after packaging. | PASS |

## Source conversion coverage

| Source | Units reviewed | Result |
|---|---|---|
| API catalog | API #19 row, shared Enrollment and ApiEnvelope schemas, status/error declarations | Complete for this API. |
| AC material | AC-12 index row, full AC-12 diagram nodes and edges | Complete for the relevant flow. |
| DB design | enrollments and lesson_progress table sections and relevant ERD entities/relationships | Complete for both changed tables. |
| Checked-in SQL | users, courses, lessons, enrollments and lesson_progress DDL | Complete for relevant tables; not live-schema proof. |
| Current Study runtime | API router, auth helper, route context, tests context and focused module/test inventory | Complete for route/auth/test status; API #19 is absent. |
| Authoring baseline | createDD-markdown instructions, all 8 template files, recent API #16–#18 DD/worklogs | Complete for this DD's authoring pattern. |

## Source defects and introduced defects

- Preserved source defects/gaps: DB_UNICA_TABLES vs DB.sql FK nullability; absent enrollment uniqueness; API request identity/path-body ambiguity; missing lesson-set and initial Progress rules; unspecified EnrollmentStatus/timestamp rules.
- Introduced defects: None found by the listed structural checks.
- No source contract or schema was normalized as part of this Draft.

