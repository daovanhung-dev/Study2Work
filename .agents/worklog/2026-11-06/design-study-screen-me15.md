---
task_id: "2026-11-06-design-study-screen-me15"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-14 returns operation UUID and notification IDs; ME-15 must trace #64 notification status and #18 generic operation polling against AC-25/current Study source"]
status: "COMPLETE"
---

# Worklog: Detailed Design màn hình Study ME-15

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 202; shortage: none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from current UI/API source; Study Web is UNWIRED; preserve assets; test files and DDL are not runtime/live-schema evidence.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace current handlers and response shape; do not infer client route, polling, debounce or cache; preserve API/design discrepancies and test NOT_RUN status.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Verify source availability for each API; keep DECLARED_NOT_RUNNABLE separate from SOURCE_BACKED; AC flow order can conflict with inventory; do not infer navigation/runtime from mockup.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-15 only in this session; read current screen assets and relevant AC/API/source; write ME-15_PLAN.md before marker map, annotation and DD; preserve screen.png/code.html; produce sequential 1:1 markers and A–F DD; update list_screen.md, global plan and worklog.
- Inventory: ME-15 “Theo dõi gửi thông báo”; proposed route `/mentor/notifications/:notificationId/status`; AC-25; APIs #18 and #64; linked ME-14/SH-07; expected states queued/sending/complete/failed. Inventory says #64 reads notification_id and #18 may read operation_id; IDs must remain distinct.
- ME-14 handoff: #63 local source returns an Operation UUID in `data.id` and notification IDs int64 in `meta.notification_ids`. #64 status path is per notification ID. API #18 is currently unwired per ME-14/source inventory, and AC-25 has no edge to #18; reverify in current sources before writing ME-15.
- Current target asset inventory: folder initially contains only `screen.png` (1563×1600; SHA-256 `6172c259a4dfca9a37a6652ebdae83d3f10831b63dd8b59b5e988a23ea534713`) and `code.html` (22,004 bytes; SHA-256 `ccd0151ae1352662dc006483ff0e00094d9317d35762e76515252c32b7dda70f`). No plan/DD/marker/annotated image existed at preflight.

## CURRENT_BEHAVIOR

- Screenshot was visually inspected at 1563×1600. The HTML has one button (`#refreshBtn`), 13 anchors (all `href="#"`), no form/input/select, and no fetch/XHR/WebSocket. The refresh handler only disables/spins, waits 800ms, shows a success toast, then hides it after 3000ms; it changes no status values. The page's real-time/ACK/channel/progress/report/SyncEngine claims are static copy.
- Study Web remains registered `UNWIRED`; no current runtime route, auth guard, API client, status polling or navigation behavior can be inferred from these static assets.

## SOURCE_TRACE

