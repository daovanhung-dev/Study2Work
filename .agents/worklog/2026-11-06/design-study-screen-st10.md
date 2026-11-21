---
task_id: "2026-11-06-design-study-screen-st10"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-09 course overview to ST-10 lesson access/start handoff; APIs #22/#23/#24; downstream ST-11 lesson player; Study Web route/auth boundary"]
status: "PARTIAL"
---

# Worklog: Detailed Design màn hình Study ST-10

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; 3 exact-type docs worklogs of 171 selected; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-gs01.md
    - carry_forward: Separate expected from current UI/API behavior; Study Web feature routes are UNWIRED; preserve source assets and do not invent unsupported navigation or data.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs02.md
    - carry_forward: Trace backend source independently from catalog, record route/field discrepancies, and do not treat mockup interactions or API declarations as runtime.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs03.md
    - carry_forward: One Screen ID per session; distinguish source-backed APIs from DECLARED_NOT_RUNNABLE operations; preserve expected/current behavior and security blockers.
- shortage: none

## EXPECTED_BEHAVIOR

- User objective read this turn from /home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md. Per-screen requirements: one Screen ID per session; plan before DD/annotation; preserve screen.png; create ordered marker map/annotated image and source-traced DD; update tracker/worklog; separate DD READY, IMPLEMENTATION BLOCKED and RUNTIME VERIFIED.
- Current expected inventory: ST-10 route /student/lessons/:lessonId/start, Student actor, AC-14, APIs #22/#23/#24, links ST-09/ST-11, states checking/denied/started/failure. Sequence is GET #22; if allowed POST #23 (anti-repeat intent); GET #24; then ST-11. If denied, do not call #24 or play media.
- AC-14 says Student enrolled in the course containing lesson; AC-15 says Student has lesson-view permission. API catalog declares Bearer JWT / Student and path lesson_id:int64! for #22–#24. Contracts and API DDs remain Draft.
- Skill registry confirms createDD-markdown excludes web-ui-only-dd; no canonical UI-only screen DD skill is registered.

## CURRENT_BEHAVIOR

- Source/config: ST-10 folder initially contained only screen.png (1566×1600, SHA256 5d1386bbeba8a21d2ee48cc4b62099cdd6fab3a0d3e0d96b2bc24f3133e840ce) and code.html (SHA256 87178684dcd4dd6f4ca47fa3ed26ff63823616d84ca402015aa72a190d431b87). HTML is static; all anchors use href=#, no router/fetch/product handlers; Start button is disabled and aria-disabled=true. It shows 423_LOCKED, gate progress 2/5, a “Session Token” message, and static checking/denied/started cards. No lessonId is bound.
- Study Web: editable source/package/router absent; ignored dist has only root route /. No current ST-10 runtime route.
- Study Server: exact route/module/query/test search found no Student API #22/#23/#24. Current Admin lesson routes (#83–#86) are under /api/v1/admin/lessons and use ADMIN; they do not implement the Student endpoints.
- API declarations/DDs: #22 GET /api/v1/lessons/{lesson_id}/access; #23 POST /api/v1/lessons/{lesson_id}/start; #24 GET /api/v1/lessons/{lesson_id}. All require Student Bearer JWT/int64 path and have Draft — Needs Confirmation DDs. #22 response ApiEnvelope<Lesson> cannot express allow/reason; #23 catalog says 201 ApiEnvelope<Lesson> while AC says UPSERT progress IN_PROGRESS; #24 Lesson fields include optional content/video_url, but access/publish predicates and projection are open.
- Access contract open questions: enrollment status/prerequisite predicate; JWT identity binding; 403 reason wire shape; 404 visibility/resource semantics; query/projection/live schema.
- Start contract open questions: unique key for UPSERT; update/preserve fields and repeated starts; idempotency vs 201; response assembly; direct-call authorization; 404/422; transaction/failure/live schema.
- Content contract open questions: direct-call entitlement/JWT binding; lesson/course publication scope; 403/404 and error payload; projection/schema; nullable serialization/status enum; path validation.
- DB evidence: DB.sql is checked-in candidate, not live schema. lessons.course_id is nullable in DDL despite design/catalog requiring it; lesson_progress has candidate status/progress_percent/last_accessed_at/completed_at but no unique(user_id, lesson_id) constraint. Candidate enrollment status enum/eligibility and live deployment are unverified.
- Tests: no API #22/#23/#24-specific test source found; test suites were not run.
- Current upstream: ST-09 design has no lesson list/selection and its CTA does not supply lessonId, so current assets do not provide ST-10 route input.

## SOURCE_TRACE

