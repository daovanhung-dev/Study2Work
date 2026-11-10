# ST-26 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-26-EV-001` | `ST26-EV-01` / ST26-EV-01 — Mở màn hình và tải trang thông báo | See source event detail below |
| `ST-26-EV-002` | `ST26-EV-02` / ST26-EV-02 — Ánh xạ response #43 và tính hiển thị list/badge | See source event detail below |
| `ST-26-EV-003` | `ST26-EV-03` / ST26-EV-03 — Empty, error hoặc lỗi tải notification | See source event detail below |
| `ST-26-EV-004` | `ST26-EV-04` / ST26-EV-04 — Chọn “Tất cả thông báo” | See source event detail below |
| `ST-26-EV-005` | `ST26-EV-05` / ST26-EV-05 — Chọn “Chưa đọc” | See source event detail below |
| `ST-26-EV-006` | `ST26-EV-06` / ST26-EV-06 — Chọn tab loại thông báo | See source event detail below |
| `ST-26-EV-007` | `ST26-EV-07` / ST26-EV-07 — Mở/đánh dấu một notification đã đọc | See source event detail below |
| `ST-26-EV-008` | `ST26-EV-08` / ST26-EV-08 — Theo deep link của notification | See source event detail below |
| `ST-26-EV-009` | `ST26-EV-09` / ST26-EV-09 — Đánh dấu tất cả đã đọc | See source event detail below |
| `ST-26-EV-010` | `ST26-EV-10` / ST26-EV-10 — Thay đổi notification channel preferences | See source event detail below |
| `ST-26-EV-011` | `ST26-EV-11` / ST26-EV-11 — Hiển thị thống kê tuần | See source event detail below |
| `ST-26-EV-012` | `ST26-EV-12` / ST26-EV-12 — Liên hệ điều phối viên | See source event detail below |
| `ST-26-EV-013` | `ST26-EV-13` / ST26-EV-13 — Điều hướng header, breadcrumb, search và profile | See source event detail below |
| `ST-26-EV-014` | `ST26-EV-14` / ST26-EV-14 — Footer navigation, policy và contact | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

Events below describe `EXPECTED` design handling only. No Student #43–#45 or Study Web UI flow is wired in current source. Keep `DERIVED`, `SOURCE_REQUIRED` and `NOT_FOUND` statuses visible.

### ST26-EV-01 — Mở màn hình và tải trang thông báo

- **Element / loại:** Route lifecycle; ST26-EL-16; `Load`.
- **Điều kiện:** Expected Student signed in per AC-20; route/auth guard is not present in current Study Web.
- **Input:** Proposed `/student/notifications`; optional query `unread_only:boolean`, `page:int32`; Bearer JWT from Student session if session wiring is implemented. Do not accept user ID from URL/query/body.
- **Xử lý:** (1) Resolve proposed route; (2) check Student session/role through approved shell; (3) normalize only the declared query fields; (4) request API #43; (5) do not add category/sort/size or derive unread state from sample content.
- **API:** `GET /api/v1/users/me/notifications`; Student Bearer; no body; 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. API DD page defaults/order are `DERIVED`.
- **Output:** Expected `loading` then a Page result; current route/request does not exist.
- **Ngoại lệ:** Invalid `page`/boolean query behavior is not declared as 422 for #43; 401/403 UX, network timeout, retry, malformed response and empty-page metadata remain unresolved.

### ST26-EV-02 — Ánh xạ response #43 và tính hiển thị list/badge

