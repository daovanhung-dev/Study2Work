# ST-26 Plan — Thông báo học viên

## 1. Scope and outcome

- Screen ID: `ST-26` only for this session.
- Screen name: Thông báo học viên (Page); proposed route `/student/notifications`; actor `Student`; source: [`list_screen.md`](../../../list_screen.md); AC-20.
- Expected API sequence: GET #43 to load the current Student notification page; PATCH #44 when one notification is marked read/opened; PATCH #45 for the mark-all action; then GET #43 to refresh the visible list/read state. Exact mutation/navigation ordering remains subject to the AC and API DD gaps described below.
- Screen outputs/links declared in inventory: ST-09, ST-17 and ST-25. Screenshot sample CTAs also name ST-19, ST-25, ST-11, ST-22 and an external Google Meet destination; none is a trusted route contract by itself.
- Preserve `screen.png` and `code.html`. Annotate the populated screenshot because it is the only source showing the loaded layout; document the static HTML empty-state fallback separately. Do not render or substitute the HTML for the screenshot.
- Expected completion state may be `DD BLOCKED` and `IMPLEMENTATION BLOCKED`; do not call it `DD READY` or `RUNTIME VERIFIED` while contracts/source are unresolved.

## 2. Source inventory and expected/current behavior

### Expected behavior

- AC-20: a signed-in Student opens the notification center; the backend reads recipient notifications and the UI shows the unread badge/list. The Student can mark one or all read; AC-20 names `NotificationRecipient.read_at` and requires the UI read state to synchronize.
- Inventory filter inputs: #43 supports only `unread_only?:boolean` and `page?:int32`. It does not declare the screenshot's assignment, mentor, or discussion category filters.
- #43: `GET /api/v1/users/me/notifications`, Student Bearer, response `ApiEnvelope<Page<Notification>>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/500.
- #44: `PATCH /api/v1/notifications/{notification_id}/read`, Student Bearer, path `notification_id:int64!`, no catalog body/query; response `ApiEnvelope<Page<Notification>>`; 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/404/422/500.
- #45: `PATCH /api/v1/notifications/read-all`, Student Bearer, catalog `body{}`; response `ApiEnvelope<Page<Notification>>`; 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/422/500. Whether `{}` is mandatory and what Page contains remain open.
- API #43/#44/#45 DDs are `Draft — Needs Confirmation`, with 7/7/8 open questions. Their derived recipient predicates, page size/order, singleton/bulk Page projections and legacy `is_read` mutations remain proposals.

### Current behavior and artifacts

- `screen.png`: populated notification center, 1081×1600, SHA-256 `e9078467e90538daffcdade2a8a80f9d2936aa99338c93071dd9eb417d93587d`. It displays six sample notifications, all/unread/category tabs, mark-all action, a notification-preference panel, weekly statistics, emergency-help panel, and footer.
- `code.html`: SHA-256 `3c040253758a64bf2d3287ff22fcf491325773476c657b5d2ab4a680e5965922`; static no-notification state with a Guest header, login/register links, no data/list/filter/mutation/API wiring, and a link to `/student/courses`. It imports remote Google fonts and a Tailwind CDN; that is prototype content and conflicts with the Study Web guide's no-remote-font target if implemented.
- Current Study Web editable source, package manifest, router and Student notification screen are absent; the ignored `dist` artifact contains only `/`. Route/auth/list behavior is not runtime-verified.
- Current Study Server registers Mentor notification routes #63/#64 and Admin notification routes #92–#96. Current source search found no Student #43/#44/#45 route, module, query or tests.
- The screenshot's label “Cập nhật tự động qua API #48” is not API evidence: current catalog #48 is Mentor lecture detail (`GET /api/v1/mentor/lectures/{lecture_id}`). No Student notification-preference contract was found.

## 3. Source trace and unresolved contracts

