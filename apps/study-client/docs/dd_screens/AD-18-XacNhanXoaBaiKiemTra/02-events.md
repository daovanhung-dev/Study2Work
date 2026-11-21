# AD-18 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-18-EV-001` | `Source heading` / EV-01 — Mở AD-18 và nạp/nhận diện target Quiz | See source event detail below |
| `AD-18-EV-002` | `Source heading` / EV-02 — Return to AD-15 | See source event detail below |
| `AD-18-EV-003` | `Source heading` / EV-03 — Cancel safely | See source event detail below |
| `AD-18-EV-004` | `Source heading` / EV-04 — Confirm quiz deletion (disabled; candidate API flow) | See source event detail below |
| `AD-18-EV-005` | `Source heading` / EV-05 — Audit reason field (disabled) | See source event detail below |
| `AD-18-EV-006` | `Source heading` / EV-06 — Shell, notification, breadcrumb and footer controls | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Current source also validates positive signed-int64 route IDs locally, keeps the page read-only and makes no API call; browser runtime chưa được xác minh.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### EV-01 — Mở AD-18 và nạp/nhận diện target Quiz

- **Element/trigger:** AD-15 delete branch or direct route entry; candidate route param `quizId`.
- **Type/preconditions:** Route/load. Angular page preserves `quizId` as text and validates digits, positivity and the signed-int64 maximum used by #90; AD-15 currently links only positive safe integer IDs. This does not prove AC-35 fine-grained permission behavior or browser runtime.
- **Input/source:** `quizId` from URL or selected item handoff. Catalog #90 path is positive-int64-shaped `quiz_id`; #87 local list item includes `id`, `course_id`, `title`, `duration_minutes`, `passing_score`, `questions=[]`.
- **Sequence:** 1) Parse route param only after authentication/authorization policy is determined. 2) Validate ID mapping; do not parse arbitrary slug/UUID as int64. 3) Determine approved source for selected Quiz. 4) If handoff is #87 item, map only fields present in that response. 5) Do not invent a GET detail; no such API is listed/wired. 6) Do not show a fabricated course title or attempt count. 7) If the target cannot be resolved, keep confirm disabled and surface the owner-approved missing-target state; that state/copy is not specified.
- **API:** No API call is defined for page entry. #90 is mutation only; #87 is a list and is not a direct detail endpoint.
- **Output/exceptions:** Current Angular page shows the raw route ID and read-only notice; locally invalid IDs show an alert and no request is sent. It does not load a title/course/history record. Mockup values `--`/“Chưa chọn bản ghi” are design-source placeholders. Backend #90 remains authoritative and returns 422 for an invalid raw path if called; absent/hard-deleted Quiz maps to #90 404. Exact detail/error/recovery UX remains open.

### EV-02 — Return to AD-15

- **Elements/trigger:** #13 breadcrumb or #15 top return control; click.
- **Type/preconditions:** Navigation. Current Angular return links target `/admin/quizzes`; route/history and filter/page restoration beyond that target are not established here.
- **Input:** Current candidate `quizId`; possible source AD-15 page/filter state is not represented in URL/contract.
- **Sequence:** 1) Current Angular breadcrumb/back link navigates to `/admin/quizzes`. 2) Preserve filters/page only if the application defines that state handoff. 3) Do not send #90 or mutate cache. The supplied Stitch HTML still uses `href="#"`; browser navigation has not been visually verified.
- **Output/exceptions:** Expected screen relation is AD-15. Runtime destination, fallback when entry was direct, history behavior and state restoration need product/UI contract.

### EV-03 — Cancel safely

- **Element/trigger:** Current Angular safe-return link; click. Marker #33 is the corresponding Stitch design element.
- **Type/preconditions:** Navigation/cancel before any delete request. Angular link returns to AD-15; the original mockup anchor has `href="#"` and no handler.
- **Input:** Current route/history; no body or mutation input.
- **Sequence:** 1) Confirm no DELETE request is in flight or initiated. 2) Angular link navigates to AD-15. 3) No state mutation or cache invalidation. 4) Browser navigation remains unverified.
- **Output/exceptions:** The Angular source defines AD-15 as the safe destination; filter/page restoration is unspecified. No cancel confirmation or unsaved-data prompt is needed because the audit textarea is disabled and no editable state exists.