- API #63 current handoff: `apps/study-server/app/modules/mentor/api_63_mentor_notifications_create/view.py` creates one UUID for the batch, persists it on each notification, accumulates each returned notification integer ID, and returns HTTP 202 `DESIGN_OPERATION_ACCEPTED` with `data: OperationResponse` (`id` UUID, `NOTIFICATION_DISPATCH`, `QUEUED`, owner/timestamps) plus `meta.notification_ids:int64[]`. `apps/study-server/tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py` asserts the UUID and IDs `[30001, 30002]`. This establishes two distinct identifiers; it does not identify which batch recipient the ME-15 route should select.
- API #64 current source: route in `apps/study-server/app/api/v1.py` is `GET /api/v1/mentor/notifications/{notification_id}/status`, HTTP 200. `apps/study-server/app/modules/mentor/api_64_mentor_notification_status/view.py` authenticates MENTOR before parsing, parses a signed-int64 path value (malformed/out-of-range maps 404; persisted notification IDs are positive), runs one read-only aggregate query, then checks `sender_id`. Wrong owner → 403; missing notification, missing operation link or no delivery rows → 404; malformed projection/query failure → safe 500. `query.py` groups one notification with its delivery rows and counts QUEUED/SENT/FAILED. The response is an Operation-like envelope with UUID `data.id`; status is derived per notification as QUEUED if any queued, otherwise FAILED if any failed, otherwise SENT if all are sent. It does not return batch-wide status or channel/recipient details. Source uses local outbox state; provider delivery/worker/live schema are not verified here.
- API #18 current source scan: no Study route, module, query or focused test is present. The DD folder marks #18 design-only/unwired. `docs/lists/list_api.md` row #18 says `operation_id:int64`, while the global ID convention, Operation schema and AC diagrams use UUID; the operation tracking summary says to poll #18. Do not call #18 from ME-15 or substitute its UUID for #64's int64 `notification_id`.
- AC-25 in `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`: connected node `n8` is #64 with `notification_id:int64`; separate `operation_status` node is #18 with `operation_id:uuid` and has no incident edge. This diagram is a design artifact, not runtime evidence. SH-07 likewise records #18 as unwired and #64 as notification-specific.
- Catalog entries #63/#64/#18 are design contracts. #64 catalog response uses `ApiEnvelope<Operation>`; current route/model/source agrees on Operation-shaped response but uses `DESIGN_RESOURCE_RETRIEVED` as the success code, while live schema/provider behavior is not verified.
- Expected/current discrepancy: inventory route `/mentor/notifications/:notificationId/status` can identify one int64 notification; #63 exposes several notification IDs per one UUID batch operation. No selected-recipient mapping, batch-level aggregation, polling cadence/terminal policy or return destination is approved. Prototype currently has a placeholder system ID, static queued-style label and fake refresh timer, and makes no request.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ME-15 assets | Initial folder has only original PNG and HTML. | INITIAL_INVENTORY | Preserve both bytes and record baseline hashes. |
| Operation and notification IDs | #63 source/test hand off one UUID plus `meta.notification_ids:int64[]`; #64 path is one int64; #18 has no Study implementation and its catalog path type conflicts with shared UUID schema. | VERIFIED_DISCREPANCY | Preserve both IDs and block producer-to-screen selection and generic polling. |
| API #64 projection | Current view/query computes local aggregate status for one notification and returns Operation-shaped response. | SOURCE_BACKED_LOCAL / LIVE_SCHEMA_UNVERIFIED | Can specify source-backed contract, not external delivery truth or a whole batch. |
| Study Web runtime and prototype | Static HTML only; `#refreshBtn` is mock timer/toast, anchors are placeholders, and no network transport is present. Study Web is `UNWIRED`. | UNWIRED / MOCK | Do not describe prototype copy as verified system state or claim polling. |
| AC-25 relation | #64 `n8` connected; #18 `operation_status` node disconnected. | VERIFIED_DESIGN_CONTRACT | ME-15 traces #64 only; generic SH-07 remains separate. |

## CHANGES

- Before deep source trace, created this worklog with exact-type worklog review and ME-15 expected contract.
- Created `ME-15_PLAN.md` before marker map, annotated image and DD.
- Added 54-element `ME-15_markers.json`, `screen_annotated.png`, A–F `ME-15.md`, and updated ME-15 rows in `apps/study-client/docs/list_screen.md` and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- CONTEXT_UPDATES: none; source findings are screen-specific and do not make the existing context pages inaccurate.
- Assumptions: none; source/design gaps will be recorded as blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected three exact-type docs worklogs of 202; no shortage. | VERIFIED |
| Selected docs worklogs | GS-01, GS-02, GS-03 read in full. | VERIFIED |
| Current screen/API/AC handoff trace | Read screenshot/HTML, #63 route/model/view/test, #64 route/view/query, #18 source absence, API catalog rows, AC-25 graph and SH-07 notes. | VERIFIED_READ; no tests run |
| Static asset/marker/DD audit | JSON parses; IDs 1–54 sequential and unique, all marker centers in bounds and separated; 54 marker IDs match 54 DD element rows in order; source and annotated PNG are 1563×1600; original `screen.png` and `code.html` SHA-256 values unchanged; required files and relative DD links exist; annotated image inspected visually. | VERIFIED |
| Tracker and diff audit | ME-15 inventory/global-plan rows updated; global count/checkpoint advanced to 50/83; `git diff --check` completed with no output/errors. | VERIFIED |
| Tests/runtime | Not run for this documentation task. | NOT_RUN |

## HANDOFF

- Remaining blockers: #18 is unwired and ID-discrepant; caller selection from #63's notification ID array, batch semantics, inventory/#64 state mapping, channel/detail report, ACK/realtime/polling behavior, link destinations and Study Web implementation remain unresolved. Live schema/worker/provider also remain unverified.
- Session scope completed: ME-15 only. The next suitable screen is ME-16 in a separate session; it was not started here.
