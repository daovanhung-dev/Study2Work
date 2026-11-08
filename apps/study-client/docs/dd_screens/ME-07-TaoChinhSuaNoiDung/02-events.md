# ME-07 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-07-EV-001` | `ME07-EV-01` / ME07-EV-01 — Resolve editor mode from route | See source event detail below |
| `ME-07-EV-002` | `ME07-EV-02` / ME07-EV-02 — Load edit data with GET #49 | See source event detail below |
| `ME-07-EV-003` | `ME07-EV-03` / ME07-EV-03 — Edit title | See source event detail below |
| `ME-07-EV-004` | `ME07-EV-04` / ME07-EV-04 — Choose content type | See source event detail below |
| `ME-07-EV-005` | `ME07-EV-05` / ME07-EV-05 — Change display order | See source event detail below |
| `ME-07-EV-006` | `ME07-EV-06` / ME07-EV-06 — Enter detailed content/media | See source event detail below |
| `ME-07-EV-007` | `ME07-EV-07` / ME07-EV-07 — Create Content with POST #50 | See source event detail below |
| `ME-07-EV-008` | `ME07-EV-08` / ME07-EV-08 — Update Content with PUT #51 | See source event detail below |
| `ME-07-EV-009` | `ME07-EV-09` / ME07-EV-09 — Cancel unsaved work | See source event detail below |
| `ME-07-EV-010` | `ME07-EV-10` / ME07-EV-10 — Header, breadcrumb and footer navigation | See source event detail below |
| `ME-07-EV-011` | `ME07-EV-11` / ME07-EV-11 — Render side panels and session message | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Detailed event specification

### ME07-EV-01 — Resolve editor mode from route

