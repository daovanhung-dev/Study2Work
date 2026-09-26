# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #15 — GET /api/v1/courses/{course_id}/enrollment-status |
| Output | apps/study-server/docs/dd/15_courses_enrollment_status/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Runtime implementation | NOT_FOUND — current Study router/module/test không có API #15 |

## Template fingerprint

| File | SHA-256 |
|---|---|
| 00_Cover.md baseline | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md baseline | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md baseline | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md baseline | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md baseline | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md baseline | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md baseline | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md baseline | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Source coverage

| Source | Read/parsed | Role |
|---|---:|---|
| docs/lists/list_api.md | Yes | API #15 contract and reusable Enrollment schema |
| AC_02_STUDENT_LEARNING.drawio | Yes | AC-12 sequence and public enrollment-status node |
| 00_AC_API_INDEX.md | Yes | AC-12 API mapping |
| infra/postgres/study-server/DB.sql | Yes | Current checked-in courses and enrollments schema |
| DB_UNICA_TABLES.md | Yes | Enrollment relationship and design-only status |
| apps/study-server/app/api/v1.py | Yes | Current route surface; API #15 absent |
| DD_API_Template_MD/* | Yes | 8-file template baseline |
| createDD_MARKDOWN_SKILL.md | Yes | Authoring and verification gates |

## Contract checks

- [x] API ID 15 matches list_api.md.
- [x] Method and canonical endpoint `/api/v1/courses/{course_id}/enrollment-status` are preserved.
- [x] Plan path discrepancy is retained: one plan line omits `/enrollment-status`; DD follows list_api.md/AC sources.
- [x] Public/no-Bearer contract is preserved.
- [x] Path course_id:int64! is preserved.
- [x] Response ApiEnvelope<Enrollment> is preserved.
- [x] Success 200 DESIGN_RESOURCE_RETRIEVED is preserved.
- [x] Errors 404 DESIGN_RESOURCE_NOT_FOUND and 500 DESIGN_INTERNAL_ERROR are preserved.
- [x] No 401/403/422/409 is invented for the contract.
- [x] No route, source code, migration, schema, column, index or business code was created.

## Structural checks

- [x] 8 sheet files.
- [x] YAML front matter.
- [x] Markdown table column consistency.
- [x] 3 JSON examples parse.
- [x] Relative links resolve; no unresolved anchors were introduced.
- [x] One-field/one-condition/one-error/one-column rules reviewed; unresolved selection rules remain explicitly marked.
- [x] Read-only DB mapping is explicit and does not create mutation mapping.

## Output fingerprint

| File | SHA-256 |
|---|---|
| 00_Cover.md | 6e343de974da6160692237122c0d59463a9f1337ac30c757517f482ae6c69c9c |
| 01_Lich_su.md | 52cf4c25936b523a22ba64dbe676fd042ea01e4479c088d55af3e6c5aa27e02b |
| 02_Overview.md | 7b13dc7bb284e0db7f47c9d46b844f1b6bdae0ee6cca3fb45caf979f37a96626 |
| 03_Request.md | dce51371a0865eb0069cc78835e4dfdd0ca5eddf4c3c27585cecc7ab4be6966a |
| 04_Response.md | 959960f4c76796dc7202bb7df01fda139ea0e4f29fd9a78171b88ac679c5dcd5 |
| 05_Data_Mapping.md | 01722c22ad7b51914cbf2f2b85cb13454c05aadc1fa2eb97926bf61c86a0ccd7 |
| 06_Error.md | 06de8fed4a0a1930adcc7f485ea2d159d1af3f654db84dd3ec70c6501e094fea |
| 07_table.md | 1142131cdccf538100b4ba8441bd45ceabdc5695972898e49d4d8b0dbf9adc0f |
| PLAN_RESULT.md | 8c2d3fb8910ba75c6d3fa60ea1a7aa3ba4ef4571a343e0477af33ff51ea9ff47 |
| OPEN_QUESTIONS.md | 13fac794a4c8f304aa2b537f2909724301196f5c0856cd8ee06252a8afea9908 |
| VERIFICATION_REPORT.md | N/A — self-referential fingerprint omitted |

## Runtime checks

- [x] app/api/v1.py has no route for API #15.
- [x] No API #15 module/query/view/model/test was found.
- [x] Current status is UNWIRED / NOT_FOUND.
- [x] Current schema source has courses and enrollments columns used by the response.
- [N/A] Runtime HTTP test — endpoint is not wired.

## Known gaps retained

- Public contract has no user identity while Enrollment is user-scoped: `SOURCE_REQUIRED / BLOCKING DISCREPANCY`.
- HTTP 404 semantics are not separated between course and enrollment.
- Course PUBLISHED predicate is derived from AC-12, not explicit in API row.
- Multiple enrollment selection/uniqueness is not source-backed.
- EnrollmentStatus enum values are not source-backed.
- Live database metadata has not been verified.

## Verification executions

| Check | Result |
|---|---|
| Static DD check | PASS — STATIC_VALIDATION_OK |
| git diff --check | PASS |
| deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift | PASS — AGENT_CONTEXT_OK |
| Full context drift check | CONTEXT_STALE — repository-wide pre-existing drift across registered scopes; no manifest changes made in docs-only task. |

## Final assessment

PARTIALLY COMPLETED / NEEDS USER DECISION — DD structure and source-backed enrollment columns are documented, while the Public contract cannot yet define a unique enrollment selection without an approved identity/selection rule.
