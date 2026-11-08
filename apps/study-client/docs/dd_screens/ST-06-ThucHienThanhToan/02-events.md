# ST-06 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-06-EV-001` | `Source heading` / EV-01 — Route entry và Student/Order context | See source event detail below |
| `ST-06-EV-002` | `Source heading` / EV-02 — Initiate payment using API #17 (DESIGN_ONLY) | See source event detail below |
| `ST-06-EV-003` | `Source heading` / EV-03 — Track Operation via API #18 (DESIGN_ONLY / ID DISCREPANCY) | See source event detail below |
| `ST-06-EV-004` | `Source heading` / EV-04 — Interpret trusted payment outcome and continue | See source event detail below |
| `ST-06-EV-005` | `Source heading` / EV-05 — Return to order check | See source event detail below |
| `ST-06-EV-006` | `Source heading` / EV-06 — Header, breadcrumb and footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Route entry và Student/Order context

- **Trigger / loại:** Browser load candidate `/student/pay/:orderId`; page navigation.
- **Điều kiện:** AC-12 expects authenticated Student and paid branch after Order creation at ST-05. Current Study Web has no route/session guard; current API #16 is not wired.
- **Input:** `orderId` candidate URL segment. API #17 body requires `order_id:int64`. ST-05 API #16 logical response defines `data.id:int64`; continuity, parse policy, ownership and eligibility remain unresolved.
- **Xử lý:** (1) Route target must resolve Student identity/role using an approved session contract. (2) Validate/normalize order identifier only per approved int64 contract. (3) Resolve Order ownership/eligible state on a trusted backend; current code has no such endpoint/source. (4) Do not call #17 until prior Order and provider mapping are approved. (5) Do not infer retry or create a new order/payment from page load.
- **API / side effect:** No route-entry API is declared separately. #17 requires Bearer Student; #18 also Bearer JWT with unresolved owner policy. Current HTML makes no call.
- **Output / errors:** Current local HTML shows static unavailable state. Expected auth/order errors and route recovery target are not defined.
- **Current status:** Study Web `UNWIRED`; `RUNTIME NOT VERIFIED`.

### EV-02 — Initiate payment using API #17 (DESIGN_ONLY)

- **Trigger / loại:** Expected payment initiation in the AC-12 paid flow after Order creation. Exact UI trigger or automatic route-entry rule is not specified; HTML has no initiation control.
- **Input:** `order_id:int64` from an approved ST-05 Order handoff; `provider:string` from an approved provider mapping; Bearer Student JWT. No query/path parameter or additional body field is declared.
- **API:** `POST /api/v1/payments`, `Content-Type: application/json`; body `{ "order_id": <int64>, "provider": <string> }`; success HTTP 202 `DESIGN_OPERATION_ACCEPTED`; response `ApiEnvelope<Operation>`.
- **Trình tự:** (1) Resolve Student auth and approved Order ownership/eligibility. (2) Validate only required int64 and string fields per contract; provider allowlist/case/format constraints are not defined. (3) Choose initiation trigger only after product/API approval. (4) Send one request according to an approved duplicate/idempotency rule; none currently exists. (5) Parse the envelope and business code. (6) HTTP 202 means accepted/queued according to contract, not paid. (7) Store/retain operation ID only after the canonical ID type and response mapping are approved. (8) Do not repeat #17 automatically on timeout or refresh.
- **Success mapping:** Logical Operation per reusable schema: `id:uuid`, `kind:OperationKind`, `status:OperationStatus`, `owner_id:int64`, `submitted_at`, `updated_at`, optional `completed_at`, optional `result:Payment`. This is design shape only; allowed enums, storage and values are unresolved.
- **Errors:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 503 `DESIGN_DEPENDENCY_UNAVAILABLE`; 500 `DESIGN_INTERNAL_ERROR`. No 404/409 in #17 catalog. UI error mapping, retryable subset, rollback and network timeout behavior are unresolved.
- **Side effect/current status:** API DD describes Payment insert/external payment as design-only; no current endpoint, gateway invocation, Payment row or Operation is verified. Payment table DDL is not live-schema proof.

