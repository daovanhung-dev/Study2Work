# OPEN_QUESTIONS — Study API #64

DD status: `Draft — Needs Confirmation`. The direct catalog contract remains unchanged. The local implementation fallback below follows the user's conflict-resolution order and is not approved business policy or evidence of deployed schema.

<a id="q-64-01-response-shape"></a>

## Q-64-01 — Operation response versus delivery summary

**Evidence:** Catalog #64 declares `ApiEnvelope<Operation>`; AC-25 describes delivery status; reusable `NotificationDelivery` has status and counts.

**Local fallback:** Preserve Operation in `data`. Reconstruct its identity/owner/timestamps from API #63's local notification row and map aggregate delivery state into `data.status`. Do not add counts to `meta` or replace the direct response type.

**Remaining gap:** Delivery counts and channel-level partial success are not visible through Operation. The catalog response itself still disagrees with the activity's delivery-summary intent.

<a id="q-64-02-id-handoff"></a>

## Q-64-02 — `notification_id` and `operation_id`

**Evidence:** API #64 path is int64; API #63 `data.id` is UUID but current local response includes `meta.notification_ids:int64[]`.

**Local fallback:** Client takes each notification ID from #63 metadata for API #64. API #64 returns the stored operation UUID in `data.id`; it never substitutes one identifier for the other.

**Remaining gap:** The metadata bridge is DERIVED and is not a first-class field in the catalog Operation schema. API #18's ID convention remains unresolved.

<a id="q-64-03-storage"></a>

## Q-64-03 — Physical delivery source

**Evidence:** API #63 added local legacy BIGINT `notification_deliveries` and nullable `notifications.operation_id` in migration 009. The separate V1-PILOT UUID relation is incompatible with the int64 path.

**Local fallback:** Query the same checked-in legacy relations written by API #63. Do not read `is_read` as send status or join the UUID pilot schema.

**Remaining gap:** Migration 009 has not been applied or live-verified.

<a id="q-64-04-aggregate"></a>

## Q-64-04 — Status aggregation across channels

**Evidence:** API #63 writes one unique outbox row per notification/channel with states `QUEUED`, `SENT`, or `FAILED`; direct OperationStatus members and partial-success behavior are unspecified.

**Local fallback:** If any channel is queued, report `QUEUED`; otherwise if any channel failed, report `FAILED`; otherwise report `SENT` when every channel row is sent. This uses only the current local outbox states.

**Remaining gap:** Mixed sent/failed is summarized as `FAILED` and channel counts are not exposed by the direct Operation response. Retry attempts, partial success and final-state semantics need contract-owner confirmation.

<a id="q-64-05-authorization"></a>

## Q-64-05 — Mentor ownership and 403/404

**Evidence:** Catalog requires Mentor and allows both 403/404. API #63 writes the authenticated numeric Mentor `sub` to `notifications.sender_id`.

**Local fallback:** A different sender receives 403; absent notification or absent dispatch status resource receives 404. The handler reads by notification ID before checking sender so it can preserve both catalog outcomes.

**Remaining gap:** This derives access from the API #63 local write binding, not an approved global notification permission policy.

<a id="q-64-06-pending"></a>

## Q-64-06 — Missing outbox/delivery state

**Evidence:** API #63 atomically inserts at least one outbox row before 202; older notification rows may have no Operation ID/outbox.

**Local fallback:** A notification without `operation_id` or delivery rows has no API #63 dispatch-status resource and returns 404. No status is inferred from `is_read`.

**Remaining gap:** A future worker/retry implementation must preserve a durable row for every dispatch state.

<a id="q-64-07-enums"></a>

## Q-64-07 — Operation and delivery status values

**Evidence:** Catalog names `OperationStatus` but does not enumerate values. Migration 009 constrains the local outbox to `QUEUED|SENT|FAILED`; API #63 already returns `QUEUED` for Operation.

**Local fallback:** Reuse those outbox values in `Operation.status` using Q-64-04 precedence. Do not invent `PARTIAL`, `COMPLETED` or a Payment result.

**Remaining gap:** Enum compatibility and terminal/retry semantics need confirmation.

<a id="q-64-08-path-errors"></a>

## Q-64-08 — Non-int64 path

**Evidence:** Catalog lists only 401/403/404/500; framework path validation could otherwise emit 422.

**Local fallback:** Keep the raw path string in the handler while declaring int64 in OpenAPI. Malformed or out-of-range values return 404 `DESIGN_RESOURCE_NOT_FOUND`; no new business code is added.

<a id="q-64-09-operation-tracking"></a>

## Q-64-09 — API #18 generic Operation polling

**Evidence:** API #18 is not connected to an edge in AC-25; its path ID, owner, result and Study persistence remain unresolved.

**Scope:** API #64 returns Operation as direct schema but does not implement generic #18 polling, alter its contract or change the distinction between notification ID and Operation UUID.

<a id="q-64-10-error-envelope"></a>

## Q-64-10 — Error envelope and middleware

**Evidence:** Shared `error_response(...)` currently emits `data:null`; parameterized design route paths are recognized from `DESIGN_CONTRACT_PATHS`.

**Current local implementation:** The exact parameterized API #64 template is in `DESIGN_CONTRACT_PATHS`; the view uses only the catalog's four error codes and OpenAPI suppresses the framework-generated 422 for this raw-path endpoint.

**Remaining gap:** The middleware/error envelope and runtime outcomes are locally covered by tests, but this does not approve a changed global error policy or prove live deployment.

## Handoff AC-25

- #63 `meta.notification_ids` supplies int64 keys; #64 reads the corresponding per-recipient notification/outbox rows.
- #63 Operation UUID remains in `notifications.operation_id`; API #64 maps it into Operation `data.id` and derives status from per-channel rows.
- API #18 remains a separate unresolved operation-tracking contract.
- DD stays Draft until response intent, status policy, ownership and live schema are confirmed. See [PLAN_RESULT.md](./PLAN_RESULT.md) and [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
