# ST-17 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-17-EV-001` | `ST17-EV-01` / ST17-EV-01 — Open assignment detail and request #33 | See source event detail below |
| `ST-17-EV-002` | `ST17-EV-02` / ST17-EV-02 — Map approved Assignment fields to the page | See source event detail below |
| `ST-17-EV-003` | `ST17-EV-03` / ST17-EV-03 — Deadline, countdown and late-policy display | See source event detail below |
| `ST-17-EV-004` | `ST17-EV-04` / ST17-EV-04 — Pre-submit checklist interaction | See source event detail below |
| `ST-17-EV-005` | `ST17-EV-05` / ST17-EV-05 — Open video, attachments and mentor contact actions | See source event detail below |
| `ST-17-EV-006` | `ST17-EV-06` / ST17-EV-06 — Continue to ST-18 submission preparation | See source event detail below |
| `ST-17-EV-007` | `ST17-EV-07` / ST17-EV-07 — Authentication, global navigation and failure handling | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả events

### ST17-EV-01 — Open assignment detail and request #33

- **Trigger/type:** route load; no visual marker. Actor Student.
- **Precondition:** proposed route has `assignmentId`; Student auth context must exist. Assignment/course entitlement and direct-entry/refresh rules are not approved.
- **Input:** `assignmentId` from path, expected int64 by API catalog; Student Bearer token from auth boundary. No `user_id`, query or body.
- **Steps:** (1) read the route parameter; do not invent positivity/range rules; (2) require Student auth context in client; (3) call GET #33 once with path `assignment_id` and Bearer; (4) parse only the approved envelope/schema; (5) on valid 200, enter a result-mapping state; (6) on catalog error/network/malformed response, enter safe error/not-found/access state and do not reuse screenshot data.
- **API:** #33 `GET /api/v1/assignments/{assignment_id}`; Student Bearer; no query/body; response `ApiEnvelope<Assignment>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500 per catalog. Route/module/test not found in current source.
- **Output:** target loading → open/closed/not-found/error; exact open/closed mapping is blocked by Q-33-01/02. There is no retry, cache or timeout policy in the #33 contract.

### ST17-EV-02 — Map approved Assignment fields to the page

- **Trigger/type:** API success response mapping.
- **Precondition:** HTTP 200 and valid `ApiEnvelope<Assignment>` under an approved projection.
- **Input:** `id:int64`, `course_id:int64`, `title:string`, `description?:string`, `due_at?:date-time`, `max_score:decimal-string`.
- **Steps:** (1) validate envelope/business code; (2) map title and optional description; (3) retain course/assignment IDs for approved route context; (4) show due date/max score only after null/timezone/decimal rules are set; (5) omit unsupported fields and avoid deriving progress/weight/rubric/status/history/mentor/resource data; (6) render the response without trusting sample copy as authoritative.
- **API:** #33 only. Do not call #09, #20, #34, #35 or #36 to fill missing ST-17 values without approved orchestration.
- **Output:** only server-supplied, policy-approved fields may be shown. `course_id`/`max_score` nullable DDL conflict and optional-field serialization remain blockers.

### ST17-EV-03 — Deadline, countdown and late-policy display

- **Trigger/type:** render/timer update; no authoritative API call beyond #33.
- **Precondition:** API supplies `due_at` and product/BE approves timestamp timezone, server-time source, deadline boundary and read-vs-submit enforcement.
- **Input:** candidate optional `due_at`; client wall clock may drift and timezone serialization is unspecified.
- **Steps:** (1) do not use local time to authorize submission; (2) do not infer open/closed from screenshot countdown or late-penalty copy; (3) only derive/display a countdown after clock/timezone rules are approved; (4) keep server decision authoritative; (5) treat AC-17 403/409 as unresolved against the #33 catalog set.
- **API:** no separate deadline/status endpoint is declared in ST-17. #33 may still return assignment after the deadline; Q-33-02 is open.
- **Output/exception:** until policy is approved, the displayed “5 days”, countdown digits, date and 10%/24h penalty remain samples. No automatic navigation or submission lock can be claimed.

### ST17-EV-04 — Pre-submit checklist interaction

- **Trigger/type:** click/tap/keyboard on four checkbox-like rows.
- **Precondition:** product owner defines whether rows are informational checks, local reminders, or persisted assignment completion data.
- **Input:** user toggle per row; current API provides no checklist state, validation rule or persistence endpoint.
- **Steps:** (1) do not count local checks as verified deliverables; (2) do not gate ST-18 or #35 on them; (3) do not persist/cache a checklist without an approved contract; (4) once semantics are approved, expose each row with label and checked state, keyboard operation and accessible name.
- **API:** none in current ST-17 contract.
- **Output:** current behavior is not wired; keep display-only/disabled until behavior is approved. The 0/4 screenshot value is sample.

### ST17-EV-05 — Open video, attachments and mentor contact actions

- **Trigger/type:** click/tap/keyboard on #14, #26–#28, #45–#46.
- **Precondition:** approved URL/resource ID, access/expiry policy and external destination are supplied.
- **Input:** displayed filenames, sizes, video title, Discord and office-hours labels are samples, not URLs/IDs.
- **Steps:** (1) do not build a download URL from filename; (2) do not treat API #34 upload as a download API; (3) do not infer public/private access, signed-link lifetime, preview or MIME behavior; (4) do not create Discord/calendar links; (5) enable only after source and destination contracts are approved.
- **API:** none is declared by the ST-17 row; #33 has no resource/mentor projection. Current #34 is a source-backed multipart upload (`purpose=SUBMISSION`) that returns an UploadAsset reference; it is not a resource-download API and is not called from this detail screen. Student #35/#36 have no current route/module/test.
- **Output:** actions are design-only and have no verified file, network or external side effect.

### ST17-EV-06 — Continue to ST-18 submission preparation

- **Trigger/type:** click/tap/keyboard on #36 CTA.
- **Precondition:** approved server state says assignment is open and Student may submit; current `Assignment` schema has no explicit status/eligibility field and #33 deadline behavior is unresolved.
- **Input:** current `assignmentId` path value; no form body or file payload on ST-17.
- **Steps:** (1) require an approved open/eligible state; (2) navigate to proposed ST-18 `/student/assignments/:assignmentId/submit` with the same assignment ID only; (3) do not call #34/#35/#36 from ST-17; (4) if access/deadline decision cannot be sourced, do not present the action as usable.
- **API:** none in ST-17; AC-17 calls #34 upload, #35 create submission and #36 confirmation later in the flow.
- **Output:** expected design handoff to ST-18, not a current route. Submission creation/status is not asserted on this screen.

### ST17-EV-07 — Authentication, global navigation and failure handling

- **Trigger/type:** route/API result or user activation of header/footer links.
- **Precondition:** route and shell implementation exist and destinations are approved.
- **Input:** Bearer auth result, #33 HTTP/business code, network/response error, or navigation input.
- **Steps:** (1) 401 → authentication-required state; exact reauth destination not defined; (2) 403 → access-denied state, keeping 403-vs-404 owner masking open; (3) 404 → not-found/unavailable without exposing another Student's data; (4) 500 → safe internal-error copy, no SQL/stack details; (5) network/malformed envelope → safe error, no sample fallback; (6) keep 409 out of the #33 implementation until catalog is changed; (7) do not infer header/footer routes from prototype links.
- **API:** only #33 catalog error set; no retry/cache policy specified.
- **Accessibility:** when implemented, use semantic anchors/buttons, visible focus, keyboard navigation, status text plus icons/text, responsive reflow and reduced motion per Study Web design target. These behaviors are target requirements, not current runtime.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
