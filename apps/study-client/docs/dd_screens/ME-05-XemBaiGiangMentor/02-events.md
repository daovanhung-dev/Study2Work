# ME-05 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-05-EV-001` | `ME05-EV-01` / ME05-EV-01 — Open lecture detail / GET #48 | See source event detail below |
| `ME-05-EV-002` | `ME05-EV-02` / ME05-EV-02 — Map successful response and render states | See source event detail below |
| `ME-05-EV-003` | `ME05-EV-03` / ME05-EV-03 — Breadcrumb to ME-02 course list | See source event detail below |
| `ME-05-EV-004` | `ME05-EV-04` / ME05-EV-04 — Breadcrumb to ME-03 course workspace | See source event detail below |
| `ME-05-EV-005` | `ME05-EV-05` / ME05-EV-05 — Copy lecture link | See source event detail below |
| `ME-05-EV-006` | `ME05-EV-06` / ME05-EV-06 — Preview Student lesson (ST-11) | See source event detail below |
| `ME-05-EV-007` | `ME05-EV-07` / ME05-EV-07 — Change lecture status | See source event detail below |
| `ME-05-EV-008` | `ME05-EV-08` / ME05-EV-08 — Edit lecture | See source event detail below |
| `ME-05-EV-009` | `ME05-EV-09` / ME05-EV-09 — Media player controls | See source event detail below |
| `ME-05-EV-010` | `ME05-EV-10` / ME05-EV-10 — Jump to chapter | See source event detail below |
| `ME-05-EV-011` | `ME05-EV-11` / ME05-EV-11 — Copy code sample | See source event detail below |
| `ME-05-EV-012` | `ME05-EV-12` / ME05-EV-12 — Download an asset | See source event detail below |
| `ME-05-EV-013` | `ME05-EV-13` / ME05-EV-13 — Open PDF | See source event detail below |
| `ME-05-EV-014` | `ME05-EV-14` / ME05-EV-14 — Open GitHub repository | See source event detail below |
| `ME-05-EV-015` | `ME05-EV-15` / ME05-EV-15 — Display lecture analytics | See source event detail below |
| `ME-05-EV-016` | `ME05-EV-16` / ME05-EV-16 — Read/reply to lesson discussion | See source event detail below |
| `ME-05-EV-017` | `ME05-EV-17` / ME05-EV-17 — Open all discussions | See source event detail below |
| `ME-05-EV-018` | `ME05-EV-18` / ME05-EV-18 — Course structure and previous/current/next lesson | See source event detail below |
| `ME-05-EV-019` | `ME05-EV-19` / ME05-EV-19 — Global header search, notifications and account | See source event detail below |
| `ME-05-EV-020` | `ME05-EV-20` / ME05-EV-20 — Footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 4. Event specification

All behavior below is an expected DD contract candidate unless tagged **CURRENT SOURCE**. Current `code.html` has no inline handlers; all anchors target `#`. No browser action is runtime verified.

### ME05-EV-01 — Open lecture detail / GET #48

- **Trigger/input:** Open proposed `/mentor/lectures/:lectureId`; `lectureId` is a path string; authenticated Mentor Bearer token is required by API #48.
- **Preconditions:** Browser route exists, auth token is available, and requested lecture is in the access scope accepted by the API. The first two conditions are not currently wired/verified.
- **Processing (current source):** API checks MENTOR auth first; parses signed int64; Q1 resolves non-DELETED lecture + parent course; enforces direct owner; Q2 resolves ordered uploads within owner/purpose/course scope.
- **Success/output:** 200 `DESIGN_RESOURCE_RETRIEVED`, `data:Lecture`; render only returned fields, preserve `content:null`, `assets:[]`, and stored status. Do not infer author/course name/video/analytics.
- **Errors:** 401 authentication required; 403 access denied (wrong role or direct-owner mismatch); 404 invalid/missing/deleted lecture; 500 safe internal error for DB/parent/asset mapping failures. Source has no API #48 422 branch for path parse.
- **Side effect:** Read-only; no commit or mutation.
- **Evidence/status:** Route/module/tests exist locally; source test uses fake DB and was not run in this task; deployment/runtime not verified.

### ME05-EV-02 — Map successful response and render states

- **Trigger/input:** Successful #48 envelope.
- **Processing:** Map `data.id/title/course_id/content/assets/order/status` as defined in §2. Do not synthesize values for missing screenshot panels. Confirm whether `content` is renderable before interpreting it as formatted notes.
- **Output:** `ready` state only for source-supported fields. `content:null` and `assets:[]` are successful values, not transport errors. No per-panel partial-load behavior is possible from #48 alone.
- **Errors/status:** UI loading/retry/cancel/partial-content behavior remains unimplemented. Do not show fixture values as fallback.

### ME05-EV-03 — Breadcrumb to ME-02 course list

- **Trigger/input:** Activate #6.
- **Processing/output:** Expected route to Mentor course list; retain no token in URL. Whether to preserve filters/page is unspecified.
- **Current:** `href="#"`; route/handoff not wired.

### ME05-EV-04 — Breadcrumb to ME-03 course workspace

- **Trigger/input:** Activate #7; course context requires `data.course_id` once #48 succeeds.
- **Processing/output:** Proposed `/mentor/courses/:courseId` (ME-03), with numeric `data.course_id`; sample course title/code is not supplied by #48.
- **Current:** `href="#"`; mapping from lecture route to workspace is proposed only. If load failed before `data.course_id`, return destination behavior is unresolved.

### ME05-EV-05 — Copy lecture link

- **Trigger/input:** Click #12.
- **Processing:** Construct canonical URL only after route/base URL rules are approved; write to clipboard only with user activation.
- **Output/error:** Show accessible success/failure feedback. No copy handler, clipboard permission fallback, URL format or toast design exists in source.
- **Status:** BLOCKED.

