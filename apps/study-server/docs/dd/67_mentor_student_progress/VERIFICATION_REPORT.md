# VERIFICATION_REPORT — Study API #67

## Kết quả

- DD status: Draft — Needs Confirmation. Contract response, roster/privacy mapping, progress schema, duplicate handling and summary formula include DERIVED runtime decisions and still need product/schema approval.
- Runtime: GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress is wired through the Mentor route and middleware contract allowlist. It authenticates before database access, checks direct course ownership and ACTIVE Student roster eligibility, and performs read-only lesson progress mapping.
- Runtime response: the singular StudentCourseProgress detail follows AC-26's selected-Student purpose. The diagram/catalog still declare ApiEnvelope<Page<Course>>; this remains an explicit discrepancy, not a catalog change.
- Deliverables: 8 canonical sheets plus OPEN_QUESTIONS, PLAN_RESULT and this report (11 Markdown files).
- AC-26 macro-review: source and HTTP behavior for #65–#67 was reviewed together; the #67 response/schema and business-policy choices remain DERIVED.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector selected 3 coding worklogs (#34, #47, #48); all were read; no shortage. | PASS |
| Plan before coding | Requirement, source trace, discrepancies and eight-step implementation plan were recorded before implementation. | PASS |
| API #67 HTTP suite | 25 passed; includes auth-before-DB, int64 paths, ownership/roster, ordered lessons, missing progress, aggregate, invalid rows, DB errors, read-only behavior and OpenAPI. | PASS |
| Linked #65/#66 regression | 38 passed. | PASS |
| Full Study suite | 723 passed; one upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | Full app/tests lint passed. | PASS |
| OpenAPI | API #67 path present; 37 unique /api/v1 paths and 38 operations. | PASS |
| DD static check | 11 Markdown files; JSON blocks, relative file links, code fences, trailing whitespace and exact template appendix suffixes checked. | PASS |
| Template appendix | All 8 canonical sheets preserve their registered template appendix suffix byte-for-byte. | PASS |
| git diff --check | Passed after implementation and DD/context updates. | PASS |
| Context validator | Deno execution works. With --skip-drift it reports pre-existing missing db-admin context/source paths and links; default run also reports broad dirty-tree source drift. No db-admin changes were made. | BASELINE INVALID |
| Live DB/deployment | Fake-session HTTP tests do not prove deployed schema, database state or deployment behavior. | NOT VERIFIED |

## Output fingerprints — SHA-256

| Sheet | SHA-256 |
|---|---|
| 00_Cover.md | 37adce5d9618145f1fa65f53638eef3dbe97a4bb486ca4c81a70a81a5d5193b5 |
| 01_Lich_su.md | 99543dcae3b06cbd6e541387c444df172b4ef75ac7c9a633f5c7690200933e1a |
| 02_Overview.md | 5ef559f09748188857e78626031034dadc3d74cacd55a857f273d5d134d177cd |
| 03_Request.md | 62d765634481aa44dd2d62678e8de4f8535b177027bb3dc23087e58dc3adc8dc |
| 04_Response.md | 3d00de7d06ce66cddfbdc869b9ce53908cfac0c0d94dd3167915606dab5bc9ad |
| 05_Data_Mapping.md | 6380a7957e518dd51e722b2015be63a1284351fffacfe66693e23be6d259b303 |
| 06_Error.md | ba3be04b09a6317e489d44b1a4fbcf3d4ea9cc4096d6060bba50a25f2a7ef604 |
| 07_table.md | 9c868924b33f358e9a1f2d05706752c2667cadc3179bf9dc58483a2193893c30 |

## AC-26 macro-review

- #65 reports course roster progress; #66 reports course-wide learning-event analytics; #67 returns current lesson progress for one selected Student. The diagram describes UI orchestration and no server-to-server API call.
- #65 and #67 share a source-consistent candidate lesson denominator and floor-average calculation. #66 event counts remain a separate measure; current progress rows are not treated as event evidence.
- The catalog/diagram Page<Course> response and the singular AC-26 detail response do not agree. The runtime follows the DD's DERIVED drill-down proposal while keeping the DD Draft and recording the discrepancy.
- Checked-in legacy BIGINT tables support the local SQL candidate; the separate UUID V1-PILOT schema does not map directly to this int64 API. No live schema or deployed behavior was verified.