```text
Expected: route ST-26 → GET #43 → render Page<Notification>
                                   → PATCH #44 (one) or #45 (all)
                                   → GET #43 refresh → synchronize list/badge
                                   → navigate only through a validated deep-link contract
Current: no Study Web route/component; Student #43–#45 are not present in Study API source
Other current notification APIs: Mentor #63–#64, Admin #92–#96 (different actor and contracts)
```

- API reusable `Notification` requires `id`, `title`, `content`, `channels`, `status`, `created_at`; optional `read_at` and `scheduled_at`. It does not include `is_read`, category/type, unread count, sender, icon, or `action_url`.
- AC-20 names logical `NotificationRecipient` and `read_at`; neither is present in the legacy Study DDL. The checked-in legacy `notifications` candidate has BIGINT ID, nullable `user_id`/`sender_id`, title/content/type, `is_read BOOLEAN DEFAULT FALSE` (not declared `NOT NULL`), `created_at TIMESTAMP`, and `operation_id`. It has no `read_at`, recipient table, channels, status, scheduled_at, or action_url.
- Separate V1-PILOT DDL has UUID notification and learner IDs, `read_at`, `action_url`, `expires_at`, and payload. It does not match the catalog's int64 IDs/current numeric Student principal. Neither DDL is live-schema/deployment evidence.
- There is no approved source for `channels`, `NotificationStatus`, unread/read mapping, per-recipient broadcast state, or the screenshot's category. Do not equate `type`↔`channels`, `is_read`↔`status`, or derive `read_at` from a boolean.
- The safe-deep-link requirement has no corresponding field in the API `Notification` schema. The pilot `action_url` is not interchangeable with the numeric-ID legacy/catalog contract. Do not route by notification title/body, screenshot labels, or external URL sample.
- The screenshot contains a visible consistency conflict: first four cards have unread blue dots while each also says “Đã đọc”; the title/tab say five new while only four dots are visible. No unread badge/count rule may be inferred.
- Every notification API DD is Draft. #43 has questions on recipient/broadcast, missing fields, read_at, pagination/order/page validation, timezone, null/omission and error envelope. #44 has questions on recipient/read_at, notification fields, Page semantics, 404/concealment, idempotency and shared timestamps. #45 also leaves schema choice, broadcast, channels/status, bulk Page, empty-body validation, nullable `is_read`, timezone/retention, error envelope and idempotency unresolved.

## 4. Marker map plan

Markers are assigned in top-to-bottom, left-to-right visual order. Composite rows group static content that has no independent interaction; actionable controls are separate. Final IDs must be sequential, unique, within the source image, and map 1:1 to the element table in `ST-26.md`.

