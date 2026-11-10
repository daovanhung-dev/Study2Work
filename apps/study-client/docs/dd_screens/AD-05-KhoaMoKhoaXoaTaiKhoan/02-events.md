# AD-05 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-05-EV-001` | `Source heading` / EV-01 — Mở màn hình và tải tài khoản | See source event detail below |
| `AD-05-EV-002` | `Source heading` / EV-02 — Chọn lock/unlock/delete tab | See source event detail below |
| `AD-05-EV-003` | `Source heading` / EV-03 — Xác nhận khóa hoặc mở khóa trạng thái | See source event detail below |
| `AD-05-EV-004` | `Source heading` / EV-04 — Xác nhận xóa tài khoản | See source event detail below |
| `AD-05-EV-005` | `Source heading` / EV-05 — Quay lại AD-02 / AD-03 | See source event detail below |
| `AD-05-EV-006` | `Source heading` / EV-06 — Reason, policy, shell and footer controls | See source event detail below |
| `AD-05-EV-007` | `Source heading` / API request/response matrix | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Mở màn hình và tải tài khoản

- **Trigger / type:** Route entry or handoff from AD-02/AD-03; `Load`.
- **Elements:** #16, #17, #18; entry shell #6/#8.
- **Input:** numeric route param `userId`/handoff `user_id` using signed-int64 path representation. No account ID exists in the prototype. Authentication credential comes from the approved client session; permission requirement is AC-31 Admin user-management permission.
- **Prerequisite:** route/client and permission mapping implemented; ID present and parseable. Local API access requires Bearer JWT/Admin.
- **Ordered processing:**
  1. Read `userId` from route/handoff; validate the signed-int64 form without converting display codes or PII.
  2. Apply the client auth policy. If no usable session, do not present a mutation-ready state. The route's unauthenticated destination is not yet specified.
  3. Call `GET /api/v1/admin/users/{user_id}` (#69), with Bearer JWT/Admin; no body or query.
  4. Accept only HTTP 200 + `DESIGN_RESOURCE_RETRIEVED` + valid `UserProfile`. API #69 local source checks shared ADMIN and parses the ID before reading the legacy `users` candidate.
  5. Map returned profile ID and status into #16/#17; do not infer role/status aliases or permission result. Set the page to ready-read-only until action policies are approved.
  6. On 401/403/404/500 or network/invalid-envelope response, map to unauthenticated/forbidden/not-found/error; do not show a fake profile or activate Confirm.
- **Output / cache / navigation:** read-only target profile and source-backed status; cache key/invalidation policy follows shared client contract and remains unwired. No mutation or automatic navigation is defined.
- **Current prototype:** no route param, selected user, request or handler.

### EV-02 — Chọn lock/unlock/delete tab

- **Trigger / type:** Click #21, #22 or #23; `Click`.
- **Input:** one local action key (`lock`, `unlock`, or `delete`) and the displayed profile/status from EV-01. These labels are UI actions, not API enums.
- **Prerequisite:** EV-01 has a target profile and approved permission/action policy. Until then, tabs remain non-actionable.
- **Ordered processing:**
  1. Read selected tab; do not send mutation while changing tabs.
  2. Check that the target user and permitted action policy are available; do not use static gate/RBAC badges.
  3. Set local draft action and update selected/focus state. Candidate mapping to #71 `SUSPENDED`/`ACTIVE` or #72 is DERIVED and requires approval.
  4. Keep reason/confirm disabled unless reason persistence and mutation requirements are approved.
- **Output:** selected draft action only; no network effect/cache write. Leaving this view or changing tabs does not mutate the account.
- **Current prototype:** tab roles/classes exist but there is no click listener or dynamic selection update.

### EV-03 — Xác nhận khóa hoặc mở khóa trạng thái

- **Trigger / type:** Click #30 while #21 or #22 is selected; `Submit`/`Click`.
- **Input:** route `user_id`, displayed current status from #69, desired action, session/auth context. Candidate JSON body is `{ "status": "SUSPENDED" }` for lock or `{ "status": "ACTIVE" }` for unlock. This shape and mapping are **DERIVED** from local source; AC/catalog omit the body. Reason text is not sent because no API field exists.
- **Prerequisite:** #71 body/status contract approved; valid `user_id`; AC-31 permission mapping, self/last-Admin and other safeguards decided; selected action allowed for current state; audit/session rules approved. Until all are met, #30 stays disabled.
- **Ordered processing:**
  1. Normalize target ID from route and desired status from the approved action mapping. Do not serialize display aliases.
  2. Validate client-required input and preconditions only from approved rules. Do not invent required reason length or transition constraints.
  3. Disable repeat submission while this request is in flight; no optimistic status mutation.
  4. Send one `PATCH /api/v1/admin/users/{user_id}/status` (#71), Bearer JWT/Admin, approved JSON body. Local source uses strict `{status}` and Pydantic body validation may happen before view authorization; mixed invalid-body/unauthenticated ordering is not characterized.
  5. On HTTP 200 + `DESIGN_RESOURCE_UPDATED` + `UserProfile`, map returned profile/status, then refetch #68/#69 according to approved AC-31 refresh/route policy.
  6. On 401/403/404/422/500, map to corresponding state. Local #71 view row-locks status and accepts only current `ACTIVE`/`SUSPENDED`; other current values (including `DELETED` and `PENDING_EMAIL_VERIFICATION`) → 422. A same-state request still updates `updated_at`; repeated SUSPENDED can revoke newly eligible unrevoked/unexpired refresh rows. Suspend revocation and status update share a transaction; access JWT may remain valid. Activate does not restore revoked refresh rows. Local query/projection/revocation/commit failures roll back and return safe 500.
  7. On timeout/network ambiguity, show unknown mutation outcome and require an approved reconciliation path; do not automatically retry.
- **Output:** updated user profile/status on verified success; no claim that all active sessions ended immediately. The UI must present the actual approved session behavior.
- **Current prototype:** #21/#22 are visual tabs, textarea/Confirm disabled, no API call.

### EV-04 — Xác nhận xóa tài khoản

- **Trigger / type:** Click #30 while #23 is selected; `Submit`/`Click`.
- **Input:** `user_id` from route, current profile/status, auth/session; DELETE has no request body or query. The reason textarea is not submitted by current contract.
- **Prerequisite:** deletion, retention/anonymization, relationship/dependency, token/session, visibility, permission and audit policies approved. Confirm remains disabled before this gate.
- **Ordered processing:**
  1. Read numeric route ID and confirm the delete mode is selected; do not interpret “vĩnh viễn” as hard delete.
  2. Apply approved permission and lifecycle/safeguard checks. AC-31 calls for delete per policy; no local API dependency check is evidenced.
  3. Send a single `DELETE /api/v1/admin/users/{user_id}` (#72), Bearer JWT/Admin, no body/query.
  4. On HTTP 200 + `DESIGN_RESOURCE_DELETED` + `DeleteResult`, display success only for the approved deletion meaning. Local response status is `deleted`; `deleted_at` aliases `updated_at` from the status-marker update.
  5. Per approved flow, refresh #68/#69 and route. Local #68/#69 do not hide `DELETED`; local #72 does not anonymize data, delete related rows, record audit or revoke refresh tokens. API #03 blocks new login/refresh for non-ACTIVE accounts; existing access JWT may remain usable.
  6. Map 401/403/404/422/500 and network/unknown outcome as in the response table. Local #72 returns 404 for missing or already-`DELETED`; invalid signed-int64 path is 422. No 409 dependency-conflict behavior is present in current contract/source.
  7. Do not retry automatically or promise undo/recovery absent an approved policy.
- **Output:** response-backed delete state only. Whether to keep, hide or navigate away from the deleted row remains a blocker.
- **Current prototype:** action tab and button do not submit; “permanent delete” is unsupported by local implementation semantics.

### EV-05 — Quay lại AD-02 / AD-03

- **Trigger / type:** Click #9 or #29; `Click`.
- **Input:** current route, numeric `user_id` if present, source screen/return target if provided. No mutation payload.
- **Prerequisite:** router and return policy approved; auth session remains governed by shared app shell.
- **Ordered processing:**
  1. Resolve target screen from approved navigation state (AD-02 list or AD-03 detail).
  2. Preserve only route ID/query state approved for that target; do not add PII to URL.
  3. Navigate without calling #69/#71/#72 as a side effect of the link itself. Any list/detail refresh follows the explicit success/handoff policy.
- **Output:** return to approved screen and retain context per route contract.
- **Current prototype:** both hrefs are `/admin/users`, and no Study Web router is present; “Return safe” does not implement safety, selection retention or dirty-state confirmation.

### EV-06 — Reason, policy, shell and footer controls

- **Trigger / type:** Attempt to type into #25; click #2/#4/#6/#7/#15/#26/#29/#31/#32/#34 or render the related static copy; `Input`/`Click`/`Render` where applicable.
- **Input:** no source-backed API input. Any Admin reason, policy decision, notification count, system health, audit identifier, RBAC assurance, compliance state or support destination requires its own approved source/contract.
- **Prerequisite:** a verified data source and destination contract must exist before enabling an interaction. For audit reason, define storage/API, actor, retention and validation first.
- **Ordered processing:**
  1. Keep disabled/unwired controls non-interactive; do not create fictitious requests.
  2. Render static shell content without presenting it as verified permission, health, audit, compliance or enforcement state.
  3. Do not send reason text through #71/#72; current APIs have no accepted field.
  4. If future contracts add these capabilities, specify them in their owning API/screen DD before linking them here.
- **Output:** no mutation, cache update or navigation unless a separate source-backed interaction is approved.
- **Current prototype:** #25 is disabled; nav/footer placeholders have no destinations; badges and compliance/audit claims are static.

### API request/response matrix

| API | Direct catalog/AC contract | Current local implementation | Screen mapping |
|---|---|---|---|
| #69 | `GET /api/v1/admin/users/{user_id}`; Bearer JWT/Admin; signed `int64` path; no body/query. 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`; 401/403/404/500. | Shared ADMIN guard; signed-int64 parsing; safe read-only projection from local legacy `users` candidate. | Load selected user/status. Do not treat static profile, permission or audit copy as API response. |
| #71 | `PATCH /api/v1/admin/users/{user_id}/status`; Bearer JWT/Admin; signed `int64` path. Catalog/AC omit request body. 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<UserProfile>`; 401/403/404/422/500. | Strict required body `{status: "ACTIVE"|"SUSPENDED"}` is `DERIVED`; row lock; only current ACTIVE/SUSPENDED; update status/updated_at; suspend revokes eligible refresh rows in same transaction. | Keep disabled until body, transition/status vocabulary, permission and session effects are approved. Never attach reason with this contract. |
| #72 | `DELETE /api/v1/admin/users/{user_id}`; Bearer JWT/Admin; signed `int64` path; no body/query. 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`; 401/403/404/422/500. | Conditional soft marker `DELETED`; returns `{id,status:"deleted",deleted_at}` with `deleted_at` aliasing updated_at. Preserves profile/dependent/token rows; no audit/anonymization/dependency check. | Keep disabled until deletion/retention/visibility/session policy is approved; do not label as irreversible hard delete. |

**Shared request rules:** send Bearer credentials only through the approved HTTP client; never place tokens or PII in the URL. Do not add query parameters, `reason`, audit IDs, client-generated deletion time, `X-Trace-Id`, idempotency key or retry semantics unless the API contract defines them. The catalog has no retry, timeout or duplicate-submission guarantee for these mutations. Error envelope carries `data:null`; surface safe server message according to common error policy without exposing SQL/stack traces.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