### EV-04 — Confirm quiz deletion (disabled; candidate API flow)

- **Element/trigger:** Current Angular destructive button; disabled. Design marker #34 maps to the original Stitch button. No click handler exists, so no request can start.
- **Type/preconditions:** Submit/destructive action. Require resolved target, positive signed-int64 ID mapping, authenticated Admin, approved quiz-management permission, and owner-approved policy for attempts/answer-only/no-history and concurrent creation. Until all blockers are resolved, keep action unavailable.
- **Input:** Path `quiz_id:int64!`; Bearer JWT. No query and no request body. Do not include audit reason: #90 catalog is path-only and route reads no body.
- **Candidate request:** `DELETE /api/v1/admin/quizzes/{quiz_id}`. Current route passes raw path and Authorization to #90. Local validator authenticates/authorizes role `ADMIN` before positive signed-int64 parse. Positive-only/minimum and parser implementation are current local behavior; the fine-grained permission mapping is unresolved.
- **Backend current side effects (not approved policy):** #90 locks Quiz, then Quiz questions/choices, checks any `quiz_attempts` and linked `quiz_answers`. If attempt or answer exists, local branch sets `status='DELETED'`, updates `updated_at`, and preserves children/history. If neither exists, local branch deletes choices → questions → Quiz in one transaction. If already tombstoned, local code returns 200 with the old `updated_at`. These are source facts marked `DERIVED` in API DD, not front-end promises. AC-35 explicitly supports only soft-delete when attempts exist; it is silent on the other branches.
- **Response parsing:** On HTTP 200 require valid envelope and `businessCode=DESIGN_RESOURCE_DELETED`; data contract is `{id:int64,status:"deleted",deleted_at:date-time}`. Validate returned ID matches requested target before marking success. `message`, `meta`, and `traceId` follow envelope; do not use them as source for additional UI fields.
- **Success result:** Set candidate state `deleted` and invalidate/refetch #87 as inventory expects. Exact cache implementation, toast/copy, and navigation destination are undefined. #87 current query hides tombstones, but this is local source behavior; not an approved product lifecycle. Do not state audit was recorded unless a source is added.
- **Error mapping:** 401 → authentication/session handling per shared auth flow; 403 → access denied; 404 → target absent/not found; 422 → `quiz_id` validation in current local code, not conflict; 500 → safe service failure. Catalog does not define 409, so do not map history/attempts to a conflict response. Network/timeout/unknown outcome, retry, duplicate click and idempotency policy are not defined; do not auto-resend a destructive request until reconciliation behavior is approved.
- **Concurrency:** Local #90 parent lock alone does not establish safety against API #29 attempt creation; no matching local #29 route/module was found. Do not claim attempt race is closed.

### EV-05 — Audit reason field (disabled)

- **Element/trigger:** #31 textarea/#29 label; user input would ordinarily be `input/change`, but current textarea has `disabled` and no handler.
- **Input/validation:** Placeholder suggests a mandatory reason and ISO-27001 policy, but no approved field length, requiredness, policy source or #90 request body exists. Catalog and current route define no body.
- **Processing/output:** Current state is disabled; keyboard/pointer input produces no editable value and no request. Do not mark it required or send text. Enabling the control needs a separate approved API/contract and audit policy decision.

### EV-06 — Shell, notification, breadcrumb and footer controls

- **Elements/trigger:** #2–#6, #8, #10, #12–#15, #38–#40. The notification button has no listener; navigation anchors have `href="#"`; remaining shell copy is static.
- **Input/preconditions:** None available. No router, notification endpoint or identity/system-status provider in this screen source.
- **Processing/output:** No request, route change or state update. Do not invent link destinations or interpret “System Normal”/RBAC labels as current service state.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