| # | Element ID | Screenshot element/group |
|---:|---|---|
| 1 | ST26-EL-01 | Study2Work brand/logo in global header |
| 2 | ST26-EL-02 | Global primary navigation |
| 3 | ST26-EL-03 | Global course/search field |
| 4 | ST26-EL-04 | Notification bell and red badge |
| 5 | ST26-EL-05 | Student profile/avatar/dropdown |
| 6 | ST26-EL-06 | Semester and enrollment-status strip |
| 7 | ST26-EL-07 | Home and Student/notification breadcrumb |
| 8 | ST26-EL-08 | Page title and “5 mới” sample badge |
| 9 | ST26-EL-09 | Supporting description |
| 10 | ST26-EL-10 | “Đánh dấu tất cả đã đọc” action, labeled API #45 in screenshot |
| 11 | ST26-EL-11 | “Tất cả thông báo” tab |
| 12 | ST26-EL-12 | “Chưa đọc” tab and sample count |
| 13 | ST26-EL-13 | “Bài tập & Chấm điểm” category tab |
| 14 | ST26-EL-14 | “Lịch hẹn Mentor” category tab |
| 15 | ST26-EL-15 | “Hoạt động diễn đàn” category tab |
| 16 | ST26-EL-16 | Notification-list region and vertical item collection |
| 17 | ST26-EL-17 | Sample notification 1: icon/category/time/title/body/read marker |
| 18 | ST26-EL-18 | Notification 1 CTA to ST-19, sample only |
| 19 | ST26-EL-19 | Sample notification 2: icon/category/time/title/body/read marker |
| 20 | ST26-EL-20 | Notification 2 CTA to ST-25, sample only |
| 21 | ST26-EL-21 | Sample notification 3: icon/category/time/title/body/read marker |
| 22 | ST26-EL-22 | Notification 3 Google Meet CTA, external target sample |
| 23 | ST26-EL-23 | Sample notification 4: icon/category/time/title/body/read marker |
| 24 | ST26-EL-24 | Notification 4 CTA to ST-11, sample only |
| 25 | ST26-EL-25 | Sample notification 5: icon/category/time/title/body/read marker |
| 26 | ST26-EL-26 | Notification 5 CTA to ST-22, sample only |
| 27 | ST26-EL-27 | Sample notification 6: icon/category/time/title/body/read marker |
| 28 | ST26-EL-28 | Notification-channel preferences panel heading/copy |
| 29 | ST26-EL-29 | Email-notification toggle |
| 30 | ST26-EL-30 | Web Push toggle |
| 31 | ST26-EL-31 | SMS Mentor-reminder toggle |
| 32 | ST26-EL-32 | “Cập nhật tự động qua API #48” status strip |
| 33 | ST26-EL-33 | Weekly-statistics heading and bar chart |
| 34 | ST26-EL-34 | Weekly-statistics legend and sample counts |
| 35 | ST26-EL-35 | Emergency-help card heading and description |
| 36 | ST26-EL-36 | Contact-coordinator CTA |
| 37 | ST26-EL-37 | Footer brand, description and certification badges |
| 38 | ST26-EL-38 | Footer program links |
| 39 | ST26-EL-39 | Footer community/support links |
| 40 | ST26-EL-40 | Footer office/contact details |
| 41 | ST26-EL-41 | Footer copyright and legal links |

## 5. Event plan

All events are expected design flows, not current runtime. Each event in `ST-26.md` must include trigger, precondition, input, ordered processing, API contract (or explicit no-API/blocked status), output and exceptions.

| Event ID | Trigger and planned coverage |
|---|---|
| ST26-EV-01 | Enter ST-26; Student route/access condition; call API #43 with only catalog query fields. |
| ST26-EV-02 | Parse/map successful #43 Page; describe unresolved Notification fields, unread count and read-state mapping. |
| ST26-EV-03 | #43 error/empty/malformed/network result; preserve only catalog 401/403/500 codes and record UI copy/retry gaps. |
| ST26-EV-04 | Select “Tất cả thông báo”; #43 unfiltered query/page reset semantics remain DERIVED or open. |
| ST26-EV-05 | Select “Chưa đọc”; #43 `unread_only=true`; count and response-state mapping remain blocked. |
| ST26-EV-06 | Select category tab; no category/type query exists in #43; document visual-only or contract-extension blocker. |
| ST26-EV-07 | Open/mark one notification; #44 path ID, catalog errors, then #43 refresh per inventory; ownership/404/read_at/response details remain Draft. |
| ST26-EV-08 | Navigate through a notification deep link; require trusted typed payload and allowlisted route mapping first; no raw URL/title/body routing. |
| ST26-EV-09 | Mark all read; #45 `body{}`; successful refresh #43; body requiredness, bulk Page, empty result and read-state update unresolved. |
| ST26-EV-10 | Toggle email/Push/SMS channel controls; no Student preference API/field; screenshot's API #48 label is contradicted by catalog. |
| ST26-EV-11 | View weekly chart/counters; static sample with no #43–#45 aggregate or event source. |
| ST26-EV-12 | Activate emergency-support CTA; destination/service is not defined by ST-26 contract. |
| ST26-EV-13 | Use shared header/nav/search/profile controls; route/search/menu semantics are not established by this screen's source. |
| ST26-EV-14 | Use footer navigation/legal/contact links; destinations are not runtime-wired or verified. |

