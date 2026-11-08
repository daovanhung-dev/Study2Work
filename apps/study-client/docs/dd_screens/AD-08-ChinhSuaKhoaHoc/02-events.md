# AD-08 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-08-EV-001` | `Source heading` / EV-01 — Load Course detail | See source event detail below |
| `AD-08-EV-002` | `Source heading` / EV-02 — Map successful Course data | See source event detail below |
| `AD-08-EV-003` | `Source heading` / EV-03 — Change a candidate field | See source event detail below |
| `AD-08-EV-004` | `Source heading` / EV-04 — Save Course metadata (#75) | See source event detail below |
| `AD-08-EV-005` | `Source heading` / EV-05 — Cancel or return to detail | See source event detail below |
| `AD-08-EV-006` | `Source heading` / EV-06 — Shell, support, preview and diagnostics affordances | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Load Course detail

- **Element/trigger:** Route entry from AD-07 or direct route; `Load` (not a numbered control).
- **Preconditions:** Proposed route is implemented; numeric ID and session token exist; access policy is approved.
- **Inputs:** `courseId` path string from `Course.id`. Target request #74: `GET /api/v1/admin/courses/{course_id}`, no body/query. Header `Authorization: Bearer <JWT>`.
- **Steps:** (1) Read route ID without substituting course code. (2) Request #74. (3) Validate HTTP/envelope and Course projection according to the confirmed contract. (4) On success, hand data to EV-02. (5) On error, select distinct auth/forbidden/not-found/service/network state. No retry/cache/timeout policy is currently specified.
- **API/current mapping:** API #74 is locally wired, read-only; its local implementation maps one Course to a singleton `Page<Course>`; API DD remains Draft. Do not call public #08 or infer counters/category/curriculum.
- **Outcome:** Success leads to target `ready`; 401/403/404/500 to corresponding state. Current prototype renders fixed values and sends no request. Runtime not verified.

### EV-02 — Map successful Course data

- **Element/trigger:** Internal UI render after EV-01 returns 200.
- **Inputs:** Confirmed Course page; local source fields include numeric ID, title, nullable description/thumbnail, decimal-string price, status and mentor. Final cardinality/nullability must follow approved API contract.
- **Processing:** Preserve ID for later #75 path; map only fields backed by response and approved UI. Keep price decimal exact in transport state; display formatting needs an owner-approved rule. Status and mentor are read-only under current #75 implementation. Never synthesize course code from ID, or counts from mockup labels.
- **Outputs:** Candidate fields render in form/preview; static thumbnail, Active badge, mentor, chapters, enrollment and batch code must not be shown as response data until bound to real fields/source.
- **Exceptions:** Missing/malformed response policy depends on final envelope contract. Current backend #74 projection failures return 500; no frontend fallback is implemented.

### EV-03 — Change a candidate field

- **Element/trigger:** `input` or `change` on title #26, mentor #32, price #35, description #38 or thumbnail #40; target only.
- **Preconditions:** Corresponding body field and UI control are approved and enabled. Current form is disabled; thumbnail area is not an input element.
- **Inputs:** User-edited draft. Local #75 candidate supports only `title`, `description`, `thumbnail_url`, `price`; no mentor, course code, status, file binary or counters.
- **Processing/result:** Keep draft in the screen state only under an approved client design. The existing artifacts do not define dirty tracking, formatting, null/clear UI, persistence across navigation, or validation timing. Current API candidate constraints are documented in EV-04; do not imply they are approved UI rules.
- **Thumbnail edge case:** A cleared URL could map to null in the candidate body, but there is no approved file-selection/upload or clear semantics. Do not accept the prototype's dimensions/file types/size as a validator.
- **Current result:** No control can be edited; no change event is wired.

### EV-04 — Save Course metadata (#75)

- **Element/trigger:** Save button #43; `Submit`/click target. Current element is disabled `type=button`, so it does not submit.
- **Preconditions:** AC permission mapping, body/full-replacement semantics, selected fields and validation, thumbnail handling, route/client, response/revalidation strategy approved. Those blockers currently prevent implementation.
- **Input/API:** Bearer JWT; path `{course_id:int64}`; no query. Current local model expects strict `application/json` candidate with all four keys: `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`; extra keys forbidden. Body is omitted by catalog/AC; candidate requires API owner approval.
- **Ordered local server processing:** (1) Framework validates parsed body model; malformed/missing/wrong-type/extra fields may return 422 before view-level role guard. (2) Shared guard checks JWT role `ADMIN` → 401/403. (3) Parse signed-int64 path → 422 if invalid/out of range. (4) Candidate title length and price decimal validation → 422; title whitespace is retained and no nonblank rule exists; negative price is accepted. (5) Parameterized metadata UPDATE by course ID and `updated_at`; preserve status/mentor. (6) Missing row → rollback/404. (7) Query #74 Course/mentor projection in same transaction; validate identity and build singleton Course page; any query/projection/mapping issue → rollback/safe 500. (8) Commit only after response data validates; commit failure → rollback/safe 500. (9) Success → 200 `DESIGN_RESOURCE_UPDATED`, `Course updated.`, response envelope.
- **Response handling:** Local response contains `data.items[0]` and `pagination` values 1/1/1/1, plus `success`, `businessCode`, `message`, `meta`, `traceId`; Page cardinality is local/DERIVED. Decide whether client uses this response, performs another GET #74, or invalidates its cache before implementation.
- **Side effects/retry:** Local SQL changes only legacy metadata columns and `updated_at`; no status, mentor, audit, multipart, S3 or counter operation. No concurrency token/409 contract. Retry/timeout/double-submit behavior is not specified; identical PUT still changes timestamp.
- **Current result:** Button is disabled; no API request, UI state update, success toast, or navigation occurs.

### EV-05 — Cancel or return to detail

- **Element/trigger:** Back link #15 or Cancel #42; click.
- **Inputs:** Current proposed route, numeric Course ID, browser history, and possible unsaved edits. No state persistence contract is present.
- **Processing/result:** Current anchors both navigate to `/admin/courses`, despite #15 copy naming AD-07. Candidate target is AD-07 with same ID; exact route, history behavior, list restoration and unsaved-change guard remain open. Cancel/back does not itself call #75 or #74. If destination is AD-07, it may load #74 under that screen's approved policy.
- **Current result:** Native link navigation to list only. There is no dirty state or confirmation prompt.

### EV-06 — Shell, support, preview and diagnostics affordances

- **Element/trigger:** Click on #2–#15, #46–#57, #59–#61; `Click`/`Load`/static render.
- **Inputs:** Static markup only. No route map, support URI, PDF, auth/session data, health signal, or analytics contract is supplied.
- **Processing/result:** Current `#` anchors only navigate to fragment; notification button has no handler; labels/cards do not trigger requests. Do not create routes, monitoring, downloads, audit behavior or permission claims from their copy. Wire only after source contracts exist.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
