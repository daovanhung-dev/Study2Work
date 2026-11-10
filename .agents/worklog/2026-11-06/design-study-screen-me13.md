---
task_id: "2026-11-06-design-study-screen-me13"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-13 course/student recipient selection hands selected recipient IDs to ME-14 and API #63; trace APIs #46/#62/#63 against AC-25 and current Study Server source"]
status: "COMPLETE"
---

# Worklog: Detailed Design màn hình Study ME-13

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; 3 exact-type docs worklogs selected of 200; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-gs01.md
    - carry_forward: Separate expected behavior from current source; preserve original screen assets; Study Web remains UNWIRED; APIs/local DDL/tests do not establish live runtime or schema.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs02.md
    - carry_forward: Trace query/body and response precisely; keep screenshot/HTML/API discrepancies visible; do not invent filters, fields or route behavior.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs03.md
    - carry_forward: One Screen ID per session; trace caller/callee/DB/response/tests; preserve API DD draft and live-schema limits; no Study Web runtime claims.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Complete only ME-13 in this session; write ME-13_PLAN.md before marker map, annotation and DD; preserve screen.png/code.html; produce one-to-one ordered markers and A–F DD; trace AC-25, navigation, API handoff and errors; update inventory, global DD plan and worklog.
- Inventory: ME-13 “Chọn người nhận thông báo”, proposed /mentor/notifications/new/recipients, actor Mentor, AC-25, APIs #46 and #62, next ME-14; expected states loading/empty/selected/denied.
- Cross-screen expected flow: choose course, load course students, preserve selected recipient identifiers for ME-14; ME-14 uses #62/#63. Exact query/body handoff must be verified against current API and AC.
- Initial asset inventory before deep source trace: folder contained screen.png (1600×1546, SHA-256 2764685b871d5e2340942fded53ed9c67a392cd9d65dd4239c007d282ecf45ed) and code.html (22,336 bytes, SHA-256 2547eb7f6b7263cb509916a66833b2484c9494b3d608263e856da15c807b72ca); no plan, DD, marker map/overlay or annotated image.

## CURRENT_BEHAVIOR

- screen.png is a 1600×1546 static design and code.html has no app handlers, fetch/XHR/WebSocket, form submit or router binding. Anchors use href="#"; Continue is disabled. The screenshot shows no loaded student rows.
- Study Web is registered UNWIRED; no screen runtime or route implementation was found.
- The course selector has static slug values cs101/fe202/ba301/qa401. The screenshot claims current semester/assigned Mentor and support-needed classification; the dependent APIs do not return these semantics.
- #46 route/module/test source returns paginated direct-owner courses with optional DRAFT/PUBLISHED status. It has no semester/assignment fields.
- #62 route/module/test source returns ACTIVE-enrolled role STUDENT rows with id:int64, full_name and optional avatar_url, filtered to direct course owner. It has no progress/attendance fields, pagination or email.
- #63 route/module/tests locally accept CSV recipients and channels, title≤200 and content:int64, then commit notification rows and QUEUED delivery outbox rows before HTTP 202. The response has Operation UUID separately from notification_ids:int64[]. No delivery worker/provider is wired; API DD remains Draft and CSV mapping is DERIVED.

## SOURCE_TRACE

