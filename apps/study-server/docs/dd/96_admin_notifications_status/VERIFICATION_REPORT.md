# VERIFICATION_REPORT — Study API #96 Admin notification status

## Scope

Implementation review of API #96 against catalog row #96, AC-36 diagram, checked-in candidate DDL and current Study source. Includes local fake-DB HTTP/OpenAPI tests, linked AC-36 notification regression, Study Server full suite, Ruff, DD static checks and agent-context validation. Live database/deployment was not checked.

## Deliverable manifest

| File | Vai trò |
|---|---|
| `00_Cover.md` | Cover |
| `01_Lich_su.md` | Lịch sử |
| `02_Overview.md` | Overview |
| `03_Request.md` | Request |
| `04_Response.md` | Response |
| `05_Data_Mapping.md` | Data mapping |
| `06_Error.md` | Error |
| `07_table.md` | Read-only table source record |
| `PLAN_RESULT.md` | Plan, decisions and change boundary |
| `OPEN_QUESTIONS.md` | Remaining source/owner decisions |
| `VERIFICATION_REPORT.md` | Implementation verification |
| `AC-36_MACRO_REVIEW.md` | Cross-API review #92–#96 |

## Verification results

| Check | Result | Status |
|---|---|---|
| Direct contract | GET/path/Admin Bearer/no body-query/`ApiEnvelope<Notification>`/200 and exact 401/403/404/500 retained | PASS — SOURCE/OPENAPI |
| AC-36 flow | Delivery aggregate is read before returning status; response has no added count fields | PASS — SOURCE REVIEW |
| API #96 tests | 16 focused HTTP/OpenAPI tests passed | PASS — LOCAL FAKE DB |
| Linked #92–#96 tests | 103 notification-flow tests passed | PASS — LOCAL FAKE DB |
| Full Study Server suite | 1300 passed; one upstream Starlette/httpx TestClient deprecation warning | PASS — LOCAL |
| Ruff | `ruff check app tests` and scoped `ruff format --check` passed | PASS — STATIC |
| OpenAPI | 56 `/api/v1` path templates / 67 operations; #96 exposes only 200/401/403/404/500 and has no requestBody/query parameter | PASS — LOCAL |
| DD package | 12 Markdown files; direct response fields documented; local links/examples/fences/table syntax checked | PASS — STATIC |
| Template appendices | All eight appendix bodies match template-backed #49 after trimming terminal whitespace; edits were confined before the appendix marker | PASS — STATIC |
| Context manifest | API #96 module/test paths registered; validator reported only the known missing DB Admin scope files outside Study | PARTIAL — OUT-OF-SCOPE BASELINE |
| Live DB/deployment/provider | Not checked; fake DB tests do not prove schema availability, migration application or delivery-worker behavior | NOT_CHECKED |

## Preserved discrepancies and limits

- Catalog #96 returns `Notification` while AC-36 separately calls for reading a delivery aggregate. Runtime maps aggregate status into existing `channels/status`; it does not return queued/sent/failed counts.
- Legacy BIGINT `notifications` and `notification_deliveries` are local candidates reused from API #92. V1-PILOT UUID learner tables are not used. No live schema or migration deployment is verified.
- QUEUED/FAILED/SENT precedence, positive-int64 parsing, malformed-ID-to-404, no-delivery-to-404 and `EMAIL`/`PUSH` values are `DERIVED` from adjacent local source, not owner-approved catalog rules.
- Fine-grained AC-36 permission, retry/recipient grain, enum approval and #93 Operation bridge remain open; DD stays `Draft — Needs Confirmation`.
- The repository-wide context validator exits nonzero because `.agents/db-admin/` and `apps/db-admin-*` sources listed by the manifest are absent in this checkout. It reported no missing API #96 or Study Server context/source path.
