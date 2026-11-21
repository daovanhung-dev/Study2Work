# ME-13 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-13-EV-001` | `Source heading` / E01 — Khởi tạo màn hình / tải course list | See source event detail below |
| `ME-13-EV-002` | `Source heading` / E02 — Chọn course và tải roster | See source event detail below |
| `ME-13-EV-003` | `Source heading` / E03 — Thay đổi recipient scope | See source event detail below |
| `ME-13-EV-004` | `Source heading` / E04 — Chọn/bỏ chọn từng học viên | See source event detail below |
| `ME-13-EV-005` | `Source heading` / E05 — Continue to ME-14 | See source event detail below |
| `ME-13-EV-006` | `Source heading` / E06 — Hủy bỏ | See source event detail below |
| `ME-13-EV-007` | `Source heading` / E07 — Header, breadcrumb and profile navigation | See source event detail below |
| `ME-13-EV-008` | `Source heading` / E08 — Footer links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### E01 — Khởi tạo màn hình / tải course list

- **Trigger:** entry vào route đề xuất /mentor/notifications/new/recipients; screen-level event, không có marker riêng.
- **Preconditions/input:** authenticated Mentor session and numeric identity; current source has no Study Web guard/router. Initialize courseId=null, roster=[], selectedIds=[], loading/error state. Scope default in screenshot is all, but runtime default requires confirmation.
- **Steps:** (1) Route guard checks Mentor session using the approved shared auth shell. (2) Clear stale ME-13 state unless confirmed resume behavior exists. (3) GET /api/v1/mentor/courses with Authorization: Bearer token; no query is required for default page, or use approved status/page/size. (4) On 200 DESIGN_RESOURCE_RETRIEVED, read data.items and data.pagination; map course.id to int64-safe option value, title to visible label. (5) Load subsequent pages if pagination indicates more and product expects the full set; keep request order stable. (6) Show course list; if items=[], show a course-empty state only after its copy/layout is designed. (7) On error, keep no stale course option marked selected and show app-approved error.
- **API/error:** GET #46, 200; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR. Network/timeout behavior follows the shared client policy, which was not found in this unwired app.
- **Output:** course options plus page metadata; no server mutation. Never infer semester/assignment from title.
- **Blockers:** HTML slugs do not map to API IDs; course status eligibility, complete-page fetching, current-semester label and assigned-Mentor scope need decisions. Do not claim this event currently executes.

### E02 — Chọn course và tải roster

- **Trigger:** change course selector #25.
- **Preconditions/input:** selected option must be a course returned by #46 with a valid int64 id. The HTML's static string slugs are not valid source evidence.
- **Steps:** (1) Read the selected option's source course id. (2) Clear old roster, selection IDs, derived count and old errors so recipients from course A cannot remain attached to course B. (3) Start GET /api/v1/mentor/courses/{course_id}/students with Bearer auth. (4) While pending, expose a roster loading state and keep Continue unavailable. (5) On 200, verify response.data is an array; map each item id/full_name/avatar_url and preserve source order; handle [] as roster-empty. (6) Apply response only if it matches the currently selected course, avoiding stale response overwrite. (7) On error, clear roster and selection; map error using source code and keep the course selection only if the shared UI policy permits.
- **API/error:** #62 path course_id:int64. 200 DESIGN_RESOURCE_RETRIEVED, data StudentSummary[]; 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND for invalid/nonexistent course; 500 DESIGN_INTERNAL_ERROR.
- **Output:** roster summaries and course context in client state. No server mutation, no pagination or progress data.
- **Edge cases:** malformed course ID => 404; missing/deleted course => 404; no direct ownership => 403; empty roster => success with []; repeated course changes must not show previous course rows. Do not add account or status filters on client.
- **Blockers:** course id mapping, eligibility of DRAFT courses, empty-roster action, cancellation behavior for in-flight GET and retry policy are not defined.

### E03 — Thay đổi recipient scope

