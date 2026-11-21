# ST-06 — Detailed Design Plan

## 1. Scope and order

- Screen: ST-06 “Thực hiện thanh toán”, inventory row 20, candidate route `/student/pay/:orderId`, AC-12, APIs #17/#18.
- This session handles ST-06 only. Do not author ST-07 or another Screen ID.
- Sequence: source/contract review → save this plan → render HTML to a separate image if valid → measure/create marker JSON/SVG/annotated image → author A–F screen DD → update inventory/global plan/worklog → static audit.
- Preserve original [`screen.png`](./screen.png) and [`code.html`](./code.html). The PNG is 1280×1024 and almost blank. If the HTML renders, use `screen_rendered_from_html.png` as the annotation base and state its provenance; do not overwrite either source asset.
- Keep expected inventory/AC/API design separate from current source/prototype. Do not invent provider choice, gateway protocol, operation status, polling cadence, retry/idempotency, paid-state proof, identifier conversion, storage, or route behavior.
- No application tests or runtime calls are planned. Existing test inventory is read-only evidence only.

## 2. Evidence register and asset preservation

| Evidence | Purpose | Status / boundary |
|---|---|---|
| [`screen.png`](./screen.png), 1280×1024, SHA-256 `d1dc527fdad7c423a42aa6eac0caf57137ad7eebe3e7c6184f55c79b00289a36` | Preserve original, compare with HTML. | Original retained; almost blank and unusable for element mapping. |
| [`code.html`](./code.html), 9,303 characters, SHA-256 `c74f162474fdaed4708d6a5f049b47e0552fa8da04a5e9748416abd1bbdc3c2b` | Static public shell, breadcrumb, payment-status card, return link and footer. | 15 static anchors; no form/control, fetch/XHR, API path or handler. |
| Inventory row 20 in [`list_screen.md`](../../../list_screen.md) and ST-06 row in [`dd_screens/PLAN.md`](../../dd_screens/PLAN.md) | Proposed route, states, #17/#18, safe retry requirement, ST-07/SH-07 links. | Expected design, not runtime evidence. |
| [AC-12](../../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Student precondition; #17 → gateway → payment decision; #18 tracking node; enrollment continuation after payment success. | Design flow. #18 node is not connected to the sequence. |
| [API catalog #17/#18](../../../../../../docs/lists/list_api.md) and their Draft DDs | Request/auth/response/errors and shared Operation schema. | Design-only; #17/#18 runtime is `UNWIRED / NOT_FOUND`. |
| API #17 `OPEN_QUESTIONS.md` and API #18 `OPEN_QUESTIONS.md` | Order linkage, ownership, provider, amount/currency, gateway, status/lifecycle/storage, operation ID and result conflicts. | `NEEDS USER DECISION` / `SOURCE_REQUIRED`. |
| Study Server route/test search and [.agents/server-study route context](../../../../../../.agents/server-study/apis/declared-routes.md) | Confirm current #17/#18 route and test boundary. | No #17/#18 route/module/query/model/test found. |
| [DB_UNICA_TABLES.md](../../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [DB_UNICA_ERD.drawio](../../../../../study-server/docs/diagrams/DB_UNICA_ERD.drawio), checked-in [DB.sql](../../../../../../infra/postgres/study-server/DB.sql) | Inspect Payment, Order and Operation persistence evidence. | `payments` exists as design/DDL artifact without `order_id`; Order and Operation tables are absent. Live schema/deployment unverified. |
| ST-05 [`ST-05.md`](../ST-05_kiem-tra-don-hang-checkout/ST-05.md) | Prior Order handoff and unresolved `data.id` → `order_id` mapping. | Expected prior screen; API #16 is design-only. |
| Current Study Web tree and [`design.md`](../../../../../../.agents/web-study/design.md) | Route availability and visual/accessibility target. | No editable app source/router/package manifest; Study Web `UNWIRED`. Guide is intended design only. |

## 3. Expected behavior and current behavior

### Expected behavior

Inventory row 20 describes a Student payment page after ST-05. Its candidate flow is:

```text
ST-05 approved Order handoff
→ POST API #17 with order_id and approved provider
→ receive Operation
→ conditionally GET API #18
→ use trusted server/gateway payment outcome
→ continue to ST-07 only after payment is confirmed
```

The inventory states pending/running/failed/cancelled/succeeded and requests safe retry. AC-12 describes gateway success as continuing to enrollment, and failure/cancel as stopping the flow. It includes a separate #18 operation-status node, but that node is not connected to AC-12’s sequence.

API #17 catalog contract: `POST /api/v1/payments`, Bearer JWT, role Student, body `{order_id:int64!, provider:string!}`; success 202 `DESIGN_OPERATION_ACCEPTED` with `ApiEnvelope<Operation>`; errors 401/403/422/503/500. API #18 contract row: `GET /api/v1/operations/{operation_id}`, Bearer JWT, path `operation_id:int64!`, owner actor; success 200 `DESIGN_OPERATION_RETRIEVED`; errors 401/403/404/500. These are design contracts, not running endpoints.

### Current behavior

- The HTML renders a public shell, breadcrumb, a static “Chưa có thông tin thanh toán để hiển thị.” message, a static explanation that a transaction was not found or may have ended, a return CTA, and footer.
- It displays no Order ID, payment amount/provider, gateway, operation status, transaction ID, payment result or confirmation. All 15 anchors are literal static links; there are no controls, API calls or event handlers.
- Breadcrumb “Kiểm tra đơn hàng” links to `/student/checkout` without an ID. CTA “Quay lại kiểm tra đơn hàng” links to the literal route template `/student/checkout/:courseId`, not an interpolated course identifier.
- The original PNG does not show the HTML. If browser rendering succeeds, create a separate HTML-derived image and annotate that render.
- Study Web has no editable source/router/package manifest or candidate payment route. Study Server has no current #17/#18 route/module/query/model/test.

### Discrepancies to retain

1. Inventory asks for safe retry, but neither #17 nor #18 defines idempotency, retry conditions, duplicate suppression or a retryable outcome. Do not specify safe retry as implemented behavior.
2. ST-05’s logical Order response has `data.id:int64`; #17 request requires `order_id:int64`. The handoff mapping and eligibility/ownership rules remain unresolved.
3. #17 returns `Operation`; the shared Operation schema and AC-12 #18 path use UUID, while API #18 catalog row says `operation_id:int64`. Client cannot safely poll until one canonical type is approved.
4. AC-12 says gateway success/failure/cancel but does not define a polling edge or map #18 Operation status/result to a trusted payment outcome. The #18 node is disconnected from the diagram sequence.
5. API #18 authorization conflicts: catalog row and AC diagrams say owner-only, while the operation-tracking summary allows owner/Admin. Exact caller identity mapping is unresolved.
6. `OperationKind`, `OperationStatus`, PaymentStatus, storage, lifecycle and Payment result semantics are unresolved. `Operation.result` is optional Payment even though operation tracking also covers other job types.
7. Current `payments` SQL has no `order_id`, and no Study Order/Operation table is defined. `payments.user_id/course_id` nullability differs between SQL and table documentation.
8. The current static page is an unavailable/finished state, not the inventory’s pending/running flow. Its public shell conflicts with AC-12 Student authentication context.
9. Return breadcrumb/CTA do not carry valid order/course identity. The CTA’s literal path placeholder is not runtime interpolation.
10. The prototype imports Plus Jakarta Sans and Material Symbols from Google Fonts and Tailwind from a CDN; the Study Web guide requires Inter/system fonts and says not to add remote imports. No approved visual exception is recorded.

## 4. Planned marker targets

Measure actual DOM bounds after rendering at a 1280×1024 CSS viewport and device scale 2. Each visible target receives one sequential `ST06-EL-01`… ID and one numbered marker. Group related links into one navigation target and enumerate each contained anchor in the DD. If the rendered layout changes targets, update this plan before writing marker JSON/SVG or the annotated image.

| Marker | Target | Evidence boundary |
|---:|---|---|
| #1 | Header Study2Work brand link | Static `href="/"`. |
| #2 | Header primary navigation group | Home, Courses, My Courses, Progress. |
| #3 | Header Sign In link | Static `/login`; no auth guard evidence. |
| #4 | Header Sign Up link | Static `/register`. |
| #5 | Breadcrumb group | Home, Courses, “Kiểm tra đơn hàng”, current “Thực hiện thanh toán”. The order link omits an ID. |
| #6 | Page-title header group | H1 “Thực hiện thanh toán” with its bottom separator line. |
| #7 | Centered payment-status card/surface | Layout only; not a Payment or Operation record. |
| #8 | Credit-card/payment icon | Static `credit_card` visual inside the card. |
| #9 | Card title H2 “Thực hiện thanh toán” | Static repeated title within the card. |
| #10 | Status headline “Chưa có thông tin thanh toán để hiển thị.” | Static prototype copy; not a #17/#18 response. |
| #11 | Supporting explanation | Static copy says transaction not found or may have ended. |
| #12 | “Quay lại kiểm tra đơn hàng” CTA | Static anchor to literal `/student/checkout/:courseId`. |
| #13 | Footer brand | Static Study2Work wordmark. |
| #14 | Footer navigation group | Home, Courses, Sign In and Sign Up. |

## 5. Event plan

| Event | Trigger | Planned handling and limit |
|---|---|---|
| EV-01 Route entry and Student/order context | Candidate `/student/pay/:orderId` load | Requires Student auth by AC-12/#17 and order identifier from ST-05. Route/session guard is absent; ST-05 `data.id` → `order_id` handoff and ownership/eligibility are unresolved. Do not create Payment merely by loading until trigger semantics are approved. |
| EV-02 Initiate payment (#17) | Approved initiation action/flow after valid Order context | Contract: Student Bearer JWT; POST `/api/v1/payments`; body `{order_id:int64, provider:string}`; 202 `DESIGN_OPERATION_ACCEPTED`, `ApiEnvelope<Operation>`; errors 401/403/422/503/500. AC-12 places it after #16. Provider continuity, gateway protocol, ownership, persistence and idempotency are open. |
| EV-03 Track operation (#18) | Operation identifier available and polling approved | Contract row: Bearer JWT, GET `/api/v1/operations/{operation_id}`, int64 path and 200/401/403/404/500; shared schema/AC use UUID. #18’s AC node is unconnected. Do not choose type, owner policy, poll interval, terminal states, cache or retry. |
| EV-04 Interpret payment result / continue | Trusted server/gateway result is defined | AC-12: success proceeds to enrollment; failure/cancel stops. HTTP 202 only means accepted, and client callback is not payment proof. No source maps Operation or Payment status to these branches; do not redirect to ST-07 or show paid without approved mapping. |
| EV-05 Return to order check | Activate CTA #12 | Current target is literal `/student/checkout/:courseId`; no actual ID or state is supplied. Breadcrumb target `/student/checkout` is also missing ID. Correct destination and payload need approval. |
| EV-06 Header/footer navigation | Activate #1–#5 or #14 | Record static hrefs only; Study Web route availability/auth-aware behavior is not verified. |

## 6. Blockers carried to DD

- Order ID mapping from ST-05/API #16 to #17 `order_id` and server-side Order ownership/eligibility.
- Provider values and continuity between #16 `payment_provider:PaymentProvider` and #17 `provider:string`.
- Payment gateway protocol, callback/webhook verification, decline/cancel semantics and side-effect/transaction boundary.
- Operation ID conflict (API #18 row int64 versus shared Operation schema and AC UUID), plus owner-only versus owner/Admin authorization.
- Study Operation storage, enum values, lifecycle, polling condition/interval, result-per-kind schema and retention.
- Retry safety/idempotency and duplicate handling are not specified despite inventory language.
- Payment status mapping and the trusted server signal required before ST-07.
- Study Web route/auth guard is unwired; original screenshot is blank relative to the HTML.
- Current font/CDN styling differs from the Study Web design guide and needs approval/alignment before frontend implementation.
- Return breadcrumb/CTA have no valid identity handoff; CTA uses literal placeholder route.
- Checked-in Payment schema has no Order relation; nullability documentation discrepancy and live database/deployment remain unresolved.

## 7. Completion and status criteria

- Create `screen_rendered_from_html.png` only after this plan is saved; target 2560×2048 from CSS viewport 1280×1024 at 2× after document/fonts settle.
- Create DOM-measured sequential, unique, in-bounds marker records and an annotation based on the derived render; keep callouts off text.
- Author `ST-06.md` sections A–F with every visible target and identified event; separate inventory/AC/API expectations from current source/prototype; mark #17/#18 `DESIGN_ONLY / UNWIRED`.
- Update only the ST-06 inventory/global-plan rows and append the session checkpoint; do not begin ST-07.
- Static audit: marker order/count/bounds and 1:1 DD mapping; JSON/XML parse; local links; image dimensions; original asset hashes; 83-screen inventory/folder count; core artifact count; scoped `git diff --check`.
- Do not run application tests/runtime. Keep statuses distinct: `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until identifier, payment and operation contracts are resolved.
