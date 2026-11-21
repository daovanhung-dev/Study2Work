---
task_id: "2026-11-07-design-study-screen-ad19"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-36; API #92; AD-19 → AD-20/AD-21 notification handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-19

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 224; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; trace catalog, current route/source and test evidence; do not infer UI behaviors or data mapping from mockup; retain permission and schema blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep Study Web `UNWIRED` unless editable router/client proves otherwise; inspect exact API filters/response; preserve original assets; use test source/history as evidence, not proof of current runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep current source separate from catalog/AC; don't infer lifecycle, PII, or route state from static UI; document API source classification and separate DD/implementation/runtime status.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad18.md` — AD-18 is complete; its screen task recorded the one-screen-per-session boundary, plan-first order, static source/API distinctions, `R` reverse-index rule and repository-wide context-validator failure. AD-19 is the next Screen ID.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-19 only; inspect inventory, AC-36/API #92 and current screen/source state; save `AD-19_PLAN.md` before markers/annotation/DD; preserve source assets; create ordered one-to-one marker artifacts and A–F DD; update inventory, reverse API index, G-12/global tracker and this worklog; run static artifact audit; do not start AD-20.
- Inventory row 77: AD-19 “Danh sách thông báo quản trị”, candidate `/admin/notifications`, AC-36, API #92; list/search status/channel, rows for draft/scheduled/sent, links AD-20 and AD-21; expected `loading/empty/ready/error`; P1. AC-36 names Admin with notification-management permission; flow opens management, GET #92, queries notifications, then branches Create/Update/Delete/Status and reload.
- Direct catalog #92: `GET /api/v1/admin/notifications`, Bearer/Admin; query `status?:string`, `channel?:string`, `page?:int32`; direct response `ApiEnvelope<Notification>` with reusable fields `id,title,content,channels,status,read_at?,scheduled_at?,created_at`; exact statuses 200/401/403/503/500. API DD is Draft. Current route/source and prototype must be compared; do not infer filtering, metrics, campaign grain or lifecycle from screenshot.

## CURRENT_BEHAVIOR

- Target folder contains only `screen.png` (1600×1411, SHA-256 `cc7639d88514680b8a7f99cc5cceffffd3b530842dd7e9ffe9121c39bb8b0064`) and `code.html` (22,898 bytes, SHA-256 `1145efb6cb148acdb5624357ed11c7fd012effa4ee1ba74b81ab7cdc587c661b`). Screenshot is a static empty state with four zero-count cards, search/channel/status controls, seven table headers, empty-state copy, disabled pagination and a policy note.
- Study Web root currently contains only `dist/`, `docs/`, `node_modules/`, and `tsconfig.tsbuildinfo`; no editable source/router/API client. Current route/runtime is `UNWIRED` / `NOT VERIFIED`.
- HTML has no fetch/XHR/API request. Reset locally clears search and selects; refresh only spins/disables the button for 800 ms. Pagination buttons are disabled. CTA uses `/admin/notifications/create` while inventory AD-20 route is `/admin/notifications/new`; policy link is `/admin/guidelines/notifications` with no inventory/source target; shell/footer anchors use `#`.
- API #92 route is registered and uses shared `ADMIN` auth before query/page validation or DB. Filters are raw exact-match status/channel; page defaults to 1, positive int32; two read-only count/list queries use fixed size 20 and `created_at DESC,id DESC`. Source joins legacy BIGINT `notifications` to `notification_deliveries`, includes only rows with at least one delivery, computes channels (`EMAIL|PUSH`) and aggregate status (`QUEUED|FAILED|SENT`, queued then failed then all sent). Response is local `Page<Notification>` with id/title/content/channels/status/created_at and pagination; optional read_at/scheduled_at are omitted. No recipient, scheduled send time, campaign counts or draft rows are mapped. No commit or provider call.
- Direct catalog response is `ApiEnvelope<Notification>`, so local Page is `DERIVED`/discrepant. Local OpenAPI also declares 422 page validation beyond direct catalog errors; catalog status/channel enum values are not specified. API DD remains `Draft — Needs Confirmation`, with open questions on pagination, recipient-vs-campaign grain, legacy vs V1-PILOT model, enums, permission/scope, 503 trigger, empty/422 behavior and #93 Operation bridge.
- Checked-in legacy DDL has BIGINT `notifications` with recipient/sender IDs, title/content/type/is_read/created_at/operation_id; migration 009 adds a delivery outbox with PUSH/EMAIL and QUEUED/SENT/FAILED. This is a design/schema candidate, not live DB proof. V1-PILOT notification schema is a separate learner-scoped UUID model.
- Test source exists. `.agents/server-study/tests.md` records 20 focused #92 HTTP tests and 85 linked #63/#64/#87/#92; tests use fake DB projections. The 2026-11-01 report records a post-fix temporary-branch Uvicorn check for empty/populated filters (20/20 requests) and full suite 1326 passed; this is historical, not run in this session and not UI/live production evidence.
- Inventory row 77/API reverse index #092 both initially say D; global AD-19 plan row says `CHƯA_BẮT_ĐẦU`; G-12 is a broad notification/moderation blocker. Manifest registry confirms `createDD-markdown` is API-DD-only and excludes `web-ui-only-dd`; no canonical UI-only DD skill applies.

## SOURCE_TRACE