- **Trigger:** click/change radio #28, #29 or #30.
- **Preconditions/input:** a chosen course and a successful #62 roster are required before a scope can yield IDs. Input values are all, support_needed, specific.
- **Steps:** (1) Validate value belongs to the three prototype values. (2) Update local scope only; no API is evidenced for this interaction. (3) For all, derive recipient IDs from every roster item; for specific, use only explicitly selected rows. (4) For support_needed, do not calculate a set from absent progress/attendance fields; show blocked behavior only after product chooses approved copy/action. (5) Keep selected count and estimated total consistent with unique IDs. (6) Disable Continue when course/recipient set is absent or invalid.
- **Output:** scope and candidate IDs held in temporary client state. The API #63 common-course check is a secondary enforcement and does not prove the exact displayed course.
- **Exceptions:** changing course clears IDs; empty roster yields 0; duplicate response IDs are rejected as inconsistent by #62 source, but client should still prevent duplicate selection.
- **Open decisions:** whether all is default; whether scope changes preserve prior specific selections; support-needed rule; what estimated count means for all vs specific; selection retention on back navigation.

### E04 — Chọn/bỏ chọn từng học viên

- **Trigger:** future row checkbox/selection control; no such visual element exists in this prototype, so there is no marker.
- **Preconditions/input:** #62 returned roster rows; selected row ID is an id from that response. Full name/avatar are display fields only.
- **Steps:** (1) Confirm row ID belongs to the currently selected course's loaded roster. (2) Add/remove that ID from selectedIds without duplicates, preserving roster order for stable handoff. (3) Recompute selected count from unique IDs; recompute estimated count only according to approved definition. (4) Set scope to specific if product confirms manual selection implies this. (5) Enable Continue only with a valid non-empty set.
- **Output:** explicit int64 IDs held in UI state; no API call.
- **Exceptions/security:** discard stale IDs after course change or roster reload; do not send names/emails as recipient identity; do not coerce int64 through an unsafe JavaScript number.
- **Blocker:** screenshot has no roster rows, checkbox, select-all row, pagination/search or loaded state. Row design and selection semantics need approval before implementation.

### E05 — Continue to ME-14

- **Trigger:** click disabled/enabled action #44 or next-step label #20 if it later becomes interactive.
- **Preconditions/input:** approved numeric course context and at least one recipient ID. #63 validator rejects blank recipients; no recipient count may be inferred from the course alone.
- **Steps:** (1) Revalidate selected course and recipient IDs against the loaded roster. (2) Reject stale, duplicate, malformed or empty selection; display approved inline feedback and remain on ME-13. (3) Preserve the selected IDs and context using the approved handoff mechanism. (4) Navigate to proposed ME-14 route only after state handoff succeeds. (5) ME-14 then resolves the Draft #63 encoding decision; ME-13 does not call POST #63. (6) On handoff/navigation failure, retain ME-13 state without fabricating a successful transition.
- **Output:** handoff data logically contains course_id:int64 and recipient_ids:int64[]; exact route-state contract/persistence is not confirmed. #63 currently takes recipients as CSV string and does not accept course_id.
- **Failure cases:** no course; empty recipients; current #63 403 common-course mismatch; stale route; missing auth. Do not retry a send because no send occurs here.
- **Blocker:** selected IDs transport, back-navigation restore, selected course relation and string CSV serialization require approval. The button copy says course-only requirement, while #63 also requires recipients.

### E06 — Hủy bỏ

- **Trigger:** click Hủy bỏ #42.
- **Input:** current temporary selections and route/session context.
- **Steps:** (1) Do not call API. (2) Navigate to the confirmed parent/list route or apply a confirmed draft-discard policy. (3) If unsaved selection should be retained/confirmed, use approved shared flow; no dialog is evidenced in this image.
- **Output:** leave ME-13 only when destination is configured.
- **Current behavior:** anchor href="#"; browser/app action is not wired. Destination, confirmation and state cleanup are unknown.

### E07 — Header, breadcrumb and profile navigation

- **Trigger:** activate markers #1–#10 as applicable to anchors; some header items include logo, navigation, bell and profile.
- **Input:** selected navigation item; no ME-13 data payload.
- **Steps:** (1) Resolve each link against an approved Study Web route. (2) Apply current Mentor shell/auth rules. (3) Navigate only after destination exists. No API call is evidenced from this screen.
- **Output:** destination-specific navigation.
- **Current behavior:** HTML anchors have href="#"; stepper elements are static text. No route destinations or handlers can be claimed. Do not map unrelated links to guessed screen IDs.

### E08 — Footer links

- **Trigger:** activate footer links #47–#49.
- **Steps/output:** open approved Mentor rules, assessment standards or technical-support destinations; no API call is evidenced.
- **Current behavior:** each href is "#"; no external URL, route or open-new-tab behavior is specified.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
