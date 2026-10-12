# PLAN_RESULT

## API result

- API: #18 — Theo dõi tác vụ bất đồng bộ.
- Method/endpoint: GET /api/v1/operations/{operation_id}.
- Document status: Draft — Needs Confirmation.
- Completion: PARTIALLY COMPLETED.
- Decision status: NEEDS USER DECISION.
- Runtime status: UNWIRED / NOT_FOUND — no Study route/module/query/test found.
- Output folder: apps/study-server/docs/dd/18_operations/.
- Archive: apps/study-server/docs/dd/18_operations.zip.
- Sheets: 00_Cover.md, 01_Lich_su.md, 02_Overview.md, 03_Request.md, 04_Response.md, 05_Data_Mapping.md, 06_Error.md, 07_table.md.
- Supporting documents: OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md.

## Basis

- Canonical design contract: API #18 row and reusable schemas in docs/lists/list_api.md.
- Flow coverage: AC-12, AC-25, AC-36 and AC-38 in apps/study-server/docs/diagrams/AC_UNICA/.
- Data design/current boundary: DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio and infra/postgres/study-server/DB.sql.
- Current runtime/test evidence: apps/study-server/app/api/v1.py, .agents/server-study route/test context and scoped source search.
- Prior related DD: apps/study-server/docs/dd/17_payments/ and its OPEN_QUESTIONS.md.
- Authoring baseline: .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ and createDD_MARKDOWN_SKILL.md.

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API row, reusable Operation/Payment schemas, global convention, producer rows and Operation tracking summary.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC mapping for API #18.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12.
- [AC_03_MENTOR_TEACHING.drawio](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — AC-25.
- [AC_04_ADMIN_MANAGEMENT.drawio](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — AC-36 and AC-38.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) and [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — Study design schema has no Operation table.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in Study schema/design only; live metadata is not verified.
- [v1.py](../../../app/api/v1.py), [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) and [tests.md](../../../../../.agents/server-study/tests.md) — current Study route/test boundary.
- [API #17 OPEN_QUESTIONS.md](../17_payments/OPEN_QUESTIONS.md) — existing Operation gaps and ID discrepancy.
- [Work Server schema](../../../../../infra/postgres/work-server/schema.sql) — same table name, separate owner FK to work_users; no shared API mapping established.
- [DD_API_Template_MD](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) and [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — required template and authoring gates.

## Tables read

- Operation — logical schema only; Study physical table/query SOURCE_REQUIRED.
- Caller identity and owner relation — claim-to-owner and storage lookup SOURCE_REQUIRED.

## Tables write

- N/A — read-only API; no mutation mapping is applicable.

## Assumptions

- Scope is documentation only for Study Server API #18.
- Contract conflicts remain open; no int64/UUID or owner/Admin policy is selected.
- Work Server operations table is non-authoritative for Study absent an approved cross-service contract.
- No runtime, API catalog, database, migration, diagram or other scope files are changed.

## Conflicts

- API #18 operation_id is int64 in its row but UUID in the catalog convention, reusable Operation schema and diagrams.
- Authorization differs between owner-only row/diagrams and owner-or-Admin tracking summary.
- Operation result is declared as Payment while tracking includes notification and export jobs.
- Producer catalog rows for API #93 and API #103 do not consistently declare Operation response data.
- Study Operation persistence, enums, lifecycle and physical owner mapping are unresolved.
- API contract lists both 403 and 404 without defining wrong-owner/missing-resource privacy behavior.

## Verification result

- DD structure, template order, front matter, source links, JSON syntax, Markdown tables, code fences and archive integrity: see VERIFICATION_REPORT.md.
- Study application tests: NOT_RUN — API #18 is not wired and application tests were excluded by the approved plan.
