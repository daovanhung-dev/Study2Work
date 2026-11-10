---
task_id: "2026-11-06-design-study-screen-me14"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-14 consumes recipient IDs selected in ME-13, calls API #63, and hands Operation UUID plus notification_ids to later #18/#64 flows; compare AC-25 and current Study Server source"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-14

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; 3 exact-type docs worklogs selected of 201; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-gs01.md
    - carry_forward: Keep expected behavior separate from current source; preserve assets; Study Web is UNWIRED; no canonical skill applies to UI-only DD; API/catalog and DDL are not runtime proof.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs02.md
    - carry_forward: Keep screenshot/HTML discrepancies and API contract limits explicit; do not infer URL/router/cache behavior; source test files were read, not run.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs03.md
    - carry_forward: Trace exact route/view/query/response/errors; distinguish SOURCE_BACKED from DECLARED_NOT_RUNNABLE; preserve cross-screen and operation-ID semantics; no runtime claim.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-14 only in this session; read current screen assets and AC/API/backend source; write ME-14_PLAN.md before marker map, annotation and DD; preserve screen.png/code.html; create one-to-one sequential annotation and A–F DD; update screen/API tracker, global plan and worklog.
- Inventory: ME-14 “Soạn thông báo mentor”; proposed route /mentor/notifications/new; AC-25; APIs #62/#63; next ME-15; states draft/validating/sending/accepted/error; inventory expects ME-13 recipients → POST #63 → #18 if an operation ID is returned.
- Prior screen handoff: ME-13 preserves unique Student int64 IDs, but exact transport/persistence is unresolved. Do not assume route state, query string, session storage or CSV conversion is approved.

## CURRENT_BEHAVIOR

- Before visual/deep source review, the ME-14 directory contained only screen.png (1267×1600; SHA-256 bc6d536347650aaa8ab357da960fe14753b4b261b5c77657af0e90072f9b2324) and code.html (31,875 bytes; SHA-256 ebb83dd43389906390a57bd16895311fca1a12c5ff8c1b02b0b0078f5af2c6de). No plan, DD, marker map or annotated image existed.
- Study Web remains registered UNWIRED. Screen markup, API requests, route state and authentication behavior are not current browser runtime evidence.
- HTML contains title maxlength=120 and a title/body-only preview/counter script; all other controls are handlerless. There is no form, file input, draft persistence, router, fetch/XHR, websocket, or API integration.
- API #63 route/module/model/view/query and focused test source exist locally. Strict request fields are recipients CSV, title max 200, signed int64 content and PUSH/EMAIL CSV. For schema-valid requests the Mentor guard precedes CSV/scope/DB; recipient scope is common ACTIVE Student enrollment in a directly owned course, inferred because the body has no course_id. Source writes notification/outbox rows transactionally and returns 202 after commit, with Operation UUID in data.id and notification int64 IDs in meta. API DD is Draft/Needs Confirmation; CSV/scope/projection are DERIVED; tests were read but not run.
- API #64 route/module/model/query/test source exists locally. It reads a single int64 notification_id, checks sender ownership and derives Operation status from delivery rows; no worker/provider delivery is wired. API #18 has no Study route/module/query/test and has unresolved ID/lifecycle contract issues; AC-25 does not connect it to the send flow.
- API #34 accepts only SUBMISSION/LECTURE purposes; source has no MIME allowlist or app size cap, but does not provide notification attachment linkage. The screen's PDF/DOCX/ZIP/25 MB claims are not current API #34 behavior.

## SOURCE_TRACE

