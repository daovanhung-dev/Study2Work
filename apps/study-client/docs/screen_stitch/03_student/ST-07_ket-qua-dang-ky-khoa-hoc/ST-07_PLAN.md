# ST-07 — Detailed Design Plan

## 1. Scope and sequence

- Screen: ST-07 “Kết quả đăng ký khóa học”, inventory row 21, candidate route `/student/enroll/result/:courseId`, AC-12, APIs #18/#19/#20.
- This session handles ST-07 only. Do not author ST-08 or another Screen ID.
- Sequence: inspect source and contracts → save this plan → render valid HTML separately because original PNG is nearly blank → measure DOM and finalize marker map → annotate the derived render → author A–F DD → update ST-07 inventory/global tracker/worklog → static audit.
- Preserve original [`screen.png`](./screen.png) (1280×1024, SHA-256 `d667f387fcecd0eb4bfe048a048932f4d555c9c3872018b69f4941dbca4d6500`) and [`code.html`](./code.html) (8,913 bytes, SHA-256 `c2661fe474dd1d0ed0f50dafca99310e2ec681899bb55ae554337a0c05436c58`). If the browser render is usable, save it as `screen_rendered_from_html.png` and use it as the separate annotation base. Do not overwrite the source assets.
- Keep AC/inventory/API design separate from current HTML and Study source. Do not invent payment confirmation, entitlement validation, trigger timing, request fields, status mapping, retry/idempotency, Operation ID handoff, pagination, response shape, course destination, or route behavior.
- The context registry identifies `createDD-markdown` as API-DD-only and excludes `web-ui-only-dd`; no canonical skill applies to this UI screen DD.
- Do not run application tests or runtime calls; use source inventories and static evidence only.

## 2. Evidence register and preservation