- **Trigger:** open proposed ME-07 route.
- **Input:** `courseId` and optional `contentId` from path; Bearer session is required by the server APIs. No navigation state or loaded route exists in current Study Web.
- **Processing:** choose candidate create mode if `contentId` absent, edit mode if present; keep both IDs out of query-string secrets. API #50 needs course ID in body; #51 needs Content ID in path. The optional route syntax is from inventory only.
- **Output:** create form starts blank; edit form remains loading until #49 row is found. Exact entrypoints from ME-06 are not implemented.
- **Errors:** malformed IDs are eventually rejected by server paths (API #49 invalid course → 404; #51 invalid content ID → 404). Client route validation and user message are open.

### ME07-EV-02 — Load edit data with GET #49

- **Trigger:** route contains `contentId`; inventory proposes GET #49 to find existing Content. Create mode may also load #49 for course context; whether that extra fetch is required is unresolved.
- **Request:** `GET /api/v1/mentor/courses/{course_id}/content`, Bearer JWT, no body/query.
- **Steps:** auth role MENTOR → parse course int64 → direct-owner check → fetch every active Content row → validate flat projection/tree → return envelope. Client finds row where `data[].id == contentId` and confirms `course_id == route courseId` before populating title/type/payload; `order/status/parent_id` are preserved as read-only data unless field-write support is approved.
- **Success:** 200 `DESIGN_RESOURCE_RETRIEVED`; empty tree is 200 with `data:[]`. An edit ID absent from the collection becomes UI not-found. Do not invent a second detail API.
- **Errors:** 401; 403 role/owner; 404 bad/missing course; 500 DB/projection/tree failure. No partial collection. Cache policy, retry and loading feedback are not implemented.
- **Side effect:** none; #49 is read-only.

### ME07-EV-03 — Edit title

- **Trigger/input:** text input #9 `content_title` change.
- **Current markup:** input text field, no required/max-length/trim attribute or event logic.
- **Expected candidate:** store raw input in local form state and mark dirty; show validation only after title rule is approved. The visual star indicates required, and #50/#51 require the field to exist and be a string, but current server does not define nonempty, whitespace or length validation.
- **Output:** no request on keystroke; preserve unsaved text locally. On change/cancel/reload, unsaved-state policy requires explicit design.

### ME07-EV-04 — Choose content type

- **Trigger/input:** select #10 change; sample values `theory`, `reading`, `practice`.
- **Current:** no change handler; no server enum/payload correspondence.
- **Expected candidate:** set `content_type`, dirty state and select the matching subtype editor only after the allowed type list and payload schema are approved.
- **Output/error:** no API request on selection. Empty selection should not submit while visually required, but accepted values and validation code remain open; do not send these labels as a finalized enum by assumption.

### ME07-EV-05 — Change display order

- **Trigger/input:** numeric field #11.
- **Mockup rule:** `min=1`, label “Số nguyên dương”.
- **Current API:** #50 takes no order and allocates root order starting at 0; #51 does not take order and preserves current placement. #49 exposes `order:int32` only.
- **Output/status:** `BLOCKED`. Do not include `sort_order` in POST/PUT bodies (extra fields are forbidden). Decide whether to remove/disable the input, make it read-only, or add an approved reorder contract; do not silently coerce between 0-based and 1-based values.

### ME07-EV-06 — Enter detailed content/media

- **Trigger:** interact with panel #13 or locked note #14.
- **Current:** no contenteditable/textarea/upload control; the panel explicitly says it is waiting for protocol integration and locks media.
- **Expected:** a type-specific editor must serialize exactly one approved JSON object `payload` for #50/#51; media upload needs its own approved API/asset reference contract. No media API is part of ME-07’s inventory.
- **Output/status:** no current event/request; save cannot be enabled until payload schema/editor mapping exists. Do not send arbitrary HTML or infer Markdown/media keys.

### ME07-EV-07 — Create Content with POST #50

- **Trigger:** save action while in create mode. Current button is disabled; event is a contract candidate only.
- **Preconditions:** Mentor session, course access accepted by server, approved `content_type/title/payload`, valid `courseId`; agreed destination after create.
- **Request:** `POST /api/v1/mentor/content`; `Authorization: Bearer`; strict body `{course_id:int64, content_type:string, title:string, payload:object}`. No parent/order/status/version.
- **Processing:** Pydantic shape validation → MENTOR guard → lock course → compare numeric JWT principal to `courses.mentor_id` → compute next active root order (first 0) → insert Content root with `PENDING_REVIEW` → verify returned projection → commit.
- **Success:** HTTP 201 `DESIGN_RESOURCE_CREATED`, `data:Content`. Keep returned ID/type/title/payload/status/parent/order; inventory expects refresh/invalidate #49. Show a success state only after server success. Whether to stay in editor or return to ME-06 is not defined.
- **Errors:** 401 auth; 403 role, missing course or wrong direct owner; 422 body shape; 500 safe DB/mapping/commit error. The server has no idempotency key; do not auto-repeat an ambiguous network timeout, as a second POST may create a duplicate.
- **Side effect:** inserts one root; not an update of existing node.

### ME07-EV-08 — Update Content with PUT #51

- **Trigger:** save action while in edit mode with a current Content ID. Current button is disabled.
- **Preconditions:** #49 resolved exact row for the route course; user is Mentor owner; approved full-replacement body and payload schema; no server version token is available.
- **Request:** `PUT /api/v1/mentor/content/{content_id}`. Current-source body is `{content_type,title,payload}` and extra fields are rejected. This body is DERIVED and missing from catalog; do not declare it finalized until owner approval.
- **Processing:** auth → parse ID → lock current Content and Course → direct-owner check → insert prior state into `content_versions` with `version_no=MAX+1`/`archived_by` → update three body fields, set current status `PENDING_REVIEW`, retain course/parent/order → validate returned Content → commit.
- **Success:** HTTP 200 `DESIGN_RESOURCE_UPDATED` + Content, no `version` field. Refresh #49 per inventory; it returns current rows but cannot select an archived version.
- **Errors:** 401; malformed/missing/deleted ID 404; non-owner 403; invalid body 422; database/snapshot/update/mapping/commit 500. There is no 409/current-version check; stale forms are not detected by API source.
- **Side effect:** snapshot plus current-row update in one transaction. A PUT can reset a previously published current row to `PENDING_REVIEW`; public-reader behavior/version promotion remains an open lifecycle decision.

### ME07-EV-09 — Cancel unsaved work

- **Trigger:** click #15.
- **Current:** link targets `#`; no dirty-state handler or destination.
- **Candidate:** return to ME-06 with `courseId`, preserving no secret in URL. If dirty, show an accessible discard confirmation only after confirmation behavior/copy is decided. Never silently POST/PUT on cancel.
- **Output:** return destination and whether newly saved server state must be reloaded are open; no current runtime behavior.

### ME07-EV-10 — Header, breadcrumb and footer navigation

- **Trigger:** click #1–#5 or #29–#31.
- **Current:** all anchors are `href="#"`; profile is static. No notification/auth/profile/route handler exists.
- **Expected:** route map and course context must be bound from approved navigation contract; the current name/course/title sample does not provide `courseId`. These shell actions do not mutate Content.

### ME07-EV-11 — Render side panels and session message

- **Trigger:** screen render (elements #8, #17–#28).
- **Current:** mode label, data rules, “Đang đối soát”, two-thirds progress and image/caption are static. #49–#51 do not provide these values, status or progress.
- **Expected:** render policy text only when approved; never use a badge/progress bar as authorization. Server authorization remains the per-request MENTOR/direct-owner check. Use approved image source and semantic alt text; no event/API call is implied.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