- **Element / loại:** API response mapping for ST26-EL-08, ST26-EL-12, ST26-EL-16…27; `Load result`.
- **Điều kiện:** Expected HTTP 200 and parseable `ApiEnvelope<Page<Notification>>`.
- **Input:** Schema fields `id`, `title`, `content`, `channels`, `status`, optional `read_at`/`scheduled_at`, `created_at`; Page metadata.
- **Xử lý:** (1) Validate envelope/business code; (2) use only approved Page fields; (3) keep `channels/status/read_at/scheduled_at` unresolved until source/schema decisions; (4) do not infer `is_read`, category, sender, icon, badge count or CTA URL from another field; (5) do not map screenshot names/counts/times into API data.
- **API:** #43 GET result above; API DD proposes page=1/size=20/newest-first but no approval. `Page.total` for unread-only count is not an approved badge rule.
- **Output:** Current contract cannot fully construct screenshot cards or unread/read display. Loaded data should remain blocked until required fields and read/count mapping are confirmed.
- **Ngoại lệ:** Missing required Notification field, malformed Page and null/omission timestamp behavior lack approved client handling; do not fabricate values.

### ST26-EV-03 — Empty, error hoặc lỗi tải notification

- **Element / loại:** ST26-EL-16 list region; `Load state`.
- **Điều kiện:** #43 returns an empty Page, catalog error, transport failure or invalid response.
- **Input:** HTTP/business code; `items`/pagination if valid; transport/parser error from client.
- **Xử lý:** (1) Preserve catalog 401/403/500 distinctions; (2) show a distinct empty result only when response validly says no items; (3) do not convert network/500 to empty or 404; (4) preserve trace ID if available; (5) retry CTA/copy/session redirect are not specified by ST-26 source.
- **API:** #43 catalogs 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- **Output:** Inventory includes `empty/error`; screenshot shows populated state only. Current UI has no state renderer.
- **Ngoại lệ:** Network offline, timeout, error-envelope mismatch (`data:null` guideline vs current shared helper `{}`), malformed JSON and session-expiry recovery require a client/API decision; no extra business code is added.

### ST26-EV-04 — Chọn “Tất cả thông báo”

- **Element / loại:** ST26-EL-11 tab; `Click`.
- **Điều kiện:** Tab is available and user activates it.
- **Input:** Current filter/page UI state; API #43 optional `unread_only`, `page`.
- **Xử lý:** (1) Treat “all” as an intended unfiltered view; (2) exact encoding as omitted vs `false`, page reset, URL/cache synchronization are not approved; (3) after decision, fetch #43 with only catalog parameters; (4) show response only after a valid result.
- **API:** #43 GET; no mutation. Do not send a category/type query.
- **Output:** Expected all-notification list when contract and response mapping are approved; current tab is static in source screenshot.
- **Ngoại lệ:** Request errors follow EV-03; unsupported/stale filter state is not a runtime behavior today.

### ST26-EV-05 — Chọn “Chưa đọc”

- **Element / loại:** ST26-EL-12 tab; `Click`.
- **Điều kiện:** User activates unread filter.
- **Input:** Expected `unread_only=true`; page selection if approved; no user identity from client data.
- **Xử lý:** (1) Request #43 with `unread_only=true`; (2) do not encode the filter as a category or status; (3) render rows only if read-state semantics are resolved; (4) do not infer global unread badge from page item count; (5) refresh list after accepted mutation per inventory.
- **API:** `GET /api/v1/users/me/notifications?unread_only=true` (query order illustrative); Student Bearer; 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. No `size` is declared.
- **Output:** Expected filtered Page; screenshot's `(5)` is unverified sample. API Notification lacks `is_read`; API DD still needs to settle filter storage/response mapping.
- **Ngoại lệ:** Invalid boolean/page mapping and badge count semantics are open; preserve #43 catalog errors.

### ST26-EV-06 — Chọn tab loại thông báo

- **Element / loại:** ST26-EL-13, ST26-EL-14, ST26-EL-15; `Click`.
- **Điều kiện:** User activates grading, mentor or forum category tab.
- **Input:** Screenshot labels only; API #43 accepts `unread_only` and `page`, not category/type.
- **Xử lý:** (1) Recognize the visible tab; (2) do not invent wire enum, query parameter, filter list, or mapping from legacy `type`; (3) treat active-filter behavior as blocked until catalog/API/schema approves it.
- **API:** None currently defined for category filtering. API #43 must not receive an undocumented parameter.
- **Output:** Current source does not wire these tabs; target behavior cannot be selected from screenshot labels alone.
- **Ngoại lệ:** Unsupported filter cannot be reported as API success or silently mapped to a broader query.

