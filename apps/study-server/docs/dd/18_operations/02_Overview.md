---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 18 |
| Module | STUDENT / LEARNING & INTERACTION; operation tracking is also referenced by Mentor and Admin flows |
| Method | GET |
| Endpoint | /api/v1/operations/{operation_id} |
| Purpose | Tra cứu trạng thái và thông tin của một tác vụ bất đồng bộ đã được chấp nhận |
| Consumer/Actor | Bearer JWT; API row names the operation owner; role and Admin access have a contract discrepancy |
| Authentication | Bearer JWT |
| Authorization | DISCREPANCY — owner-only versus owner-or-Admin; see OPEN_QUESTIONS.md |
| Basis | DIRECT — API #18 catalog row, shared Operation schema, operation-tracking section, and AC diagrams; design contract is not runtime-verified |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | N/A — read-only API; no transaction contract is specified |
| Side effects | N/A — no mutation or external side effect is specified |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #18 row, ApiEnvelope and Operation schemas, common error codes, producer summary and global ID convention.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-12, AC-25, AC-36 and AC-38 traceability.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12 tracking reference and UUID path declaration.
- [AC_03_MENTOR_TEACHING.drawio](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — mentor flow tracking reference and UUID path declaration.
- [AC_04_ADMIN_MANAGEMENT.drawio](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — admin flow tracking references and UUID path declaration.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) and [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — Study design tables; no Operation table is defined there.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in Study schema/design artifact; it has no operations table. Live database metadata is not verified.
- [v1.py](../../../app/api/v1.py), [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md), and [tests.md](../../../../../.agents/server-study/tests.md) — current route/test coverage; API #18 is source-wired and has dedicated local HTTP tests.
- [OPEN_QUESTIONS.md for API #17](../17_payments/OPEN_QUESTIONS.md) — carried-forward Operation persistence/lifecycle and API #18 ID conflict.
- [Work Server schema](../../../../../infra/postgres/work-server/schema.sql) — contains a separate operations table tied to work_users; no shared Study contract was found, so it is not used as this API physical mapping.

## Tables read

- Operation — logical resource from the reusable catalog schema; Study physical table/query is SOURCE_REQUIRED.
- Caller identity and Operation owner relation — physical identity source and lookup predicate are SOURCE_REQUIRED.

## Tables write

- N/A — read-only API; no DB mutation is specified.

## Mục chú ý

- The API row declares operation_id:int64, while the shared ID convention, Operation.id and AC diagrams declare UUID.
- The API row says operation owner; the operation-tracking summary says owner or Admin; diagrams list Student, Mentor and Admin with owner-only access.
- OperationKind and OperationStatus values, persistence, lifecycle and per-kind result contents are unspecified.
- The common Operation schema declares result?:Payment while tracking covers payment, notification and report-export jobs.
- Study runtime has an API #18 handler, but the checked-in Study schema has no generic operations table; current lookup is notification-specific.

## Assumptions

- This DD documents the Study Server API #18 design contract only.
- The API is read-only because the catalog declares GET and no mutation.
- The Operation lookup and response fields remain logical contract data until storage and query sources are approved.
- No value, status transition, polling cadence, retention policy or owner identity mapping is inferred.

## Conflicts

- DISCREPANCY: API #18 path ID is int64 in its row and UUID in the catalog convention, reusable Operation.id and AC diagrams.
- DISCREPANCY: operation access is owner-only in the API row/diagrams but owner-or-Admin in the tracking summary.
- DISCREPANCY: list_api.md producer rows for admin notification and report export do not both declare Operation as success data, while the tracking summary says all producers return Operation.
- SOURCE_REQUIRED: Study physical persistence/query, enums, lifecycle, ownership source and result schema by operation kind.
- SOURCE-BACKED: API #18 route/module/query and dedicated tests exist; the query covers notification outbox rows only. No generic Study operations table is defined.
- NOT_VERIFIED: Checked-in SQL does not prove live database metadata or deployment state.

## Current source audit (2026-11-16)

- `GET /api/v1/operations/{operation_id}` is registered in `app/api/v1.py`; OpenAPI declares a UUID path. The Shared validator passes `STUDENT`, `MENTOR`, and `ADMIN` to the shared JWT guard, then the query binds both UUID and authenticated owner ID.
- The current view projects notification operations only, with `kind=NOTIFICATION_DISPATCH` and `QUEUED`/`FAILED`/`SENT` status mapping from notification delivery rows. It does not implement a generic operation store or payment/export lifecycle.
- A missing required `role` argument in the auth call was corrected. The dedicated API #18 HTTP suite passes 8 tests; the full Study suite passes 1492 tests. These tests use local/fake DB behavior and do not verify live schema or deployment.
- Current implementation is source evidence, not contract approval. The DD remains Draft while ID type, owner/Admin policy, generic storage/lifecycle, per-kind results, producer response and wrong-owner semantics stay open.

## Security note

- Keep Bearer JWT authentication and the catalog-listed 401/403/404 responses.
- Do not decide whether Admin bypasses ownership or how caller identity maps to owner_id.
- Do not expose Operation data for another owner until the authorization contract is resolved.
- Do not expose database errors or internal details in the response.

## Performance note

- No polling interval, cache policy, rate limit, retention window or query SLA is specified.
- No physical index can be recommended without an approved Study operations schema and query source.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md.
- Sheet logic: Overview.
