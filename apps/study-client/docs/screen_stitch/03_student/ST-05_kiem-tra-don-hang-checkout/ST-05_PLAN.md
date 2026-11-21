# ST-05 — Detailed Design Plan

## 1. Scope and order

- Screen: ST-05 “Kiểm tra đơn hàng / checkout”, inventory row 19, proposed route `/student/checkout/:courseId`, AC-12, APIs #08/#16.
- This session handles ST-05 only. Do not author ST-06, ST-07, or another Screen ID.
- Sequence: source/contract review → save this plan → render HTML to a separate image if the prototype renders → measure and create marker JSON/SVG/annotated image → author A–F screen DD → update inventory/global plan/worklog → static audit.
- Preserve original [`screen.png`](./screen.png) and [`code.html`](./code.html). The original PNG is 1280×1024 and visually almost blank. If the HTML renders, use only `screen_rendered_from_html.png` as the annotated visual base and record its provenance. Never overwrite the original PNG or HTML.
- The plan separates expected inventory/AC behavior from current source and prototype behavior. Do not infer a confirmation control, provider choice, amount/currency rule, retry, idempotency, transaction, order persistence, or backend route from the mockup.
- No application tests or runtime calls are planned. Existing tests are read-only evidence only.

## 2. Evidence register and preservation