### ST26-EV-07 — Mở/đánh dấu một notification đã đọc

- **Element / loại:** ST26-EL-17, ST26-EL-19, ST26-EL-21, ST26-EL-23, ST26-EL-25, ST26-EL-27 card rows; expected `Open`/`Mark read`.
- **Điều kiện:** Student activates one notification whose identity and recipient relation have been supplied by an approved #43 response. Screenshot labels/dots are inconsistent and cannot be used to decide unread.
- **Input:** `notification_id:int64!` from a trusted API item; Student Bearer; no catalog body/query/header.
- **Xử lý:** (1) Confirm row identity/state using approved contract; (2) avoid starting a duplicate in-flight mutation; (3) call #44; (4) on 200, follow expected GET #43 refresh; (5) do not update local read state from sample dot/“Đã đọc”; (6) navigation timing is separate EV-08 and is not decided here.
- **API:** `PATCH /api/v1/notifications/{notification_id}/read`; 200 `DESIGN_RESOURCE_UPDATED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Direct-recipient predicate, 404 concealment, `is_read` vs `read_at`, repeat behavior and singleton Page are Draft/DERIVED.
- **Output:** Expected read state/list sync only after approved response + #43 refresh; no current handler exists.
- **Ngoại lệ:** #44 may have committed even if refresh fails; do not blindly repeat. 404 may conceal non-ownership by proposal only; exact feedback/retry requires approval.

### ST26-EV-08 — Theo deep link của notification

- **Element / loại:** ST26-EL-18, ST26-EL-20, ST26-EL-22, ST26-EL-24, ST26-EL-26 and clickable card content; `Navigate`/external link.
- **Điều kiện:** Notification has a typed, trusted action payload and destination rule approved by API/security/Product. That prerequisite is not met in current catalog.
- **Input:** Current Notification schema contains no `action_url`, route type, destination ID or payload. Screenshot CTA labels/Google Meet URL are illustrative only; pilot `action_url` belongs to UUID schema alternative.
- **Xử lý:** (1) Never derive a destination from title/body; (2) do not open raw server URLs or pass arbitrary route names/IDs; (3) validate typed target, required ID and allowlist only after contract is approved; (4) mark-read vs navigate ordering needs approval; (5) route to ST-19/ST-25/ST-11/ST-22 or external Meet only if a corresponding payload contract exists.
- **API:** No deep-link API/field is present in #43; #44 only accepts notification ID. No endpoint is inferred.
- **Output:** Current safe destination is unresolved; navigation is blocked rather than opening sample destinations.
- **Ngoại lệ:** Missing, malformed, external, unrecognized, stale or unauthorized action target needs a defined safe fallback; do not route on invalid data.

### ST26-EV-09 — Đánh dấu tất cả đã đọc

- **Element / loại:** ST26-EL-10; `Click`/`Submit`.
- **Điều kiện:** Student activates mark-all after current unread set has been loaded; pending guard behavior is proposed, not implemented.
- **Input:** Student Bearer; catalog `body{}`; no path/query. API DD proposes `{}` but body requiredness/unknown-key rule is unresolved.
- **Xử lý:** (1) Do not run on page load; user action is required; (2) use only approved request body semantics; (3) submit #45 once per active UI action; (4) parse success; (5) refetch #43 per inventory; (6) derive badge/list from approved refreshed response, not local decrement or returned sample count.
- **API:** `PATCH /api/v1/notifications/read-all`; 200 `DESIGN_RESOURCE_UPDATED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Candidate atomic bulk `is_read=TRUE` and all-changed rows Page are Draft/DERIVED.
- **Output:** Expected unread list/badge synchronization after refresh; present screenshot count “5” is not authoritative. No current route/mutation is wired.
- **Ngoại lệ:** No unread rows may be success/no-op under a DD proposal but has no approved response projection; if mutation outcome is uncertain, do not blindly resubmit; body validation and retry policy are open.

