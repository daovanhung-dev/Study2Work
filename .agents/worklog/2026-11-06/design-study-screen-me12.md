---
task_id: "2026-11-06-design-study-screen-me12"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-11 requestId handoff to ME-12; trace APIs #59 detail, #60 reply and #61 resolve against AC-24 and current Study Server source"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-12

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 199; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from current source; Study Web is UNWIRED; source tests/local DDL do not prove live DB/runtime.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve original assets; do not infer interactions from static HTML; API contract/source discrepancies and fake-session test limits must be explicit.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Keep one Screen ID per session; distinguish screen assets from app runtime; trace linked API status, ownership and response fields; record AC/inventory discrepancies without guessing.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Handle ME-12 only in this session; write its plan before creating marker/DD; preserve `screen.png` and `code.html`; create an ordered one-to-one marker map, annotated image and A–F DD; trace APIs and handoff; update the global tracker and worklog.
- Inventory: ME-12 is Mentor support conversation/resolve at proposed `/mentor/support/:requestId`, AC-24, APIs #59/#60/#61; expected predecessor ME-11 and reverse link ME-11. F09 sequence is #58 inbox → #59 detail → #60 reply → #61 resolve only when allowed.
- Session facts established before deep source review: folder currently contains only `screen.png` (1600×1585, SHA-256 `35e218e17f8e9a55d7a8ba315887f3910979b2e3920801ef9d2c781e6b6f6df4`) and `code.html` (SHA-256 `4d4290f881dfaa94208851250083f95e4fddfa619be787fe43fcfc6512f3e6fc`).

## CURRENT_BEHAVIOR

- ME-12 folder initially had screen.png (1600×1585) and code.html only. Their SHA-256 hashes remain 35e218e17f8e9a55d7a8ba315887f3910979b2e3920801ef9d2c781e6b6f6df4 and 4d4290f881dfaa94208851250083f95e4fddfa619be787fe43fcfc6512f3e6fc.
- Static HTML has no script, submit handler, API fetch, XHR, WebSocket, route binding, attachment picker or dynamic character counter. Header/back/help/footer anchors are href="#". Request ID, status, empty-state copy, 0/2000 counter, disabled controls and Socket/TLS text are literals.
- Study Web remains UNWIRED in the context manifest and has no app source/package/router. Static prototype is not app runtime.
- #59, #60 and #61 have local route/module/query/model/test sources. API DD packages are Draft — Needs Confirmation; local schema and lifecycle choices remain DERIVED; live database and deployment are unverified.
- Migration 008 defines local BIGINT support_requests, support_messages and support_message_uploads tables. This is checked-in migration evidence only.

## SOURCE_TRACE

