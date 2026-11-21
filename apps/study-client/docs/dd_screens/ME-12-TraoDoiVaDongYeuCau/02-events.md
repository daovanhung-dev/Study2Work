# ME-12 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-12-EV-001` | `Source heading` / D.1. Shared API envelope and error handling | See source event detail below |
| `ME-12-EV-002` | `Source heading` / E01 — Load request detail | See source event detail below |
| `ME-12-EV-003` | `Source heading` / E02 — Return to ME-11 | See source event detail below |
| `ME-12-EV-004` | `Source heading` / E03 — Edit reply draft and validate | See source event detail below |
| `ME-12-EV-005` | `Source heading` / E04 — Send reply | See source event detail below |
| `ME-12-EV-006` | `Source heading` / E05 — Resolve support request | See source event detail below |
| `ME-12-EV-007` | `Source heading` / E06 — Header, help and footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### D.1. Shared API envelope and error handling

API success envelopes expose success, businessCode, message, data, meta and traceId. For #59–#61, success data is one SupportRequest object. Use the API-returned businessCode and HTTP status; do not infer success from HTTP status alone. Optional null fields may be omitted by response serialization.

| Response field | Type/meaning | UI mapping |
|---|---|---|
| success, businessCode, message, meta, traceId | Envelope fields; success is boolean, businessCode/message are strings, meta is an object, traceId is a string. | Check success and businessCode; retain traceId for diagnostics according to shared logging policy, without logging message content. |
| data.id | Positive int64 SupportRequest identifier in the response model. | Must equal route requestId; mismatch is a projection error. |
| data.course_id | Positive int64 course identifier. | No course title/slug is returned by #59–#61; do not derive a label. |
| data.student | User summary with id:int64, full_name:string and optional avatar_url:string. | Render only where the approved thread header needs student identity; privacy/display policy remains open. |
| data.status | String status. | Map only confirmed values; #61 local lifecycle includes OPEN, IN_PROGRESS, WAITING_LEARNER, RESOLVED, CANCELLED. |
| data.messages[] | Ordered message array; each item has id:int64, author summary, content:string, attachments array and created_at:datetime. | Render in server order; no pagination metadata is returned. |
| message.author | User summary with id, full_name and optional avatar_url. | Message author/time layout is not present in source mockup. |
| message.attachments[] | UploadAsset response items with id, name, url, content_type, size_bytes and status. | Render only returned metadata and link; attachment UI and file safety/download policy remain open. |
| data.created_at / data.resolved_at | Request creation datetime; optional resolution datetime (null fields can be omitted). | Display format/time zone is not defined by this screen source. |

Current catalog error sets are:

| API | HTTP/business outcomes in local source |
|---|---|
| #59 GET detail | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR |
| #60 POST reply | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR |
| #61 PATCH resolve | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR, including STATE_NOT_RESOLVABLE; 500 DESIGN_INTERNAL_ERROR |

The exact safe message comes from the API response. Do not expose SQL/database details. No source contract declares 409, 503, a retry-after value, or a socket error code.

### E01 — Load request detail

