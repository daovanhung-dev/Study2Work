---
task_id: "2026-10-27-design-study-screen-sh04"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-04 -> Study API #02 verification-email dispatch; SH-03 supplies user_id/email; SH-02 is linked destination"]
status: "PARTIAL"
---

# Worklog: Thiết kế Study Web screen SH-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh01.md`
    - carry_forward: Giữ Study ocean palette/brand và 4px rhythm; design resource không chứng minh UI runtime; ảnh desktop của SH-01 có 41 markers đã visual review.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh02.md`
    - carry_forward: Auth screens cần artwork riêng nhưng thống nhất palette; token/session/role contract chưa resolve; ghi rõ khi ChatGPT website không khả dụng và không nhận claim runtime từ local renderer.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh03.md`
    - carry_forward: SH-03 đã mô tả 201 → SH-04 theo expected journey, nhưng API #01 hiện chỉ log pending; SH-04/API #02 mặc định là stub accepted, không delivery/verify. Giữ no-email-delivery claim.
- shortage: `none` (135 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Thiết kế đúng một screen theo lượt: SH-04 “Handoff xác thực email”, page `/register/verification`, Guest, AC-01, API #02. Lập plan trước, ảnh clean/annotated có marker cho từng element, bảng mô tả chi tiết UI/behavior/responsive, và ZIP trong `apps/study-client/docs/dd_screens/resource/SH-04/`.
- Canonical target: `.agents/web-study/design.md`, SH-04 inventory row và flow F01 trong `apps/study-client/docs/dd_screens/list_screen.md`; Study API #02 catalog/DD/current source.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-client/` hiện chỉ chứa screen inventory; chưa có Study Web runtime/router/client. `.agents/web-work/study/*` theo context map không tồn tại trong checkout; `.agents/web-study/design.md` là canonical design target.
- API #02: Public `POST /api/v1/auth/verify-email/send`; request JSON `user_id:int`, `email:string`; không dùng Authorization/DB/ownership check theo current route. View validate request, gọi injectable `VerificationEmailProvider`, success HTTP 202 `DESIGN_OPERATION_ACCEPTED` với `{status:"accepted"}` và optional `reason`; provider exception → 500 safe message. Default provider là stub: nhận request nhưng không gửi email, không tạo token/link.
- Connected flow: Inventory F01 yêu cầu SH-03 nhận #01 `data.id`/`data.email` rồi gọi #02 trên SH-04. Current API #01 chỉ log pending và không gọi #02. Không có confirm OTP/link endpoint trong catalog.
- Tests: Đã đọc test source #02; không chạy trong task screen/docs. Test fixtures/fake provider không chứng minh email delivery/provider triển khai/live runtime.

## SOURCE_TRACE

```text
Expected inventory: SH-03 #01 201 data.id/email -> SH-04 #02 POST user_id/email -> HTTP 202 accepted -> SH-02 link
Current source: Study Web absent; direct public #02 -> validate -> injected provider.dispatch -> default Stub returns accepted -> 202; no email/token/link/DB mutation. SH-03 #01 currently does not call #02.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web runtime | Scoped client tree currently has inventory only. | `SOURCE_REQUIRED` | Mark output as `DESIGN_TARGET / NOT_IMPLEMENTED`. |
| Email dispatch | API #02 `202 accepted`; default stub does not send a message or generate verification token/link. | `DISCREPANCY / STUB` | Never say email was sent, delivered, or verified. Explain acceptance vs delivery honestly. |
| SH-03 → #02 wiring | F01 expects #02 after #01, but current #01 only logs `verification_dispatch_pending`. | `DISCREPANCY / UNWIRED` | SH-04 request is expected choreography, not a proven automatic runtime transition. |
| Confirmation mechanism | API catalog has no OTP/link confirmation endpoint; #02 only dispatches. | `NOT_FOUND / BLOCK` | Do not design OTP, code input, confirm link or verified-success state. |
| Retry/resend policy | DD remains Draft; no source-backed rate limit, retry worker, idempotency or delivery status. | `SOURCE_REQUIRED / OPEN_DECISION` | Avoid repeated POST/resend UX or delivery promise until approved. |
| Identity handoff | Expected #02 body needs `user_id` and `email`; Study Web storage/route transport is absent. | `SOURCE_REQUIRED / OPEN_DECISION` | Do not put PII in URL or invent persistence/transport. |

## CHANGES

- Files changed: `.agents/worklog/2026-10-27/design-study-screen-sh04.md` and `apps/study-client/docs/dd_screens/resource/SH-04/` (`PLAN.md`, `SCREEN.md`, two screen PNG/SVGs, transparent artwork PNG/SVG, `build.py`, and ZIP).
- CONTEXT_UPDATES: None planned; no Study Web runtime or API contract will be changed.
- Context pages changed: None.
- Assumptions: Main visual state represents #02 HTTP 202 with `data.status=accepted` while explicitly separating acceptance from email delivery; no sample email/user, OTP, link, resend or verification-success claim. Direct/missing handoff reuses CTA #17 for SH-03 only in `INVALID_HANDOFF`.
- Design-intelligence review: Read the `design` skill and used `ui-ux-pro-max` search for async request acceptance/delivery-unknown copy. Applied one polite status announcement and separated accepted request from unknown delivery; retained Study guide's preference for restrained surfaces and calm motion.
- User visual feedback / revision 2: The first handoff felt too flat and generic. Updated the plan before rebuilding: introduced one ocean-deep editorial panel with white/soft copy, redrew the request-folio vector with a larger readable silhouette and restrained orbit detail, balanced the CTA vertically, and changed the button to a flat Study primary fill. Preserved the 17-element map and all API/state boundaries.
- Authoring provenance update: Retried this turn with `getState()`, Chrome, and the in-app browser; no browser is exposed and both tab creation attempts returned `Browser is not available`. No prompt was sent to the ChatGPT website. Revision 2 is locally authored as editable SVG and rendered with installed Chrome headless; do not attribute the design to the ChatGPT website.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; existing SH-01/02/03 untracked resources/worklogs preserved. | VERIFIED |
| Worklog selector + selected files | 3 exact-type docs worklogs selected/read, no shortage (135 available). | VERIFIED |
| `.agents/web-study/design.md`, full `list_screen.md`, SH-04 row, F01, API catalog #02 | Canonical visual rules, route/actor/states/API/screen links and target-vs-current disclosure reviewed. | VERIFIED_STATIC_ONLY |
| `.agents/server-study/AGENTS.md`, `INDEX.md`, `modules/README.md`, API #02 route/model/validator/view/provider/DD/open questions/test source | Confirmed public/no-DB dispatch, strict raw integer + normalized email, 202 `accepted`, optional provider reason, default stub no delivery/token/link, 422/500 and absence of confirm endpoint. Test source read only. | VERIFIED_STATIC_ONLY |
| Context manifest skill/workflow registry | `createDD-markdown` is wired to Web/API DD but explicitly excludes Web UI-only DD; no UI DD skill canonical. | VERIFIED_STATIC_ONLY |
| `ui-ux-pro-max` search `async request accepted status delivery unknown email confirmation screen messaging --domain ux -n 5` | Guidance supports meaningful async status announcements and explicit action feedback; applied with no focus steal. | VERIFIED_STATIC_ONLY |
| `.agents/project/INDEX.md`, `architecture.md`, `dependencies.md`, `contracts.md` | Confirmed Study Web→Study Server contract boundary and Study OpenAPI placeholder; no cross-app assumption added. | VERIFIED_STATIC_ONLY |
| `apps/study-client/docs/dd_screens/resource/SH-04/PLAN.md` | Authored plan first with source trace, 17 targets, exact desktop geometry, state/navigation, responsive/accessibility, API discrepancy and quality gates. | VERIFIED_STATIC_ONLY |
| Chrome CUA | `getState()` returned `{apps:[], browsers:[]}`; both `createBrowserTab("chrome", ...)` and `createBrowserTab("iab", ...)` returned `Browser is not available`. No tab was available to upload the plan. | TOOL_UNAVAILABLE |
| `python3 apps/study-client/docs/dd_screens/resource/SH-04/build.py` | Revision 2 rendered clean/annotated screens at 1440×960 and transparent request-folio artwork at 470×270; regenerated SCREEN.md and `SH-04_design_handoff_v2.zip` with 17 element rows/markers. | VERIFIED_ARTIFACT |
| Visual review via `view_image` | Re-opened clean and annotated revision 2 at original resolution after removing a stray illustration line. Dark editorial panel and light status card read as distinct regions; badge numbers 1–17 remain legible and outside copy, artwork focal area, status values, and CTA label. | VERIFIED_VISUAL |
| Contrast review with `frontend-design/scripts/contrast-checker.py` | `#FFFFFF/#073B57` 11.85:1; `#E8F4FA/#073B57` 10.58:1; `#FFFFFF/#0B5F8A` 6.96:1; `#536A7A/#FFFFFF` 5.66:1; `#0B5F8A/#E8F4FA` 6.21:1. All composed normal text pairs pass WCAG AA. | VERIFIED_STATIC_ONLY |
| ZIP and exact element audit (Python stdlib) | `zipfile.testzip()` clean; all 9 package members byte-match workspace; screen PNGs 1440×960 and artwork 470×270 with alpha; plan and screen agree on CTA bounds; detail table and annotated badge IDs are exactly 1–17. Current package is v2; stale v1-named archive removed. | VERIFIED_ARTIFACT |
| Project tests | No API/frontend tests run; this is a design/documentation artifact task, not runtime implementation. | NOT_RUN |

## HANDOFF

- SH-04 revision 2 is locally built, visually reviewed and artifact-audited: `PLAN.md`, `SCREEN.md`, clean/annotated images, editable SVG, transparent artwork, repeatable `build.py`, and verified v2 ZIP.
- Requested ChatGPT website authoring remains incomplete because CUA exposes neither Chrome nor the in-app browser; no prompt or files were submitted. Do not describe the local revision as ChatGPT-authored. If the browser becomes available later, ask ChatGPT to critique this package and provide a concrete fix pass.
- Next screen in inventory order: SH-05 in a separate screen session. Keep the overall all-screen goal active.