- Expected handoff: ME-11 #58 returns data[].id; route proposal is /mentor/support/:requestId; ME-12 reads with #59, replies with #60, refreshes #59 per inventory and resolves with #61 when permitted. No frontend runtime performs this flow.
- API #59 route is GET /api/v1/mentor/support/{request_id}; Mentor auth runs before path parsing/database access. Local parser accepts signed int64 syntax; invalid/out-of-range path maps to 404. Query is owner-scoped by courses.mentor_id, reads request/course/student plus the full ordered thread, and resolves ordered attachments. messages:[] is valid. No pagination; GET does not commit; projection/query failures roll back and return safe 500.
- API #60 route is POST /api/v1/mentor/support/{request_id}/reply. Strict required body is message:string and attachment_refs:string; attachment_refs contains JSON for unique signed-int64 upload IDs, with "[]" for no attachments. Blank-only message is invalid; source does not define a maximum and stores original text. Uploads must match Mentor, course, LECTURE purpose and UPLOADED state. Message and ordered links commit atomically after full-thread response validation. Returns full updated SupportRequest. No idempotency key; source permits reply on RESOLVED/CANCELLED and preserves status. Framework body validation may return 422 before view auth.
- API #61 route is PATCH /api/v1/mentor/support/{request_id}/resolve with no body/query. Active fallback states OPEN, IN_PROGRESS, WAITING_LEARNER transition to RESOLVED; RESOLVED is idempotent; CANCELLED/unsupported state returns 422. It does not enforce minimum messages or learner satisfaction. It reloads/returns full thread and commits after validation; failure rolls back.
- API #59/#60/#61 response is a singleton SupportRequest with student summary, status, full messages and attachment metadata. Null optional fields may be excluded. #59 invalid path maps to 404 while #60/#61 invalid path maps to 422.
- AC-24 says resolve when the learner is satisfied, otherwise keep OPEN; mockup says resolve unlocks after one valid exchange. #61 allows three active statuses and has no message minimum/confirmation input. #60 post-resolve reply behavior conflicts with a likely locked UI assumption.
- Historical API test reports use fake DB sessions. Tests and runtime were not run for this docs task; they do not prove live migration/deployment.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #59–#61 source/contract | Local route/module/query/model/test source and API DD packages; DDs remain Draft, fallback schema/lifecycle DERIVED. | R local source; contract/live DB unverified | Do not leave ME-12 classified D, but do not claim deployed behavior. |
| ME-11 handoff | Expected #58 data[].id and proposed numeric requestId route; frontend has no route. | EXPECTED only | Verify route ID equals #59 response id; UI wiring absent. |
| Empty/loading display | Static “Đang nạp...” ID and empty thread; AC-24 precondition says request exists. | DISCREPANCY | Distinguish loading, valid messages:[], not-found and forbidden. |
| Reply policy | Mockup 2000 counter; #60 source has no maximum, attachment picker absent, post-resolved replies allowed, no idempotency. | BLOCKED | Limit, attachment UI and lifecycle need product/API decision. |
| Resolve policy | Mockup minimum-one-exchange gate; AC satisfaction; #61 lacks minimum-message/confirmation input. | BLOCKED | Keep resolution unavailable until gate/confirmation is approved. |
| Prototype claims | Socket/TLS 1.3, SLA, settlement, survey, source/privacy statements lack API evidence. | UNVERIFIED | Do not document as implemented behavior. |
| Runtime/schema | Study Web registered UNWIRED; migration 008 is local; no live deployment evidence. | UNWIRED / NOT VERIFIED | No runtime verification claim. |

## CHANGES

- Created ME-12_PLAN.md before marker map/overlay/annotated image/DD; final plan status records that plan actions executed while DD remains blocked.
- Created ME-12_markers.json with 43 sequential elements, ME-12_markers.svg and screen_annotated.png at 3200×3170; source image remains 1600×1585.
- Created ME-12.md with A–F, 43 element rows, events E01–E06, API/data/error/state mapping and open decisions.
- Updated apps/study-client/docs/list_screen.md: ME-12 screen dependency D→R based on local #59–#61 source, refreshed blockers, reverse API #59–#61 classifications D→R, aggregate screen classification D:72, M:1, R:9, S:1.
- Updated apps/study-client/docs/screen_stitch/dd_screens/PLAN.md: ME-12 row and checkpoint; 47/83 core artifact sets present, 36 missing at least one.
- No API implementation, API DD, .agents context page, original screen.png or code.html was modified.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 + selected-file review | Selected and read the three exact-type docs worklogs; no shortage. | VERIFIED |
| Static asset audit | screen.png and code.html hashes match pre-work values; dimensions are 1600×1585 and annotated output 3200×3170. | VERIFIED |
| Marker/DD audit | 43 IDs sequential, unique and in-bounds; SVG groups/text ordered 1–43; DD section C has 43 rows matching JSON IDs; A–F present; six event headings E01–E06. | VERIFIED |
| Visual inspection | Annotated image inspected at full resolution; labels legible, controls/text not obscured. | VERIFIED |
| Source paths / context | API route/modules/tests, AC, ME-11 DD, migration 008 and context manifest checked. | VERIFIED |
| Tests/runtime | Not run; docs task, and no runtime is wired. | NOT_RUN |
| git diff --check / relative links / tracker consistency | Static audit passed: no changed-line whitespace errors; relative links resolve; inventory classifications and aggregate counts match; 47/83 core artifact sets. | VERIFIED |

## HANDOFF

- Remaining blockers: loaded-thread/layout/scale; reply max-length/count rule; attachment UI and purpose; resolve minimum exchange/satisfaction confirmation; post-resolve/cancelled reply policy; POST ambiguity/refetch strategy; static SLA/realtime/settlement/survey claims; navigation destinations; API DD approval/live DB; Study Web wiring.
- Next action: final static audit passed; stop this session at ME-12.
- Next Mentor Screen ID for a separate session: ME-13.
