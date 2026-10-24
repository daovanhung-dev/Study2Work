# Plan result — API #94 Admin cập nhật notification

## Status
- Result: PARTIALLY COMPLETED — source-backed DD authored; owner decisions remain.
- DD status: Draft — Needs Confirmation.
- Runtime status: UNWIRED / NOT_FOUND by scoped static source scan.
- AC-36 macro-review: pending until #96 DD is complete.

## Direct API requirement
- API #94: PUT /api/v1/admin/notifications/{notification_id}.
- Auth: Bearer JWT; role Admin; AC-36 requires notification-management permission.
- Direct request: notification_id:int64!; no body or query declared.
- Direct response: ApiEnvelope<Notification>.
- Success: HTTP 200 DESIGN_RESOURCE_UPDATED.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.
- AC-36 branch: UPDATE Notification, then reload notification management.

## Sources reviewed
- Catalog #94 and Notification/NotificationChannel/NotificationStatus/AudienceSegment schemas.
- AC/API index and AC-36 diagram UPDATE branch.
- DD #92 and #93, plus Admin PUT precedents #75 and #89.
- Legacy Study notifications table guide/DDL and separate V1-PILOT notification/delivery DDL.
- Current Study router, middleware, API Guidelines and registered createDD-markdown template pack.
- Selector worklogs #48–#50; each was read before authoring.

## Data and side effects
- Catalog and diagram have no #94 body. Proposal reuses #93 audience/title/content/channels and adds scheduled_at; all remain DERIVED.
- Logical mutations are Notification UPDATE and proposed recipient association replacement. No compatible Admin physical relation is approved.
- Scheduler, queue, operation tracking, transaction, actor audit, ID model and lifecycle transition are SOURCE_REQUIRED.
- No application code or schema was changed; no application tests were run.

## Conflicts preserved
- UPDATE intent without request body or field list.
- Notification logical schema versus partial legacy BIGINT table and separate V1-PILOT UUID delivery model.
- Draft/scheduled intent without enum/state transition or scheduler contract.
- #93 Notification-vs-Operation response and identifier bridge remain open.

## Output
- Eight standard sheets 00_Cover.md through 07_table.md.
- One supplementary recipient association mapping.
- Three standard reports.
- Study workflow output is a Markdown folder; no ZIP.
