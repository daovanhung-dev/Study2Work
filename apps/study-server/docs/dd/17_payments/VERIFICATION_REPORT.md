# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #17 — POST /api/v1/payments |
| Output | apps/study-server/docs/dd/17_payments/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Runtime implementation | UNWIRED / NOT_FOUND — không có route/module/query/test API #17 |

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

## Template comparison

- Eight baseline files were copied in original order and use the actual template headings/table structures.
- Excel cell dump sections were replaced by source-template pointers, matching the existing API #16 DD convention.
- Template source remains unchanged.

## Source coverage

| Source | Read/parsed | Role |
|---|---:|---|
| docs/lists/list_api.md | Yes | Approved API #17 contract, shared Operation/Payment schemas and API #18 row |
| AC_02_STUDENT_LEARNING.drawio | Yes | AC-12 paid/free flow, gateway outcomes, API #18 UUID path |
| DB_UNICA_TABLES.md | Yes | payments design fields/relationships and DESIGN_ONLY status |
| DB_UNICA_ERD.drawio | Yes | ERD V1 payment relations and Order limitation |
| infra/postgres/study-server/DB.sql | Yes | Checked-in payments column types/nullability; no orders/operations |
| .agents/server-study/database.md | Yes | Current DB evidence boundary/live metadata status |
| apps/study-server/app/api/v1.py and declared-routes.md | Yes | Current route surface; API #17 absent |
| apps/study-server/app and tests scan | Yes | No API #17 payment/order/operation implementation/test found |
| API #16 OPEN_QUESTIONS.md | Yes | Carried-forward Order/provider/amount gaps |
| DD_API_Template_MD/* | Yes | Ordered 8-sheet baseline and SHA-256 fingerprints |
| createDD_MARKDOWN_SKILL.md | Yes | Authoring, traceability, review and delivery gates |

## Contract checks

- [x] API ID, method, endpoint, Student Bearer JWT and request fields match list_api.md.
- [x] Response is ApiEnvelope<Operation>; reusable Operation and Payment fields are listed individually.
- [x] Success is HTTP 202 DESIGN_OPERATION_ACCEPTED.
- [x] Error cases retain only HTTP 401/403/422/503/500 and catalog business codes.
- [x] AC-12 places API #17 in paid-course branch after Order; success continues, failure/cancel stops.
- [x] API #18 operation_id uuid/int64 discrepancy is recorded without choosing a type.
- [x] Order/payment association, provider/gateway, amount/currency and Operation gaps remain SOURCE_REQUIRED.
- [x] payments columns are limited to checked-in schema; no orders/order_id/operations physical table is invented.
- [x] DB.sql vs DB_UNICA_TABLES nullability discrepancy for user_id/course_id is recorded.
- [x] Expected design and current runtime/schema status remain separate.
- [x] No runtime, catalog, schema, migration or diagram changes were made.

## Structural checks

- [x] Eight template sheet files present in baseline order.
- [x] YAML front matter present for all eight sheets.
- [x] JSON examples parse.
- [x] Markdown table column counts are consistent.
- [x] Relative file links and anchors resolve.
- [x] Code fences are closed.
- [x] No trailing whitespace in DD/worklog.
- [x] Placeholder values are explained and not presented as accepted provider/enum values.
- [x] Output fingerprints recorded below.
- [x] ZIP includes all 11 Markdown deliverables and passes unzip -t.

## Output fingerprint

SHA-256 fingerprints for the 8 sheets and support docs. VERIFICATION_REPORT.md is excluded to avoid self-reference.

| File | SHA-256 |
|---|---|
| 00_Cover.md | d2d7e2bd835524a8a88f34ecd4a724db2c556212ad7bf800a791221df2882ca9 |
| 01_Lich_su.md | 99bc0a2b07ad6e165c9fc01ef1992ad4710e9334bc27a9af806ed469cd054772 |
| 02_Overview.md | d865aaf413f5f4b792cf2fd28e15f1ba165dbf06650b7aa051acb4895414566f |
| 03_Request.md | 16da810806cba9793e47f7c393f4e9c4630090705742aa9d2b3cbf2272847637 |
| 04_Response.md | 76572d21547ad2a2b0e00e531c6b5007193b7dd95cda8557d7f07577b58d5980 |
| 05_Data_Mapping.md | b4808262a129d606f3a4cc40742bc1bd039394eae8b66e2012aba2f34b6affd6 |
| 06_Error.md | f0f908d944e4509566b3d1b51127b777a355ff862c8da9d8d7eaaa93aa3b3568 |
| 07_table.md | 73e5571526eea987b4be97bed6592754d5ce8c9ec902242a43b48f00edd28c6e |
| PLAN_RESULT.md | 6c748ab5632a8d70cd008d749733e08f04fb43bc50cbf1797a42a23726f29f55 |
| OPEN_QUESTIONS.md | 3bb23981b0d10a5fa69cfb9264c21e9895eddb54b85b153899d2f2ae6cee8c6e |
| VERIFICATION_REPORT.md | N/A — self-referential fingerprint omitted |

## Runtime checks

- [x] Current route declaration/source has no POST /api/v1/payments.
- [x] No API #17 payment/order/operation module/query/test source found.
- [N/A] Runtime HTTP test — API #17 is not wired.

## Known gaps retained

- Physical Order table and Order-to-Payment association remain SOURCE_REQUIRED.
- Provider values/continuity, amount/currency/user/course mapping and direct-call ownership/eligibility remain open.
- Gateway protocol, idempotency, retry, payment states and transaction boundary are not specified.
- Operation persistence/lifecycle/enums and API #18 operation_id discrepancy remain open.
- payments.user_id/course_id nullability differs between DB.sql and DB_UNICA_TABLES.
- Live database metadata was not checked.

## Source defects preserved

- API catalog remains design-only; it is not treated as runtime proof.
- AC-12 gateway flow is not expanded into an invented callback/state machine.
- Existing API #18 type conflict and DB payment-schema discrepancies are recorded without source edits.

## Introduced defects

- None found by source-consistency and static validation checks.