### EV-03 — Track Operation via API #18 (DESIGN_ONLY / ID DISCREPANCY)

- **Trigger / loại:** Conditional GET after #17 returns an Operation identifier and polling is approved. The inventory says “GET #18 theo điều kiện chốt”; AC-12 diagram node has no sequence edge.
- **Input:** Bearer JWT and operation ID returned by #17. API #17 shared Operation schema returns `data.id:uuid`; API #18 row requires `operation_id:int64`; AC-12 and other diagrams use UUID. No canonical route value can be passed until conflict is resolved.
- **API:** `GET /api/v1/operations/{operation_id}`; no query/body. API #18 catalog status: 200 `DESIGN_OPERATION_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Authorization discrepancy:** API row says owner, AC diagrams say Student|Mentor|Admin owner-only, tracking summary says owner or Admin. Caller claim → `owner_id` mapping and non-owner 403/404 leakage policy are unresolved.
- **Processing:** (1) Do not cast UUID to int64 or derive an ID. (2) Once the owner resolves ID type, auth policy, physical store and producer mapping, send GET with Bearer. (3) Validate response Operation fields/status only against an approved enum/state machine. (4) Poll cadence, stop/terminal conditions, cache, timeout and UI update policy are not defined. (5) No endpoint or storage exists in current Study source.
- **Output/side effects:** Read-only logical `Operation`; no Payment mutation is specified by #18. 202 does not guarantee an Operation can be read yet. Error response UI and retry are unresolved.

### EV-04 — Interpret trusted payment outcome and continue

- **Trigger / loại:** Trusted gateway/server confirms an outcome, or an approved #18 Operation result maps to one. No current HTML event/control represents this.
- **Input:** AC-12 payment decision: success vs failure/cancel. Candidate Operation `status` and optional `result:Payment` do not have approved enum or mapping. Client callback/redirect query is not a trusted payment proof.
- **Processing:** (1) Require a server-verified outcome source and approved status mapping. (2) Success may continue to enrollment #19 only after payment/entitlement confirmation. (3) Failure or cancellation stops AC-12 flow. (4) Do not reinterpret unknown, missing, stale, or nonterminal Operation data as success or failure. (5) Do not invent retry/continue/return copy for these cases.
- **Output/navigation:** Verified success → ST-07 result path per inventory, with subsequent server-owned #19/#20 flow. Failure/cancel → stop and show approved state. Current page has no such event or state transition.

### EV-05 — Return to order check

- **Trigger / loại:** Click CTA #12.
- **Input hiện tại:** Static `href="/student/checkout/:courseId"`; no actual courseId/orderId/state.
- **Xử lý hiện tại:** Browser follows literal path if route resolves; no API or mutation. Breadcrumb #5 separately links to `/student/checkout` without ID.
- **Output / issue:** Neither target is confirmed as a valid route. Intended prior screen is ST-05, whose route uses `:courseId`; ST-06 route uses `:orderId`. Correct return URL/payload mapping and route interpolation require approval.

### EV-06 — Header, breadcrumb and footer navigation

- **Trigger / loại:** Click anchors #1–#5 or #14; #13 footer brand is static text, not a link.
- **Input:** Static hrefs `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`, plus breadcrumb `/student/checkout`.
- **Processing:** (1) Browser/client reads the literal href. (2) Navigate only if the route exists. (3) No auth-aware selection, order/payment ID, filter, query state, API call or mutation exists in markup. (4) Header primary nav uses `hidden xl:flex`; no mobile navigation replacement appears in HTML.
- **Output/errors:** Static target only; Study Web routes/runtime are unverified. Sign In/Sign Up links do not establish Student session state.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
