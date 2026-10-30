# PLAN_RESULT — Study API #96

## Kết quả implementation plan

- Task `coding`, scope `server-study`; coding selector returned/read three #74–#76 worklogs, 89 available and no shortage.
- Contract kept: `GET /api/v1/admin/notifications/{notification_id}/status`, Admin Bearer, `notification_id:int64!`, no body/query, `ApiEnvelope<Notification>`, HTTP 200 and exact errors 401/403/404/500.
- AC-36 status branch requires the delivery aggregate step before reloading notification management.
- Local implementation uses one read-only query over legacy BIGINT `notifications` and `notification_deliveries`, the same checked-in candidate used by APIs #92–#95. It is not a live schema or deployment claim.
- `data.channels/status` reuse API #92's local mapping. Channels are ordered; status precedence is `QUEUED` if any row is queued, then `FAILED` if any failed, otherwise `SENT` when all are sent. No delivery count fields are added.
- Missing notification/no delivery row and invalid positive-int64 path map to catalog 404. This is `DERIVED`, consistent with #64 status lookup and the #96 catalog's lack of 422.
- `read_at` and `scheduled_at` are optional in Notification but absent from the candidate projection and are omitted. GET does not commit or call a provider.
- Fine-grained AC-36 permission, official Admin schema/grain, enum approval, aggregate retry semantics and #93 Operation bridge remain open. DD stays `Draft — Needs Confirmation`.

## Ma trận requirement

| Item | DIRECT/DERIVED/SOURCE_REQUIRED | Nội dung |
|---|---|---|
| Method/path/actor | DIRECT | GET status; Admin Bearer JWT. |
| Input | DIRECT | `notification_id:int64!`; không body/query. |
| Success | DIRECT | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Notification>`. |
| Errors | DIRECT | 401, 403, 404, 500 với đúng codes catalog. |
| Delivery aggregate step | DIRECT from AC-36 | Đọc aggregate rồi reload management. |
| Candidate query/schema | DERIVED | Reuse legacy BIGINT parent/outbox source used by #92–#95; live schema unknown. |
| Delivery-to-Notification projection | DERIVED | Reuse #92 channel/status projection; no new response fields. |
| Invalid ID/no-delivery mapping | DERIVED | Return catalog 404; no unlisted 422/503. |
| Permission policy and aggregate grain | SOURCE_REQUIRED | Fine-grained policy, recipient/attempt/retry grain and status approval remain unresolved. |
| Mutation | N/A | GET read-only; no provider call. |

## Sources reviewed

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) #96 and reusable `Notification`, `NotificationDelivery`, `OperationStatus`.
- [AC/API index AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio).
- DD #92–#95 sources and API #64 status precedent.
- Legacy `DB.sql`, migration 009, V1-PILOT schema, current Study router/middleware/database helper and focused tests.
- Registry-wired `createDD-markdown`, canonical eight Markdown templates, and Study Markdown-only workflow.

## Change boundary

Added API #96 module, route and middleware path; added focused HTTP/OpenAPI tests and updated linked API #92/#94/#95 OpenAPI-count assertions. Updated this DD and Study Server context. No catalog, diagram, database DDL, migration, provider, or client changes.