- ME-13 handoff → ME-14: ME-13 selected Student IDs are int64 but the carrier and course binding remain unresolved. No ME-14 fetch of #62 is evidenced; #62 is the upstream roster call.
- AC-25: #62 roster → select recipients/title/content → POST #63 → queued notification/outbox → Push/Email → #64 status. AC diagram also has an isolated #18 operations node, with a UUID/path discrepancy versus the #18 catalog row; no flow edge connects it to #63/#64.
- #63: route at `apps/study-server/app/api/v1.py`; request/view/query/model in `app/modules/mentor/api_63_mentor_notifications_create/`; error and open-question DD read; focused tests read. Request requires positive int64 CSV recipients, title max 200, signed-int64 content and PUSH/EMAIL CSV; extra keys forbidden. Scope is common ACTIVE roster on at least one directly owned Mentor course, with no course_id. Writes one notification per recipient plus per-channel QUEUED rows; commits before 202; response separates Operation UUID and notification IDs. Errors are 401/403/422/503/500. No idempotency key or worker/provider.
- #64: router/view/model/validator/query/DD/test source read. Single notification int64 ID; Mentor sender-only check; 401/403/404/500; read-only aggregation; `QUEUED` if any queued, else `FAILED` if any failed, else `SENT` when all sent. Status projection is DERIVED and no worker is wired.
- #18: current source/module scan found no route/module; DD says UNWIRED/NOT_FOUND; operation ID type, owner/admin policy, persistence/lifecycle/result and producer response remain unresolved.
- #34: upload route/module/policy/request DD/open questions read. Only SUBMISSION/LECTURE purposes; any MIME and no application size cap currently; no notification-purpose relationship or #63 attachment field.
- Current prototype: full screenshot and HTML inspected. Title/body only handlers update local DOM preview/counters; channel, toolbar, attachment, save, send, nav/help/footer do not work in this artifact. Screenshot metric, compliance and delivery copy have no source-backed runtime evidence.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ME-14 assets | Current folder initially has only original PNG and HTML. | INITIAL_INVENTORY | Preserve both bytes and record initial hashes. |
| Recipient handoff | ME-13 inventory and DD preserve IDs but exact carrier is not approved. | EXPECTED / OPEN | Confirm transport from current design/source; do not guess. |
| Body text mapping | Prototype accepts free text; API #63 model requires signed int64 `content`. | DISCREPANCY / BLOCKER | Do not convert body text to integer or invent a content source. |
| Recipient/course scope | ME-13 handoff carrier unresolved; API #63 lacks course_id and infers a common owned active roster. | DISCREPANCY / BLOCKER | Cannot guarantee send targets selected course. |
| Title/channel | Prototype title max 120 and In-app/Email; #63 title max 200 and PUSH/EMAIL. | DISCREPANCY / BLOCKER | Product must approve bounds and channel mapping. |
| Attachment/draft | Prototype claims file upload and exposes save draft; no handlers/API link; #34 purpose is unrelated. | PROTOTYPE ONLY / BLOCKER | No upload/draft contract to implement. |
| API #63/#64 | Local source/module/model/query/test files exist; DD status Draft/DERIVED. | SOURCE_PRESENT / tests NOT_RUN | Keep 202 queued distinct from delivered; separate Operation and notification IDs. |
| API #18 | No Study route/module/query/test; unresolved catalog/diagram IDs and lifecycle. | UNWIRED / NOT_FOUND | Do not poll from ME-14; AC-25 has no edge. |
| Study Web runtime | Context registry marks Study Web UNWIRED. | UNWIRED | Do not claim current route, editor state or API integration. |

## CHANGES

- Created `ME-14_PLAN.md` before marker map/DD, with source boundary, event plan, blockers and review gate.
- Created 68-element `ME-14_markers.json`, reproducible `ME-14_markers_overlay.svg`, and 2× `screen_annotated.png`; source image and HTML were not edited.
- Created `ME-14.md` sections A–F; documented #63/#64/#18/#34 current source versus design, prototype-only behavior, and blockers.
- Updated ME-14 in `list_screen.md` and global plan, corrected AC-25/F10 ID handoff, and marked API #64 source-backed based on local route/module/test presence. API #63/#64 tests remain unrun.
- CONTEXT_UPDATES: none; current context registry remains accurate.
- Assumptions: none; unapproved mapping decisions are listed as blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal objective | Reread before this Screen ID session. | VERIFIED |
| Docs worklog preflight | Selector returned and all three exact-type worklogs were read; no shortage. | VERIFIED |
| Source trace | AC-25, #63, #64, #18 and #34 current source/docs/tests read; tests not run. | VERIFIED / NOT_RUN |
| Source hashes | Current `screen.png` and `code.html` SHA-256 match initial values. | VERIFIED |
| Marker/DD/tracker audit | 68 markers = 68 DD rows; IDs sequential/unique/in-bounds; 13 event IDs; 8 local links exist; original PNG/HTML hashes unchanged; `git diff --check` clean; annotated PNG 2534×3200 inspected. | VERIFIED |
| Tests/runtime | Not run for this documentation task. | NOT_RUN |

## HANDOFF

- Remaining blockers: course-bound ME-13 handoff; body content type; title bound/blank rule; channel/provider; notification attachment; draft persistence/retry; Study Web route/auth/state wiring. API #18 remains separate and unwired.
- Next action: stop after ME-14. ME-15 is a separate session and must not be started here.
