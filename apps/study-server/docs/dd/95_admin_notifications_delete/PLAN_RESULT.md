# Plan result — API #95 Admin xóa hoặc hủy notification

## Status
- Result: IMPLEMENTED AND LOCALLY VERIFIED; owner decisions remain open.
- DD status: Draft — Needs Confirmation.
- Runtime status: WIRED in the Study FastAPI source; route/module/tests use fake DB projections.
- AC-36 macro-review: `VERIFIED_WITH_OPEN_QUESTIONS`; APIs #92–#95 are locally wired and #96 remains unwired.

## Direct API requirement
- API #95: `DELETE /api/v1/admin/notifications/{notification_id}`.
- Auth: Bearer JWT; role Admin; AC-36 additionally names notification-management permission.
- Request: `notification_id:int64!`; no body/query.
- Response: HTTP 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>` with `id:int64`, literal `status="deleted"`, `deleted_at:date-time`.
- Errors: exact 401/403/404/422/500 catalog business codes.
- AC-36 branch: `DELETE/mark cancelled`, then reload notification management.

## Local implementation fallback — DERIVED
- Shared ADMIN guard precedes signed-int64 path validation and database access.
- Lock one legacy BIGINT notification row, then its delivery rows in stable channel order.
- Require at least one delivery and every status to be `QUEUED`; otherwise rollback and return catalog 422.
- DELETE only the path-selected parent, use checked-in FK cascade for its outbox rows, map `CURRENT_TIMESTAMP` from DELETE RETURNING to `deleted_at`, validate envelope, then commit.
- Missing/previously deleted parent returns 404; no scheduler/provider call is made.
- The rule applies to one recipient row only; sibling rows sharing `operation_id` remain untouched.

## Evidence and boundaries
- Reviewed catalog #95/#96, reusable schemas, parsed AC-36 diagram, DDL/migration 009, current #93/#94, DELETE #90 precedent, tests and registered DD skill/template pack.
- The legacy BIGINT target is the model currently used by #93/#94; checked-in DDL does not prove live deployment.
- Fake DB tests do not prove PostgreSQL locks/cascade, worker behavior, provider cancellation or fine-grained Admin permission.
- DD stays Draft; owner decisions on lifecycle, retention, scheduler, schema, permission and Operation bridge remain open.

## Verification
- API #95 focused: 21 passed.
- Linked #92–#95, full Study suite, Ruff, OpenAPI and DD/context checks: record final results after completion.

## Conflict status
- Catalog says delete draft/cancel conditionally; diagram says DELETE/mark cancelled; local hard-delete and queued-only rule are DERIVED.
- DeleteResult says deleted; response does not confirm external cancellation.
- Legacy BIGINT outbox model and V1-PILOT UUID learner model remain separate.
- No persisted timestamp/tombstone or idempotency contract exists; repeated DELETE returns 404 locally.
