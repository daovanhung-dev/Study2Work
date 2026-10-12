# VERIFICATION_REPORT

## Scope

| Hạng mục | Kết quả |
|---|---|
| API | #16 — POST /api/v1/orders |
| Output | apps/study-server/docs/dd/16_orders/ |
| Document status | Draft — Needs Confirmation |
| Completion status | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Runtime implementation | UNWIRED / NOT_FOUND — không có route/module/query/test API #16 |

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

- Eight baseline files were copied in the original order and retain their sheet headings and table structure.
- Sample workbook cell dumps were replaced with a short pointer to each baseline template, following the existing API #15 DD convention.

## Source coverage

| Source | Read/parsed | Role |
|---|---:|---|
| docs/lists/list_api.md | Yes | Approved design contract, API #16 row and Order response schema |
| AC_02_STUDENT_LEARNING.drawio | Yes | AC-12 paid/free branch, Order PENDING, API #17 next step |
| DB_UNICA_TABLES.md | Yes | Payments design and absence of orders in ERD |
| DB_UNICA_ERD.drawio | Yes | V1 note does not split orders |
| infra/postgres/study-server/DB.sql | Yes | Checked-in schema contains payments, no orders |
| apps/study-server/app/api/v1.py and declared-routes.md | Yes | Current route surface; API #16 absent |
| apps/study-server/app/core/responses.py | Yes | Current envelope/error default convention; not API #16 runtime proof |
| apps/study-server/app and tests search | Yes | No API #16 route/module/query/test source found |
| DD_API_Template_MD/* | Yes | Ordered 8-sheet baseline and source fingerprints |
| createDD_MARKDOWN_SKILL.md | Yes | Authoring, traceability, quality and delivery gates |

## Contract checks

- [x] API ID, method, endpoint, Student Bearer JWT and request fields match list_api.md.
- [x] Response is ApiEnvelope<Order> with fields from the catalog schema.
- [x] Success is HTTP 201 DESIGN_RESOURCE_CREATED.
- [x] Error cases retain only HTTP 401/403/422/500 and their catalog business codes.
- [x] AC-12 places logical Order creation with status PENDING in the paid-course branch, before separate API #17.
- [x] PaymentProvider allowed values and purpose remain SOURCE_REQUIRED.
- [x] No Order-to-payments persistence mapping is asserted.
- [x] Expected design and current runtime/schema status are documented separately.
- [x] No runtime, schema, diagram, migration or business-code changes were made.

## Structural checks

- [x] Eight template sheet files are present in baseline order.
- [x] YAML front matter is present for all eight sheets.
- [x] JSON examples parse.
- [x] Markdown table column counts are consistent.
- [x] Relative file links and anchors resolve.
- [x] Code fences are closed.
- [x] No trailing whitespace found in the DD or worklog.
- [x] Placeholder values in examples are explained and are not presented as accepted provider/currency values.

## Output fingerprint

SHA-256 fingerprints for the 8 sheets and support docs. VERIFICATION_REPORT.md is excluded to avoid self-reference.

| File | SHA-256 |
|---|---|
| 00_Cover.md | 0d0ad2fa57e78ac6a9fab3860db203c79e7668c8f29b5a201ea749bce01e5241 |
| 01_Lich_su.md | f9eb9e5f87d60ab4da8036531db440e3c1e1e12b5a809ae23b3535f724918586 |
| 02_Overview.md | 3820c7bb7d5c0a0200f6840f168f5c65b4b773b4a2b2aac662745a9e11d03b90 |
| 03_Request.md | 23cabf5d7ad7a22cb9f6d5ce248e112b9e36e331fedc9f4df583d40e9af6c657 |
| 04_Response.md | ddb823d6b705733ee2524783fa4d62097332d39c2569e1c21cdec779847b7be1 |
| 05_Data_Mapping.md | 9de78f6259c7c592086d4d5d72b1b4e6cb40ba13c386e86b61032bd8eebc96af |
| 06_Error.md | db8d25d4a9e43d848b2eb007826ed4edabb9eaf57ef232f70f728591c06819b4 |
| 07_table.md | 52a86cb47d580e4dec067b897368a9f2ed1b1693c8f2808f3b143c7ef4d486eb |
| PLAN_RESULT.md | 7e57e9e6b13b920fcfdcd46725909e379c2551c4569e25fcba51d5fd5f555730 |
| OPEN_QUESTIONS.md | 7cbadd6c1a2e65b4dfbf99c61d753d4c5df74eb4dae969b05a6288c26abd8524 |
| VERIFICATION_REPORT.md | N/A — self-referential fingerprint omitted |

## Runtime checks

- [x] Current route declaration/source has no POST /api/v1/orders.
- [x] No API #16 module/query/test was found under Study app/tests.
- [N/A] Runtime HTTP test — API #16 is not wired.

## Known gaps retained

- Physical Order table, columns, constraints, transaction and idempotency remain SOURCE_REQUIRED.
- PaymentProvider members and relationship to API #17 provider input remain SOURCE_REQUIRED.
- Amount/currency mapping and OrderStatus values beyond PENDING are not defined.
- Direct-call eligibility behavior for free/missing/already-enrolled courses is unresolved.
- Live database metadata was not checked.

## Source defects preserved

- The API catalog remains design-only and is not treated as runtime proof.
- The Order/persistence mismatch, missing PaymentProvider values and missing OrderStatus catalog remain explicit gaps.
- Existing V1 ERD simplification and the current payments-only SQL are recorded without edits.

## Introduced defects

- None found by the structural and source-consistency review.

## Verification executions

| Check | Result |
|---|---|
| Inline static DD validation | PASS — STATIC_VALIDATION_OK for front matter, JSON, tables, relative links/anchors, code fences and whitespace |
| Current-source search | PASS — API #16 route/module/query/test not found |
| Runtime tests | NOT_RUN — endpoint is not wired |
| ZIP package | PASS — archive created; unzip -t reports no errors. |

## Package

- Archive: apps/study-server/docs/dd/16_orders.zip
- Archive check: PASS — all entries tested successfully with unzip -t.

## Final assessment

PARTIALLY COMPLETED / NEEDS USER DECISION — the source-backed contract and AC-12 flow are recorded, while persistence, provider, amount/currency and related behavior gaps remain blocking for runtime implementation.

