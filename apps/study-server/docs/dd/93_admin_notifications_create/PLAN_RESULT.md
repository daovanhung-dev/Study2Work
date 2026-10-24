# Plan result — API #93 Tạo/phát notification

## Status

- Result: PARTIALLY COMPLETED — source-backed DD authored; confirmation gaps remain.
- DD status: Draft — Needs Confirmation.
- Runtime status: UNWIRED / NOT_FOUND by static source scan.
- AC-36 macro-review: pending until #92–#96 can be reviewed after #96.

## Direct API requirement

- API #93: POST /api/v1/admin/notifications.
- Auth: Bearer JWT; role Admin; AC-36 notification-management permission.
- Body: recipients?:int64[], segment?:AudienceSegment, title:string!, content:string!, channels:NotificationChannel[]!.
- Response: ApiEnvelope<Notification>.
- Success: HTTP 202 DESIGN_OPERATION_ACCEPTED.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 422 DESIGN_VALIDATION_ERROR; 503 DESIGN_DEPENDENCY_UNAVAILABLE; 500 DESIGN_INTERNAL_ERROR.

## Sources reviewed

- Catalog #93, reusable Notification/Operation schemas, Operation tracking paragraph.
- AC-36 index and diagram nodes/edges.
- Legacy Study table guide/DDL and separate V1-PILOT notification/delivery DDL.
- DD #92, #63, #64 and #18.
- Current Study router/test scan, API Guidelines, registered createDD-markdown skill, eight templates and Study workflow.
- Selector worklogs #48–#50; all selected worklogs reviewed before authoring.

## Data and side effects

- Audience query source: not approved.
- Logical writes: Notification and recipient association per diagram.
- Legacy notifications is a partial candidate only; recipient relation not found.
- Immediate dispatch after acceptance is DERIVED because action is absent.
- Transaction, queue, Operation store, ID allocation and retry policy are SOURCE_REQUIRED.

## Conflicts

- Catalog/diagram response Notification vs Operation tracking summary.
- Conditional send vs no action/schedule request field.
- Legacy BIGINT and V1-PILOT UUID models remain separate.
- API #18 UUID/int64 ID conflict and #96 handoff remain open.

## Output

- Eight standard sheets 00_Cover.md through 07_table.md.
- One supplementary recipient mapping and three standard reports.
- Study scope delivers Markdown folder; no ZIP.
