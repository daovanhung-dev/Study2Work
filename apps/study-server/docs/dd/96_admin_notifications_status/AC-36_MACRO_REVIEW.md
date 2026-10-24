# AC-36 Macro-review — Admin notification APIs #92–#96

## Review scope and status

- Review set: #92 list, #93 create/send, #94 update, #95 delete/cancel, #96 delivery status.
- Sources: API catalog and reusable schemas, AC/API index, AC-36 activity diagram, DD #92–#96 (overview/request/response/data mapping/open questions/verification reports), plus the current Study router/schema evidence cited in those DDs.
- Result: `VERIFIED_WITH_OPEN_QUESTIONS` at document level. This review checks cross-API contract consistency and records unresolved owner decisions; it does not verify runtime, deployment, live schema, or approval.

## Per-API review

| API | Direct contract retained | Cross-API finding | Status / required decision |
|---|---|---|---|
| #92 list | GET with optional `status`, `channel`, `page`; response `ApiEnvelope<Notification>`; exact catalog 200/401/403/503/500. | List intent and `page` query suggest a collection, while the response is one `Notification`; no `PageMeta` or empty-list behavior is defined. The 503 trigger is also unspecified. | `DISCREPANCY / SOURCE_REQUIRED`: owner must select cardinality, pagination and dependency semantics. DD proposal remains separate from direct contract. |
| #93 create/send | POST body has optional `recipients` or `segment`, required `title`, `content`, `channels`; response `ApiEnvelope<Notification>` at 202; exact catalog errors retained. | AC-36 has conditional Send and Push/Email dispatch, but request has no `action` or `scheduled_at`. Operation tracking prose says notification POST returns `Operation`; catalog/diagram say `Notification`. Notification ID is int64, while Operation schema uses UUID; API #18 also has an ID type discrepancy. | `DISCREPANCY / SOURCE_REQUIRED`: owner must decide send/schedule request semantics, response and the Operation-to-notification ID handoff. |
| #94 update | PUT path-only with `notification_id:int64!`; no direct body/query; response `ApiEnvelope<Notification>` and exact catalog 200/401/403/404/422/500. | Diagram says UPDATE Notification but catalog omits a body. DD body/audience/channel/schedule replacement and Draft/Scheduled interpretation are proposals marked `DERIVED`; no physical model or scheduler source supports them. | `DERIVED / SOURCE_REQUIRED`: confirm whether and how to add a body, editable states, replacement semantics and scheduling behavior before implementation. |
| #95 delete/cancel | DELETE path-only; response `ApiEnvelope<DeleteResult>` with `status:"deleted"`; exact catalog 200/401/403/404/422/500. | Diagram says `DELETE/mark cancelled`. Eligibility based on Draft/Scheduled and “delivery not started,” tombstone, repeat DELETE and scheduler cancellation are derived proposals. #96 direct response cannot currently supply the delivery aggregate needed to decide eligibility. | `DISCREPANCY / SOURCE_REQUIRED`: choose delete/cancel state semantics, delivery-start source, scheduler coordination, timestamp and idempotency policy. |
| #96 status | GET path-only; response `ApiEnvelope<Notification>`; exact catalog 200/401/403/404/500. | Diagram requires “Đọc delivery aggregate,” but `Notification` has no `queued`, `sent`, `failed`, or per-channel result fields. Reusable `NotificationDelivery` is a separate logical schema and is not declared as #96 response. | `DISCREPANCY / SOURCE_REQUIRED`: choose aggregate source/grain and whether a projection fits existing `Notification.status` or needs a contract change. Do not append aggregate fields silently. |

## Shared unresolved decisions

1. **Admin notification model and grain:** legacy BIGINT `notifications` has recipient-oriented columns and lacks campaign/channel/status/schedule/delivery fields. V1-PILOT uses UUID learner notifications and a separate delivery model. Neither is approved as the Admin model.
2. **Audience and delivery relation:** AC-36 creates Notification plus recipients, but no agreed campaign/recipient/channel grain, deduplication, retries, or count semantics are present in the reviewed schema.
3. **Enums and projection:** `AudienceSegment`, `NotificationChannel`, `NotificationStatus`, and `OperationStatus` values/transition rules are not defined here. `is_read` is not delivery status; delivery status is not automatically notification status.
4. **Permission:** catalog says Admin and AC-36 requires notification-management permission; Study Admin guard, permission key, principal mapping, and global/tenant scope are not source-verified.
5. **Errors and lifecycle:** preserve each endpoint's exact catalog error set. Do not copy #92's 503 to #96 or add 409/410/422 where absent. Decide 403/404 precedence, missing/tombstoned behavior, transaction/concurrency, scheduler race, and error envelope convention.
6. **Operation bridge:** resolve whether #93 returns Notification, Operation, or both, and how the int64 notification identifier relates to UUID operation tracking. Keep #18 operation polling a distinct contract until the owner defines the bridge.

## Consistent constraints for implementation planning

- Keep each endpoint's direct contract and its `DERIVED` proposals visibly separate until approved design updates the catalog/diagram.
- Do not merge legacy BIGINT and V1-PILOT UUID schemas or infer an Admin table from either artifact.
- Do not treat `NotificationDelivery` as #96's response or claim that its counts can drive #95 policy until the source, grain, and aggregate rules are selected.
- Keep all five DDs `Draft — Needs Confirmation` while the shared decisions above remain open.

## Verification boundary

The five DD folders are present and their source-wiring checks classify #92–#96 as `UNWIRED / NOT_FOUND`. No Study application tests, live database checks, deployment checks, or owner approvals were run for this document review.
