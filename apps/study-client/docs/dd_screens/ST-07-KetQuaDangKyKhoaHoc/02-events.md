# ST-07 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-07-EV-001` | `Source heading` / EV-01 — Route entry và Student/course context | See source event detail below |
| `ST-07-EV-002` | `Source heading` / EV-02 — Create enrollment with API #19 (DESIGN_ONLY) | See source event detail below |
| `ST-07-EV-003` | `Source heading` / EV-03 — Track payment Operation with API #18 (conditional / blocked) | See source event detail below |
| `ST-07-EV-004` | `Source heading` / EV-04 — Refresh My Courses with API #20 (DESIGN_ONLY) | See source event detail below |
| `ST-07-EV-005` | `Source heading` / EV-05 — Interpret and display enrollment/payment outcome | See source event detail below |
| `ST-07-EV-006` | `Source heading` / EV-06 — Navigate to My Courses | See source event detail below |
| `ST-07-EV-007` | `Source heading` / EV-07 — Header, breadcrumb and footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Route entry và Student/course context

- **Trigger / loại:** Load candidate `/student/enroll/result/:courseId` (page navigation; no element marker).
- **Điều kiện:** AC-12 Student authenticated, course exists. Current Study Web has no route/auth guard; static HTML can be opened without identity.
- **Input:** Candidate `courseId` URL segment; Student session; possible prior free-entitlement/payment outcome. Route has no `operationId`, Enrollment ID or outcome token. Catalog #19 path requires int64 but min/max/parse policy not specified.
- **Xử lý:** (1) Read only the route segment/session supplied by an approved router/auth contract. (2) Do not treat a URL segment, refresh, browser history or CTA as proof of enrollment/payment. (3) Resolve authorized Student and entitlement on a trusted backend before any write. (4) If the approved result handoff cannot be resolved, remain in a non-success state; recovery copy/route must be approved. (5) Do not auto-call #19 merely because the result route loaded.
- **API / side effect:** No route-entry API is declared. Current HTML makes no call. #18/#19/#20 are all unwired.
- **Output / errors:** Current page always shows static #9/#10. Expected 401/403/course-not-found/direct-entry behavior and destination are not fully defined; preserve only catalog codes if an API is actually called.
- **Current status:** Study Web `UNWIRED`; `RUNTIME NOT VERIFIED`.

### EV-02 — Create enrollment with API #19 (DESIGN_ONLY)

