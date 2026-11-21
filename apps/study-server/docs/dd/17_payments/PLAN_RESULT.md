# PLAN_RESULT

## Status

- Document status: Draft — Needs Confirmation.
- Completion: PARTIALLY COMPLETED.
- Decision status: NEEDS USER DECISION.
- Runtime status: UNWIRED / NOT_FOUND — API #17 chưa có route/module/query/test Study.

## Output folder

- Folder: apps/study-server/docs/dd/17_payments/
- Archive: apps/study-server/docs/dd/17_payments.zip
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_table.md.
- Supporting docs: OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md.

## Basis

- Approved design contract: API #17 trong docs/lists/list_api.md.
- Business flow: AC-12 trong apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio.
- Data design evidence: DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, infra/postgres/study-server/DB.sql.
- Current runtime evidence: apps/study-server/app/api/v1.py, .agents/server-study/apis/declared-routes.md, current app/tests scan.
- Authoring baseline: .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ và createDD-markdown v2.0.0.

## Sources

- docs/lists/list_api.md — request/response/auth/status/error contract; reusable Operation and Payment schemas.
- AC_02_STUDENT_LEARNING.drawio — AC-12 paid/free branch, Payment Gateway outcomes and enrollment sequence.
- DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — design-only payment mapping/relationships and V1 limitations.
- infra/postgres/study-server/DB.sql — checked-in payments schema.
- .agents/server-study/database.md — live database metadata not established by checked-in SQL.
- app/api/v1.py and .agents/server-study/apis/declared-routes.md — API #17 is absent from current route surface.
- apps/study-server/docs/dd/16_orders/OPEN_QUESTIONS.md — carried-forward Order/provider/amount gaps.
- .agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md and DD_API_Template_MD/* — required authoring/template baseline.

## Tables read

- Logical Order: API catalog schema; physical table/query SOURCE_REQUIRED.
- payments: candidate design table in DB_UNICA_TABLES/ERD V1 and DB.sql; live runtime availability NOT_VERIFIED.
- Operation store: SOURCE_REQUIRED; no table/service found.
- External Payment Gateway: flow-level dependency only; protocol SOURCE_REQUIRED.

## Tables write

- payments: DESIGN_ONLY INSERT/external payment label from DB_UNICA_TABLES; each physical column is captured without asserting runtime use or missing order_id.
- Operation: logical accepted result; persistence SOURCE_REQUIRED.

## Assumptions

- API #17 runs in AC-12 paid-course branch after API #16.
- Only contract-level fields, codes and flow statements are normative in this draft.
- No runtime, catalog, DB, migration or diagram changes are within the approved scope.

## Conflicts

- Payment.order_id has no physical payments.order_id column; physical orders table is absent.
- API #18 operation_id is uuid in catalog convention/Operation schema/AC diagrams but int64 in the API #18 row.
- DB.sql allows NULL for payments.user_id/course_id while DB_UNICA_TABLES describes them as required.
- Provider values, amount/currency source, gateway behavior and Operation storage/lifecycle are unresolved; see OPEN_QUESTIONS.md.

## Verification result

- Source and contract review: completed.
- Eight template sheets and support documents: created from approved Markdown baseline.
- Markdown/link/JSON/table/fingerprint checks: PASS; final fingerprints are in VERIFICATION_REPORT.md.
- ZIP integrity: PASS — unzip -t 17_payments.zip reported no errors after final packaging.
- Runtime tests: NOT_RUN — API #17 is not wired.