| Evidence | Purpose | Status / boundary |
|---|---|---|
| [`screen.png`](./screen.png), 1280×1024, SHA-256 `9f03e86f469e9d09a1cb9cdeb5486a56f84343dc0067d80cafe7a8925e225657` | Preserve original and compare against HTML. | Original retained; almost blank and unusable for element mapping. |
| [`code.html`](./code.html), 9,096 characters, SHA-256 `21a1cc9001c2051c46c0cf1db4b66e6f0262bc2046e9206f956bca2716fe77fa` | Static page prototype: public header, breadcrumb, checkout-unavailable card, return anchor and footer. | No form, button, input, fetch/XHR, API path or event handler. |
| Inventory row 19 in [`list_screen.md`](../../../list_screen.md) and ST-05 row in [`dd_screens/PLAN.md`](../../dd_screens/PLAN.md) | Candidate route, #08/#16, revalidation, explicit confirmation, order handoff, states and blockers. | Expected design; not evidence of implementation. |
| [AC-12](../../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Student precondition; #08 course detail → #15 enrollment status → free/paid branch; paid path creates pending Order, then payment/enrollment flow. | Design flow. Its sequence does not identify the inventory’s second #08 revalidation point. |
| [API catalog #08/#16](../../../../../../docs/lists/list_api.md) and [API #16 DD](../../../../../study-server/docs/dd/16_orders/02_Overview.md) | Method, actor, request/response, status/business codes and unresolved fields. | #08 current source-backed; #16 catalog contract and Draft DD only. |
| API #16 `OPEN_QUESTIONS.md`, `05_Data_Mapping.md`, `06_Error.md`, `PLAN_RESULT.md` | Persistence, provider, amount/currency, status, direct-call and rollback/idempotency gaps. | `NEEDS USER DECISION` / `SOURCE_REQUIRED`; no implementation proof. |
| Current #08 route/module/query/mapper/test and Study Server route search | Verify course read and check #16 implementation. | #08 route is source-backed/read-only; no #16 route/module/query/test found. Tests were not run. |
| [DB_UNICA_TABLES.md](../../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [DB_UNICA_ERD.drawio](../../../../../study-server/docs/diagrams/DB_UNICA_ERD.drawio), and checked-in [DB.sql](../../../../../../infra/postgres/study-server/DB.sql) | Check order/payment persistence evidence. | ERD V1 and DDL include `payments` but no `orders`; checked-in files do not prove live schema/deployment. |
| Current Study Web tree and [`design.md`](../../../../../../.agents/web-study/design.md) | Check route availability and design conventions. | No editable `src`, router or package manifest; Study Web is `UNWIRED`. Design guide is target guidance, not runtime evidence. |

## 3. Expected behavior and current behavior

### Expected behavior

Inventory row 19 expects Student checkout for the paid branch of AC-12. The candidate flow is:

```text
ST-04 / courseId
→ revalidate published course with API #08 (inventory requirement)
→ show approved amount/provider/terms
→ explicit Student confirmation
→ POST API #16 once per user action
→ retain the returned order identifier
→ ST-06 payment flow
```

API #16 catalog contract: `POST /api/v1/orders`, Bearer JWT, role Student, body `{course_id:int64!, payment_provider:PaymentProvider!}`; success 201 `DESIGN_RESOURCE_CREATED` with logical Order `{id,course_id,user_id,amount,currency,status,created_at}`; catalog errors 401/403/422/500. AC-12 says the paid path creates an Order in initial status `PENDING`.

### Current behavior

- The current HTML renders a public shell with Sign In/Sign Up, a breadcrumb, a static payment-unavailable status card and footer. The card says “Quy trình thanh toán chưa thể bắt đầu.” and explains that order information could not be initialized. No amount, currency, provider, course identity, confirmation, order ID or API result is present.
- The CTA label is “Quay lại kiểm tra ghi danh” but its anchor target is `/courses`. The breadcrumb item “Kiểm tra ghi danh” also targets `/courses`.
- `screen.png` does not depict the HTML. If rendered successfully, `screen_rendered_from_html.png` will be derived from the valid HTML and clearly remain a separate artifact.
- Study Web has no editable app source/router/package manifest and no checkout route. API #08 is a read-only current route; API #16 is not wired in Study Server.

### Discrepancies to retain

1. Inventory requires a second #08 read before #16; AC-12 only places #08 before #15 and the paid/free branch. The timing and stale-price behavior are not specified.
2. AC-12 requires Student login, while this prototype exposes the public guest shell. No Study Web guard is wired.
3. The visible prototype is an unavailable state with no confirmation control, while inventory expects a confirming/order-creating flow.
4. Prototype CTA/breadcrumb wording says enrollment check, while both link to `/courses`; no `courseId` is passed.
5. API #16 requires `payment_provider`, but allowed values and relationship to API #17 `provider` are unresolved. The response’s amount/currency have no approved source/mapping.
6. The logical Order lacks a physical table in ERD V1 and checked-in `DB.sql`. Do not map it to `payments`, which belongs to the subsequent payment step.
7. Inventory says retain `order_id`; API #16 response defines `data.id`, but API #17 uses `order_id:int64`. Treat them as a candidate identifier handoff only until the owner confirms mapping/continuity.
8. AC-12’s #18 node is not connected in its sequence; catalog API #18 uses `operation_id:int64` while the AC diagram node shows UUID. Its status lifecycle is also unresolved and remains a downstream ST-06 blocker; do not specify it here beyond the handoff boundary.

## 4. Planned marker targets

Measure target DOM bounds after rendering at a 1280×1024 CSS viewport and device scale 2. Each visible target receives one sequential `ST05-EL-01`… ID and one numbered marker. Group related links into a navigation target, with each link listed in the corresponding DD row. If the rendered layout changes the targets, update this plan before writing marker JSON/SVG or the annotated image.

| Marker | Target | Evidence boundary |
|---:|---|---|
| #1 | Header Study2Work brand link | Static `href="/"`. |
| #2 | Header primary navigation group | Home, Courses, My Courses, Progress anchors. |
| #3 | Header Sign In link | Static `/login`; does not prove auth guard. |
| #4 | Header Sign Up link | Static `/register`. |
| #5 | Breadcrumb group | Home, Courses, and “Kiểm tra ghi danh”; each link target recorded. |
| #6 | Cart/checkout status icon | Static `shopping_cart_checkout` visual. |
| #7 | Centered status card/surface | Layout container for the unavailable state. |
| #8 | H1 “Kiểm tra đơn hàng” | Static page heading. |
| #9 | Status headline | “Quy trình thanh toán chưa thể bắt đầu.”; prototype copy, not an API response. |
| #10 | Supporting explanation | Static unavailable-state text. |
| #11 | “Quay lại kiểm tra ghi danh” CTA | Anchor currently targets `/courses`; mismatch must remain visible. |
| #12 | Footer brand | Static Study2Work mark. |
| #13 | Footer navigation group | Home, Courses, Sign In and Sign Up anchors. |

## 5. Event plan

| Event | Trigger | Planned handling and limit |
|---|---|---|
| EV-01 Route entry and Student context | Candidate `/student/checkout/:courseId` load | Inventory route is proposed only. AC-12 expects logged-in Student; Study Web route/session guard is absent. No authenticated UI behavior can be claimed from the public prototype. |
| EV-02 Revalidate published course (#08) | Route `courseId` is available | Inventory requires GET #08 before confirmation. Catalog: public `GET /api/v1/courses/{course_id}`, `course_id:int64`; current handler returns a singleton `Page<Course>` on 200, 404 for unavailable/invalid IDs, and 500 on its mapper/system errors. This is read-only. AC-12 does not state the second-read timing or price-change policy. |
| EV-03 Explicit order confirmation | User activates an approved confirmation control | Expected by inventory but absent from current HTML. Do not create a control or enable this transition until amount, currency, provider and order terms are approved. |
| EV-04 Create Order (#16) | One explicit confirmation action after approved validation | Design contract: Student Bearer JWT; POST `/api/v1/orders`; required `course_id:int64` and `payment_provider:PaymentProvider`; 201 logical Order; 401/403/422/500. No #16 runtime exists. No retry/idempotency/duplicate/rollback/direct-call policy is specified. A response ID must not be handed to ST-06 until `data.id` ↔ `order_id` continuity is confirmed. |
| EV-05 Return to enrollment check | Activate CTA #11 | Current HTML follows `/courses`; there is no course ID. Desired ST-04 return route/data are not supported by the present anchor and require correction/approval. |
| EV-06 Header and footer navigation | Activate #1–#5 or #12–#13 | Record static `href` targets only. Candidate route availability and post-auth navigation are not verified. |

## 6. Blockers carried to DD

- Order physical schema, key, constraints, transaction/rollback and idempotency are unresolved; checked-in DDL is not live-schema proof.
- `PaymentProvider` values and its relationship to API #17’s separate `provider` are unresolved.
- Amount calculation/source, currency and behavior if price changes between ST-04 and ST-05 are unresolved.
- API #16 direct-call rules for free, unavailable or already-enrolled courses are unspecified; do not add 404/409 beyond its catalog contract.
- Inventory revalidation step differs from AC-12 sequence; needs an approved timing and stale-data rule.
- AC-12 Student precondition conflicts with public shell; Study Web route/auth guard is not wired.
- The expected confirmation control and event have no source-backed visual implementation in current HTML.
- Current CTA/breadcrumb route text does not carry the course identifier or return to ST-04.
- API #16 is design-only; #17/#18 and trusted payment verification are downstream and unverified.
- API #18 catalog `operation_id:int64` differs from the AC-12 diagram UUID; its lifecycle is not connected in the AC sequence.
- Original screenshot is blank compared with the HTML. Derived render provenance must be explicit; preserve the original.

## 7. Completion and status criteria

- Create `screen_rendered_from_html.png` only after this plan is saved; target 2560×2048 from CSS viewport 1280×1024 at 2× after document/fonts settle.
- Create sequential, unique, in-bounds DOM-measured marker records and annotation based on the derived render; keep marker positions off important text.
- Author `ST-05.md` sections A–F with every visible target and every identified event, distinguish expected design from current behavior, and mark API #16 `DESIGN_ONLY / UNWIRED`.
- Update inventory row 19 and global plan with the completed session and explicit blockers; do not change unrelated screens or API reverse-index classifications.
- Static audit: marker order/count/bounds and 1:1 DD mapping; JSON/XML parse; local links; image dimensions; original asset hashes; 83-screen inventory/folder count; core artifact count; scoped `git diff --check`.
- Do not run application tests/runtime. Keep statuses distinct: `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until contract gaps are resolved.

## 8. Execution record

- Plan saved before render, marker, annotation and DD authoring.
- `screen_rendered_from_html.png` SHA-256 `e64076e96e4dc62ca856c28c683821274d7c591806c7084495ac2d107b344f07`; `screen_annotated.png` SHA-256 `9f11165765094c6d6be5943d09bc4fbf8686e37f0feb5d023f5c954f1fe2626a`; both 2560×2048. Original `screen.png` and `code.html` hashes above remain unchanged.
- 13 DOM-measured markers are sequential, unique, inside the 1280×1024 CSS viewport and non-overlapping. JSON/SVG and DD element mapping were checked; annotation was visually reviewed.
- Static local-link, JSON/XML parse and image-dimension checks passed. Screen inventory/folder count is 83/83; four-core-artifact count is 80/83, with ST-01, ST-06 and ST-07 still incomplete.
- `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No application test or runtime was run.
