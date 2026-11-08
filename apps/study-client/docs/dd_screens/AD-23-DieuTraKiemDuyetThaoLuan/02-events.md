# AD-23 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-23-EV-001` | `Source heading` / EV-01 — Load moderation detail | See source event detail below |
| `AD-23-EV-002` | `Source heading` / EV-02 — Return from header | See source event detail below |
| `AD-23-EV-003` | `Source heading` / EV-03 — Return from empty thread | See source event detail below |
| `AD-23-EV-004` | `Source heading` / EV-04 — Select moderation action | See source event detail below |
| `AD-23-EV-005` | `Source heading` / EV-05 — Enter action reason | See source event detail below |
| `AD-23-EV-006` | `Source heading` / EV-06 — Apply moderation decision | See source event detail below |
| `AD-23-EV-007` | `Source heading` / EV-07 — Optional delete after moderation | See source event detail below |
| `AD-23-EV-008` | `Source heading` / EV-08 — Cancel / return | See source event detail below |
| `AD-23-EV-009` | `Source heading` / EV-09 — Shell, notification and footer links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Load moderation detail

- **Element / type:** page entry and #17–#20 summary; future `Load` event. No load handler is present in HTML.
- **Preconditions:** expected Admin session; Discussion ID received from AD-22; path must satisfy catalog `int64!`. The source of the ID, whether a reported child reply can be passed, and report association are unresolved.
- **Input:** candidate route parameter `discussionId` / API path `discussion_id:int64!`. No query or body is declared by catalog #98.
- **Expected API contract:** `GET /api/v1/admin/discussions/{discussion_id}`, Bearer JWT, role Admin. Direct response `ApiEnvelope<Page<Discussion>>`; success `200 DESIGN_RESOURCE_RETRIEVED`; errors `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `404 DESIGN_RESOURCE_NOT_FOUND`, `500 DESIGN_INTERNAL_ERROR`.
- **Current local source:** role `ADMIN` is checked before ID parsing/DB; invalid/non-positive/overflow ID returns 404; missing Discussion returns 404; current projection reads Discussion/author and direct child comments, sorts comments ascending by timestamp then ID, maps a content-derived title and returns a singleton page. Report data is not queried. Query/projection failure returns safe 500 and rolls back; success is read-only and does not commit.
- **Processing and output:** current HTML performs no validation/request/mapping and stays on placeholders. A future UI cannot satisfy AC's report inspection from the current #98 projection. Do not populate report-specific fields from #97 or infer them from Discussion content.
- **Exceptions/state:** catalog describes the HTTP/business codes above. Local invalid ID is also 404 rather than a separately catalogued validation result. No frontend handling, timeout/retry/cache or session redirect behavior is implemented or approved. Do not invent one.

### EV-02 — Return from header

- **Element / type:** #13, click on anchor/button.
- **Preconditions/input:** none in current static prototype; expected destination AD-22.
- **Processing:** browser follows `href="#ad-22"`; no router navigation, #97 call, history-state transfer or filter/page restoration exists.
- **Output/errors:** current output is fragment navigation only. Future return behavior should use the approved AD-22 route and handoff contract; it is not implemented here.

### EV-03 — Return from empty thread

- **Element / type:** #29, click on anchor/button.
- **Preconditions/input:** none; link is always shown with empty state.
- **Processing/output:** follows `#ad-22`. No Discussion ID or report context is passed; no #97 refresh is triggered. Filter/page restoration remains unspecified.

### EV-04 — Select moderation action

- **Element / type:** #33–#36, radio `change`.
- **Preconditions:** controls are disabled in the current prototype; therefore the event cannot be performed.
- **Input:** HTML radios share `name="moderation_action"`; no `value` attribute is defined. No current selected/default action.
- **Expected business choices:** AC-37 names hide, lock and warn at a high level. It does not define exact request tokens or state transitions. #99 catalog accepts `action:string!` but has no enum. Permanent deletion is a separate optional #100 flow according to AC; the prototype incorrectly shows it as a #99-group radio.
- **Processing/output:** no local state changes and no API call. Keep options locked until action tokens, target scope, eligibility and authorization are approved. Do not derive `hide|lock|warn` values from examples in Draft documentation.