### ME05-EV-06 — Preview Student lesson (ST-11)

- **Trigger/input:** Click #13.
- **Processing/output:** Requires approved preview route, identity/role transition and privacy/access rules. #48 does not return a Student preview URL or preview entitlement.
- **Current:** No route or preview API is wired; the label crosses Mentor → Student context.
- **Status:** BLOCKED; do not use `/student/...` by guessing.

### ME05-EV-07 — Change lecture status

- **Trigger/input:** Click #14 and choose a status (choices not defined).
- **Current source:** #48 GET only. API #47 creates `PUBLISHED`; #48 returns stored status (except `DELETED` is hidden). No Mentor status mutation endpoint was identified in this screen contract.
- **Output:** No mutation can be submitted. Do not show selectable state or optimistic update.
- **Status:** BLOCKED pending approved status state machine/API.

### ME05-EV-08 — Edit lecture

- **Trigger/input:** Click #15.
- **Current:** No Mentor lecture update endpoint/route in ME-05 inventory or #48. Do not repurpose #51, which is Content update, as lecture update.
- **Output/status:** No edit navigation; hide/disable until owner confirms endpoint and body.

### ME05-EV-09 — Media player controls

- **Trigger/input:** Player buttons: play/pause, seek/progress, volume, speed, captions, watermark and fullscreen.
- **Required data:** Media resource/stream URL, duration, subtitle/caption tracks, allowed speeds and playback policy. None appears in #48; the HTML has no `<video>` or media source.
- **Output/error:** No playback state or media error behavior can be specified from current contract. No mock transcript/stream should be presented as server data.
- **Status:** BLOCKED; define media API, source and access before implementation.

### ME05-EV-10 — Jump to chapter

- **Trigger/input:** Select one of the three visible chapter cards in #17.
- **Processing/output:** Requires chapter IDs/time ranges and playable media; #48 returns neither. Watched/completed state is not a #48 field.
- **Status:** BLOCKED; displayed times/titles are fixtures.

### ME05-EV-11 — Copy code sample

- **Trigger/input:** Click #19.
- **Processing/output:** Would copy selected #20 code text and announce result. No code field/source or handler exists; code is hardcoded in the HTML.
- **Status:** BLOCKED until code content ownership and clipboard feedback are agreed.

### ME05-EV-12 — Download an asset

- **Trigger/input:** Click #22 on one `data.assets[]` item.
- **Processing:** Resolve item by returned asset ID and metadata; use `url` only under an approved access policy. Do not construct a URL from ID or trust screenshot filename.
- **Output/error:** Browser download, filename/disposition, auth, expired URL and retry behavior are not defined. #34/#48 local source returns a URL but object storage/provider reachability has not been exercised.
- **Status:** BLOCKED pending access and download contract.

### ME05-EV-13 — Open PDF

- **Trigger/input:** Click #23.
- **Processing/output:** Only eligible if `content_type` and URL policy confirm preview support. The label says PDF but API permits generic upload bytes/MIME.
- **Errors/status:** Unsupported MIME, unsafe external URL, auth failure and viewer behavior unspecified; do not assume PDF.

### ME05-EV-14 — Open GitHub repository

- **Trigger/input:** Click #24.
- **Processing/output:** External URL must come from an approved field and be validated; current repository/branch values are fixture text, not #48 assets contract.
- **Status:** BLOCKED; no destination/allowlist source.

### ME05-EV-15 — Display lecture analytics

- **Trigger/input:** Render #25.
- **Current:** #48 has no view count, retention, duration, rating, vote or realtime fields. No analytics API is declared for ME-05 inventory.
- **Output/status:** Do not render sample numbers/chart as actual values. Metric definitions/source/update frequency are blockers.

### ME05-EV-16 — Read/reply to lesson discussion

- **Trigger/input:** Render discussion previews (#26), then activate “Trả lời ngay” (#27).
- **Current:** #48 returns no discussion/thread IDs or reply contract. Card contents and action are static mockup text.
- **Output/status:** No data source, reply permission, route, write API or error state established. BLOCKED.

### ME05-EV-17 — Open all discussions

- **Trigger/input:** Activate #28.
- **Processing/output:** Mockup points to ST-25 and displays count 8. Inventory identifies ST-25 as Student-facing and does not link it from ME-05. Mentor discussion route/count/permissions need product decision.
- **Status:** BLOCKED; do not silently navigate Mentor to Student screen.

### ME05-EV-18 — Course structure and previous/current/next lesson

- **Trigger/input:** Render #29–#32; select a row if it is actionable.
- **Current:** API #48 returns only current lecture/order/course_id. ME-06 inventory uses #49 for a separate Content tree; #48 does not return lesson siblings, chapter tree, duration or next/previous IDs.
- **Output/status:** Current row can be identified by route lectureId only after routing is implemented. No sibling links, tree panel data or selection behavior can be fabricated. Decide whether the panel links to ME-06 or consumes another approved API.

### ME05-EV-19 — Global header search, notifications and account

- **Trigger/input:** Search typing (#3), notification (#4), account (#5), or global nav (#1–#2).
- **Current:** Input has no ID/form/handler; all anchors are `#`; badge `3` and Mentor profile are fixture content. No ME-05 API/session/nav shell source exists.
- **Output/status:** Destinations, search semantics, notification read state, menu actions and auth-expiry flow are not specified here. Keep as shell dependencies, not #48 effects.

### ME05-EV-20 — Footer navigation

- **Trigger/input:** Activate a footer link under #33.
- **Current/output:** All footer links are `#`; destinations and support workflow are absent. No route is claimed.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
