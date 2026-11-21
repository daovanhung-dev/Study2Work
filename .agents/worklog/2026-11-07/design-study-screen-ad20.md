---
task_id: "2026-11-07-design-study-screen-ad20"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-36; API #93; AD-20 → AD-21/SH-07 notification handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-20

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; 3 exact-type docs worklogs selected of 225; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-07/design-study-screen-ad01.md
    - carry_forward: Preserve expected/current separation; do not infer UI behavior or KPI mapping from mockups; keep Study Web UNWIRED unless editable source proves otherwise; trace API/auth/data/tests and do not claim tests/runtime/live schema verified.
  - path: .agents/worklog/2026-11-07/design-study-screen-ad02.md
    - carry_forward: Keep AC permission distinct from local ADMIN fallback; do not infer fields/actions from mockups; preserve PII/schema blockers; API DD and UI DD have different skill boundaries.
  - path: .agents/worklog/2026-11-07/design-study-screen-ad03.md
    - carry_forward: Check Study Web tree each session; preserve source assets; trace API source and response/errors; fake DB tests do not prove live schema; avoid guessed identity, route or operation semantics.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-20 only; inspect current inventory, AC-36, API #93/catalog and backend source; save AD-20_PLAN.md before marker/image/DD; preserve source; produce ordered marker map and 2x annotated image; write A–F screen DD with traceable events, API/errors, state and navigation; update list_screen.md, dd_screens/PLAN.md and this worklog; do not continue to AD-21.
- Inventory row 78: AD-20 “Soạn/gửi thông báo hệ thống”, route /admin/notifications/new, AC-36, POST #93. Expected fields include recipients or segment, channels, preview and confirmation; expected response 202; if response has operation_id then go to SH-07, and 202 does not mean delivered. Links AD-21 and SH-07; expected states draft/submitting/accepted/failed; P1; tracker blocker says recipient/segment delivery schema and operation ID unclear.
- AC-36 expected flow: Admin with notification-management permission opens notification management, loads #92, then chooses Create/Update/Delete/Status. #93 is a conditional create/send branch; response/operation handoff conflicts must be preserved.
- Source review: selector and three same-type worklogs were completed before deep inspection. Source asset folder, AC-36, catalog, #93 API DD/open questions/verification report, #18 contract/SH-07, current route/module/query/view/model/tests/DDL and Study Web tree were inspected.

## CURRENT_BEHAVIOR

- Before this session's artifact work, inventory row 78 remained D and global AD-20 plan row remained CHƯA_BẮT_ĐẦU; AD-19 is the previous completed screen (72/83 core artifact sets).
- AD-20 source folder contains the original 1242×1600 `screen.png` and 30,107-byte `code.html`; SHA-256 values: image `e5aa0769daf49ef5571598a9993fe38e5eb3a7760a00a8ba3d487186ecc9a6b4`, HTML `e65ba6bb2f63775a512e1c46e6a7d90408b445f93d8b7c8dab808b95fb65cfe9`.
- Study Web has no editable `src/`, router, app manifest or API client in the current checkout; the artifact HTML is not an application route. Its only script mirrors title/body into the preview. Segment/channel/priority controls, toolbar, save/send controls and technical lifecycle card have no event handlers; Send is statically disabled. Anchors use `#`; no fetch/XHR or form submit exists.
- Current API #93 route is registered in `apps/study-server/app/api/v1.py` (POST, HTTP 202). It authenticates shared `ADMIN` before body/database work; local validation requires explicit nonempty, unique positive int64 recipients, rejects any supplied segment, requires nonblank title/content, title ≤200 characters, and unique nonempty `PUSH|EMAIL` channels. These are current local fallback rules, not approved product requirements.
- Current #93 view queries explicit user IDs without role/status/course filtering, inserts one legacy notification per recipient and one QUEUED delivery row per notification/channel, attaches a shared UUID `meta.operation_id` and all notification IDs, validates the response projection, commits the batch, then returns 202 with the first notification in `data` and `DESIGN_OPERATION_ACCEPTED`. It does not create an Operation record, call a provider, or dispatch a worker. Errors include auth 401/403, validation/unknown recipients 422, DB OperationalError/invalidated connection 503, and other query/projection/commit failure 500 with rollback attempts.
- Catalog row #93 and AC-36 n5 specify `ApiEnvelope<Notification>` at 202, while the general operation-tracking prose says #93 returns `ApiEnvelope<Operation>`. Local source follows direct Notification data and adds UUID metadata; API #93 DD labels that metadata a DERIVED fallback. API #18 declares `operation_id:int64` in its row while its reusable Operation schema, diagrams and UUID convention use UUID; no Study #18 route/module/query/test or generic Operation table was found. SH-07 explicitly blocks producer mapping and polling. Preserve all discrepancies; no SH-07 navigation can be treated as runtime contract.
- AC-36 macro review #92–#96 remains `VERIFIED_WITH_OPEN_QUESTIONS`; #93 DD is `Draft — Needs Confirmation` with Q-93-01…10. Local focused tests exist (including direct Notification response, auth-before-body, invalid request, unknown recipients, rollback, projection, OpenAPI assertions); tests were inspected but not run. Prior API verification report records fake-DB test results only and does not prove live schema, deployment, provider delivery or owner approval.
- The checked-in legacy BIGINT notification/outbox DDL is only a local candidate; the separate V1-PILOT UUID model is not interchangeable, and no live DB schema was verified.