### EV-05 — Enter action reason

- **Element / type:** #38, text input `input`/`change`.
- **Preconditions:** disabled in prototype; no input event currently fires.
- **Input:** future `reason:string!` per #99 catalog. Catalog does not specify min/max length, trimming, empty-string acceptance, prohibited content, localization or relation to the reason on a report.
- **Processing/output:** no current value or validation. AC expects an audit trail, but no source-backed audit persistence/atomicity exists. Do not claim input is persisted to audit or set validation limits without an approved contract.

### EV-06 — Apply moderation decision

- **Element / type:** #40, disabled button; future `Submit`/click.
- **Preconditions:** current disabled button prevents submission. Future prerequisites (valid ID, selected approved action, valid reason, permission, current/stale-state handling) are not fully defined.
- **Input / API:** catalog #99 is `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`; Bearer JWT, role Admin; path `discussion_id:int64!`; required body `{action:string!, reason:string!}`; direct response `ApiEnvelope<Page<Discussion>>`.
- **Expected processing if contract is finalized:** send only the approved values once; inspect HTTP/business code; on 200 `DESIGN_RESOURCE_UPDATED`, use the response only according to finalized mapping; then update screen/return path only after AC and UI behavior are confirmed. No local #99 endpoint exists today, so this sequence is conditional documentation, not executable current behavior.
- **Catalog errors:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`.
- **Exceptions and data integrity:** retry, idempotency, duplicate submission, stale version/conflict, audit atomicity and response refresh policy are not specified. Catalog has no 409. Do not report success, create audit evidence or optimistically update state in the current UI.

### EV-07 — Optional delete after moderation

- **Element / type:** AC-37 conditional deletion path; no correctly mapped delete element or confirmation flow is present. #36 is a conflicting placeholder radio, not an approved trigger.
- **Preconditions:** AC says delete is optional after review; eligibility and whether a prior #99 action is mandatory are unresolved.
- **API contract:** #100 `DELETE /api/v1/admin/discussions/{discussion_id}`; Bearer JWT, role Admin; required path `discussion_id:int64!`; no body/query declared; direct response `ApiEnvelope<DeleteResult>`; success `200 DESIGN_RESOURCE_DELETED`; errors `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `404 DESIGN_RESOURCE_NOT_FOUND`, `422 DESIGN_VALIDATION_ERROR`, `500 DESIGN_INTERNAL_ERROR`.
- **Expected AC behavior:** conditional soft delete and preservation of audit trail. API DD notes `DeleteResult` fields `id`, `status:"deleted"`, `deleted_at`, but physical mapping and timestamp source are unresolved; catalog response type alone does not approve all persistence details.
- **Current behavior / output:** no local #100 route/test and no delete request. Prototype copy claims permanent/full deletion, which conflicts with AC. Do not implement hard delete, submit delete through #99, invent a confirmation modal, or assume repeat/retention semantics.

### EV-08 — Cancel / return

- **Element / type:** #41, click on anchor/button.
- **Preconditions/input:** current page has no editable decision state because controls are disabled.
- **Processing/output:** follows `#ad-22`; no discard dialog, API call or saved-draft state. If future editing becomes possible, unsaved-change behavior needs a separate approved requirement.

### EV-09 — Shell, notification and footer links

- **Element / type:** #1–#6, #8, #10, #43–#45, click/anchor as applicable.
- **Preconditions/input:** none in prototype.
- **Processing/output:** anchors use `href="#"`; notification bell has no event handler. No route targets, data requests or navigation state are wired. The shell does not establish authentication, identity or RBAC despite its labels.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