## 6. State and navigation plan

- Inventory states: `unread`, `read`, `empty`, `marking`, `error`; document `loading`, `ready`, auth-denied and mutation-pending transitions only as expected UI states where supported, not as current implementation.
- Entry → load → empty/ready/error; one-item mutation and bulk mutation → pending → success then #43 refresh, or error. No optimistic update before a contract-approved response; reconcile with AC-20 reload and API DD Page gaps.
- All/unread/category selection may require query changes, but only `unread_only` and `page` exist in #43 catalog. Category filter semantics, page size/order, count and URL persistence are open.
- Deep links to ST-09/ST-17/ST-25 and screenshot targets ST-19/ST-11/ST-22 or external Meet remain blocked until a source-backed action payload, safe allowlist, required route parameters and mark-before-navigation policy are approved.
- Auth/403/401 behavior must follow an approved Student shell/session policy. Current Study Web has no guard or route implementation.

## 7. Authoring and annotation steps

1. Preserve original source asset hashes; use the populated PNG as annotation base.
2. Create a marker JSON with 41 sequential IDs; `x/y` mark source-image positions, while `anchor_x/anchor_y` and badge positions use annotated-canvas coordinates. Create a transparent SVG marker layer with numbered callouts outside the original screenshot pixels.
3. Composite source image at offset `(112,24)` on a planned `1305×1648` canvas. Compare the embedded screenshot crop to `screen.png` and require pixel difference `AE=0`; visually inspect number legibility and connector placement.
4. Author `ST-26.md` A–F with 41 element rows, 14 ordered event details, route/AC/API trace, state/navigation matrix, acceptance checklist, and explicit `EXPECTED`/`CURRENT`/`DERIVED`/`SOURCE_REQUIRED` distinctions.
5. Update only the ST-26 tracker row and append an ST-26 checkpoint with fresh counts from `list_screen.md` and screen folders. Preserve other screen pointers.
6. Update this worklog with final file list, static verification, blockers and next Student screen pointer. No tests/runtime checks unless requested; context validator is not required unless a context page/manifest changes.

## 8. Verification checklist

- [x] Original `screen.png`/`code.html` SHA-256 values unchanged.
- [x] Annotated canvas is 1305×1648 and its source crop is pixel-identical (`AE=0`); callouts do not cover original content.
- [x] Marker JSON is valid; 41 marker IDs are ordered and unique; `x/y` are inside the source, leader anchors equal the source offset in the annotated canvas, badges sit in gutters, SVG parses, and each marker maps to exactly one DD row.
- [x] DD includes sections A–F and 14 sequential events with all required event fields.
- [x] API #43–#45 methods/endpoints/inputs/responses/status/business codes match catalog; Draft/open-question limitations (7/7/8) are visible.
- [x] All 23 relative Markdown links in ST-26 DD/plan resolve.
- [x] Tracker row/status, 83 screen IDs, 44 core artifact sets, and next pointer ME-10 reflect current inventory.
- [x] `git diff --check` and authored-file whitespace scan pass; tests/runtime were not run or claimed.

## 9. Results

Static verification passed: source hashes unchanged; annotated image 1305×1648 with source crop `AE=0`; 41 sequential markers map 1:1 to 41 DD elements and remain outside the source crop; 14 sequential events contain all required fields; sections A–F, API #43–#45 contract codes, Q counts, and all 23 local links checked. Tracker reflects 83 inventory IDs, 44/83 core artifact sets (39 incomplete), and next pointer ME-10. `git diff --check` and authored-file whitespace scan pass. Tests and runtime verification were not run. Status remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until the listed notification schema, read-state, response, filter, preference and deep-link contracts are resolved.
