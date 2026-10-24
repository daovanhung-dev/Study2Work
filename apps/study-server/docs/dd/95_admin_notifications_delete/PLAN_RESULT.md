# Plan result — API #95 Admin xóa hoặc hủy notification

## Status
- Result: PARTIALLY COMPLETED — source-backed DD authored; owner decisions remain.
- DD status: Draft — Needs Confirmation.
- Runtime status: UNWIRED / NOT_FOUND by scoped static source scan.
- AC-36 macro-review: pending until #96 DD is authored.

## Direct API requirement
- API #95: DELETE /api/v1/admin/notifications/{notification_id}.
- Auth: Bearer JWT; role Admin; AC-36 requires notification-management permission.
- Direct request: notification_id:int64!; no body/query.
- Direct response: ApiEnvelope<DeleteResult>, with id:int64, literal status="deleted", deleted_at:date-time.
- Success: HTTP 200 DESIGN_RESOURCE_DELETED.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.
- AC-36 branch: DELETE/mark cancelled, then reload notification management.

## Sources reviewed
- Catalog #95/#96, DeleteResult/Notification schemas and Operation tracking summary.
- AC/API index and parsed AC-36 diagram branch/edges.
- DD #92–#94 and Admin DELETE precedents #77/#90.
- Legacy Study notifications DDL and separate V1-PILOT notification/delivery schema.
- Current Study router/middleware, API Guidelines, registered skill/template pack.
- Selector worklogs #48–#50 and current #94 worklog; selected worklogs were read before authoring.

## Data and side effects
- Proposed rule: logically remove Draft; cancel Scheduled only before delivery begins; reject disallowed state with existing 422. All are DERIVED.
- Preserve delivery/recipient history; no hard DELETE or physical columns are inferred.
- Scheduler, tombstone timestamp, lifecycle enum, Admin permission and transaction are SOURCE_REQUIRED.
- #96 response does not expose a delivery aggregate and cannot source cancellation eligibility.
- No application code or schema was changed; no application tests were run.

## Conflicts preserved
- Delete draft vs cancel scheduled and the missing lifecycle policy.
- DeleteResult literal "deleted" when logical outcome is cancellation.
- Legacy BIGINT and V1-PILOT UUID models remain separate.
- #93 Notification-vs-Operation/ID bridge remains open.
- AC-36 macro-review remains pending until #96.
