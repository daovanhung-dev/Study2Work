# API DD Checklist - LEARN-PATH-002

| Field | Value |
|---|---|
| API code | `LEARN-PATH-002` |
| Module | `LEARNING` |
| Status | `DRAFT` |
| Updated | `2026-07-02` |
| Worklog | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` |

## Business Readiness

- [x] API exists in `docs/checklists/API.md` canonical section.
- [x] BD section, business rules and diagrams are linked.
- [x] Study-only scope is explicit.
- [x] Open questions are listed with owner/date.

## Contract Readiness

- [x] Method and endpoint are copied from API checklist.
- [x] Auth scheme, role, permission and ownership/scope are explicit at draft level.
- [x] Request fields cover path, query, header, body and auth context where source allows.
- [x] Response examples are valid JSON.
- [x] Success and error envelopes include `businessCode`, `timestamp` and `traceId`.

## Runtime Readiness

- [x] DataMapping lists known read/write tables from checklist and BD data dictionary.
- [x] Transaction boundary is explicit at draft level.
- [x] Idempotency and concurrency are defined or marked as review-needed.
- [x] Audit log and outbox/event/job behavior are defined where source mentions them.
- [x] Retry/DLQ behavior is defined at draft level for async work.

## Test Readiness

- [x] Happy path test is defined.
- [x] Validation failure tests are defined.
- [x] Authentication/authorization/ownership tests are defined.
- [x] State transition tests are defined where relevant.
- [x] Dependency failure and retry tests are defined where relevant.

## Open Questions

| ID | Owner | Status | Question |
|---|---|---|---|
| LEARN-PATH-002-OQ-001 | BA/PO + Tech Lead | OPEN | Xác nhận schema request/response chi tiết trước khi chuyển DD sang IN_REVIEW hoặc APPROVED. |

## Approval

| Role | Reviewer | Status | Date | Note |
|---|---|---|---|---|
| BA/PO | `TBD` | `PENDING` | `2026-07-02` | Review business scope, request schema and rule completeness. |
| Tech Lead | `TBD` | `PENDING` | `2026-07-02` | Review architecture, data mapping, idempotency and async behavior. |
| QA | `TBD` | `PENDING` | `2026-07-02` | Review testability, negative cases and safe error messages. |
