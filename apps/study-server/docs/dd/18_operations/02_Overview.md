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
| Consumer/Actor | Bearer JWT; Student, Mentor or Admin; caller must own the operation |
| Authentication | Bearer JWT |
| Authorization | Current-source behavior selected for SH-07: Student/Mentor/Admin roles with owner-bound lookup; no Admin ownership bypass |
| Basis | DIRECT — API #18 catalog row, shared Operation schema, operation-tracking section, and AC diagrams; design contract is not runtime-verified |
| Status | Draft — Needs Confirmation for generic lifecycle/result and non-notification producer behavior |
| Completion | SH-07 notification slice reconciled; generic operation scope remains partial |
| Decision status | RESOLVED_FOR_SH-07; generic operation decisions remain open |
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

- Operation — logical resource; current Study source projects notification groups from `notifications` and `notification_deliveries`; generic Operation storage remains unsupported.
- Caller identity and Operation owner relation — current lookup uses the authenticated numeric subject against `notifications.sender_id`; other operation kinds have no mapping.

## Tables write

- N/A — read-only API; no DB mutation is specified.

## Mục chú ý

- Current API #18 path and the shared ID convention, Operation.id and AC diagrams use UUID.
- The current API row and selected SH-07 flow require owner-only access for Student, Mentor and Admin callers; Admin does not bypass ownership.
- OperationKind and OperationStatus values, persistence, lifecycle and per-kind result contents are unspecified.
- The common Operation schema declares result?:Payment while tracking references payment, notification and report-export jobs. The notification projection currently omits `result`; generic per-kind results remain unresolved.
- Study runtime has an API #18 handler, but the checked-in Study schema has no generic operations table; current lookup is notification-specific.

## Assumptions

- This DD documents the Study Server API #18 design contract only.
- The API is read-only because the catalog declares GET and no mutation.
- The Operation lookup and response fields remain logical contract data until storage and query sources are approved.
- Generic operation values, transitions, retention and non-notification owner mapping are not inferred. Notification status and owner mapping follow current source and the 2026-11-21 SH-07 decision.

## Conflicts

- RESOLVED_FOR_SH-07 (2026-11-21): API #18 path is UUID, matching current source, shared Operation schema and diagrams.
- RESOLVED_FOR_SH-07 (2026-11-21): all supported roles remain owner-only; Admin has no ownership bypass.
- RESOLVED_FOR_SH-07: API #93 exposes its accepted notification operation UUID in `meta.operation_id`; AD-20 consumes this field and hands it to notification-only API #18. Generic producer response inconsistencies, including report export, remain.
- SOURCE_REQUIRED: Study physical persistence/query, enums, lifecycle, ownership source and result schema by operation kind.
- SOURCE-BACKED: API #18 route/module/query and dedicated tests exist; the query covers notification outbox rows only. No generic Study operations table is defined.
- NOT_VERIFIED: Checked-in SQL does not prove live database metadata or deployment state.

## Current source audit (2026-11-21)

- `GET /api/v1/operations/{operation_id}` is registered in `app/api/v1.py`; OpenAPI declares a UUID path. The Shared validator passes `STUDENT`, `MENTOR`, and `ADMIN` to the shared JWT guard, then the query binds both UUID and authenticated owner ID.
- The current view projects notification operations only, with `kind=NOTIFICATION_DISPATCH` and `QUEUED`/`FAILED`/`SENT` status mapping from notification delivery rows. It does not implement a generic operation store or payment/export lifecycle.
- A missing required `role` argument in the auth call was corrected. The dedicated API #18 HTTP suite passed 8 tests in this task; fake DB behavior does not verify live schema or deployment.
- For the approved SH-07 scope, selected behavior is UUID path, Student/Mentor/Admin role eligibility, caller-owner lookup, and 404 for absent/non-owned operations; other roles return 403. The DD remains Draft for generic operation persistence/lifecycle, per-kind results and broader producer contracts.

## Security note

- Keep Bearer JWT authentication and current-source 401/403/404/500 branches.
- Require the authenticated caller to own the notification Operation; Admin has no ownership bypass.
- A wrong-owner lookup returns 404 and does not expose operation existence.
- Do not expose database errors or internal details in the response.

## Performance note

- No polling interval, cache policy, rate limit, retention window or query SLA is specified.
- No physical index can be recommended without an approved Study operations schema and query source.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md.
- Sheet logic: Overview.
