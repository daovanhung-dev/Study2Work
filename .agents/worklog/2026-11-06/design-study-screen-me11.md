---
task_id: "2026-11-06-design-study-screen-me11"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-11 inbox depends on current Study Server API #58; course filter options and request-row handoff to ME-12 must match the Mentor course/API and support contracts"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-11

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 worklogs of 198 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected requirements separate from current API/UI source; preserve original assets; Study Web remains UNWIRED; fake-session tests do not prove live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Record screenshot/HTML divergence, unsupported filters and route behavior explicitly; do not treat prototype handlers or sample data as runtime.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Trace each API route/view/query/DB effect/response; keep unavailable contracts and linked-screen handoffs explicit; one Screen ID per session.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-11 only in this session; write its plan before marker map, annotation and DD; preserve source assets; map every visible element to sequential markers and DD rows; detail events, states, APIs and navigation; update the tracker and this worklog.
- Inventory: ME-11 is the Mentor support inbox at proposed `/mentor/support`, AC-24, API #58. Expected controls include status tabs and a course filter; expected states include loading/empty/ready/error; selecting a request continues to ME-12.
- Cross-screen flow: `ME-01 → ME-11 (#58) → ME-12 (#59 detail → #60 reply → #61 resolve)`. The selected request ID must hand off to ME-12; ME-11 must not perform reply/resolve mutations.
- UC/AC: `docs/diagrams/UC_UNICA.drawio` identifies UC24 “Hỗ trợ học viên” with actor Mentor. AC-24’s precondition says the Mentor has a support request in their responsibility scope; its flow starts with #58 and continues to request detail/reply/conditional resolve. The empty-state screenshot/inventory conflict with that precondition and needs a decision.
- API catalog #58 declares optional `course_id` and `status`, Mentor Bearer access, `SupportRequest[]`, and 200/401/403/422/500. API DD #58 remains `Draft — Needs Confirmation`; its local fallback choices are not approved production contract.
- UI-only skill routing: the machine registry marks `createDD-markdown` as Web/API DD and explicitly excludes `web-ui-only-dd`; no canonical UI-only screen DD skill applies.

## CURRENT_BEHAVIOR

- Assets: At session start the ME-11 folder contained only `screen.png` (1600×1425, SHA-256 `2cbdc3691a241ee755ce6f422768472c943ddb352554f9ed9159df1cd5105272`) and `code.html` (SHA-256 `54536f7794787f3c93772c54805c42712f2339434a4c7f58fd3611925b64b2d5`). The screenshot is an empty inbox with three status tabs, a course selector, refresh control, SLA/realtime claims, three guidance cards and footer links.
- Prototype HTML: Header/footer anchors use `href="#"`. Status-tab clicks update `aria-selected`/CSS classes only; they do not filter records or update counts. The course select has no change handler and hard-coded slug values (`all`, `fe-adv`, `be-node`, `fullstack-capstone`) rather than #58’s positive-int64 course IDs. Refresh performs a local 650ms spinner/disable cycle and writes a browser clock value to `lastUpdatedTime`; no application API request, polling, push, or realtime listener exists. The HTML references Tailwind CDN and Google Fonts, which are design dependencies, not Study Web runtime wiring.
- Study Web: current checkout has no editable application source/package/router; frontend is `UNWIRED`. No ME-11 route, auth provider or client API integration is verified.
- API #58 source: registered `GET /api/v1/mentor/support/requests`; FastAPI validates `course_id` as optional positive int64, while `status` is any optional string. The view applies shared MENTOR Bearer/JWT guard before DB access; if `course_id` exists but belongs to another Mentor it returns 403; a nonexistent course yields an empty collection. Query uses exact AND filters, direct `courses.mentor_id` ownership, stable request order `created_at DESC, id DESC`, then bulk-loads all messages ordered by `created_at ASC, id ASC` and matching uploaded assets. No page/size, status counts, last-updated field, course title, student contact field, unread flag or SLA deadline is returned. Unknown status strings are exact-match filters and return `[]` rather than validation errors. GET is read-only and does not commit.
- Response projection: each request has `id`, `course_id`, `student{id,full_name,avatar_url?}`, `status`, complete `messages[]`, `created_at`, and `resolved_at?`; messages include author summary, content, attachments[] and created_at. Attachments are returned only when linked upload ID, author, course, role-specific purpose and `UPLOADED` status match. Null optional fields are omitted. Response `data` is an array, `meta` is empty, and success is 200 `DESIGN_RESOURCE_RETRIEVED`.
- Database: checked-in `infra/postgres/study-server/DB.sql` and migration `008_support_requests.sql` both contain BIGINT `support_requests`, `support_messages`, and `support_message_uploads`; their tables/status values are a DERIVED local fallback. This disproves the ME-11 inventory note that the support table is absent from `DB.sql`. The live schema and migration deployment remain unverified; the separate V1-PILOT UUID design is not the current #58 query target.
- Tests: focused test source exists and `.agents/server-study/tests.md` records 12 historical #58 passes. Tests use fake sessions/rows and do not verify live schema or migration deployment. No tests were run in this docs session.

## SOURCE_TRACE

Expected: ME-01 support navigation → proposed `/mentor/support` → GET #58 with optional course/status filter → list request IDs → open selected request in proposed ME-12 route. ME-12, not this screen, owns #59 detail, #60 reply and #61 resolve.