- AC-25 page confirms Mentor actor and the course → #62 roster → recipients/title/content → #63 → DB/outbox → Push/Email → #64 status flow. Current source has local #46/#62/#63 routes and tests; this docs task did not execute tests.
- #46: GET /api/v1/mentor/courses; Bearer Mentor; optional status DRAFT/PUBLISHED, page≥1, size 1..100; direct owner; order created_at DESC/id ASC; 200 CoursePage with pagination; empty page allowed; query errors 422; auth 401/403; query/mapping errors 500.
- #62: GET /api/v1/mentor/courses/{course_id}/students; path int64; active enrollment + STUDENT role; direct owner; distinct IDs sorted ascending; 200 data[] {id:int64,full_name,avatar_url?}; empty array is success; 401/403/404/500. No account-status filtering or progress/checkpoint/attendance.
- #63: POST /api/v1/mentor/notifications; strict required recipients:string CSV positive int64, title:string≤200, content:signed int64, channels:string CSV PUSH/EMAIL; extra fields rejected. Entire recipient set must share an ACTIVE course directly owned by Mentor, but body has no course_id. 202 DESIGN_OPERATION_ACCEPTED follows transaction commit; Operation.id is UUID and meta.notification_ids are int64 IDs. Errors 401/403/422/503/500. No idempotency key or consumer/provider.
- Discrepancies: ME-13 HTML slugs vs int64 IDs; semester/assigned-course copy vs #46; support-needed copy vs no progress/attendance source; privacy/email/WCAG claims vs APIs; #63 content:int64 vs free-form text expectation; #63 lacks selected course and local DD is Draft; no exact ME-14 selection transport.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| APIs #46/#62/#63 | Current route/module/query/model/test files exist locally; #63 DD is Draft and several mappings are DERIVED. | SOURCE-BACKED LOCALLY; not live/runtime verified | Reverse source index can be D→R for local source presence; DD/DB/deployment status remains separate. |
| Course selector | Prototype slugs; #62 needs int64 course_id; #46 returns numeric id/title. | DISCREPANCY | Must bind source IDs; no mapping from slugs exists. |
| Course eligibility | Prototype says current semester/assigned course; #46 direct owner, no term field. | BLOCKER | Product must approve eligible course/status/ownership semantics. |
| support_needed | Prototype describes late/low-checkpoint/absence; #62 returns no such metrics. | BLOCKER | Do not infer criteria from other endpoints or calculate unsupported group. |
| Recipient selection/handoff | Prototype lacks loaded rows/checkboxes; #63 uses CSV but has no course_id; inventory expects IDs to ME-14. | BLOCKER / DERIVED | Confirm loaded-row UX, int64-safe storage and handoff/CSV contract before implementation. |
| Content/privacy/channel claims | Prototype claims free-form notification, anonymity, linked-school email/WCAG; #63 content is int64 and has no privacy field. | DISCREPANCY / BLOCKER | Product/security/API must resolve; no implied behavior in DD. |
| Study Web runtime | Context manifest and current app source still show UNWIRED. | UNWIRED | No route, API call or interaction is runtime verified. |

## CHANGES

- Created ME-13_PLAN.md before marker map, annotated image and DD.
- Created 49-entry ME-13_markers.json, ME-13_markers.svg, 3200×3092 screen_annotated.png and ME-13.md A–F. Original screen.png and code.html were not intentionally modified.
- Updated ME-13 row in list_screen.md and dd_screens/PLAN.md; reverse source index #46/#62/#63 changed D→R based on local route/module/test presence. Screen and API DD/runtime states remain separate.
- CONTEXT_UPDATES: none; no registered context statement was found to be inaccurate. API local-source classification is recorded in the screen inventory/tracker, while open DD/live-schema/runtime limits remain explicit.
- Assumptions: none. Unsupported UI claims and unresolved course/recipient/content/privacy/handoff decisions are blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective file | Reread before continuing this Screen ID session. | VERIFIED |
| Docs worklog preflight | Selector selected and all three exact-type worklogs were read; no shortage. | VERIFIED |
| Source, marker, link, asset and tracker audit | 49 markers sequential/unique/in-bounds and matching between plan, JSON, SVG and 49 DD rows; eight events present; relative links resolve; screen.png and code.html hashes match preflight; screen_annotated.png is 3200×3092 and was visually reviewed; inventory row/API index/global status checked; core artifact count is 48/83; git diff --check passes. | PASS_STATIC |
| node scripts/validate-agent-context.mjs | Failed with repository-level missing DB Admin context/source paths and stale server-study context fingerprints. No context page or manifest was changed in this task; this is outside ME-13 screen artifacts. | FAIL_EXISTING_REPO_CONTEXT |
| Tests/runtime | Not run for this docs task. | NOT_RUN |

## HANDOFF

- Remaining blockers: course slug→int64 and eligibility; semester/assignment; support-needed criteria; loaded roster UI and selection retention; int64-safe ME-14 handoff and course binding; #63 content:int64 vs text; privacy/channel claims; no delivery worker/provider; Study Web UNWIRED.
- Current status: DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Result: static verification complete; source assets preserved; tracker/worklog updated. Stop after ME-13. Do not start ME-14.
