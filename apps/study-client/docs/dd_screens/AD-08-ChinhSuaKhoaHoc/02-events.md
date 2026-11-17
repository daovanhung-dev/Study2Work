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
- **Preconditions:** Angular route/page and GET #74 caller are present in source; raw route ID and Admin session are available. AC-32 permission mapping remains open; browser/deployment runtime is unverified.
- **Inputs:** `courseId` path string from `Course.id`. Target request #74: `GET /api/v1/admin/courses/{course_id}`, no body/query. Header `Authorization: Bearer <JWT>`.
- **Steps:** (1) Read route ID without substituting course code. (2) Request #74. (3) Validate HTTP/envelope and Course projection according to the confirmed contract. (4) On success, hand data to EV-02. (5) On error, select distinct auth/forbidden/not-found/service/network state. No retry/cache/timeout policy is currently specified.
- **API/current mapping:** API #74 is locally wired, read-only; its local implementation maps one Course to a singleton `Page<Course>`; API DD remains Draft. Do not call public #08 or infer counters/category/curriculum.
- **Outcome:** Angular source maps the response into `loaded`; API/network failures map to `error`. The Stitch prototype still renders fixed values without a request. Browser/deployment runtime is unverified.

### EV-02 — Map successful Course data

- **Element/trigger:** Internal UI render after EV-01 returns 200.
- **Inputs:** Confirmed Course page; local source fields include numeric ID, title, nullable description/thumbnail, decimal-string price, status and mentor. Final cardinality/nullability must follow approved API contract.
- **Processing:** Preserve the raw route ID; current Angular source maps title, description, price, status, mentor and thumbnail URL from #74. Title/description/price populate a local draft; mentor/status are read-only. Never synthesize course code from ID or counts from mockup labels.
- **Outputs:** Angular form/preview shows mapped draft fields, mentor/status and thumbnail URL as text. It does not load an image or show chapter/enrollment metrics or batch code. Stitch prototype values remain static.
- **Exceptions:** Missing/malformed response policy depends on final envelope contract. Current backend #74 projection failures return 500; no frontend fallback is implemented.

### EV-03 — Change a candidate field

- **Element/trigger:** Angular `input` on title #26, price #35 or description #38 updates the local draft. Mentor is read-only; thumbnail selection is unavailable.
- **Preconditions:** Angular title/price/description inputs are enabled for component-memory drafts. Persistence/body approval remains open; thumbnail area is not a file input.
- **Inputs:** User-edited draft. Local #75 candidate supports only `title`, `description`, `thumbnail_url`, `price`; no mentor, course code, status, file binary or counters.
- **Processing/result:** Current Angular source updates a component-memory draft and local preview. It has no dirty indicator, persistence, or client validation. Current API candidate constraints are documented in EV-04; do not imply they are approved UI rules.
- **Thumbnail edge case:** A cleared URL could map to null in the candidate body, but there is no approved file-selection/upload or clear semantics. Do not accept the prototype's dimensions/file types/size as a validator.
- **Current result:** Title, description and price inputs emit draft changes; ID and mentor are read-only, thumbnail selection and Save are disabled. No PUT request is wired.

### EV-04 — Save Course metadata (#75)

- **Element/trigger:** Save button #43; `Submit`/click target. Current element is disabled `type=button`, so it does not submit.
- **Preconditions:** Route/client source exists. AC permission mapping, body/full-replacement semantics, selected persisted fields and validation, thumbnail handling, and response/revalidation strategy remain blockers to enabling Save.
- **Input/API:** Bearer JWT; path `{course_id:int64}`; no query. Current local model expects strict `application/json` candidate with all four keys: `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`; extra keys forbidden. Body is omitted by catalog/AC; candidate requires API owner approval.
- **Ordered local server processing:** (1) Framework validates parsed body model; malformed/missing/wrong-type/extra fields may return 422 before view-level role guard. (2) Shared guard checks JWT role `ADMIN` → 401/403. (3) Parse signed-int64 path → 422 if invalid/out of range. (4) Candidate title length and price decimal validation → 422; title whitespace is retained and no nonblank rule exists; negative price is accepted. (5) Parameterized metadata UPDATE by course ID and `updated_at`; preserve status/mentor. (6) Missing row → rollback/404. (7) Query #74 Course/mentor projection in same transaction; validate identity and build singleton Course page; any query/projection/mapping issue → rollback/safe 500. (8) Commit only after response data validates; commit failure → rollback/safe 500. (9) Success → 200 `DESIGN_RESOURCE_UPDATED`, `Course updated.`, response envelope.
- **Response handling:** Local response contains `data.items[0]` and `pagination` values 1/1/1/1, plus `success`, `businessCode`, `message`, `meta`, `traceId`; Page cardinality is local/DERIVED. Decide whether client uses this response, performs another GET #74, or invalidates its cache before implementation.
- **Side effects/retry:** Local SQL changes only legacy metadata columns and `updated_at`; no status, mentor, audit, multipart, S3 or counter operation. No concurrency token/409 contract. Retry/timeout/double-submit behavior is not specified; identical PUT still changes timestamp.
- **Current result:** Button is disabled; no API request, UI state update, success toast, or navigation occurs.

### EV-05 — Cancel or return to detail

- **Element/trigger:** Back link #15 or Cancel #42; click.
- **Inputs:** Current proposed route, numeric Course ID, browser history, and possible unsaved edits. No state persistence contract is present.
- **Processing/result:** Stitch prototype anchors navigate to `/admin/courses` despite #15 copy naming AD-07. Angular Back/Cancel RouterLinks navigate to `/admin/courses/:courseId` with the raw route ID. No dirty state or unsaved-change guard exists. Cancel/back does not call #75.
- **Current result:** Prototype links go to the list; Angular Back/Cancel links go to AD-07. There is no dirty state or confirmation prompt.

### EV-06 — Shell, support, preview and diagnostics affordances

- **Element/trigger:** Click on #2–#15, #46–#57, #59–#61; `Click`/`Load`/static render.
- **Inputs:** Static Stitch markup and current Angular page/layout. No support URI, PDF, health signal, or analytics contract is supplied.
- **Processing/result:** Stitch `#` anchors only navigate to fragment and its notification button has no handler. Angular page has no metrics, image load, support/download/monitoring effect. Do not create these behaviors from prototype copy.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
