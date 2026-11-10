---
task_id: "2026-11-06-design-study-screen-st17"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-17 and API #33 result data; ST-17 → ST-18 submission handoff; ST-09 course context"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-17

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 selected of 178 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Separate expected design from current UI/API evidence; preserve source assets; fake-session tests and design guide are not runtime proof; keep Study Web `UNWIRED` explicit.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace current API validation/query/response independently from catalog; document screenshot/HTML mismatches and unsupported fields/actions without inventing behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Verify API route/module/test presence per dependency; preserve AC-vs-inventory discrepancies; UI route and backend source statuses are separate.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Goal objective reread from `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; this session processes ST-17 only, creates its plan before DD/annotation changes, preserves originals, documents element/event/state/API traceability, updates the master tracker/worklog, and keeps DD/implementation/runtime status distinct.
- Inventory row: ST-17 — Chi tiết bài tập (Page), actor Student, proposed route `/student/assignments/:assignmentId`, AC-17, API #33, linked ST-18 and ST-09, states `loading/open/closed/not-found`. Expected flow is GET #33 and server-side deadline/permission enforcement; UI clock is not the sole source of deadline truth.
- API catalog #33: `GET /api/v1/assignments/{assignment_id}`, Student Bearer JWT, required `assignment_id:int64` path only, no query/body; `ApiEnvelope<Assignment>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500. Logical `Assignment` fields: `id`, `course_id`, `title`, optional `description`, optional `due_at`, required decimal-string `max_score`.
- AC-17 expects assignment read + submission rule, then a permission/deadline decision; if allowed it proceeds to input/file selection, #34 upload, #35 create submission and #36 read confirmation. Its diagram says overdue/no permission → 403/409, while #33 catalog has no 409. ST-17 CTA should relate to ST-18 submission, but only as a proposed screen handoff; no current Study Web route exists.
- API #33 DD is `Draft — Needs Confirmation`; Q-33-01…05 leave assignment/course access and 403/404, deadline/read behavior and 403-vs-409, submission-rule schema, nullable/timestamp/decimal serialization, and path parsing/error mapping open. Do not add fields or codes.
- Skill registry: machine manifest excludes `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only DD skill is wired.

## CURRENT_BEHAVIOR

- `screen.png`: 667×1600 RGB; SHA-256 `7ac187345ca89ef08462767a6269e91af888944d4a8b76494896596e1f6c7c86`. It is a loaded Student assignment detail mockup with static project/status chips, title/description, progress and score, deadline/countdown, mentor/SLA, preview video, requirements, rubric, resource downloads, submission instructions, status/checklists, mentor contacts, submission history and footer. All concrete names, dates, scores, percentages, counts, URLs, contacts, and copy are design samples unless sourced by an approved contract.
- `code.html`: 9,745 bytes; SHA-256 `82de50d864c0be013a198358a1f41de72acf032d18add1107114eb07c76580f6`. It is a static Guest unavailable state with login/register header and a link to `/student/courses`; it has no assignment route hydration, API request, form, submission UI or own behavior script. It does not represent the loaded Student screenshot.
- Study Web current checkout is documented as `UNWIRED`: editable source/package manifest and Student routes are absent; ignored `dist` is not evidence of this route or deployment.
- API #33 is catalog/DD design only. Current `apps/study-server/app/api/v1.py`, `app/modules/`, `tests/` and declared-route inventory have no Student GET `/api/v1/assignments/{assignment_id}`, API #33 module or API #33 test. Current APIs #54–#57 are Mentor submission flows and do not implement the Student assignment-detail read. No API #33 runtime behavior is verified.
- Candidate `assignments` table in checked-in DDL has `id`, nullable `course_id`, `name`, nullable `description`, nullable `due_at TIMESTAMP`, nullable `max_score NUMERIC(6,2) DEFAULT 10`, timestamps. Logical `Assignment` requires `course_id` and `max_score`; DDL/table notes conflict. This is design evidence only, not live-schema evidence. No submission-rule, rubric, resource-list, video, progress, course title, mentor/SLA, or submission-history fields are in #33 `Assignment`.
- Tests were inspected by search/context only; no #33 test exists and no tests were run. No frontend/runtime or live DB check was run.

## SOURCE_TRACE

```text
Expected AC-17: ST-17 open → GET #33 → read Assignment/submission rule → permission/deadline decision
  → allowed: ST-18 input/file → #34 upload → #35 submit → #36 confirmation
  → denied/error: 403/409 branch (409 conflicts with #33 catalog)
Current source: no Student #33 route/module/test; no Study Web route; Mentor #54–#57 submissions are separate actor/operations.
```

- `apps/study-client/docs/list_screen.md` ST-17 row supplies proposed route, actor, AC/API, linked ST-18/ST-09 and expected states; ST-18 row supplies the related submission screen/route. These are design inventory entries, not runtime routes.
- `docs/lists/list_api.md` #33 defines GET path-only with Student Bearer, `ApiEnvelope<Assignment>`, and 200/401/403/404/500. Reusable schema contains only assignment identity/course/title/optional description/optional due time/maximum score; no submission rule or visible screenshot detail projection.
- AC-17 index and `AC_02_STUDENT_LEARNING.drawio` show: open assignment → GET #33 → read Assignment + submission rule → permission/deadline decision → input/file → #34 upload → storage → #35 submit → DB write → #36 confirmation → “Đã nộp”; negative branch from decision to error. AC-17 overdue/no-permission 403/409 conflicts with the #33 error set.
- API #33 DD files (`02_Overview`, `03_Request`, `04_Response`, `05_Data_Mapping`, `06_Error`, `OPEN_QUESTIONS`, `PLAN_RESULT`, `VERIFICATION_REPORT`) are Draft. Candidate query reads `assignments`; auth helper could return numeric Student identity but #33 does not call it. Access predicate, deadline enforcement, null/timestamp/decimal projection and path error behavior remain open.
- Current route/module/test search finds no Student `GET /api/v1/assignments/{assignment_id}` or `api_33` module/test. `declared-routes.md` shows only Mentor `/api/v1/mentor/submissions*` for current submission operations; modules #54–#57 authenticate Mentor and use assignment joins but are not Student #33.
- `infra/postgres/study-server/DB.sql` and `DB_UNICA_TABLES.md` are checked-in candidate schema; `assignments.name` maps to logical title in the API DD, but physical nullability/defaults conflict with the logical schema. No live schema verified.
- Manifest/skill registry exclude UI-only screen DD from `createDD-markdown`; this screen does not use the API DD authoring template.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST17-D01 screenshot/HTML | PNG is loaded Student assignment detail; HTML is Guest generic unavailable state with `/student/courses` link. | `DISCREPANCY` | Preserve both originals; neither proves runtime. |
| ST17-D02 Study Web route | Current Study Web has no editable app source/package/Student router; only ignored compiled root route is known. | `UNWIRED / NOT_FOUND` | No current ST-17 UI, navigation, event, or API call is verified. |
| ST17-D03 API #33 | Catalog and Draft API DD exist, but no Student route/module/test in current source. | `DESIGN_ONLY / NOT_FOUND / DECLARED_NOT_RUNNABLE` | Do not describe assignment data retrieval or permission enforcement as active. |
| ST17-D04 response coverage | `Assignment` only exposes six logical fields; screenshot adds course title, status/submitted state, weight/progress, rubric, resources/video, mentor/SLA, checklist and history. | `BLOCKER — response/source required` | Do not fabricate dashboard/rubric/resources/history or additional API calls. |
| ST17-D05 access/deadline | Q-33-01/02 leave assignment/course access, whether #33 rejects after deadline, boundary, and owner predicate open. | `BLOCKER — API #33 contract` | Server clock/policy must govern eligibility; client countdown is not authorization. |
| ST17-D06 error discrepancy | AC-17 uses 403/409 for overdue/no permission; API #33 catalog lists 401/403/404/500 only. | `DISCREPANCY` | Do not add 409 or choose mapping without contract resolution. |
| ST17-D07 schema/serialization | `course_id`/`max_score` are required logically but nullable in DDL; `due_at` has no timezone rule; null/decimal formatting open. | `DISCREPANCY / DESIGN_ONLY` | Response mapping is not implementable without owner/schema decision. |
| ST17-D08 checklist/resources/contact actions | Screenshot has checkboxes, resource/video actions, Discord/office-hours links; #33 and inventory provide no interaction/persistence/file/contact contract. | `DESIGN_ONLY / SOURCE_REQUIRED` | Keep as design-only; no side effect or route is assumed. |
| ST17-D09 submission handoff/state | ST-18 is linked and AC continues through #34–#36; ST-17 response has no submission status/ID/history. | `DESIGN_ONLY / OPEN` | CTA handoff may carry assignment ID to proposed ST-18; do not call #35/#36 or assert submitted state from #33. |

## CHANGES

- Created `ST-17_PLAN.md` before marker map, annotation and DD authoring, with 49 planned elements and seven event flows.
- Created `ST-17_markers.json`, `ST-17_markers_overlay.svg`, and `screen_annotated.png` with 49 ordered, non-overlapping gutter markers; original `screen.png` and `code.html` were preserved.
- Created `ST-17.md` with sections A–F, 49 element mappings, seven events, API/error/state/navigation/accessibility detail and explicit blockers.
- Updated the ST-17 master-tracker row/status, global artifact tally and next pointer to ST-18.
- CONTEXT_UPDATES: none; no source contract, code, schema or agent context page changed.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective and docs preflight | Objective reread; `node scripts/select-worklogs.mjs --type docs --limit 3` returned READY, 3/178 exact-type docs worklogs, and all three selected logs were read. | VERIFIED |
| Original assets | `screen.png` remains 667×1600, 8-bit RGB, SHA-256 `7ac187345ca89ef08462767a6269e91af888944d4a8b76494896596e1f6c7c86`; `code.html` remains 9,745 bytes, SHA-256 `82de50d864c0be013a198358a1f41de72acf032d18add1107114eb07c76580f6`. | VERIFIED |
| Marker map and DD | Static audit found markers #1–#49 in sequence, unique `ST17-EL-01`…`ST17-EL-49`, valid target/badge/gutter coordinates, no overlapping badges, and exact ordered match to all 49 DD rows. Seven event IDs are sequential. | VERIFIED |
| Annotation output | SVG parsed with 49 numeric labels; canvas is 859×1600 at 2× scale; `screen_annotated.png` is 1718×3200. The image was visually inspected; markers are legible in side gutters without covering screenshot content. | VERIFIED |
| Links and inventory | All local links in `ST-17.md` and `ST-17_PLAN.md` resolve. Inventory audit found 83 unique IDs/folders and 83 source PNG/HTML pairs; 27 complete six-file sets and 56 incomplete sets. ME-01 was counted from existing files only and was not reviewed in this ST-17 session; its separate mentor-scope next pointer ME-02 is preserved, while the W2 Student-flow pointer is ST-18. Tracker ST-17 status matches. | VERIFIED |
| Whitespace | Explicit scan of changed text files found no trailing whitespace; `git diff --check` reported no issue. | VERIFIED |
| Tests/runtime | No tests, frontend runtime or live database check was run; no runtime behavior is claimed. | NOT RUN |

## HANDOFF

- Remaining blockers: API #33 is `Draft — Needs Confirmation` with no current Student route/module/test; assignment/course access, deadline/read boundary, submission-rule schema, 403/409 discrepancy, path error mapping, optional serialization and candidate DDL nullability remain unresolved. The loaded Student screenshot contains many fields/actions absent from `Assignment`; the HTML is a Guest unavailable fallback; Study Web is `UNWIRED`.
- Next screen: ST-18, in a separate session. Do not process another Screen ID in this session.