### ST26-EV-10 — Thay đổi notification channel preferences

- **Element / loại:** ST26-EL-29…32; toggle/change.
- **Điều kiện:** User activates Email, Web Push or SMS control.
- **Input:** Screenshot checkbox state and copy only. No preference endpoint/request/default/consent/device-token field is defined for ST-26.
- **Xử lý:** (1) Record visual affordance; (2) do not persist or send a mutation; (3) do not call API #48 because current catalog #48 is Mentor lecture detail; (4) wait for an approved preference contract.
- **API:** None in ST-26 catalog. #43–#45 concern list/read state only.
- **Output:** No verified settings update or automatic save. Green “updated via API #48” message is design-only and contradicted by the current API catalog.
- **Ngoại lệ:** Permission denied/browser Push permission/SMS consent/update failure states are not defined; do not fabricate toggles as working preferences.

### ST26-EV-11 — Hiển thị thống kê tuần

- **Element / loại:** ST26-EL-33…34; static data display.
- **Điều kiện:** Screen is rendered.
- **Input:** Screenshot literals: weekly total 42 and category counts 14/8/16/4.
- **Xử lý:** (1) Treat as visual sample; (2) no aggregation from #43 items because page can be partial and fields/categories are absent; (3) do not call unrelated API.
- **API:** None in #43–#45.
- **Output:** No current data source or live chart behavior is verified.
- **Ngoại lệ:** Missing/partial aggregate semantics, time zone and date range have no contract; do not display sample metrics as user facts.

### ST26-EV-12 — Liên hệ điều phối viên

- **Element / loại:** ST26-EL-36; external/contact action.
- **Điều kiện:** User activates emergency-help CTA.
- **Input:** Screenshot label and external-link icon; no verified URL, phone, service, severity rule or contact channel.
- **Xử lý:** (1) Do not infer a URL from adjacent contact text; (2) require owner-approved destination and safety policy before navigation/call.
- **API:** None in ST-26 contract.
- **Output:** Current destination/action is not defined; control is visual-only in the source evidence.
- **Ngoại lệ:** No destination, invalid destination, unavailable contact or urgent-service fallback policy is supplied.

### ST26-EV-13 — Điều hướng header, breadcrumb, search và profile

- **Element / loại:** ST26-EL-01…07; `Click`/menu/search.
- **Điều kiện:** User activates a header/breadcrumb control.
- **Input:** Screenshot labels and Student profile sample. HTML fallback uses generic `#` for its Guest header; it is not routing evidence for this populated screen.
- **Xử lý:** (1) Identify the activated control; (2) do not assume route, search endpoint, menu/logout behavior, or history preservation; (3) use only routes independently approved in the Study Web route inventory after implementation exists.
- **API:** No API #43–#45 is attached to these controls. Header search is outside the screen contract.
- **Output:** Current links/handlers are absent or unverified.
- **Ngoại lệ:** Broken/unknown destinations and session transitions need shell-level definitions; no navigation result can be asserted.

### ST26-EV-14 — Footer navigation, policy và contact

- **Element / loại:** ST26-EL-38, ST26-EL-39, ST26-EL-41; link click.
- **Điều kiện:** User activates a footer link.
- **Input:** Screenshot labels, links and contact literals; no verified destinations.
- **Xử lý:** Preserve informational copy as visual source only; do not invent route or support API from link labels.
- **API:** None in ST-26.
- **Output:** Footer links are not runtime-wired in current Study Web.
- **Ngoại lệ:** Unknown route/contact must be resolved before implementation; HTML `#` anchors are prototype placeholders.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