```text
Expected: AC-36 Admin with notification-management permission opens AD-19, calls #92 with supported filters, reviews notification rows, and chooses AD-20 or AD-21; inventory lists search/status/channel and draft/scheduled/sent list use cases. Direct catalog #92 is a Notification response, not a defined page or metric contract.
Current: Study Web has no editable route/client; HTML is static except local Reset and 800ms refresh animation. CTA route differs from AD-20 inventory route. Local #92 uses ADMIN, exact status/channel filters, 1-based page size 20 and returns a legacy/outbox-derived Page limited to rows with deliveries. It omits recipient and scheduled time, and its Page/status/channel semantics remain DERIVED against the direct catalog. No metrics/detail API is defined by #92.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #92 response | Catalog direct `ApiEnvelope<Notification>`; current local route returns `ApiEnvelope<Page<Notification>>` with a delivery-derived projection. | DISCREPANCY / DERIVED | Do not map pagination or empty state as approved contract until owner resolves cardinality. |
| Search, status/channel filters | Screenshot has title search, app/email/system, draft/scheduled/published; catalog has no search and does not enumerate values; local exact-match source accepts EMAIL/PUSH and FAILED/QUEUED/SENT. | DISCREPANCY / BLOCKER | Do not send unsupported query or silently translate casing/enum values. |
| Metrics and table columns | Cards imply totals/published/scheduled/drafts; recipient and send-time columns. #92 only returns paged delivery-backed rows with title/content/channels/status/created_at. | STATIC_ONLY / UNMAPPED | No counts/recipient/scheduled-time mapping; do not derive from current page or extra calls. |
| CTA and guidelines routes | HTML `/admin/notifications/create` and `/admin/guidelines/notifications`; inventory AD-20 `/admin/notifications/new`; no router or guideline screen found. | DISCREPANCY / UNWIRED | No verified destination; reconcile create path before implementation. |
| Study Web wiring | Current tree has docs/dist/node_modules/build metadata only, no editable source/router/API client. | UNWIRED / NOT_VERIFIED | Candidate URL only. |
| Permission/schema/lifecycle | AC-36 requires notification-management permission; local code only checks ADMIN; notification campaign grain and live schema unresolved. | BLOCKER | Keep row grain, global/tenant scope, status mapping, sent/delivery semantics and runtime availability open. |

## CHANGES

- Active worklog created after docs preflight and before deep source inspection.
- Completed AD-19 plan, 48-marker JSON/SVG/annotated image, A–F screen DD, inventory row 77, reverse #092, G-12 and global tracker. AD-20/AD-21 screen artifacts were not edited.
- AD-19_PLAN.md was saved before marker creation; generated 48-point JSON/SVG markers and a 3200×2822 annotated PNG from the original 1600×1411 screen. Original PNG/HTML hashes remain unchanged; annotated output was visually inspected and the markers do not obscure the main copy or controls.
- CONTEXT_UPDATES: none; no executable code, API/DB contract or shared agent context page changed.
- Assumptions: none; unresolved decisions remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, `.agents/AGENTS.md`, context map, worklog contract/template read; exact docs selector READY 3/224; AD-01/02/03 worklogs fully reviewed. | VERIFIED_PREFLIGHT |
| AD-19 source/contract review | Verified inventory/AC-36/API catalog and Draft DD, route/validator/query/model/view, DDL candidate, focused test source/history, HTML handlers/links, screenshot and Study Web source absence; findings and discrepancies recorded above. No application tests run. | VERIFIED_SOURCE_REVIEW |
| Marker/annotation generation and visual review | 48 sequential in-bounds marker points, JSON and SVG overlay created; annotated PNG is 3200×2822 (2×) and was visually inspected for clipping/overlap. | VERIFIED_ARTIFACT |
| Static artifact audit | JSON/SVG parse; marker IDs/coordinates and DD rows 1–48 match; plan/JSON/SVG/DD coordinate maps match; 22 relative links resolve; image dimensions/hashes and 83/83 IDs/folders verified; core artifact sets 72/83; git diff --check passes. New authored files and changed tracker lines are whitespace-clean. Whole-file scan found pre-existing trailing spaces on unchanged list_screen.md lines 3–6. | VERIFIED_STATIC |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Source review completed before plan authoring. Key implementation trace: apps/study-server/app/api/v1.py:2692-2706 → api_92_admin_notifications_list/validate.py:54-101 → query.py:3-73 / models.py:16-63 → view.py:186-254; fake DB test source: tests/modules/admin/api_92_admin_notifications_list/test_admin_notifications_list.py:121-207. Catalog/AC and data-model open questions are recorded in EXPECTED_BEHAVIOR, CURRENT_BEHAVIOR and DISCREPANCIES_AND_STATUSES.
- Saved the required AD-19_PLAN.md after source review and before marker/image/DD authoring. Its 48-point marker map, event plan, contract splits and blockers are recorded in the screen folder.
- AD-19.md is complete with A–F, 48 element rows and EV-01…EV-10 ordered flows. Direct catalog and local #92 behavior remain separate; unresolved product/API decisions are marked blockers.
- Remaining work: none for AD-19; the next Screen ID is a separate session.
- Remaining blockers: direct catalog singleton vs local Page response; filter/status/search and metric/data mappings; Admin permission, row grain/live schema, #93 Operation bridge, CTA/guidelines routes and Study Web wiring.
- Status: DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. AD-20 is next only in a separate session.