- Expected route: ST-09 lesson selection → ST-10 route/lessonId → access #22 → conditional start #23 → content #24 → ST-11. Current ST-09 asset has no selected lessonId handoff.
- Current client: apps/study-client has no editable router/source; the screenshot/HTML is a static prototype with placeholder navigation and a disabled start button.
- API declarations: catalog/list_screen → API #22/#23/#24 Draft folders and OPEN_QUESTIONS; no runtime implementation.
- Current Study router search shows Admin lesson detail routes only under /api/v1/admin/lessons/{lesson_id}; corresponding tests cover APIs #82–#86, not the Student lesson endpoints.
- API #23 candidate side effect per AC-14: UPSERT lesson_progress state IN_PROGRESS. Checked-in DDL candidate has no unique key on user_id/lesson_id; no API implementation/query proves transaction or retry behavior.
- API #24 expected data per catalog: Lesson fields; no current Student read path. Checked-in DB.sql is candidate only; lesson.course_id nullability conflicts with required response/design mapping.
- API #22 access result and 403 reason: declared envelope/code only; AC diagram reason shape not present in reusable error schema.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST-10 UI | Complete static gated mockup; status 423_LOCKED and token copy are not catalogued; button permanently disabled. | DISCREPANCY | Do not claim runtime 423 or token issuance; UI does not implement expected checking/started flow. |
| Upstream lessonId | ST-09 asset has no lesson list or lesson selection; CTA contains no ID. | UNWIRED / DESIGN GAP | ST-10 route input cannot be produced from current preceding design. |
| APIs #22–#24 | Catalog and API DD Draft exist; no Student route/module/query/test source. | DECLARED_NOT_RUNNABLE / NOT_FOUND | Screen calls are design-only. |
| #22 allow/reason response | Catalog success type Lesson; access boolean/reason not modeled; AC says 403 plus reason but payload is unspecified. | DISCREPANCY / OPEN | HTTP status can signal expected allow/denied branches (200 vs 403), but exact predicate and denied reason payload/message remain unresolved. |
| #23 repeated start | AC says UPSERT IN_PROGRESS and inventory expects anti-repeat; catalog says 201 Created; unique key/field updates/repeat semantics unresolved. | DISCREPANCY / OPEN | Retry/dedup and state preservation cannot be specified. |
| #23 trigger | Inventory orders #23 after #22 allowed but does not state auto-start vs user submit; mockup Start button is disabled. | OPEN | Do not choose a trigger or enable rule without product decision. |
| #24 protected content | Catalog returns Lesson with optional content/video_url; access, publish, projection and direct-call authorization unresolved. | SECURITY BLOCKER | Prior #22 client call does not prove #24 server-side protection; current #09 public projection is not a substitute. |
| Candidate DB | Checked-in DDL is not live schema; course_id nullability mismatch; progress uniqueness missing. | DESIGN_ONLY / DISCREPANCY | Do not derive query/upsert/live behavior from candidate schema. |
| Study Web wiring | Editable app source/router absent; ignored dist only has /. | UNWIRED | Runtime, auth, route and navigation cannot be verified. |

## CHANGES

- Files changed: this worklog; `apps/study-client/docs/screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_PLAN.md`, `ST-10.md`, `ST-10_markers.json`, `ST-10_markers_overlay.svg`, `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`. Original `screen.png` and `code.html` were preserved.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; unresolved product/API decisions remain explicitly open.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Objective + docs worklog preflight | Objective read; selector and all selected exact-type worklogs completed. | VERIFIED |
| ST-10 static audit | 21 ordered unique markers; 21 DD element rows map to marker IDs; 10 event headings; 21 SVG circles; source PNG 1566×1600 and annotated PNG 3372×3200; local DD links resolve; source PNG/HTML SHA-256 match baseline. | VERIFIED |
| Visual review | Annotated image inspected; markers remain in side gutters and do not cover the source content. | VERIFIED |
| `git diff --check` + whitespace audit | `git diff --check` exited 0; custom audit found no trailing whitespace in changed text/config files. | VERIFIED |
| Tests/runtime | Not requested; no suites or runtime calls run. | NOT_RUN |

## HANDOFF

- Remaining blockers: access predicate/JWT/reason and 404 semantics for #22; #23 trigger, upsert key/idempotency/field updates/transaction; #24 direct authorization/publish/projection/null behavior; missing ST-09 lessonId handoff; Study Web route/auth wiring; unresolved static 423/token/permanent-lock claims; ST-11 ownership of the #24 read. DD BLOCKED; implementation BLOCKED; runtime NOT VERIFIED.
- Next owner/action: ST-10 static audit is complete; the next independent session may start ST-11. Do not add another Screen ID in this session.

