# AD-24 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-24-EV-001` | `Source heading` / EV-01 — Load report | See source event detail below |
| `AD-24-EV-002` | `Source heading` / EV-02 — Change date bounds | See source event detail below |
| `AD-24-EV-003` | `Source heading` / EV-03 — Change learner segment | See source event detail below |
| `AD-24-EV-004` | `Source heading` / EV-04 — Apply filters | See source event detail below |
| `AD-24-EV-005` | `Source heading` / EV-05 — Reset filters | See source event detail below |
| `AD-24-EV-006` | `Source heading` / EV-06 — Refresh query | See source event detail below |
| `AD-24-EV-007` | `Source heading` / EV-07 — Export to AD-25 | See source event detail below |
| `AD-24-EV-008` | `Source heading` / EV-08 — Shell and footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Load report

- **Trigger / type:** future page entry, `Load`; no page load handler exists.
- **Precondition:** expected Admin principal with approved report/analytics permission. Current HTML establishes neither.
- **Inputs:** optional query values for #101 (`from?:date`, `to?:date`) and #102 (`from?:string`, `to?:string`, `segment?:string`). The screenshot date values are prototype literals, not approved defaults. No body or path parameter is declared for either API.
- **Expected API contracts:**
  - #101 `GET /api/v1/admin/reports/summary`; Bearer JWT, role Admin; `ApiEnvelope<Report>`; 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
  - #102 `GET /api/v1/admin/reports/community-impact`; Bearer JWT, role Admin; `ApiEnvelope<Report>`; same declared success/error set.
- **AC order:** diagram edges are `open → #101 → aggregate KPI → #102 → validate date range + report permission → aggregate learning/community metrics → render`. The position of validation after the #102 call is an unresolved sequence discrepancy; do not reorder silently.
- **Current processing:** nothing is called; static placeholders remain. No #101/#102 route/query/model/test exists locally.
- **Response and UI mapping:** Draft API DDs describe `Report.period`, `metrics[{key,value,label}]` and `generated_at`; concrete metric keys/formulas/empty semantics are not approved. Do not map `metrics[]` to the four KPI cards or chart without owner-approved semantics.
- **Errors/edge cases:** catalog lists only 401/403/500. Date parse/reversed-range errors have no declared 400/422; network timeout/retry, partial response, empty metrics, cache/freshness and duplicate-load policy are unspecified. Current page has no response states.

### EV-02 — Change date bounds

- **Trigger / type:** #18/#19 native date inputs, `change`.
- **Input/current validation:** values are browser date-input values; initial HTML values are `2025-01-01` and `2025-03-31`. There is no input listener, min/max, required flag or `from <= to` check.
- **Expected contract:** #101 accepts optional `date`; #102 accepts optional `string`. The two catalog types differ. API DDs propose ISO date parsing and inclusive windows, but mark date format/default/inclusive behavior as DERIVED; these are not approved validation rules.
- **Processing/output:** current browser control changes its local DOM value only. No API, URL or cache change occurs until Apply is clicked, and even Apply has no request.
- **Errors:** invalid dates/range have no cataloged business-code mapping. Do not add 400/422 or client messaging without approval.

### EV-03 — Change learner segment

- **Trigger / type:** #20 select `change`.
- **Input:** current values `all`, `interns`, `graduates`, `alumni`; default `all`.
- **Expected contract:** #102 exposes only `segment?:string`. API DD proposal uses `learning`/`community` to select metric groups and marks both values DERIVED. No mapping exists from audience labels to those metric groups. #101 does not accept a segment.
- **Processing/output:** current selection changes only in DOM; no normalization, API call, URL state or dependent option filtering occurs.
- **Exceptions:** blank, unknown, case variants and audience-to-metric semantics are not defined by catalog. No error response is listed for unknown segment.

### EV-04 — Apply filters

- **Trigger / type:** #21 button `click`.
- **Current precondition/input:** button is enabled; current values are whatever #18–#20 contain. No validation or dirty-state detection.
- **Current processing/output:** adds `opacity-80` then removes it after 300 ms. It neither reads the controls nor calls an endpoint; values and URL stay as they were.
- **Expected flow boundary:** inventory expects #101 summary and #102 filtered by `from/to/segment`; AC-38 draws #101 before #102. It does not define whether each click invokes both APIs, the precise refresh sequence, URL query format, debounce/cancellation, or how #101 `date` and #102 `string` are normalized.
- **Conditional request details:** if API calls are approved, #101 has no body and receives only optional date bounds; #102 has no body and receives optional string bounds/segment. Both use Bearer JWT/Admin and return `ApiEnvelope<Report>`; success 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500. Do not send `segment` to #101 or invent extra filters.
- **State/result/errors:** no current data is rendered or error state shown. Range validation, invalid segment, partial success between two calls, stale data policy, retry, concurrent clicks and cache update behavior are open.

### EV-05 — Reset filters

- **Trigger / type:** #22 button `click`.
- **Input:** none beyond the existing date and segment DOM values.
- **Current processing/output:** directly sets #18 to `2025-01-01`, #19 to `2025-03-31`, and #20 to `all`. It does not call Apply, invoke #101/#102, update the URL or change chart/KPI content.
- **Expected behavior:** no approved reset/default-period policy exists. Keep these as current hard-coded prototype defaults; do not substitute current date or a rolling window inferred from API DD proposals.

### EV-06 — Refresh query

- **Trigger / type:** #31 button `click`.
- **Current processing:** save current button text; set text to “Đang đồng bộ máy chủ...”; add `opacity-75` and `pointer-events-none`; after 900 ms restore text and classes.
- **API/side effect:** none. No polling, query invalidation, server synchronization, timeout or error is performed.
- **Output/exceptions:** button looks temporarily busy and then returns to default even if no data exists. Do not describe the timer as report freshness or success.

### EV-07 — Export to AD-25

- **Trigger / type:** #17 anchor `click`.
- **Current input/output:** browser follows `/admin/reports/export`; current values in #18–#20 are not serialized and no request is initiated by this element.
- **Expected handoff:** inventory links AD-24 to AD-25 and says preserve filter URL for export. No approved query serialization or state-transfer mechanism is present. API #103 catalog accepts optional `filters?:string`, `format?:string`, but its row says HTTP 202 `ApiEnvelope<Report>` while Operation tracking says it returns `Operation` and should be polled via `/api/v1/operations/{operation_id}`. This is an AD-25/API contract blocker, not an AD-24 runtime behavior.
- **Output/errors:** no success or export status appears in current AD-24. Do not claim #103 was called, a job was accepted, or a file is ready.

### EV-08 — Shell and footer navigation

- **Trigger / type:** #2–#6, #8, #10, #40–#42 anchors/buttons.
- **Current processing:** nav/footer anchors use `href="#"`; notification button has no listener; breadcrumb spans are static. No destination/API/state update is defined.
- **Output/security:** labels and role badges remain visible static copy. They do not authenticate Admin, fetch profile, prove system health or enforce RBAC.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
