# AC-36 Macro-review — Admin notification APIs #92–#96

## Review scope and status

- Review set: #92 list, #93 create/send, #94 update, #95 delete/cancel, #96 delivery status.
- Sources: API catalog and reusable schemas, AC/API index, AC-36 activity diagram, DD #92–#96 (overview/request/response/data mapping/open questions/verification reports), plus the current Study router/schema evidence cited in those DDs.
- Result: `VERIFIED_WITH_OPEN_QUESTIONS` at document level. This review checks cross-API contract consistency and records unresolved owner decisions; it does not verify runtime, deployment, live schema, or approval.

## Per-API review

| API | Direct contract retained | Cross-API finding | Status / required decision |
|---|---|---|---|
| #92 list | GET with optional `status`, `channel`, `page`; response `ApiEnvelope<Notification>`; exact catalog 200/401/403/503/500. | List intent and `page` query suggest a collection, while the response is one `Notification`; no `PageMeta` or empty-list behavior is defined. The 503 trigger is also unspecified. | `DISCREPANCY / DERIVED`: local runtime uses Page, fixed pagination and DB-connectivity→503 fallbacks; owner must confirm cardinality, pagination, dependency semantics and Admin schema. DD proposal remains separate from direct contract. |
| #93 create/send | POST body has optional `recipients` or `segment`, required `title`, `content`, `channels`; response `ApiEnvelope<Notification>` at 202; exact catalog errors retained. | AC-36 has conditional Send and Push/Email dispatch, but request has no `action` or `scheduled_at`. Operation tracking prose says notification POST returns `Operation`; catalog/diagram say `Notification`. Runtime preserves Notification, writes one legacy candidate row per recipient plus `QUEUED` delivery rows, and adds derived UUID/ID batch metadata. | `DISCREPANCY / DERIVED / SOURCE_REQUIRED`: local fallback is wired and fake-DB tested; owner must decide send/schedule semantics, response metadata, Admin model and Operation-to-notification handoff. |
| #94 update | PUT path-only with `notification_id:int64!`; no direct body/query; response `ApiEnvelope<Notification>` and exact catalog 200/401/403/404/422/500. | Runtime is wired with a strict `{title, content}` fallback over legacy BIGINT candidate rows and updates only when all locked delivery rows are `QUEUED`. It preserves audience/channels/schedule and returns channel/status projection from the outbox. These rules are DERIVED; live schema and fine-grained permission remain unverified. | `WIRED / DERIVED / SOURCE_REQUIRED`: fake-DB tested; owner must confirm body, row grain, QUEUED editability, Admin permission and schedule/audience scope. DD remains Draft. |
| #95 delete/cancel | DELETE path-only; response `ApiEnvelope<DeleteResult>` with `status:"deleted"`; exact catalog 200/401/403/404/422/500. | Wired locally with shared ADMIN auth, positive signed-int64 path parsing, parent-then-delivery locks, and a `DERIVED` fallback that hard-deletes one recipient-level legacy BIGINT row only when one or more locked outbox rows are all `QUEUED`; checked-in FK cascades those rows. DB `CURRENT_TIMESTAMP` maps to `deleted_at`; repeated DELETE returns 404. | `WIRED / DERIVED / SOURCE_REQUIRED`: fake-DB tests pass. Owner must confirm lifecycle/retention and queued-only policy, live schema, dedicated permission, scheduler/worker coordination, external cancellation and repeat-delete policy. A local 200 does not prove provider cancellation. |
| #96 status | GET path-only; response `ApiEnvelope<Notification>`; exact catalog 200/401/403/404/500. | Wired local read-only aggregate uses the same legacy BIGINT notification/outbox candidate and `QUEUED`/`FAILED`/`SENT` precedence as #92, mapped to existing `Notification.channels/status`; malformed ID and no-delivery result map to 404. | `WIRED / DERIVED / SOURCE_REQUIRED`: focused and linked HTTP tests pass. Do not add aggregate counts. Owner must confirm source/grain, enum/precedence, empty-state behavior, fine-grained permission, live schema and Operation bridge. |

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

APIs #92–#96 are wired and locally verified with fake DB projections (see their verification reports). API #96 reuses #92's Notification model and aggregate precedence without adding response fields. No live database checks, deployment checks, provider delivery, or owner approvals were performed. The group remains `VERIFIED_WITH_OPEN_QUESTIONS`; local fallbacks do not resolve the shared Admin model, fine-grained permission, scheduler behavior, or Operation bridge.