- **Trigger:** Route entry, refresh/deep link, or an explicit future user-initiated retry.
- **Elements:** Screen-level load; #15 request ID, #16 status, #19–#22 conversation/empty state.
- **Inputs:** requestId from route, Mentor access token, optional X-Trace-Id. No body/query. Expected ME-11 handoff is #58 data[].id. API path uses request_id.
- **Preconditions:** Mentor session is available; route ID parses to the expected request key. Local APIs use signed int64 path parsing. #59 returns 404 for invalid/out-of-range ID; a valid but absent ID returns 404. Do not call with missing route data.
- **Processing:** (1) Enter loading state. (2) Send GET /api/v1/mentor/support/{request_id} with Authorization: Bearer token and optional X-Trace-Id. (3) API authenticates Mentor before path parse/DB, checks request and course ownership, reads the full thread and ordered attachment projections. (4) On 200 DESIGN_RESOURCE_RETRIEVED, validate data as one SupportRequest and verify response id matches route requestId. (5) Map status/student/timestamps/messages/attachments. (6) If messages is empty, show the approved empty-thread state; if nonempty, render a loaded-thread design only after layout is approved. (7) Leave operation state idle.
- **Success output:** One mapped request. #59 has no commit; the API reads request/course/student and full message/attachment data. Response order is created_at ASC NULLS FIRST then id ASC; attachment links are ordered by asset_position. No pagination or cursor.
- **Errors:** 401 shared session flow; 403 owner-scope denied; 404 absent or invalid request; 500 query/projection failure. Network failure is a client transport condition, not an API business code. Keep error state distinct from messages:[].
- **Retry/cache:** No automatic retry is specified. User retry repeats GET. Do not cache data across owner/session changes without shared auth cache policy.
- **Trace:** inventory row ME-12 and F09; API #59 route/module/query/view/models; API #59 test and Draft DD; AC-24 precondition.

### E02 — Return to ME-11

- **Trigger:** Click #9 breadcrumb or #11 back button.
- **Inputs:** Current route requestId may be used for analytics only if that is later approved; no navigation payload contract beyond returning to the support list exists.
- **Processing:** Navigate to proposed /mentor/support. Do not call #59/#60/#61. Do not fabricate filter restoration, list refresh or browser history semantics. A real router should preserve the Mentor session and guard destination.
- **Success output:** ME-11 inbox route. No mutation or backend side effect.
- **Failure/edge cases:** If no router exists, current href="#" is inert. Session expiry remains governed by the future shared auth boundary.
- **Trace:** inventory ME-12 related screen ME-11; ME-11 expected route /mentor/support; prototype anchor href="#".

### E03 — Edit reply draft and validate

- **Trigger:** Input/change on #25.
- **Inputs:** User-entered string; initial draft is empty. #24 currently displays a static 0 / 2000.
- **Processing:** (1) Keep draft in local page state. (2) Update a future counter from a documented counting rule. (3) Determine empty-only validation using trim/strip semantics compatible with #60. (4) Do not truncate text or enforce 2000 until BA/BE approves UI/API maximum and Unicode counting semantics. (5) Enable #27 only after request/status policy and service readiness are approved.
- **API:** None.
- **Success output:** Draft retained locally. The current HTML does not bind counter or validation.
- **Errors/edge cases:** Whitespace-only input is rejected by #60 with 422 if sent; prevent the request in the UI once the approved validation copy exists. Very long messages have no API maximum; this policy must be decided before release.
- **Trace:** code.html textarea id instructor-response-textarea, rows=5, no maxlength; literal static counter; #60 validate.py/message validation; API #60 OPEN_QUESTIONS Q60-05.

### E04 — Send reply