- **Trigger / loại:** Expected one-time Enrollment creation after trusted free eligibility or payment success. Exact trigger and owning screen (ST-04, ST-07 or another transition) are unresolved; HTML has no create button/handler.
- **Preconditions:** Student Bearer; backend confirms course eligibility and, for paid branch, trusted payment success; duplicate policy and request contract approved. AC-12 says this operation precedes the Enrollment + Progress transaction.
- **Input:** `courseId:int64` candidate path; API body notation repeats `course_id:int64!` and `user từ JWT:string!`; current shared auth helper parses numeric `sub` to int, but #19 wire field/claim mapping is unresolved. No additional client `user_id` may be invented.
- **API:** `POST /api/v1/courses/{course_id}/enrollments`, `Content-Type: application/json`, Student Bearer JWT; no query. Request body must retain the declared unresolved notation until API owner confirms exact JSON schema. Success 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Enrollment>`.
- **Trình tự dự kiến:** (1) Validate auth/role and approved course identifier. (2) Verify backend entitlement and any existing Enrollment according to approved contract. (3) Reconcile path/body course IDs and JWT identity before serializing request. (4) Invoke #19 once under an approved retry/idempotency rule; current HTML offers no trigger and the rule is absent. (5) Parse envelope/business code. (6) On 201, map only returned Enrollment fields defined by the approved schema; no client status defaults. (7) AC-12 transaction is expected to insert Enrollment and initialize Progress atomically, with duplicate prevention; physical query/commit behavior is not implemented. (8) Continue to #20 only per the approved AC/API sequence; if reload fails after #19 may have committed, do not repeat #19 automatically.
- **Response:** Logical `Enrollment`: `id:int64`, `course_id:int64`, `user_id:int64`, `status:EnrollmentStatus`, `enrolled_at:date-time`, optional `completed_at:date-time`. Initial status, timestamp source and null/omit policy remain open. Catalog success does not provide an approved screen-specific message.
- **Errors:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 409 `DESIGN_STATE_CONFLICT`; 500 `DESIGN_INTERNAL_ERROR`. Exact 404 resource, 409 duplicate condition and recoverability/retry behavior remain unresolved; do not add errors.
- **Side effect/current status:** AC-12 design calls for Enrollment + Progress in one transaction. No current #19 handler/query/model/test or runtime write exists. Checked-in DDL is not live-schema proof.

### EV-03 — Track payment Operation with API #18 (conditional / blocked)

- **Trigger / loại:** Conditional GET only after an approved Operation ID is handed off and #18 is connected to this screen flow. AC-12 puts #18 in a detached node; ST-07 candidate route contains only `courseId`.
- **Input:** Bearer JWT plus `operationId`. API #17 shared Operation schema/AC use UUID; catalog #18 path row declares int64. Owner-only vs owner/Admin is also unresolved.
- **API:** `GET /api/v1/operations/{operation_id}`; no query/body. Catalog response 200 `DESIGN_OPERATION_RETRIEVED`, `ApiEnvelope<Operation>`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Processing:** (1) Do not obtain or synthesize an ID from `courseId`. (2) Wait for contract owner to resolve ID type, owner policy, result schema and producer handoff. (3) Only then could a client issue GET under approved poll/stop rules. (4) No status, stale-result, terminal-state, interval, timeout or cache behavior is currently defined.
- **Output / side effects:** Logical read-only Operation. Do not map a raw callback/redirect to paid. No current endpoint or Operation storage is verified; no polling behavior is implemented.

### EV-04 — Refresh My Courses with API #20 (DESIGN_ONLY)

- **Trigger / loại:** Expected after approved #19 success according to AC-12; GET from AC-12/AC-13 reload step.
- **Input:** Student Bearer; optional `status:string` and `page:int32`; no request body. Route candidate courseId does not define query defaults or binding.
- **API:** `GET /api/v1/users/me/courses`; 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- **Trình tự:** (1) Use Student auth per contract. (2) Pass only status/page values with approved meanings; no defaults/page size are defined. (3) Parse direct UserProfile envelope without coercing it into a course list. (4) AC-13 expects Enrollment JOIN Course and calls #21 separately for progress, then merges client-side. (5) Because the declared UserProfile does not encode membership, no course row/empty-state mapping can be finalized. (6) Cache invalidation/reload retry is unspecified; do not retry #19 as a substitute.
- **Side effect/current status:** Read-only by DD; API #20 has no current route/query/model/focused test. Result mapping is blocked by contract discrepancy.

### EV-05 — Interpret and display enrollment/payment outcome

- **Trigger / loại:** A trusted server result, approved #19 response, or approved #18 result maps to a terminal state. No current event/control/state model exists in HTML.
- **Input:** AC-12 free/paid branch; API #19 201 Enrollment; or trusted payment result. API #20 response contract is currently UserProfile and is not a course membership signal.
- **Processing:** (1) Use only the server-owned outcome and approved state mapping. (2) AC-12 payment failure/cancel stops before #19; never label enrolled. (3) AC-12 places #20 before the “registered/open course” UI, but handling #19 commit followed by #20 failure is unspecified. (4) Inventory `awaiting-confirmation/enrolled/conflict/failure` labels are expected design states, not current API enum values. (5) Unknown/missing/late responses cannot be reinterpreted as success/failure or retried as a new enrollment without an approved rule.
- **Output:** Current #9/#10 remain fixed copy and do not change. Approved success/pending/conflict/failure copy, CTA visibility, retry/refresh and direct-entry behavior still need product/API decisions.

### EV-06 — Navigate to My Courses

- **Trigger / loại:** Click CTA #11.
- **Input:** Static `href="/student/courses"`; no courseId, enrollmentId, operationId, status or response state.
- **Xử lý hiện tại:** Browser follows the literal link if a route resolves; no API or mutation. It corresponds to candidate ST-08 route, but Study Web route/auth is unwired.
- **Output / issue:** No direct course target. AC-12 says open course after #20 but does not define route/payload, and catalog #20 response is not a course list.

### EV-07 — Header, breadcrumb and footer navigation

- **Trigger / loại:** Click anchors in #1–#5 or #13. #12 footer brand is static text, not a link.
- **Input:** Literal links `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`; no result/course identity in these links.
- **Processing:** (1) Browser/client reads the literal `href`. (2) Navigate only if route exists. (3) No auth-aware selection, API, mutation, or persisted state exists in markup. (4) Header nav uses `hidden md:flex`; no mobile replacement is shown.
- **Output/errors:** Static navigation targets only; route availability, session expiry behavior and focus-visible state are unverified.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