| Evidence | Purpose | Status / boundary |
|---|---|---|
| [`screen.png`](./screen.png), 1280×1024, SHA-256 `d667f387fcecd0eb4bfe048a048932f4d555c9c3872018b69f4941dbca4d6500` | Original design image. | Preserved; nearly blank and not usable for element mapping. |
| [`screen_rendered_from_html.png`](./screen_rendered_from_html.png) | Derived image for visual inspection/annotation. | Chrome 155 headless CDP; `file://code.html`; CSS viewport 1280×1024, DPR 2; `document.readyState=complete`, fonts loaded, Tailwind config present. The render has 2560×2048 pixels. |
| [`code.html`](./code.html), 8,913 bytes, SHA-256 `c2661fe474dd1d0ed0f50dafca99310e2ec681899bb55ae554337a0c05436c58` | Static public shell, breadcrumb, result card and CTA. | 14 literal anchors; no interactive controls, event handlers, API requests or dynamic enrollment result. Copy says result cannot be confirmed; not backend evidence. |
| [Inventory row 21](../../../list_screen.md) and [global plan](../../dd_screens/PLAN.md) | Candidate route, expected states, APIs, screen links and blocker. | Expected design only; not runtime proof. |
| [AC-12](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Paid/free enrollment sequence. | Free branch goes to #19; paid branch goes #16/#17/gateway/decision then #19 on success; #19 transaction precedes #20 and “Đã đăng ký”/open course. #18 is a detached node; AC-12 has no explicit ST-07 screen route. |
| [AC-13](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | My Courses list and empty state. | #20 Enrollment+Course query is followed by #21 progress and a client merge. Catalog #20 response still says UserProfile. |
| [API catalog #18/#19/#20](../../../../../../docs/lists/list_api.md) and [API #18 open questions](../../../../../../apps/study-server/docs/dd/18_operations/OPEN_QUESTIONS.md), [#19 DD/open questions](../../../../../../apps/study-server/docs/dd/19_courses_enrollments/), [#20 DD/open questions](../../../../../../apps/study-server/docs/dd/20_users_me_courses/) | Request/response/status, identity, lifecycle, enrollment mutation and course reload contract. | API #18/#19/#20 are catalog/Draft-only; current Study route/module/query/model/test is absent. #19 duplicate/eligibility/transaction details and #20 response/filter/page/empty semantics remain unresolved. |
| Current [Study route source](../../../../../../apps/study-server/app/api/v1.py), [route index](../../../../../../.agents/server-study/apis/declared-routes.md), [test inventory](../../../../../../.agents/server-study/tests.md) and focused source search | Verify runtime/API boundary. | Composition ends at #98; no #18/#19/#20 route/module/query/model/focused test found. No application tests run. |
| [DB tables](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [ERD](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_ERD.drawio), checked-in [DB.sql](../../../../../../infra/postgres/study-server/DB.sql) | Enrollment and Progress relationships/effects. | Design/DDL evidence only; table docs say Enrollment/Progress foreign keys are required, but SQL FK columns are nullable; no enrollment `(user_id, course_id)` unique constraint; live schema/deployment unverified. |
| Prior [ST-06 DD](../ST-06_thuc-hien-thanh-toan/ST-06.md) | Payment-to-result screen handoff. | ST-06 requires trusted server/gateway proof but #18 ID/access/lifecycle and result handoff remain blocked; route has courseId only, no operationId. |
| Current Study Web tree and [design guide](../../../../../../.agents/web-study/design.md) | Route availability and target visual/accessibility rules. | Editable source/router/package manifest absent; route is `UNWIRED`. Guide is intended design only and disallows adding remote imports. Prototype loads external Google Fonts and Tailwind CDN. |

## 3. Expected behavior and current behavior

### Expected behavior

AC-12 establishes this logical flow:

```text
free eligible course ───────────────────────────────┐
paid course → Order → Payment → trusted success ────┤
                                                    ↓
POST #19 → Enrollment + Progress transaction → GET #20 → display registered/open course
```

Inventory row 21 assigns a separate ST-07 result surface at `/student/enroll/result/:courseId`, lists states `awaiting-confirmation/enrolled/conflict/failure`, and APIs #18/#19/#20. It says #19 only after the backend proves free/paid entitlement and #20 refreshes My Courses. AC-12 itself has no explicit ST-07 route; #18 appears as a detached operation-status node. Do not infer that #19 runs automatically on every ST-07 page load or that #20's declared UserProfile payload can identify the course.

API #19 catalog contract: Student Bearer; `POST /api/v1/courses/{course_id}/enrollments`; path `course_id:int64!`; body notation repeats `course_id:int64!` and says `user from JWT:string!`; 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Enrollment>`; errors 401/403/404/422/409/500. AC-12 expects an Enrollment + Progress transaction and duplicate prevention. The API DD leaves request identity/wire field, entitlement/course guards, duplicate and concurrency semantics, lesson set, status/timestamps/defaults and physical schema source unresolved.

API #20 catalog contract: Student Bearer; `GET /api/v1/users/me/courses`; optional query `status:string`, `page:int32`; 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`; errors 401/403/422/500. AC-13 expects Enrollment + Course rows, then separately calls #21 for progress and merges client-side. The response type, filter meaning, pagination, empty wire shape and identity binding are unresolved.

API #18 is conditional only if an approved operation ID is supplied and the status contract is resolved. Catalog row uses int64; AC diagrams and shared Operation schema use UUID. Owner-only vs owner/Admin, status/lifecycle/result and poll/terminal rules are unresolved; it is detached from the AC-12 sequence.

### Current behavior

- Original `screen.png` is almost blank. `code.html` renders the public Study2Work header/footer, breadcrumb, page/card title, static icon, static “Chưa thể xác nhận kết quả đăng ký.” status, explanatory copy, and a CTA linking to `/student/courses`.
- The copy says the system has not recorded activation, but there is no API, Enrollment ID, payment status, operation ID, course identity/metadata, loading state, or dynamic data mapping. It does not establish that enrollment failed or is pending.
- The 14 anchors are literal links. There are no buttons, form controls, fetch/XHR or event handlers. Study Web has no editable route/client source; candidate ST-07 route is not wired.
- Study Server currently has no route/module/query/model/test for #18/#19/#20. API DDs and DDL are design evidence only; no current enrollment or progress initialization side effect is verified.

### Discrepancies to retain

1. AC-12 ends with #19 transaction → #20 reload → “Đã đăng ký”/open course; it does not name a separate ST-07 page. Inventory adds ST-07 and includes #18 plus awaiting-confirmation/conflict/failure states.
2. AC-12 #18 is detached; ST-07 route has `courseId`, not `operationId`. API #18 catalog says int64 while shared Operation/AC says UUID; access policy and lifecycle remain unresolved.
3. API #19 says body `course_id` plus “user from JWT” without an approved wire key/claim; course/payment eligibility, duplicate predicate, repeat/race behavior and 409 semantics remain open. AC-12's transaction intent does not define all Progress rows/defaults.
4. API #20 catalog returns `UserProfile`, while AC-13 requires a Course collection and empty-state decision. Status/page/empty/identity semantics are open.
5. Table docs say Enrollment/Progress foreign keys are required but checked-in SQL leaves those columns nullable and lacks a unique enrollment pair constraint; it does not prove live database state.
6. Current static “unconfirmed” card has no API or source state; do not label it as real pending/failure/enrolled state.
7. Current Study Web route/auth/client is unwired. Prototype uses remote fonts/CDN rather than the Study Web design guide's system font/no-new-remote-import target.

## 4. Planned marker targets

Render at a 1280×1024 CSS viewport and 2× device scale after this plan is saved; measure final target bounds in DOM and update this plan before marker JSON/SVG or annotation if the rendered layout changes the target list.

| Marker | Target and rendered DOM bounds (`x,y,w,h`, CSS px) | Evidence boundary |
|---:|---|---|
| #1 | Header Study2Work brand link — `32,14,149.281,36` | Static `href="/"`. |
| #2 | Header primary navigation group — `213.281,18,364.75,28` | Trang chủ, Khóa học, Khóa học của tôi, Tiến độ. |
| #3 | Sign In link — `1047.516,12,105.375,40` | Static `/login`; no auth guard. |
| #4 | Sign Up link — `1160.891,12,87.109,40` | Static `/register`. |
| #5 | Breadcrumb group — `32,96,1216,20` | Trang chủ, Khóa học, current “Kết quả đăng ký khóa học”; no course identity. |
| #6 | Page H1 — `32,140,1216,38` | “Kết quả đăng ký khóa học”; static page heading. |
| #7 | Result/status card surface — `304,202,672,389.5` | Layout only; not an Enrollment or payment record. |
| #8 | Assignment/check icon — `617.984,285,44.016,44` | Static decorative Material Symbol; does not mean enrollment succeeded. |
| #9 | Card title H2 — `456.609,371,366.766,30` | “Chưa thể xác nhận kết quả đăng ký.”; hard-coded copy. |
| #10 | Supporting status paragraph — `384,405,512,45.5` | Static text says activation is not recorded; not an API result. |
| #11 | “Về khóa học của tôi” CTA — `541.656,482.5,196.688,44` | Static anchor `/student/courses`; intended ST-08 link, route runtime unverified. |
| #12 | Footer brand group — `32,968,148.875,32` | Static non-anchor Study2Work mark. |
| #13 | Footer navigation group — `950.484,976,297.516,16` | Trang chủ, Khóa học, Đăng nhập, Đăng ký. |

**Final target count:** 13 grouped visible targets. The rendered DOM confirms the H1 and the card's status H2/body are distinct targets; no extra title/divider exists in the card. Marker centers/leader endpoints are recorded in `ST-07_markers.json` and `ST-07_markers_overlay.svg`.

## 5. Event plan

| Event | Trigger | Planned handling and boundary |
|---|---|---|
| EV-01 Route entry and Student/course context | Candidate `/student/enroll/result/:courseId` load | Authenticate Student and parse positive int64 only if approved route policy exists. Route/auth source absent. Route contains courseId, not operationId or trusted outcome. No implicit mutation on refresh. |
| EV-02 Create enrollment via #19 | Approved trigger after backend proves free entitlement or trusted paid success | Student Bearer; POST `/api/v1/courses/{course_id}/enrollments`; preserve path/body request notation and unresolved JWT identity field; 201 Enrollment; errors 401/403/404/422/409/500. Enrollment + Progress transaction is AC-12 design only; trigger ownership, repeat/idempotency and response mapping need approval. |
| EV-03 Track payment Operation via #18 | Conditional only if a trusted Operation ID is handed off and tracking contract is approved | GET `/api/v1/operations/{operation_id}`; Bearer JWT; catalog 200/401/403/404/500; row int64 conflicts with AC/shared UUID. No ID in route, no AC-12 edge, no current route/store; do not synthesize or poll. |
| EV-04 Refresh My Courses via #20 | After an approved #19 success when AC-12 flow calls for refresh | GET `/api/v1/users/me/courses`; Bearer Student; optional `status:string`, `page:int32`; 200 UserProfile / errors 401/403/422/500. AC-13 expects Course list; no current mapping/cache/empty behavior. Do not use this response as invented enrollment confirmation. |
| EV-05 Map server-confirmed outcome to result state | Verified #19 response or approved payment/Operation outcome | Map only after contract defines success, pending, conflict and failure; no current UI state machine. Unknown/timeout/missing response must not be reported as enrolled or failed. |
| EV-06 Navigate to My Courses | Click marker #11 | Browser follows literal `/student/courses`; intended ST-08. No request/mutation on click; current route availability unverified. No course ID is passed. |
| EV-07 Shared header/breadcrumb/footer navigation | Click markers #1–#5 or #13 | Follow literal anchors only if route exists. No course/result identity or auth-aware behavior in current HTML; mobile nav replacement not present. |

## 6. Blockers carried into DD

- Product/API owner must decide whether ST-07 exists as a separate route and which screen owns the one-time #19 POST; define safe direct entry and repeated-page-load behavior.
- Resolve ST-06 → ST-07 trusted payment proof, Operation ID handoff, #18 ID type, ownership/access, result mapping, polling interval and terminal states.
- Resolve API #19 body identity wire shape, course/payment entitlement guards, duplicate predicate/repeat/race handling, 409 rule, transaction boundary, lesson set/defaults and EnrollmentStatus/timestamp mapping.
- Resolve API #20 response schema vs AC-13 course list, query filter meaning, page contract, empty result shape and JWT-sub-to-Enrollment mapping.
- Wire Study Web route/auth/client and Study Server #18/#19/#20 before implementation/runtime verification; confirm live schema before relying on DDL.
- Confirm course navigation destination (ST-08 vs course detail) and carry required course ID only under an approved contract.
- Align prototype fonts/CDN with the Study Web design guide before implementation.

## 7. Completion and verification criteria

- Save this plan before creating the derived render, marker map/SVG, annotation or ST-07 DD.
- If source screenshot is unusable, preserve it and create separate `screen_rendered_from_html.png`; annotate that render and document its provenance.
- Finalize unique sequential DOM-measured markers and in-bounds positions; 1:1 match every marker to an ST-07 DD element row; keep callouts off meaningful text.
- Author ST-07.md sections A–F with expected/current separation, route/actor/preconditions, visible elements, each identified event's inputs/ordered handling/API/auth/status/errors/side effects/output, state matrix and navigation payloads.
- Keep unresolved API/AC/source discrepancies as blockers. Do not claim `DD READY`, implementation completion, or runtime verification where gates are open.
- Update only ST-07's inventory/global plan rows plus append the session checkpoint; do not start ST-08.
- Static audit: source hashes unchanged; image dimensions/provenance; JSON/XML; marker order/count/bounds/DD mapping; local Markdown links; 83 inventory IDs and folders; core artifact count; authored text whitespace; scoped `git diff --check`.
