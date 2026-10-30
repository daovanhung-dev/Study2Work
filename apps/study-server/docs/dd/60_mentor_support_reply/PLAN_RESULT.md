# PLAN_RESULT — Study API #60

## Kết quả plan/implementation

- Task: `coding`; secondary `docs,test`; scope `server-study`; không có dependency cross-scope.
- API: #60 — `POST /api/v1/mentor/support/{request_id}/reply`.
- Deliverable: route, request/response models, validator, SQL constants, transaction view, HTTP tests, Markdown DD và context/worklog updates.
- DD status: `Draft — Needs Confirmation`. Local choices dưới đây là `DERIVED`, không phải business-owner approval.

## Evidence và status

| Source | Bằng chứng | Status |
|---|---|---|
| API catalog row #60 | Method/path, Mentor Bearer, int64 path, required message/attachment refs, HTTP 200 `DESIGN_RESOURCE_UPDATED`, SupportRequest, error set 401/403/404/422/500 | `DIRECT` |
| AC-24 diagram | #60 inserts a support reply; #61 owns resolve decision; #60 does not change status | `DIRECT` |
| API #58 migration 008 and current #58/#59 source | Local BIGINT support tables, course owner relation, shared response and message/attachment projections | `LOCAL_FALLBACK`; live schema unverified |
| API #34 source | UploadAsset numeric IDs and legacy `uploads` metadata; Mentor `LECTURE`, same course and `UPLOADED` constraints | `CURRENT_SOURCE`; live DB/storage unverified |
| API #47 source | Ordered unique int64 IDs encoded as JSON array string; `[]` accepted | `CURRENT_SOURCE`; #60 key remains `DERIVED` |
| DB helper / mutation APIs | Helpers do not commit; caller owns transaction and validates projection before commit | `CURRENT_SOURCE_PATTERN` |
| User direction | Choose a reasonable, easy-to-understand local fallback when contract/DDL conflict remains | `AUTHORIZED_DERIVED_FALLBACK` |

## Local behavior implemented

1. Shared MENTOR guard runs before database access; numeric JWT `sub` is the Mentor user ID.
2. Raw path text is parsed as signed int64; malformed/overflow input returns 422. Valid absent values return 404.
3. The view locks `support_requests`, validates joined course/student projections, returns missing 404 and another direct owner 403.
4. `message` must be nonblank after `strip()` but the original string is stored. `attachment_refs` must be a strict string containing a JSON array of unique signed-int64 IDs; `[]` means no assets.
5. Every referenced upload must match current Mentor, request course, `LECTURE`, and `UPLOADED`; missing/out-of-scope assets return generic 404.
6. The view inserts `support_messages`, then ordered `support_message_uploads` rows with zero-based positions, then reloads the full thread through API #59's query and a shared pure projection module.
7. The response is validated as `ApiEnvelope<SupportRequest>` with `DESIGN_RESOURCE_UPDATED`. The request status is unchanged; commit occurs after complete projection; query/link/projection/commit failures roll back and return safe 500.

## Implementation files

- Route and contract-error mapping: `app/api/v1.py`, `app/core/middleware.py`.
- Runtime: `app/modules/mentor/api_60_mentor_support_reply/`.
- Shared projection used by API #59 and #60: `app/modules/mentor/_shared/support_request_projection.py`.
- Tests: `tests/modules/mentor/api_60_mentor_support_reply/`.
- DD: seven non-table sheets, two mappings based on the table template, and three reports (12 Markdown files total).

## Remaining discrepancies

| Topic | Status |
|---|---|
| Support DDL and int64 IDs | Local migration 008 fallback; no live schema/deployment evidence |
| `attachment_refs` wire key/JSON encoding | DERIVED from API #47 implementation; catalog labels only a required string |
| Direct course-owner authorization | DERIVED local policy; assigned-Mentor relation not source-backed |
| Blank/length policy, post-resolve reply policy, thread bound | DERIVED/open as recorded in `OPEN_QUESTIONS.md` |
| Live API, DB concurrency and Storage URL behavior | Not verified by fake-DB TestClient tests |

## Macro-review boundary

AC-24 currently shows #58 list → #59 detail/thread → #60 reply → #61 resolve decision. API #60 does not own request status. Review #58–#61 together after #61 is available; harmonize reference semantics with #34/#35/#47 before claiming approved contract readiness.