Current: `apps/study-server/app/api/v1.py` route → `get_mentor_support_requests` → shared `validate_current_user_request(role="MENTOR")` → optional direct-course ownership query → `LIST_MENTOR_SUPPORT_REQUESTS` → if nonempty, `LIST_MENTOR_SUPPORT_MESSAGES` → `_map_requests` / `_append_messages` / response model validation → success envelope. Database errors, invalid projection and broken attachment links roll back the read transaction and return safe 500; successful GET does not commit. Query `course_id` validation is performed by FastAPI route parameters before the route function invokes the view-level auth guard, so invalid course input can produce 422 before 401/403; the catalog does not state precedence and tests do not establish unauthenticated-invalid-query behavior.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Inventory schema/status note | Inventory says SupportRequest is absent from `DB.sql` and marks #58 `D`; current #58 route/test source plus candidate `DB.sql` and migration 008 exist. | STALE INVENTORY / DISCREPANCY | Correct ME-11/#58 source classification; keep live schema/deployment unverified. |
| Empty-state precondition | AC-24 says Mentor has an in-scope request; screenshot and inventory include an empty inbox. | DISCREPANCY | Confirm whether empty state is valid outside AC-24’s precondition or whether the precondition is only for the reply flow. |
| Loaded list design | Screenshot and HTML provide only the empty state; no request-row/card structure or loaded-state interaction is present. | DESIGN GAP / BLOCKED | Do not invent a loaded row, ordering label or list-page presentation; DD remains blocked until visual/field presentation is confirmed. |
| Course filter | HTML uses static slugs, while #58 requires positive int64 `course_id`; #58 returns only course_id. Existing #46 could provide Mentor courses but is not listed for ME-11. | CONTRACT GAP | Confirm course-option source/ID mapping; do not send placeholder slugs. |
| Status tabs/counts | #58 accepts exact optional status strings but does not enumerate status counts; DDL candidate lists five statuses, while screenshot has All/Open/Resolved tabs only. | CONTRACT GAP | Define whether “Open” groups OPEN/IN_PROGRESS/WAITING_LEARNER, how CANCELLED is shown, and count source. |
| API response grain | #58 returns every matching request plus full messages and attachments, with no pagination. #59 reloads full thread on detail. | DERIVED / PERFORMANCE RISK | Preserve current response evidence; decide list payload/pagination before claiming scalable inbox behavior. |
| SLA/realtime/guidance claims | Screenshot shows <4-hour SLA, immediate/automatic notifications, standard replies and Google Meet help; #58 has no SLA/realtime/count/template field and HTML has no service calls. | UNSUPPORTED DESIGN CLAIMS | Confirm or remove claims/links before implementation. |
| Student request producer | Current route inventory/source has Mentor reads/reply/resolve but no Student support-request creation endpoint. | NOT_FOUND / SYSTEM BLOCKER | Existing UI may display seeded/externally created rows only; no Student CTA/creation flow can be asserted. |
| Study Web runtime | No editable Study Web source/package/router; HTML is only a prototype. | UNWIRED | No client interaction, route, auth or runtime behavior can be marked verified. |

## CHANGES

- Added `apps/study-client/docs/screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11_PLAN.md` before marker/DD authoring; plan status is now COMPLETE.
- Added `ME-11_markers.json` (33 sequential IDs), `ME-11_markers_overlay.svg`, `screen_annotated.png` (3200×2850), and `ME-11.md` (A–F, six events, #58 source trace).
- Updated ME-11 row and API #58 source status in `apps/study-client/docs/list_screen.md`; removed the stale “SupportRequest table absent” statement, refreshed the local DB/API overview claims against current source, and adjusted the dependency classification aggregate from D:74/R:7 to D:73/R:8.
- Updated ME-11 row and progress checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; current four-core artifact count is 46/83.
- Source assets were preserved: `screen.png` SHA-256 `2cbdc3691a241ee755ce6f422768472c943ddb352554f9ed9159df1cd5105272`; `code.html` SHA-256 `54536f7794787f3c93772c54805c42712f2339434a4c7f58fd3611925b64b2d5`.
- CONTEXT_UPDATES: none; existing Web/Study Server context correctly marks Study Web unwired, support tables as a local fallback and live schema as unverified.
- Assumptions: none; candidate use of API #46 for course options remains an open decision, not a wired screen dependency.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Three exact-type docs worklogs selected and read; no shortage. | VERIFIED |
| ME-11 source/API/DB review | Inventory/AC/UC, screenshot/HTML, #58 route/view/query/models/tests/API DD, support DDL/migration and cross-screen route list read. | VERIFIED |
| Marker/image/link/content audit | 33 JSON/SVG markers sequential, unique, in-bounds and matched 1:1 to DD rows; six event IDs; annotated image is 3200×2850; local links resolve; original asset hashes unchanged. | VERIFIED |
| Inventory/artifact audit | 83 screen directories; 46/83 have the four core artifacts; ME-11 and #58 tracker rows updated. | VERIFIED |
| `git diff --check` | No whitespace errors in diff. The broader whole-file scan noticed an existing trailing space at `list_screen.md:3`; that line is unchanged, and all edited/new lines are clean. | VERIFIED |
| Tests/runtime | Not run for this docs task. | NOT_RUN |

## HANDOFF

- Remaining blockers: loaded-row design, empty-state/AC precondition, status mapping/counts, course-option source, unsupported SLA/realtime/canned-answer/meeting claims, Student request producer, API #58 derived projection approval, and live schema/deployment.
- Final screen status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next screen in Mentor flow: ME-12, in a separate session. No other Screen ID was started.
