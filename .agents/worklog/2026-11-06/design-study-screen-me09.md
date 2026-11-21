---
task_id: "2026-11-06-design-study-screen-me09"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-09 GET API #54 returns a submission collection; selecting data.items[].id links to ME-10 GET #55; API #54 ownership and response schema are server-owned"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-09

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs selected of 195 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve source assets; separate expected catalog behavior from current API/UI; Study Web remains UNWIRED; test source and checked-in DDL are not screen runtime proof.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: One Screen ID per session; preserve screenshot/HTML disagreement; trace API caller through query and response; record unsupported fields and filters instead of assuming UI behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: UI-only DD has no canonical skill; Study Web has no editable app/router; keep source-backed server behavior distinct from UI runtime and unresolved API DD decisions.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-09 only in this session. The active goal objective requires a per-screen plan before screen DD/annotation work, an ordered marker map, source-traced DD, and tracker/worklog updates; preserve original `screen.png` and `code.html`.
- Inventory: `apps/study-client/docs/list_screen.md` row 49 specifies Mentor route `/mentor/submissions`, AC-23, API #54, course/status filters, a list of submissions with deadline/owner, and a click using `submission_id` to ME-10. UI states are loading/empty/ready/error. It explicitly says not to assert a `Page` response while the contract says `Submission`, and marks response cardinality as blocked.
- Cross-screen flow: F09 links ME-09 API #54 to ME-10 API #55; ME-10 then calls #56 grade and #57 feedback as separate mutations. ME-09 must pass the selected identifier to the proposed route `/mentor/submissions/:submissionId`; no #55/#56/#57 action occurs on this screen.
- Skill routing: `.agents/context-manifest.json` excludes `web-ui-only-dd` from `createDD-markdown`; no canonical screen-DD skill is registered.

## CURRENT_BEHAVIOR

- Screen assets: folder initially contained only `screen.png` (1600×1280, SHA-256 `cc69bf224b53dc95a7900800d16bb626d2bd956d3cf8474db3adb68d3db9f18f`) and `code.html` (SHA-256 `9127d4ce896dbb1347f5ae55c3cf616d9fc5c4bdc351a4f88b8d258e7f320cc8`). Screenshot is a Mentor empty-state view with course/status/search controls and a refresh action. HTML has the same empty-state structure, static course/status options, and no result rows/table.
- Prototype behavior: HTML resets three controls locally. Its refresh handler only animates/disables the button for 750 ms; select/search fields have no data-load or filtering handlers. Header, notification, profile and footer anchors use `href="#"`. The page claims automatic sync, a 48-hour Mentor deadline, standard rubrics and training support; these are visible copy, not source-backed behavior. No API call is made by the HTML.
- Study Web: current context and source inventory show docs/assets and ignored `dist`, but no editable source, package manifest, feature router or ME-09 route. Runtime is `UNWIRED` and not verified.
- API #54 source: `apps/study-server/app/api/v1.py` registers GET `/api/v1/mentor/submissions`. Route inputs are optional positive signed-int64 `course_id`, optional exact `status:string`, and `page` default 1 constrained to positive signed-int32. View authenticates MENTOR before DB reads, scopes count/list to `courses.mentor_id = numeric JWT sub`, optionally owner-checks a supplied course, uses exact course/status predicates, fixed page size 20 and `submitted_at DESC, id DESC`, and returns `ApiEnvelope<Page<Submission>>` with `data.items` and `data.pagination`. Empty/missing-course results return HTTP 200 empty Page; wrong course owner returns 403. Query/mapping failures return 500. FastAPI query constraints produce 422. Source has no 409 branch.
- API contract status: `AC_03_MENTOR_TEACHING.drawio` now declares `ApiEnvelope<Page<Submission>>`; API #54 DD says this collection interpretation was DERIVED for AC-23 and its status remains `Draft — Needs Confirmation`. `list_screen.md` still describes the earlier singular contract. API #54 open questions still include file URL producer #35, assigned-Mentor access, status lifecycle/409, nullability/timestamp/live schema, and 422/409 contract confirmation.
- Tests/schema: focused API #54 test source covers auth, direct-owner denial, filters/pagination/order, empty results, constrained upload matching, malformed projection, database errors, query bounds and OpenAPI. Existing context reports 12 focused tests and historical branch-backed HTTP checks; tests are not being run in this screen-doc task. Checked-in DDL and fake rows do not prove live production schema or deployment.

## SOURCE_TRACE