- **Trigger:** Submit/click #27.
- **Inputs:** requestId; Mentor Bearer token; message string; attachment_refs string. Current screen has no file picker, so use "[]" to represent an empty attachment list if the API is approved for this screen.
- **Preconditions:** Valid loaded request, valid Mentor session/ownership, non-whitespace message, approved status policy, no reply request currently in flight. Do not assume a maximum from the static counter.
- **Request:** POST /api/v1/mentor/support/{request_id}/reply; Content-Type application/json; Authorization: Bearer token; optional X-Trace-Id. Body has exactly message and attachment_refs. attachment_refs is a JSON-encoded string array of unique signed int64 UploadAsset IDs; empty list is serialized as the string "[]". Extra body fields are forbidden.
- **Processing:** (1) Keep original message text but reject trim-empty. (2) Serialize refs exactly once. (3) Send POST once and disable duplicate click while in flight. (4) Backend auth checks Mentor, parses path, locks request, verifies course owner and every upload is owned by the Mentor/course with purpose LECTURE and status UPLOADED. (5) Backend inserts support_messages and ordered upload links in one transaction. (6) Backend rehydrates/validates full SupportRequest response and commits once. (7) On 200 DESIGN_RESOURCE_UPDATED, map returned request as proof of successful post. (8) Perform the inventory-required GET #59 refresh. Do not repeat POST because the subsequent GET failed.
- **Success output:** Full updated SupportRequest with new message and ordered attachments, status preserved. Current API does not reopen the request. No idempotency key exists; an ambiguous POST retry can duplicate a message.
- **Errors:** 401 auth; 403 role/owner denial; 404 missing request or out-of-scope/missing upload; 422 malformed body/refs, whitespace-only message or invalid path; 500 DB/projection/commit failure. FastAPI request-body model validation may produce 422 before the view's auth guard. Backend transaction rolls back on pre-commit DB/projection failure. Keep draft after safe failure if confirmed by UX policy.
- **POST-success/refresh-failure:** Do not present the reply as failed and do not resend. Preserve the returned updated request and surface a refresh warning only through an approved common UI pattern.
- **Retry/cache:** No automatic POST retry. Disable repeat submit while pending. Manual recovery after an ambiguous transport result needs a user-visible policy because server idempotency is absent. Update thread/status only from successful API response.
- **Trace:** inventory ME-12 sequence; API #60 route/module/models/validate/query/view/tests; #60 Open Questions Q60-01, Q60-05, Q60-06, Q60-07, Q60-08 and Q60-09.

### E05 — Resolve support request

- **Trigger:** Click #32 only when the action is enabled under approved AC-24 satisfaction and lifecycle rules. The current mockup button is disabled and no confirmation modal exists.
- **Inputs:** requestId, Mentor Bearer token. No body, query, resolution reason or satisfaction payload.
- **Preconditions:** Request exists and is in Mentor scope. Source allows OPEN, IN_PROGRESS and WAITING_LEARNER; source idempotently accepts RESOLVED; source rejects CANCELLED and other unsupported states. Whether at least one exchange is required and how learner satisfaction is confirmed are unresolved.
- **Processing:** (1) Confirm user intent only through a BA-approved UI interaction; do not invent a modal. (2) Send PATCH /api/v1/mentor/support/{request_id}/resolve with Authorization and optional X-Trace-Id, no body/query. (3) Backend authenticates, parses signed int64, locks the request, verifies ownership, and checks lifecycle. (4) Active allowed status is conditionally updated to RESOLVED with resolved_at set once using COALESCE semantics. (5) A RESOLVED retry returns the request without a second transition; a CANCELLED/unsupported state returns 422. (6) Backend reloads the full thread, validates response and commits. (7) Map returned status/resolved_at and update local view. Do not assert settlement/survey side effects.
- **Success output:** Full SupportRequest, status RESOLVED for a new transition. resolved_at may be omitted/null on an idempotent retry of an existing row with no timestamp.
- **Errors:** 401 auth; 403 role/owner; 404 missing request; 422 invalid path/state; 500 DB/projection/commit error. Backend rolls back on failure. Network error is ambiguous; PATCH is idempotent for already RESOLVED state in current source, but client retry policy still needs confirmation.
- **Trace:** AC-24 decision YES→resolve, NO→keep OPEN; inventory ME-12; API #61 route/module/query/view/validate/tests and Draft DD; API #61 OPEN_QUESTIONS Q-61-02.

### E06 — Header, help and footer navigation

- **Trigger:** Click any apparent navigation/link element among #1–#8, #38 and #41–#43.
- **Inputs:** Click target only; prototype does not contain destinations beyond href="#".
- **Processing:** No API or mutation is supported by current source. Bind destinations only after route/URL ownership is confirmed. Support inbox item #5 should resolve to ME-11 when the app router is implemented. Header menu/profile behavior and guide/legal/support URLs remain unknown.
- **Success/failure:** No expected destination can be asserted from the prototype. Until a route is confirmed, these links remain an implementation blocker or are rendered as noninteractive text according to the approved shell design.
- **Trace:** code.html anchors href="#"; Study Web subcontext is UNWIRED.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