## SOURCE_TRACE

Expected flow: Admin notification-management permission → AD-20 draft inputs recipients or segment, title/content/channels → validate and submit POST #93 → inspect HTTP 202/business code and approved response shape → if a valid operation_id exists, hand off to SH-07; accepted is not delivered.

Current flow: browser prototype presents static inputs/options; title/body input events update only preview text. No app router/API client or control submission is present. If implemented against current local #93 source, the backend would require explicit recipient IDs (segment is rejected), queue per-recipient/channel rows and return 202 after commit; this is DERIVED local fallback, not approved screen behavior. API #93 direct `Notification` response conflicts with the tracking prose's `Operation`; source adds `meta.operation_id:UUID`, but no Operation row is created. The ID also conflicts with API #18's int64 path declaration, while SH-07 has no current #18 runtime. Therefore the expected AD-20→SH-07 handoff is blocked until API #93/#18 and producer contracts are approved; 202 never means delivered.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #93 Notification vs Operation and #18 ID | Catalog/AC-36: Notification at 202; tracking prose: Operation; local source: first Notification + `meta.operation_id:UUID`; #18 row: int64 vs schema/AC/SH-07 UUID; no #18 runtime/store. | DISCREPANCY / BLOCKER | Specify accepted response only as conflicting design/local shapes; no operation polling or SH-07 route is ready. |
| Recipient vs segment, channel and notification grain | Catalog leaves selection/enum rules open; local fallback requires explicit recipients and PUSH/EMAIL, fans out one legacy notification per user/channel; AC-36 only says Notification + recipients and conditional Push/Email. | OPEN / DERIVED_LOCAL_FALLBACK | Do not infer segment predicates, role eligibility, channel mapping, campaign semantics or approved physical schema. |
| Validation, permission and dispatch | AC-36 says notification-management permission and conditional Send; local source checks ADMIN, has no action/schedule, and commits QUEUED outbox rows without worker/provider call. | DISCREPANCY / OPEN | UI cannot promise draft/send semantics, fine-grained permission, provider dispatch or delivery success. |
| Study Web route | Inventory candidate `/admin/notifications/new`; no editable Study Web app/router/API client exists in current source tree. | UNWIRED | Document route as candidate only and runtime as unverified. |

## CHANGES

- Files changed: AD-20_PLAN.md, AD-20_markers.json, AD-20_markers_overlay.svg, screen_annotated.png, AD-20.md, list_screen.md row 78/API #093, dd_screens/PLAN.md AD-20 row/checkpoint, and this worklog.
- Completed one screen only. AD-21 screen files were not edited.
- Annotation: 54 sequential markers, source coordinate map 1242×1600, rendered PNG 2484×3200 and visually reviewed after moving badges away from text.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; DERIVED fallback behavior is labeled and does not replace unresolved contract.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective file read at session start; root router instructions, context map, worklog README/template and exact docs selector state retained from this goal session; selector READY 3/225; AD-01/02/03 reviewed in full. | VERIFIED_PREFLIGHT |
| AD-20 source/contract review | Inspected source image/HTML (dimensions and hashes above), list_screen inventory, AC-36 macro boundary, API catalog and #93 DD/open questions/report, #93 route/model/validator/query/view/tests, legacy DDL/migration, #18 DD and SH-07 contract, Study Web tree. Discrepancies and local fallback separated. | VERIFIED_SOURCE_REVIEW |
| Plan and artifact generation | AD-20_PLAN.md saved before marker/image/DD work; 54 marker map, SVG overlay, 2484×3200 annotation and A–F DD created. Visual review confirms marker coverage and readable primary copy/controls. | VERIFIED_ARTIFACT |
| Static artifact/tracker audit | Plan/JSON/SVG/DD IDs and coordinates match; 54 unique sequential in-bounds markers; 12 events; all local DD links resolve; source hashes unchanged; inventory IDs/folders 83/83; complete core artifacts 73/83; annotated PNG 2484×3200; `git diff --check` passes; all five new authored text files pass trailing-whitespace check. | VERIFIED_STATIC |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining work: none for AD-20; process AD-21 only in a separate session.
- Remaining blockers: #93 response/audience/channel/permission/model/action approval; #18 ID/schema/runtime and SH-07 producer mapping; Study Web remains unwired. No decision is inferred.
- Final status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Stop after AD-20; AD-21 is a separate-session screen.