- Expected screen flow: inventory ME-09/F09 and AC-23 list → select a submission → ME-10 GET #55 by path `submission_id`; grade #56 and feedback #57 are separate later actions. ME-09 itself uses only read API #54.
- Route: `apps/study-server/app/api/v1.py` registers `GET /api/v1/mentor/submissions`, binds optional positive signed-int64 `course_id`, exact string `status`, and positive signed-int32 `page` defaulting to 1, then constructs `MentorSubmissionsQuery` and calls `get_mentor_submissions`.
- Auth/access: `view.get_mentor_submissions` calls `validate_current_user_request(..., role="MENTOR")` before DB access. Optional `course_id` is checked via `FIND_MENTOR_COURSE`; a found course with different `mentor_id` returns 403. Count/list are always scoped to authenticated numeric `mentor_id`; a missing course proceeds to an empty result.
- Query/effects: `COUNT_MENTOR_SUBMISSIONS` and `LIST_MENTOR_SUBMISSIONS` read candidate `assignment_submissions` joined to `assignments`, `courses`, and `users`. Both apply identical optional course/status filters. List order is `submitted_at DESC, id DESC`, limit is shared `DEFAULT_SIZE=20`, offset is `(page-1)*20`. A LATERAL upload lookup matches exact `file_url`, `owner_id=user_id`, `purpose='SUBMISSION'`, and course; it returns at most one candidate asset. The endpoint is read-only and does not commit; failure paths safely rollback if needed.
- Mapping/response: `_map_submissions` maps `id`, assignment/user IDs, nullable content, `files[]`, status, timestamp, optional decimal-string score and feedback. `SubmissionPage` contains `items` and `pagination`; success response is HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with Page data, `{}` meta and trace ID. Empty results are 200 with empty items/zero totals. Auth errors are 401/403; query constraints are 422; query/projection failures are safe 500. Catalog 409 has no current source trigger.
- Downstream link: use source response `data.items[].id` for ME-10 path `submission_id`, but keep the inventory name/cardinality discrepancy visible. No UI route, client cache, auto-refresh or actual navigation is present.
- DDL/API DD: current DB/API DD describes legacy nullable assignment relationships, `file_url` relation as DERIVED, direct-owner access only, status lifecycle and timestamp questions. These are not live production schema facts.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ME-09 collection cardinality | `list_screen.md` still cites singular `Submission`; current route/model and AC diagram return `Page<Submission>`; API DD calls Page a DERIVED fallback and remains draft. | DISCREPANCY | Contract owner approval remains required; do not silently override the inventory. |
| Ready-state/list layout | Screenshot and HTML show empty state only; no submission-row layout. Inventory expects deadline/owner, while #54 response has no deadline/course title/student name and does not return `submission_id` by that key (identifier is `id`). | DESIGN GAP / BLOCKER | Need approved row fields/layout and route identifier mapping; do not invent deadline/owner values. |
| Filters/search | HTML uses static course IDs `all/fe/be/ux`, lower-case sample statuses `pending/graded/recheck`, and a search input. #54 expects numeric `course_id`, accepts exact string status without enum/normalization, and has no assignment-title search parameter. No UI handler calls API. | DISCREPANCY / IMPLEMENTATION BLOCKED | Course source, status map, unsupported search behavior and which values are valid need product/API confirmation. |
| Empty-state claims/actions | Copy claims live auto-sync, 48-hour SLA, standard rubric and support contact; refresh is a 750ms local animation with no fetch. #54 does not expose deadline or rubric. | UNSOURCED / UNWIRED | Treat as design copy only; no runtime promises or unsupported data mapping. |
| Study Web screen runtime | No editable frontend source/router/package is present. | UNWIRED / RUNTIME NOT VERIFIED | No screen behavior can be runtime verified from this checkout. |

## CHANGES

- Created `apps/study-client/docs/screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_PLAN.md` before marker/DD authoring.
- Created ME-09 DD, 27-marker JSON map, matching SVG overlay and 2× `screen_annotated.png`; original `screen.png`/`code.html` were not edited.
- Updated `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` ME-09 row and current artifact-count checkpoint (43/83).
- Updated this worklog with preflight, expected/current evidence, source trace, audit and handoff.
- Context pages/manifest were not changed. No API/backend source changed.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Mandatory preflight | Selector returned READY with 3 exact-type docs worklogs of 195 and no shortage; GS-01, GS-02 and GS-03 were individually read. | VERIFIED |
| Source trace | Current API #54 route, model, view, SQL, response, #54 test source, AC-23 and API #54 DD/open questions reviewed. | VERIFIED_STATIC |
| Preserved source assets | `screen.png` SHA-256 `cc69bf224b53dc95a7900800d16bb626d2bd956d3cf8474db3adb68d3db9f18f`; `code.html` SHA-256 `9127d4ce896dbb1347f5ae55c3cf616d9fc5c4bdc351a4f88b8d258e7f320cc8`; unchanged after authoring. | VERIFIED |
| Image artifacts | Source 1600×1280; annotated 3200×2560. Full annotated image was viewed. Marker #4 moved below active nav; marker #22 moved above rubric claim to avoid covering the control/copy. | VERIFIED |
| Marker map | 27 markers numbered 1–27; unique IDs; all centers in source bounds; SVG has 27 matching groups/circles/text; DD has 27 matching element rows. | VERIFIED |
| DD structure/events/links | Sections A–F present; 9 sequential event sections; relative Markdown links resolve. | VERIFIED |
| Tracker/worklog | ME-09 row has separate DD/implementation/runtime status; artifact checkpoint recounts 43/83. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| API tests / screen runtime / live DB | Not run in this docs task; no current Study Web route to execute. | NOT_RUN / NOT_VERIFIED |
| Context validator | No `.agents/` context page or registry changed. | NOT_REQUIRED |

Final post-authoring audit was repeated after the last DD wording/link adjustment; the source hashes, dimensions, marker map, event IDs, relative links, 83-screen inventory, 43/83 artifact count and `git diff --check` all passed.

## HANDOFF

- ME-09 status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Remaining blockers: API #54 cardinality approval (`Page<Submission>` current vs inventory's singular note; API DD still Draft); approved loaded-row layout and deadline/owner/title fields; course option source/status enum/default/search and page controls; unsupported autosync/48h/rubric/support copy; API #54 open schema/access/file/status/error questions; Study Web source/router absent.
- Next Mentor Screen ID: **ME-10**, in a separate session. This session did not author or edit ME-10 artifacts.
